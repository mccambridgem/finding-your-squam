# Finding Your Squam

Private research site for the five-couple lake-compound search. Two regional sweeps, one app:

- **Northeast** — every qualifying lake (106) and live listing (131) within ~6.5 hours of NYC,
  plus the full written briefing and sweep appendix.
- **Midwest** — every qualifying lake (88) and live listing (61) in Wisconsin and Michigan
  between 4 and 8 hours of Chicago, with its own briefing. Trout Lake, the second archetype
  from the original brief, is the reference point here the way Squam is in the Northeast.

Each region has a Map tab and a Full-briefing tab; the region switcher is the top row of tabs.
Deep links work: `#ne/map`, `#ne/brief`, `#mw/map`, `#mw/brief`.

Both maps also carry a **rental layer** (green triangles, hideable with the "Rentals · 8 couples"
chip): summer rentals that can host eight couples — 7+ bedrooms or a whole-resort buyout,
waterfront with a dock — on the Tier 1 lakes only (plus Torch Lake by request). Each entry
carries the platform listing and, where one exists, the off-platform booking route. Each
briefing has a matching "Renting for eight couples" section.

**Live site:** deployed on Vercel (static — `index.html` at the repo root is the whole app).

## Structure
- `index.html` — the entire site, self-contained (both maps, both briefings, data inlined)
- `data/map_data.json` — Northeast source of truth: lakes, listings, rentals, exclusion ledger
- `data/midwest_map_data.json` — Wisconsin/Michigan source of truth, same schema (rentals are
  authored in `build/midwest_data.py`; the Northeast rentals live directly in the JSON)
- `build/` — regeneration pipeline:
  - edit a `data/*.json` file (or `build/briefing_content.html` / `build/midwest_briefing_content.html`)
  - `cd build && npm install && npm run generate` → rewrites `index.html`
  - `build/merge_data.py` + `build/sweep/*.json` document how the Northeast dataset was assembled
  - `build/midwest_data.py` is the Wisconsin/Michigan dataset in source form — edit it and
    `python3 midwest_data.py` to regenerate `data/midwest_map_data.json`
- `build/build_site.js` is region-parameterized: add a region config to the `REGIONS` array
  (dataset, briefing file, basemap window, origin city, drive rings, map labels) and it renders
  its own tab, map and briefing with no other changes.

## Provenance
Northeast: compiled July–August 2026 from state lake-monitoring data (NHDES VLAP, Lakes of Maine/LEA/
30MRWA, NY DEC CSLAP, VT DEC), boating regulations, and live listing feeds.

Midwest: compiled September 2026 from Wisconsin DNR lake data and the Citizen Lake Monitoring
Network, Michigan's MiCorps Cooperative Lakes Monitoring Program, Tip of the Mitt Watershed Council,
the Leelanau Conservancy Secchi record, individual lake associations, county shoreland ordinances
(NR 115 and its county implementations; Michigan's Part 301), and live listing feeds.

Listing statuses move fast — re-confirm with brokers before acting. Research support: Claude.
