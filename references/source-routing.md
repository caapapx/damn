# Source Routing

There is no global search primary. Route by intent, domain, freshness, and required
authority. A purchased provider is only an available adapter until benchmarked.

## Intent matrix

| Intent | Preferred source | Search adapters | Deep-read path |
| --- | --- | --- | --- |
| Local implementation | repository, tests, runtime | none | Read/Grep/semantic index |
| GitHub implementation | GitHub API/MCP, fixed commit | Brave/Exa for discovery | GitHub contents/raw |
| Official capability | vendor docs, API, changelog | any locator | official page/PDF |
| Academic | OpenAlex, Crossref, Semantic Scholar | Exa/Brave | paper/preprint/full text |
| Realtime | official announcement, feed, X | Brave News/GDELT/X | original post/page |
| Semantic landscape | independent search indexes | Exa, Brave, Tavily | Firecrawl/Crawl4AI |
| Exact SERP | SERP provider | SerpApi if required | result page and target URL |
| Restricted source | authorized API/browser/export | search only for discovery | authorized browser or user file |

## Adapter order

1. Use an authoritative vertical adapter when one exists.
2. Otherwise route general discovery by `search_intent`: exact/general, semantic,
   realtime, or exact SERP.
3. Use search output only as candidates. Fetch the original page before adopting a
   claim.
4. Select the lowest-cost sufficient reader: direct HTTP/WebFetch, Firecrawl,
   Crawl4AI, then authorized browser.
5. Record provider health and benchmark results. Do not hard-code Brave, Exa, or
   Tavily as universal primary.

## Search intent fields

```yaml
search_intent:
  kind: exact | semantic | landscape | realtime | vertical
  domain: code | academic | news | social | official_docs | general
  freshness_required: high | medium | low
  primary_source_required: true
  languages: [zh-CN, en]
  storage_required: false
```

## Configured adapters

```yaml
adapters:
  brave:
    kind: general_web_search
    credential_ref: env:BRAVE_API_KEY
    status: candidate
  firecrawl:
    kind: reader_crawler
    status: existing
  exa:
    kind: semantic_search
    status: trial
  searxng:
    kind: self_hosted_metasearch
    status: fallback
```

Secrets, cookies, and tokens never belong in this file or in manifests.
