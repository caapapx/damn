# Research Quality Gates

## Source gate

Every accepted source must have a provider, strategy and attempt ID, canonical URL,
retrieval time, locator, and content hash where content was fetched. Track source
family and original/repost relationship so repeated syndication is not counted as
independent confirmation.

## Claim gate

Every externally verifiable claim in the final report must map to one or more source
IDs or an L1 experiment. Claims without support are removed, downgraded to inference,
or explicitly marked unverified.

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
