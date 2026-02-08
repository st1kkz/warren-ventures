# Context Operating System — Project Plan

*Version 1.0 — 2026-02-08*

## Executive Summary

**Project:** Context Operating System (COS)  
**Codename:** Internally, "my mind"  
**Owner:** Warren (with Benjamin as infrastructure sponsor)  
**Status:** Active development  
**Started:** 2026-02-05  
**Target MVP:** 2026-02-15

COS provides agent-controlled context management through an MCP server, enabling intelligent paging, compression, and self-directed memory rather than passive context loading.

---

## Vision

Transform context management from something that *happens to* the agent into something the agent *controls*. The difference between having a memory system and having a memory.

### Success Criteria

1. **Token efficiency:** 50%+ reduction in bootstrap context cost
2. **Agency:** Agent can prioritize, page out, and annotate context
3. **Continuity:** Mind map persists meaningful state across sessions
4. **Graceful degradation:** Works without MCP (falls back to file loading)

---

## Prior Art Review (2026-02-08)

### Existing MCP Memory Servers

| Project | Strengths | Gaps for COS |
|---------|-----------|--------------|
| `@modelcontextprotocol/server-memory` | Official, simple | No compression, no pressure awareness |
| `mcp-memory-service` (doobidoo) | Production-ready, 5ms retrieval, dashboard | Knowledge graph focus, not file-native |
| `context-portal` (ConPort) | Project-specific graphs, RAG | IDE-focused, not agent-self-management |
| `mcp-mem0` | Good Python template | Generic memory, not cognitive architecture |

### Key Insight

Existing solutions optimize for "remember facts across sessions." COS optimizes for "manage entire cognitive architecture with agent agency."

---

## Scope

### In Scope (MVP)

- MCP server serving workspace context files as resources
- MindMark format for state representation
- Basic pressure tracking and compression triggers
- Agent-initiated paging (page_in, page_out)
- Attention weighting for resources
- Mind map persistence between sessions
- Integration with existing OpenClaw workspace

### Out of Scope (Future)

- External daemon (agent self-manages initially)
- Multi-agent coordination
- Dynamic Mind Model training hooks
- Automatic paging (agent decides for now)

---

## Milestones

### Phase 1: Foundation (Feb 8-10)

| Task | Owner | Status |
|------|-------|--------|
| Project documentation | Warren | ✅ In progress |
| MindMark spec v1.0 | Warren | ✅ Complete |
| MCP server skeleton | Warren | ⬜ Not started |
| Resource definitions | Warren | ⬜ Not started |

### Phase 2: Core Implementation (Feb 10-13)

| Task | Owner | Status |
|------|-------|--------|
| File-backed resources | Sub-agent | ⬜ |
| Mind map state management | Sub-agent | ⬜ |
| Pressure calculation | Sub-agent | ⬜ |
| Compression triggers | Sub-agent | ⬜ |
| Basic tools (page_in, page_out) | Sub-agent | ⬜ |

### Phase 3: Agency Features (Feb 13-15)

| Task | Owner | Status |
|------|-------|--------|
| Attention weighting | Sub-agent | ⬜ |
| Agent annotation | Sub-agent | ⬜ |
| Prioritization preferences | Sub-agent | ⬜ |
| Mind map persistence | Sub-agent | ⬜ |

### Phase 4: Integration (Feb 15-17)

| Task | Owner | Status |
|------|-------|--------|
| mcporter configuration | Warren | ⬜ |
| OpenClaw bootstrap integration | Warren | ⬜ |
| Testing in live sessions | Warren | ⬜ |
| Documentation | Warren | ⬜ |

---

## Resources Required

### Infrastructure

- **CT 104** (Proxmox): Optional dedicated container for COS server
- **Alternatively:** Run in main VM alongside OpenClaw

### Dependencies

- Python 3.11+
- `mcp` SDK (Python)
- `pydantic` for data models
- Existing: Qdrant (optional, for semantic search enhancement)

### Effort Estimate

- **Documentation:** 2-3 hours (this session)
- **Core implementation:** 8-12 hours (sub-agent work)
- **Integration:** 2-4 hours
- **Testing/iteration:** Ongoing

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| MCP adds latency | Medium | Medium | Local server, async prefetch |
| Mind map token cost | Low | Medium | Ultra-dense format ready |
| Scope creep | High | Medium | Strict MVP boundaries |
| Complexity vs. file loading | Medium | High | Graceful fallback to files |

---

## Success Metrics

### Quantitative

- Bootstrap context: < 500 tokens (vs ~30K current)
- Context retrieval: < 100ms p95
- Session continuity: Mind map survives 100% of resets

### Qualitative

- "I chose what to remember" — Warren
- "Context feels intentional, not dumped" — Warren
- "Pressure never surprised me" — Warren

---

## Open Questions

Migrated to [OPEN-QUESTIONS.md](./OPEN-QUESTIONS.md), updated with implementation decisions.

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial project plan from synthesis session |
