# DAMN Harness Contract

DAMN defines the research protocol; the host creates and runs agents. A host adapter
must never be inferred from a product name alone. Probe capabilities at runtime and
fall back to the current agent when a capability is unavailable.

## Runtime objects

### CapabilityProfile

Record `available`, `unavailable`, or `unknown` for `subagents`, `parallel`,
`resume`, `cancel`, `persistent_files`, `browser`, `search`, `mcp`, `code_execution`,
and `structured_output`. Include the probe time and limitations.

### TaskGraph

Each node has `id`, `goal`, `inputs`, `allowed_tools`, `depends_on`, `parallel_group`,
`budget`, `success_criteria`, and `failure_policy`. Nodes must be independently
useful before they are scheduled in parallel. Fixed role lists are not a task graph.

### SpawnPolicy

Spawn only when at least one is true: source domains are independent, context must be
isolated, or an independent verification materially reduces risk. Set limits for
depth, instances, tool calls, tokens, and wall time. Stop workers that produce no new
evidence. Track critical-path time, not just the number of workers.

### EvidencePacket

Workers return a structured packet, not an unreviewed report. The canonical schema is
`references/evidence-packet.schema.json`. A partial worker failure must preserve
successful packets and return a typed error.

### Durable run state

When the host supports files, persist `brief.json`, `task-graph.json`,
`source-ledger.jsonl`, `claim-ledger.jsonl`, `open-gaps.json`, `evidence/`, and
`run-summary.json`. Resume from these artifacts, never from console output.

## Error and fallback contract

Distinguish startup/auth/config errors, transient network/rate-limit errors, permanent
source errors, criteria failures, timeout, permission denial, and worker execution
failure. Retry the same strategy only for transient errors. Use the next strategy after
a permanent error or failed success criteria. A fallback result must be marked
`fallback_won` and may require human review.

## Host mapping

- Claude Code: native subagent/task mechanism plus filesystem packets.
- Cursor: native Agent/Task; Cursor SDK is an optional adapter implementation.
- Codex: native task capability when exposed; otherwise serial fallback.
- Kimi Code: native team/subagent capability when exposed; filesystem packet protocol
  remains the stable boundary.
- Grok: Bot/Workspace/tool capability only when the account exposes it; web Chat
  teammates must not be assumed to be externally programmable.

All adapters return `run_id`, `agent_id`, `status`, `packet_ref`, `error_type`,
`retryable`, and `budget_used`.
