from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Iterable, List, Tuple

import yaml

from agent_loom.pack.models import PackManifest


def _packs_root():
    return resources.files("agent_loom.pack").joinpath("packs")


def list_pack_ids() -> List[str]:
    root = _packs_root()
    if not root.is_dir():
        return []
    ids: List[str] = []
    for child in root.iterdir():
        if child.is_dir() and child.joinpath("pack.yaml").is_file():
            ids.append(child.name)
    return sorted(ids)


def pack_dir(pack_id: str):
    return _packs_root().joinpath(pack_id)


def load_manifest(pack_id: str) -> PackManifest:
    pd = pack_dir(pack_id)
    mf = pd.joinpath("pack.yaml")
    if not mf.is_file():
        raise FileNotFoundError(f"unknown pack: {pack_id}")
    with resources.as_file(mf) as p:
        raw = Path(p).read_text(encoding="utf-8")
    doc = yaml.safe_load(raw)
    if not isinstance(doc, dict):
        raise ValueError(f"invalid pack.yaml for {pack_id}: expected mapping")

    def _require_str(k: str) -> str:
        v = doc.get(k)
        if not isinstance(v, str) or not v.strip():
            raise ValueError(
                f"invalid pack.yaml for {pack_id}: {k} must be a non-empty string"
            )
        return v.strip()

    def _require_list_str(k: str) -> List[str]:
        v = doc.get(k)
        if not isinstance(v, list) or not all(
            isinstance(x, str) and x.strip() for x in v
        ):
            raise ValueError(
                f"invalid pack.yaml for {pack_id}: {k} must be a list of strings"
            )
        return [str(x).strip() for x in v]

    upstream = doc.get("upstream")
    if upstream is not None and not isinstance(upstream, dict):
        raise ValueError(f"invalid pack.yaml for {pack_id}: upstream must be a mapping")
    if isinstance(upstream, dict):
        upstream = {str(k): str(v) for k, v in upstream.items()}

    mid = _require_str("id")
    if mid != pack_id:
        raise ValueError(
            f"invalid pack.yaml for {pack_id}: id must match directory name"
        )

    return PackManifest(
        id=mid,
        version=_require_str("version"),
        description=_require_str("description"),
        install_roots=_require_list_str("install_roots"),
        managed_globs=_require_list_str("managed_globs"),
        protected_globs=_require_list_str("protected_globs"),
        upstream=upstream,
    )


def iter_pack_files(pack_id: str) -> Iterable[Tuple[str, Path]]:
    """Yield (repo-relative path, concrete file path) for pack files."""
    pd = pack_dir(pack_id)
    files_root = pd.joinpath("files")
    if not files_root.is_dir():
        return []

    def _walk(base, prefix: str) -> List[Tuple[str, Path]]:
        out: List[Tuple[str, Path]] = []
        for child in base.iterdir():
            name = str(getattr(child, "name", ""))
            if not name:
                continue
            next_prefix = f"{prefix}/{name}" if prefix else name
            if child.is_dir():
                out.extend(_walk(child, next_prefix))
            elif child.is_file():
                with resources.as_file(child) as p:
                    out.append((next_prefix, Path(p)))
        return out

    out = _walk(files_root, "")
    out.sort(key=lambda x: x[0])
    return out
