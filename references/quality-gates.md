# Research Quality Gates

## Routing gate

Before accepting web-dependent conclusions:

1. Stage 2 includes a CapabilityProfile (doctor JSON or host MCP inventory)
   **internally** — the chat-facing Stage 2 card may summarize it in a table (see
   `presentation-widgets.md`); raw doctor walls in the user-visible reply fail the
   Presentation gate, not this gate.
2. Discovery used ≥2 adapters, or documented `single_adapter_reason` + `fallback_won`.
   A call that errors or returns no hits does not count; see Discovery result gate.
3. Known canonical URLs were attempted with WebFetch/official `.md`/raw before crawl.
4. A single search+scrape MCP used as the entire stack without the above → **routing
   gate fail**; fix the run or lower confidence and disclose.

## Source gate

Every accepted source must have a provider, strategy and attempt ID, canonical URL,
retrieval time, locator, and content hash where content was fetched. Track source
family and original/repost relationship so repeated syndication is not counted as
independent confirmation.

## Claim gate

Every externally verifiable claim in the final report must map to one or more source
IDs or an L1 experiment. Claims without support are removed, downgraded to inference,
or explicitly marked unverified.

## Discovery result gate

Calling an adapter is not a successful discovery channel:

1. HTTP 4xx/5xx, tool error, empty result set, or a query that returns no usable hits → status `降级`, not `通过`.
2. At least **one** discovery channel must return a non-empty hit before the run can count toward the ≥2-adapter bar. Otherwise retry with a different query, `gh`, or WebFetch, or document `fallback_won`.
3. Confidence ≥80% with no effective hit → **gate fail**; lower confidence and disclose, or fix the run.

## L1 skip gate

When a decision sentence depends on "it runs if installed" or "an unknown product will be scanned this way", and the environment can execute a minimal check (CLI `--help`, local skill/path probe, a one-shot page action):

1. Do that minimal L1, **or** cap confidence at **75%** and name the measurement that was skipped.
2. README text and star counts are not L1.

## Presentation gate

Before accepting the user-visible final answer (any mode except pure tool-error stops):

1. **Decision surface**: Fast mode has the 5-block契约 and does **not** open with stage cards; standard/deep open with a
   decision card (conclusion + weight matrix + confidence).
2. **No duplicate executive summary**: Stage 3 findings are not restated as a second
   long摘要 in Stage 5.
3. **Stage 2 card**: CapabilityProfile / search_intent are not pasted as multi-line
   key:value walls; use the探测卡 tables (or a ≤6-row status table). Fast mode does not paste this card at all.
4. **Tables**: No table larger than 8×6 without an overview + appendix split; cells
   stay short.
5. **Flows**: Workflows use Mermaid (or a one-line `A → B → C` fallback), not ASCII
   box diagrams longer than 5 lines.
6. **Evidence**: Material numeric claims show L1–L4 nearby or in an evidence ledger.
7. **Length**: Deep mode over ~20% above `word-count-guide` must mark overflow as
   附录（默认不展开）.
8. **Fast mode stage cards**: A fast-mode final answer that contains `【阶段一】`, `【阶段二】`, `【阶段三】`, or a 「模式选择」 block → **fail**; strip them and resubmit.
9. **收束**: Standard/deep final answer has no `收束` block, or that block restates chapters (`第 N 节` / `第一节`) or rewrites the decision card → **fail**. Fast mode does not add this block.

Fail → fix layout before treating the research as complete.

## Citation audit

Before writing the final report:

1. Re-open the cited source or snapshot.
2. Verify that the locator supports the claim, not merely a nearby topic.
3. Check freshness, version and scope.
4. Check contradictions and source independence.
5. Reject search snippets as final evidence.

## Gap-driven follow-up

After each execution wave, list uncovered required claims, single-source high-risk
claims, stale sources, and contradictions. Create follow-up tasks only for those gaps.
Stop when coverage and support thresholds pass or the budget is exhausted.
