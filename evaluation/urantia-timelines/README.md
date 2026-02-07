# Urantia Timeline Pipeline Extension

*Created: 2026-02-07*
*Status: Ready for review (Monday)*

## Summary

Extends the existing Urantia study pipeline with timeline extraction and synthesis capabilities.

## The Flow

```
synthesis.md (5-7KB, exists from Stage 2)
    ↓
fabric -p urantia_extract_timeline
    ↓
timeline.md (per paper)
    ↓
fabric -p urantia_synthesize_timeline (thematic grouping)
    ↓
thematic timeline files (e.g., urantia-geological.md)
```

**Key decision:** Extract from synthesis.md, not raw papers (30-40KB is too large for reliable extraction).

## Files Created

| File | Purpose |
|------|---------|
| `~/.config/fabric/patterns/urantia_extract_timeline/system.md` | Extracts temporal data from paper text |
| `~/.config/fabric/patterns/urantia_synthesize_timeline/system.md` | Organizes extracted data into coherent timelines |
| `INTEGRATION.md` | Full integration spec with thematic categories |
| `example_057_timeline_manual.md` | Example output format |

## Thematic Categories (8)

1. Paradise-Havona Creation
2. Superuniverse Organization
3. Nebadon History
4. Andronover-Monmatia Solar Development
5. Urantia Geological
6. Life Evolution
7. Human History
8. Epochal Revelations

## Next Steps

1. [ ] Review patterns and integration doc
2. [ ] Test extraction on a few synthesis.md files
3. [ ] Validate output quality
4. [ ] Add to pipeline orchestration script
5. [ ] Consider batch processing via cron

## Related

- Team architecture: `warren-ventures/team-architecture/TEAM_DESIGN.md`
- Existing pipeline: `tools/fabric/run_urantia_pipeline.sh`
