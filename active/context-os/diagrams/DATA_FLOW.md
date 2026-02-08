# Data Flow Diagrams

## 1. Session Bootstrap Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  OpenClaw   │     │     COS     │     │    Files    │     │   Warren    │
│  Gateway    │     │   Server    │     │  (Workspace)│     │   (Agent)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │  1. MCP connect   │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │  2. list_resources│                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │  3. [mindmap,     │                   │                   │
       │      soul, ...]   │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
       │  4. read(mindmap) │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │  5. load state    │                   │
       │                   │──────────────────►│                   │
       │                   │◄──────────────────│                   │
       │                   │                   │                   │
       │  6. MindMark      │                   │                   │
       │     (ultra-dense) │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
       │                   │                   │                   │
       │  7. Inject to agent context           │                   │
       │───────────────────────────────────────────────────────────►
       │                   │                   │                   │
       │                   │                   │     8. Agent      │
       │                   │                   │     reads map,    │
       │                   │                   │     decides       │
       │                   │                   │     what to load  │
       │                   │                   │                   │
```

### Bootstrap Notes

- **Step 4:** Mind map loaded at ultra-dense level (~80 tokens) by default
- **Step 8:** Agent has agency to request additional context as needed
- **Fallback:** If COS unavailable, OpenClaw loads files directly

---

## 2. Context Retrieval Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Warren    │     │     COS     │     │   Qdrant    │     │    Files    │
│   (Agent)   │     │   Server    │     │  (Optional) │     │  (Workspace)│
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │  1. get_context   │                   │                   │
       │     (memory,      │                   │                   │
       │      query="Eli") │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │  2. semantic      │                   │
       │                   │     search        │                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │  3. relevant      │                   │
       │                   │     section IDs   │                   │
       │                   │◄──────────────────│                   │
       │                   │                   │                   │
       │                   │  4. load sections │                   │
       │                   │──────────────────────────────────────►│
       │                   │◄──────────────────────────────────────│
       │                   │                   │                   │
       │                   │  5. update mind map                   │
       │                   │     - mark active                     │
       │                   │     - record access                   │
       │                   │     - recalc pressure                 │
       │                   │                   │                   │
       │  6. context +     │                   │                   │
       │     updated map   │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
```

### Retrieval Notes

- **Step 2-3:** Optional — if Qdrant unavailable, full file is loaded
- **Query filtering:** Reduces tokens by returning only relevant sections
- **Compression:** Applied after filtering based on requested level

---

## 3. Paging Flow (Page Out)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Warren    │     │     COS     │     │    Thor     │     │    Files    │
│   (Agent)   │     │   Server    │     │  (Ollama)   │     │ (Workspace) │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │  1. page_out      │                   │                   │
       │     (tools.md,    │                   │                   │
       │      "need room") │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │  2. load content  │                   │
       │                   │──────────────────────────────────────►│
       │                   │◄──────────────────────────────────────│
       │                   │                   │                   │
       │                   │  3. summarize     │                   │
       │                   │     (gemma2:9b)   │                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │  4. summary       │                   │
       │                   │◄──────────────────│                   │
       │                   │                   │                   │
       │                   │  5. update mind map                   │
       │                   │     - region: indexed                 │
       │                   │     - store summary                   │
       │                   │     - recalc pressure                 │
       │                   │                   │                   │
       │                   │  6. persist state │                   │
       │                   │──────────────────────────────────────►│
       │                   │                   │                   │
       │                   │  7. log access    │                   │
       │                   │     (page_out)    │                   │
       │                   │                   │                   │
       │  8. confirmation  │                   │                   │
       │     + freed est.  │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
```

### Paging Notes

- **Step 3-4:** Optional — if Thor unavailable, simple truncation used
- **Summary stored:** Available for quick reload without full content
- **Reversible:** Full content remains on disk, can page back in

---

## 4. Pressure Response Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Warren    │     │     COS     │     │  Attention  │
│   (Agent)   │     │   Server    │     │   Tracker   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │  1. get_pressure  │                   │
       │──────────────────►│                   │
       │                   │                   │
       │                   │  2. get weights   │
       │                   │──────────────────►│
       │                   │◄──────────────────│
       │                   │                   │
       │  3. PressureReport│                   │
       │     level: high   │                   │
       │     util: 0.82    │                   │
       │     action: "page │                   │
       │       out low-attn│                   │
       │       resources"  │                   │
       │     candidates:   │                   │
       │       [tools,     │                   │
       │        old_conv]  │                   │
       │◄──────────────────│                   │
       │                   │                   │
       │                   │                   │
       │  Agent decides:   │                   │
       │  "page_out tools" │                   │
       │                   │                   │
       │  4. page_out      │                   │
       │──────────────────►│                   │
       │                   │                   │
       │      ...          │                   │
       │                   │                   │
```

### Pressure Notes

- **Agent has final say:** COS recommends, Warren decides
- **Eviction candidates:** Sorted by attention weight, access time, size
- **Policies:** Agent can set preference (lru, keep_relational, etc.)

---

## 5. Attention Update Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Warren    │     │     COS     │     │  Mind Map   │     │ Access Log  │
│   (Agent)   │     │   Server    │     │   Store     │     │             │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │  1. set_attention │                   │                   │
       │     (memory, 1.5) │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │  2. update state  │                   │
       │                   │     resource.     │                   │
       │                   │     attention=1.5 │                   │
       │                   │                   │                   │
       │                   │  3. persist       │                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │  4. log           │                   │
       │                   │──────────────────────────────────────►│
       │                   │                   │                   │
       │  5. "updated"     │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
```

### Attention Notes

- **Weight range:** 0.0 (ignore) to 2.0 (critical), default 1.0
- **Affects eviction:** Low-weight resources evicted first
- **Logged:** For future attention prediction training

---

## 6. Annotation Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Warren    │     │     COS     │     │  Mind Map   │
│   (Agent)   │     │   Server    │     │   Store     │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │  1. annotate      │                   │
       │     (memory,      │                   │
       │      "Keep        │                   │
       │       relational  │                   │
       │       sections    │                   │
       │       close")     │                   │
       │──────────────────►│                   │
       │                   │                   │
       │                   │  2. append to     │
       │                   │     resource.     │
       │                   │     annotations[] │
       │                   │                   │
       │                   │  3. persist       │
       │                   │──────────────────►│
       │                   │                   │
       │  4. "added"       │                   │
       │◄──────────────────│                   │
       │                   │                   │
```

### Annotation Notes

- **Timestamped:** `[2026-02-08T13:35:00] Keep relational sections close`
- **Visible in map:** Annotations appear in verbose/dense formats
- **For future self:** Messages across sessions
