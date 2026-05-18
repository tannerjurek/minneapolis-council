#!/usr/bin/env python3
"""Validate agenda-coded Minneapolis council item data before timestamps exist."""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_COLUMNS = {
    "meeting_id",
    "meeting_date",
    "body_name",
    "source_url",
    "item_id",
    "agenda_section",
    "agenda_order",
    "file_number",
    "item_title",
    "item_description",
    "policy_area",
    "action_taken",
    "coding_status",
    "reviewer_notes",
}

POLICY_AREAS = {
    "Housing and homelessness",
    "Public safety and emergency response",
    "Transportation, streets, and public works",
    "Budget, taxes, procurement, and finance",
    "Land use, zoning, planning, and development",
    "Climate, environment, and public health",
    "Labor, employment, and city operations",
    "Civil rights, equity, and community safety",
    "Licenses, permits, and business regulation",
    "Governance, elections, appointments, and procedure",
    "Arts, culture, parks, and public realm",
    "Other / unclear",
}

CODING_STATUSES = {
    "agenda_coded",
    "needs_review",
    "reviewed",
    "time_segmented",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate agenda-coded item CSV data.")
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="data/agenda_items.csv",
        help="Path to the agenda items CSV. Defaults to data/agenda_items.csv.",
    )
    return parser.parse_args()


def is_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_row(row: dict[str, str], row_number: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for column in REQUIRED_COLUMNS:
        if not row[column].strip() and column not in {"reviewer_notes", "file_number"}:
            errors.append(f"row {row_number}: {column} is required")

    if not is_date(row["meeting_date"]):
        errors.append(f"row {row_number}: meeting_date must be YYYY-MM-DD")

    try:
        agenda_order = int(row["agenda_order"])
        if agenda_order < 1:
            errors.append(f"row {row_number}: agenda_order must be positive")
    except ValueError:
        errors.append(f"row {row_number}: agenda_order must be an integer")

    if row["policy_area"] not in POLICY_AREAS:
        warnings.append(
            f"row {row_number}: unknown policy_area {row['policy_area']!r}; use README taxonomy"
        )

    if row["coding_status"] not in CODING_STATUSES:
        warnings.append(
            f"row {row_number}: unexpected coding_status {row['coding_status']!r}"
        )

    if row["source_url"] and not row["source_url"].startswith(("http://", "https://")):
        warnings.append(f"row {row_number}: source_url should be an absolute URL")

    return errors, warnings


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv)
    if not input_path.exists():
        print(f"ERROR: {input_path} does not exist", file=sys.stderr)
        return 2

    with input_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            print("ERROR: CSV is empty", file=sys.stderr)
            return 2

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            print(f"ERROR: missing required columns: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2

        row_count = 0
        errors: list[str] = []
        warnings: list[str] = []
        seen_item_ids: set[str] = set()
        for row_count, row in enumerate(reader, start=2):
            item_id = row["item_id"]
            if item_id in seen_item_ids:
                errors.append(f"row {row_count}: duplicate item_id {item_id!r}")
            seen_item_ids.add(item_id)

            row_errors, row_warnings = validate_row(row, row_count)
            errors.extend(row_errors)
            warnings.extend(row_warnings)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s).",
            file=sys.stderr,
        )
        return 1

    data_rows = max(row_count - 1, 0)
    print(
        f"Validation passed: {data_rows} row(s), {len(warnings)} warning(s), "
        f"source={input_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
