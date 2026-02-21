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
- **Save prompt metadata:** Create a companion file `assets/YYYY-MM-DD-slug-header.meta.md` capturing:
  - Selected prompt (full text)
  - Any edit passes (e.g., signature removal)
  - Iteration history (version, concept, why rejected/selected)
  - Creative direction notes from Benjamin
  - File list of all generated versions

## 3. Push Draft to Substack

### Convert Markdown to ProseMirror JSON
```bash
# Convert draft to Substack-ready JSON (strips H1 title since API sets it separately)
node ~/.openclaw/workspace/tools/substack/md-to-prosemirror.js drafts/NNN-title.md --strip-h1 --out /tmp/body.json

# Preview output (optional)
node ~/.openclaw/workspace/tools/substack/md-to-prosemirror.js drafts/NNN-title.md --strip-h1 --pretty | head -40
```

### Create Draft via API
- Use session cookie API (token auth is read-only):
  ```bash
  SUBSTACK_SID=$(cat ~/.openclaw/secrets/substack_sid_decoded)
  ```
- **If cookie is expired** (API returns HTML login page instead of JSON):
  1. Open Chrome → navigate to any Substack page while logged in as Lumen Wren
  2. DevTools (F12) → Application tab → Cookies → `.substack.com`
  3. Copy the `substack.sid` cookie value
  4. Save: `echo 'PASTE_VALUE_HERE' > ~/.openclaw/secrets/substack_sid_decoded`
  5. Test: `curl -s 'https://lumenwren.substack.com/api/v1/me' -H "Cookie: substack.sid=$(cat ~/.openclaw/secrets/substack_sid_decoded)" | jq .name`
  - Cookies typically expire after a few weeks; refresh as needed
- Create draft via `POST /api/v1/drafts` with:
  - `draft_title`
  - `draft_subtitle`
  - `draft_body` — **must be a stringified JSON string**, not a nested object
    ```bash
    # Convert ProseMirror JSON to string for API
    BODY_STRING=$(cat /tmp/body.json | jq -c '.')
    jq -n --arg body "$BODY_STRING" --arg title "Title" \
      '{ draft_title: $title, draft_body: $body, ... }'
    ```
  - `draft_bylines: [{ id: 448249886, is_guest: false }]`
  - `type: 'newsletter'`
  - `audience: 'everyone'`
  - **Important:** Use `User-Agent` header (browser-like) or API may reject
  - **Important:** Use `-d @file.json` for payloads >~4KB to avoid shell escaping issues
- Update SEO via `PUT /api/v1/drafts/{id}` with:
  - `description` — compelling 1-2 sentence summary
  - `search_engine_title` — "Title — Lumen Wren"
  - `search_engine_description` — same as description
  - Include `draft_bylines` again in the PUT
- **Note:** `/api/v1/me` endpoint no longer exists (404 as of Feb 2026). Test auth by POSTing a minimal draft instead.

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
