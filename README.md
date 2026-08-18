# Finding Your Squam

Private research site for the five-couple lake-compound search: an interactive map of every
qualifying lake (106) and live listing (131) in the Northeast within ~6.5 hours of NYC, plus
the full written briefing with the complete sweep appendix.

**Live site:** deployed on Vercel (static — `index.html` at the repo root is the whole app).

## Structure
- `index.html` — the entire site, self-contained (map, briefing, data inlined)
- `data/map_data.json` — source of truth: lakes, listings, exclusion ledger
- `build/` — regeneration pipeline:
  - edit `data/map_data.json` (or `build/briefing_content.html`)
  - `cd build && npm install && npm run generate` → rewrites `index.html`
  - `build/merge_data.py` + `build/sweep/*.json` document how the dataset was assembled

## Provenance
Compiled July–August 2026 from state lake-monitoring data (NHDES VLAP, Lakes of Maine/LEA/30MRWA,
NY DEC CSLAP, VT DEC), boating regulations, and live listing feeds. Listing statuses move fast —
re-confirm with brokers before acting. Research support: Claude.
