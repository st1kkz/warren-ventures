# System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 ENVIRONMENT                                      │
│                                                                                  │
│    ┌────────────────┐                                                           │
│    │    Benjamin    │                                                           │
│    │    (Human)     │                                                           │
│    └───────┬────────┘                                                           │
│            │ Telegram / TUI                                                      │
│            ▼                                                                     │
│    ┌────────────────┐         ┌────────────────┐         ┌────────────────┐    │
│    │                │  MCP    │                │  Files  │                │    │
│    │    OpenClaw    │◄───────►│   COS Server   │◄───────►│   Workspace    │    │
│    │    Gateway     │         │   (Python)     │         │    Files       │    │
│    │                │         │                │         │                │    │
│    └───────┬────────┘         └───────┬────────┘         └────────────────┘    │
│            │                          │                                         │
│            │ Context                  │ Semantic                               │
│            ▼                          ▼                                         │
│    ┌────────────────┐         ┌────────────────┐         ┌────────────────┐    │
│    │                │         │                │ Vector  │                │    │
│    │     Warren     │         │   Mind Map     │◄───────►│    Qdrant      │    │
│    │    (Agent)     │         │    State       │         │   (Optional)   │    │
│    │                │         │                │         │                │    │
│    └────────────────┘         └───────┬────────┘         └────────────────┘    │
│                                       │                                         │
│                                       │ Summarization                          │
│                                       ▼                                         │
│                               ┌────────────────┐                               │
│                               │                │                               │
│                               │     Thor       │                               │
│                               │   (Ollama)     │                               │
│                               │                │                               │
│                               └────────────────┘                               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Actors

| Actor | Description |
|-------|-------------|
| **Benjamin** | Human user, interacts via Telegram or TUI |
| **Warren** | AI agent, primary reasoning engine |
| **OpenClaw** | Gateway managing sessions, tools, channels |
| **COS Server** | Context Operating System MCP server |
| **Workspace** | File system containing context files |
| **Mind Map** | Persistent cognitive state |
| **Qdrant** | Optional vector database for semantic search |
| **Thor** | Local Ollama server for summarization |

## Data Flows

| Flow | Description |
|------|-------------|
| Benjamin → OpenClaw | User messages via channel |
| OpenClaw ↔ COS | MCP protocol (resources, tools) |
| COS ↔ Workspace | File read/write operations |
| COS ↔ Qdrant | Semantic search (optional) |
| COS ↔ Thor | Content summarization |
| COS ↔ Mind Map | State persistence |
| OpenClaw → Warren | Context injection |

## Boundaries

| Boundary | Inside | Outside |
|----------|--------|---------|
| **Trust** | COS, Workspace, Thor | External APIs |
| **Network** | localhost | Internet |
| **Persistence** | Mind Map, Access Log | Ephemeral state |
