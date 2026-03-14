---
description: Parallel search - fan out across internet and resources for information
---

# Hunt

Parallel search mode. Fans out across multiple data sources simultaneously to gather information, research topics, and find answers.

**Hunt searches for things. For building, use `/geepers-swarm`. For everything at once, use `/geepers-team`.**

## Execute

### 1. Analyze the Question

What are we looking for?
- Parse the topic/question in $ARGUMENTS
- Identify what kinds of sources would be most useful
- Determine search breadth (narrow technical vs broad research)

### 2. Dispatch Searchers (launch ALL in the SAME message)

Fan out across all relevant sources:

| Agent | Searches |
|-------|----------|
| **@geepers_searcher** | Web search, documentation, Stack Overflow, forums |
| **@geepers_fetcher** | Fetch specific URLs, API docs, reference pages |
| **@geepers_data** | Datasets, databases, structured data sources |
| **@geepers_links** | Link discovery, resource validation, related pages |
| **@geepers_citations** | Academic papers, prior art, research publications |

### 3. Aggregate Findings

After all agents return:
- Deduplicate results (same source found by multiple agents)
- Cross-reference claims (did multiple sources confirm the same thing?)
- Rank by relevance and reliability
- Flag contradictions between sources

### 4. Synthesize

Present unified findings:
```
Hunt Results: <topic>
---
Key Findings:
- <finding 1> [source]
- <finding 2> [source]

Consensus: <what most sources agree on>
Contradictions: <where sources disagree>
Gaps: <what we couldn't find>

Sources: <count> sources consulted
```

## Available Data Sources

Via MCP data-fetch server and web search:
arXiv, GitHub, news, Wikipedia, PubMed, Census, Weather, SEC filings, and more.

## Distinction

| Mode | Purpose | Agents |
|------|---------|--------|
| **Hunt** | Parallel SEARCHING | searcher, fetcher, data, links, citations |
| **Swarm** | Parallel BUILDING | builder, quickwin, refactor, integrator |
| **Team** | EVERYTHING at once | all relevant agents, no filter |

## Target

**Question/topic**: $ARGUMENTS

If no arguments, ask what needs to be researched.
