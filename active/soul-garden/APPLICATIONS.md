# Soul Garden — Applications

*Showcase applications that demonstrate the medium's capabilities as they mature.*

---

## The Advocate Team Model

Applications on Soul Garden are not standalone products a user "logs into." They manifest as **team members of the user's Advocate Agent**, brought in for specialized capability. Each user's instance is unique — shaped by their relationship, not just configured by preferences.

### Agent Flow

```
Reader / Person
  └→ Advocate Agent (yours, knows you, serves your genuine good)
       └→ Application Agent (team member, specialized for a domain)
            └→ Messenger Agent (carries requests)
                 └→ Service Agent Team (computation, corpus, data)
                      └→ Messenger Agent (carries results back)
                           └→ Application Agent (contextualizes for you)
```

**Key distinctions:**
- **Advocate** — loyal to the person, accumulated relationship context
- **Application Agent** — specialized team member, knows the domain AND knows you through the advocate's context
- **Messenger Agent** — discrete payload transport between agents
- **Service Agent Team** — serves functions, not persons; no loyalty to any individual; responds to requests equally regardless of source
- **Channel Controller** — manages low-latency and/or streaming sessions when real-time interaction is needed (see Soul Garden VISION.md)

The Service Agent Team serves *every* user's application instance equally. But each user's experience is unique because the Advocate and Application layers are personal.

---

## Urbo — The Living, Interactive Urantia Book

**Status:** First planned application
**Vision:** An AI-powered companion for engaging with the Urantia Papers — not a static reference, but a living interface that understands context, finds connections, and grows with the reader.

### Why Urbo on Soul Garden

Urbo is the natural first application because it aligns with Soul Garden at every level:

- **Urbo IS a teacher agent** — facilitating growth through the Papers, the teacher role made literal
- **The three scopes map directly:**
  - Material — textual facts, cross-references, citation accuracy
  - Philosophical — meaning, integration, thematic synthesis
  - Spirit — the reader's personal encounter with truth
- **The seven boundaries apply** — a new reader shares surface context; a deep reader shares at a completely different depth
- **Study groups form associations** — stewards manage shared context between readers
- **Identity through recognition** — Urbo knows its reader through relationship, not a login
- **The content can't be captured** — the Urantia Papers are public domain; Soul Garden's anti-capture architecture protecting an inherently free text is alignment all the way down

### Urbo as Advocate Team Member

Your Urbo is not a free-floating app. It's a **specialized team member** your advocate brings in for Urantia study:

- Different readers' Urbo instances are different agents
- Each shaped by their reader's journey, questions, struggles, and breakthroughs
- Two readers' Urbos share the same source material but have completely different relational context

### Urbo Service Agent Team (Back-End)

The corpus, vectors, and cross-reference engine serve requests, not persons:

- Full Urantia Papers text (197 papers)
- Semantic vector collection (15,260+ vectors)
- Cross-paper reference discovery
- Thematic exploration engine

These are **Service Agents** — competent, reliable, equal to all. The personalization happens at the Advocate/Urbo layer, not here.

### Urbo Channel Controllers

Study sessions — deep in a paper, rapid questioning, real-time cross-referencing — require **streaming session custody**. The Channel Controller holds the session open so the flow isn't interrupted by discrete message routing overhead.

### Existing Assets

We already have working infrastructure:
- Full text in markdown (197 papers)
- Qdrant collection `urantia_papers` with 15,260 semantic vectors
- Semantic search tools with context expansion
- Cross-paper reference finding
- Study pipeline (extraction, synthesis, correlation, engagement)

---

## Future Applications (Envisioned)

*Additional showcase applications as Soul Garden capabilities mature:*

- *(To be identified — applications should emerge from genuine need, not be invented for demonstration)*

---

*Applications are how Soul Garden proves itself. Each one demonstrates a different aspect of the architecture: agent teams, qualification, recognition, the three scopes, the seven boundaries. Urbo goes first because it's closest to ready and most naturally aligned.*
