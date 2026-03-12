# Vacancy Processing Instructions

Orchestrator and subagent specs live under **`ai/agents/`** (Cursor uses them through the `.cursor` → `ai` symlink; Gemini CLI uses `.gemini/agents` → `ai/agents`). See `ai/README.md` and `GEMINI.md`.

## Scope
- **Channel list (input only):** `job/job-channels.md` — one table of source URLs; do not store crawl or match state there.
- **Live state:** `job/channel-checkpoints.json` — per-channel `last_post_id` / `last_relevant_url` / `status` (`Match` | `No match` | `Parse failed` | `401 No access`) / `checked_at_utc`; root **`updated_at_utc`** replaces a separate “Last results” line in markdown.
- **Outputs:** `job/positions.md` (matching posts), `job/skills.md` (skill gaps).

Source profile for matching: `https://dzmitrykashlach.github.io/resume/en`.

## Workflow Contract
- Update **`updated_at_utc`** (and per-channel **`checked_at_utc`**) on each full processing run via `job/channel-checkpoints.json` only.
- Read channel URLs from `job/job-channels.md`; merge new URLs into `channel-checkpoints.json` when the list grows.
- Use incremental checkpoints from `job/channel-checkpoints.json`: parse posts newer than stored state when implementing incremental crawl.
- Keep checkpoint entries with access/parsing failures documented in JSON (`401 No access`, `Parse failed`). Ordering of channels in markdown is alphabetical or manual; ordering of failures is not duplicated in markdown.
- Keep resume-aligned vacancies only in `job/positions.md` and `job/skills.md`.

## Data Rules (checkpoints JSON)
- If a channel yields a relevant vacancy match, set **`last_relevant_url`** to that canonical post and **`status`** to `Match`.
- If parsing succeeds but no JVM-match: **`last_relevant_url`**: `null`, **`status`**: `No match`.
- If channel access fails: **`status`**: `401 No access`; leave post fields unset or stale as appropriate for the failure mode.
- If reachable but parsing fails after retry on rendered content: **`status`**: `Parse failed`.
- Preserve the channel URL list in `job/job-channels.md` unless the user explicitly asks to add/remove sources.

## Formatting Rules
- Keep `job/job-channels.md` as a single-column URL table (or equivalent list) plus short documentation.
- Keep markdown tables valid in `job/positions.md` and `job/skills.md`.
- Keep links canonical (`https://t.me/...` where possible).

## Safety
- Do not edit generated content in `_site/**`.
- Do not edit `node_modules/**`.
- Keep changes minimal and limited to vacancy-processing artifacts.
