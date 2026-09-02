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
- **`verify-urls.txt`** — 165 URLs, one per line, priority-ordered, nothing else.
  Feed this to the plugin.
- **`verify-sources.csv`** — the same URLs with context:

  | column | meaning |
  |---|---|
  | `priority` | P1 → P4, see below |
  | `url` | the page |
  | `source` | which lake / listing / claim it backs |
  | `what_to_verify` | the specific thing to look for |
  | `as_published_in_the_report` | what the site currently asserts, so you can diff |
  | `checked_2026_09_01` | finding from the 1 Sep re-query, where one was done |

## Priorities

- **P1 (31)** — a recommendation fails if this is wrong. The 17 listings whose
  price or frontage I could not establish (they show "confirm w/ broker" on the
  map), the headline listings the Tier 1 picks rest on, and the three
  load-bearing non-listing claims: the Vilas County guest-house rule, NR 115,
  and the Oneida County resort-decline figure.
- **P2 (41)** — active listings to re-confirm, plus the regulatory and market
  citations in the briefing prose.
- **P3 (68)** — per-lake water quality, acreage and depth. Grindstone's 23-ft
  Secchi record is the one to check first: the whole "truest Squam analog"
  claim rests on it.
- **P4 (1)** — the single drive-time calibration point. Every other drive
  estimate on the map is interpolated from it, so a few direct route lookups
  would be worth more than re-checking this one.

## Verification pass, 1 September 2026

Seven P1 items were re-queried through the search channel (still not opened
directly). Three of them turned up real errors, now fixed in the site:

1. **Moose Jaw Resort was on the wrong lake.** It sits at W770 Wind Song Ln,
   Park Falls, in *Price* County, on Round Lake of the **Pike Chain** — 726
   acres, 24 ft deep, root-beer coloured, moderately high phosphorus. The
   report had placed it on the 3,294-acre Round Lake near Hayward and made it
   a Tier 1 anchor and the number-two headline. It is now a program-not-water
   buy, alongside Halfway Lake and Herendeene.
2. **The resort-decline figure covered 1961–1968, not "since 1961."** Oneida
   County lost 23.4% of resort-type establishments in those seven years
   against 13.9% statewide, ~98% of them seasonal cottage places. Restated,
   and a modern data point added: Wisconsin's vacation-home share of mortgage
   originations halved between 2021 and 2025.
3. **12391 W Moreland Rd is pending.** With Moose Jaw removed, Round Lake
   (Sawyer) has no live inventory; its verdict moved from "buy" to "patient."

Four checked out, with detail added: Donner's Bay (MLS 210365, 74 years in one
family, sources still differ on 6 vs 7 cabins and $1.57M vs $1.595M), Pine
Valley Lodge (MLS 217391), Lac du Lune (MLS 218079, and the lake is 442 ac with
~20 ft clarity, better than credited), and Grindstone's 23-ft Secchi record —
though the DNR fishery plan gives 19 ft with an 11–33 ft range, now stated too.

The `checked_2026_09_01` column in the CSV carries the finding for each.
Everything without a value in that column is still unverified.

**Three errors in seven checks.** Assume a similar rate across the remaining
queue, and do not act on any single listing in this report without the broker.

## Rental layer (added 1 Sep)

The 24 rental URLs are queued as P2. Airbnb and VRBO were as blocked as everything
else, so bedroom counts, docks and rates came through search results; each entry says
which of those it could not settle. The user's stated preference is an off-platform
booking at a reduced rate — where a direct site exists it is listed alongside the platform
page, and the ask on every platform listing is the owner's direct rate.

## Two known weak spots

The Vilas County zoning PDF is a 2003 copy. The county's live page now shows a
General Zoning Ordinance updated 15 December 2025 — get that one. The 2003 text
does confirm the shape of the rule (a non-rental guesthouse is not a principal
structure, one allowed per unsewered lake lot), but the guest-house rule is the
hinge of the entire strategy, so read the current version. Zoning & Planning:
zoning@vilascountywi.gov, (715) 479-3620. And the resort-decline
statistic comes from a 1973 academic paper — the direction of travel is well
attested since, but that specific number is fifty years old.

## Regenerating

`research/` is produced from the dataset and briefing, so it stays in sync:
re-run the generator in the commit that created it after editing either.
