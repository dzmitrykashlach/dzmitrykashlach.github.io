---
name: refresh-job-channels
description: Update channel-checkpoints.json from a crawl; keep job-channels.md as URL-only input.
model: inherit
---
# Refresh Job Channels

Use this skill when asked to refresh vacancy processing results.

## Steps
1. Open **`job/job-channels.md`** — confirm it remains a **list of channel URLs only** (no bookmarks or timestamps).
2. Update **`job/channel-checkpoints.json`**:
   - Root **`updated_at_utc`** when the run completes.
   - Per channel: **`last_post_id`** / **`last_post_hash`**, **`last_relevant_url`**, **`status`**, **`checked_at_utc`** as applicable.
   - **`401 No access`** on access failure.
   - **`Parse failed`** when access succeeds but parsing fails after retry.
   - Checkpoint **`No match`** when parse succeeds with no relevant vacancy.
3. Do **not** add a second column or “Last results” to **`job/job-channels.md`**.
4. Ensure error **`status`** values are recorded in JSON (not duplicated as extra markdown columns).
5. Keep markdown table formatting valid for the single-column URL table.

## Output
- Briefly summarize updated channels and access failures using checkpoint **`status`** fields.
