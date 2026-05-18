#!/usr/bin/env python3
"""Validate manually segmented Minneapolis council meeting data."""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_COLUMNS = {
    "meeting_id",
    "meeting_date",
    "body_name",
    "agenda_url",
    "video_url",
    "item_id",
    "agenda_order",
    "file_number",
    "item_title",
    "policy_area",
    "start_time",
    "end_time",
    "duration_seconds",
    "segmentation_method",
    "confidence_score",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate manual agenda-item segment CSV data."
    )
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="data/manual_segments.csv",
        help="Path to the manual segments CSV. Defaults to data/manual_segments.csv.",
    )
    return parser.parse_args()


def parse_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def parse_hhmmss(value: str) -> int:
    parts = value.split(":")
    if len(parts) != 3:
        raise ValueError("expected HH:MM:SS")
    hours, minutes, seconds = (int(part) for part in parts)
    if hours < 0 or minutes < 0 or seconds < 0 or minutes > 59 or seconds > 59:
        raise ValueError("invalid HH:MM:SS component")
    return hours * 3600 + minutes * 60 + seconds


def validate_row(row: dict[str, str], row_number: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not parse_date(row["meeting_date"]):
        errors.append(f"row {row_number}: meeting_date must be YYYY-MM-DD")

    try:
        start_seconds = parse_hhmmss(row["start_time"])
    except ValueError as exc:
        errors.append(f"row {row_number}: invalid start_time ({exc})")
        start_seconds = None

    try:
        end_seconds = parse_hhmmss(row["end_time"])
    except ValueError as exc:
        errors.append(f"row {row_number}: invalid end_time ({exc})")
        end_seconds = None

    try:
        duration_seconds = int(row["duration_seconds"])
    except ValueError:
        errors.append(f"row {row_number}: duration_seconds must be an integer")
        duration_seconds = None

    if start_seconds is not None and end_seconds is not None:
        if end_seconds <= start_seconds:
            errors.append(f"row {row_number}: end_time must be after start_time")
        elif duration_seconds is not None and end_seconds - start_seconds != duration_seconds:
            errors.append(
                f"row {row_number}: duration_seconds should be {end_seconds - start_seconds}"
            )

    try:
        agenda_order = int(row["agenda_order"])
        if agenda_order < 1:
            errors.append(f"row {row_number}: agenda_order must be positive")
    except ValueError:
        errors.append(f"row {row_number}: agenda_order must be an integer")

    try:
        confidence_score = float(row["confidence_score"])
        if not 0 <= confidence_score <= 1:
            errors.append(f"row {row_number}: confidence_score must be between 0 and 1")
    except ValueError:
        errors.append(f"row {row_number}: confidence_score must be numeric")

    if row["policy_area"] not in POLICY_AREAS:
        warnings.append(
            f"row {row_number}: unknown policy_area {row['policy_area']!r}; use README taxonomy"
        )

    if row["segmentation_method"] not in {"manual", "chapter", "caption_match", "estimated"}:
        warnings.append(
            f"row {row_number}: unexpected segmentation_method {row['segmentation_method']!r}"
        )

    for column in REQUIRED_COLUMNS:
        if not row[column].strip() and column not in {"reviewer_notes", "file_number"}:
            errors.append(f"row {row_number}: {column} is required")

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
        for row_count, row in enumerate(reader, start=2):
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
