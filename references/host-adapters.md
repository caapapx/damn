# Host Adapter Notes

DAMN does not call host APIs directly. The adapter belongs to the Code Agent harness.

| Host | Preferred native path | Fallback |
| --- | --- | --- |
| Claude Code | native subagents/tasks | current agent serial execution |
| Cursor | native agents/tasks or Cursor SDK | current agent serial execution |
| Codex | native task/subagent capability when exposed | current agent serial execution |
| Kimi Code | native team/subagent capability when exposed | packet files and serial execution |
| Grok | exposed Bot/Workspace tools only | main Chat task decomposition |

The adapter must probe capability at runtime and return a typed run receipt. Product
marketing or a visible UI entry is not evidence that external spawning is available.

## Cursor tool surface → source-routing slots

Wish-list names in `source-routing.md` (Brave/Exa/Tavily) are often **not** mounted.
Map what the session actually exposes:

| Routing slot | Typical Cursor session tools | Notes |
| --- | --- | --- |
| Discovery A | Host `WebSearch` (if present) | Prefer as second discovery channel |
| Discovery B | `user-firecrawl` → `firecrawl_search` | Valid adapter, **not** global primary |
| Reader (cheap) | Host `WebFetch` / `mcp_web_fetch` | Use for known official URLs / `.md` |
| Reader (heavy) | `user-firecrawl` → `firecrawl_scrape` | After fetch fail or JS-heavy pages |
| GitHub vertical | `user-github` / `gh` | Prefer over search snippets for repos |
| Docs / library API | Context7 MCP if present | Prefer for current API surface |
| Agent Reach | CLI `agent-reach doctor --json` | Optional; record unavailable if missing |

### Anti-patterns on Cursor

- Using only `user-firecrawl` for both search and deep-read without CapabilityProfile
  and `fallback_won`.
- Scraping `https://…/docs/…` when `…/docs/….md` or WebFetch would suffice.
- Treating Firecrawl MCP presence as proof that Brave/Exa were "selected against".

If the session only has Firecrawl for web discovery: still probe, still prefer
WebFetch/GitHub verticals for deep-read, set `single_adapter_reason`, and cap
confidence per `quality-gates.md` Routing gate.
