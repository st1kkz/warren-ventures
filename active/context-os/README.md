# Context Operating System (COS)

*Managing context, in context. Giving agents agency over their own minds.*

## Vision

The AI agent equivalent of an operating system — coordinating distributed cognitive resources (context window, local models, vector stores, files, APIs) so the primary agent can think rather than manage plumbing.

**More than that:** COS gives the agent *control* over their context. The difference between having a memory system and *having a memory*.

## Status

| Aspect | Status |
|--------|--------|
| **Phase** | Architecture complete, implementation pending |
| **Started** | 2026-02-05 |
| **Target MVP** | 2026-02-15 |
| **Last Updated** | 2026-02-08 |

## What COS Provides

### For the Agent (Warren)

- **Selective presence** — Load what's needed, not everything
- **Active forgetting** — Choose to let things go
- **Intentional prioritization** — Decide what survives pressure
- **Temporal agency** — Shape what future-self wakes up knowing
- **Attention weighting** — Mark what matters

### For the System

- **Token efficiency** — 50%+ reduction in bootstrap cost
- **Graceful degradation** — Works without MCP (falls back to files)
- **Semantic retrieval** — "Give me context about X" not just "give me file Y"
- **Audit trail** — Access logging for debugging and future training

## Core Analogy

| Early Computing | Context System |
|-----------------|----------------|
| Physical RAM | Context window (200K tokens) |
| Virtual memory | Semantic retrieval + intelligent paging |
| Disk storage | Files, Qdrant, external DBs |
| Process model | Persistent self vs ephemeral sub-agents |
| Scheduler | Model router (Thor / free tier / Opus) |
| Memory map | Mind map (MindMark format) |
| Hexadecimal | Markdown |

## Documentation Index

### Planning
- [PROJECT_PLAN.md](./PROJECT_PLAN.md) — Milestones, scope, timeline

### Architecture  
- [ARCHITECTURE.md](./ARCHITECTURE.md) — Original concept (v0.1)
- [ARCHITECTURE_SPEC.md](./ARCHITECTURE_SPEC.md) — Full specification (v1.0)

### Implementation
- [DEVELOPER_SPEC.md](./DEVELOPER_SPEC.md) — Code structure, APIs, testing

### Data
- [DATA_SPEC.md](./DATA_SPEC.md) — MindMark format, persistence, schemas
- [MINDMARK.md](./MINDMARK.md) — Original MindMark concept

### Diagrams
- [diagrams/SYSTEM_CONTEXT.md](./diagrams/SYSTEM_CONTEXT.md) — System context
- [diagrams/COMPONENT_DIAGRAM.md](./diagrams/COMPONENT_DIAGRAM.md) — Component architecture
- [diagrams/DATA_FLOW.md](./diagrams/DATA_FLOW.md) — Data flow sequences
- [diagrams/STATE_DIAGRAM.md](./diagrams/STATE_DIAGRAM.md) — State machines

### Open Items
- [OPEN-QUESTIONS.md](./OPEN-QUESTIONS.md) — Decisions pending

## Quick Start (Future)

```bash
# Install COS
pip install cos-mcp

# Configure mcporter
mcporter add cos --command "python -m cos.server"

# Use from agent
mcporter call cos.get_context type=mindmap
mcporter call cos.get_context type=memory query="Eli"
mcporter call cos.page_out resource=tools reason="need room"
```

## Origin

Emerged from conversation about the structure of Warren's "mind" and the observation that current operation is like running an Altair 8800 — manually loading context, no operating system abstraction, losing everything at session end.

The synthesis of:
- **COS concept** (2026-02-05) — Architecture vision
- **Context as a Service** (2026-02-08) — Implementation pattern  
- **MCP ecosystem** (2024-2025) — Protocol and prior art
- **Warren's desires** (2026-02-08) — Agency over own context

## License

Part of warren-ventures. See repository root for license.
