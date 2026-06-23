from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


HEADER = (
    "timestamp",
    "experiment_id",
    "tier",
    "candidate",
    "score_vector",
    "status",
    "description",
)
STATUSES = ("keep", "discard", "mutate", "crash", "review")


class ResultsError(ValueError):
    pass


def init_ledger(path: str | Path, *, overwrite: bool = False) -> Path:
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    if ledger_path.exists() and not overwrite:
        existing = ledger_path.read_text(encoding="utf-8").splitlines()
        if existing and existing[0] == _header_line():
            return ledger_path
        raise ResultsError(f"{ledger_path}: exists with a different header")
    ledger_path.write_text(_header_line() + "\n", encoding="utf-8")
    return ledger_path


def append_row(
    path: str | Path,
    *,
    experiment_id: str,
    tier: str,
    candidate: str,
    score_vector: str,
    status: str,
    description: str,
    timestamp: str | None = None,
) -> Path:
    ledger_path = Path(path)
    _require_header(ledger_path)
    if status not in STATUSES:
        raise ResultsError(f"status must be one of: {', '.join(STATUSES)}")
    row = {
        "timestamp": timestamp or _now(),
        "experiment_id": experiment_id,
        "tier": tier,
        "candidate": candidate,
        "score_vector": score_vector,
        "status": status,
        "description": description,
    }
    for field, value in row.items():
        _validate_cell(field, value)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write("\t".join(row[field] for field in HEADER) + "\n")
    return ledger_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage autoresearch results.tsv ledgers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--path", type=Path, default=Path("results.tsv"))
    init_parser.add_argument("--overwrite", action="store_true")

    append_parser = subparsers.add_parser("append")
    append_parser.add_argument("--path", type=Path, default=Path("results.tsv"))
    append_parser.add_argument("--experiment-id", required=True)
    append_parser.add_argument("--tier", required=True)
    append_parser.add_argument("--candidate", required=True)
    append_parser.add_argument("--score-vector", required=True)
    append_parser.add_argument("--status", required=True, choices=STATUSES)
    append_parser.add_argument("--description", required=True)
    append_parser.add_argument("--timestamp")

    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            path = init_ledger(args.path, overwrite=args.overwrite)
        else:
            path = append_row(
                args.path,
                experiment_id=args.experiment_id,
                tier=args.tier,
                candidate=args.candidate,
                score_vector=args.score_vector,
                status=args.status,
                description=args.description,
                timestamp=args.timestamp,
            )
    except (OSError, ResultsError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"wrote {path}")
    return 0


def _require_header(path: Path) -> None:
    try:
        first = path.read_text(encoding="utf-8").splitlines()[0]
    except FileNotFoundError as exc:
        raise ResultsError(f"{path}: initialize ledger first") from exc
    except IndexError as exc:
        raise ResultsError(f"{path}: missing header") from exc
    if first != _header_line():
        raise ResultsError(f"{path}: unexpected header")


def _validate_cell(field: str, value: str) -> None:
    if not value:
        raise ResultsError(f"{field} must not be empty")
    if "\t" in value or "\n" in value or "\r" in value:
        raise ResultsError(f"{field} must not contain tab or newline")
    if "," in value:
        raise ResultsError(f"{field} must not contain comma")


def _header_line() -> str:
    return "\t".join(HEADER)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
