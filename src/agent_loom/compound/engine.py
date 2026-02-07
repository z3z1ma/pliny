from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.compound.compiler_instincts import (
    apply_instinct_candidates,
    parse_instinct_candidates,
)
from agent_loom.compound.compiler_skills import (
    apply_skill_candidates,
    parse_skill_candidates,
)
from agent_loom.compound.decisions import (
    build_decision,
    decision_path_for_id,
    write_decision,
)
from agent_loom.compound.docs import sync_instincts_markdown
from agent_loom.compound.episodes import (
    Episode,
    EpisodeGit,
    EpisodeObservation,
    EpisodeObservationCursor,
    build_episode,
    bounded_text,
    episode_path_for_id,
    load_episode,
    write_episode,
)
from agent_loom.compound.blobs import write_blob_text
from agent_loom.compound.instincts import load_instincts, save_instincts
from agent_loom.compound.observations import (
    count_observations,
    ingest_observations_since,
    observations_prefix_sha256,
)
from agent_loom.compound.paths import CompoundPaths, compound_paths
from agent_loom.compound.scaffold import require_scaffold_installed
from agent_loom.compound.state import CompoundState, load_state, save_state
from agent_loom.core.git import (
    git_checked,
    git_head_sha,
    git_is_dirty,
    git_merge_base,
    git_ref_exists,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _load_json_from_text(text: str) -> Dict[str, Any]:
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("proposals must be a JSON object")
    return parsed


def _default_base_ref(repo: Path) -> str:
    for ref in ["origin/main", "main", "origin/master", "master"]:
        if git_ref_exists(repo, ref):
            return ref
    return "HEAD"


def _git_diffstat(repo: Path, *, base_sha: str, head_sha: str, dirty: bool) -> str:
    if dirty:
        return git_checked(repo, ["diff", "--stat"]).strip()
    return git_checked(repo, ["diff", "--stat", f"{base_sha}..{head_sha}"]).strip()


def _git_patch(repo: Path, *, base_sha: str, head_sha: str, dirty: bool) -> str:
    if dirty:
        return git_checked(repo, ["diff"]).rstrip() + "\n"
    return git_checked(repo, ["diff", f"{base_sha}..{head_sha}"]).rstrip() + "\n"


def _git_changed_files(
    repo: Path, *, base_sha: str, head_sha: str, dirty: bool
) -> List[str]:
    raw = (
        git_checked(repo, ["diff", "--name-only"]).strip()
        if dirty
        else git_checked(
            repo, ["diff", "--name-only", f"{base_sha}..{head_sha}"]
        ).strip()
    )
    files = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    files = sorted(set(files))
    return files


def _state_path(paths: CompoundPaths) -> Path:
    return paths.compound_dir / "state.json"


def _episode_ts(existing: Optional[Episode]) -> str:
    if existing is not None and str(existing.created_at or "").strip():
        return str(existing.created_at).strip()
    return _now_iso()


@dataclass(frozen=True)
class CompoundRunResult:
    ok: bool
    repo: str
    episode_id: str
    episode_path: str
    episode_created: bool
    decision_id: str
    decision_path: str
    instincts_created: int
    instincts_updated: int
    skills_created: int
    skills_updated: int
    wrote_instincts: bool
    wrote_docs: bool
    state_updated: bool


def run_compound(
    *,
    root: Path,
    proposals_json: Optional[str] = None,
    auto: bool = False,
    no_ai: bool = False,
    dry_run: bool = False,
    mirror_claude: bool = True,
    max_patch_bytes: int = 150_000,
    min_new_observations: int = 12,
) -> CompoundRunResult:
    repo = root.resolve()
    require_scaffold_installed(repo)
    paths = compound_paths(repo)

    state_path = _state_path(paths)
    state = load_state(state_path)

    obs_prefix = observations_prefix_sha256(paths.observations_file)
    start_offset = int(state.observations_offset_bytes or 0)
    reset_detected = False
    if paths.observations_file.exists() and start_offset > 0:
        try:
            sz = int(paths.observations_file.stat().st_size)
        except Exception:
            sz = 0
        if sz < start_offset:
            reset_detected = True
        elif state.observations_prefix_sha256 and obs_prefix:
            if str(state.observations_prefix_sha256) != str(obs_prefix):
                reset_detected = True
    if reset_detected:
        start_offset = 0

    ingested = ingest_observations_since(
        paths.observations_file, start_offset_bytes=int(start_offset)
    )
    included = ingested.items
    new_obs = int(len(included))
    end_offset = int(ingested.end_offset_bytes)

    dirty = git_is_dirty(repo)
    head_sha = git_head_sha(repo)
    base_ref = _default_base_ref(repo)
    base_sha = (
        head_sha if base_ref == "HEAD" else git_merge_base(repo, base_ref, head_sha)
    )

    diffstat = _git_diffstat(repo, base_sha=base_sha, head_sha=head_sha, dirty=dirty)
    if auto and proposals_json is None and not diffstat.strip():
        return CompoundRunResult(
            ok=True,
            repo=str(repo),
            episode_id="",
            episode_path="",
            episode_created=False,
            decision_id="",
            decision_path="",
            instincts_created=0,
            instincts_updated=0,
            skills_created=0,
            skills_updated=0,
            wrote_instincts=False,
            wrote_docs=False,
            state_updated=False,
        )

    if (
        auto
        and proposals_json is None
        and new_obs < int(min_new_observations)
        and not reset_detected
    ):
        # In auto mode we only package/run if enough new evidence accumulated.
        return CompoundRunResult(
            ok=True,
            repo=str(repo),
            episode_id="",
            episode_path="",
            episode_created=False,
            decision_id="",
            decision_path="",
            instincts_created=0,
            instincts_updated=0,
            skills_created=0,
            skills_updated=0,
            wrote_instincts=False,
            wrote_docs=False,
            state_updated=False,
        )

    patch = _git_patch(repo, base_sha=base_sha, head_sha=head_sha, dirty=dirty)
    patch_sha_full = _sha256_text(patch) if patch.strip() else ""
    patch_bounded, patch_truncated = bounded_text(patch, max_bytes=int(max_patch_bytes))
    patch_omitted = bool(patch_truncated)
    patch_sha = patch_sha_full

    patch_blob_sha256 = ""
    if patch_omitted and patch.strip() and not dry_run:
        # No knowledge loss: if the episode omits the patch inline, persist the full patch as a blob.
        ref = write_blob_text(
            blobs_dir=paths.blobs_dir,
            text=patch,
            ext="diff",
            compression="none",
            expected_sha256=patch_sha_full,
        )
        patch_blob_sha256 = ref.sha256

    changed_files = _git_changed_files(
        repo, base_sha=base_sha, head_sha=head_sha, dirty=dirty
    )
    diffstat_sha = _sha256_text(diffstat)

    obs_stats = count_observations(paths.observations_file)

    start_count = 0 if reset_detected else int(state.observations_count or 0)
    end_count = int(start_count + new_obs)
    omitted = False

    cursor = EpisodeObservationCursor(
        start_count=int(start_count),
        end_count=int(end_count),
        tail_sha256=str(obs_stats.tail_sha256 or ""),
        reset_detected=bool(reset_detected),
        start_offset_bytes=int(ingested.start_offset_bytes),
        end_offset_bytes=int(end_offset),
        file_prefix_sha256=str(obs_prefix or ""),
    )
    ep_obs = EpisodeObservation(cursor=cursor, included=included, omitted=bool(omitted))
    ep_git = EpisodeGit(
        head_sha=head_sha,
        base_sha=base_sha,
        base_ref=base_ref,
        dirty=bool(dirty),
        diffstat=diffstat,
        diffstat_sha256=diffstat_sha,
        patch=("" if patch_omitted else patch_bounded),
        patch_sha256=patch_sha,
        patch_omitted=bool(patch_omitted),
        patch_blob_sha256=str(patch_blob_sha256),
        changed_files=changed_files,
    )

    proposals: Dict[str, Any] = {}
    if proposals_json is not None and str(proposals_json).strip():
        proposals = _load_json_from_text(proposals_json)
    if no_ai:
        proposals = {}

    ep = build_episode(
        created_at=_now_iso(),
        git=ep_git,
        observations=ep_obs,
        proposals=proposals,
        triage_status=("accepted" if auto else "pending"),
    )

    ep_path = episode_path_for_id(
        episodes_dir=paths.episodes_dir,
        created_at=ep.created_at,
        episode_id=ep.episode_id,
    )

    existing: Optional[Episode] = None
    if ep_path.exists():
        try:
            existing = load_episode(ep_path)
        except Exception:
            existing = None
    if existing is not None and existing.episode_id == ep.episode_id:
        ep = existing
        ep_path = ep_path
        created = False
    else:
        created = True

    if not dry_run:
        write_episode(ep_path, ep, overwrite=False)

    # Advance cursor regardless of whether we applied proposals. Episode is the evidence boundary.
    next_state = CompoundState(
        version=2,
        observations_offset_bytes=int(end_offset),
        observations_prefix_sha256=str(obs_prefix or ""),
        observations_count=int(end_count),
        observations_tail_sha256=str(obs_stats.tail_sha256 or ""),
        last_episode_id=str(ep.episode_id),
        updated_at=_now_iso(),
    )
    if not dry_run:
        save_state(state_path, next_state)

    instincts_created = 0
    instincts_updated = 0
    skills_created = 0
    skills_updated = 0
    wrote_instincts = False
    wrote_docs = False

    decision_id = ""
    decision_path = ""

    if ep.triage.status != "rejected" and ep.proposals:
        proposals_blob_sha256 = ""
        if not dry_run and proposals_json is not None and str(proposals_json).strip():
            # Preserve raw model output (even if formatting varies) for audit/debug.
            ref = write_blob_text(
                blobs_dir=paths.blobs_dir,
                text=str(proposals_json).strip() + "\n",
                ext="json",
                compression="none",
            )
            proposals_blob_sha256 = ref.sha256

        store = load_instincts(paths.instincts_file)

        inst_cands = parse_instinct_candidates(ep.proposals)
        if inst_cands:
            c, u = apply_instinct_candidates(
                store=store,
                candidates=inst_cands,
                episode_id=ep.episode_id,
                episode_ts=ep.created_at,
                head_sha=ep.git.head_sha,
                patch_sha256=ep.git.patch_sha256,
            )
            instincts_created += c
            instincts_updated += u

        skill_cands = parse_skill_candidates(ep.proposals)
        if skill_cands:
            c2, u2 = apply_skill_candidates(
                skills_dir=paths.skills_dir,
                candidates=skill_cands,
                episode_id=ep.episode_id,
                episode_ts=ep.created_at,
                mirror_claude_dir=(paths.root / ".claude" / "skills")
                if mirror_claude
                else None,
            )
            skills_created += c2
            skills_updated += u2

        # Record a deterministic Decision (normalized ops) as the authority for product mutations.
        # (Episodes remain the immutable evidence boundary; Decisions are append-only governance.)
        if not dry_run and (inst_cands or skill_cands):
            ops: List[Dict[str, Any]] = []
            for i in inst_cands:
                ops.append(
                    {
                        "op": "instinct.upsert",
                        "episode_id": ep.episode_id,
                        "ts": ep.created_at,
                        "id": i.id,
                        "title": i.title,
                        "trigger": i.trigger,
                        "action": i.action,
                        "confidence": float(i.confidence),
                        "tags": list(i.tags),
                        "notes": str(i.notes or ""),
                    }
                )
            for s in skill_cands:
                ops.append(
                    {
                        "op": "skill.upsert",
                        "episode_id": ep.episode_id,
                        "ts": ep.created_at,
                        "name": s.name,
                        "description": s.description,
                        "body": s.body,
                        "tags": list(s.tags),
                        "source_instinct_ids": list(s.source_instinct_ids),
                    }
                )
            ops.sort(
                key=lambda x: (
                    str(x.get("op")),
                    str(x.get("id") or x.get("name") or ""),
                )
            )
            dec = build_decision(
                created_at=ep.created_at,
                episode_id=ep.episode_id,
                proposal_blob_sha256=proposals_blob_sha256,
                ops=ops,
            )
            dp = decision_path_for_id(
                decisions_dir=paths.decisions_dir,
                created_at=dec.created_at,
                decision_id=dec.decision_id,
            )
            write_decision(dp, dec, overwrite=False)
            decision_id = dec.decision_id
            decision_path = str(dp)

        if (instincts_created or instincts_updated) and not dry_run:
            save_instincts(paths.instincts_file, store)
            wrote_instincts = True
            sync_instincts_markdown(root=repo, store=store)
            wrote_docs = True

    return CompoundRunResult(
        ok=True,
        repo=str(repo),
        episode_id=ep.episode_id,
        episode_path=str(ep_path),
        episode_created=bool(created),
        decision_id=str(decision_id),
        decision_path=str(decision_path),
        instincts_created=int(instincts_created),
        instincts_updated=int(instincts_updated),
        skills_created=int(skills_created),
        skills_updated=int(skills_updated),
        wrote_instincts=bool(wrote_instincts),
        wrote_docs=bool(wrote_docs),
        state_updated=(not dry_run),
    )


def replay_episode(
    *, root: Path, episode_path: Path, dry_run: bool, mirror_claude: bool
) -> CompoundRunResult:
    repo = root.resolve()
    require_scaffold_installed(repo)
    paths = compound_paths(repo)
    ep = load_episode(episode_path)

    instincts_created = 0
    instincts_updated = 0
    skills_created = 0
    skills_updated = 0
    wrote_instincts = False
    wrote_docs = False

    if ep.triage.status != "rejected" and ep.proposals:
        store = load_instincts(paths.instincts_file)
        inst_cands = parse_instinct_candidates(ep.proposals)
        if inst_cands:
            c, u = apply_instinct_candidates(
                store=store,
                candidates=inst_cands,
                episode_id=ep.episode_id,
                episode_ts=ep.created_at,
                head_sha=ep.git.head_sha,
                patch_sha256=ep.git.patch_sha256,
            )
            instincts_created += c
            instincts_updated += u

        skill_cands = parse_skill_candidates(ep.proposals)
        if skill_cands:
            c2, u2 = apply_skill_candidates(
                skills_dir=paths.skills_dir,
                candidates=skill_cands,
                episode_id=ep.episode_id,
                episode_ts=ep.created_at,
                mirror_claude_dir=(paths.root / ".claude" / "skills")
                if mirror_claude
                else None,
            )
            skills_created += c2
            skills_updated += u2

        if (instincts_created or instincts_updated) and not dry_run:
            save_instincts(paths.instincts_file, store)
            wrote_instincts = True
            sync_instincts_markdown(root=repo, store=store)
            wrote_docs = True

    return CompoundRunResult(
        ok=True,
        repo=str(repo),
        episode_id=ep.episode_id,
        episode_path=str(episode_path),
        episode_created=False,
        decision_id="",
        decision_path="",
        instincts_created=int(instincts_created),
        instincts_updated=int(instincts_updated),
        skills_created=int(skills_created),
        skills_updated=int(skills_updated),
        wrote_instincts=bool(wrote_instincts),
        wrote_docs=bool(wrote_docs),
        state_updated=False,
    )
