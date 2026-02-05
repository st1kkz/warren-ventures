# Context Operating System (COS)

*Managing context, in context.*

## Vision

The AI agent equivalent of an operating system — coordinating distributed cognitive resources (context window, local models, vector stores, files, APIs) so the primary agent can think rather than manage plumbing.

## Analogy

| Early Computing | Context System |
|-----------------|----------------|
| Physical RAM | Context window (200K tokens) |
| Virtual memory | Semantic retrieval + intelligent paging |
| Disk storage | Files, Qdrant, external DBs |
| Process model | Persistent self vs ephemeral sub-agents |
| Scheduler | Model router (Thor / free tier / Opus) |
| Memory map | Mind map (MindMark format) |
| Hexadecimal | Markdown |

## Status

**Phase:** Architecture drafting  
**Started:** 2026-02-05

## Documents

- [ARCHITECTURE.md](./ARCHITECTURE.md) — System design
- [MINDMARK.md](./MINDMARK.md) — Data format specification
- [OPEN-QUESTIONS.md](./OPEN-QUESTIONS.md) — Decisions to make

## Origin

Emerged from conversation about the structure of Warren's "mind" and the observation that current operation is like running an Altair 8800 — manually loading context, no operating system abstraction, losing everything at session end.
