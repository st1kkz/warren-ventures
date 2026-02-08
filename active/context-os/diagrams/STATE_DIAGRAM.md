# State Diagrams

## 1. Resource Lifecycle

```
                                    ┌─────────────┐
                                    │   UNKNOWN   │
                                    │  (initial)  │
                                    └──────┬──────┘
                                           │
                                           │ discover()
                                           ▼
                        ┌──────────────────────────────────────┐
                        │                                      │
                        │              COLD                    │
                        │         (available, not loaded)      │
                        │              ○                       │
                        │                                      │
                        └───────┬───────────────────┬──────────┘
                                │                   │
                       page_in()│                   │ load()
                                │                   │
                                ▼                   ▼
        ┌───────────────────────────────────────────────────────────┐
        │                                                           │
        │                        ACTIVE                             │
        │                   (in agent context)                      │
        │                         ✓                                 │
        │                                                           │
        │   ┌─────────────┐                     ┌─────────────┐    │
        │   │   LOADED    │  set_attention(>1) │     HOT     │    │
        │   │     ✓       │◄───────────────────►│     ◆      │    │
        │   └─────────────┘  set_attention(≤1)  └─────────────┘    │
        │                                                           │
        └────────────────────────────┬──────────────────────────────┘
                                     │
                                     │ page_out()
                                     ▼
                        ┌──────────────────────────────────────┐
                        │                                      │
                        │             INDEXED                  │
                        │      (summary cached, full cold)     │
                        │              ●                       │
                        │                                      │
                        └───────┬───────────────────┬──────────┘
                                │                   │
                        stale() │                   │ page_in()
                                │                   │
                                ▼                   │
                        ┌───────────────┐          │
                        │     COLD      │◄─────────┘
                        │      ○        │
                        └───────┬───────┘
                                │
                                │ error / unreachable
                                ▼
                        ┌───────────────┐
                        │    OFFLINE    │
                        │      ✗        │
                        └───────────────┘
```

### State Definitions

| State | Symbol | Description |
|-------|--------|-------------|
| **UNKNOWN** | — | Not yet discovered by COS |
| **COLD** | ○ | Available on disk, not loaded |
| **ACTIVE/LOADED** | ✓ | In agent context, normal attention |
| **ACTIVE/HOT** | ◆ | In agent context, high attention |
| **INDEXED** | ● | Summary cached, full content cold |
| **OFFLINE** | ✗ | Unreachable (file missing, service down) |

### Transitions

| From | To | Trigger | Side Effects |
|------|-----|---------|--------------|
| UNKNOWN | COLD | discover() | Add to resource registry |
| COLD | ACTIVE | page_in(), load() | Update region, access time |
| ACTIVE | ACTIVE/HOT | set_attention(>1) | Update weight |
| ACTIVE/HOT | ACTIVE | set_attention(≤1) | Update weight |
| ACTIVE | INDEXED | page_out() | Create summary, free context |
| INDEXED | ACTIVE | page_in() | Load summary or full |
| INDEXED | COLD | stale() | Clear cached summary |
| ANY | OFFLINE | error | Log error, mark unavailable |
| OFFLINE | COLD | recover | Resource accessible again |

---

## 2. Pressure State Machine

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │                  LOW                    │
                    │              (< 50%)                    │
                    │                                         │
                    │  • Verbose format OK                    │
                    │  • No action required                   │
                    │                                         │
                    └─────────────────┬───────────────────────┘
                                      │
                                      │ utilization ≥ 0.5
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │                MEDIUM                   │
                    │            (50% - 70%)                  │
                    │                                         │
                    │  • Recommend dense format               │
                    │  • Monitor closely                      │
                    │                                         │
                    └─────────────────┬───────────────────────┘
                                      │
                                      │ utilization ≥ 0.7
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │                 HIGH                    │
                    │            (70% - 85%)                  │
                    │                                         │
                    │  • Ultra-dense format                   │
                    │  • Recommend paging                     │
                    │  • Provide eviction candidates          │
                    │                                         │
                    └─────────────────┬───────────────────────┘
                                      │
                                      │ utilization ≥ 0.85
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │               CRITICAL                  │
                    │              (> 85%)                    │
                    │                                         │
                    │  • Emergency summarization              │
                    │  • Urgent eviction required             │
                    │  • Warn agent immediately               │
                    │                                         │
                    └─────────────────────────────────────────┘


                         ▲                           │
                         │                           │
                         │ utilization decreases     │
                         │ (any level)               │
                         │                           │
                         └───────────────────────────┘
```

### Pressure Level Details

| Level | Range | Compression | Action |
|-------|-------|-------------|--------|
| **LOW** | 0-50% | Verbose (L1) | None needed |
| **MEDIUM** | 50-70% | Dense (L2) | Monitor |
| **HIGH** | 70-85% | Ultra-dense (L3) | Recommend paging |
| **CRITICAL** | >85% | Ultra-dense (L3) | Urgent eviction |

### Hysteresis

To prevent oscillation, transitions down require 5% buffer:
- HIGH→MEDIUM: utilization < 0.65 (not 0.70)
- MEDIUM→LOW: utilization < 0.45 (not 0.50)

---

## 3. Session Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   [Session Start]                                                       │
│         │                                                               │
│         ▼                                                               │
│   ┌─────────────┐                                                       │
│   │   LOADING   │  Load persisted mind map                              │
│   └──────┬──────┘                                                       │
│          │                                                              │
│          │ state loaded                                                 │
│          ▼                                                              │
│   ┌─────────────┐                                                       │
│   │  BOOTSTRAP  │  Inject ultra-dense map to agent                      │
│   └──────┬──────┘                                                       │
│          │                                                              │
│          │ agent begins reasoning                                       │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                                                                 │  │
│   │                           ACTIVE                                │  │
│   │                                                                 │  │
│   │   ┌──────────────────────────────────────────────────────────┐ │  │
│   │   │                     Normal Operation                     │ │  │
│   │   │                                                          │ │  │
│   │   │  • get_context() ──► load resources                      │ │  │
│   │   │  • page_in() ──► activate resources                      │ │  │
│   │   │  • page_out() ──► evict resources                        │ │  │
│   │   │  • set_attention() ──► adjust priorities                 │ │  │
│   │   │  • annotate() ──► leave notes                            │ │  │
│   │   │                                                          │ │  │
│   │   └──────────────────────────────────────────────────────────┘ │  │
│   │                           │                                     │  │
│   │                           │ pressure > critical                 │  │
│   │                           ▼                                     │  │
│   │   ┌──────────────────────────────────────────────────────────┐ │  │
│   │   │                    Pressure Response                     │ │  │
│   │   │                                                          │ │  │
│   │   │  • Compress mind map to ultra-dense                      │ │  │
│   │   │  • Recommend evictions                                   │ │  │
│   │   │  • Agent decides what to page out                        │ │  │
│   │   │  • Execute page_out operations                           │ │  │
│   │   │                                                          │ │  │
│   │   └──────────────────────────────────────────────────────────┘ │  │
│   │                                                                 │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│          │                                                              │
│          │ session ending / reset                                       │
│          ▼                                                              │
│   ┌─────────────┐                                                       │
│   │  PERSISTING │  Save mind map state                                  │
│   └──────┬──────┘                                                       │
│          │                                                              │
│          │ state saved                                                  │
│          ▼                                                              │
│   ┌─────────────┐                                                       │
│   │    ENDED    │                                                       │
│   └─────────────┘                                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Session States

| State | Description |
|-------|-------------|
| **LOADING** | Reading persisted mind map from disk |
| **BOOTSTRAP** | Injecting minimal context to agent |
| **ACTIVE** | Normal operation, handling requests |
| **ACTIVE/PRESSURE** | High pressure, managing evictions |
| **PERSISTING** | Saving state before session end |
| **ENDED** | Session complete |

---

## 4. Eviction Policy State

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │                  LRU                    │
                    │           (Least Recently Used)         │
                    │                                         │
                    │  Sort by: last_accessed ASC             │
                    │  Default policy                         │
                    │                                         │
                    └─────────────────────────────────────────┘
                                      │
                                      │ set_priority("size_first")
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │              SIZE_FIRST                 │
                    │           (Largest First)               │
                    │                                         │
                    │  Sort by: size_tokens DESC              │
                    │  For rapid pressure relief              │
                    │                                         │
                    └─────────────────────────────────────────┘
                                      │
                                      │ set_priority("keep_relational")
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │           KEEP_RELATIONAL               │
                    │       (Protect relationship context)    │
                    │                                         │
                    │  Protected: SOUL, USER, IMPRESSIONS     │
                    │  Evict first: tools, technical files    │
                    │  For personal conversations             │
                    │                                         │
                    └─────────────────────────────────────────┘
                                      │
                                      │ set_priority("keep_technical")
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │            KEEP_TECHNICAL               │
                    │       (Protect technical context)       │
                    │                                         │
                    │  Protected: TOOLS, config, code         │
                    │  Evict first: relational, daily logs    │
                    │  For debugging/coding sessions          │
                    │                                         │
                    └─────────────────────────────────────────┘

                         ▲                           │
                         │                           │
                         │ set_priority("lru")       │
                         │ (reset to default)        │
                         │                           │
                         └───────────────────────────┘
```

### Policy Definitions

| Policy | Sort Order | Use Case |
|--------|------------|----------|
| **lru** | access_time ASC, attention ASC | Default, general use |
| **size_first** | size DESC | Emergency pressure relief |
| **keep_relational** | type (technical first) | Personal conversations |
| **keep_technical** | type (relational first) | Coding/debugging |

### Attention Override

Regardless of policy, attention weight is always the primary sort key:
```
actual_priority = (attention_weight, policy_sort_key)
```

Low-attention resources are always evicted before high-attention ones.
