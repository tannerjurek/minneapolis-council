# Next Steps

This project should move from planning to a small, auditable prototype before building a scraper or dashboard. The immediate goal is to prove that agenda items can be matched to meeting-video time ranges accurately enough to support analysis.

## Next 7 days

1. **Pick a narrow first sample.** Use 5 recent City Council meetings and 5 recent committee meetings so the sample includes both formal council action and committee-level discussion.
2. **Create a meeting inventory.** For each meeting, record the date, body, agenda URL, marked-agenda URL, video URL, and whether captions or video chapters are available using `data/meetings.example.csv` as the template.
3. **Manually segment the videos.** Record start and end timestamps for each agenda item in `data/manual_segments.example.csv` format.
4. **Assign first-pass policy labels.** Use the README taxonomy and mark uncertain labels as `Other / unclear` rather than guessing.
5. **Build the first chart from the manual sample.** Start with minutes by policy area because it directly tests whether the taxonomy and segmentation are useful.
6. **Write down every ambiguity.** Track unclear agenda items, missing timestamps, consent-calendar items, public-comment blocks, and mismatches between the agenda and the video.

## Prototype acceptance criteria

The prototype is ready to automate only when all of these are true:

- At least 10 meetings are represented in a single normalized CSV or database table.
- At least 90% of agenda items in the sample have a start time, end time, and duration.
- Every segment has a `segmentation_method` value such as `manual`, `chapter`, `caption_match`, or `estimated`.
- Every policy label has a `confidence_score` or a reviewer note.
- A reviewer can click from a chart back to the meeting agenda and video source.
- The project has a short methodology note explaining what meeting time can and cannot prove.

## First implementation tasks

1. Replace the example rows in `data/meetings.example.csv` and `data/manual_segments.example.csv` with real reviewed data.
2. Run `scripts/validate_segments.py` to check columns, timestamps, durations, confidence scores, and policy labels.
3. Run `scripts/summarize_time_by_policy.py` to aggregate total minutes by `policy_area`.
4. Run `scripts/chart_policy_area_minutes.py` to generate a static SVG chart from the summary.
5. Update `docs/methodology.md` with meeting-selection and coding decisions from the manual review.
6. Only after those work, automate LIMS extraction and transcript matching.

## Do not build yet

Avoid these until the manual prototype works:

- Fully automated scraping for multiple years.
- Council-member ranking by speaking time.
- LLM-only policy classification without human review.
- Complex effectiveness scores that combine unrelated ideas like speed, importance, and disagreement.
