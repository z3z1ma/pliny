# Staging Area + Commit Flow

ID: ticket:20260526-mill-shaping-staging
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - atomic multi-file writes with cross-reference resolution; branch state management
Depends On: ticket:20260526-mill-shaping-blocks

## Summary

Manages draft records proposed by the interaction block engine: CRUD operations on
staged records, branch management (create/switch/compare/merge), cross-reference
tracking between staged records, and the atomic commit flow that materializes the
entire staged subgraph to `.loom/` with correct IDs and a durable session record.

Closure claim: Records can be proposed into a staging area, edited, branched, and
atomically committed to `.loom/` with correct cross-references and a durable
session record.

## Related Records

- `plan:20260526-mill-shaping-sessions` - parent plan
- `ticket:20260526-mill-shaping-blocks` - produces proposals that feed staging
- `spec:mill-shaping-sessions` - commit flow and staging behavior
- `loom-mill/src/loom_mill/api/design.py:204-227` - existing record creation pattern

## Scope

Write:
- `loom-mill/src/loom_mill/shaping/staging.py` — staged record management + branching
- `loom-mill/src/loom_mill/shaping/commit.py` — atomic commit flow
- `loom-mill/src/loom_mill/shaping/session.py` — extend with staging/commit methods
- `loom-mill/src/loom_mill/api/shaping.py` — staging and commit endpoints
- `loom-mill/tests/test_shaping_staging.py` — test coverage

Non-goals:
- Do NOT implement conflict resolution for records that already exist on disk (for now, staged records are always new)
- Do NOT implement partial commit (all-or-nothing)
- Do NOT build the frontend staging panel (ticket 5)

## Detailed Design

### Staged Record Operations

```python
# loom_mill/shaping/staging.py

class StagingArea:
    """Manages draft records within a shaping session."""
    
    def __init__(self, session: ShapingSession):
        self.session = session
    
    def propose(self, surface: str, title: str, content: str, branch: str = "main") -> StagedRecord:
        """Add a new proposed record to the staging area."""
        temp_id = f"temp:{surface}:{slugify(title)}"
        record = StagedRecord(
            temp_id=temp_id,
            surface=surface,
            title=title,
            content=content,
            branch=branch,
            status="proposed",
            proposed_at=utc_now(),
        )
        self.session.state.staged_records.append(record)
        self.session._persist_state()
        return record
    
    def update(self, temp_id: str, content: str | None = None, title: str | None = None) -> StagedRecord:
        """Update a staged record's content or title."""
        record = self._find(temp_id)
        if content is not None:
            record.content = content
        if title is not None:
            record.title = title
        record.status = "modified"
        record.modified_at = utc_now()
        self.session._persist_state()
        return record
    
    def accept(self, temp_id: str) -> StagedRecord:
        """Mark a staged record as accepted by the operator."""
        record = self._find(temp_id)
        record.status = "accepted"
        self.session._persist_state()
        return record
    
    def reject(self, temp_id: str) -> None:
        """Remove a staged record."""
        self.session.state.staged_records = [
            r for r in self.session.state.staged_records if r.temp_id != temp_id
        ]
        self.session._persist_state()
    
    def list_branch(self, branch: str = "main") -> list[StagedRecord]:
        """List staged records on a specific branch."""
        return [r for r in self.session.state.staged_records if r.branch == branch]
    
    def create_branch(self, branch_id: str, label: str) -> None:
        """Create a new branch, copying current staged records."""
        if branch_id in self.session.state.branches:
            raise ValueError(f"Branch {branch_id} already exists")
        self.session.state.branches.append(branch_id)
        # Copy all main-branch records to new branch
        for record in self.list_branch(self.session.state.active_branch):
            copy = StagedRecord(
                temp_id=f"{record.temp_id}:{branch_id}",
                surface=record.surface,
                title=record.title,
                content=record.content,
                branch=branch_id,
                status=record.status,
                proposed_at=record.proposed_at,
            )
            self.session.state.staged_records.append(copy)
        self.session._persist_state()
    
    def switch_branch(self, branch_id: str) -> None:
        """Switch the active branch."""
        if branch_id not in self.session.state.branches:
            raise ValueError(f"Branch {branch_id} not found")
        self.session.state.active_branch = branch_id
        self.session._persist_state()
    
    def merge_branch(self, source_branch: str, target_branch: str = "main") -> None:
        """Merge records from source into target, replacing target versions."""
        source_records = self.list_branch(source_branch)
        # Remove target records that have source equivalents
        source_surfaces = {(r.surface, r.title) for r in source_records}
        self.session.state.staged_records = [
            r for r in self.session.state.staged_records
            if r.branch != target_branch or (r.surface, r.title) not in source_surfaces
        ]
        # Move source records to target branch
        for record in source_records:
            record.branch = target_branch
        self.session.state.active_branch = target_branch
        # Remove the merged branch
        self.session.state.branches = [b for b in self.session.state.branches if b != source_branch]
        self.session._persist_state()
    
    def cross_references(self) -> dict[str, list[str]]:
        """Map each temp_id to the temp_ids it references in its content."""
        refs = {}
        active_records = self.list_branch(self.session.state.active_branch)
        all_temp_ids = {r.temp_id for r in active_records}
        for record in active_records:
            refs[record.temp_id] = [
                tid for tid in all_temp_ids
                if tid != record.temp_id and tid in record.content
            ]
        return refs
    
    def _find(self, temp_id: str) -> StagedRecord:
        for r in self.session.state.staged_records:
            if r.temp_id == temp_id:
                return r
        raise ValueError(f"Staged record {temp_id} not found")
```

### Commit Flow

```python
# loom_mill/shaping/commit.py

from datetime import date
from pathlib import Path
import subprocess

class CommitFlow:
    """Atomically materializes staged records to .loom/."""
    
    def __init__(self, session: ShapingSession, workspace_root: Path, store: MillStateStore):
        self.session = session
        self.workspace_root = workspace_root
        self.store = store
    
    async def commit(self) -> CommitResult:
        """
        Materialize all staged records on the active branch to .loom/.
        
        Steps:
        1. Resolve temp IDs to real IDs (generate dates, slugs)
        2. Replace temp_id references in content with real IDs
        3. Write all records atomically
        4. Create a git commit
        5. Write durable session record (research or knowledge)
        6. End the session
        """
        active_records = self.session.staging.list_branch(self.session.state.active_branch)
        if not active_records:
            raise ValueError("Nothing to commit")
        
        # Step 1: Generate real IDs
        today = date.today().strftime("%Y%m%d")
        id_map: dict[str, str] = {}  # temp_id → real_id
        path_map: dict[str, Path] = {}  # temp_id → file path
        
        for record in active_records:
            slug = slugify(record.title)
            real_id = f"{record.surface.rstrip('s')}:{today}-{slug}"  # e.g., "ticket:20260526-auth-fix"
            id_map[record.temp_id] = real_id
            path_map[record.temp_id] = self.workspace_root / ".loom" / record.surface / f"{today}-{slug}.md"
        
        # Step 2: Replace temp references in content
        for record in active_records:
            resolved_content = record.content
            for temp_id, real_id in id_map.items():
                resolved_content = resolved_content.replace(temp_id, real_id)
            # Also update the ID: line in the record itself
            record.content = resolved_content
        
        # Step 3: Write all records to disk
        written_paths: list[Path] = []
        try:
            for record in active_records:
                path = path_map[record.temp_id]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(record.content, encoding="utf-8")
                written_paths.append(path)
        except Exception:
            # Rollback on failure
            for p in written_paths:
                p.unlink(missing_ok=True)
            raise
        
        # Step 4: Git commit
        relative_paths = [str(p.relative_to(self.workspace_root)) for p in written_paths]
        subprocess.run(
            ["git", "add"] + relative_paths,
            cwd=self.workspace_root,
            capture_output=True,
        )
        commit_msg = self._generate_commit_message(active_records)
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=self.workspace_root,
            capture_output=True,
        )
        
        # Step 5: Write durable session record
        session_record_path = self._write_session_record(active_records, id_map)
        
        # Step 6: End session
        self.session.state.ended_at = utc_now()
        self.session._persist_state()
        
        # Publish events
        self.store.publish(ShapingEvent(
            session_id=self.session.session_id,
            event="session_ended",
            data={"reason": "committed", "records_created": len(active_records)}
        ))
        
        return CommitResult(
            records_created=len(active_records),
            paths=relative_paths,
            commit_message=commit_msg,
            session_record_path=str(session_record_path),
        )
    
    def _generate_commit_message(self, records: list[StagedRecord]) -> str:
        """Generate a meaningful commit message summarizing shaped records."""
        surfaces = {}
        for r in records:
            surfaces.setdefault(r.surface, []).append(r.title)
        
        parts = []
        for surface, titles in surfaces.items():
            parts.append(f"{len(titles)} {surface}")
        
        summary = ", ".join(parts)
        title_list = "\n".join(f"- {r.title}" for r in records)
        return f"shape: {summary}\n\nShaped records:\n{title_list}"
    
    def _write_session_record(self, records: list[StagedRecord], id_map: dict) -> Path:
        """Write a durable knowledge record capturing the session reasoning."""
        today = date.today().isoformat()
        slug = f"{today.replace('-', '')}-shaping-session"
        path = self.workspace_root / ".loom" / "knowledge" / f"{slug}.md"
        
        record_refs = "\n".join(f"- `{real_id}` — {r.title}" for r, (_, real_id) in zip(records, id_map.items()))
        
        content = f"""# Shaping Session Record

ID: knowledge:{slug}
Type: Knowledge Preference
Status: active
Created: {today}
Updated: {today}

## Summary

Shaping session that produced {len(records)} records through interactive
exploration and operator collaboration.

## Records Created

{record_refs}

## Session Context

The full session context document is available at:
`.mill/shaping-sessions/{self.session.session_id}/context.md`

## Decisions Made

(Extracted from session interaction history)
"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        
        # Git add the session record too
        subprocess.run(
            ["git", "add", str(path.relative_to(self.workspace_root))],
            cwd=self.workspace_root,
            capture_output=True,
        )
        
        return path

@dataclass
class CommitResult:
    records_created: int
    paths: list[str]
    commit_message: str
    session_record_path: str
```

### API Endpoints

```python
# POST /shaping/sessions/{session_id}/staged
# Body: {"surface": "tickets", "title": "...", "content": "..."}
# Returns: StagedRecord JSON
# Manually stage a record (usually done by the engine, but operator can too)

# PUT /shaping/sessions/{session_id}/staged/{temp_id}
# Body: {"content": "...", "title": "..."}  (partial update)
# Returns: updated StagedRecord JSON

# DELETE /shaping/sessions/{session_id}/staged/{temp_id}
# Rejects/removes a staged record

# POST /shaping/sessions/{session_id}/staged/{temp_id}/accept
# Marks a staged record as accepted

# POST /shaping/sessions/{session_id}/branch
# Body: {"branch_id": "...", "label": "..."}
# Creates a new branch

# POST /shaping/sessions/{session_id}/branch/{branch_id}/switch
# Switches active branch

# POST /shaping/sessions/{session_id}/branch/{source}/merge
# Body: {"target": "main"}
# Merges source branch into target

# POST /shaping/sessions/{session_id}/commit
# Returns: CommitResult JSON
# Atomically commits all staged records on active branch to .loom/
```

## Acceptance

- ACC-001: Records can be proposed, updated, accepted, and rejected through the API.
  - Evidence: Test full CRUD cycle on staged records.
  - Audit: Verify persistence survives session reload.

- ACC-002: Branching works: create branch, switch, propose on branch, merge back.
  - Evidence: Test branch lifecycle, verify records move correctly.
  - Audit: Verify no orphaned records after merge.

- ACC-003: Commit writes all staged records to correct `.loom/` paths with resolved
  cross-references (temp IDs replaced with real IDs).
  - Evidence: Stage 3 records that reference each other, commit, verify files on disk have real IDs.
  - Audit: Verify no temp_id strings remain in committed files.

- ACC-004: Commit creates a git commit with a meaningful message.
  - Evidence: After commit, check `git log --oneline -1`.

- ACC-005: Commit produces a durable knowledge record at `.loom/knowledge/`.
  - Evidence: After commit, verify knowledge record exists with correct content.

- ACC-006: Failed commit rolls back (no partial writes to `.loom/`).
  - Evidence: Test with a path that can't be written (permission error), verify no files created.

- ACC-007: Backend tests pass.
  - Evidence: Test output.

## Current State

Implementation is complete and ready for review/audit. Staging CRUD, branch
management, engine proposal integration, commit materialization, API endpoints,
and focused tests are in place. Validation passed for the focused staging suite,
full backend suite, and frontend build. Repository-wide whitespace check is still
limited by pre-existing trailing whitespace in `GraphSidebar.svelte`, outside this
ticket's write scope; touched-file whitespace check passed.

## Evidence

- `evidence:20260526-mill-shaping-staging-validation` - focused staging tests, full
  backend tests, frontend build, and whitespace checks.

## Journal

- 2026-05-26: Started implementation in the current session. Read ticket, parent
  plan, prerequisite block-engine ticket, shaping-session spec, and existing
  record creation pattern. Working inside the ticket write scope for staging,
  commit flow, API endpoints, engine proposal integration, and focused tests.
- 2026-05-26: Implemented staging manager, commit flow, API endpoints, engine
  proposal staging hook, and focused tests. Validation evidence recorded in
  `evidence:20260526-mill-shaping-staging-validation`; moved ticket to review
  pending audit.
- 2026-05-26: Created ticket. Fourth in the shaping sessions plan. Handles the
  materialization of shaped work into durable Loom records.
