#!/usr/bin/env python3
"""Create a simple SVG bar chart for policy-area meeting minutes."""

import argparse
import csv
from html import escape
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render policy-area minutes summary as an SVG bar chart."
    )
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="outputs/policy_area_minutes.csv",
        help="Policy-area summary CSV. Defaults to outputs/policy_area_minutes.csv.",
    )
    parser.add_argument(
        "--output",
        default="outputs/charts/policy_area_minutes.svg",
        help="Output SVG path. Defaults to outputs/charts/policy_area_minutes.svg.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv)
    output_path = Path(args.output)

    with input_path.open(newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    chart_rows = [
        (row["policy_area"], float(row["total_minutes"]), int(row["item_count"]))
        for row in rows
    ]
    max_minutes = max((minutes for _, minutes, _ in chart_rows), default=0)

    width = 960
    row_height = 44
    top = 64
    left = 300
    right = 40
    bar_max_width = width - left - right
    height = top + max(len(chart_rows), 1) * row_height + 36

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="36" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#1f2937">Meeting minutes by policy area</text>',
    ]

    if not chart_rows:
        lines.append(
            '<text x="24" y="84" font-family="Arial, sans-serif" font-size="16" fill="#6b7280">No rows to chart.</text>'
        )
    else:
        for index, (policy_area, minutes, item_count) in enumerate(chart_rows):
            y = top + index * row_height
            bar_width = 0 if max_minutes == 0 else (minutes / max_minutes) * bar_max_width
            lines.extend(
                [
                    f'<text x="24" y="{y + 24}" font-family="Arial, sans-serif" font-size="14" fill="#374151">{escape(policy_area)}</text>',
                    f'<rect x="{left}" y="{y + 6}" width="{bar_width:.1f}" height="24" rx="4" fill="#2563eb"/>',
                    f'<text x="{left + bar_width + 8:.1f}" y="{y + 24}" font-family="Arial, sans-serif" font-size="14" fill="#111827">{minutes:.2f} min ({item_count} item(s))</text>',
                ]
            )

    lines.append("</svg>")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n")
    print(f"Wrote chart to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
