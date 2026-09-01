# Source verification queue

Everything in the Midwest sweep (`data/midwest_map_data.json` and
`build/midwest_briefing_content.html`) was compiled through a search tool that
returns synthesized answers. **No source page was opened directly** — the
research environment blocks outbound HTTPS to every host cited here, all 47 of
them, including Wikipedia, the Wisconsin DNR and the lake associations, not just
the listing sites. Both fetch channels were tested and agree.

That means the figures are second-hand: accurate as far as the search index
reported them, but not read off the page. This directory is the queue for
closing that gap with a browser that can actually load them.

## Files
- **`verify-urls.txt`** — 130 URLs, one per line, priority-ordered, nothing else.
  Feed this to the plugin.
- **`verify-sources.csv`** — the same URLs with context:

  | column | meaning |
  |---|---|
  | `priority` | P1 → P4, see below |
  | `url` | the page |
  | `source` | which lake / listing / claim it backs |
  | `what_to_verify` | the specific thing to look for |
  | `as_published_in_the_report` | what the site currently asserts, so you can diff |

## Priorities

- **P1 (25)** — a recommendation fails if this is wrong. The 17 listings whose
  price or frontage I could not establish (they show "confirm w/ broker" on the
  map), the headline listings the Tier 1 picks rest on, and the three
  load-bearing non-listing claims: the Vilas County guest-house rule, NR 115,
  and the Oneida County resort-decline figure.
- **P2 (38)** — active listings to re-confirm, plus the regulatory and market
  citations in the briefing prose.
- **P3 (66)** — per-lake water quality, acreage and depth. Grindstone's 23-ft
  Secchi record is the one to check first: the whole "truest Squam analog"
  claim rests on it.
- **P4 (1)** — the single drive-time calibration point. Every other drive
  estimate on the map is interpolated from it, so a few direct route lookups
  would be worth more than re-checking this one.

## Two known weak spots

The Vilas County zoning PDF is a 2003 copy; the current ordinance governs, and
the guest-house rule is the hinge of the entire strategy. And the resort-decline
statistic comes from a 1973 academic paper — the direction of travel is well
attested since, but that specific number is fifty years old.

## Regenerating

`research/` is produced from the dataset and briefing, so it stays in sync:
re-run the generator in the commit that created it after editing either.
