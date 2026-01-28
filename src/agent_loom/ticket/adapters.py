from __future__ import annotations

import base64
import hashlib
import os
import re
from typing import Any, Dict, Tuple

import requests

from agent_loom.core.time import isoformat_z, utcnow
from agent_loom.ticket.models import Ticket
from agent_loom.ticket.store import TicketStore


class ExternalAdapter:
    name: str = "base"

    def can_handle(self, external_ref: str) -> bool:
        del external_ref
        raise NotImplementedError

    def sync(
        self,
        *,
        store: TicketStore,
        ticket: Ticket,
        external_ref: str,
        dry_run: bool,
        force: bool,
    ) -> Dict[str, Any]:
        del store, ticket, external_ref, dry_run, force
        raise NotImplementedError


_GH_REF_RE = re.compile(
    r"^gh:(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)[#/]?(?P<num>\d+)$"
)
_GH_SHORT_RE = re.compile(r"^gh-(?P<num>\d+)$")


class GitHubIssueAdapter(ExternalAdapter):
    name = "github"

    def can_handle(self, external_ref: str) -> bool:
        external_ref = (external_ref or "").strip()
        return bool(_GH_REF_RE.match(external_ref) or _GH_SHORT_RE.match(external_ref))

    def sync(
        self,
        *,
        store: TicketStore,
        ticket: Ticket,
        external_ref: str,
        dry_run: bool,
        force: bool,
    ) -> Dict[str, Any]:
        del force
        cfg = store.load_config()
        m = _GH_REF_RE.match(external_ref.strip())
        repo = ""
        num = ""
        if m:
            repo = m.group("repo")
            num = m.group("num")
        else:
            m2 = _GH_SHORT_RE.match(external_ref.strip())
            if not m2:
                raise ValueError(
                    f"Unrecognized GitHub external_ref: {external_ref}. Use gh:owner/repo#123 or gh-123 (with TK_GITHUB_REPO)."
                )
            num = m2.group("num")
            repo = os.getenv("TK_GITHUB_REPO") or cfg.github_default_repo
            if not repo:
                raise ValueError(
                    "GitHub shorthand external_ref 'gh-123' requires TK_GITHUB_REPO env var or .tickets/config.yaml github.default_repo"
                )

        api_url = f"https://api.github.com/repos/{repo}/issues/{num}"
        headers = {"Accept": "application/vnd.github+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        etag = ""
        ext = ticket.fm.get("external") or {}
        if isinstance(ext, dict):
            etag = str(ext.get("etag") or "")
        if etag:
            headers["If-None-Match"] = etag

        r = requests.get(api_url, headers=headers, timeout=20)
        if r.status_code == 304:
            return {"changed": False, "note": "Not modified (etag)", "external": ext}
        if r.status_code >= 400:
            raise RuntimeError(
                f"GitHub API error {r.status_code} for {api_url}: {r.text[:200]}. "
                "If this is an auth issue, set GITHUB_TOKEN."
            )

        data = r.json()
        updated_ext = {
            "system": "github",
            "repo": repo,
            "number": int(num),
            "url": data.get("html_url", ""),
            "api_url": api_url,
            "title": data.get("title", ""),
            "state": data.get("state", ""),
            "updated_at": data.get("updated_at", ""),
            "etag": r.headers.get("ETag", ""),
        }

        if not dry_run:
            ticket.fm["external"] = updated_ext
            ticket.fm["last_sync"] = isoformat_z(utcnow())
            store.save_ticket(ticket)

        return {"changed": True, "external": updated_ext}


_JIRA_KEY_RE = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
_JIRA_REF_RE = re.compile(r"^jira:(?P<key>[A-Za-z][A-Za-z0-9]+-\d+)$")
_JIRA_URL_RE = re.compile(
    r"^https?://[^/]+/(?:.*?/)?browse/(?P<key>[A-Za-z][A-Za-z0-9]+-\d+)",
    re.IGNORECASE,
)


def _sha256_hex(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _ticket_h1_and_rest(body: str) -> Tuple[str, str]:
    """Split ticket markdown body into (h1_line, rest).

    If no H1 exists, returns ("", full_body).
    """

    lines = (body or "").splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            h1 = line.rstrip()
            rest = "\n".join(lines[i + 1 :]).lstrip("\n")
            return h1, rest
    return "", body or ""


def _normalize_text_for_hash(s: str) -> str:
    return (s or "").replace("\r\n", "\n").strip() + "\n"


def _adf_to_text(adf: Any) -> str:
    """Best-effort conversion from Jira ADF -> plain text.

    We only need a minimal representation for syncing bodies.
    """

    if not adf or not isinstance(adf, dict):
        return ""

    out: list[str] = []

    def walk(node: Any) -> None:
        if node is None:
            return
        if isinstance(node, list):
            for x in node:
                walk(x)
            return
        if not isinstance(node, dict):
            return

        ntype = str(node.get("type") or "")
        if ntype == "text":
            out.append(str(node.get("text") or ""))
            return

        if ntype in {"hardBreak"}:
            out.append("\n")
            return

        if ntype in {"paragraph", "heading", "blockquote", "listItem"}:
            walk(node.get("content") or [])
            out.append("\n\n")
            return

        # default: recurse
        walk(node.get("content") or [])

    walk(adf)
    text = "".join(out)
    # collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def _text_to_adf(text: str) -> Dict[str, Any]:
    """Convert plain text -> minimal Jira ADF doc."""

    t = (text or "").replace("\r\n", "\n").strip("\n")
    if not t.strip():
        return {"type": "doc", "version": 1, "content": []}

    paras: list[dict[str, Any]] = []
    for para in re.split(r"\n\n+", t):
        para = para.strip("\n")
        if not para.strip():
            continue
        paras.append(
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": para}],
            }
        )

    return {"type": "doc", "version": 1, "content": paras}


class JiraIssueAdapter(ExternalAdapter):
    name = "jira"

    def can_handle(self, external_ref: str) -> bool:
        ref = (external_ref or "").strip()
        if not ref:
            return False
        if _JIRA_REF_RE.match(ref):
            return True
        if _JIRA_URL_RE.match(ref):
            return True
        return False

    def _resolve_base_url(self, cfg) -> str:
        return (
            os.getenv("TK_JIRA_BASE_URL")
            or os.getenv("JIRA_BASE_URL")
            or cfg.jira_base_url
            or ""
        ).rstrip("/")

    def _resolve_auth_headers(self) -> Dict[str, str]:
        bearer = os.getenv("TK_JIRA_TOKEN") or os.getenv("JIRA_TOKEN") or ""
        if bearer.strip():
            return {"Authorization": f"Bearer {bearer.strip()}"}

        email = (os.getenv("TK_JIRA_EMAIL") or os.getenv("JIRA_EMAIL") or "").strip()
        token = (
            os.getenv("TK_JIRA_API_TOKEN") or os.getenv("JIRA_API_TOKEN") or ""
        ).strip()
        if email and token:
            basic = f"{email}:{token}".encode("utf-8")
            b64 = base64.b64encode(basic).decode("ascii")
            return {"Authorization": f"Basic {b64}"}

        raise ValueError(
            "Jira auth missing. Set JIRA_EMAIL + JIRA_API_TOKEN (recommended for Jira Cloud) "
            "or JIRA_TOKEN (bearer)."
        )

    def _parse_ref(self, *, external_ref: str, base_url: str) -> Tuple[str, str, str]:
        ref = (external_ref or "").strip()
        m = _JIRA_REF_RE.match(ref)
        if m:
            key = m.group("key").upper()
            if not _JIRA_KEY_RE.match(key):
                raise ValueError(f"Invalid Jira key: {key}. Expected like PROJ-123.")
            if not base_url:
                raise ValueError(
                    "Jira base URL missing. Set TK_JIRA_BASE_URL (or JIRA_BASE_URL) or .tickets/config.yaml jira.base_url"
                )
            browse_url = f"{base_url}/browse/{key}"
            return base_url, key, browse_url

        m2 = _JIRA_URL_RE.match(ref)
        if m2:
            key = m2.group("key").upper()
            # base_url inferred from the URL itself
            m_base = re.match(r"^(https?://[^/]+)", ref, re.IGNORECASE)
            inferred_base = m_base.group(1) if m_base else ""
            browse_url = f"{inferred_base}/browse/{key}" if inferred_base else ref
            return inferred_base.rstrip("/"), key, browse_url

        raise ValueError(
            f"Unrecognized Jira external_ref: {external_ref}. Use jira:PROJ-123 or a browse URL like https://your-domain/browse/PROJ-123."
        )

    def _get_issue(
        self, *, api_base: str, key: str, headers: Dict[str, str]
    ) -> Dict[str, Any]:
        url = f"{api_base}/rest/api/3/issue/{key}"
        r = requests.get(
            url,
            headers={
                **headers,
                "Accept": "application/json",
            },
            params={"fields": "summary,description,updated"},
            timeout=20,
        )
        if r.status_code >= 400:
            raise RuntimeError(
                f"Jira API error {r.status_code} for {url}: {r.text[:200]}. "
                "Check auth (JIRA_EMAIL+JIRA_API_TOKEN or JIRA_TOKEN) and base URL."
            )
        return r.json()

    def _put_description(
        self,
        *,
        api_base: str,
        key: str,
        headers: Dict[str, str],
        description_adf: Dict[str, Any],
    ) -> None:
        url = f"{api_base}/rest/api/3/issue/{key}"
        payload = {"fields": {"description": description_adf}}
        r = requests.put(
            url,
            headers={
                **headers,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20,
        )
        if r.status_code >= 400:
            raise RuntimeError(
                f"Jira API error {r.status_code} for {url}: {r.text[:200]}. "
                "Check auth (JIRA_EMAIL+JIRA_API_TOKEN or JIRA_TOKEN) and base URL."
            )

    def sync(
        self,
        *,
        store: TicketStore,
        ticket: Ticket,
        external_ref: str,
        dry_run: bool,
        force: bool,
    ) -> Dict[str, Any]:
        cfg = store.load_config()
        base_url_cfg = self._resolve_base_url(cfg)
        auth_headers = self._resolve_auth_headers()

        base_url, key, browse_url = self._parse_ref(
            external_ref=external_ref, base_url=base_url_cfg
        )
        api_base = base_url or base_url_cfg
        if not api_base:
            raise ValueError(
                "Jira base URL missing. Set TK_JIRA_BASE_URL (or JIRA_BASE_URL) or .tickets/config.yaml jira.base_url"
            )

        data = self._get_issue(api_base=api_base, key=key, headers=auth_headers)
        fields = data.get("fields") or {}
        summary = str(fields.get("summary") or "")
        updated_at = str(fields.get("updated") or "")
        remote_adf = fields.get("description")
        remote_text = _adf_to_text(remote_adf)
        remote_hash = _sha256_hex(_normalize_text_for_hash(remote_text))

        h1, local_desc = _ticket_h1_and_rest(ticket.body)
        local_desc_norm = _normalize_text_for_hash(local_desc)
        local_hash = _sha256_hex(local_desc_norm)

        ext0 = ticket.fm.get("external")
        ext: Dict[str, Any] = ext0 if isinstance(ext0, dict) else {}
        is_prev_jira = str(ext.get("system") or "") == "jira" and str(
            ext.get("key") or ""
        )
        prev_remote_hash = str(ext.get("remote_description_hash") or "")
        prev_local_hash = str(ext.get("local_description_hash") or "")

        first_sync = not is_prev_jira or not prev_remote_hash or not prev_local_hash
        remote_changed = (not first_sync) and (remote_hash != prev_remote_hash)
        local_changed = (not first_sync) and (local_hash != prev_local_hash)

        # Decide direction
        direction = "noop"
        if first_sync:
            local_has_content = bool(local_desc.strip())
            remote_has_content = bool(remote_text.strip())
            if remote_has_content and not local_has_content:
                direction = "pull"
            elif local_has_content and not remote_has_content:
                direction = "push"
            elif not local_has_content and not remote_has_content:
                direction = "noop"
            else:
                if force:
                    direction = "push"
                else:
                    return {
                        "changed": False,
                        "note": "conflict: both local and remote have content (rerun with --force to push local)",
                        "external": {
                            "system": "jira",
                            "base_url": api_base,
                            "key": key,
                            "url": browse_url,
                            "api_url": f"{api_base}/rest/api/3/issue/{key}",
                            "summary": summary,
                            "updated_at": updated_at,
                        },
                    }
        else:
            if remote_changed and not local_changed:
                direction = "pull"
            elif local_changed and not remote_changed:
                direction = "push"
            elif not remote_changed and not local_changed:
                direction = "noop"
            else:
                if force:
                    direction = "push"
                else:
                    return {
                        "changed": False,
                        "note": "conflict: local and remote both changed (rerun with --force to push local)",
                        "external": ext,
                    }

        changed = False

        if direction == "pull":
            changed = True
            if not dry_run:
                # preserve local H1/title; replace everything after it with remote description
                if h1:
                    ticket.body = (
                        h1
                        + "\n\n"
                        + (remote_text.rstrip() + "\n" if remote_text.strip() else "")
                    )
                else:
                    ticket.body = remote_text.rstrip() + "\n"

                # local description now matches remote
                local_hash = remote_hash

        if direction == "push":
            changed = True
            if not dry_run:
                self._put_description(
                    api_base=api_base,
                    key=key,
                    headers=auth_headers,
                    description_adf=_text_to_adf(local_desc),
                )
                # Refresh remote view after update
                data = self._get_issue(api_base=api_base, key=key, headers=auth_headers)
                fields = data.get("fields") or {}
                summary = str(fields.get("summary") or "")
                updated_at = str(fields.get("updated") or "")
                remote_adf = fields.get("description")
                remote_text = _adf_to_text(remote_adf)
                remote_hash = _sha256_hex(_normalize_text_for_hash(remote_text))

        updated_ext = {
            "system": "jira",
            "base_url": api_base,
            "key": key,
            "url": browse_url,
            "api_url": f"{api_base}/rest/api/3/issue/{key}",
            "summary": summary,
            "updated_at": updated_at,
            "remote_description_hash": remote_hash,
            "local_description_hash": local_hash,
            "last_direction": direction,
        }

        if not dry_run:
            ticket.fm["external"] = updated_ext
            ticket.fm["last_sync"] = isoformat_z(utcnow())
            store.save_ticket(ticket)

        return {"changed": changed, "external": updated_ext}


__all__ = ["ExternalAdapter", "GitHubIssueAdapter", "JiraIssueAdapter"]
