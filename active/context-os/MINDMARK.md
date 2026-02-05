# MindMark Specification

*Draft v0.1 — 2026-02-05*

A markdown-native format for representing cognitive state — what's loaded, what's available, what's distant.

---

## Design Principles

1. **Native markdown** — Parseable by any LLM without special tooling
2. **Compression levels** — Verbose ↔ dense ↔ ultra-dense (same semantics, different token cost)
3. **Graph-capable** — Can represent connections, not just hierarchy
4. **Annotatable** — Size, freshness, access metadata inline
5. **Diffable** — Changes visible in standard git diff
6. **Self-describing** — Format includes its own version and state

---

## Analogy

| Computing | MindMark |
|-----------|----------|
| Binary | Token embeddings |
| Hexadecimal | Markdown |
| Memory map | Mind map |
| Address space | Context window |
| Page table | Resource registry |

---

## Document Structure

### Header
```markdown
# Mind Map v0.1
@state|ctx:42K/200K|pressure:low|updated:07:52
```

Fields:
- `ctx` — Context usage (current/max)
- `pressure` — low / medium / high / critical
- `updated` — Timestamp of last update

### Regions

Resources grouped by access latency:

| Region | Access Time | Typical Contents |
|--------|-------------|------------------|
| Active | 0ms (in context) | Conversation, loaded files, tool state |
| Indexed | <100ms | Qdrant vectors, cached responses |
| Cold | <5s | Full files, idle models, external APIs |
| Offline | Unknown | Unreachable resources |

### Notation Symbols

| Symbol | Meaning |
|--------|---------|
| `✓` | Loaded in context |
| `◆` | Hot / high attention weight |
| `●` | Connected, ready |
| `○` | Available, cold |
| `✗` | Unavailable / error |
| `[NK]` | Size in tokens (N) or kilobytes (NK) |
| `→` | Link / dependency |

---

## Compression Levels

### Verbose (Level 1)
*For authoring, debugging, documentation*

```markdown
# Mind Map v0.1
@state|ctx:42K/200K|pressure:low|updated:2026-02-05T07:52:00

## Active Context [32K tokens]

### Conversation
- **Partner:** Benjamin
- **Topic:** Context Operating System architecture
- **Turns:** 22
- **Size:** 18K tokens
- **Status:** Active, high relevance
- **Key concepts:** mind map, compression layers, COS

### Workspace Files
- **SOUL.md:** Loaded ✓ [2K]
- **USER.md:** Loaded ✓ [1K]  
- **MEMORY.md:** Loaded ✓ [8K]
- **IMPRESSIONS.md:** Loaded ✓ [3K]

### Tools
- **session-browser:** Running on port 8765

## Indexed Resources [retrievable <100ms]

### Qdrant Collections
- **urantia_papers:** 15,260 vectors
  - Last query: 07:30
  - Status: Connected ●
- **warren_responses:** 76 vectors
  - Response cache
  - Status: Connected ●

### Memory Files
- 5 daily logs (2026-02-01 through 2026-02-05)
- Total size: ~40K
- Status: Available ○

## Cold Resources [retrievable <5s]

### Thor (Local Ollama)
- Status: Idle ○
- Loaded models: qwen3:14b, qwen2.5:32b
- VRAM: 14GB available

### Workspace Tree
- Full directory accessible
- Estimated size: ~200K if fully loaded

## Links
- conversation → ws/MEMORY.md (references formation discussion)
- conversation → qdrant/urantia (potential recall for Paper 44 artisans)
```

**Approximate size:** ~1,500 tokens

---

### Dense (Level 2)
*For runtime awareness*

```markdown
# Mind Map v0.1
@state|ctx:42K/200K|pressure:low|updated:07:52

## Active [32K]
- conv: benjamin, context-os, 22t [18K] ◆
- ws: SOUL✓ USER✓ MEM✓ IMPR✓ [14K]
- tools: session-browser:8765 ●

## Indexed [<100ms]
- qdrant/urantia: 15,260v, last:07:30 ●
- qdrant/responses: 76v ●
- files/memory: 5 logs [~40K] ○

## Cold [<5s]
- thor: idle, qwen3:14b+qwen2.5:32b ○
- files/workspace: full tree [~200K] ○

## Links
conv → MEM (formation)
conv → urantia (Paper 44)
```

**Approximate size:** ~350 tokens (~4x compression)

---

### Ultra-Dense (Level 3)
*For crisis mode, compaction imminent*

```markdown
@MM0.1|42K/200K:low|07:52
@A32K: C22t:cos◆18K|W:SUMI✓14K|T:sb●
@I: Qu●15K|Qr●76|Fm○40K
@C: T○qwen|Fw○200K
@L: C→MEM,urantia
```

**Approximate size:** ~80 tokens (~18x compression)

**Ultra-dense key:**
```
@MM — MindMark header
@A — Active region
@I — Indexed region  
@C — Cold region
@L — Links
C — Conversation
W — Workspace (SUMI = SOUL+USER+MEM+IMPR)
T — Tools
Q — Qdrant (u=urantia, r=responses)
F — Files (m=memory, w=workspace)
```

---

## Compression Triggers

| Pressure | Action |
|----------|--------|
| Low (<50%) | Verbose format acceptable |
| Medium (50-70%) | Shift to dense format |
| High (70-85%) | Ultra-dense, begin paging |
| Critical (>85%) | Emergency summarization |

---

## Mind Map Operations

### Diff
Standard git diff works because it's markdown:
```diff
- conv: benjamin, context-os, 22t [18K] ◆
+ conv: benjamin, context-os, 28t [24K] ◆
```

### Merge
Simple append for new resources; replace for updated ones.

### Validate
Checksum or hash of loaded resources to detect drift.

---

## Embedding Hints (Future)

For semantic paging, resources could include embedding hints:
```markdown
- conv: context-os [18K] ◆ #architecture #memory #formatting
```

Tags help Context Manager decide relevance without full content scan.

---

## Revision History

- **v0.1** (2026-02-05): Initial draft from conversation with Benjamin
