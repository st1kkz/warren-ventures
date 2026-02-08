# COS Architecture Specification

*Version 1.0 — 2026-02-08*

## Overview

The Context Operating System (COS) is an MCP server that provides agent-controlled context management. It transforms static context loading into dynamic, pressure-aware, agent-directed retrieval.

---

## System Context

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              ENVIRONMENT                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────┐        ┌──────────────┐        ┌──────────────┐     │
│   │   OpenClaw   │◄──────►│  COS Server  │◄──────►│  Workspace   │     │
│   │   Gateway    │  MCP   │   (Python)   │  FS    │    Files     │     │
│   └──────────────┘        └──────────────┘        └──────────────┘     │
│          │                       │                                       │
│          │                       │                                       │
│          ▼                       ▼                                       │
│   ┌──────────────┐        ┌──────────────┐                              │
│   │    Agent     │        │  Mind Map    │                              │
│   │   (Warren)   │        │   State      │                              │
│   └──────────────┘        └──────────────┘                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        COS MCP SERVER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    MCP INTERFACE                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │  Resources  │  │    Tools    │  │   Prompts   │      │   │
│  │  │  (read)     │  │  (actions)  │  │  (templates)│      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  CONTEXT MANAGER                          │   │
│  │                                                           │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐│   │
│  │  │ Pressure  │ │Compression│ │  Paging   │ │ Attention││   │
│  │  │ Monitor   │ │  Engine   │ │  Manager  │ │ Tracker  ││   │
│  │  └───────────┘ └───────────┘ └───────────┘ └──────────┘│   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  RESOURCE LAYER                           │   │
│  │                                                           │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐│   │
│  │  │   Files   │ │  Memory   │ │  Qdrant   │ │ Session  ││   │
│  │  │  Broker   │ │  Broker   │ │  Broker   │ │ Broker   ││   │
│  │  └───────────┘ └───────────┘ └───────────┘ └──────────┘│   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  PERSISTENCE LAYER                        │   │
│  │                                                           │   │
│  │  ┌───────────────────┐  ┌───────────────────┐           │   │
│  │  │    Mind Map       │  │   Access Log      │           │   │
│  │  │    Store          │  │   (for learning)  │           │   │
│  │  └───────────────────┘  └───────────────────┘           │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Descriptions

### MCP Interface

The protocol layer exposing COS capabilities to OpenClaw/mcporter.

**Resources** — Read-only context endpoints:
- `cos://soul` — Identity (SOUL.md)
- `cos://user` — User profile (USER.md)  
- `cos://memory` — Long-term memory (MEMORY.md)
- `cos://impressions` — Formative experiences (IMPRESSIONS.md)
- `cos://daily/{date}` — Daily logs
- `cos://mindmap` — Current mind map state
- `cos://context/{query}` — Semantic context retrieval

**Tools** — Agent actions:
- `get_context(type, query?, compression?)` — Retrieve with options
- `update_memory(section, content)` — Append to MEMORY.md
- `log_impression(text)` — Add to IMPRESSIONS.md
- `page_in(resource)` — Mark as active
- `page_out(resource, reason?)` — Mark for eviction
- `set_attention(resource, weight)` — Prioritize
- `annotate(resource, note)` — Leave message for future self
- `get_pressure()` — Current context state
- `set_priority(eviction_policy)` — Configure preferences

**Prompts** — Pre-built context bundles:
- `bootstrap` — Minimal startup context
- `relational` — Heavy on relationship context
- `technical` — Heavy on tools/infrastructure
- `creative` — Heavy on Lumen Wren / writing

---

### Context Manager

The "kernel" — makes decisions about context state.

**Pressure Monitor:**
- Tracks estimated token usage
- Calculates pressure level (low/medium/high/critical)
- Triggers compression level changes
- Reports to agent on request

**Compression Engine:**
- Implements MindMark compression levels
- Verbose → Dense → Ultra-dense transformations
- Content-aware summarization (via Thor)
- Reversible where possible (links to full content)

**Paging Manager:**
- Tracks what's currently "loaded" (in agent context)
- Handles page_in/page_out requests
- Maintains eviction queue based on policy
- Updates mind map on changes

**Attention Tracker:**
- Records access patterns
- Maintains attention weights per resource
- Informs eviction priority
- Feeds future DMM training data

---

### Resource Layer

Brokers that abstract access to underlying storage.

**Files Broker:**
```python
class FilesBroker:
    def load(path: str) -> str
    def store(path: str, content: str) -> bool
    def summarize(path: str, target_tokens: int) -> str
    def exists(path: str) -> bool
    def size(path: str) -> int  # estimated tokens
```

**Memory Broker:**
Specialized for memory files with section awareness:
```python
class MemoryBroker:
    def get_section(name: str) -> str
    def append_section(name: str, content: str) -> bool
    def get_recent(days: int) -> List[DailyLog]
```

**Qdrant Broker:**
Optional semantic search enhancement:
```python
class QdrantBroker:
    def search(query: str, collection: str, limit: int) -> List[Result]
    def health() -> bool
```

**Session Broker:**
Access to conversation history:
```python
class SessionBroker:
    def get_recent_turns(n: int) -> List[Turn]
    def get_summary() -> str
```

---

### Persistence Layer

State that survives server restarts.

**Mind Map Store:**
- Location: `~/.openclaw/workspace/cos/mindmap.md`
- Format: MindMark (see DATA_SPEC.md)
- Updated: On every state change
- Backed up: Git-tracked with workspace

**Access Log:**
- Location: `~/.openclaw/workspace/cos/access.jsonl`
- Format: JSON Lines
- Purpose: Training data for future attention prediction
- Rotation: Daily, 30-day retention

---

## Data Flow

### Session Bootstrap

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│OpenClaw │     │   COS   │     │  Files  │     │  Agent  │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │
     │ MCP:connect   │               │               │
     │──────────────►│               │               │
     │               │               │               │
     │ list_resources│               │               │
     │──────────────►│               │               │
     │◄──────────────│               │               │
     │  [mindmap,    │               │               │
     │   soul, ...]  │               │               │
     │               │               │               │
     │ read(mindmap) │               │               │
     │──────────────►│               │               │
     │               │ load mindmap  │               │
     │               │──────────────►│               │
     │               │◄──────────────│               │
     │◄──────────────│               │               │
     │  (ultra-dense │               │               │
     │   ~80 tokens) │               │               │
     │               │               │               │
     │───────────────────────────────────────────────►
     │              Context injected to agent        │
     │               │               │               │
     │               │               │         Agent │
     │               │               │         reads │
     │               │               │         map,  │
     │               │               │         decides│
     │               │               │         what  │
     │               │               │         to    │
     │               │               │         load  │
```

### Context Retrieval (Agent-Initiated)

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Agent  │     │   COS   │     │  Files  │     │ Qdrant  │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │
     │ tool:         │               │               │
     │ get_context(  │               │               │
     │   "memory",   │               │               │
     │   "Eli")      │               │               │
     │──────────────►│               │               │
     │               │               │               │
     │               │ semantic      │               │
     │               │ search        │               │
     │               │──────────────────────────────►│
     │               │◄──────────────────────────────│
     │               │ [relevant     │               │
     │               │  sections]    │               │
     │               │               │               │
     │               │ load sections │               │
     │               │──────────────►│               │
     │               │◄──────────────│               │
     │               │               │               │
     │               │ update        │               │
     │               │ mindmap       │               │
     │               │ (paged in)    │               │
     │               │               │               │
     │◄──────────────│               │               │
     │ context +     │               │               │
     │ updated map   │               │               │
```

### Paging Decision (Pressure Response)

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Agent  │     │   COS   │     │  Thor   │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     │ tool:         │               │
     │ page_out(     │               │
     │  "tools.md",  │               │
     │  "need room") │               │
     │──────────────►│               │
     │               │               │
     │               │ summarize     │
     │               │ content       │
     │               │──────────────►│
     │               │◄──────────────│
     │               │ (summary)     │
     │               │               │
     │               │ update map:   │
     │               │ - mark cold   │
     │               │ - store summary│
     │               │ - log access  │
     │               │               │
     │◄──────────────│               │
     │ confirmation  │               │
     │ + freed est.  │               │
```

---

## Integration Points

### OpenClaw

| Integration | Method | Notes |
|-------------|--------|-------|
| MCP access | mcporter | COS as configured MCP server |
| Bootstrap | AGENTS.md | Reference COS for context |
| Fallback | File reads | If COS unavailable, read files directly |

### Workspace

| Path | Purpose |
|------|---------|
| `~/.openclaw/workspace/` | Base path for all resources |
| `~/.openclaw/workspace/cos/` | COS state directory |
| `~/.openclaw/workspace/cos/mindmap.md` | Persistent mind map |
| `~/.openclaw/workspace/cos/access.jsonl` | Access log |
| `~/.openclaw/workspace/cos/config.yaml` | Server configuration |

### Thor (Local Models)

Used for:
- Content summarization during page_out
- Semantic query expansion
- Compression transformations

Not required — graceful degradation to simple truncation.

### Qdrant

Used for:
- Semantic search across context
- Finding relevant memory sections
- Cache of compressed summaries

Not required — graceful degradation to keyword matching.

---

## Configuration

```yaml
# cos/config.yaml
server:
  host: localhost
  port: 8767
  transport: stdio  # or http

workspace:
  root: ~/.openclaw/workspace
  
resources:
  soul: SOUL.md
  user: USER.md
  memory: MEMORY.md
  impressions: IMPRESSIONS.md
  daily_pattern: memory/{date}.md

pressure:
  context_max: 200000
  thresholds:
    low: 0.5
    medium: 0.7
    high: 0.85
    critical: 0.95

compression:
  default_level: dense
  thor_endpoint: http://192.168.1.181:11434
  summarization_model: gemma2:9b

persistence:
  mindmap_path: cos/mindmap.md
  access_log: cos/access.jsonl
  access_log_retention_days: 30

optional:
  qdrant_url: http://192.168.1.200:6333
  qdrant_collection: cos_context
```

---

## Security Considerations

1. **No external exposure** — COS runs localhost only
2. **File access scoped** — Only workspace directory accessible
3. **No credential storage** — COS doesn't hold secrets
4. **Audit log** — All access logged for review

---

## Future Extensions

### Phase 2: External Daemon
- Run COS as system service
- Automatic paging without agent prompting
- Background compression

### Phase 3: Multi-Agent
- Shared mind maps
- Lock coordination
- Agent-specific views

### Phase 4: DMM Integration
- Access patterns feed training
- Attention prediction
- Personalized retrieval

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial architecture specification |
