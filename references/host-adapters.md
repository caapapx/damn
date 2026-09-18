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
