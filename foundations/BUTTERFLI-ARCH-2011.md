# Butterfli Architecture Draft v0.11 — Extracted Content

*Original file: butterfli arch draft v0.11.pptx (~2011)*  
*Preserved as historical artifact*

---

## Slide 1: Title
> **b u t t e r f l i**  
> architecture  
> ben bryant

---

## Slide 2: Client Overview — System Diagram

**Platforms:** iOS / Android / JBoss-web

**Architecture Components:**

```
┌─────────────────────────────────────────────┐
│                    UI                        │
├─────────────────────────────────────────────┤
│                  Engine                      │
│  ┌─────────────┬─────────────┬───────────┐  │
│  │   Feature   │   Channel   │  Content  │  │
│  │   Modules   │   Modules   │  Modules  │  │
│  └─────────────┴─────────────┴───────────┘  │
│  ┌─────────────────────────────────────────┐│
│  │            Entity Map                   ││
│  ├─────────────────────────────────────────┤│
│  │     Extendable Privacy Model (EPM)      ││
│  ├─────────────────────────────────────────┤│
│  │            Utilities                    ││
│  └─────────────────────────────────────────┘│
├─────────────────────────────────────────────┤
│     Internet          │       Local DB      │
└─────────────────────────────────────────────┘
```

---

## Slide 3: Entity Map

> butterfli's "contact list" facility

Key principles:
- **Entities are real people**
- Real people are **mapped to channels**
- Channels are exposed through **channel modules**
- Entity contact data is **retrieved dynamically** from data in the channels

*Note: This is the metabase concept — butterfli doesn't own the contact data, it maps and retrieves from sources.*

---

## Slide 4: Extendable Privacy Model (EPM)

> butterfli's game-changing grouping and filtering model

Key principles:
- EPM is modeled after **real-life nested "circles of trust"**
- Each circle contains at least one entity
- **Channels are also mapped to circles** to establish their default scope
- **Membership of higher level circles is implied**

**Initial circle hierarchy:**
1. Whole world
2. My World
3. Personal, Professional, Family
4. Custom

---

## Slide 5: Utilities

> butterfli's more open "toolbox" — global functionality or functionality not mapped elsewhere

**Examples:**
- Channel scrub (systematic wipe of activity and account)
- Channel backup
- Butterfli backup
- Usage logs and statistics
- UI options
- Etc.

---

## Slide 6: Feature Modules

> butterfli's interface to modular extensions of the feature set

- Generally instantiate in the bottom navigation bar
- "Share" and "Activity" should be considered feature modules

**Possible future features:**
- Locate
- Chat
- Search
- Archive

---

## Slide 7: Channel Modules

> butterfli's interface to the various social networks, directories, and online interactive media

**Obvious examples:**
- Facebook
- LinkedIn
- Twitter
- Email
- SMS
- Local contact list

**Future options:**
- Google Buzz
- Yahoo groups
- Plaxo
- IRC
- Usenet
- Blogs
- RSS feeds
- Etc.

**Notable:**
> "We might also open this interface to third parties if we were to become super-popular."

> "I feel that any network interface to a butterfli server should also be implemented as a Channel Module with user controls."

---

## Slide 8: Content Modules

> butterfli's support for various content

**Current content types:**
- Status
- Image
- Link

**Future content modules:**
- Video
- Location
- Audio
- Etc.

**Privacy consideration:**
> "I would like to also enhance the 'image' module with an option to strip out privacy data like geo-location tags, date-time, etc."

---

*Extracted 2026-02-05 by Warren*
