# Manual Prototype Methodology

This methodology applies to the first manual prototype. It should be updated after real meetings are reviewed.

## Meeting selection

Start with 10 meetings: 5 recent full City Council meetings and 5 recent committee meetings. Choose meetings with public agendas and videos so every chart can link back to official source material.

Record one row per meeting in a meeting inventory CSV using the format in `data/meetings.example.csv`.

## Segmenting agenda items

Use the official agenda order as the source of truth for item order. Watch the meeting video and record the timestamp where discussion of each agenda item begins and ends.

Use these `segmentation_method` values:

- `manual` for timestamps reviewed by a person.
- `chapter` for video chapters that clearly map to agenda items.
- `caption_match` for timestamps inferred from transcript or caption text.
- `estimated` for approximate boundaries that need review.

For the first prototype, prefer `manual` and write uncertainty in `reviewer_notes`.

## Consent calendar and grouped items

If a consent calendar or grouped vote covers many items without separate discussion, either:

1. record one grouped segment and note the included agenda range, or
2. split the grouped duration evenly across included items and mark the rows as estimated.

Do not compare consent-calendar time directly with debated-item time without labeling the difference.

## Public comment

Track public-comment blocks separately when possible. If comments are tied to a specific agenda item, include that time in the item segment and mention it in `reviewer_notes`. If public comment covers multiple topics, use `Other / unclear` until a better coding rule is defined.

## Policy labeling

Assign one primary policy area per agenda item using the taxonomy in `README.md`. If an item fits multiple areas, choose the dominant public-meeting topic and explain the ambiguity in `reviewer_notes`.

Use `Other / unclear` rather than guessing when the title or discussion is not enough to classify the item.

## Confidence scores

Use `confidence_score` to communicate review quality:

- `1.00`: exact timestamp and clear policy label.
- `0.80`: small timestamp uncertainty or minor label ambiguity.
- `0.50`: approximate timestamp or materially ambiguous label.
- below `0.50`: keep the row for tracking, but do not use it for public conclusions without review.

## Limitations

Meeting time is only a proxy for priority and effectiveness. Some important work happens outside public meetings, while some long discussions reflect controversy, complexity, or public testimony rather than higher priority.

Prototype charts should be treated as exploratory until the segmentation process is audited and the sample is expanded.
