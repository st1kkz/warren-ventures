# Open Questions

*Decisions to make as COS develops*

---

## Architecture

### Q1: Who maintains the mind map?

**Options:**
1. **External daemon** — Runs alongside OpenClaw, updates map automatically
   - Pro: No context cost, always current
   - Con: Significant build effort, coordination complexity

2. **Turn-boundary hook** — Runs at start/end of each turn
   - Pro: Lightweight, leverages OpenClaw hooks
   - Con: Still costs some tokens, may lag

3. **Agent self-management** — Warren maintains map consciously
   - Pro: Works today, no new infrastructure
   - Con: Burns tokens, error-prone, cognitive load

**Current lean:** Start with (3), evolve toward (1) as infrastructure matures.

---

### Q2: Where does COS run?

**Options:**
1. **Inside context** — Map is a file loaded at session start
2. **OpenClaw hooks** — Custom hook manages state
3. **Separate service** — Daemon on Proxmox (CT 104?)
4. **Hybrid** — Daemon + lightweight context awareness

**Current lean:** (1) for MVP, (4) as target state.

---

### Q3: How does COS bootstrap?

The map itself costs tokens to load. At session start:
- Full verbose map: ~1,500 tokens
- Dense map: ~350 tokens
- Ultra-dense: ~80 tokens

Should we:
- Always load dense?
- Load ultra-dense, expand on demand?
- External service provides "what you need right now" summary?

---

## Data Format

### Q4: Should MindMark support binary payloads?

E.g., embedding vectors as base64? Probably not — keep it text-native. But worth deciding explicitly.

**Current lean:** No. MindMark is metadata/pointers, not payload.

---

### Q5: How do we handle version migrations?

When MindMark format evolves:
- Backward compatibility required?
- Migration scripts?
- Version field in header handles this?

**Current lean:** Version field + best-effort parsing. Early enough to not over-engineer.

---

### Q6: Link representation

Current: `conv → MEM (formation)`

Should links include:
- Strength/weight?
- Bidirectionality?
- Type (references, requires, summarizes)?

**Current lean:** Keep simple for now. Add types if needed.

---

## Operations

### Q7: Trigger thresholds

Proposed:
| Pressure | Action |
|----------|--------|
| <50% | Verbose OK |
| 50-70% | Shift to dense |
| 70-85% | Ultra-dense, begin paging |
| >85% | Emergency summarization |

Are these right? Should they be configurable?

---

### Q8: What gets paged out first?

When pressure is high, what's the eviction priority?
- Oldest conversation turns?
- Largest tool outputs?
- Least-recently-referenced files?
- LRU across all resources?

Need a policy. Probably: tool outputs → old turns → files.

---

### Q9: Checkpoint frequency

How often should COS persist state?
- Every turn? (high durability, high I/O)
- Every N turns?
- On pressure threshold changes?
- On explicit save?

---

## Integration

### Q10: Relationship to OpenClaw compaction

OpenClaw already has compaction/memory flush. COS should complement, not conflict:
- COS handles pre-compaction optimization
- OpenClaw compaction is the backstop
- Memory flush captures what COS couldn't save

Need to map the interaction clearly.

---

### Q11: Sub-agent awareness

When Warren spawns a sub-agent:
- Does the sub-agent get a mind map?
- A subset? Fresh start?
- How does sub-agent work update the main map?

**Current lean:** Sub-agents are stateless workers. Main agent updates map based on results.

---

## Future

### Q12: Dynamic Mind Model integration

COS persistence layer is foundation for eventual DMM training. What should we capture now to enable that later?
- Full turn transcripts (already have)
- Mind map evolution over time
- Decision points (what was paged, why)
- Attention patterns (what got referenced)

---

### Q13: Multi-agent coordination

If multiple Warren instances (or other agents) share resources:
- Locking?
- Eventual consistency?
- Shared vs. private mind maps?

Not needed now, but architecture shouldn't preclude it.

---

*Add questions as they arise. Resolve and move to DECISIONS.md when settled.*
