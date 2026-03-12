# Vacancy orchestrator usage

Use this guide to run a full vacancy refresh with **`vacancy-orchestrator`** from **Cursor** or **Gemini CLI**.

## Prerequisites

- **`job/job-channels.md`** — static list of channel/RSS URLs only (no bookmarks).
- **`job/channel-checkpoints.json`** — live checkpoints, **`updated_at_utc`**, per-channel **`status`**, **`last_relevant_url`**, etc.
- Matching output: **`job/positions.md`**, **`job/skills.md`**.

Agent specs: [`ai/agents/`](agents/). Gemini: `/agents reload`.

## Recommended prompts

### Full end-to-end refresh

```text
Run vacancy-orchestrator end-to-end.
Read channel URLs from job/job-channels.md; update only job/channel-checkpoints.json for state.
Use resume baseline https://dzmitrykashlach.github.io/resume/en.
Run collector -> analyst -> editor, then report changes and counts.
```

### Strict backend-only pass

```text
Run vacancy-orchestrator with strict conservative JVM/backend filtering.
Update checkpoints JSON and positions/skills; keep job-channels.md URL-only.
```

### Dry-run

```text
Dry-run vacancy-orchestrator: collect + analyze; show proposed checkpoint and table edits without writing files.
```

## Expected output checklist

- **`job/channel-checkpoints.json`**: **`updated_at_utc`** and per-channel **`checked_at_utc`** / **`status`** / **`last_relevant_url`** as applicable.
- **`job/job-channels.md`**: unchanged structure (single-column URLs only).
- **`job/positions.md`** / **`job/skills.md`** updated.
- Brief report: counts, failures (from JSON **`status`**), top skill gaps.

## Troubleshooting

- **`401 No access`** / **`Parse failed`** → recorded in JSON only.
- **`No match`** → **`last_relevant_url`**: `null`, appropriate **`status`**.
- Never restore bookmark columns to **`job/job-channels.md`**.
