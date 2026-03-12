---
name: dedupe-and-sort-channels
description: Normalize the URL list in job-channels.md; optional ordering of checkpoint entries.
model: inherit
---
# Dedupe And Sort Channels

Use this skill to clean the channel source list before or after updates.

## Steps
1. Inspect **`job/job-channels.md`** — one URL per row in the table (or bullet list).
2. Remove duplicate URLs while preserving order or sorting alphabetically if requested.
3. **`job/channel-checkpoints.json`:** merge duplicate keys if duplicates existed; optionally sort channel keys for readability (document if you reorder JSON).
4. Do **not** merge bookmark data in markdown — bookmarks exist only in JSON.

## Output
- Report duplicate URLs removed and whether **`job/channel-checkpoints.json`** was reconciled.
