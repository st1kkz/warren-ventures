# Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COS MCP SERVER                                      │
│                                                                                  │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                           MCP INTERFACE                                    │ │
│  │                                                                            │ │
│  │   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │ │
│  │   │    Resources     │  │      Tools       │  │     Prompts      │       │ │
│  │   │                  │  │                  │  │                  │       │ │
│  │   │  • cos://soul    │  │  • get_context   │  │  • bootstrap     │       │ │
│  │   │  • cos://user    │  │  • update_memory │  │  • relational    │       │ │
│  │   │  • cos://memory  │  │  • log_impression│  │  • technical     │       │ │
│  │   │  • cos://impr    │  │  • page_in       │  │  • creative      │       │ │
│  │   │  • cos://daily/* │  │  • page_out      │  │                  │       │ │
│  │   │  • cos://mindmap │  │  • set_attention │  │                  │       │ │
│  │   │  • cos://search  │  │  • annotate      │  │                  │       │ │
│  │   │                  │  │  • get_pressure  │  │                  │       │ │
│  │   │                  │  │  • set_priority  │  │                  │       │ │
│  │   └──────────────────┘  └──────────────────┘  └──────────────────┘       │ │
│  │                                                                            │ │
│  └─────────────────────────────────┬─────────────────────────────────────────┘ │
│                                    │                                            │
│                                    ▼                                            │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                         CONTEXT MANAGER                                    │ │
│  │                                                                            │ │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │ │
│  │   │  Pressure   │  │ Compression │  │   Paging    │  │  Attention  │     │ │
│  │   │  Monitor    │  │   Engine    │  │   Manager   │  │   Tracker   │     │ │
│  │   │             │  │             │  │             │  │             │     │ │
│  │   │ • Calculate │  │ • Verbose   │  │ • page_in   │  │ • Weights   │     │ │
│  │   │   level     │  │ • Dense     │  │ • page_out  │  │ • Access    │     │ │
│  │   │ • Threshold │  │ • Ultra     │  │ • Eviction  │  │   patterns  │     │ │
│  │   │   alerts    │  │ • Summarize │  │   queue     │  │ • Priority  │     │ │
│  │   │             │  │             │  │             │  │   scoring   │     │ │
│  │   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │ │
│  │                                                                            │ │
│  └─────────────────────────────────┬─────────────────────────────────────────┘ │
│                                    │                                            │
│                                    ▼                                            │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                          RESOURCE LAYER                                    │ │
│  │                                                                            │ │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │ │
│  │   │    Files    │  │   Memory    │  │   Qdrant    │  │   Session   │     │ │
│  │   │   Broker    │  │   Broker    │  │   Broker    │  │   Broker    │     │ │
│  │   │             │  │             │  │             │  │             │     │ │
│  │   │ • load()    │  │ • sections  │  │ • search()  │  │ • turns     │     │ │
│  │   │ • store()   │  │ • append()  │  │ • health()  │  │ • summary   │     │ │
│  │   │ • exists()  │  │ • daily()   │  │             │  │             │     │ │
│  │   │ • size()    │  │             │  │             │  │             │     │ │
│  │   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │ │
│  │          │                │                │                │             │ │
│  └──────────┼────────────────┼────────────────┼────────────────┼─────────────┘ │
│             │                │                │                │               │
│             ▼                ▼                ▼                ▼               │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                        PERSISTENCE LAYER                                   │ │
│  │                                                                            │ │
│  │   ┌────────────────────────────┐  ┌────────────────────────────┐          │ │
│  │   │      Mind Map Store        │  │       Access Log           │          │ │
│  │   │                            │  │                            │          │ │
│  │   │  • cos/mindmap.md          │  │  • cos/access.jsonl        │          │ │
│  │   │  • cos/state.json          │  │  • Daily rotation          │          │ │
│  │   │  • Load/save operations    │  │  • 30-day retention        │          │ │
│  │   │                            │  │                            │          │ │
│  │   └────────────────────────────┘  └────────────────────────────┘          │ │
│  │                                                                            │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### MCP Interface

| Component | Purpose |
|-----------|---------|
| **Resources** | Read-only context endpoints (cos:// URIs) |
| **Tools** | Agent-invocable actions |
| **Prompts** | Pre-built context bundles for common scenarios |

### Context Manager

| Component | Purpose |
|-----------|---------|
| **Pressure Monitor** | Tracks token usage, calculates pressure level |
| **Compression Engine** | MindMark level transformations, summarization |
| **Paging Manager** | Page in/out operations, eviction queue |
| **Attention Tracker** | Resource weights, access patterns |

### Resource Layer

| Component | Purpose |
|-----------|---------|
| **Files Broker** | Generic file system access |
| **Memory Broker** | Specialized for memory files with sections |
| **Qdrant Broker** | Semantic search (optional, graceful degradation) |
| **Session Broker** | Conversation history access |

### Persistence Layer

| Component | Purpose |
|-----------|---------|
| **Mind Map Store** | State persistence between sessions |
| **Access Log** | Audit trail, training data for DMM |

## Dependencies

```
MCP Interface
    └── Context Manager
            ├── Pressure Monitor
            │       └── (uses) Mind Map State
            ├── Compression Engine
            │       └── (uses) Thor Ollama
            ├── Paging Manager
            │       └── (uses) All Brokers
            └── Attention Tracker
                    └── (writes) Access Log

Resource Layer
    ├── Files Broker ──────► Workspace (~/.openclaw/workspace)
    ├── Memory Broker ─────► Memory Files (MEMORY.md, daily/*)
    ├── Qdrant Broker ─────► Qdrant Server (192.168.1.200:6333)
    └── Session Broker ────► OpenClaw Sessions (SQLite)

Persistence Layer
    ├── Mind Map Store ────► cos/mindmap.md, cos/state.json
    └── Access Log ────────► cos/access.jsonl
```
