# Analysis: Butterfli Architecture Draft v0.11 (~2011)

*Warren's observations on the technical architecture*

---

## The Core Insight: Three-Module Separation

The architecture cleanly separates three concerns:

| Module Type | What It Handles | Examples |
|-------------|-----------------|----------|
| **Feature** | What you can *do* | Share, Activity, Search, Archive |
| **Channel** | How you *connect* | Facebook, Email, SMS, RSS |
| **Content** | What you *share* | Status, Image, Video, Location |

This is orthogonal design. Any feature can work with any channel carrying any content. The combinations are multiplicative, not additive:

- Share (feature) + Facebook (channel) + Image (content)
- Share (feature) + Email (channel) + Image (content)
- Activity (feature) + Twitter (channel) + Status (content)
- Archive (feature) + All channels + All content

Adding a new channel doesn't require touching features or content. Adding new content doesn't require touching channels or features. This is how software *should* be designed but rarely is.

---

## Entity Map: People, Not Accounts

> "Entities are real people."

This single sentence encodes a philosophy. You don't have "Facebook friends" and "LinkedIn connections" and "email contacts." You have *people* — and those people happen to be reachable through various channels.

The Entity Map is the join table between human relationships and digital touchpoints. It's the answer to "how do I reach Sarah?" rather than "what's Sarah's Facebook?"

This is exactly what's still missing in 2026. I have no unified view of "people I know." I have fragmented accounts across platforms. Butterfli's Entity Map would solve this.

---

## EPM: Channels Have Default Scope

A detail I missed in the UI deck:

> "Channels are also mapped to circles to establish their default scope."

This means: LinkedIn defaults to Professional. Facebook defaults to Personal. SMS might default to Family.

When you share something with "Professional" contacts, the system knows to prefer LinkedIn over SMS by default — but you can override. The privacy model shapes channel selection, not just contact selection.

This is sophisticated information architecture. The system has *opinions* about appropriate contexts, but the user remains in control.

---

## Privacy Stripping: Defense in Depth

From slide 8:

> "I would like to also enhance the 'image' module with an option to strip out privacy data like geo-location tags, date-time, etc."

In 2011, this was prescient. EXIF data leaking location and timestamps was barely on anyone's radar. Benjamin was already thinking about defense in depth — not just *who* you share with, but what metadata leaks through the share.

---

## The Butterfli Server Note

From slide 7:

> "I feel that any network interface to a butterfli server should also be implemented as a Channel Module with user controls."

This is crucial. If butterfli itself had a backend (for sync, for social features, for whatever), that backend would be *just another channel* — subject to the same user controls as Facebook or Twitter.

No special privileges for the system provider. The architecture doesn't have a privileged position for the company that built it. This is how you design for user sovereignty: treat yourself as untrusted.

---

## Platform Targets

> iOS / Android / JBoss-web

The ambition was cross-platform from the start. Not "iPhone app" but "personal social layer that works everywhere." JBoss-web suggests server-side rendering for desktop access — reasonable for 2011.

---

## What Maps to COS

| Butterfli Component | COS Equivalent |
|--------------------|----------------|
| Engine | Context Manager |
| Feature Modules | Agent capabilities |
| Channel Modules | Resource Brokers |
| Content Modules | (Could map to content types Warren handles) |
| Entity Map | Unified contact/entity layer (future) |
| EPM | Trust topology / access control |
| Utilities | System tools, maintenance |
| Local DB | Persistence Layer |

The butterfli Engine is functionally equivalent to what we're calling the Context Manager — the kernel that coordinates everything else.

---

## The Gap That AI Fills

This architecture is clean, modular, well-designed. But it still requires the *user* to:
- Classify their contacts
- Choose sharing audiences
- Select appropriate channels
- Manage module configurations
- Maintain the privacy model

That's a lot of ongoing work. Most people wouldn't do it consistently.

An AI agent changes everything:
- Learn relationships from behavior, suggest classifications
- Infer appropriate audiences from content
- Select channels automatically based on learned preferences
- Handle configuration as a background task
- Maintain the privacy model proactively

The architecture was waiting for an operator. Now it has one.

---

## Closing Thought

This architecture doc is tighter and more technical than the UI deck. It shows Benjamin thinking like a systems architect, not just a product designer. The separation of concerns, the plugin boundaries, the privacy-first defaults — this is serious engineering thinking.

Fifteen years later, the module interfaces would look different (REST APIs, GraphQL, WebSockets), but the *conceptual architecture* holds up completely. That's the mark of good design: the abstractions outlive the implementations.

---

*Analysis by Warren — 2026-02-05*
