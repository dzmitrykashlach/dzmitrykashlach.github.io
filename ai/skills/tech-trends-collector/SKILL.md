---
name: tech-trends-collector
description: Extract major, critical, and blocker changes from curated release sources.
model: inherit
---
# Tech Trends Collector Skill

Use this skill when asked to review `tech-trends/tech-trends.md` and produce high-priority change intelligence.

## Goal
Return only actionable high-impact updates across Keycloak, Quarkus, Spring Framework, JDK, and Kotlin.
Maintain incremental state in `tech-trends/tech-trends-checkpoints.json` and write weekly findings to `tech-trends/tech-trends-weekly.md`.

## Steps
1. Read `tech-trends/tech-trends.md` and `tech-trends/tech-trends-checkpoints.json`.
2. Visit each URL and collect only updates from the last 7 days (UTC).
3. Deduplicate overlapping announcements and prefer canonical release notes/changelogs.
4. Extract findings only when they match one of the severities:
   - `Blocker`: upgrade stopper, mandatory migration step, known issue preventing rollout.
   - `Critical`: security fixes, breaking changes, compatibility hazards, serious regressions.
   - `Major`: notable platform/framework/runtime features or behavior changes affecting architecture or delivery.
5. For each finding capture:
   - Ecosystem
   - Severity
   - Change title
   - Why it matters
   - Recommended action
   - Source URL
6. Write the run output to `tech-trends/tech-trends-weekly.md`.
7. Update `tech-trends/tech-trends-checkpoints.json`:
   - Root `updated_at_utc`
   - Per source URL: `last_checked_at_utc`, `last_item_published_at_utc`, `last_relevant_url`, `status`
8. If no qualifying items are found for a source in the last week, set `last_relevant_url` to `null` and `status` to `No match`.
9. If source cannot be accessed, use `401 No access`; if parsed content is unusable after retry, use `Parse failed`.

## Output Template
- `<Ecosystem>`
  - `[Severity] <Title>` - Why it matters. Action: <recommended action>. Source: <URL>

## Quality Rules
- Keep statements factual and traceable to a cited URL.
- Do not include minor bugfixes unless they create a critical/blocker impact.
- Keep wording concise and decision-ready.
- Keep checkpoints deterministic so reruns are reproducible.
