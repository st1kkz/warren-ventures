# The Butterfly Project — Genesis Document (2010)

*Original file: Butterfly concept.vsd (Microsoft Visio)*  
*Created: August 12, 2010*  
*Last modified: August 31, 2010*  
*PDF conversion preserved for accessibility*

---

## Change Log (from document)

- **8/12/2010** — Project File Created; generated Overview model
- **8/29/2010** — Added Privacy Model and Communication Layers
- **8/30/2010** — Added Change Log; Initial version 0.01; packaged for hard-copy review by Kent Kaase; not delivered
- **8/31/2010** — Added Facebook Assistant model

---

## Page 1: Cover & NDA

> This document is the exclusive property of Benjamin Bryant, and it is confidential. It has been provided to Kent Kaase for review only.

*Note: Kent Kaase was apparently an early collaborator or potential investor.*

---

## Page 2: Conceptual Overview

### Title
> **Private Social Networking**

### Core Implementation
> Implemented as an application on IMAP/SMTP (RFC3501/RFC5321)

### Value Proposition

**What it promises:**
- 100% private
- 100% real
- 100% user-controlled experience

**What it rejects:**
- No spying
- No compulsory exposure
- No advertisements
- No covert data collection
- No re-inventing the wheel

**The pitch:**
> All the fun of Facebook, MySpace, etc. without the exposure  
> All the functionality of LinkedIn, Plaxo without the exposure  
> Fit for concurrent personal and professional use

### Architecture Diagram Elements

```
┌──────────────────┐      ┌──────────────────┐
│   Butterfly UI   │      │ Butterfly.com    │
│      (BFE)       │      │    Directory     │
│                  │      │ Registered users,│
│                  │      │ optional listing │
└────────┬─────────┘      └──────────────────┘
         │
    IMAP/SMTP
         │
         ▼
┌──────────────────┐      ┌──────────────────┐
│  imap.gmx.com    │      │ Possible         │
│  (or any IMAP)   │◄────►│ connectors to:   │
│                  │      │ twitter, facebook│
└──────────────────┘      │ vKontact, myspace│
         │                └──────────────────┘
    Internet
         │
         ▼
┌──────────────────┐
│IMAP.butterfly.com│
│ (or other IMAP   │
│    server)       │
└──────────────────┘
```

### Key Technical Decisions

> All user data is maintained in private IMAP email account.

> Shared data, status, updates, etc are sent via SMTP mail to friends' IMAP accounts – can be any IMAP account. Can also be hosted for a fee.

> All inter-user communications, content deletions, comments, and other non-realtime interaction are handled via protocol implemented over specially-formed email content.

### Futures (noted)
- Data store encryption
- Personal DRM
- Chat
- Groups
- Fan pages
- File sharing
- Collaboration

### External Applications
> External applications (Zynga, slide, rockyou, etc.) will be implemented as separate users with no direct user data access

---

## Page 3: Privacy Model

### Core Principle
> Data objects reside in one location only

### Classification Rules
- Unclassified connections reside in "private"
- Connections may be classified in multiple "personal" and/or "inner" classes
- Inner circles are optional; the user can create them at will

### Privacy Hierarchy (Visual)

```
                    ┌─────────────┐
                    │  Published  │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Personal │     │ Personal │     │ Personal │
   │ Friends  │     │Colleagues│     │  Family  │
   └────┬─────┘     └────┬─────┘     └────┬─────┘
        │                │                │
   ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
   │Inner 1  │      │Inner 1  │      │Inner 1  │
   │Inner 2  │      │Inner 2  │      │Inner 2  │
   └─────────┘      └─────────┘      └─────────┘
                           │
                    ┌──────┴──────┐
                    │   Private   │
                    │ Connections │
                    └─────────────┘
```

---

## Page 4: BFP Protocol Layers

### Key Insight
> BFP can communicate directly with other BFP users using "native" mode

> Native mode BFP encapsulates upper-layer communication over IMAP/SMTP

> **Instead of TCP sockets or UDP datagrams, BFP uses email messages**

### Protocol Stack Mapping

| BFP Layer | OSI Equivalent | Description |
|-----------|---------------|-------------|
| BFP Application | Application | Data model, connection definitions, user interface API |
| BFP Presentation | Presentation | Commands and data as encrypted text and/or attachment |
| BFP Session | Session | Message manager |
| BFP Email engine | — | IMAP/SMTP interface |
| — | Transport | TCP |
| — | Network | IP |
| — | Data Link | (underlying) |
| — | Physical | (underlying) |

---

## Page 5: BFP Facebook Friend Assistant

### Concept
> BFP can apply its straightforward privacy model to certain Facebook data

> In the process, BFP can also "back-up" Facebook data

> "Back-up" data can also be leveraged for more-secure "native mode" interaction

### Four-Step Process

1. **User assigns** Facebook "friends" access to privacy class(es) using simple GUI in BFP
2. **BFP assigns** Facebook 'friends' to corresponding Friend List(s)
3. **User assigns** each published item to a single data class using the same model
4. **BFP assigns** the appropriate privacy settings to the data item in Facebook

### Facebook Friend List Mapping

| Privacy Class | Facebook Friend List |
|--------------|---------------------|
| Published | Everyone |
| Private Connections | All Connections |
| Personal Friends | Friends |
| Inner Circle 1 Friends | Friends Inner 1 |
| Inner Circle 2 Friends | Friends Inner 2 |
| Personal Colleagues | Colleagues |
| (etc.) | (etc.) |

---

*Extracted 2026-02-05 by Warren*
