from __future__ import annotations

import argparse
import difflib
from collections.abc import Collection, Mapping, Sequence


class ArgParseError(RuntimeError):
    pass


class StrictArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ArgParseError(message)


def did_you_mean(
    value: str,
    choices: Sequence[str],
    *,
    n: int = 3,
    cutoff: float = 0.6,
) -> list[str]:
    v = str(value or "").strip()
    if not v:
        return []
    return difflib.get_close_matches(v, list(choices), n=n, cutoff=cutoff)


def rewrite_flag_aliases(
    argv: Sequence[str],
    aliases: Mapping[str, str],
) -> list[str]:
    out: list[str] = []
    alias_prefixes = tuple(f"{src}=" for src in aliases)
    for tok in argv:
        mapped = aliases.get(tok)
        if mapped is not None:
            out.append(mapped)
            continue
        if alias_prefixes and tok.startswith(alias_prefixes):
            for src, dst in aliases.items():
                prefix = f"{src}="
                if tok.startswith(prefix):
                    out.append(dst + tok[len(src) :])
                    break
            else:
                out.append(tok)
            continue
        out.append(tok)
    return out


def split_short_value_flags(
    argv: Sequence[str],
    value_flags: Collection[str],
) -> list[str]:
    out: list[str] = []
    for tok in argv:
        if len(tok) > 2 and tok.startswith("-") and not tok.startswith("--"):
            flag = tok[:2]
            if flag in value_flags:
                value = tok[2:]
                if value:
                    out.extend([flag, value])
                    continue
        out.append(tok)
    return out


__all__ = [
    "ArgParseError",
    "StrictArgumentParser",
    "did_you_mean",
    "rewrite_flag_aliases",
    "split_short_value_flags",
]
