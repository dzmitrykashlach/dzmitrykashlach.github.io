---
name: vacancy-quality-audit
description: Audit job artefacts for stale data, malformed links/tables, checkpoint consistency.
model: inherit
---
# Vacancy Quality Audit

Use this skill after updates to verify output quality.

## Checks
1. **`job/channel-checkpoints.json`** has **`updated_at_utc`** in UTC format when a run completed.
2. **`job/job-channels.md`** is **URL-only** (no “Last processed post”, no **Last results** line).
3. Each URL in **`job/job-channels.md`** has a corresponding entry in **`job/channel-checkpoints.json`** after a full run (or document missing as new sources).
4. **`status`** values in JSON are consistent with outcomes (`Match`, `No match`, `Parse failed`, `401 No access`).
5. **`job/positions.md`** / **`job/skills.md`** tables valid; links canonical where possible.
6. No stale duplicate state between markdown and JSON (markdown must not recreate bookmark columns).

## Output
- List pass/fail per check and suggested fixes.
