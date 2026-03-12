# Gemini CLI — project context

Vacancy tooling for this repo is driven by **`ai/agents/vacancy-orchestrator.md`** after `collector` → `analyst` → `editor`.

- **Agents (subagents):** [`ai/agents/`](ai/agents/) — same Markdown as Cursor; reload with `/agents reload`.
- **Human-readable rules:** [`ai/rules/`](ai/rules/) — vacancy process and Jekyll safety; encode critical bits in prompts when running headless Gemini.
- **Working agreement:** [`AGENTS.md`](AGENTS.md).

Resume baseline for matching: `https://dzmitrykashlach.github.io/resume/en`.

**Data split:** `job/job-channels.md` = URL list only; `job/channel-checkpoints.json` = all crawl/match timestamps and bookmarks.
