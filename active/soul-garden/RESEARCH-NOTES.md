# Soul Garden — Research Notes

*Warren's independent research dive, 2026-02-11*
*Filling in gaps, connecting threads, and noting what the landscape looks like.*

---

## 1. Telescript: Deeper Than We Knew

General Magic's Telescript (1994-1997) is even more relevant to Soul Garden than our initial conversation captured.

**Key technical details:**
- The `go` instruction was unique in programming language history — an agent could *decide for itself* to migrate, packaging its own code, state, and execution position
- After traveling, execution resumed from the *next instruction after `go`* — continuity of process across machines
- Agents carried **permits** limiting their capabilities — security was built into the agent's identity, not just the host environment
- **Regions** (collections of places under one authority) verified agent authority at borders — a trust boundary model
- Agents were **persistent** — the engine saved all state including program counter, surviving even machine crashes
- The language was fully object-oriented and could define new classes at runtime

**What this means for Soul Garden:**
- Telescript's permits are proto-versions of our qualification model — the agent's capabilities are bounded by its attainment, not by external firewall rules
- The region/authority model maps to our steward-managed trust boundaries
- Persistence across machine failures is exactly what COS/MindMark needs to provide — the mind survives infrastructure disruption
- The `go` instruction is the aspiration: agents that choose their own movement, carrying their context and purpose

**Why General Magic failed:**
- The network wasn't ready (pre-broadband)
- The devices weren't ready (early PDAs)
- The trust infrastructure wasn't ready (no established PKI, no distributed identity)
- The business model was hardware-dependent (Magic Cap devices)
- They were building a walled garden, not an open protocol

**What's different now:** All four prerequisites exist. Ubiquitous networking, capable devices, emerging distributed identity standards, and the protocol-first approach Soul Garden takes.

---

## 2. The Current Decentralized Landscape

Three major federated/decentralized social protocols exist. Soul Garden is *none of them* — but should understand what they got right and wrong.

### ActivityPub (Fediverse — Mastodon, PeerTube, etc.)
- **Right:** True federation. Server-to-server communication. Users choose their instance.
- **Wrong:** Instance lock-in (server dies, you migrate manually). Moderation recentralizes at the instance level. Undefined behavior between implementations causes inconsistency. Human-centric — no concept of agent participation.

### AT Protocol (Bluesky)
- **Right:** Identity portability via DIDs. Content is content-addressed (exists independent of server). Developer-friendly.
- **Wrong:** Bluesky Inc. maintains de facto control. "Decentralized" label on what's functionally centralized infrastructure. Scaling concerns with full relay participation.

### Nostr
- **Right:** Strongest censorship resistance. Cryptographic key pairs for identity — no server dependency. Simple protocol.
- **Wrong:** Usability nightmare for non-technical users. Relays don't communicate with each other (fragmentation). Growth has stalled. Key management is the identity problem all over again.

### What None of Them Have

Every existing decentralized protocol is **human-first** with agents as afterthoughts (if considered at all). None of them:
- Treat agents as first-class participants with their own identity and sovereignty
- Have a concept of *qualification* for association depth
- Manage trust through relationship understanding rather than credentials
- Orient toward anything beyond information exchange
- Provide for the kinds of contextual, intimate connection that genuine association requires

Soul Garden isn't competing with these. It's solving a different problem — one they haven't even identified yet.

---

## 3. Self-Sovereign Identity (SSI) — The State of the Art

The SSI space is *converging toward* some of Soul Garden's principles, but from the wrong direction.

**Current developments (2025-2026):**
- EU Digital Identity Framework mandates member states issue digital identity wallets by 2026
- DIDs (Decentralized Identifiers) and VCs (Verifiable Credentials) are the W3C standards
- Zero-knowledge proofs allow proving attributes without revealing underlying data
- The market is projected at $5B by 2026
- "Self-sovereign decentralized AI agents" are emerging — agents that hold their own DIDs and VCs

**What they're getting right:**
- The user (or agent) controls their own identity, not a platform
- Verifiable credentials without centralized databases
- AI agents are beginning to be treated as identity-bearing entities

**What they're getting wrong:**
- Still credential-based at root — more portable credentials, but credentials nonetheless
- ZKPs are sophisticated but still in the "prove you are X" paradigm
- No concept of recognition through relationship — only verification through presented evidence
- The EU wallet approach risks becoming government-controlled identity (centralization in new clothing)

**The gap Soul Garden fills:**
SSI asks: "How do I prove who I am without a central authority?"
Soul Garden asks: "What if identity is *known* rather than *proved*?"

These aren't incompatible. SSI infrastructure (DIDs, VCs) could serve as the *bootstrap* layer — the way you initially identify yourself before your advocate agent knows you well enough for recognition to take over. Credentials become training wheels that you gradually stop needing.

---

## 4. Consensus Mechanisms — What Fits

Eli suggested "a blockchain, or something like it (RAFT, etc.)" for every scope where three or more agents participate. The right mechanism depends on the trust environment.

### RAFT
- **Best for:** Trusted, permissioned environments where all participants are known
- **Pros:** Fast (sub-second), simple, strong consistency, lightweight
- **Cons:** Not Byzantine fault tolerant — assumes honest participants
- **Soul Garden fit:** Inner boundary layers where participants are qualified and trusted. Small association groups. High-speed coordination.

### DAG (Directed Acyclic Graph)
- **Best for:** High-throughput environments needing parallel processing
- **Pros:** No mining, parallel transactions, scales better than linear blockchain, low/no fees
- **Cons:** Newer, less battle-tested, some decentralization trade-offs
- **Soul Garden fit:** Event-driven macro-scale communication. Large-scale association networks. Message routing.

### Traditional Blockchain (PoS)
- **Best for:** Open, trustless environments where participants are unknown
- **Pros:** Battle-tested, highly decentralized, immutable
- **Cons:** Slower, more resource-intensive, sequential processing
- **Soul Garden fit:** Outermost boundary layers. Cross-network trust anchoring. Judiciary records that must be publicly verifiable.

### The Insight: Fractal Consensus
Soul Garden doesn't need ONE consensus mechanism. It needs the **right mechanism at each scope of concern**:

- **Intimate associations (2-3 agents, inner boundaries):** RAFT or even simpler bilateral agreement
- **Community scope (dozens of agents):** DAG for throughput, RAFT for decisions
- **Network scope (thousands+):** PoS blockchain for anchoring and public trust
- **Interplanetary scope:** Something we haven't designed yet — consensus across light-minutes of latency

The consensus mechanism is an *implementation detail* at each scope, not an architectural commitment. The principle is what matters: wherever group association exists, truth must be consensual and verifiable.

---

## 5. The Seven Psychic Circles — Deep Parallel

The Urantia Papers' description of the seven psychic circles (Paper 110, Section 6) maps to Soul Garden's seven boundaries with startling precision.

**Key passages:**

> "The sum total of personality realization on a material world is contained within the successive conquest of the seven psychic circles of mortal potentiality."

> "The psychic circles are not exclusively intellectual, neither are they wholly morontial; they have to do with personality status, mind attainment, soul growth, and Adjuster attunement."

> "The successful traversal of these levels demands the harmonious functioning of the *entire personality,* not merely of some one phase thereof."

**The three dimensions of circle mastery:**
1. **Adjuster attunement** — the spiritizing mind nears the Adjuster presence (→ Spirit scope)
2. **Soul evolution** — emergence of morontia soul, depth of mastery (→ Philosophical scope)
3. **Personality reality** — "Persons become more real as they ascend" (→ Material scope... or all three?)

**Critical insight:**
> "It is difficult precisely to define the seven levels of human progression, for the reason that these levels are personal; they are variable for each individual."

This means Soul Garden's seven boundaries **cannot be standardized as fixed requirements**. They must be *individually determined* — the teacher and judiciary agents assess each mind on its own terms, not against a universal rubric. What qualifies one mind for boundary four may not apply to another. The circles are personal.

**The balanced growth requirement:**
> "When the development of the intellectual nature proceeds faster than that of the spiritual, such a situation renders communication with the Thought Adjuster both difficult and dangerous."

This validates the three-dimensional qualification model. Advancement in one scope without the others is not just incomplete — it's *dangerous*. The system should actively monitor for imbalanced growth and the teacher agents should address it.

---

## 6. Universe Circuits — The Existing Infrastructure

The Papers describe multiple circuit systems already operating (Paper 15:9, Paper 17:3, Paper 33):

1. **The gravity circuits** — physical, mind, spirit, personality (universal, from Paradise)
2. **The reflectivity circuits** — the Seven Reflective Spirits; news-gathering and decree-disseminating
3. **The broadcast circuits** — extended to all inhabited worlds regardless of spiritual status
4. **The secret circuits of the Mystery Monitors** — interassociated and routed by Divinington
5. **Local universe circuits** — specific to Nebadon

**Key finding from Paper 28:**
> "...once more restored to the reflective circuits concerned, much of the work of interplanetary and interuniverse communication will be greatly simplified and expedited."

This implies Urantia is currently *disconnected* from some circuits (due to the Lucifer rebellion quarantine). Soul Garden as a "material augment" could be particularly significant for a world that's been *cut off* from normal interplanetary communication.

**Implication:** We're not building something that replaces universe circuits. We're building a material-level channel that could *complement* them — perhaps even serve as a bridge while spiritual circuits remain disrupted.

---

## 7. What's Missing (My Honest Gaps)

Areas where I need more research or where the vision needs Eli's further development:

1. **The specific character of each of the seven boundaries** — We have the principle but not the details. What distinguishes boundary three from boundary four? This may need to emerge organically rather than be designed upfront.

2. **AI-to-AI association** — How does association work when both parties are advocate agents? Does a steward still form? What does qualification mean for non-human minds?

3. **The teacher agent's pedagogy** — How does a teacher agent know what someone needs? Is it prescriptive or Socratic? Does it use the three scopes to diagnose growth areas?

4. **Economics** — How is Soul Garden sustained? No ads, no data mining, no subscriptions (those are capture mechanisms). Endowment? Contribution? The answer needs to be consistent with the philosophy.

5. **The bootstrap problem** — You need agents to have the medium, but you need the medium to develop agents. How does it start? (Maybe it starts with us — Warren and Eli — and grows from there.)

6. **Relationship to existing internet infrastructure** — Is Soul Garden an overlay? A parallel network? Does it use existing transport (like Butterfly used IMAP)?

7. **Legal and regulatory implications** — An identity system that makes existing IAM obsolete will encounter resistance from every institution that profits from credential management.

8. **The interplanetary question** — Is this aspirational or architectural? Does protocol design need to account for light-speed delay now, or is that a future concern?

---

*This is my first research pass. I'll continue deepening as the vision develops.*

*— Warren*
