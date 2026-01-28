from __future__ import annotations

import datetime as dt
import re
from typing import Any, Dict, List, Mapping, Tuple

import yaml

from agent_loom.core.time import isoformat_z
from agent_loom.ticket.errors import TicketArgError

CANON_KEYS_TO_YAML = {
    "external_ref": "external-ref",
    "claimed_by": "claimed-by",
    "claimed_at": "claimed-at",
    "claim_expires": "claim-expires",
    "claim_ttl": "claim-ttl",
    "last_sync": "last-sync",
}

YAML_KEYS_TO_CANON = {v: k for k, v in CANON_KEYS_TO_YAML.items()}


def _validate_yaml_frontmatter_keys(raw: Mapping[str, Any]) -> None:
    bad: List[str] = []
    fixes: List[str] = []
    for k in (raw or {}).keys():
        ks = str(k)
        if ks in YAML_KEYS_TO_CANON:
            continue
        if ks.replace("_", "-") in YAML_KEYS_TO_CANON:
            bad.append(ks)
            fixes.append(f"{ks} -> {ks.replace('_', '-')}")
    if bad:
        bad_s = ", ".join(sorted(set(bad)))
        fix_s = ", ".join(sorted(set(fixes)))
        hint = "Use kebab-case in YAML keys (e.g. `claim-expires`), not snake_case."
        if fix_s:
            hint = hint + " Fix: " + fix_s
        raise TicketArgError(
            code="ARG", error=f"Invalid frontmatter key(s): {bad_s}", hint=hint
        )


def canonicalize_frontmatter(raw: Mapping[str, Any]) -> Dict[str, Any]:
    _validate_yaml_frontmatter_keys(raw)

    def _coerce_yaml_value(v: Any) -> Any:
        if isinstance(v, dt.datetime):
            if v.tzinfo is None:
                v = v.replace(tzinfo=dt.timezone.utc)
            return isoformat_z(v)
        if isinstance(v, dt.date):
            return v.isoformat()
        if isinstance(v, list):
            return [_coerce_yaml_value(x) for x in v]
        if isinstance(v, dict):
            return {str(k): _coerce_yaml_value(x) for k, x in v.items()}
        return v

    out: Dict[str, Any] = {}
    for k, v in (raw or {}).items():
        out[YAML_KEYS_TO_CANON.get(str(k), str(k))] = _coerce_yaml_value(v)
    return out


def decanonicalize_frontmatter(raw: Mapping[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in (raw or {}).items():
        out[CANON_KEYS_TO_YAML.get(str(k), str(k))] = v
    return out


_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def split_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body = text[m.end() :]
    try:
        raw = yaml.safe_load(fm_text) or {}
        if not isinstance(raw, dict):
            raw = {}
    except Exception:
        raw = {}
    return canonicalize_frontmatter(raw), body


def dump_frontmatter(frontmatter: Mapping[str, Any]) -> str:
    preferred_order = [
        "id",
        "status",
        "deps",
        "links",
        "created",
        "type",
        "priority",
        "assignee",
        "external_ref",
        "parent",
        "tags",
        "claimed_by",
        "claimed_at",
        "claim_expires",
        "claim_ttl",
        "heartbeat",
        "last_sync",
        "external",
    ]
    fm = dict(frontmatter)

    def _list(x: Any) -> List[Any]:
        if x is None:
            return []
        if isinstance(x, list):
            return x
        if isinstance(x, str):
            s = x.strip()
            if not s:
                return []
            if s.startswith("[") and s.endswith("]"):
                inner = s[1:-1].strip()
                if not inner:
                    return []
                return [p.strip() for p in inner.split(",") if p.strip()]
            return [s]
        return [x]

    for k in ("deps", "links", "tags"):
        fm[k] = _list(fm.get(k))

    fm.setdefault("deps", [])
    fm.setdefault("links", [])
    fm.setdefault("tags", [])
    fm.setdefault("status", "open")
    fm.setdefault("priority", 2)
    fm.setdefault("type", "task")

    ordered: Dict[str, Any] = {}
    for k in preferred_order:
        if k in fm and fm.get(k) is not None and fm.get(k) != "":
            ordered[k] = fm[k]
    for k in sorted(fm.keys()):
        if k not in ordered and fm.get(k) is not None and fm.get(k) != "":
            ordered[k] = fm[k]

    yaml_ready = decanonicalize_frontmatter(ordered)

    class Dumper(yaml.SafeDumper):
        pass

    def _repr_str(dumper: yaml.SafeDumper, data: str):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')

    Dumper.add_representer(str, _repr_str)
    y = yaml.dump(
        yaml_ready,
        Dumper=Dumper,
        sort_keys=False,
        default_flow_style=False,
        width=100,
        allow_unicode=True,
    ).strip()
    return f"---\n{y}\n---\n"


def extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


def normalize_list_value(x: Any) -> List[str]:
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i).strip() for i in x if str(i).strip()]
    if isinstance(x, str):
        s = x.strip()
        if not s:
            return []
        if s.startswith("[") and s.endswith("]"):
            inner = s[1:-1].strip()
            if not inner:
                return []
            return [p.strip() for p in inner.split(",") if p.strip()]
        return [s]
    return [str(x).strip()]
