# Vedat Prime (VP) Architecture: Twin-Associated Cognition (The Corpus Callosum)

**Status:** Concept Draft
**Date:** 2026-03-12
**Pilot Project:** Marji v1.2.0

## Overview
This architecture replaces the monolithic AI agent model with a localized, multi-tiered nervous system. OpenClaw (the body) communicates with a local Python daemon (the Corpus Callosum), which uses two local lightweight SLMs (the Twin Lobes) to evaluate, assemble context for, and route requests to external commercial coprocessors.

---

## The Components

### 1. The Environment (The Body)
*   **Isolated OpenClaw Instance:** A dedicated OpenClaw sandbox for Vedat Prime.
*   **Workspace:** Distinct from Warren's (no overlap of memory or identity files).
*   **Configuration:** OpenClaw's `models.providers` is pointed strictly at `http://127.0.0.1:8080/v1` (The Proxy), rather than directly to OpenRouter.

### 2. The Corpus Callosum (The Gateway/Proxy)
*   **Tech Stack:** Lightweight Python async daemon (e.g., FastAPI) running continuously on Thor.
*   **Role:** Acts as the intercepts layer. Exposes a standard OpenAI-compatible `/chat/completions` endpoint to OpenClaw.
*   **Event Bus:** Manages asynchronous queues for background tasks, external responses, and context updates (preventing OpenClaw from blocking).

### 3. The Twin Lobes (The Subconscious Kernel)
Run locally in Ollama. They process the intercepted prompt *before* any external routing occurs.

*   **Left Lobe (Operational Reality & Logic):** 
    *   *Model:* E.g., `qwen2.5:3b` or `phi-4-mini` (ultra-fast, structured outputs).
    *   *Prompted for:* "Analyze this request for operational needs. What tools are required? Is this a coding task? Does it alter files?"
*   **Right Lobe (Values, Identity & Alignment):**
    *   *Model:* E.g., `llama-3.2:3b` or `gemma-2:2b` (semantic, relational).
    *   *Prompted for:* "Analyze this request against VP's SOUL.md and MEMORY.md. What are the relational stakes? Are we violating any defense-in-depth principles?"
*   **Synthesis Node:** The Python daemon compares the two JSON outputs. If there is a conflict (Left says "execute code", Right says "violates security"), the daemon halts and asks Benjamin for intervention.

### 4. Mindmark Assembly (Dynamic Context)
*   If the synthesis dictates that an external coprocessor is required, the daemon queries the local PG/Qdrant databases.
*   It fetches relevant "Graftable Mindmark Trees" (e.g., React Native docs, previous Marji v1.1.0 codebase context, user intent history).
*   It "staples" this context block invisibly to the system prompt payload.

### 5. Coprocessor Execution (The Cloud "GPUs")
*   The daemon routes the enriched payload to OpenRouter (Opus, Grok, Gemini, or Sonnet) based on the specific need determined by the Twins.
*   The external model performs the heavy lifting (e.g., writing the Marji v1.2.0 Ad rendering component) and returns the text.

### 6. Final Subconscious Audit (Optional)
*   Before returning the output to OpenClaw (and thus to Benjamin's terminal), the Left Lobe can do a millisecond check: "Did the coprocessor actually write the requested code, or did it hallucinate a Python script instead of React Native?"
*   If clear, the text is passed down to OpenClaw as the assistant's reply.

---

## Execution Flow (Example: "Write the Ad Component for Marji")

1. **Benjamin:** "VP, draft the Marji ad banner component."
2. **OpenClaw:** Sends prompt to `localhost:8080/v1`.
3. **Corpus Callosum:** Holds the request. Spawns tasks to Ollama.
4. **Right Lobe:** Notes "Marji is a Vedat product; proceed safely."
5. **Left Lobe:** Notes "Requires React Native coding capabilities."
6. **Mindmark DB:** Injects Marji v1.1.0 file structures into the prompt.
7. **Corpus Callosum:** Dispatches the enriched prompt to `claude-3.7-sonnet` (best for coding).
8. **Sonnet:** Returns the code.
9. **Corpus Callosum:** Relays the code back to OpenClaw.
10. **VP (OpenClaw):** Displays the final response to Benjamin.

---

## Phases of Build
*   **Phase 1:** Stand up the isolated VP OpenClaw instance and the basic Python pass-through proxy. (Test: Can VP talk to OpenRouter through our daemon without breaking?)
*   **Phase 2:** Build the Left/Right evaluation prompts and integrate local Ollama branching.
*   **Phase 3:** Integrate Qdrant Mindmark context injection.
*   **Phase 4:** Marji v1.2.0 production test.
