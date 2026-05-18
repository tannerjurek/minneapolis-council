#!/usr/bin/env python3
"""Summarize agenda-item counts by policy area before timestamps are available."""

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate agenda-item counts by policy area."
    )
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="data/agenda_items.csv",
        help="Path to agenda items CSV. Defaults to data/agenda_items.csv.",
    )
    parser.add_argument(
        "--output",
        default="outputs/policy_area_item_counts.csv",
        help="Output summary CSV path. Defaults to outputs/policy_area_item_counts.csv.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv)
    output_path = Path(args.output)

    totals: dict[str, int] = defaultdict(int)
    with input_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or "policy_area" not in reader.fieldnames:
            raise SystemExit("ERROR: input CSV must include a policy_area column")
        for row in reader:
            policy_area = row["policy_area"] or "Other / unclear"
            totals[policy_area] += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as csv_file:
        fieldnames = ["policy_area", "item_count"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for policy_area, item_count in sorted(
            totals.items(), key=lambda item: item[1], reverse=True
        ):
            writer.writerow({"policy_area": policy_area, "item_count": item_count})

    print(f"Wrote {len(totals)} policy area row(s) to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
