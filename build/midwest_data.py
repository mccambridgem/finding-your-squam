#!/usr/bin/env python3
"""
Builds ../data/midwest_map_data.json — the Wisconsin/Michigan sweep.

Same schema as data/map_data.json (the Northeast sweep) so build_site.js can
render both regions from one code path:

    refs      reference points (Chicago = origin of every drive estimate,
              Trout Lake = the archetype)
    lakes     every lake that passed the archetype bar, tiered t1/t2/watch
    listings  live opportunities, geo-located to their host lake
    excluded  the honest ledger: evaluated and rejected, with reasons

Run:  python3 midwest_data.py
"""
import json, os

UPDATED = "September 2, 2026"

# ---------------------------------------------------------------- reference
REFS = [
    dict(key="chicago", cls="ref", shape="star", name="Chicago", state="IL",
         lat=41.882, lon=-87.628, drive="", acres=None,
         blurb="Start of every drive estimate (the Loop). The 4-hour ring is the near edge of the brief: everything inside it is weekend-cottage country, not the archetype.",
         links=[]),
    dict(key="trout", cls="ref", shape="ring", name="Trout Lake (the archetype)", state="WI",
         lat=46.030, lon=-89.665, drive="~5:50", acres=3816,
         blurb="The reference point, and the one lake here you already know. 3,816 acres, 117 ft deep, gin-clear, wrapped almost entirely by the 236,000-acre Northern Highland–American Legion State Forest. Almost no private frontage exists — and none was for sale this month.",
         links=[["Northern Highland–American Legion State Forest", "https://vilaswi.com/your-guide-to-the-northern-highland-american-legion-state-forest/"],
                ["Trout Lake waterfront (Gold Bar)", "https://www.goldbarrealty.com/lakes/troutlake"]]),
]

# ---------------------------------------------------------------- lakes
# (key, name, state, lat, lon, acres, drive, tier, score, clarity, motors, blurb, links, new)
L = []
def lake(key, name, state, lat, lon, acres, drive, tier, score, clarity, motors, blurb, links=None, new=False):
    L.append(dict(key=key, name=name, state=state, lat=lat, lon=lon, acres=acres, drive=drive,
                  tier=tier, score=score, clarity=clarity, motors=motors, blurb=blurb,
                  links=links or [], cls=tier, new=new))

# ---- Wisconsin · Vilas County (Northern Highland) --------------------------
lake("black_oak", "Black Oak Lake", "WI", 46.128, -89.297, 564, "~6:00", "t2", 9.5,
     "Widely cited as Wisconsin's clearest — Secchi routinely 25–30 ft. 85 ft max, 34 ft mean.",
     "Full-motor lake, no horsepower cap. Skiing legal and practiced; small landing keeps traffic low.",
     "The clearest water in the state and the closest thing here to Squam's gin-clarity. Sub-bar at 564 acres — a real constraint for five boats — but the water quality is unmatched and the culture is old Land O'Lakes camps. Inventory is famously thin; one 3BR is live at $699K.",
     [["Black Oak Lake listings", "https://www.lakehomes.com/wisconsin/black-oak-lake-land-olakes"],
      ["Why it's the cleanest", "https://www.islands.com/1999520/black-oak-lake-wisconsin-cleanest-lake-crystal-clear-scenic-day-trip-getaway/"]]),

lake("presque_isle_lake", "Presque Isle Lake", "WI", 46.198, -89.720, 1165, "~6:05", "t2", 9.0,
     "Clear, deep (103 ft), spring-fed; among the better Vilas readings.",
     "Full motor; the town's ethos is quiet, and the lake sits at the end of the road.",
     "1,165 acres and 103 feet deep at the top-left corner of Vilas County, half an hour past where day-trippers turn around. State and county forest on much of the shore, an understated summer-camp culture, and a market that actually trades — 30 active listings countywide this summer, average ask ~$520K.",
     [["Presque Isle lake property", "https://www.lakeplace.com/forsale/wi/presque-isle/"]]),

lake("big_muskellunge", "Big Muskellunge Lake", "WI", 46.021, -89.617, 897, "~5:50", "t2", 8.5,
     "Clear; part of the NTL-LTER long-term research set (the most-studied water in the Midwest). 70 ft max.",
     "Full motor, no horsepower cap; NHAL landing only.",
     "Trout Lake's smaller neighbor, and nearly its equal on water: deep, clear, forest-ringed. Same problem — state forest owns most of the shore, so listings are events, not inventory. Set alerts and be ready.",
     [["Big Muskellunge Lake", "https://vilaswi.com/lake-river/big-muskellunge-lake/"]]),

lake("plum_lake", "Plum Lake", "WI", 45.955, -89.510, 1057, "~5:45", "t2", 8.5,
     "DNR classifies it very clear; 57 ft max.",
     "Full motor; connected to Big St. Germain via the Plum–Star chain.",
     "Sayner's lake, and one of the oldest continuous summer colonies in the Northwoods — the kind of place where the same six families have held frontage since the 1890s. Clear water, decent size, and a real (if small) market. Plum Lake Public Library and the Sayner store are the entire downtown.",
     [["Plum Lake", "https://www.starlake.org/topic/plum"]]),

lake("star_lake_vilas", "Star Lake", "WI", 45.963, -89.487, 1206, "~5:45", "t2", 8.5,
     "Clear, 68 ft max; long-term monitoring by the Plum–Star association.",
     "Full motor; NHAL forest landing, no marina.",
     "1,206 acres inside the state forest, with the historic Star Lake hamlet (population ~40) at one end and virtually nothing at the other. The quietest big water in Vilas County that still has private frontage on it.",
     [["Plum & Star Lakes association", "https://www.starlake.org/topic/plum"]]),

lake("north_twin", "North Twin Lake", "WI", 46.088, -89.100, 2871, "~5:45", "t2", 8.5,
     "Moderately clear; 60 ft max, 28 ft mean. Class-A musky water.",
     "Full motor, no cap; connected by channel to South Twin (628 ac, very clear).",
     "Phelps' big lake — 2,871 acres with real running room, a channel to a clearer 628-acre second basin, and the most active high-end frontage market in the county (a 61-acre, 1,022-ft assemblage listed at $5.2M this year). Also home to a live 1897 resort at $2.8M.",
     [["North Twin Lake", "https://vilaswi.com/lake-river/north-twin-lake/"]]),

lake("long_lake_phelps", "Long Lake (Phelps)", "WI", 46.048, -89.048, 886, "~5:45", "t2", 8.0,
     "Clear and unusually deep for its size — 88 ft max.",
     "Full motor; quiet, few public amenities.",
     "886 acres and 88 feet deep east of Phelps, hard against the Michigan line and the Nicolet National Forest. Deep-and-clear on a small footprint; the trade is a shorter ski fetch.",
     []),

lake("lac_vieux_desert", "Lac Vieux Desert", "WI/MI", 46.128, -89.130, 4017, "~6:05", "t2", 7.5,
     "Moderately clear; shallow for its size (38 ft max) so it warms and colors by August.",
     "Full motor; straddles the state line — carry both registrations if you keep a boat here.",
     "The headwater of the Wisconsin River, 4,017 acres straddling the border at Land O'Lakes. Plenty of water for five boats and prices well under the Vilas average, but it is not archetype-clear — mark it a size-and-value play, not a water play.",
     []),

lake("big_st_germain", "Big St. Germain Lake", "WI", 45.925, -89.492, 1617, "~5:40", "t2", 7.5,
     "Moderately clear; 42 ft max.",
     "Full motor; busy channel to Little St. Germain.",
     "1,617 acres with a genuine ski culture and the best restaurant density in the region. Honest tradeoff: this is the Northwoods at its most trafficked — pontoon-heavy weekends, a big landing, and a bar-and-grill shoreline. Program-friendly, atmosphere-compromised.",
     []),

lake("big_arbor_vitae", "Big Arbor Vitae Lake", "WI", 45.925, -89.660, 1070, "~5:35", "watch", 6.5,
     "Moderate; 42 ft max, weedier bays.",
     "Full motor; heavy summer traffic from Woodruff/Minocqua.",
     "1,070 acres 10 minutes from Minocqua — which is exactly the problem. Listed for completeness and for the one live 34.5-acre multi-dwelling property on it ($3.25M).",
     []),

lake("high_fishtrap", "High & Fishtrap Lakes", "WI", 46.152, -89.442, 700, "~5:55", "t2", 7.5,
     "Clear; part of the Headwaters chain.",
     "Full motor; connected chain, low traffic.",
     "A quiet connected chain between Land O'Lakes and Boulder Junction, deep in the forest. A live 5BR/3.5BA on High Lake at $1.03M is the sort of beachhead this strategy wants.",
     []),

lake("big_portage", "Big Portage Lake", "WI", 46.052, -89.362, 1000, "~5:55", "watch", 7.0,
     "Moderately clear.",
     "Full motor.",
     "1,000 quiet acres northeast of Boulder Junction with state forest holdings on part of the shore. Modest inventory; a reasonable second-choice if the Trout/Muskellunge cluster stays dry.",
     []),

lake("fence_lake", "Fence Lake (Lac du Flambeau chain)", "WI", 45.978, -89.828, 3555, "~5:40", "watch", 6.5,
     "Moderate; the chain's ten lakes vary widely.",
     "Full motor, big connected chain — the most ski-friendly water in the county.",
     "3,555 acres on the ten-lake Lac du Flambeau chain: unmatched cruising, genuinely mixed water quality, and a shoreline substantially within the Lac du Flambeau Band's reservation, where non-member purchase and leasing rules are their own diligence project. Enter only with counsel who has done it before.",
     []),

lake("lac_du_lune", "Lac du Lune", "WI", 46.140, -89.250, 442, "~6:00", "watch", 7.5,
     "Clear — nearly 20 ft of transparency, 68 ft max.",
     "Full motor; very low traffic.",
     "442 acres, 68 feet deep and nearly 20 feet of clarity near Land O'Lakes — better water than its size suggests. On the list chiefly for one extraordinary listing: 27.1 acres with 1,181 ft of sand frontage at $1.35M, the largest single-owner frontage assemblage found in Vilas County this sweep.",
     []),

lake("dunn_lake", "Dunn Lake", "WI", 46.212, -89.760, 300, "~6:05", "watch", 6.0,
     "Clear, small.",
     "Full motor but too small to ski properly.",
     "Well under the size bar and included for one reason: a 14+ acre parcel with over 1,000 ft of frontage at $347.5K. Cheapest big-frontage canvas in the sweep — pair it with boat storage on Presque Isle Lake, five minutes away.",
     []),

# ---- Wisconsin · Oneida / Iron / Forest -----------------------------------
lake("tomahawk_lake", "Lake Tomahawk", "WI", 45.832, -89.622, 3392, "~5:30", "t2", 9.0,
     "Clear; 84 ft max — one of the deeper big lakes in Oneida County.",
     "Full motor, no cap. Real ski culture; slow-no-wake within 100 ft of shore.",
     "The best size-clarity-drive combination in Wisconsin: 3,392 acres, 84 feet deep, an hour closer than the Vilas cluster, and a market with actual compound-scale product — a legacy estate with main home plus furnished cabins and multiple docks is live at $3.3M. Busier than Trout, quieter than Minocqua.",
     [["Lake Tomahawk", "https://www.lake-link.com/wisconsin-lakes/oneida-county/tomahawk-lake/3444/"]]),

lake("willow_flowage", "Willow Flowage", "WI", 45.748, -89.848, 6306, "~5:25", "t2", 8.0,
     "Moderately clear, tannin-tinted; shallow at 30 ft max.",
     "Full motor; no wake within 100 ft. Very few docks, almost no development.",
     "6,306 acres of state-designated Scenic Waters — the most undeveloped big water within 5½ hours of Chicago, with eagles, no shoreline lighting, and a drawdown regime. Frontage is scarce because the state owns most of it, and the water is bog-tinted rather than clear. Pure atmosphere, compromised on the water bar.",
     [["Willow Flowage Scenic Waters Area", "https://dnr.wisconsin.gov/topic/lands/willowflowage"]]),

lake("squirrel_lake", "Squirrel Lake", "WI", 45.882, -89.752, 1309, "~5:35", "t2", 7.5,
     "Moderately clear; 46 ft max.",
     "Full motor; modest traffic.",
     "1,309 quiet acres between Minocqua and Lac du Flambeau with a low-key camp shoreline and prices below the Minocqua premium. A sensible value fallback.",
     []),

lake("two_sisters", "Two Sisters Lake", "WI", 45.850, -89.552, 719, "~5:30", "watch", 7.0,
     "Clear; county forest on part of the shore.",
     "Full motor.",
     "719 clear acres ringed partly by Oneida County forest. Under the size bar for five boats but a strong second lake if you buy nearby.",
     []),

lake("pelican_lake", "Pelican Lake", "WI", 45.498, -89.200, 3585, "~5:00", "t2", 7.5,
     "Moderate; 40 ft max.",
     "Full motor, no cap; the closest genuinely big ski lake to Chicago in this report.",
     "3,585 acres at five hours flat — the best drive-to-size ratio in Wisconsin. The water is good rather than elite and the shore is more developed than Vilas, but a nine-acre resort with 204 ft of frontage is live here at $724.9K, which is compound math almost nobody else offers.",
     []),

lake("sugar_camp_chain", "Sugar Camp Chain", "WI", 45.882, -89.322, 1200, "~5:35", "watch", 7.0,
     "Mixed across the five lakes.",
     "Full motor; connected chain.",
     "Five connected lakes northeast of Rhinelander with real cruising and a live $1.499M frontage listing. Water quality varies lake to lake — sample before you commit.",
     []),

lake("turtle_flambeau", "Turtle–Flambeau Flowage", "WI", 46.100, -90.150, 12942, "~6:15", "t1", 8.0,
     "Moderately clear, tannin-stained; ~50 ft max.",
     "Full motor; 195 islands and enormous open water. Slow-no-wake near shore only.",
     "Wisconsin's seventh-largest lake and its wildest — 12,942 acres, 195 islands, and a state Scenic Waters designation that keeps virtually the entire shoreline undeveloped. If your five couples want the feeling of being alone on big water, nothing in this report beats it. The water is tea-colored, not gin: an honest, deliberate trade.",
     [["Turtle-Flambeau Flowage", "https://dnr.wisconsin.gov/topic/Lands/TurtleFlambeau/history.html"]]),

lake("pike_lake_chain", "Pike Lake Chain", "WI", 46.112, -90.050, 1400, "~6:15", "watch", 7.0,
     "Moderately clear.",
     "Full motor; five connected lakes.",
     "A quiet five-lake chain outside Mercer with low prices and low traffic. Not archetype water, but the cheapest connected cruising in the sweep.",
     []),

lake("metonga", "Lake Metonga", "WI", 45.572, -88.900, 2157, "~5:15", "t2", 8.0,
     "Clear; 80 ft max — one of the clearest lakes in the Nicolet.",
     "Full motor, no cap.",
     "2,157 acres and 80 feet deep at Crandon, five and a quarter hours out — clear, deep, underpriced, and almost entirely absent from Chicago's mental map of the Northwoods. The sweep's best-kept secret on the Wisconsin side.",
     [], new=True),

lake("franklin_butternut", "Franklin & Butternut Lakes", "WI", 45.955, -88.978, 1200, "~5:35", "t2", 8.0,
     "Franklin is notably clear (spring-fed, 65 ft); Butternut is larger and moderate.",
     "Full motor on Butternut; Franklin is small and quiet.",
     "The Anvil/Franklin corner of the Chequamegon-Nicolet National Forest east of Eagle River: federal forest on nearly all the shoreline, old CCC-era camps, and the best hiking within a mile of the water anywhere in this report.",
     []),

# ---- Wisconsin · Sawyer / Bayfield / Douglas ------------------------------
lake("grindstone", "Grindstone Lake", "WI", 45.978, -91.300, 3176, "~6:20", "t1", 9.5,
     "Elite — volunteer Secchi averaged 23 ft across 1993–2005; the DNR fishery plan gives 19 ft with a 11–33 ft range. Oligotrophic, 60 ft max, 10.5 mi of shoreline. (Acreage is cited as 3,117 by DNR and 3,176 elsewhere.)",
     "Full motor, no cap; low traffic, one landing. Skiing legal and normal.",
     "The truest Squam analog west of Lake Michigan: 3,176 acres, thirteen years of 23-foot Secchi readings, sand beaches, and a shoreline shared between old family camps and the Lac Courte Oreilles Band. Big enough for five boats, quiet enough to hear loons at noon. Live inventory exists — a chalet-plus-guest-cottage pairing is on the market now.",
     [["Grindstone Lake Association", "https://grindstonelake.org/the-lake/"],
      ["WI DNR water quality", "https://apps.dnr.wi.gov/lakes/lakepages/LakeDetail.aspx?wbic=2391200&page=waterquality"]]),

lake("lco", "Lac Courte Oreilles", "WI", 45.900, -91.352, 5039, "~6:20", "t1", 9.0,
     "Very clear per DNR; 90 ft max, 25.4 mi of shoreline.",
     "Full motor, no cap; big enough that traffic disperses.",
     "5,039 acres and 90 feet deep — the largest genuinely clear ski lake in this report that still trades at compound prices. Twenty-five miles of shoreline means real variety: quiet coves, sand beaches, and one legacy estate live at $2.495M with 10.82 acres and 320 ft of level sand. Note the reservation boundary and title questions on parts of the shore; use a Hayward attorney.",
     [["Hayward Lakes — LCO", "https://haywardlakes.com/activities/lakes/"]]),

lake("round_lake_sawyer", "Round Lake", "WI", 45.982, -91.098, 3294, "~6:25", "t1", 9.0,
     "Clear; 74 ft max, ~33 ft mean.",
     "Full motor, no cap; Chequamegon National Forest shoreline keeps development low.",
     "3,294 acres wrapped by national forest northeast of Hayward — the buildable Trout Lake, on the water. The market is the problem: the one two-building listing (12391 W Moreland Rd, $1.95M) went pending on Sep 1, and nothing else is live. A relationships-and-letters lake, like Kezar in the Northeast report.",
     [["Hayward Lakes", "https://haywardlakes.com/activities/lakes/"]]),

lake("teal_lost_land", "Teal & Lost Land Lakes", "WI", 46.042, -91.098, 2300, "~6:25", "t2", 8.0,
     "Moderately clear; connected pair.",
     "Full motor; connected by a navigable thoroughfare.",
     "A connected 2,300-acre pair inside the Chequamegon National Forest, historically resort country — which means grandfathered cabin clusters, the exact product this brief is hunting.",
     []),

lake("spider_chain", "Spider Lake Chain", "WI", 46.028, -91.150, 1500, "~6:25", "t2", 7.5,
     "Moderately clear across the five basins.",
     "Full motor; connected chain.",
     "Five connected lakes in the national forest north of Hayward with an old resort economy and one of the highest densities of multi-cabin properties in the state.",
     []),

lake("chippewa_flowage", "Chippewa Flowage", "WI", 45.900, -91.100, 15300, "~6:20", "t2", 8.0,
     "Moderate, tannin-stained; 92 ft max.",
     "Full motor; 200+ miles of shoreline, most of it undeveloped.",
     "15,300 acres, 140 islands, and more than 200 miles of shoreline that will never be built on — Wisconsin's third-largest lake and its most convincing wilderness. Stumps, drawdowns and stained water are the price of admission; five couples who want scale over sparkle should look hard here.",
     [["Chippewa Flowage", "https://dnr.wisconsin.gov/topic/lands/chippewaflowage"]]),

lake("big_sissabagama", "Big Sissabagama Lake", "WI", 45.952, -91.252, 805, "~6:15", "watch", 7.0,
     "Clear; 48 ft max.",
     "Full motor.",
     "805 clear acres near Stone Lake with a quiet, almost entirely residential shore. Under the size bar; a good second lake.",
     []),

lake("nelson_lake", "Nelson Lake", "WI", 46.060, -91.300, 2500, "~6:25", "watch", 6.0,
     "Stained and shallow — fails the water bar.",
     "Full motor; wide open.",
     "2,500 acres of cheap frontage near Hayward. Big and boat-friendly, but tea-dark and shallow. In the report for price transparency, not as a recommendation.",
     []),

lake("lake_owen", "Lake Owen", "WI", 46.352, -91.300, 1250, "~6:45", "t2", 9.0,
     "Elite — Secchi ~24.6 ft, graded A. 95 ft max. DNR classifies it very clear.",
     "Full motor, no cap; Chequamegon National Forest landing, minimal traffic.",
     "The northern jewel: 1,250 acres, 95 feet deep, 24.6-foot clarity, and national forest on most of the shore south of Cable. Smaller than the bar wants and priced accordingly at the top (a 5.3-acre, 350-ft retreat is asking $3M) — but the water and the hush are Squam-grade.",
     [["Lake Owen listings", "https://www.zillow.com/cable-wi/lake-owen_att/"]]),

lake("namekagon_lake", "Lake Namakagon", "WI", 46.222, -91.052, 2897, "~6:35", "t2", 8.0,
     "Clear; shallow-ish for its size at 51 ft max, 16 ft mean.",
     "Full motor, no cap; national forest shoreline.",
     "2,897 acres in the Chequamegon-Nicolet National Forest above Cable — the headwater of the Namekagon National Scenic Riverway, with real running room and prices well under the Vilas/Antrim premium (Bayfield County average ask ~$627K). Shallower than the depth-lovers want.",
     []),

lake("eau_claire_lakes", "Eau Claire Lakes chain", "WI", 46.348, -91.500, 1100, "~7:00", "t2", 7.5,
     "Clear; three connected basins with sand bottoms.",
     "Full motor; connected chain, low traffic.",
     "Three connected clear-water basins in far Bayfield County — sand bottoms, pines, and almost no through traffic. Sub-bar individually, credible as a chain.",
     []),

lake("nebagamon", "Lake Nebagamon", "WI", 46.512, -91.700, 981, "~7:15", "t2", 7.5,
     "Clear; sand-bottomed.",
     "Full motor; village lake with a genuine summer-colony culture.",
     "981 acres and a hundred-year-old summer village an hour from Duluth. Sub-bar on size but archetype-grade on culture, and among the cheapest clear frontage in the sweep.",
     []),

# ---- Michigan · Grand Traverse / Leelanau / Benzie ------------------------
lake("crystal_lake_benzie", "Crystal Lake", "MI", 44.660, -86.150, 9854, "~5:15", "t1", 9.5,
     "Elite — marl-bottomed, 165 ft max, 70 ft mean; the 'Caribbean of the North'.",
     "Full motor, no cap; Michigan's statewide no-wake band is 100 ft from shore / under 3 ft depth.",
     "Michigan's ninth-largest inland lake and one of its two clearest: 9,854 acres, 165 feet deep, 21 miles of shoreline, and turquoise water over white marl. Five and a quarter hours from the Loop — the best water-to-drive ratio in this entire report. The trade is price and pace: Beulah frontage runs $1.2M–$1.9M for ordinary cottages, and a compound means assembling.",
     [["Crystal Lake Watershed Association", "https://crystallakewatershed.org/watershed-facts/"],
      ["Crystal Lake listings", "https://www.lakehomes.com/michigan/crystal-lake-beulah"]]),

lake("big_glen", "Big Glen Lake", "MI", 44.878, -85.972, 4871, "~5:30", "t2", 9.0,
     "Excellent — Secchi just over 19 ft in the Leelanau Conservancy dataset; 130 ft max.",
     "Full motor, no cap; the narrows to Little Glen are no-wake.",
     "4,871 acres inside Sleeping Bear Dunes National Lakeshore — federal land on a large share of the shore, water that photographs like the Caribbean, and dunes for a backdrop. The most beautiful lake in this report. Also among the most expensive and the most supply-constrained: very few homes trade in any year, and $3M is an ordinary ask.",
     [["Leelanau Conservancy Secchi data", "https://leelanauconservancy.org/wp-content/uploads/2012/01/Secchi_meanMinMax_allLakes_allyears.pdf"]]),

lake("lake_leelanau", "Lake Leelanau (N & S)", "MI", 45.020, -85.720, 8607, "~5:30", "t2", 8.5,
     "Good; North basin 121 ft max, South 62 ft.",
     "Full motor; the narrows at Leland Township are no-wake. Active wake-boat debate — Lake Leelanau Lake Association is a lead advocate for 500-ft setbacks.",
     "8,607 acres across two connected basins in the middle of Leelanau's wine country — big water, good clarity, real running room, and a shore that mixes orchards with cottages. Cheaper than Glen, busier than Crystal.",
     [["Lake Leelanau Association on wake boats", "https://lakeleelanau.org/wake-boats/"]]),

lake("long_lake_gt", "Long Lake (Grand Traverse)", "MI", 44.752, -85.752, 2860, "~5:15", "t2", 8.0,
     "Good; deep basins, sand bottom, several islands.",
     "Full motor; township ordinances govern speed near the islands.",
     "2,860 acres and several wooded islands twenty minutes west of Traverse City. Clear sand-bottom water, established cottage culture, and — unusually for the region — enough size for five boats without feeling like a highway.",
     []),

lake("platte_lake", "Big Platte Lake", "MI", 44.702, -86.048, 2517, "~5:15", "t2", 7.5,
     "Good; the subject of a decades-long, court-supervised phosphorus cleanup that worked.",
     "Full motor; Sleeping Bear National Lakeshore adjoins.",
     "2,517 acres beside Sleeping Bear, with a shoreline association that litigated its way to clean water and won. Quieter and cheaper than Glen or Crystal, and a real ski lake.",
     []),

lake("portage_lake_onekama", "Portage Lake (Onekama)", "MI", 44.362, -86.282, 2110, "~4:50", "t2", 7.5,
     "Good; channel to Lake Michigan.",
     "Full motor; a working channel to Lake Michigan means a mixed fleet.",
     "2,110 acres with its own channel to Lake Michigan — the only lake in this report where you can ski all morning and run to big water in the afternoon. Under five hours out. The channel is also the caveat: this is a boating lake, not a hushed one.",
     []),

lake("hamlin_lake", "Hamlin Lake", "MI", 44.052, -86.402, 4990, "~4:30", "watch", 6.5,
     "Moderate; shallow upper basin, dark water in the narrows.",
     "Full motor; Ludington State Park landing draws real crowds.",
     "4,990 acres at four and a half hours — the closest big lake that clears the drive floor. Good boating, ordinary water, and state-park traffic all summer. A convenience play, not an archetype one.",
     []),

# ---- Michigan · Antrim / Charlevoix / Emmet ------------------------------
lake("elk_lake", "Elk Lake", "MI", 44.900, -85.418, 7730, "~5:25", "t1", 9.0,
     "Elite — 192 ft max, oligotrophic, part of the Elk River Chain of Lakes monitoring program.",
     "Full motor, no cap; quieter than neighboring Torch by a wide margin.",
     "Torch Lake's water without Torch Lake's sandbar. 7,730 acres, 192 feet deep, the same improbable blue, and a shoreline of old cottages rather than party barges — plus a connection through the Chain of Lakes to Torch and Bellaire when you want the scene. The strongest single lake on the Michigan side.",
     [["Elk Lake", "https://www.lakehouse.com/elk-lake-antrim-county-michigan-lake-homes-for-sale-b3736.html"]]),

lake("torch_lake", "Torch Lake", "MI", 44.982, -85.352, 18770, "~5:35", "t2", 7.5,
     "Elite on paper — 330 ft max, 111 ft mean, ranked among the clearest lakes in the Western Hemisphere.",
     "Full motor, no cap; the sandbar at the south end is a nationally known party anchorage on summer weekends.",
     "The most beautiful water in the Midwest and the least Squam-like culture in this report. 18,770 acres of turquoise over marl — and, on a July Saturday, several hundred rafted boats on the south sandbar. Buy on the quiet northeast shore or don't buy here; a 14-acre, 4BR at $999K shows it can be done.",
     [["Torch Lake real estate guide", "https://brickcorbett.com/neighborhoods/torch-lake"]]),

lake("lake_bellaire", "Lake Bellaire", "MI", 44.982, -85.222, 1775, "~5:35", "t2", 8.0,
     "Good; 96 ft max, part of the Chain of Lakes.",
     "Full motor; connected to Torch via the Torch River / Clam River.",
     "1,775 acres at the quiet end of the Antrim chain: clear enough, deep enough, connected to everything, and priced meaningfully below Torch or Elk. The value entry into the Chain of Lakes.",
     []),

lake("intermediate_lake", "Intermediate Lake", "MI", 45.048, -85.222, 1520, "~5:40", "watch", 7.0,
     "Moderate; shallower and more colored than its neighbors.",
     "Full motor; chain-connected.",
     "1,520 acres at the top of the Antrim chain, notably cheaper than the lakes below it — and notably less clear. A budget route onto the chain.",
     []),

lake("lake_charlevoix", "Lake Charlevoix", "MI", 45.282, -85.152, 17260, "~5:50", "t2", 8.0,
     "Good to very good; 122 ft max, channel to Lake Michigan.",
     "Full motor; the South Arm is markedly quieter than the main basin.",
     "17,260 acres, a Lake Michigan channel, and Boyne City and Charlevoix on its shores — the Midwest's Lake Winnipesaukee, with the same virtues and the same crowding. The South Arm is the play: median frontage runs ~$2,450/ft there against $7,000–$12,000/ft on the main basin.",
     [["Lake Charlevoix waterfront", "https://www.brookwalsh.com/lake-charlevoix-realestate.php"]]),

lake("walloon_lake", "Walloon Lake", "MI", 45.282, -84.952, 4584, "~6:00", "t2", 9.0,
     "Elite — oligotrophic, visibility frequently over 20 ft, 100 ft max.",
     "Full motor, no cap; no public marina, one modest launch, and a shoreline culture that polices its own noise.",
     "The Squam of the Midwest, in every sense including price. 4,584 acres of oligotrophic water, Hemingway's boyhood lake, no commercial shoreline, and generational owners who do not sell. Twelve listings totalled $64.7M this summer; entry cottages start in the mid-$800Ks and the good frontage is $7M+. Include it, tour it, and know the odds.",
     [["Tip of the Mitt — Walloon Lake", "https://watershedcouncil.org/waterbody/walloon-lake/"]]),

lake("crooked_pickerel", "Crooked & Pickerel Lakes", "MI", 45.442, -84.852, 3450, "~6:05", "t2", 8.0,
     "Good; Pickerel is the deeper and clearer of the pair.",
     "Full motor; the Inland Waterway connects them to Burt, Mullett and Lake Huron.",
     "3,450 combined acres at the west end of the Inland Waterway — the 38-mile chain that runs from Conway to Cheboygan and out to Lake Huron. Quiet, forested, and priced well below Walloon ten minutes away.",
     [["Tip of the Mitt Watershed Council", "https://watershedcouncil.org/watersheds/burt-lake-watershed/"]]),

lake("burt_lake", "Burt Lake", "MI", 45.442, -84.628, 17436, "~6:10", "t2", 8.0,
     "Good — the Watershed Council rates it a large, deep, high-quality lake. 73 ft max, 35 mi shoreline.",
     "Full motor, no cap; big enough to absorb traffic.",
     "Michigan's fourth-largest inland lake, 17,436 acres in the middle of the Inland Waterway, with a state park, a big forested east shore, and prices far below the Torch/Walloon corridor. Room for five boats and then some.",
     [["Tip of the Mitt — Burt Lake", "https://watershedcouncil.org/waterbody/burt/"]]),

lake("mullett_lake", "Mullett Lake", "MI", 45.502, -84.522, 16630, "~6:15", "t2", 8.5,
     "Very good — 145 ft max, 200 billion gallons, rated high-quality by the Watershed Council.",
     "Full motor, no cap.",
     "16,630 acres and 145 feet deep — Michigan's fifth-largest and, for its size, remarkably underdeveloped. Twenty-eight miles of shoreline, an Inland Waterway connection, and Cheboygan County prices. The best acreage-per-dollar on clear Michigan water.",
     [["Tip of the Mitt — Mullett Lake", "https://watershedcouncil.org/waterbody/mullett-lake/"]]),

lake("douglas_lake", "Douglas Lake", "MI", 45.572, -84.680, 3727, "~6:15", "t2", 8.5,
     "Very good and improving — Secchi 10–14 ft; the Watershed Council notes it now borders on oligotrophy. 80 ft max.",
     "Full motor; low traffic, no town on the lake.",
     "3,727 acres wrapped by the University of Michigan Biological Station — a century of research, no commercial shoreline, no village, and the quietest big water in the northern Lower Peninsula. The closest thing Michigan has to a state-forest lake with private frontage on it.",
     [["Tip of the Mitt — Douglas Lake", "https://watershedcouncil.org/waterbody/douglas-lake-cheboygan-county/"]], new=True),

lake("black_lake_mi", "Black Lake", "MI", 45.472, -84.272, 10130, "~6:25", "watch", 6.5,
     "Moderate; 50 ft max, more colored than its neighbors.",
     "Full motor; low traffic, state forest campground.",
     "10,130 acres of cheap frontage east of Onaway with state forest on part of the shore. Big and quiet; the water is ordinary. A value fallback.",
     []),

# ---- Michigan · northeast & central LP -----------------------------------
lake("higgins_lake", "Higgins Lake", "MI", 44.472, -84.722, 9600, "~5:25", "t2", 9.0,
     "Elite — Secchi 28.5–35 ft across the basins; 135 ft max, 21 mi shoreline. Michigan's clearest large lake alongside Torch.",
     "Full motor, no cap; two state parks and heavy summer boat traffic on weekends.",
     "The clearest big water within five and a half hours of Chicago: 9,600 acres and Secchi readings in the thirties. The tradeoff is honest and significant — two state parks, a fully developed ring road, and midsummer Saturdays that feel like a lake in a metro area. Buy on the quiet north or east shore; frontage runs ~$1M–$1.9M.",
     [["Higgins Lake Foundation water testing", "https://www.higginslake-foundation.org/protect/water-testing/"],
      ["HLPOA water quality", "https://hlpoa.org/studies-surveys-general-water-quality/"]]),

lake("lake_margrethe", "Lake Margrethe", "MI", 44.658, -84.782, 1920, "~5:45", "watch", 6.5,
     "Moderate; 65 ft max.",
     "Full motor; Camp Grayling adjoins — expect occasional National Guard activity.",
     "1,920 acres outside Grayling with state land and the Camp Grayling reservation on part of the shore. Cheap, quiet on weekdays, and not archetype-clear.",
     []),

lake("hubbard_lake", "Hubbard Lake", "MI", 44.822, -83.572, 8850, "~6:45", "t2", 7.5,
     "Good, not elite — Secchi around 12 ft; 97.5 ft max.",
     "Full motor, no cap; very low traffic.",
     "8,850 acres and nearly 100 feet deep in the empty northeast corner of the Lower Peninsula — big, deep, quiet, and dramatically cheaper than anything on the Lake Michigan side. Twelve-foot clarity is the honest limit; the value is not.",
     [["Hubbard Lake", "https://www.visitalpena.com/visit-alpena/hubbard-lake/"]]),

lake("grand_lake_pi", "Grand Lake", "MI", 45.302, -83.532, 5660, "~6:55", "t2", 7.5,
     "Good; spring-fed, shallow-to-moderate depth.",
     "Full motor; almost no commercial development.",
     "5,660 spring-fed acres on the Presque Isle peninsula, minutes from two Lake Huron lighthouses and essentially undiscovered by the Chicago market. Cheap, quiet, and genuinely remote.",
     []),

# ---- Michigan · Upper Peninsula ------------------------------------------
lake("chicaugon", "Chicaugon Lake", "MI", 46.132, -88.618, 1100, "~6:15", "t2", 8.5,
     "Excellent and improving — 115 ft max, among the deepest lakes of its size in the UP.",
     "Full motor, no cap; low traffic year-round.",
     "1,100 acres and 115 feet deep outside Iron River — the UP's best-kept clear-water secret, with improving Secchi trends, an active property owners association, and prices that would embarrass Vilas County. Under the size bar; over-delivers on everything else.",
     [["Chicaugon Lake POA", "https://chicaugonlake.weebly.com/"]], new=True),

lake("cisco_chain", "Cisco Chain of Lakes", "MI/WI", 46.198, -89.282, 4025, "~6:20", "t2", 8.0,
     "Moderate to good; Thousand Island Lake is the deepest at ~40 ft, most basins are shallower.",
     "Full motor throughout; 15 connected lakes and 270 miles of shoreline — the largest connected chain in this report.",
     "Fifteen connected lakes, 4,025 acres and 270 miles of shoreline straddling the state line at Watersmeet — you can run a boat all day and not repeat a bay. Substantially Ottawa National Forest shoreline. Shallow enough that the water colors by August; the cruising is unmatched anywhere in the Midwest.",
     [["Cisco Chain properties (Eliason)", "https://www.eliasonrealty.com/cisco-chain/"],
      ["Cisco Chain overview", "https://explorewesternup.com/things-to-do/cisco-chain-of-lakes/"]]),

lake("lake_gogebic", "Lake Gogebic", "MI", 46.500, -89.582, 13380, "~7:05", "t2", 7.0,
     "Moderate; 38 ft max — big but shallow.",
     "Full motor; state park landing, very low traffic.",
     "The UP's largest inland lake at 13,380 acres, ringed by Ottawa National Forest and state park, with almost no development and the lowest waterfront prices per foot in this report — roughly 400 ft of raw east-shore frontage is live at $595K. Shallow water is the tradeoff.",
     []),

lake("michigamme", "Lake Michigamme", "MI", 46.532, -88.098, 4292, "~6:55", "watch", 6.5,
     "Weak — Secchi 7–8 ft; tannin-stained.",
     "Full motor; islands and rock, very low traffic.",
     "4,292 acres of dramatic rock-and-pine country west of Marquette. Spectacular setting, genuinely poor clarity. Listed for honesty: the sweep's best scenery-to-water-quality mismatch.",
     []),

lake("lake_independence", "Lake Independence", "MI", 46.548, -87.722, 1860, "~7:15", "watch", 6.5,
     "Moderate; shallow.",
     "Full motor; a mile from Lake Superior at Big Bay.",
     "1,860 acres at Big Bay, twenty minutes from Lake Superior and about as far from Chicago as this brief allows. Remote, cheap, and not clear.",
     []),

lake("brevoort_lake", "Brevoort Lake", "MI", 46.028, -85.048, 4233, "~6:45", "watch", 6.5,
     "Moderate; shallow (~30 ft).",
     "Full motor; Hiawatha National Forest shoreline.",
     "4,233 acres inside the Hiawatha National Forest west of St. Ignace — nearly all federal shoreline, so private frontage is rare and cheap when it appears. Shallow, stained water.",
     []),

lake("les_cheneaux", "Les Cheneaux Islands", "MI", 46.002, -84.422, 6000, "~7:00", "t2", 8.5,
     "Excellent — Lake Huron water, cold and clear, in a sheltered 36-island archipelago.",
     "Full motor; protected channels mean flat water most days. This is Great Lakes water, not an inland lake.",
     "The outlier and, for some groups, the answer: 36 islands and a dozen sheltered channels on northern Lake Huron, with a century-old wooden-boat culture, no crowds, and cottage prices a third of Torch Lake's. A private island with 575 ft of frontage and a three-stall boathouse is live at $1.0M. The catch: Great Lakes weather, a shorter season, and seven hours of driving.",
     [["Les Cheneaux Islands", "https://www.uptravel.com/places-to-visit/islands/les-cheneaux/"]], new=True)

# ---- second pass: lakes surfaced by the county-by-county sweep -------------
lake("manitowish_chain", "Manitowish Waters Chain", "WI", 46.132, -89.882, 3800, "~5:55", "t2", 8.0,
     "Mixed across the ten basins — Rest and Spider are clear, the flowage arms are stained.",
     "Full motor throughout; ten connected lakes, the most navigable chain in Vilas County.",
     "Ten connected lakes and roughly 3,800 acres in the northwest corner of Vilas County — genuine all-day cruising, a village with a grocery and an airstrip, and inventory that actually moves. The chain's water is good, not great; buy on Rest or Spider, not the flowage arms.",
     []),

lake("kentuck_lake", "Kentuck Lake", "WI", 46.028, -88.960, 958, "~5:50", "watch", 7.0,
     "Moderately clear; shallow (~26 ft).",
     "Full motor; Chequamegon-Nicolet National Forest shoreline.",
     "958 acres in the national forest east of Eagle River with federal land on much of the shore. Shallow, but almost undeveloped and cheap.",
     []),

lake("little_st_germain", "Little St. Germain Lake", "WI", 45.945, -89.478, 987, "~5:40", "watch", 6.5,
     "Moderate; four connected bays, weedier than Big St. Germain.",
     "Full motor; connected to Big St. Germain.",
     "987 acres in four bays with a dense cottage shore. Included for market depth rather than water quality.",
     []),

lake("boulder_lake_vilas", "Boulder Lake", "WI", 46.095, -89.635, 542, "~5:50", "watch", 7.5,
     "Clear; NHAL State Forest lake.",
     "Full motor; forest landing only.",
     "542 clear acres inside the state forest just north of Trout Lake. Under the size bar, but the frontage that exists here is the closest anyone gets to owning on the archetype cluster.",
     []),

lake("clear_lake_oneida", "Clear Lake (Oneida)", "WI", 45.808, -89.518, 470, "~5:30", "watch", 7.5,
     "Clear, as advertised; spring-fed.",
     "Full motor; very low traffic.",
     "470 acres of genuinely clear water near Lake Tomahawk. Well under the size bar; a strong second lake for a Tomahawk purchase.",
     []),

lake("moen_chain", "Moen Chain", "WI", 45.660, -89.310, 1100, "~5:20", "watch", 7.0,
     "Moderate across four connected basins.",
     "Full motor; connected chain.",
     "Four connected lakes north of Rhinelander with reasonable cruising and prices below the Minocqua belt. Ordinary water.",
     []),

lake("whitefish_sawyer", "Whitefish Lake", "WI", 45.852, -91.155, 800, "~6:15", "watch", 7.5,
     "Clear; deep basins.",
     "Full motor.",
     "800 clear acres south of Hayward with a quiet residential shore. Under the size bar; good water and good value.",
     []),

lake("middle_eau_claire", "Middle Eau Claire Lake", "WI", 46.322, -91.492, 880, "~7:00", "watch", 7.5,
     "Clear, sand-bottomed.",
     "Full motor; part of the three-lake Eau Claire chain.",
     "880 sand-bottomed acres in far Bayfield County — the best of the Eau Claire basins, and among the cheapest clear water in the state.",
     []),

lake("upper_st_croix", "Upper St. Croix Lake", "WI", 46.288, -91.828, 856, "~7:10", "watch", 6.5,
     "Moderate; shallow.",
     "Full motor; headwater of the St. Croix National Scenic Riverway.",
     "856 acres at the head of the St. Croix Riverway. Historic setting, ordinary water, and about as far west as this brief reaches.",
     []),

lake("lake_lucerne", "Lake Lucerne", "WI", 45.612, -88.702, 1000, "~5:20", "t2", 7.5,
     "Clear; 65 ft max, spring-fed.",
     "Full motor, no cap; Nicolet National Forest shoreline.",
     "1,000 clear, deep acres in the Nicolet north of Crandon, with federal forest on much of the shore and essentially no Chicago awareness. Pairs with Lake Metonga fifteen minutes away.",
     [], new=True),

lake("roberts_lake", "Roberts Lake", "WI", 45.612, -88.842, 470, "~5:15", "watch", 7.0,
     "Moderately clear.",
     "Full motor.",
     "470 acres near Crandon with low prices and low traffic. Under the size bar; a value satellite to Metonga.",
     []),

lake("noquebay", "Lake Noquebay", "WI", 45.238, -87.912, 2400, "~4:45", "watch", 6.0,
     "Moderate; 51 ft max but weedy bays.",
     "Full motor, no cap.",
     "2,400 acres at four and three-quarter hours — the second-closest big ski lake in the report after Pelican. The water is ordinary and the shoreline unconserved; a drive-time play only.",
     []),

# ---- Michigan · second pass ----------------------------------------------
lake("green_lake_mi", "Green Lake (Interlochen)", "MI", 44.632, -85.782, 1980, "~5:10", "t2", 8.0,
     "Very good — 100 ft max, clear and spring-fed.",
     "Full motor; Interlochen State Park landing is the only public access.",
     "1,980 acres and 100 feet deep beside Interlochen Center for the Arts — clear, deep, five hours from Chicago, and consistently overlooked by buyers fixated on Torch. Summer concerts drift across the water, which most groups count as a feature.",
     [], new=True),

lake("thumb_lake", "Thumb Lake (Lake Louise)", "MI", 45.098, -84.848, 470, "~6:00", "watch", 8.0,
     "Elite — one of Michigan's clearest, ~90 ft deep, spring-fed.",
     "Full motor; tiny landing, almost no traffic.",
     "470 acres of exceptionally clear, 90-foot-deep water in the Boyne highlands. Far under the size bar and included on water quality alone — if the group would trade running room for clarity, tour it.",
     [], new=True),

lake("bear_lake_manistee", "Bear Lake (Manistee)", "MI", 44.418, -86.128, 1745, "~4:45", "watch", 6.5,
     "Moderate; shallow (~50 ft) and warmer.",
     "Full motor, no cap.",
     "1,745 acres at four and three-quarter hours with a village on one end. Cheap, boat-friendly, ordinary water.",
     []),

lake("arbutus_chain", "Arbutus / Spider Lakes chain", "MI", 44.652, -85.478, 700, "~5:10", "watch", 7.0,
     "Good; small connected lakes in the Pere Marquette State Forest.",
     "Full motor on Arbutus; the chain narrows are no-wake.",
     "A small chain inside the state forest twenty minutes from Traverse City. Too small for five boats; notable for the forest setting and prices a third of Torch's.",
     []),

lake("paradise_lake", "Paradise Lake", "MI", 45.658, -84.788, 1900, "~6:20", "watch", 6.0,
     "Weak — 1,900 ac but only ~10 ft deep.",
     "Full motor; very low traffic.",
     "1,900 acres of very shallow water near Carp Lake. The cheapest frontage in Emmet County by a wide margin, and the reason why.",
     []),

lake("munuscong", "Munuscong Bay / St. Marys", "MI", 46.152, -84.152, 5000, "~7:10", "watch", 6.5,
     "Moderate; shallow river-system water.",
     "Full motor; freighter channel nearby.",
     "The St. Marys River system south of Sault Ste. Marie — big water, cheap frontage, and freighters on the horizon. Not the archetype; excellent for a group that wants a working Great Lakes view.",
     []),

lake("hagerman_lake", "Hagerman Lake", "MI", 46.062, -88.702, 640, "~6:10", "watch", 7.5,
     "Clear; Ottawa National Forest lake.",
     "Full motor; national forest landing.",
     "640 clear acres in the Ottawa National Forest outside Iron River, with a live 7-acre waterfront parcel at $425K. Under the size bar; the price-per-acre of clear UP water is the story.",
     []),

lake("fortune_lakes", "Fortune Lakes", "MI", 46.098, -88.898, 500, "~6:15", "watch", 7.0,
     "Clear; three connected basins.",
     "Full motor; connected chain, very low traffic.",
     "Three small connected clear lakes in Iron County. Nowhere near the size bar, but representative of what $150K–$400K buys in the western UP.",
     []),

lake("millecoquins", "Millecoquins Lake", "MI", 46.088, -85.428, 1275, "~6:55", "watch", 6.5,
     "Moderate; shallow and tannin-tinted.",
     "Full motor; almost no development.",
     "1,275 acres near Naubinway with a shoreline that is largely state and federal land. Remote and cheap; the water is bog-influenced.",
     []),

lake("deer_lake_charlevoix", "Deer Lake (Boyne)", "MI", 45.238, -84.912, 500, "~5:55", "watch", 7.0,
     "Good; small and clear.",
     "Full motor; small landing.",
     "500 clear acres at Boyne City, ten minutes from Lake Charlevoix's South Arm. Under the size bar; a credible satellite purchase.",
     []),

# ---------------------------------------------------------------- listings
LI = []
def listing(lakeKey, name, price, lat, lon, detail, url, fit, status="active", lakeName=None, state=None, new=False):
    d = dict(lakeKey=lakeKey, name=name, price=price, lat=lat, lon=lon, detail=detail,
             status=status, url=url, fit=fit, cls="listing", new=new)
    if lakeName: d["lakeName"] = lakeName
    if state: d["state"] = state
    LI.append(d)

# --- the program plays: whole cabin clusters -------------------------------
listing("round_lake_price", "Moose Jaw Resort & Campground — $2.75M", 2750000, 45.9183, -90.0794,
        "W770 Wind Song Ln, Park Falls (Price Co.); MLS 2028977; 17 ac, 8 cabins, 18 campsites, 24 boat slips, bar & restaurant; founded 1887",
        "https://www.jmdsproperties.com/wi-resorts-for-sale/w770-wind-song-lane-road-other-price-wisconsin-54552/",
        "CORRECTED Sep 1: this is Round Lake of the Pike Chain in PRICE County, not the 3,294-acre Round Lake near Hayward. Eight cabins and a licensed bar on 17 national-forest acres is a real program — but the lake is 726 ac, 24 ft deep and root-beer coloured. Program yes, water no.",
        lakeName="Round Lake (Pike Chain, Price Co.)", state="WI", new=True)
listing("north_twin", "Coady's Point of View Resort, North Twin — $2.8M", 2800000, 46.078, -89.108,
        "Resort + campground on the Twin Lakes chain; family-run since 1897",
        "https://www.lakeplace.com/forsale/wi-county/vilas/",
        "129 years of grandfathered use on 2,871 acres of Class-A water. Keep six cabins, retire the campground, and you have the sketch.")
listing("big_arbor_vitae", "11400 Santo Rd, Arbor Vitae — $3.25M", 3250000, 45.932, -89.648,
        "34.5 ac; multiple year-round dwellings and cottages, rental-capable",
        "https://www.lakeplace.com/forsale/wi-county/oneida/",
        "Thirty-four acres and a multi-dwelling permit history — the density is the asset. The lake (busy Big Arbor Vitae) is the compromise.")
listing("lower_buckatabon", "Buckatabon Lodge & Campground — $3.75M", 3750000, 46.103, -89.352,
        "32.97 wooded ac, 459 ft sand shoreline on Lower Buckatabon Lake; lodge + cabins + campground",
        "https://www.lakeplace.com/forsale/wi-county/vilas/",
        "Over budget, but the clearest picture of what a licensed Northwoods resort conveys: grandfathered cabin density on sand frontage. Worth a calibration tour.",
        lakeName="Lower Buckatabon Lake", state="WI")
listing("tomahawk_lake", "Legacy lakefront estate, Lake Tomahawk — $3.3M", 3300000, 45.838, -89.628,
        "1.45 ac, 338 ft frontage; maintained main home, furnished cabins, multiple docks",
        "https://www.lakeplace.com/forsale/wi/minocqua/",
        "Exactly the program — lodge, cabins, docks — on 3,392 acres of 84-ft-deep clear water. Stretch pricing; the closest turnkey answer in Wisconsin.")
listing("pelican_lake", "Pelican Lake resort — $724.9K", 724900, 45.492, -89.208,
        "~9 ac with 204 ft of frontage; cabin cluster",
        "https://www.commercialzip.com/wi/resorts/",
        "Under $750K for nine acres and a cabin cluster on 3,585 acres of ski water at five hours flat. Budget for a full rebuild; the entitlements are the buy.")
listing("moen_chain", "Pine Valley Lodge, Rhinelander — $1.5M", 1499999, 45.655, -89.335,
        "4000 Lakeshore Dr; MLS 217391; 27 ac with 1,900 ft on the 5-lake Moen Chain; 1920s lodge w/ full liquor licence, 5,000 sf rec hall, guest cabins, owner's residence, sand beach",
        "https://www.shorewest.com/WI/Oneida/Rhinelander/4000-Lakeshore-Dr-Rhinelander-WI-54501/217391-GNMLS",
        "Twenty-seven acres and 1,900 feet of chain frontage for $1.5M — on pure frontage-per-dollar, the best land basis in the sweep, and the buildings are already there. Moen's 1,100 acres are ordinary water; the entitlements and the shoreline are not. One source quotes $1.6M — confirm.", new=True)
listing("herendeene_lake", "Northern Michigan cabin resort (Herendeene Lake) — $2.5M", 2500000, 44.782, -85.902,
        "430–450 ft frontage; hand-hewn 5BR log home + 6BR farmhouse + 6 remodeled cabins",
        "https://www.traversenorth.com/property-search/waterfront-resorts-and-businesses.html",
        "Literally lodge + 6 cabins, between Sleeping Bear and Traverse City — BUT Herendeene is a 40-acre no-motor pond. Program 10/10, water 2/10. Tour it to calibrate, buy only with eyes open.",
        lakeName="Herendeene Lake", state="MI", new=True)
listing("halfway_lake", "Halfway Lake Cottages, Newberry — $1.595M", 1595000, 46.412, -85.522,
        "25 ac, ~1,700 ft frontage; 8 cabins + guest house + 3BR owner's residence + pole barn",
        "https://www.haydenoutdoors.com/land-for-sale/halfway-lake-cottages/",
        "Eight cabins, a guest house and a lodge for $1.6M — the single best program-per-dollar found anywhere. The lake is private and no-motor: keep the boats an hour south, or pass.",
        lakeName="Halfway Lake (private, no-motor)", state="MI", new=True)
listing("houghton_lake", "Houghton Lake cabin resort — $1.19M", 1190000, 44.335, -84.762,
        "7 cabins + 2 homes on 150 ft of frontage",
        "https://realmo.com/resorts/for-sale/mi/",
        "Nine buildings for $1.19M, forty minutes from Higgins. Houghton Lake itself is 20,000 shallow, busy acres — a program-first, lake-second fallback.",
        lakeName="Houghton Lake", state="MI")
listing("crooked_lake_lakemi", "Crooked Lake Resort, Lake MI — verify price", None, 43.988, -85.045,
        "Owner's home + 6 winterized log cabins + park model + bait store on 146 ft of sand",
        "https://www.cabinsandcamps.com/crookedlakeresort",
        "Six winterized log cabins with fireplaces and a large owner's home — the turnkey version of the program at roughly 4:15 from Chicago. Small lake; confirm price and frontage with the broker.",
        status="verify", lakeName="Crooked Lake (Lake, MI)", state="MI")

# --- the land plays: frontage to build on ---------------------------------
listing("lac_du_lune", "Lt 11-15 Briar Ln, Land O'Lakes — $1.35M", 1350000, 46.142, -89.248,
        "MLS 218079; 27.1 ac with 1,181 ft of sand frontage, and it wraps a separate 13-acre pond",
        "https://landvest.com/listing/218079/lt-11-15-briar-lane-land-o-lakes-wi-54540/",
        "The largest single-owner frontage assemblage found in Vilas County: 1,181 ft is enough for a lodge and five separately-lotted cabins under county shoreland math, on a 442-acre lake with nearly 20 ft of clarity. Build the sketch exactly.", new=True)
listing("dunn_lake", "Dunn Lake parcel, Presque Isle — $347.5K", 347500, 46.215, -89.756,
        "14+ ac with over 1,000 ft of lake frontage",
        "https://www.landflip.com/land-for-sale/wisconsin/vilas-county/waterfront-keyword",
        "A thousand feet of frontage for under $350K. Dunn is too small to ski — pair it with a slip on Presque Isle Lake five minutes away and you have a cheap, legal compound.")
listing("star_lake_private", "Star Lake (Sawyer Co.) — 646 ac — $3.8M", 3800000, 45.885, -91.462,
        "646± ac surrounding a 105-ac lake; the only private land on the water",
        "https://www.landflip.com/land-for-sale/wisconsin/vilas-county/waterfront-keyword",
        "Own the entire shoreline of your own lake — 646 acres, no neighbors, ever. Too small for towsports; the ultimate privacy play if the group will keep boats elsewhere.",
        lakeName="Star Lake (Sawyer Co., private)", state="WI")
listing("amik_lake", "Amik Lake parcel + cabin, Lac du Flambeau — $305K", 305000, 45.968, -89.812,
        "31.85 wooded acres with an existing cabin",
        "https://www.landflip.com/land-for-sale/wisconsin/vilas-county/waterfront-keyword",
        "Thirty-two acres and a standing cabin for $305K. Cheapest acreage-plus-structure in the sweep; verify frontage and reservation title questions before anything else.")
listing("lake_gogebic", "East shore frontage, Bergland — $595K", 595000, 46.518, -89.542,
        "~400 ft of undeveloped frontage on the UP's largest inland lake",
        "https://www.land.com/Upper-Peninsula-Michigan-Region/lakefront-property/",
        "Four hundred raw feet on 13,380 acres for $595K — the cheapest big-lake frontage found. Shallow water and a seven-hour drive are the price.")
listing("fence_lake_baraga", "28278 Fence Lake Rd, Michigamme — verify price", None, 46.512, -88.152,
        "14.2-ac private waterfront sanctuary, Baraga County",
        "https://www.land.com/Upper-Peninsula-Michigan-Region/lakefront-property/",
        "Fourteen private acres in the most dramatic country in this report. Clarity is the weak point; confirm price and frontage with the listing office.",
        status="verify")
listing("hagerman_lake", "Hagerman Lake Rd, Iron River — $425K", 425000, 46.062, -88.702,
        "7.07 ac lakefront, Iron County MI",
        "https://www.land.com/Upper-Peninsula-Michigan-Region/lakefront-property/",
        "Seven waterfront acres for $425K, twenty minutes from Chicaugon's 115-ft-deep water. UP pricing is the whole argument for the western route.",
        lakeName="Hagerman Lake", state="MI")
listing("iron_county_mi", "Iron County lakefront parcel — $129.9K", 129900, 46.088, -88.612,
        "3.49 ac with ~367 ft of frontage",
        "https://www.land.com/Upper-Peninsula-Michigan-Region/lakefront-property/",
        "Under $130K for 367 feet of frontage. Assemble two or three of these and the land basis for a five-cabin compound is under $400K.",
        lakeName="Iron County, MI", state="MI")

# --- the house plays: beachheads on archetype water -----------------------
listing("black_oak", "6024 Black Oak Lake Rd S — $699K", 699000, 46.122, -89.302,
        "3BR/2BA year-round home on Wisconsin's clearest lake",
        "https://www.lakehomes.com/wisconsin/black-oak-lake-land-olakes",
        "One of very few homes that trade on Black Oak in any year. A beachhead on the best water in the state; add cabins on an adjacent lot as they surface.")
listing("round_lake_sawyer", "12391 W Moreland Rd, Hayward — $1.95M (PENDING)", 1950000, 45.976, -91.104,
        "4BR/4BA, 3,037 sf on 1.04 ac; furnished cabin + guest cottage, sugar-sand frontage",
        "https://www.lakehomes.com/wisconsin/round-lake-hayward",
        "Went PENDING as of Sep 1 — the only two-building listing on clear Round Lake, and it is spoken for. Ask the Hayward brokers to flag you if it falls through, and treat Round Lake as an off-market campaign until then.",
        status="verify")
listing("lco", "Lac Courte Oreilles legacy estate — $2.495M", 2495000, 45.908, -91.342,
        "10.82 ac with 320 ft of level, sandy shoreline",
        "https://www.lakeplace.com/forsale/wi-county/sawyer/",
        "Eleven acres and 320 feet of sand on 5,039 acres of clear water. Enough land to cluster five cabins uphill of the 75-ft setback. Check reservation title carefully.")
listing("grindstone", "Grindstone chalet + guest cottage — verify price", None, 45.972, -91.292,
        "805 sf 4-season chalet + 764 sf 3-season guest cottage; level lot, sand beach",
        "https://www.lakeplace.com/forsale/wi-county/sawyer/",
        "Two buildings already on the best Secchi readings in this report. Small structures, big water — the classic Grindstone entry. Confirm price with the Hayward brokers.",
        status="verify")
listing("high_fishtrap", "High Lake 5BR — $1.025M", 1025000, 46.158, -89.448,
        "5BR/3.5BA on the High–Fishtrap chain between Land O'Lakes and Boulder Junction",
        "https://www.goldbarrealty.com/lakehomes/milliondollar",
        "A house that already sleeps most of the group, deep in the state forest belt, for a million dollars. Add two cabins and you are done.")
listing("sugar_camp_chain", "Chain Lake, Sugar Camp — $1.499M", 1499000, 45.888, -89.318,
        "201 ft of frontage on the five-lake Sugar Camp chain",
        "https://www.goldbarrealty.com/lakehomes/milliondollar",
        "Chain access with real cruising forty minutes from Rhinelander. Frontage is thin for a five-dwelling program; treat it as the lodge and buy a neighbor.")
listing("north_twin", "Phelps Class-A assemblage — $5.249M", 5249000, 46.098, -89.092,
        "61+ ac with 1,022 ft of ripple-sand frontage",
        "https://www.goldbarrealty.com/lakehomes/millionfive",
        "Well past budget, but it is the benchmark: sixty-one acres and a thousand feet of sand on Class-A musky water. Tour it to learn what the ceiling looks like.")
listing("north_twin", "Phelps 6.95-ac, 500-ft frontage — $3.15M", 3150000, 46.068, -89.118,
        "6.95 ac with 500 ft of ripple-sand frontage",
        "https://www.goldbarrealty.com/lakehomes/millionfive",
        "Five hundred feet of sand — enough frontage for two principal dwellings plus guest houses under Vilas County math. The most executable stretch play in the county.")
listing("lake_owen", "49945 N Lake Owen Dr, Cable — $3.0M", 3000000, 46.362, -91.288,
        "5.31 ac, 350 ft of frontage, 4BR/3BA, 3,735 sf",
        "https://www.lakehouse.com/49945-n-lake-owen-dr-cable-wisconsin-54821-p7237649.html",
        "The showpiece on 24.6-ft-Secchi water. Priced like Torch Lake; five acres is enough to cluster cabins behind it if the group stretches.")
listing("namekagon_lake", "Lake Namakagon inventory — $225K–$750K", 750000, 46.228, -91.048,
        "Multiple lots and homes across the range, Cable WI",
        "https://www.lakeplace.com/forsale/lake/namekagon/",
        "The assemblage lake: several sub-$750K parcels and homes live at once on 2,897 national-forest acres. Two adjacent purchases beat one big one here.")
listing("torch_lake", "3285 S East Torch Lake Dr, Bellaire — $999K", 999000, 44.938, -85.312,
        "14+ ac, 4BR/3BA between Torch and Elk",
        "https://www.lakehouse.com/torch-lake-antrim-county-michigan-lake-homes-for-sale-b1825.html",
        "Fourteen acres in the Torch–Elk corridor for under a million — rare, and enough land for the cabin cluster. Confirm which water the frontage is on.",
        lakeName="Torch/Elk corridor", state="MI")
listing("torch_lake", "Torch Lake estate parcel — 7.5 ac", None, 44.998, -85.342,
        "Rare 7.5-ac estate parcel between Torch and Elk Lakes",
        "https://brickcorbett.com/neighborhoods/torch-lake",
        "Seven and a half acres in the most supply-constrained corridor in the Midwest. Price on application; treat as a build-from-scratch canvas.",
        status="verify")
listing("crystal_lake_benzie", "3151 Crystal Dr, Beulah — $1.9M", 1900000, 44.652, -86.128,
        "4BR/3.5BA, 2,750 sf on 0.72 ac",
        "https://www.lakehomes.com/michigan/crystal-lake-beulah",
        "Turnkey on the clearest big water in Michigan — but 0.72 acres means the cabins go on a second parcel. Buy it as the lodge and keep shopping the block.")
listing("crystal_lake_benzie", "4354 Crystal Dr, Beulah — $1.2M", 1200000, 44.668, -86.176,
        "2BR/1.5BA, 1,147 sf on 0.34 ac",
        "https://www.lakehomes.com/michigan/crystal-lake-beulah",
        "The cheapest frontage on Crystal this summer. A small cottage on a small lot — value is entirely in the water and the address.")
listing("big_glen", "7953 S Glen Lake Rd, Glen Arbor — $2.995M", 2995000, 44.868, -85.962,
        "6BR/6.5BA, 4,854 sf on 0.58 ac inside Sleeping Bear",
        "https://www.lakehomes.com/michigan/glen-lake",
        "Sleeps the whole group day one on the prettiest water in this report. Sub-acre lot: this is a lodge purchase, not a compound.")
listing("big_glen", "5760 W Crystal View Rd, Glen Arbor — $1.995M", 1995000, 44.882, -85.988,
        "4.8 ac, 3BR/2BA, 2,575 sf",
        "https://www.landwatch.com/michigan-land-for-sale/glen-arbor/waterfront-property",
        "Nearly five acres in Glen Arbor for under $2M — the land, not the house, is the asset. Confirm frontage versus view.",
        status="verify")
listing("higgins_lake", "6970 W Higgins Lake Dr — $1.45M", 1450000, 44.462, -84.762,
        "6BR/1.5BA, 2,150 sf on prime west-shore frontage",
        "https://www.lakehomes.com/michigan/higgins-lake",
        "Six bedrooms on the clearest big lake in the region for $1.45M. One and a half baths is the renovation line item; the water is the point.")
listing("higgins_lake", "303 Kenwood, Roscommon — $1.55M", 1550000, 44.485, -84.702,
        "5+ wooded acres with sunset lake views",
        "https://www.lakehomes.com/michigan/higgins-lake",
        "Five acres is enough for the whole cabin cluster — but confirm whether this is frontage or view before it goes further.",
        status="verify")
listing("higgins_lake", "West-shore 6BR, 100+ ft frontage — $1.9M", 1900000, 44.455, -84.748,
        "6BR/1.5BA with over 100 ft of prime Higgins frontage",
        "https://www.lakehomes.com/michigan/higgins-lake",
        "The top of the ordinary Higgins market: six bedrooms and a hundred feet of the clearest water in Michigan.")
listing("lake_charlevoix", "South Arm estate parcel — 3.4 ac / 277 ft", None, 45.212, -85.098,
        "3.4 ac with 277 ft of South Arm frontage",
        "https://northernmichiganescapes.com/lake-charlevoix-real-estate-the-definitive-2026-guide-to-waterfront-living",
        "The South Arm arbitrage: ~$2,450/ft median here against $7,000–$12,000/ft on the main basin. Price on application.",
        status="verify")
listing("walloon_lake", "651 South Shore Dr, Walloon — $7.7M", 7700000, 45.272, -84.942,
        "1.53 ac on the lake Hemingway wrote about",
        "https://www.lakehomes.com/michigan/walloon-lake",
        "Included to calibrate, not to buy: this is what archetype water costs in Michigan when the culture never sells. Walloon's twelve listings totalled $64.7M.")
listing("les_cheneaux", "Private island cottage, Snows Channel — $1.0M", 1000000, 45.998, -84.372,
        "Own private island, 575 ft of waterfront, 3BR historic cottage, 3-stall boathouse, turret, gazebo",
        "https://greatlakesandland.com/residentialeup.php",
        "WILDCARD: your own island with 575 feet of Lake Huron frontage and a three-stall boathouse for a million dollars. Season is short and the drive is seven hours; nothing else in this report is remotely like it.", new=True)
listing("les_cheneaux", "Cedarville historic cottage — $799K", 799000, 46.002, -84.362,
        "4BR (incl. annex), 2.5BA, boathouse, sandy beach + acreage across the street with pole barn",
        "https://greatlakesandland.com/residentialeup.php",
        "A cottage, an annex, a boathouse and a back lot with a barn for $799K — the assemblage is already done. Great Lakes water, Great Lakes weather.")
listing("les_cheneaux", "Hessel turnkey waterfront — $579K", 579000, 46.008, -84.418,
        "Fully furnished, refreshed spring 2026, transferable dock slip",
        "https://greatlakesandland.com/residentialeup.php",
        "Under $600K, furnished, with a dock slip that transfers. The cheapest way to test whether the group actually likes the Les Cheneaux.")
listing("cheboygan_county", "Cheboygan County lakefront inventory", None, 45.562, -84.672,
        "~1,000 ac of lakefront land listed countywide; average ask $376K",
        "https://www.land.com/Cheboygan-County-MI/lakefront-property/",
        "Cheboygan County land runs $12K–$17K/acre against Antrim's $18K–$28K. On Douglas, Burt and Mullett that gap is the whole strategy.",
        status="verify", lakeName="Cheboygan County", state="MI")
listing("hubbard_lake", "Hubbard Lake inventory", None, 44.812, -83.562,
        "Northeast Michigan's cheapest deep-water frontage; see Alcona County listings",
        "https://www.lakehomes.com/michigan/long-lake-alpena",
        "8,850 acres and 97 feet of depth at prices the Lake Michigan side hasn't seen in twenty years. Verify current inventory with an Alpena broker.",
        status="verify")
listing("mi_dnr_auction", "Michigan DNR surplus land auction 2026", None, 45.292, -83.542,
        "97 statewide parcels, 20+ over 40 ac; Alpena/Cheboygan/Presque Isle counties Aug 21",
        "https://www.wxyz.com/news/dnr-auctioning-off-more-than-100-properties-across-michigan-in-2026-heres-how-to-bid",
        "The state sells surplus land every summer, much of it in exactly this corner. Register for the 2027 cycle now — this is how you buy 40+ acres at land value.",
        status="verify", lakeName="Statewide (MI DNR)", state="MI")

# --- second-pass listings: the resort market, county by county -------------
listing("turtle_flambeau", "Donner's Bay Resort, Turtle–Flambeau — $1.57M", 1570000, 46.040, -90.280,
        "2974N Hiawatha Rd, Butternut; MLS 210365; 7,334 sf of buildings — 6–7 year-round cabin units (sources differ) + owner's home + 1,500 sf bar & grill; 74 years in one family",
        "https://www.shorewest.com/WI/Iron/Butternut/2974n-Hiawatha-Rd-Butternut-WI-54514/210365-GNMLS",
        "THE HEADLINE: a full cabin row, an owner's lodge and a licensed bar for under $1.6M on 12,942 acres of state Scenic Waters. The literal program, in budget, on genuinely wild water. Confirm the cabin count and lot size (1.31 vs 3.1 ac) with the broker; asking price is quoted at both $1.57M and $1.595M. Stained water is the only real objection.", new=True)
listing("butternut_lake_price", "Butternut Lake resort — $849K", 849000, 46.022, -90.492,
        "2.70 ac with on-site dining and multiple cabins, direct lake access",
        "https://www.commercialzip.com/resorts/wi/",
        "Under $850K for a cabin cluster and a commercial kitchen. Butternut is a modest 1,000-acre lake — buy this for the buildings and the licence, not the water.",
        lakeName="Butternut Lake (Price Co.)", state="WI")
listing("lake_delta_bayfield", "12770 Scenic Dr, Iron River — verify price", None, 46.552, -91.408,
        "Lake Delta resort: main lodge with operating bar & restaurant, attached 3BR home",
        "https://www.commercialzip.com/resorts/wi/",
        "A full commercial lodge with a bar and a residence attached, in Bayfield County where land runs a third of Vilas prices. Confirm current ask and cabin count.",
        status="verify", lakeName="Lake Delta (Bayfield Co.)", state="WI")
listing("houghton_lake", "127 & 128 Oneida Dr, Houghton Lake — $1.5M", 1500000, 44.322, -84.782,
        "Turnkey waterfront hospitality: log cabins, owner's home, sandy shoreline",
        "https://realmo.com/resorts/for-sale/mi/",
        "A second complete Houghton Lake cluster at $1.5M. Same verdict as the first: the program is right, the lake (20,000 shallow, busy acres) is not the archetype.")
listing("rockwell_lake", "Rockwell Lake Lodge, Luther — $6.2M", 6200000, 44.038, -85.688,
        "670 ac with a private lake and a 12,000 sf lodge",
        "https://realmo.com/resorts/for-sale/mi/",
        "Far past budget and included as the ceiling: 670 acres and your own lake, four hours out. Worth one calibration visit to see what a finished private-lake compound actually feels like.",
        lakeName="Rockwell Lake (private)", state="MI")
listing("millecoquins", "8928 N Boot Lake Rd, Manistique — $650K", 650000, 46.052, -86.352,
        "Furnished lodge sleeping up to 18, on 1.77 wooded acres",
        "https://realmo.com/resorts/for-sale/mi/",
        "Sleeps eighteen, furnished, for $650K. The cheapest way in this report to house all five couples under one roof on day one — then add cabins as budget allows.",
        lakeName="Boot Lake (Manistique)", state="MI")
listing("hamlin_lake", "Free Soil seven-cabin resort — $565K", 565000, 44.112, -86.212,
        "7 vintage cabins on 2.33 ac",
        "https://realmo.com/resorts/for-sale/mi/",
        "Seven standing cabins for $565K, forty minutes from Hamlin Lake. Not waterfront — but as a source of grandfathered buildings to relocate or to learn from, it is instructive.",
        lakeName="Free Soil, MI", state="MI")
listing("hubbard_lake", "Lupton lakefront resort — $950K", 950000, 44.632, -84.012,
        "5 ac; bar, commercial kitchen with pizza oven, guest docking, electric campsites",
        "https://realmo.com/resorts/for-sale/mi/",
        "Five waterfront acres, a commercial kitchen and guest docking under $1M in Ogemaw County. Ordinary water; extraordinary entitlements per dollar.",
        lakeName="Lupton, MI", state="MI")
listing("torch_lake", "Torch Lake motel & cabins — $1.6M", 1600000, 44.918, -85.352,
        "Two adjoining parcels; fully updated 14-unit motel near the sandbar",
        "https://www.traversenorth.com/property-search/waterfront-resorts-and-businesses.html",
        "Fourteen units of grandfathered density on the Midwest's most beautiful water. It is a motel by the sandbar, not a hushed compound — but the density is nearly impossible to replicate.")
listing("elk_lake", "Torch–Elk estate parcel — 7.5 ac", None, 44.928, -85.398,
        "Rare 7.5-ac estate parcel between Torch and Elk Lakes",
        "https://brickcorbett.com/neighborhoods/torch-lake",
        "Seven and a half acres in a corridor that essentially never releases land. Price on application; the acreage is the product.",
        status="verify")
listing("les_cheneaux", "1350 S Hill Island Rd, Cedarville — vacant 150 ft", None, 46.008, -84.338,
        "150 ft of vacant waterfront just east of Cedarville",
        "https://www.lakehouse.com/1350-s-hill-island-rd-cedarville-michigan-49719-p7047997.html",
        "Vacant Les Cheneaux frontage — rare, and the cheapest route into the archipelago if the group prefers to build. Confirm price and septic feasibility.",
        status="verify")
listing("grindstone", "Hayward — 16154 US Hwy 63 — $975K", 975000, 45.998, -91.462,
        "Hayward-area property via JMDS Properties",
        "https://www.jmdsproperties.com/wi-resorts-for-sale/",
        "A Hayward listing from the region's dedicated resort brokerage — worth a call regardless, because JMDS is the desk that sees Sawyer County cabin clusters before MLS does.",
        status="verify", lakeName="Hayward, WI", state="WI")
listing("chippewa_flowage", "Chippewa Flowage inventory — 17 live", None, 45.892, -91.108,
        "17 active Chippewa Flowage listings in Hayward this summer",
        "https://haywardlakes.com/lakes/chippewa-flowage/",
        "Seventeen live listings on 15,300 acres with 200 miles of shoreline that can never be developed. The deepest inventory-to-wildness ratio in the report.",
        status="verify")
listing("presque_isle_lake", "Presque Isle inventory — 30 live, avg $520K", None, 46.192, -89.712,
        "30 active Presque Isle lake listings; range $24.9K–$1.599M",
        "https://www.lakeplace.com/forsale/wi/presque-isle/",
        "Thirty live listings averaging $520K in the quietest township in Vilas County. This is where the assemblage strategy is most likely to actually work.",
        status="verify")
listing("manitowish_chain", "Manitowish Waters chain inventory", None, 46.128, -89.872,
        "Ten connected lakes; steady turnover of chain frontage",
        "https://www.lakeplace.com/forsale/wi-county/vilas/",
        "The chain trades more often than any archetype lake in Vilas County. If the group values cruising over clarity, start saved searches here.",
        status="verify")

# ---------------------------------------------------------------- excluded
EXCLUDED = {
  "Wisconsin — inside the 4-hour ring (too close to be the archetype)": [
    {"name": 'Lake Mendota / Monona (Madison)', "reason": '2:30; urban lakes with recurring blue-green algae closures'},
    {"name": 'Lake Koshkonong', "reason": '2:45; 10,460 ac and 7 ft deep — turbid throughout'},
    {"name": 'Lake Puckaway / Buffalo Lake', "reason": '3:00; marsh lakes, no clarity'},
    {"name": "Devil's Lake", "reason": '3:15; state park, no private frontage, no motors of consequence'},
    {"name": 'Lake Redstone / Dutch Hollow', "reason": '3:15; man-made recreational lakes on subdivided shorelines'},
    {"name": 'Turtle Lake / Long Lake (Waushara)', "reason": '3:15; small and heavily cottaged'},
    {"name": 'Lake Wazeecha / Nepco', "reason": '3:30; flowages in the central sands'},
    {"name": 'Shawano Lake', "reason": '3:45; 6,178 ac but only 39 ft, weedy and busy'},
    {"name": 'Lake Poygan / Winneconne / Butte des Morts', "reason": '3:15–3:30; the Winnebago pool — shallow and wind-driven'},
    {"name": 'Wazee Lake', "reason": '4:00; 30-ft Secchi in a flooded iron mine — spectacular water, county-owned shoreline, nothing to buy'},
    {"name": 'Rock Lake (Lake Mills)', "reason": '2:00; a wake-boat ordinance battleground and far too close'},
    {"name": 'Lake Ripley / Fox Lake', "reason": '2:15–2:30; small, mesotrophic, developed'},
    {"name": "Lake Geneva", "reason": "1:30 out; Chicago's own resort lake — marquee-busy, seven-figure frontage, zero hush"},
    {"name": "Delavan Lake", "reason": "1:45; heavily developed Walworth County, mesotrophic"},
    {"name": "Lake Beulah / Como / Powers", "reason": "Under 2 h; small, ringed with development"},
    {"name": "Elkhart Lake", "reason": "2:30; 292 ac, resort village, far under the size bar"},
    {"name": "Big Green Lake", "reason": "2:45; genuinely superb water (237 ft deep, Wisconsin's deepest) but inside the drive floor and increasingly trafficked"},
    {"name": "Lake Winnebago", "reason": "3:00; 137,700 ac and 21 ft deep — wind, algae, no clarity"},
    {"name": "Castle Rock & Petenwell Flowages", "reason": "3:15; drawdown reservoirs, turbid"},
    {"name": "Lake Wisconsin", "reason": "3:15; river flowage, muddy"},
    {"name": "Chain O'Lakes (IL)", "reason": "1:00; the busiest recreational water in the Midwest"},
    {"name": "Lake Wissota", "reason": "4:15 but a flowage with a state park and heavy traffic; water bar failed"},
    {"name": "Petenwell/Nekoosa corridor", "reason": "Paper-mill river system; excluded on water quality"},
    {"name": "Kangaroo Lake (Door Co.)", "reason": "4:30; 1,100 ac but only 12 ft deep and half is a nature preserve — no towsports"},
    {"name": "Door County generally", "reason": "No inland lake of consequence; the peninsula's water is Green Bay and Lake Michigan"}
  ],
  "Wisconsin — north of the ring, evaluated and excluded": [
    {"name": 'Three Lakes Chain (28 lakes with Eagle River)', "reason": 'The largest inland chain in the world and the busiest — a bar-to-bar boating culture, not a hushed one'},
    {"name": 'Lake Katherine / Bearskin (Oneida)', "reason": 'Under the size bar; pleasant, unremarkable'},
    {"name": 'Lake Nokomis', "reason": '2,800 ac flowage; stumps, drawdown, stained'},
    {"name": 'Pelican Lake (Forest Co.)', "reason": 'Not to be confused with the Oneida County lake of the same name; small and shallow'},
    {"name": 'Post Lake / Summit Lake', "reason": 'Flowage character, ordinary water'},
    {"name": 'Lake Alice / Lake Mohawksin', "reason": 'Wisconsin River impoundments at Tomahawk; turbid'},
    {"name": 'Chetek Chain', "reason": '5:15 and 3,800 ac, but shallow, agricultural watershed, algae history'},
    {"name": 'Red Cedar / Tainter / Menomin', "reason": 'Chronic phosphorus loading; among the worst clarity in the state'},
    {"name": 'Lake Holcombe / Cornell Flowage', "reason": 'Chippewa River impoundments; drawdown'},
    {"name": 'Long Lake (Chippewa Co.)', "reason": 'Good water but 3,290 ac of heavily-developed shoreline and a strong local wake-boat conflict'},
    {"name": 'Sand Lake / Bass Lake (Sawyer)', "reason": 'Under the size bar; nice satellites, not anchors'},
    {"name": 'Lac Sault Dore / Big Lake (Vilas)', "reason": 'Small Cisco-chain basins; covered by the chain entry'},
    {"name": 'Anvil Lake', "reason": '371 ac; superb Nicolet setting, far under the bar'},
    {"name": 'Lost Lake / Crystal Lake (Vilas NHAL)', "reason": 'Research lakes; essentially no private frontage exists'},
    {"name": 'Siskiwit Lake (Bayfield)', "reason": '320 ac; clear, tiny, and nearly all conserved'},
    {"name": 'Bony Lake / Ghost Lake', "reason": 'Under the size bar'},
    {"name": 'Lake Superior south shore (Ashland/Iron)', "reason": 'Not a towsports lake; the season and the weather rule it out'},
    {"name": 'Amnicon / Dowling (Douglas)', "reason": 'Small and stained'},
    {"name": 'Big Round / Bone Lake (Polk)', "reason": 'Twin Cities weekend water; wrong direction and busier than the Northwoods'},
    {"name": "Lake Owen's north basin", "reason": 'Note only: the north end carries most of the traffic — buy south'},
    {"name": 'Yellow Lake / Big McKenzie (Burnett)', "reason": '5:45; ordinary water on a developed shore'},
    {"name": "Grindstone's public landing bay", "reason": 'Note only: the one landing concentrates traffic — avoid frontage within sight of it'},
    {"name": "Lake Minocqua / Kawaguesaga", "reason": "Marquee-busy — town lake, bar-to-bar boat traffic, the Northwoods' Winnipesaukee"},
    {"name": "Eagle River Chain (28 lakes)", "reason": "Superb cruising, but the most trafficked chain in the north; several basins fail the clarity bar"},
    {"name": "Big Sand Lake (Vilas)", "reason": "1,427 ac but DNR classifies clarity low — fails the water bar outright"},
    {"name": "Big Bearskin Lake", "reason": "400 ac; far under the size bar despite an attractive three-cabin resort listing"},
    {"name": "Allequash / Papoose / White Sand", "reason": "411–750 ac NHAL lakes: archetype water, too small for five boats, essentially no private frontage"},
    {"name": "Lake Nokomis / Rice Reservoir", "reason": "Flowages; stumps and drawdown"},
    {"name": "Gile Flowage", "reason": "Dark, stained water; excluded on clarity"},
    {"name": "Lake Superior shoreline (Bayfield/Apostles)", "reason": "Great Lakes water — spectacular, but not a towsports lake and the season is short"},
    {"name": "Shell Lake", "reason": "2,585 ac, 36 ft; ordinary water, developed village shore, 5:45 out"},
    {"name": "Balsam / Bone / Deer Lakes (Polk Co.)", "reason": "Twin Cities weekend lakes — busy, and the wrong direction from Chicago"},
    {"name": "Big Butternut / Long Lake (Washburn)", "reason": "Mesotrophic, shallow"},
    {"name": "Lake Noquebay", "reason": "2,400 ac at 4:45 but only 51 ft, weedy, and no conserved shoreline"},
    {"name": "Wheeler Lake (Oconto Co.)", "reason": "27-ft Secchi — elite water — but far under 450 ac and effectively no market"},
    {"name": "Lac du Flambeau chain (as a purchase)", "reason": "Listed as a watch lake, not a recommendation: reservation land status makes non-member acquisition a specialist matter"},
    {"name": "Clam Lake / Ghost Lake", "reason": "Under the size bar; beautiful, unbuyable"},
    {"name": "Solberg / Butternut (Price Co.)", "reason": "Shallow and stained"}
  ],
  "Michigan — Lower Peninsula, evaluated and excluded": [
    {"name": 'Lake Missaukee', "reason": '1,880 ac, 25 ft; shallow, ringed by Lake City'},
    {"name": 'Lake St. Helen', "reason": '2,390 ac, 12 ft; shallow'},
    {"name": 'Sanford / Wixom / Secord (Tittabawassee)', "reason": 'Impoundments; two dams failed in 2020'},
    {"name": 'Lake Leelanau narrows', "reason": 'Note only: the narrows are no-wake and the South basin is shallow — buy North'},
    {"name": 'Elk Rapids / Bass Lake', "reason": 'Small satellites of Elk Lake; covered by the Elk entry'},
    {"name": 'Silver Lake (Oceana)', "reason": 'Dune-buggy destination adjacent; no hush'},
    {"name": 'Muskegon / Mona / White Lake', "reason": 'Drowned river mouths with industrial legacies'},
    {"name": 'Pentwater Lake / Manistee Lake', "reason": 'Commercial channels and marina traffic'},
    {"name": 'Lake Macatawa / Spring Lake', "reason": 'Under 3 h and fully suburban'},
    {"name": 'Lake Michigan shoreline generally', "reason": 'No protected water for towsports; compound frontage at these budgets does not exist'},
    {"name": 'Torch Lake south end', "reason": 'Note only: buy north of Alden or accept the sandbar'},
    {"name": 'Intermediate / Six Mile (Antrim)', "reason": 'Cheap chain access, notably less clear than the lakes below them'},
    {"name": 'Wycamp / Larks / Munro (Emmet)', "reason": 'Under the size bar'},
    {"name": "Burt Lake's Indian River corridor", "reason": 'Note only: the Inland Waterway channel concentrates traffic'},
    {"name": 'Van Etten / Cedar (Iosco)', "reason": 'Shallow, ordinary'},
    {"name": 'Au Sable impoundments (Foote, Cooke, Five Channels)', "reason": 'Drawdown reservoirs'},
    {"name": "Lake Margrethe's Camp Grayling shore", "reason": 'Note only: military training adjoins'},
    {"name": 'Crooked Lake (Lake Co.)', "reason": 'Program-match listing noted on the map; the lake itself is under the size bar'},
    {"name": 'Herendeene Lake', "reason": '40 ac and no-motor — listed for the resort on it, never as a lake recommendation'},
    {"name": 'Halfway Lake (Luce Co.)', "reason": 'Private and no-motor; same treatment'},
    {"name": "Houghton Lake", "reason": "20,044 ac but 21 ft max, weedy and busy — Michigan's largest inland lake fails the water bar"},
    {"name": "Otsego Lake", "reason": "1,972 ac, 23 ft max, 8 ft mean — too shallow"},
    {"name": "Long Lake (Alpena Co.)", "reason": "5,652 ac but 25 ft max; warms and colors by midsummer"},
    {"name": "Lake Mitchell & Lake Cadillac", "reason": "Town lakes with heavy traffic and mesotrophic water"},
    {"name": "Fletcher Pond", "reason": "Shallow flowage, famous fishery, no clarity"},
    {"name": "Lake Skegemog", "reason": "2,650 ac but shallow and largely a state natural area — no-wake over much of it"},
    {"name": "Little Glen Lake", "reason": "12 ft max; the shallow half of the Glen pair"},
    {"name": "Gun Lake / Gull Lake / Diamond Lake", "reason": "All under 3 h — inside the drive floor, and all heavily developed"},
    {"name": "Lake St. Clair / Saginaw Bay", "reason": "Great Lakes systems; wrong side of the state and wrong character"},
    {"name": "Muskegon / White / Pentwater Lakes", "reason": "Drowned river mouths — commercial channels, ordinary water"},
    {"name": "Torch Lake sandbar (as an address)", "reason": "The lake passes; the south sandbar's weekend anchorage is a hard no for this group's brief"},
    {"name": "Lake Charlevoix main basin", "reason": "$7,000–$12,000 per frontage foot; the South Arm is the only realistic entry"},
    {"name": "Higgins Lake south shore", "reason": "Two state parks and the ring road — buy north or east or not at all"},
    {"name": "Duck Lake (Benzie)", "reason": "Under the size bar and largely private-association controlled"},
    {"name": "Big Star / Bass / Round (Lake Co.)", "reason": "Inside 4:30 but small and ordinary"}
  ],
  "Michigan — Upper Peninsula & certification pass (MN, IN, IA, OH)": [
    {"name": 'Deer Lake (Ishpeming)', "reason": 'Historic mercury contamination; a fish-consumption advisory lake'},
    {"name": 'Lake Antoine / Norway Lake (Dickinson)', "reason": 'Under the size bar'},
    {"name": 'Michigamme Reservoir / Peavy Pond', "reason": 'Impoundments; stained and drawn down'},
    {"name": 'Keweenaw Bay / Huron Bay', "reason": 'Lake Superior water; no protected towsports'},
    {"name": 'Munuscong / St. Marys system', "reason": 'Listed as a watch: freighter channel, shallow, not the archetype'},
    {"name": 'Manistique Lakes (Big, North, South)', "reason": 'All under 25 ft; wind-driven'},
    {"name": 'Thunder / Grand Sable / Beaver Lake (Alger)', "reason": 'Inside Pictured Rocks or under the bar'},
    {"name": 'Tahquamenon / Whitefish Bay', "reason": 'Superior water and a short season'},
    {"name": "Gogebic's Bergland shore", "reason": 'Note only: the cheap frontage is also the windward shore'},
    {"name": 'Burntside / Ely lakes (MN)', "reason": '9:00+; the archetype, an hour past the ceiling'},
    {"name": 'Gunflint Trail lakes (MN)', "reason": '9:30+; BWCAW motor restrictions on most of them anyway'},
    {"name": 'Mille Lacs (MN)', "reason": '7:30 and 132,000 ac of 40-ft wind-driven water'},
    {"name": 'Whitefish Chain / Gull Lake (Brainerd MN)', "reason": '7:00–7:30; excellent water, but Twin Cities weekend traffic at Northwoods prices'},
    {"name": 'Lake Wawasee / Tippecanoe (IN)', "reason": "2:30; Indiana's best natural lakes, both heavily developed and inside the floor"},
    {"name": 'Lake Maxinkuckee / Barbee Chain (IN)', "reason": '2:15–2:45; same verdict'},
    {"name": 'Indian Lake / Grand Lake St. Marys (OH)', "reason": '5:00–5:30 but shallow reservoirs; Grand Lake has chronic toxic algae'},
    {"name": 'Okoboji / Spirit Lake (IA)', "reason": '6:30 and genuinely clear — but a dense resort town shoreline and no conserved frontage'},
    {"name": 'Clear Lake (IA)', "reason": '5:30; 3,600 ac and 15 ft deep, ringed by a town'},
    {"name": "Sylvania Wilderness lakes (Crooked, Clark, High)", "reason": "Certified: motors banned. The clearest water in the Midwest and completely unusable for this brief — visit, don't shop"},
    {"name": "Big Manistique Lake", "reason": "10,130 ac, 20 ft max; shallow and wind-driven"},
    {"name": "Indian Lake (Schoolcraft)", "reason": "8,400 ac, 18 ft max — same problem"},
    {"name": "Portage/Torch Lake (Keweenaw)", "reason": "~8:30 — over the drive ceiling; also a former stamp-sand Superfund shoreline"},
    {"name": "Lac La Belle / Copper Harbor", "reason": "8:45+; past the ceiling"},
    {"name": "Drummond Island", "reason": "~8:00 plus a ferry; the ferry, not the drive, is what breaks a five-couple weekend"},
    {"name": "Au Train Lake", "reason": "830 ac and shallow; lovely, under the bar"},
    {"name": "Bond Falls Flowage", "reason": "Reservoir with drawdown; stained"},
    {"name": "Lake Vermilion, Burntside, Gull (MN)", "reason": "Certified: 8:30–9:30 from Chicago — past the ceiling. Vermilion in particular is the archetype, one hour too far"},
    {"name": "Lake Minnetonka (MN)", "reason": "6:30 and reachable, but suburban Minneapolis — the opposite of the brief"},
    {"name": "Leech / Cass / Winnibigoshish (MN)", "reason": "7:30–8:30, shallow and wind-driven"},
    {"name": "Indiana, Ohio and Iowa generally", "reason": "Certified: no natural lake over 450 ac with archetype clarity and towsports inside the band. Indiana's Wawasee (2,618 ac) and Tippecanoe are the best of them — both under 3 h and heavily developed"},
    {"name": "Lake Erie / Lake Michigan shorelines", "reason": "Not lakes for this purpose — no protected water, no compound frontage at these budgets"}
  ],
}

# ------------------------------------------------------- link backfill ----
# Every lake carries at least one source or market link, matching the Northeast
# dataset. Only URLs that were actually opened during the sweep are used here:
# county/lake market pages, Wikipedia entries, and monitoring-program pages.
WIKI = {
 "big_muskellunge": "Big_Muskellunge_Lake", "presque_isle_lake": "Presque_Isle_Lake",
 "star_lake_vilas": "Star_Lake_(Vilas_County,_Wisconsin)", "plum_lake": "Plum_Lake_(Wisconsin)",
 "north_twin": "North_Twin_Lake_(Phelps,_Wisconsin)", "fence_lake": "Flambeau_Lake",
 "namekagon_lake": "Lake_Namakagon", "round_lake_sawyer": "Round_Lake_(Wisconsin)",
 "grindstone": "Grindstone_Lake_(Wisconsin)", "lco": "Lac_Courte_Oreilles",
 "turtle_flambeau": "Turtle-Flambeau_Flowage", "willow_flowage": "Willow_Reservoir",
 "tomahawk_lake": "Tomahawk_Lake_(Wisconsin)", "squirrel_lake": "Squirrel_Lake",
 "manitowish_chain": "Mamie_Lake_(Wisconsin)", "pike_lake_chain": "Gile_Flowage",
 "elk_lake": "Elk_Lake_(Michigan)", "big_glen": "Glen_Lake",
 "lake_leelanau": "Lake_Leelanau", "crystal_lake_benzie": "Crystal_Lake_(Benzie_County,_Michigan)",
 "long_lake_gt": "Long_Lake_(Grand_Traverse_County,_Michigan)",
 "burt_lake": "Burt_Lake", "mullett_lake": "Mullett_Lake",
 "douglas_lake": "Douglas_Lake_(Cheboygan_County,_Michigan)", "walloon_lake": "Walloon_Lake",
 "higgins_lake": "Higgins_Lake", "hubbard_lake": "Hubbard_Lake",
 "grand_lake_pi": "Grand_Lake_(Michigan)", "michigamme": "Lake_Michigamme",
 "lake_gogebic": "Lake_Gogebic", "lake_independence": "Lake_Independence_(Michigan)",
 "intermediate_lake": "Lake_Skegemog", "cisco_chain": "Mamie_Lake_(Wisconsin)",
}
MARKET = {
 # Wisconsin
 "vilas": ("Vilas County lake listings", "https://www.lakeplace.com/forsale/wi-county/vilas/"),
 "oneida": ("Oneida County lake listings", "https://www.lakeplace.com/forsale/wi-county/oneida/"),
 "sawyer": ("Sawyer County lake listings", "https://www.lakeplace.com/forsale/wi-county/sawyer/"),
 "bayfield": ("Bayfield County lake listings", "https://www.lakeplace.com/forsale/wi-county/bayfield/"),
 "winorth": ("Northern Wisconsin lake listings", "https://www.lakeplace.com/forsale/wi/northern/"),
 "eagleriver": ("Eagle River lake listings", "https://www.lakeplace.com/forsale/wi/eagle-river/"),
 "minocqua": ("Minocqua lake listings", "https://www.lakeplace.com/forsale/wi/minocqua/"),
 "landolakes": ("Land O'Lakes lake listings", "https://www.lakeplace.com/forsale/wi/land-o-lakes/"),
 "presqueisle": ("Presque Isle lake listings", "https://www.lakeplace.com/forsale/wi/presque-isle/"),
 "hayward": ("Hayward lake listings", "https://www.lakeplace.com/forsale/wi/hayward/"),
 "cable": ("Cable-area listings", "https://www.lakeplace.com/forsale/wi-county/bayfield/"),
 # Michigan
 "minw": ("Northern Michigan lakefront", "https://www.landsearch.com/lakefront/northern-michigan-mi"),
 "cheboygan": ("Cheboygan County lakefront", "https://www.land.com/Cheboygan-County-MI/lakefront-property/"),
 "charlevoix": ("Charlevoix County waterfront", "https://www.redfin.com/county/1362/MI/Charlevoix-County/waterfront"),
 "roscommon": ("Roscommon County waterfront", "https://www.redfin.com/county/1419/MI/Roscommon-County/waterfront"),
 "presqueislemi": ("Presque Isle County waterfront", "https://www.redfin.com/county/1418/MI/Presque-Isle-County/waterfront"),
 "kalkaska": ("Kalkaska County lakefront", "https://www.land.com/Kalkaska-County-MI/Lakefront-Property/"),
 "otsego": ("Otsego County lakefront", "https://www.land.com/Otsego-County-MI/lakefront-property/"),
 "mialpena": ("Alpena-area inland lakes", "https://www.visitalpena.com/quick-guide-inland-fishing-alpena/"),
 "miup": ("Upper Peninsula lakefront", "https://www.land.com/Upper-Peninsula-Michigan-Region/lakefront-property/"),
 "tomw": ("Tip of the Mitt Watershed Council", "https://watershedcouncil.org/"),
}
BUCKET = {
 # Wisconsin — Vilas
 "big_muskellunge": "vilas", "plum_lake": "vilas", "star_lake_vilas": "vilas",
 "north_twin": "vilas", "long_lake_phelps": "eagleriver", "lac_vieux_desert": "landolakes",
 "big_st_germain": "vilas", "big_arbor_vitae": "minocqua", "high_fishtrap": "landolakes",
 "big_portage": "vilas", "fence_lake": "vilas", "lac_du_lune": "landolakes",
 "dunn_lake": "presqueisle", "presque_isle_lake": "presqueisle", "black_oak": "landolakes",
 "manitowish_chain": "vilas", "kentuck_lake": "eagleriver", "little_st_germain": "vilas",
 "boulder_lake_vilas": "vilas",
 # Wisconsin — Oneida / Iron / Forest
 "willow_flowage": "oneida", "squirrel_lake": "oneida", "two_sisters": "oneida",
 "pelican_lake": "oneida", "sugar_camp_chain": "oneida", "pike_lake_chain": "winorth",
 "metonga": "winorth", "franklin_butternut": "eagleriver", "clear_lake_oneida": "oneida",
 "moen_chain": "oneida", "lake_lucerne": "winorth", "roberts_lake": "winorth",
 "noquebay": "winorth",
 # Wisconsin — Sawyer / Bayfield / Douglas
 "teal_lost_land": "sawyer", "spider_chain": "sawyer", "big_sissabagama": "sawyer",
 "nelson_lake": "hayward", "whitefish_sawyer": "sawyer", "namekagon_lake": "cable",
 "eau_claire_lakes": "bayfield", "nebagamon": "bayfield", "middle_eau_claire": "bayfield",
 "upper_st_croix": "bayfield",
 # Michigan — northwest / Antrim / Charlevoix / Emmet
 "lake_bellaire": "charlevoix", "intermediate_lake": "charlevoix",
 "lake_leelanau": "minw", "long_lake_gt": "minw", "platte_lake": "minw",
 "portage_lake_onekama": "minw", "hamlin_lake": "minw", "green_lake_mi": "minw",
 "bear_lake_manistee": "minw", "arbutus_chain": "kalkaska", "deer_lake_charlevoix": "charlevoix",
 "thumb_lake": "charlevoix", "crooked_pickerel": "tomw", "burt_lake": "cheboygan",
 "mullett_lake": "cheboygan", "black_lake_mi": "cheboygan", "paradise_lake": "cheboygan",
 # Michigan — central / northeast
 "lake_margrethe": "otsego", "grand_lake_pi": "presqueislemi", "hubbard_lake": "mialpena",
 "higgins_lake": "roscommon",
 # Michigan — Upper Peninsula
 "cisco_chain": "miup", "lake_gogebic": "miup", "michigamme": "miup",
 "lake_independence": "miup", "brevoort_lake": "miup", "chicaugon": "miup",
 "hagerman_lake": "miup", "fortune_lakes": "miup", "millecoquins": "miup",
 "munuscong": "miup",
}
for _l in L:
    _links = list(_l["links"])
    _w = WIKI.get(_l["key"])
    if _w and not any("wikipedia" in u for _, u in _links):
        _links.append(["Lake profile", "https://en.wikipedia.org/wiki/" + _w])
    _b = BUCKET.get(_l["key"])
    if _b:
        _t, _u = MARKET[_b]
        if not any(u == _u for _, u in _links):
            _links.append([_t, _u])
    if not _links:
        _links.append(list(MARKET["winorth" if _l["state"].startswith("WI") else "minw"]))
    _l["links"] = _links

# ---------------------------------------------------------------- rentals
# Summer rentals that can host eight couples: 7+ bedrooms (or a resort buyout),
# waterfront with a dock, Tier 1 lakes only (plus Torch by request). Every entry
# was re-read in a browser on 2 September 2026. July–August 2026 had already
# passed, so availability was checked for the same weeks of 2027, the nearest
# bookable summer. "direct" is the off-platform route; where a direct rate exists
# it is the one quoted.
RENTALS = []
def rental(lakeKey, name, lat, lon, bedrooms, baths, sleeps, rate, detail, fit, url=None, platform=None,
           direct=None, kind="single", status="active", rateUnit="/wk", rateNote=None, season=None, dock=None,
           lakeName=None, new=False):
    RENTALS.append(dict(lakeKey=lakeKey, name=name, lat=lat, lon=lon, bedrooms=bedrooms, baths=baths, sleeps=sleeps,
        rate=rate, rateUnit=rateUnit, rateNote=rateNote, detail=detail, fit=fit, url=url, platform=platform,
        direct=direct, kind=kind, status=status, season=season, dock=dock, lakeName=lakeName, new=new))

rental("turtle_flambeau", "Large Turtle Flambeau Flowage House — Mercer", 46.098, -90.098, 7, 2, 12, None,
       "7BR/2BA. VacationRenter — the only page for it that loads — lists 12 guests, not 18; game room, sauna, heated garage, pets allowed; private dock with direct lake access; 10/10 from 5 reviews. The price is hidden there; search results quote about $707–724 a night, roughly $5,000 a week.",
       "Still the one single-house answer on the wildest water in the report, but two things changed on inspection: the capacity is 12, not 18, and Flambeau Lodging's rate card shows it manages four small cabins, not this house — so there is no off-platform route yet. Ask the VRBO host directly for an owner's rate.",
       url="https://www.vacationrenter.com/p/402281532", platform="VRBO (via VacationRenter)",
       status="verify", rateNote="~$707–724/nt in search results (≈$5,000/wk); confirm on VRBO",
       season="Summer weekly; 2027 calendar not readable through VacationRenter", dock="private dock, direct lake access", new=True)

rental("grindstone", "Dancing Water Retreat — Northwoods Beach", 45.972, -91.282, 7, 3, 16, None,
       "7BR/3BA, sleeps 16; single-level ~3,000 sq ft with two kitchens, two living rooms, two decks and a fire pit; pets allowed; a dedicated slip on a shared pier, two swim platforms, two kayaks; public launch two miles away. The RentByOwner text was last written for summer 2022 (weekly Friday to Friday, Memorial Day to September; '$3,715' was that year's early-bird rate) and the owner's Houfy page is gone.",
       "Seven bedrooms on the clearest big water in Wisconsin — but the only live page is four years stale and the $3,715 figure is a 2022 early-bird number. Message the owner through the listing, or the haywardcabinwi Facebook page, for a current rate and the 2027 calendar before counting on it.",
       url="https://www.rentbyowner.com/property/dancing-water-retreat-lake-front-cabin-grindstone-lake-hayward-w-dock/HA-3212141509", platform="VRBO (via RentByOwner)",
       status="verify", rateNote="$3,715/wk was the 2022 early-bird rate; current rate not published",
       season="Weekly, Friday to Friday, Memorial Day to end of September (2022 text)", dock="dedicated slip on a shared pier; two swim platforms", new=True)

rental("round_lake_sawyer", "5RK Ranch Lakeside — three-house peninsula buyout", 45.988, -91.092, 15, 8, 34, None,
       "Three homes on a private 20-acre peninsula on Little Round Lake: the Lodge (6BR/2.5BA, sleeps 12), Lakeside #1 (5BR/3BA, sleeps 12, new in 2026) and the Peninsula Lakehouse (4BR/2.5BA, sleeps 10, remodeled 2026, with its own dock and ~240 ft of beach) — 15 bedrooms and 34 guests in all; private docks for boats to 25 ft, 2,000+ ft of sand shore, kayaks. The owner's site quoted Jul 10–17 2027 at $8,944 for the Lodge and $7,438 for the Peninsula, taxes and fees included; Lakeside #1 shows 'from $700 a night' but was not bookable that week. VRBO lists the Lodge alone at $11,146 plus taxes for the same week, with Jul 1–24 and Aug 5–31 2027 open on its calendar.",
       "The resort-buyout thesis as a rental, and the clearest case for booking direct in either report: the owner's site is roughly a fifth under VRBO before VRBO adds its fees. Twelve adults per house unless the host approves more; half down, the rest 60 days out. Email Reservations@5RKRanchLakeside.com or call (715) 569-8255 for a three-house week.",
       url="https://www.vrbo.com/4732042", platform="VRBO (Lodge only)", direct="https://5rkranchlakeside.com/",
       kind="buyout", status="active", rateNote="direct, all-in, Jul 2027: Lodge $8,944/wk + Peninsula $7,438/wk; Lakeside #1 from $700/nt",
       season="Year-round; Jul 1–24 and Aug 5–31 2027 open on the VRBO calendar", dock="private boat docks (to 25 ft), 2,000+ ft sand shore, swim area", new=True)

rental("lco", "Majestic Retreat + next-door cabin — book two for 24", 45.905, -91.345, None, None, 24, None,
       "The main cabin is 4BR/3BA and sleeps 10, not 12: 48-ft private dock, sandy beach, ping-pong, dogs by approval; 153 reviews at 9.6. The manager, Manage Cabins LLC, owns the cabins next door, each sleeping 12, and will book two together for 24 — the second cabin's bedroom count and dock are not published. Mid-June to August is Saturday-to-Saturday full weeks only. Jul 10–17 and Aug 7–14 2027 are already blocked on the main cabin.",
       "Two houses under one owner on 5,039 clear acres — the assemblage strategy, rented. It only works as a pair, so the first questions are the neighbour cabin's bedrooms and dock, and which 2027 Saturdays both are open.",
       url="https://www.vrbo.com/993215", platform="VRBO", kind="buyout", status="verify",
       rateNote="combined rate on request (Manage Cabins LLC)", dock="48-ft private dock + sandy beach on the main cabin; confirm the second", season="Mid-June to August: Saturday-to-Saturday full weeks only")

rental(None, "Hayward Lakefront — Spruce Chalet + neighbour, 21 only across three buildings", 46.018, -91.470, 7, 4, 21, None,
       "On Lake Hayward — the Namekagon River flowage beside the town — not Lac Courte Oreilles. Spruce Chalet itself is 3BR/2BA for eight; the 21-guest figure needs the neighbouring White Birch Retreat and its Big Pine Bunkhouse (VRBO 851715) as well: three buildings, seven bedrooms, four baths. Private docks, level frontage with a shallow sandy-weedy bottom and no beach. The base rate covers two guests plus per-guest charges; the combined group rate is quoted on request. 86 reviews at 9.6; the last two summers booked solid, and Jul 10–17 2027 is already blocked.",
       "Cheap and well run, but the wrong water and the wrong shape: a river flowage ten minutes from LCO, and eight couples split across three small buildings under two listings. Keep it as the budget fallback for a scouting weekend, not the group week.",
       url="https://www.vrbo.com/961246", platform="VRBO", status="verify",
       rateNote="Spruce Chalet from ~$241/nt for two; combined 21-guest rate on request", dock="private docks on Lake Hayward; level frontage, no beach", season="Year-round; summers book solid",
       lakeName="Lake Hayward (Namekagon flowage) — not LCO")

rental("crystal_lake_benzie", "Chimney Corners Resort — Woodsmere cottage (9 BR)", 44.658, -86.205, 9, 2, 18, 4760,
       "Woodsmere: a rustic nine-bedroom, two-bath, two-storey bluff cottage sleeping 18, with fireplace and shady deck. The resort (1935; the Rogers family, third generation) has 300 ft of sand beach, swim rafts, a boat hoist, tennis, kayaks and the Rocks Landing restaurant; open May 1 to Oct 31; no jet skis. 2026 rate sheet: $4,760 a week Saturday to Saturday from late June to late August ($4,060 in the shoulder weeks, $2,610 spring and fall); Bluffholm (5BR, sleeps 14) costs the same if the group outgrows one cottage. Deposit is a third of the rent, by check; 6% + 5% Michigan tax. 2027 rates and calendar are not posted — call 231-352-7522.",
       "Nine bedrooms on the clearest big lake in Michigan for about $600 a couple, with a restaurant on site and Bluffholm next door for fourteen more. Book direct — the resort itself says so (it is also on booking.com, which it cannot modify). Two baths for nine bedrooms is the trade.",
       direct="https://www.chimneycornersresort.com/", kind="buyout", status="active",
       season="Weekly Sat–Sat in peak (Jun 20–Sep 6); 2026 rates posted, 2027 by phone", dock="resort dock, swim rafts and boat hoist on 300 ft of beach", new=True)

rental("elk_lake", "Elk Lake Estate — 198 ft of frontage, sleeps 22", 44.932, -85.402, 6, 5, 22, None,
       "6BR (four en suite) plus a hall bath and a shower room; sleeps 22 in 14 beds (3 king, 3 queen, 4 full, 4 twin); 5,000 sq ft with two kitchens, three fridges, a game room, barrel sauna and sand volleyball; over an acre with 198 ft of private frontage, a 100-ft dock with a 10×20 over-water patio, 4,000-lb boat and pontoon lifts and two jet-ski moorings (mid-May to mid-September). Premier Host Jennifer, 91 reviews at 10. VRBO quoted Jun 12–19 2027 at $2,242 a night — $15,694 for the week before taxes — and every Saturday week in July and August 2027 is already blocked.",
       "Six bedrooms, not seven — but 14 beds and a 100-foot dock on Torch's quieter twin. It books a year ahead: the summer-2027 calendar is full, so this is a 2028 conversation or a cancellation watch.",
       url="https://www.vrbo.com/274728ha", platform="VRBO", status="verify",
       rateNote="≈$15,700/wk (June 2027 quote); Jul–Aug 2027 fully blocked", season="Summer weekly; summer 2027 already booked", dock="100-ft private dock with over-water patio, boat and pontoon lifts")

rental("elk_lake", "Elk Lake Retreat — five-cabin buyout, sleeps 38", 44.905, -85.425, 10, 5, 38, 16625,
       "Five near-identical two-bedroom, one-bath cabins (cabin 1 sleeps 6, cabins 2–5 sleep 8): ten bedrooms, 30 comfortably, 40 at most. A fenced, sandy-bottom private lakefront with playground, kayaks and paddleboards; the dock is for loading only (overnight mooring buoys instead); pontoons and jet skis from the owners' rental company are hoisted on site. Booking 2027 now at $475 a night per cabin plus tax with a three-night minimum — $2,375 a night, about $16,625 a week for all five. Each cabin is also on Airbnb.",
       "The whole-resort version on Elk Lake and the only Michigan option openly taking 2027 bookings. It is a bunkhouse village, not a lodge — ten small bedrooms and five baths — and boats sleep on buoys, not the dock. Book direct with Rachel (231-883-6009).",
       direct="https://elklakeretreat.com/", kind="buyout", status="active", rateUnit="/wk + tax",
       season="Booking 2027; three-night minimum; each cabin also on Airbnb", dock="loading dock + overnight mooring buoys; sandy-bottom private frontage")

rental("torch_lake", "Quiet Spirit — 8 BR lodge, Kewadin (northeast shore)", 45.020, -85.322, 8, 10, 19, None,
       "12,000 sq ft on four floors; eight themed bedrooms (six kings), eight full and two half baths with steam showers; hot tub, sauna, eight fireplaces, two kitchens, dining for 12, theatre, arcade and gym; dock with a 6,000-lb pontoon hoist (to 27 ft) and a mooring line. Registered rental VR 2026-21; 14 reviews at 9.6; rents to single families with a one-week minimum. As of 2 Sep 2026 no Saturday week in July or August 2027 could be booked on VRBO, and the by-owner page has been taken down.",
       "The most house on Torch Lake, on the quiet northeast shore an hour by boat from the sandbar — eight bedrooms with a bath each. The catches: 'single families only' is the owner's rule, the ~$14,300 weekly figure could not be re-priced because no 2027 summer dates are open, and the only route is the VRBO host, Rich Charbonneau.",
       url="https://www.vrbo.com/2240917", platform="VRBO", status="verify",
       rateNote="~$14,300/wk quoted earlier; no Jul–Aug 2027 weeks open on VRBO",
       season="Weekly, one-week minimum; single families only; summer 2027 not bookable yet", dock="private dock with 6,000-lb pontoon hoist", new=True)

rental("torch_lake", "Noble Spirit — 7 BR, Kewadin", 45.005, -85.338, 7, 9, 19, None,
       "7,000 sq ft; seven themed bedrooms (five kings), eight full and one half baths with jetted tubs and bidets; sleeps 19; arcade (four multicades, three pinballs), HD theatre, gym, six fireplaces, two kitchens; dock with a 6,000-lb pontoon hoist and a mooring line. Registered rental VR 2026-17; 22 reviews at 9.6; minimum age 26. Same status as Quiet Spirit: no July–August 2027 Saturday weeks bookable on VRBO as of 2 Sep 2026.",
       "Same owners as Quiet Spirit, a size down. Seven bedrooms and nine baths is exactly the brief; the arcade is the reason the group will not want to leave. Ask the host whether the 2027 summer calendar is closed or simply not released.",
       url="https://www.vrbo.com/2371320", platform="VRBO", status="verify",
       rateNote="~$13,200/wk quoted earlier; no Jul–Aug 2027 weeks open on VRBO", season="Weekly, one-week minimum; summer 2027 not bookable yet", dock="private dock with pontoon hoist")

rental("torch_lake", "Torch Lake sandbar — no 7+ BR rental found", 44.872, -85.300, 4, 2.5, 8, None,
       "The largest waterfront rental found on the south-end sandbar is 'Torch Cabin' (VRBO 2322802): 4BR (king, queen, two doubles, a twin bunk), two full and one half baths, sleeps 8, dock; Premier Host Anja Stoldt, 60 reviews. Jul 10–17 2027 is already blocked. Nothing at 7+ bedrooms surfaced in Alden, Rapid City or Bellaire.",
       "Honest answer on the sandbar: it is a small-cottage shoreline. Eight couples do the sandbar by boat from Quiet Spirit or Noble Spirit, not by renting on it.",
       url="https://www.vrbo.com/2322802", platform="VRBO", status="verify", rateNote="largest found: 4 BR", dock="seasonal dock, mooring buoy", lakeName="Torch Lake (south sandbar)")

DATA_RENTALS = RENTALS

DATA = dict(refs=REFS, lakes=L, listings=LI, rentals=DATA_RENTALS, excluded=EXCLUDED, updated=UPDATED)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "midwest_map_data.json")
with open(out, "w") as f:
    json.dump(DATA, f, indent=1, ensure_ascii=False)
    f.write("\n")

n_ex = sum(len(v) for v in EXCLUDED.values())
print(f"wrote {os.path.normpath(out)}: {len(L)} lakes, {len(LI)} listings, {len(RENTALS)} rentals, {n_ex} excluded, {len(REFS)} refs")
