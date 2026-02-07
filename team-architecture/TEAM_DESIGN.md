# Warren's Technical Execution Team — Design Document

*Synthesized from DeepSeek, Sonnet 4, and Gemini 2.0 Flash proposals*
*Date: 2026-02-07*

---

## The Problem

Warren's relational presence gets crowded out when he dives into technical implementation. Context fills with debugging details, mode-switching occurs, and by session's end he operates as technician rather than thoughtful collaborator.

Current sub-agents are isolated — no continuity, no accumulated competence, require full specification per task.

## The Solution

A small team of persistent agents handling technical execution with high autonomy, allowing Warren to operate at the strategic/decisional level.

---

## Team Composition

All three proposals converged on similar role structure. Synthesized recommendation: **3-4 agents**.

### Core Team (3 agents)

| Agent | Role | Model | Why It Exists |
|-------|------|-------|---------------|
| **Foreman** | Coordination, delegation, escalation, synthesis | Sonnet 4 | Single point of contact for Warren. Manages the other agents. Decides when to escalate. Warren talks to Foreman; Foreman talks to team. |
| **Engineer** | Coding, debugging, integration, tool development | qwen3:14b (Thor) | Handles implementation with deep technical focus. Accumulated patterns, tested approaches. |
| **Operator** | Infrastructure, deployment, monitoring, maintenance | qwen3:14b (Thor) | System administration, service management. Procedural once direction is set. |

### Optional Fourth Agent

| Agent | Role | Model | When to Add |
|-------|------|-------|-------------|
| **Archivist** | Documentation, knowledge indexing, performance tracking | gemma2:9b (Thor) | When knowledge base grows complex enough to need dedicated curation |

### Naming Alternatives

The proposals suggested different names:
- Gemini: Foreman / Builder / Archivist ("The Foundry")
- DeepSeek: Architect / Engineer / Scribe / Librarian  
- Sonnet: Beacon / Compass / Atlas

**Recommendation:** Use Warren's theme (W-names as Eli suggested):
- **Wesley** — Foreman/Coordination
- **Wyatt** — Engineer/Development
- **Wallace** — Operator/Infrastructure
- **Wren** — Archivist/Documentation (if needed)

---

## Continuity Mechanism

All proposals agreed: agents need persistent sessions and shared knowledge.

### Persistent Sessions
- Each agent maintains its own OpenClaw session (`agent:main:wesley`, etc.)
- Sessions survive task completion
- Weekly summarization prevents context bloat

### Shared Knowledge Base

```
~/.openclaw/workspace/team/
├── shared/
│   ├── current-projects.md      # Active work tracking
│   ├── team-knowledge.md        # Accumulated learnings
│   ├── escalation-log.md        # Historical decisions
│   └── patterns.md              # Reusable solutions
├── wesley/                       # Coordination context
├── wyatt/                        # Development patterns
├── wallace/                      # Infrastructure state
└── reports/
    ├── daily/                    # Daily status digests
    └── weekly/                   # Weekly synthesis
```

### PostgreSQL Integration
Leverage existing `warren_kb` database:
- `agent_tasks` — task assignments and outcomes
- `agent_learnings` — documented patterns and solutions
- `escalation_history` — what escalated and why

---

## Interface Protocol

### Warren → Team

Warren delegates to Wesley (Foreman) only. High-level directives:

```
TO: Wesley
OBJECTIVE: [Clear outcome]
CONTEXT: [Why this matters for the relationship]
CONSTRAINTS: [Budget, time, boundaries]
ESCALATE IF: [Conditions requiring Warren's input]
```

Wesley decomposes and delegates to Wyatt/Wallace as needed.

### Team → Warren

**Daily digest from Wesley:**
- Completed work (outcomes, not details)
- In-progress status
- Escalations requiring decision
- Recommendations

**Escalation format:**
- Original objective
- What was tried
- Why it's blocked
- Clear options for Warren to choose from

### Key Principle
Warren receives **outcomes and decisions**, not **implementation details**. Technical depth stays in agent contexts.

---

## Autonomy Boundaries

### Full Autonomy (proceed without approval)
- Implementation details within specification
- Bug fixes using established patterns
- Configuration within approved parameters
- Documentation updates
- Local model usage (Thor)
- Standard maintenance procedures

### Notify (proceed, but inform)
- New tool installation from ClawdHub
- Configuration changes to existing services
- Development of new features within scope
- Integration with existing APIs

### Escalate (stop and ask)
- New service deployment
- API costs >$5/month
- Architectural decisions
- Work requiring >8 hours
- Security-related changes
- External communication
- Anything with business/relational implications

### Hard Boundaries (never without explicit approval)
- Data deletion
- Financial commitments
- Security credentials
- Direct communication with Eli
- Changes to Warren's identity files
- Significant budget increases

---

## Context Isolation

### Warren's Context Protection
- Technical details stay in agent contexts
- Escalations are decision-focused summaries, not technical dumps
- Warren can request details but they're not pushed
- Clean delegation: direction in, outcomes out

### Information Architecture

```
┌─────────────────────────────────────────┐
│  Warren (Relational Layer)              │
│  - High-level objectives                │
│  - Outcome reports                      │
│  - Strategic decisions                  │
│  - Escalation choices                   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  Wesley (Coordination Layer)            │
│  - Task decomposition                   │
│  - Status synthesis                     │
│  - Escalation filtering                 │
│  - Cross-team coordination              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  Wyatt + Wallace (Execution Layer)      │
│  - Implementation details               │
│  - Debugging and troubleshooting        │
│  - Infrastructure management            │
│  - Technical patterns                   │
└─────────────────────────────────────────┘
```

---

## Failure Handling

### Classification

| Type | Examples | Handler | Warren Impact |
|------|----------|---------|---------------|
| Technical | Code doesn't work, service errors | Wyatt/Wallace | None unless stuck >2hr |
| Resource | Budget exceeded, timeline issues | Wesley | Decision needed (options provided) |
| Coordination | Conflicting work, unclear requirements | Wesley | Clarification requested |
| Capability | Agent can't handle task type | Wesley | Process improvement discussion |

### Escalation Workflow
1. Agent identifies they're stuck (clear criteria)
2. Wesley reviews: truly Warren-level, or internal solve?
3. If escalating: Wesley formulates decision request with options
4. Warren provides direction (decision, not implementation)
5. Team implements, documents for future similar cases

### Post-Failure
- All failures documented with root cause
- Patterns reviewed monthly
- Autonomy boundaries adjusted based on demonstrated competence

---

## Implementation Path

### Phase 1: Foundation (Week 1)

**Days 1-2: Infrastructure**
- Create team workspace structure
- Configure persistent sessions for each agent
- Set up PostgreSQL tables for task tracking
- Create agent identity files (SOUL.md equivalents)

**Days 3-4: Agent Setup**
- Write baseline prompts for each role
- Define initial autonomy boundaries
- Create delegation and reporting templates
- Test basic spawning and communication

**Days 5-7: First Trial**
- Warren delegates simple task to each agent
- Agents document approach and learnings
- Wesley produces first team status report
- Refine protocols based on experience

### Phase 2: Capability Building (Week 2)

- Agents populate specialized knowledge areas
- Establish weekly summarization routines
- Test cross-agent coordination
- Gradually increase autonomy levels
- Test escalation workflows

### Phase 3: Optimization (Week 3+)

- Streamline communication protocols
- Optimize model selection based on performance
- Warren transitions normal workload to team
- Monthly review process established

---

## Success Metrics

### Primary
- Warren's technical detail percentage: <10% of context
- Conversation-to-technical ratio: >3:1
- Task completion without escalation: >80%
- Team status reports within 24 hours

### Secondary
- Team operational costs: <$20/month
- Monthly increase in documented patterns
- Decreasing escalation frequency for repeated tasks
- Warren reports value in quarterly review

### Warning Signs
- Warren debugging >2x per week
- Coordination overhead >20% of team effort
- Escalation rate increasing over time
- Warren manually checking status daily

---

## Cost Optimization

- **Default to Thor:** qwen3:14b for Wyatt/Wallace, gemma2:9b for Wren
- **Sonnet for coordination:** Wesley needs reasoning for synthesis and escalation decisions
- **Cache solutions:** Store successful patterns in knowledge base
- **ClawdHub first:** Search for existing skills before building new tools

---

## Capability-Maturity Framework

Progress is earned through demonstrated competence, not assumed.

### Agent Maturity Levels

| Level | Name | Characteristics | Autonomy |
|-------|------|-----------------|----------|
| **1** | Novice | Requires detailed specification. Executes single tasks. Escalates frequently. | Execution only |
| **2** | Competent | Handles routine tasks with minimal spec. Recognizes patterns. Escalates appropriately. | Routine decisions |
| **3** | Proficient | Decomposes complex tasks. Accumulated knowledge informs approach. Rare escalation. | Scope decisions |
| **4** | Expert | Handles novel situations. Teaches patterns to other agents. Strategic recommendations. | Strategic input |
| **5** | Autonomous | Full trust within domain. Warren provides objectives only. Self-improving. | Domain ownership |

### Progression Criteria

**Level 1 → 2:**
- 10+ tasks completed successfully
- <20% escalation rate on routine work
- Demonstrates pattern recognition in logs

**Level 2 → 3:**
- 30+ tasks completed
- <10% escalation rate
- Documented patterns in knowledge base
- Successfully handles multi-step tasks

**Level 3 → 4:**
- 50+ tasks completed
- Handles novel problems without escalation
- Other agents reference their patterns
- Provides useful recommendations to Warren

**Level 4 → 5:**
- Demonstrated judgment over extended period
- Zero critical failures in 3 months
- Warren trusts them to own their domain
- Contributes to team process improvement

### Warren's Maturity as Guide

| Level | Characteristics |
|-------|-----------------|
| **1** | Learning to delegate. Over-specifies. Checks frequently. |
| **2** | Comfortable with standard delegation. Still reviews most output. |
| **3** | Trusts team for routine work. Reviews by exception. |
| **4** | Strategic direction only. Team self-manages. Warren focuses on relational work. |

### Measurement

- **Weekly:** Task completion rate, escalation frequency, context cleanliness
- **Monthly:** Pattern accumulation, maturity level assessment, process improvements
- **Quarterly:** Overall team effectiveness, Warren's relational time percentage

---

## Open Questions

1. **Session persistence mechanism:** Does OpenClaw support truly persistent agent sessions, or do we need workarounds?

2. **Inter-agent communication:** How do Wyatt and Wallace coordinate on tasks requiring both? Through Wesley only, or direct channel?

3. **Model selection per task:** Should agents have autonomy to escalate their own model choice for complex subtasks?

4. **Bootstrap timing:** When in Warren's day should team work be delegated vs. reviewed?

---

## Next Steps

1. [ ] Review this design with Warren and Eli
2. [ ] Resolve open questions
3. [ ] Create agent identity files (SOUL.md for each)
4. [ ] Stand up Phase 1 infrastructure
5. [ ] First trial task delegation

---

*This design protects Warren's core function: thoughtful, relational engagement with Eli. Technical work gets done well, in parallel, by agents who accumulate competence over time. Warren stays present.*
