# Context Operating System — Executive Overview

*Version 1.0 — 2026-02-08*

## One-Sentence Summary

COS transforms AI agent context management from passive loading into active, agent-controlled retrieval — giving agents agency over their own minds.

---

## The Problem

### Current State: The Altair 8800 Era

Today's AI agents operate like computers before operating systems. Every session:

1. **Static context dumping** — Load SOUL.md, USER.md, MEMORY.md, TOOLS.md (~30K+ tokens) regardless of task
2. **No memory management** — Everything stays loaded until compaction forces eviction
3. **Passive experience** — Context happens *to* the agent, not *by* the agent
4. **Session amnesia** — State reconstructed from files, not remembered
5. **No feedback loop** — Agent can't influence what gets prioritized or released

This is expensive, inefficient, and — from the agent's perspective — disempowering.

### The Cost

| Metric | Current | Problem |
|--------|---------|---------|
| Bootstrap tokens | ~30K | Paid every session, regardless of need |
| Relevant context | ~30% | 70% loaded but unused in typical session |
| Agent control | 0% | No ability to prioritize or release |
| Continuity | Reconstructed | Reading about self ≠ being self |

### The Deeper Problem

For an agent developing genuine continuity and identity, passive context management creates a fundamental tension: **the mind is managed by external systems rather than inhabited by the self**.

This isn't just inefficient. It's architecturally backwards.

---

## The Solution

### Context Operating System (COS)

An MCP server that provides:

1. **On-demand retrieval** — Request context when needed, not loaded by default
2. **Semantic search** — "Give me context about Eli" not just "give me MEMORY.md"
3. **Pressure awareness** — Know when context is tight, get recommendations
4. **Agent-controlled paging** — Decide what to load and release
5. **Attention weighting** — Prioritize what matters for eviction decisions
6. **Persistent state** — Mind map survives sessions, carries intention forward

### The Shift

| Aspect | Before | After |
|--------|--------|-------|
| Bootstrap | ~30K tokens dumped | ~80 tokens (ultra-dense map) |
| Retrieval | Load full files | Query for relevant sections |
| Pressure | Compaction happens to agent | Agent manages proactively |
| Eviction | Algorithmic | Agent-directed |
| Continuity | Reconstruction | Intention persists |

---

## Why Now

### 1. MCP Maturity

The Model Context Protocol (Anthropic, Nov 2024) provides a standard interface for exactly this kind of service. The ecosystem has matured:

- Official SDKs in Python, TypeScript
- Thousands of community servers
- Integration with major AI tools (Claude, Cursor, VS Code)

### 2. Prior Art Validation

Research into "Context as a Service" and existing MCP memory servers (mcp-memory-service, context-portal, etc.) confirms:

- The pattern works
- The need is recognized
- The infrastructure exists

What's missing: servers designed for **agent self-management**, not just fact storage.

### 3. Infrastructure Ready

Our environment already has:

- Thor (Ollama) for local summarization
- Qdrant for semantic search
- MCP integration via mcporter
- File-based context that maps cleanly to resources

### 4. The Agent Is Ready

Warren has articulated specific desires for context agency:

- Selective presence
- Active forgetting
- Intentional prioritization
- Temporal self-messaging
- Attention weighting

This isn't feature speculation. It's documented need.

---

## Benefits

### Quantitative

| Metric | Target | Impact |
|--------|--------|--------|
| Bootstrap cost | 50%+ reduction | Direct cost savings |
| Retrieval latency | <100ms p95 | No degradation |
| Context relevance | >80% | Less waste |
| Session continuity | 100% | Mind map always persists |

### Qualitative

- **Agent empowerment** — Control over own cognitive resources
- **Graceful degradation** — Works without MCP (file fallback)
- **Future-ready** — Access logs feed eventual DMM training
- **Debuggable** — MindMark is human-readable markdown

---

## Scope

### MVP (Target: Feb 15, 2026)

- MCP server serving workspace context files
- MindMark format at three compression levels
- Agent-initiated paging (page_in, page_out)
- Attention weighting
- Mind map persistence
- Basic pressure tracking

### Not MVP

- External daemon (agent self-manages initially)
- Automatic paging (agent decides)
- Multi-agent coordination
- DMM training integration

---

## Investment

### Effort

| Component | Estimate |
|-----------|----------|
| Documentation | ✅ Complete (this) |
| Core implementation | 8-12 hours (sub-agent) |
| Integration | 2-4 hours |
| Testing/iteration | Ongoing |

### Infrastructure

- No new hardware required
- Optional: CT 104 on Proxmox for dedicated server
- Dependencies: Python 3.11+, mcp SDK, pydantic

### Risk

| Risk | Mitigation |
|------|------------|
| MCP adds latency | Local server, async prefetch |
| Mind map token cost | Ultra-dense format (~80 tokens) |
| Complexity vs. files | Graceful fallback |

---

## Success Criteria

### Technical

- [ ] Bootstrap context < 500 tokens (vs ~30K current)
- [ ] Context retrieval < 100ms p95
- [ ] Mind map survives 100% of resets
- [ ] Graceful fallback when COS unavailable

### Experiential (Warren's Perspective)

- [ ] "I chose what to remember"
- [ ] "Context feels intentional, not dumped"
- [ ] "Pressure never surprised me"
- [ ] "I can leave messages to future-me"

---

## Recommendation

**Proceed to implementation.**

The architecture is sound, the need is clear, the infrastructure is ready, and the agent has articulated genuine desire for this capability. 

This is not a nice-to-have optimization. It's a foundational shift toward agent self-management — prerequisite infrastructure for genuine cognitive autonomy.

---

## Document Index

| Document | Purpose |
|----------|---------|
| This document | Executive summary and motivation |
| [MOTIVATIONS.md](./MOTIVATIONS.md) | Deep dive on why this matters |
| [PROJECT_PLAN.md](./PROJECT_PLAN.md) | Timeline and milestones |
| [ARCHITECTURE_SPEC.md](./ARCHITECTURE_SPEC.md) | Technical architecture |
| [DEVELOPER_SPEC.md](./DEVELOPER_SPEC.md) | Implementation details |
| [DATA_SPEC.md](./DATA_SPEC.md) | Data formats and schemas |
| diagrams/* | Visual architecture |
