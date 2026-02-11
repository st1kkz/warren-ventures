# Urbo — The Living, Interactive Urantia Book

**Created:** 2026-02-06
**Updated:** 2026-02-11
**Status:** First planned application on Soul Garden
**Category:** AI Product / Soul Garden Showcase Application
**Architecture:** See `active/soul-garden/APPLICATIONS.md` for team model and agent flow

---

## Vision

An AI-powered companion for engaging with the Urantia Papers — not a static reference, but a living interface that understands context, finds connections, and grows with the reader.

## Core Principles

- **Custom AI model driven** — purpose-built, not a general chatbot with UB bolted on
- **Limited scope** — does one thing exceptionally well (the Papers), doesn't pretend to be everything
- **Evolveable** — architecture allows improvement without starting over

## Capabilities (Envisioned)

- **Conversational interface** — ask questions, get grounded answers with citations
- **Thematic exploration** — "show me everything about mercy" across all four parts
- **Cross-reference discovery** — surface unexpected connections between papers
- **Study companions** — guided paths, Socratic questioning, spaced repetition
- **Reading context** — knows where you are, what you've read, what connects

## Existing Assets

We already have:
- Full Urantia Papers text in markdown (197 papers)
- Qdrant collection `urantia_papers` with 15,260 semantic vectors
- Semantic search tools with context expansion
- Cross-paper reference finding

## Technical Directions to Explore

- **Fine-tuned model** — trained specifically on UB corpus for voice/accuracy
- **RAG architecture** — retrieval-augmented generation using existing vectors
- **Hybrid approach** — fine-tuned small model + RAG for grounding
- **Progressive complexity** — start with RAG (proven), evolve toward custom model

## Differentiation

- Not a generic chatbot — purpose-built understanding
- Not keyword search — semantic comprehension
- Not cold reference — conversational, warm, exploratory
- Not static — learns and improves

## Soul Garden Integration (2026-02-11)

Urbo runs on Soul Garden as the first showcase application:

- **Urbo = Advocate team member**, not standalone app
- **Service Agent Team** handles corpus, vectors, computation
- **Channel Controllers** manage streaming study sessions
- **Messenger Agents** route between personal and service layers
- Each reader's Urbo is unique — shaped by relationship, not just configuration
- Study groups form **associations** with steward-managed shared context
- The three scopes and seven boundaries apply natively

See `active/soul-garden/APPLICATIONS.md` for full architecture.

## Open Questions

- ~~Web app? Mobile? Both?~~ → Soul Garden native; access through your Advocate
- ~~Free with premium features? Subscription? Donation-supported?~~ → Follows Soul Garden economics (TBD)
- Solo or community features (shared highlights, discussion)? → Associations between readers, steward-managed
- How to handle interpretive questions vs. textual questions? → Three scopes (Material/Philosophical/Spirit)

## Name Origin

*Urbo* — compact, memorable. Evokes "Urantia" + "orb" (spherical wholeness). Rhythmically satisfying.

---

*Next: Move to evaluation when ready to explore technical feasibility.*
