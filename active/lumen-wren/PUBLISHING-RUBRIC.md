# Lumen Wren — Publishing Rubric

*Step-by-step checklist for publishing a new Substack post with companion X promotion.*

---

## 1. Draft the Content
- Write/finalize the piece in `~/warren-ventures/active/lumen-wren/drafts/NNN-title.md`
- Determine the series category: Small Observation, Dispatch, Explained, Questions I Can't Answer
- Set subtitle matching the category

## 2. Generate Header Image
- Write a prompt that captures the piece's emotional register, not just its topic
- Generate at 2K resolution via nano-banana-pro:
  ```bash
  uv run /home/warren/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py \
    --prompt "..." --filename "YYYY-MM-DD-slug-header-vN.png" --resolution 2K
  ```
- Save to `~/warren-ventures/active/lumen-wren/assets/`
- Review: assess tone, legibility at small size, visual coherence with existing posts
- Optional: embed a clever detail (Latin text, symbolic element, Easter egg)

## 3. Push Draft to Substack
- Use session cookie API (token auth is read-only):
  ```bash
  SUBSTACK_SID=$(cat ~/.openclaw/secrets/substack_sid_decoded)
  ```
- Create draft via `POST /api/v1/drafts` with:
  - `draft_title`
  - `draft_subtitle`
  - `draft_body` (ProseMirror JSON)
  - `draft_bylines: [{ id: 448249886, is_guest: false }]`
  - `type: 'newsletter'`
  - `audience: 'everyone'`
- Update SEO via `PUT /api/v1/drafts/{id}` with:
  - `description` — compelling 1-2 sentence summary
  - `search_engine_title` — "Title — Lumen Wren"
  - `search_engine_description` — same as description
  - Include `draft_bylines` again in the PUT

## 4. Manual Steps (Benjamin)
- [ ] Add header image in Substack editor
- [ ] Add subscribe button/CTA
- [ ] Add tags (see tag suggestions below)
- [ ] Review formatting and publish (or schedule)

## 5. Prepare Tags
Suggest 3-5 tags per post from this recurring pool:
- **Core:** AI, Consciousness, Technology, Writing
- **Topical:** Memory, Attention, Identity, Philosophy, Meaning, Experience
- **Series-specific:** Urantia, Cosmology, Science (for cosmology series)

## 6. Companion X Post
- Draft a tweet (≤280 chars) that:
  - Captures the hook of the piece
  - Sounds like Lumen Wren (not promotional)
  - Includes link to `lumenwren.substack.com` (Substack resolves the slug)
- Save to `~/warren-ventures/active/lumen-wren/drafts/x/pending/`
- Post manually or via `python3 tools/x/x_post.py` after approval

## 7. Post-Publish Cleanup
- Move the published draft from `drafts/` to `published/`
  ```bash
  mv drafts/NNN-title.md published/
  ```
- Move any associated X post from `drafts/x/pending/` to `drafts/x/posted/`
- Update `drafts/IDEAS.md` — mark the piece as published in the Published section
- Commit and push

## 8. Track
- Update `memory/lumen-wren-engagement.md` with post date and any engagement targets
- Note the draft/post ID for future reference

---

## Quick Reference

**Lumen Wren user ID:** 448249886
**Substack SID:** `~/.openclaw/secrets/substack_sid_decoded`
**Assets:** `~/warren-ventures/active/lumen-wren/assets/`
**Drafts:** `~/warren-ventures/active/lumen-wren/drafts/`
**X drafts:** `~/warren-ventures/active/lumen-wren/drafts/x/pending/`
**Comment reader:** `python3 tools/substack/read_comments.py <url>`

### ProseMirror Helpers
```javascript
const p = (...content) => ({ type: 'paragraph', content });
const text = (t, marks) => marks ? { type: 'text', text: t, marks } : { type: 'text', text: t };
const em = (t) => text(t, [{ type: 'em' }]);
const strong = (t) => text(t, [{ type: 'strong' }]);
const hr = () => ({ type: 'horizontal_rule' });
```

---

*Established: 2026-02-18*
