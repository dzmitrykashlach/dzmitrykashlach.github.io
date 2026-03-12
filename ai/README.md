# Project AI instructions (multi-tool layout)

Canonical copy lives under **`ai/`**. Tool-specific entry points are thin symlinks so Cursor and Gemini CLI resolve the same files.

| Area | Canonical path | Cursor | Gemini CLI |
|:-----|:---------------|:-------|:-------------|
| Subagents | `ai/agents/*.md` | Loaded via symlink `.cursor` → `ai` | [`/agents reload`](https://geminicli.com/) discovers `.gemini/agents/` → `ai/agents` |
| Rules | `ai/rules/*.mdc` | Cursor `.mdc` rules (glob + `alwaysApply`) | Reference from prompts or [`GEMINI.md`](../GEMINI.md); Gemini does not execute `.mdc` natively |
| Skills | `ai/skills/*/SKILL.md` | Cursor Agent Skills | Not used by Gemini CLI unless copied into an agent prompt |

## Conventions

- **Agents:** Markdown with YAML frontmatter — `name` (kebab-case, matches filename), `description` (single line), `model: inherit` unless you override.
- **Rules:** `.mdc` with YAML frontmatter — `description`, optional `globs`, optional `alwaysApply`.
- **Skills:** `SKILL.md` with YAML frontmatter — `name`, `description`.

## Symlinks (committed)

- `.cursor` → `ai` — Cursor IDE resolves its usual `.cursor/rules` paths.
- `.gemini/agents` → `../ai/agents` — Gemini CLI project subagents.

Optional local Gemini settings: `.gemini/settings.json` (gitignored).

## Vacancy pipeline data

| File | Role |
|:-----|:-----|
| `job/job-channels.md` | Input: list of channel/RSS URLs only |
| `job/channel-checkpoints.json` | Live state: checkpoints, `updated_at_utc`, per-channel `status` / `last_relevant_url` |
