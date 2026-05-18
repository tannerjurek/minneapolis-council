#!/usr/bin/env python3
"""Summarize manually segmented meeting time by policy area."""

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate manual segment durations by policy area."
    )
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="data/manual_segments.csv",
        help="Path to manual segments CSV. Defaults to data/manual_segments.csv.",
    )
    parser.add_argument(
        "--output",
        default="outputs/policy_area_minutes.csv",
        help="Output summary CSV path. Defaults to outputs/policy_area_minutes.csv.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv)
    output_path = Path(args.output)

    totals: dict[str, dict[str, float]] = defaultdict(
        lambda: {"item_count": 0, "total_seconds": 0}
    )

    with input_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            policy_area = row["policy_area"] or "Other / unclear"
            totals[policy_area]["item_count"] += 1
            totals[policy_area]["total_seconds"] += int(row["duration_seconds"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as csv_file:
        fieldnames = ["policy_area", "item_count", "total_seconds", "total_minutes"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for policy_area, values in sorted(
            totals.items(), key=lambda item: item[1]["total_seconds"], reverse=True
        ):
            total_seconds = int(values["total_seconds"])
            writer.writerow(
                {
                    "policy_area": policy_area,
                    "item_count": int(values["item_count"]),
                    "total_seconds": total_seconds,
                    "total_minutes": round(total_seconds / 60, 2),
                }
            )

    print(f"Wrote {len(totals)} policy area row(s) to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
