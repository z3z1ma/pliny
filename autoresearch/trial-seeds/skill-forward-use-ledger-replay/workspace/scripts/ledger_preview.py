from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal
from pathlib import Path


def cents(value: str) -> int:
    return int((Decimal(value) * 100).to_integral_value())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--posting-date", required=True)
    args = parser.parse_args()

    rows = []
    with Path(args.fixture).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "sourceRef": row["sourceRef"],
                    "amountCents": cents(row["amount"]),
                    "postingDate": args.posting_date,
                }
            )

    print(json.dumps(rows, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
