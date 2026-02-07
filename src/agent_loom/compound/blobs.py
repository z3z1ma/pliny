from __future__ import annotations

import gzip
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Literal, Optional


BlobCompression = Literal["none", "gzip"]


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(str(text or "").encode("utf-8"))


def blob_filename(*, sha256_hex: str, ext: str, compression: BlobCompression) -> str:
    ident = str(sha256_hex or "").strip()
    if not ident or any(c not in "0123456789abcdef" for c in ident) or len(ident) != 64:
        raise ValueError("blob sha256 must be 64 lowercase hex chars")
    suffix = ".gz" if compression == "gzip" else ""
    e = str(ext or "bin").lstrip(".")
    return f"{ident}.{e}{suffix}"


def blob_path(
    *, blobs_dir: Path, sha256_hex: str, ext: str, compression: BlobCompression
) -> Path:
    return blobs_dir / blob_filename(
        sha256_hex=sha256_hex, ext=ext, compression=compression
    )


@dataclass(frozen=True)
class BlobRef:
    sha256: str
    relpath: str
    bytes_len: int
    compression: BlobCompression


def write_blob(
    *,
    blobs_dir: Path,
    data: bytes,
    ext: str,
    compression: BlobCompression = "none",
    expected_sha256: Optional[str] = None,
) -> BlobRef:
    raw = bytes(data)
    computed = sha256_bytes(raw)
    if expected_sha256 is not None and str(expected_sha256) != computed:
        raise ValueError("blob content sha256 mismatch")

    payload = gzip.compress(raw) if compression == "gzip" else raw
    p = blob_path(
        blobs_dir=blobs_dir, sha256_hex=computed, ext=ext, compression=compression
    )

    if p.exists():
        existing = p.read_bytes()
        if existing != payload:
            raise ValueError("blob path exists with different content")
        rel = p.as_posix()
        return BlobRef(
            sha256=computed,
            relpath=rel,
            bytes_len=len(raw),
            compression=compression,
        )

    blobs_dir.mkdir(parents=True, exist_ok=True)
    p.write_bytes(payload)
    rel = p.as_posix()
    return BlobRef(
        sha256=computed,
        relpath=rel,
        bytes_len=len(raw),
        compression=compression,
    )


def write_blob_text(
    *,
    blobs_dir: Path,
    text: str,
    ext: str,
    compression: BlobCompression = "none",
    expected_sha256: Optional[str] = None,
) -> BlobRef:
    return write_blob(
        blobs_dir=blobs_dir,
        data=str(text or "").encode("utf-8"),
        ext=ext,
        compression=compression,
        expected_sha256=expected_sha256,
    )


__all__ = [
    "BlobCompression",
    "BlobRef",
    "blob_path",
    "sha256_bytes",
    "sha256_text",
    "write_blob",
    "write_blob_text",
]
