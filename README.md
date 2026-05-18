# Minneapolis Council Meeting-Time Analysis

This project is a research and visualization plan for measuring how the Minneapolis City Council spends meeting time, what priorities show up repeatedly, and whether items move efficiently from introduction to action.

## Core question

> How does the Minneapolis City Council allocate meeting time across policy areas, committees, council members, departments, neighborhoods, and procedural outcomes?

The goal is **not** to rank council members by raw speaking time alone. A useful analysis should separate routine consent items from debated items, distinguish policy substance from procedure, and connect time spent to outcomes such as approvals, referrals, continuances, amendments, and votes.

## Recommended MVP

Start with one year of meetings and build a repeatable pipeline before adding complex transcript analysis.

1. **Collect meeting metadata and agendas** from the City of Minneapolis Legislative Information Management System (LIMS).
2. **Collect linked meeting videos** from LIMS or the City's YouTube channel.
3. **Segment each meeting by agenda item** using LIMS agenda order, video chapters when available, and transcript timestamps.
4. **Classify each agenda item** by policy area, department, file type, committee, author, ward, neighborhood, action, and vote outcome.
5. **Visualize time allocation** across meetings, committees, policy areas, item types, and outcomes.
6. **Audit a sample manually** to estimate classification and timing error before publishing conclusions.

## Immediate next step

Move from planning to a small manual prototype. Start by filling out `data/manual_segments.example.csv` and `data/meetings.example.csv` for 5 recent City Council meetings and 5 recent committee meetings, then validate the rows and make the first "minutes by policy area" chart. The detailed checklist is in [`docs/next-steps.md`](docs/next-steps.md), and prototype coding rules are in [`docs/methodology.md`](docs/methodology.md).

## Best data sources

| Source | Why it matters | Notes |
| --- | --- | --- |
| [Minneapolis LIMS meeting information](https://lims.minneapolismn.gov/CityCouncil/Meetings) | Official agendas, marked agendas, proceedings, and linked videos | The City says agendas are published two business days before meetings; after meetings, agendas are marked with actions taken, and proceedings usually post after legal publication. |
| [Minneapolis City Council meetings page](https://www.minneapolismn.gov/government/city-council/meetings/) | Official landing page for calendars, agendas, video, LIMS, updates, and archives | The City describes LIMS as the place to see every agenda item, meeting subjects, videos, and past outcomes. |
| [LIMS about page](https://lims.minneapolismn.gov/home/about) | Explains LIMS fields and search/export behavior | LIMS provides file type, subcategory, department, author, ward, neighborhood, tag, date, term, meeting history, actions, votes, and attachments. |
| [Legistar Web API help](https://webapi.legistar.com/Help) | Structured API reference for events, event items, matters, histories, votes, and roll calls | Use if Minneapolis data is exposed through Legistar-compatible endpoints; otherwise scrape/export from LIMS CSVs and pages. |
| [City of Minneapolis YouTube channel](https://www.youtube.com/cityofminneapolis) | Video and captions/transcripts for meeting-time segmentation | Use video chapters when present; otherwise align transcript timestamps to agenda item titles and procedural phrases. |
| [Older meeting archive](https://wwwdocs.minneapolismn.gov) | Backfill historical agendas and proceedings | Use after the current LIMS pipeline works, because older records may be less structured. |

## Measures to calculate

### Time allocation

- Total meeting duration by body, committee, month, and year.
- Time per agenda item.
- Time per policy category, department, file type, ward, neighborhood, and tag.
- Share of time spent on consent agenda, public hearings, presentations, debate, amendments, voting, postponements, and administrative procedure.
- Agenda-position effects: whether late-agenda items receive less discussion time.

### Priority signals

- Repeated appearances of the same matter across meetings.
- Number of items by policy category compared with minutes spent per category.
- Items with high public-comment time or high amendment activity.
- Sponsor/author patterns for ordinances and resolutions.
- Departments or committees with rising or falling agenda share.

### Effectiveness and throughput

- Time from introduction to final action by file type and committee.
- Number of meetings an item appears on before disposition.
- Outcomes: approved, referred, continued, postponed, deleted, returned to author, received and filed.
- Vote patterns: unanimous, split, absent, abstain, or no recorded vote.
- Ratio of discussion time to outcome significance, while clearly labeling this as an interpretive metric.

## Suggested data model

```text
meetings
- meeting_id
- body_name
- committee_name
- meeting_date
- meeting_start_time
- agenda_url
- marked_agenda_url
- proceedings_url
- video_url
- video_duration_seconds

agenda_items
- item_id
- meeting_id
- agenda_order
- file_number
- title
- description
- file_type
- subcategory
- department
- author
- ward
- neighborhood
- tags
- action_taken
- vote_result
- consent_calendar_flag
- public_hearing_flag

segments
- segment_id
- meeting_id
- item_id
- start_seconds
- end_seconds
- duration_seconds
- segmentation_method
- confidence_score

votes
- vote_id
- item_id
- council_member
- vote
- roll_call_order

classifications
- item_id
- policy_area
- priority_theme
- classification_method
- confidence_score
- reviewer_notes
```

## Policy taxonomy

Use a small, stable taxonomy first so charts are interpretable. Add subcategories only when the broad categories work reliably.

- Housing and homelessness
- Public safety and emergency response
- Transportation, streets, and public works
- Budget, taxes, procurement, and finance
- Land use, zoning, planning, and development
- Climate, environment, and public health
- Labor, employment, and city operations
- Civil rights, equity, and community safety
- Licenses, permits, and business regulation
- Governance, elections, appointments, and procedure
- Arts, culture, parks, and public realm
- Other / unclear

## Visualization ideas

1. **Meeting timeline:** stacked bar for each meeting, colored by policy area or agenda section.
2. **Priority heatmap:** rows are committees or policy areas; columns are months; cells show minutes or item counts.
3. **Agenda funnel:** introduced → referred → amended → approved → enacted, with median days in each stage.
4. **Outcome scatterplot:** item duration vs. final outcome, sized by public-comment minutes or number of speakers.
5. **Council-member network:** sponsors, co-sponsors, amendments, and voting alignment, with strong caveats against overinterpretation.
6. **Consent vs. debated split:** share of items and share of minutes handled without discussion versus discussed individually.
7. **Department dashboard:** time and outcomes by originating department.
8. **Ward/neighborhood map:** count and duration of geographically tagged items.

## Current real data sample

The repo now includes the first real agenda-coded sample from the official marked agenda for the April 8, 2026 Minneapolis City Council adjourned meeting:

- `data/meetings.csv` has the meeting-level source record.
- `data/agenda_items.csv` has the substantive agenda item, action taken, and first-pass policy-area label.

This is agenda-coded data, not time-segmented data. The next research step is to watch the linked meeting video and add item start/end timestamps to `data/manual_segments.csv`.

## View the local site

This repo includes a static prototype site for viewing the manual CSV as a browser chart. From the repo root, run:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/site/>. The page loads `data/agenda_items.csv` by default and also lets you upload a reviewed `manual_segments.csv` file when timestamped data is ready.

## Manual prototype commands

Run these commands after replacing the example rows with reviewed meeting data:

```bash
python3 scripts/summarize_agenda_items_by_policy.py data/agenda_items.csv --output outputs/policy_area_item_counts.csv
python3 scripts/validate_segments.py data/manual_segments.example.csv
python3 scripts/summarize_time_by_policy.py data/manual_segments.example.csv --output outputs/policy_area_minutes.csv
python3 scripts/chart_policy_area_minutes.py outputs/policy_area_minutes.csv --output outputs/charts/policy_area_minutes.svg
```

## Practical pipeline

```text
extract
  -> LIMS meeting list, agenda PDFs/HTML, item pages, votes, attachments, video links
transform
  -> normalize identifiers, deduplicate files, parse agenda order, clean vote labels
segment
  -> derive item-level timestamps from chapters, transcripts, and manual review
classify
  -> rules first, then supervised/LLM-assisted labels with confidence scores
validate
  -> manual review sample, disagreement log, timing-error estimate
publish
  -> static dashboard, downloadable CSV, methodology notes, source links
```

## Recommended implementation phases

### Phase 1: Manual-proven prototype

- Pick 5-10 recent City Council and committee meetings.
- Manually label agenda item start/end times.
- Create a simple CSV and a notebook/dashboard.
- Confirm the taxonomy and visualizations are useful before automating.

### Phase 2: Semi-automated extraction

- Download/export LIMS meeting and agenda item data.
- Pull YouTube metadata and caption timestamps.
- Auto-match transcript sections to agenda item titles.
- Keep a manual override file for timing corrections.

### Phase 3: Scaled analysis

- Backfill one or more council terms.
- Add vote, author, department, ward, neighborhood, and tag analysis.
- Add confidence intervals or visible uncertainty bands for machine-classified fields.
- Publish a methodology page that explains what the dashboard can and cannot prove.

## Quality and ethics notes

- Meeting time is a **proxy**, not a complete measure of priority or effectiveness. Some high-priority work happens outside public meetings, and some routine items deserve little floor time.
- Avoid treating longer discussion as automatically better or worse.
- Separate public-comment time, staff-presentation time, council debate, and voting/procedure when possible.
- Preserve links back to official records so users can inspect context.
- Store model-generated classifications with confidence scores and review notes.
- Regularly audit samples for errors, especially for controversial topics or close votes.

## First charts to build

If you only build three charts, build these first:

1. **Minutes by policy area over time** to show changing priorities.
2. **Item throughput by file type and committee** to show process efficiency.
3. **Consent calendar vs. debated-item time** to separate routine legislative volume from contested work.

## Open questions

- Does LIMS expose a stable public JSON endpoint for Minneapolis, or should the project rely on CSV exports and page scraping?
- Are meeting video chapters consistently linked to agenda items?
- Are YouTube captions complete enough for automated segmentation, or is manual review required for all high-stakes analysis?
- Which definition of "effectiveness" is most useful: speed, completion rate, public deliberation, alignment with stated priorities, or something else?
