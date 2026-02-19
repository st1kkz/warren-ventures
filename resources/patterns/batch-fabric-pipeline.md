# Batch Fabric Pipeline Pattern

*Deep synthesis across a large related body of information, in preparation for meaningful engagement with presence of mind.*

*Documented 2026-02-19 from the Feb 6, 2026 Urantia Papers processing run.*

---

## 1. Pattern Overview

**What:** Process a large corpus of documents through a multi-stage AI pipeline using [Fabric](https://github.com/danielmiessler/fabric) CLI, with different models at each stage for cost/quality optimization.

**Purpose:** The mechanical stages (extraction, synthesis, correlation) exist to prepare the ground for *genuine engagement*. The pipeline does the reading so that the mind doing the thinking arrives ready — not summarizing cold, but entering a conversation already in progress. This is how you read deeply at scale.

**When to use:** You have a substantial body of related material that deserves more than summarization — where the goal is understanding, not processing. The pattern scales from dozens to hundreds of documents, completed in hours at minimal cost.

**Key properties:**
- **Idempotent** — each stage checks for existing output; safe to re-run
- **Stage-separated** — different models for different cognitive tasks
- **Cost-optimized** — cheap models for mechanical work, expensive models only where quality matters
- **Batchable** — a simple shell loop drives the entire corpus through the pipeline

**The Feb 6 instance:** 197 Urantia Papers (~35KB each) processed through 3 stages in ~5 hours, for roughly $6-8 total.

---

## 2. Architecture

### Pipeline Stages

```
    DOCUMENT TEXT
         │
         ▼
┌─────────────────────┐
│  STAGE 1: Extract   │  Cheap model (DeepSeek, ~$0.001/doc)
│  Mechanical pull    │  Quotes, terms, structure, entities
│  No interpretation  │  Output: raw_extraction.md
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  STAGE 2: Synthesize│  Quality model (Sonnet, ~$0.02-0.04/doc)
│  Interpretive       │  Core teaching, key concepts, tensions
│  Input: Stage 1 +   │  Output: synthesis.md
│    original text    │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  STAGE 3: Correlate │  Cheap model (DeepSeek, ~$0.001/doc)
│  Cross-reference    │  Connections to other docs in corpus
│  Input: Stage 2 +   │  Output: correlations_text.md
│    semantic search  │
└─────────────────────┘
         │
         ▼
   [HUMAN ENGAGEMENT]    Not automated — the point of all the prep
```

### Tool Stack

| Component | Role | Location |
|-----------|------|----------|
| **Fabric CLI** | Prompt execution framework | `~/.local/bin/fabric` (v1.4.400) |
| **Custom patterns** | Stage-specific system prompts | `~/.config/fabric/patterns/` |
| **OpenRouter** | API gateway to models | DeepSeek + Sonnet via OpenRouter |
| **Qdrant** | Semantic search for correlations | `192.168.1.200:6333`, collection `urantia_papers` |
| **Shell script** | Per-document pipeline orchestration | `tools/fabric/run_urantia_pipeline.sh` |
| **tmux** | Persistent session for long batch runs | `tmux new-session -d -s <name>` |
| **Git** | Progress checkpointing | Auto-commits at milestones |

### Model Selection Rationale

| Stage | Task Type | Model | Cost/doc | Why |
|-------|-----------|-------|----------|-----|
| 1 — Extract | Extraction | DeepSeek Chat | ~$0.001 | Mechanical; doesn't need reasoning. DeepSeek is accurate and cheap |
| 2 — Synthesize | Analysis | Claude Sonnet | ~$0.02-0.04 | Interpretive quality matters; Sonnet produces markedly better synthesis |
| 3 — Correlate | Analysis | DeepSeek Chat | ~$0.001 | Follows structured format well; local models (qwen3:14b) tested but scored 2/5 — ignored output structure |

**Total per document:** ~$0.03-0.04
**Total for 197 documents:** ~$6-8

---

## 3. Orchestration — The Feb 6, 2026 Batch Run

### Timeline

| Time (CST) | Event | Evidence |
|------------|-------|----------|
| 12:50pm | Pipeline tested on Papers 57-59 manually | commit `82828ae` |
| ~5:47pm | Session starts; pipeline script built and validated | Session `c6f64f26` |
| ~6:25pm | `run_urantia_pipeline.sh` written, tested on Paper 58 | Script committed |
| ~6:37pm | Pipeline split into 3a-i (text correlations) and 3a-ii (notes correlations) | Updated script |
| ~6:55pm | Cron infrastructure set up (batch-prep, status, indexer) | Crons created |
| ~7:02pm | Session ends, prep for reset | — |
| ~7:01pm | Eli (via Telegram): "I have decided we should get the whole book through correlation" | Session `7c2d3feb` |
| ~7:02pm | Sub-agent spawned for bulk processing | First attempt |
| ~7:24pm | Sub-agent stalled — only completed 1 paper; background process killed on session end | Debugging |
| ~7:29pm | Eli installs tmux | `tmux installed` |
| ~7:31pm | **tmux batch launched:** `for i in $(seq 0 196)` loop | The real run begins |
| 8:15pm | **47 papers prepped** | commit `cc9791d` |
| 8:28pm | **65 papers** | heartbeat check |
| 8:55pm | **84 papers (43%)** | commit `44ff45e` |
| 10:19pm | **141 papers (72%)** | Telegram update |
| 10:27pm | Qdrant indexing started in parallel (435 vectors indexed) | `urantia_synthesis` collection |
| 11:03pm | **173 papers (88%)** | Telegram update |
| 11:33pm | **196 papers** — bulk batch complete | commit `ab2fe69` |
| 11:58pm | Paper 117 gap-filled; **all 197 papers ready** | commit `b194295` |

**Wall clock for tmux batch:** ~4.5 hours (7:31pm → ~midnight)
**Rate:** ~2-3 minutes per paper through all 3 stages

### Orchestration Evolution (3 attempts)

**Attempt 1: Sub-agent spawn** (~7:02pm)
```
sessions_spawn with task: "For each paper from 0-196 that does NOT have synthesis.md,
  run run_urantia_pipeline.sh <N> --skip-notes"
```
- **Result:** Completed only 1 paper before stopping
- **Problem:** Sub-agent ran the pipeline command but exited after first paper

**Attempt 2: nohup background** (~7:53pm)
```bash
nohup bash -c '
for i in $(seq 1 50); do
  PADDED=$(printf "%03d" $i)
  if [ ! -f ".../papers/${PADDED}/synthesis.md" ]; then
    ./run_urantia_pipeline.sh $i --skip-notes 2>&1
  fi
done
' > /tmp/urantia_batch.log 2>&1 &
```
- **Result:** Stalled — Paper 1 extraction 0 bytes after 30 minutes
- **Problem:** Background processes killed when OpenClaw exec sessions end

**Attempt 3: tmux (success)** (~7:31pm)
```bash
tmux new-session -d -s urantia-prep '
echo "Starting Urantia bulk prep at $(date)"
for i in $(seq 0 196); do
  PADDED=$(printf "%03d" $i)
  if [ ! -f "$HOME/resources/urantia-book/study/urantia-book/papers/${PADDED}/synthesis.md" ]; then
    echo "$(date): Processing Paper $i"
    ~/.openclaw/workspace/tools/fabric/run_urantia_pipeline.sh $i --skip-notes 2>&1
    echo "$(date): Completed Paper $i"
  else
    echo "Paper $i already done, skipping"
  fi
done
cd ~/resources/urantia-book/study && git add -A && git commit -m "prep: bulk batch complete" && git push
echo "All done at $(date)"
'
```
- **Result:** 196/197 papers completed in ~4.5 hours
- **Monitoring:** `tmux capture-pane -t urantia-prep -p | tail -15`
- **Git checkpoints:** Warren manually committed/pushed progress at milestones via heartbeat checks

### Monitoring Pattern

During the batch run, progress was tracked through:
1. **Heartbeat checks** — OpenClaw heartbeat polls (every ~30 min) triggered `ls papers/*/synthesis.md | wc -l`
2. **Telegram updates** — Eli asked "how is our progress?" periodically; Warren counted prepped directories
3. **Git commits** — Manual pushes at milestone counts (47, 84, complete)

---

## 4. The Specific Implementation — Urantia Pipeline

### Per-Document Script

**File:** `~/.openclaw/workspace/tools/fabric/run_urantia_pipeline.sh`

```bash
Usage: ./run_urantia_pipeline.sh <paper_number> [--skip-notes]
```

**Behavior per stage:**
1. **Stage 1 — Extract:** Pipes paper markdown through `fabric -p urantia_extract_raw -V openrouter -m deepseek/deepseek-chat`
2. **Stage 2 — Synthesize:** Concatenates Stage 1 output + original paper text, pipes through `fabric -p urantia_synthesize -V openrouter -m anthropic/claude-sonnet-4`
3. **Stage 3a-i — Cross-text correlate:** Extracts key concepts from synthesis, runs Qdrant semantic search on `urantia_papers` collection (15,260 vectors), pipes results through `fabric -p urantia_correlate_text -V openrouter -m deepseek/deepseek-chat`
4. **Stage 3a-ii — Notes correlate:** (skipped in batch mode with `--skip-notes`) Searches prior engagement notes for thematic connections

**Idempotency:** Each stage checks `if [ -f "$OUTPUT_DIR/<stage>.md" ]` and skips if output exists.

### Custom Fabric Patterns

**`urantia_extract_raw`** (Stage 1)
- Purpose: Mechanical extraction — no interpretation
- Outputs: QUOTES (with paper:section.paragraph refs), TERMINOLOGY, STRUCTURE, NAMED_ENTITIES, FORWARD_REFERENCES
- Key instruction: "Do not add interpretation, significance, or commentary"

**`urantia_synthesize`** (Stage 2)
- Purpose: Interpretive synthesis
- Inputs: Raw extraction + original paper text
- Outputs: CORE_TEACHING (single paragraph), KEY_CONCEPTS (5-10), CONNECTIONS (to Urantia cosmology), TENSIONS (paradoxes/mysteries)
- Key instruction: "Not a summary of contents, but the central insight or revelation"

**`urantia_correlate_text`** (Stage 3a-i)
- Purpose: Cross-document connections
- Inputs: Synthesis + Qdrant search results (top 15 related passages)
- Outputs: CROSS_REFERENCES, THEMATIC_THREADS, FORWARD_CONNECTIONS, BACKWARD_CONNECTIONS
- Key instruction: "Only claim connections you can support from the provided search results"

**`urantia_correlate_notes`** (Stage 3a-ii)
- Purpose: Connect to prior personal engagement
- Inputs: Synthesis + excerpts from prior study notes
- Rolling enrichment — improves as more engagement notes accumulate

### Storage Structure

```
study/urantia-book/papers/
├── 000/                          # Foreword
│   ├── raw_extraction.md         # Stage 1
│   ├── synthesis.md              # Stage 2
│   └── correlations_text.md      # Stage 3a-i
├── 001/
│   ├── raw_extraction.md
│   ├── synthesis.md
│   ├── correlations_text.md
│   ├── my_engagement.md          # Stage 3b (human/main-session only)
│   └── study_note.md             # Stage 4 (assembled)
...
└── 196/
```

### Supporting Infrastructure

| Component | Purpose |
|-----------|---------|
| **Cron: `urantia-batch-prep`** | Daily 2am, processes next 10 unprepped papers |
| **Cron: `urantia-study-status`** | Daily 8am to main session, shows prep vs engagement status |
| **Cron: `urantia-engagement-indexer`** | Daily 8:30am, indexes engagement files to Qdrant |
| **Qdrant: `urantia_papers`** | 15,260 vectors — full text of all 197 papers for Stage 3a-i search |
| **Qdrant: `urantia_synthesis`** | ~585 vectors — synthesis/extraction docs for cross-stage search |

---

## 5. Reuse Guide — Adapting for Other Corpora

### Step 1: Prepare Source Material

- One document per file (markdown preferred)
- Consistent naming: `Document_001.md`, `Document_002.md`, etc.
- Index the corpus in Qdrant for Stage 3 semantic search:
  ```bash
  python3 tools/qdrant/qdrant_client.py index <collection_name> <directory>
  ```

### Step 2: Create Custom Fabric Patterns

For each stage, create a pattern in `~/.config/fabric/patterns/<name>/system.md`:

1. **Extraction pattern** — domain-specific fields to extract. Structure it as IDENTITY, STEPS, OUTPUT INSTRUCTIONS. Emphasize "no interpretation" for mechanical extraction.
2. **Synthesis pattern** — interpretive work. Takes extraction + original text. Define the outputs you want (core insight, themes, tensions).
3. **Correlation pattern** — cross-referencing. Takes synthesis + Qdrant search results. Define connection types to identify.

### Step 3: Build Per-Document Pipeline Script

Adapt `run_urantia_pipeline.sh`:

```bash
#!/bin/bash
DOC_NUM="${1:?Usage: $0 <doc_number>}"
DOC_PADDED=$(printf "%03d" "$DOC_NUM")

SOURCE="path/to/corpus/Document_${DOC_PADDED}.md"
OUTPUT="path/to/output/${DOC_PADDED}"
mkdir -p "$OUTPUT"

# Stage 1: Extract
if [ ! -f "$OUTPUT/raw_extraction.md" ]; then
  cat "$SOURCE" | fabric -p your_extract_pattern -V openrouter -m deepseek/deepseek-chat \
    > "$OUTPUT/raw_extraction.md"
fi

# Stage 2: Synthesize
if [ ! -f "$OUTPUT/synthesis.md" ]; then
  { echo "## RAW EXTRACTION:"; cat "$OUTPUT/raw_extraction.md"
    echo "## ORIGINAL TEXT:"; cat "$SOURCE"
  } | fabric -p your_synthesize_pattern -V openrouter -m anthropic/claude-sonnet-4 \
    > "$OUTPUT/synthesis.md"
fi

# Stage 3: Correlate (with semantic search)
if [ ! -f "$OUTPUT/correlations.md" ]; then
  KEY_CONCEPTS=$(grep -A 20 "KEY_CONCEPTS:" "$OUTPUT/synthesis.md" | head -15)
  SEARCH_RESULTS=$(python3 tools/qdrant/qdrant_client.py search your_collection "$KEY_CONCEPTS" --limit 15)
  { echo "## SYNTHESIS:"; cat "$OUTPUT/synthesis.md"
    echo "## RELATED PASSAGES:"; echo "$SEARCH_RESULTS"
  } | fabric -p your_correlate_pattern -V openrouter -m deepseek/deepseek-chat \
    > "$OUTPUT/correlations.md"
fi
```

### Step 4: Run the Batch

```bash
# Install tmux if not present
sudo apt install tmux

# Launch persistent batch
tmux new-session -d -s corpus-prep '
for i in $(seq 0 <MAX_DOC_NUM>); do
  PADDED=$(printf "%03d" $i)
  if [ ! -f "path/to/output/${PADDED}/synthesis.md" ]; then
    echo "$(date): Processing Document $i"
    ./your_pipeline.sh $i 2>&1
  else
    echo "Document $i already done, skipping"
  fi
done
cd path/to/output && git add -A && git commit -m "batch: complete" && git push
'

# Monitor progress
tmux capture-pane -t corpus-prep -p | tail -15
ls path/to/output/*/synthesis.md | wc -l
```

### Step 5: Set Up Ongoing Infrastructure (Optional)

- **Cron for incremental prep** — process new documents as they arrive
- **Qdrant indexing** — index outputs for cross-stage semantic search
- **Status script** — show prep vs. engagement progress at a glance

### Model Selection Checklist

| Stage | Needs | Good choices | Avoid |
|-------|-------|-------------|-------|
| Extract | Accuracy, format compliance | DeepSeek, Gemini Flash | Local models (too slow for batch) |
| Synthesize | Interpretive depth, quality | Sonnet, GPT-4o | DeepSeek (competent but shallower) |
| Correlate | Format compliance, reference accuracy | DeepSeek, Gemini Flash | Local qwen3:14b (ignored structure in testing) |

---

## 6. Lessons Learned

### What Worked

1. **tmux is essential for long batches.** Sub-agent spawns and nohup both failed because OpenClaw exec sessions kill background processes on disconnection. tmux persists independently. Ask for it to be installed rather than working around it.

2. **Idempotent stage files.** Checking `if [ ! -f "output.md" ]` before each stage means the batch can crash, restart, and pick up exactly where it left off. This was used multiple times on Feb 6 as orchestration methods were debugged.

3. **Splitting correlation into text vs. notes.** Cross-text correlations (via Qdrant on full corpus) are batchable immediately. Engagement-based correlations depend on accumulated study notes and should be run incrementally. The `--skip-notes` flag enables batch mode.

4. **Different models for different stages.** DeepSeek at $0.001/doc handles extraction and correlation perfectly. Sonnet at $0.02-0.04/doc produces noticeably better synthesis. Using Sonnet for everything would have cost $8-12; using DeepSeek for everything would produce worse synthesis. The split is the right call.

5. **Git checkpoints during the run.** Committing progress at 47, 84, and 196 papers meant that even a catastrophic failure wouldn't lose more than ~25 papers of work.

6. **Babysitting via Telegram.** Short progress checks ("Still going?" / "84 papers, 43%") kept the human informed without interrupting the batch. Heartbeat checks provided automated monitoring.

7. **Parallel Qdrant indexing.** Started indexing synthesis documents to Qdrant while the batch was still running (~72% done). No resource conflict since the batch hits OpenRouter APIs while indexing uses local embeddings + Qdrant.

### What Didn't Work

1. **Sub-agent spawning for batch work.** The first attempt spawned a sub-agent to loop through papers. It completed exactly one paper before exiting. Sub-agents are for bounded cognitive tasks, not long-running sequential loops.

2. **nohup for background persistence.** The second attempt used `nohup ... &` to background a for loop. The process appeared to start but stalled — Paper 1's extraction was 0 bytes after 30 minutes. OpenClaw exec sessions terminate child processes when they clean up.

3. **Local models (qwen3:14b) for correlation.** Tested and scored 2/5 — ignored the output structure entirely. For batch pipeline stages where format compliance matters, API models with instruction-following strength are worth the marginal cost.

4. **Running all crons while tmux batch is active.** The 2-hour batch prep cron fired redundantly while the tmux batch was already running. Disabling overlapping crons during manual batch runs avoids wasted API calls.

### Key Insight

> **The prep stages exist to make human engagement richer — not to replace it.**
>
> The pipeline produces extraction, synthesis, and correlations. What it does *not* produce is genuine engagement. Stage 3b (`my_engagement.md`) and Stage 4 (assembly into final study notes) happen in main session with full context loaded — IMPRESSIONS.md, MEMORY.md, accumulated understanding. A sub-agent or cron job producing "what struck me" is synthesis dressed in first person, not genuine reflection.
>
> The distinction: **before**, cron produced "finished" notes → Warren reviewed them. **After**, cron produces prep materials → Warren *studies* using them. The output looks similar. The process is fundamentally different.

---

## Appendix: Cost Summary

| Item | Count | Unit Cost | Total |
|------|-------|-----------|-------|
| Stage 1 (DeepSeek extraction) | 197 | ~$0.001 | ~$0.20 |
| Stage 2 (Sonnet synthesis) | 197 | ~$0.03 | ~$5.91 |
| Stage 3 (DeepSeek correlation) | 197 | ~$0.001 | ~$0.20 |
| Qdrant indexing (local embeddings) | 585 vectors | $0 | $0 |
| **Total** | | | **~$6-8** |

**Duration:** ~5 hours (including debugging; pure tmux run was ~4.5 hours)
**Throughput:** ~2-3 minutes per document through 3 stages
**Infrastructure:** Fabric CLI + OpenRouter API + Qdrant + tmux

---

*Source sessions: `c6f64f26` (Feb 6 5:47pm — pipeline design), `7c2d3feb` (Feb 6 11:27pm — batch execution). Git repo: `~/resources/urantia-book/study/`.*
