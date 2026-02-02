from __future__ import annotations

import inspect
from types import ModuleType
from typing import Any


def _safe_doc(obj: Any) -> str:
    doc = inspect.getdoc(obj) or ""
    return doc.strip().splitlines()[0].strip() if doc.strip() else ""


def introspect_module(mod: ModuleType, *, only_public: bool = True) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for name in dir(mod):
        if only_public and name.startswith("_"):
            continue
        try:
            obj = getattr(mod, name)
        except Exception:
            continue
        if not (inspect.isfunction(obj) or inspect.isclass(obj)):
            continue

        sig = ""
        try:
            sig = str(inspect.signature(obj))
        except Exception:
            sig = ""

        items.append(
            {
                "name": name,
                "kind": "class" if inspect.isclass(obj) else "function",
                "signature": sig,
                "doc": _safe_doc(obj),
                "module": getattr(obj, "__module__", "") or "",
            }
        )

    items.sort(key=lambda x: (x.get("kind") != "function", x.get("name") or ""))
    return {"module": getattr(mod, "__name__", ""), "symbols": items}
