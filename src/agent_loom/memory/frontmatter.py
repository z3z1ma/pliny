from __future__ import annotations

import datetime as dt
import re
from typing import Any, Dict, List, Tuple

import yaml

PREFERRED_FM_ORDER = [
    "id",
    "title",
    "aliases",
    "tags",
    "scopes",
    "links",
    "visibility",
    "status",
    "created_at",
    "updated_at",
]


def split_yaml_frontmatter(md: str) -> Tuple[Dict[str, Any], str]:
    t = (md or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = t.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, md

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, md

    fm_txt = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :])

    raw = yaml.safe_load(fm_txt) or {}
    if not isinstance(raw, dict):
        raise ValueError("frontmatter must be a YAML mapping/object")

    def _coerce(v: Any) -> Any:
        if isinstance(v, dt.datetime):
            if v.tzinfo is None:
                v = v.replace(tzinfo=dt.timezone.utc)
            v = v.astimezone(dt.timezone.utc).replace(microsecond=0)
            return v.isoformat().replace("+00:00", "Z")
        if isinstance(v, dt.date):
            return v.isoformat()
        if isinstance(v, list):
            return [_coerce(x) for x in v]
        if isinstance(v, dict):
            return {str(k): _coerce(x) for k, x in v.items()}
        return v

    return _coerce(raw), body


def dump_yaml_frontmatter(fm: Dict[str, Any]) -> str:
    fm = dict(fm or {})

    existing_order = list(fm.keys())

    ordered: Dict[str, Any] = {}
    for k in PREFERRED_FM_ORDER:
        if k in fm and fm.get(k) not in (None, "", [], {}):
            ordered[k] = fm[k]

    for k in existing_order:
        if k in ordered:
            continue
        if fm.get(k) not in (None, "", [], {}):
            ordered[k] = fm[k]

    class Dumper(yaml.SafeDumper):
        pass

    def _repr_str(dumper: yaml.SafeDumper, data: str):
        s = data

        needs_quote = False
        if s == "" or s != s.strip():
            needs_quote = True
        if any(ch in s for ch in ["\n", "\r", "\t"]):
            needs_quote = True
        if s.startswith(
            (
                "-",
                "?",
                ":",
                "{",
                "}",
                "[",
                "]",
                ",",
                "*",
                "&",
                "!",
                "%",
                "@",
                "`",
                "#",
                "|",
                ">",
                "'",
                '"',
            )
        ):
            needs_quote = True
        if ":" in s or "#" in s:
            needs_quote = True

        low = s.casefold()
        if low in {"y", "yes", "n", "no", "true", "false", "on", "off", "null", "~"}:
            needs_quote = True
        if re.match(r"^[+-]?(\d+)(\.\d+)?$", s):
            needs_quote = True
        if re.match(r"^\d{4}-\d{2}-\d{2}", s):
            needs_quote = True

        style = '"' if needs_quote else None
        return dumper.represent_scalar("tag:yaml.org,2002:str", s, style=style)

    Dumper.add_representer(str, _repr_str)

    y = yaml.dump(
        ordered,
        Dumper=Dumper,
        sort_keys=False,
        default_flow_style=False,
        width=100,
        allow_unicode=True,
    ).strip()

    out_lines: List[str] = []
    key_re = re.compile(r'^(\s*)"([A-Za-z0-9_-]+)":(.*)$')
    for ln in y.split("\n"):
        m = key_re.match(ln)
        if m:
            ln = f"{m.group(1)}{m.group(2)}:{m.group(3)}"
        out_lines.append(ln)
    y = "\n".join(out_lines)
    return f"---\n{y}\n---\n\n"


def canonicalize_rfc3339_utc(s: str) -> str:
    raw = (s or "").strip()
    if not raw:
        return ""
    txt = raw.replace("Z", "+00:00") if raw.endswith("Z") else raw
    try:
        d = dt.datetime.fromisoformat(txt)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        d = d.astimezone(dt.timezone.utc).replace(microsecond=0)
        return d.isoformat().replace("+00:00", "Z")
    except Exception:
        return raw
