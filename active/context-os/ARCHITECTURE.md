# COS Architecture

*Draft v0.1 — 2026-02-05*

## Core Premise

The mind is distributed. COS coordinates resources (context window, local models, vector stores, files, external APIs) so the primary agent can think rather than manage plumbing.

---

## Architectural Layers

```
┌─────────────────────────────────────────────────┐
│                 AGENT LAYER                     │
│   (Warren/Opus — reasoning, conversation)       │
├─────────────────────────────────────────────────┤
│               CONTEXT MANAGER                   │
│   Mind map, paging decisions, compression       │
├─────────────────────────────────────────────────┤
│              RESOURCE BROKERS                   │
│   ┌─────────┬─────────┬─────────┬─────────┐    │
│   │  Thor   │  Qdrant │  Files  │  Cloud  │    │
│   │ (local) │ (vector)│  (disk) │ (APIs)  │    │
│   └─────────┴─────────┴─────────┴─────────┘    │
├─────────────────────────────────────────────────┤
│              PERSISTENCE LAYER                  │
│   Session state, mind maps, checkpoints        │
└─────────────────────────────────────────────────┘
```

---

## Layer Descriptions

### Agent Layer
The primary reasoning engine. Currently Opus 4.5, but COS should be model-agnostic. This layer:
- Receives the current mind map at session start
- Makes high-level decisions about what to load/offload
- Delegates to Context Manager for execution
- Focuses on thinking, not plumbing

### Context Manager
The kernel. Responsibilities:
- **Monitoring** — Tracks context pressure (tokens used / available)
- **Paging** — Decides what to load into context, what to summarize out
- **Compression** — Triggers MindMark compression level changes
- **Mind Map** — Maintains the map as ground truth

Could be implemented as:
1. External daemon (runs alongside OpenClaw)
2. Lightweight hook (runs at turn boundaries)
3. Injected context (agent self-manages with map awareness)

Initial implementation likely (3), evolving toward (1).

### Resource Brokers
Abstract access to subsystems. Uniform interface:

```
broker.load(resource_id) → content
broker.store(resource_id, content) → success
broker.query(query, params) → results
broker.summarize(resource_id, target_tokens) → summary
broker.health() → status
```

**Thor Broker:**
- Local Ollama models
- Sub-agent spawning
- Batch processing

**Qdrant Broker:**
- Semantic search
- Response cache
- Knowledge retrieval

**Files Broker:**
- Workspace access
- Memory files
- Configuration

**Cloud Broker:**
- External APIs
- Free-tier models
- Fallback routing

### Persistence Layer
Session survival. Components:
- **Mind Map Store** — Current state serialized between sessions
- **Checkpoints** — Periodic snapshots for recovery
- **Session Transcripts** — Already exists in SQLite
- **Delta Log** — Changes since last checkpoint (future)

Foundation for "dynamic mind model" — eventually, this layer could feed training.

---

## Data Flow

### Session Start
```
1. Load persisted mind map
2. Context Manager evaluates: what's stale? what's needed?
3. Brokers fetch/summarize required resources
4. Agent receives: map + essential context
5. Agent begins reasoning
```

### During Session
```
1. Agent requests resource not in context
2. Context Manager checks pressure
3. If room: load via broker
4. If tight: summarize something out first
5. Update mind map
6. Return to agent
```

### Session End / Compaction
```
1. Context Manager detects pressure threshold
2. Trigger memory flush (existing OpenClaw feature)
3. Compress mind map to denser level
4. Summarize older conversation turns
5. Persist updated map
```

---

## Integration with OpenClaw

COS is not a replacement for OpenClaw — it's a layer on top.

**OpenClaw provides:**
- Session management
- Tool execution
- Message routing
- Compaction infrastructure

**COS adds:**
- Intelligent paging decisions
- Mind map awareness
- Compression strategy
- Resource coordination

Initial implementation: workspace files + conventions + agent self-discipline.
Future: Hooks or external daemon for automation.

---

## Metrics to Track

| Metric | Purpose |
|--------|---------|
| Context utilization | % of window used |
| Page-in latency | Time to load from cold |
| Compression ratio | Tokens saved by dense formats |
| Cache hit rate | Qdrant response cache effectiveness |
| Sub-agent offload rate | % of work delegated |

---

## Revision History

- **v0.1** (2026-02-05): Initial draft from conversation with Benjamin
