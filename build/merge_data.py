#!/usr/bin/env python3
"""Merge sweep results with existing site data into map_data.json."""
import json, math

def load(p):
    with open(p) as f: return json.load(f)

nh, me, ny, vt = load("sweep/nh.json"), load("sweep/me.json"), load("sweep/ny.json"), load("sweep/vt.json")
spec = load("sweep/spec.json")

REFS = [
 {"key":"nyc","cls":"ref","shape":"star","name":"New York City","state":"NY","lat":40.755,"lon":-73.984,"drive":"","acres":None,"blurb":"Start of every drive estimate (Midtown).","links":[]},
 {"key":"squam","cls":"ref","shape":"ring","name":"Squam Lake (the archetype)","state":"NH","lat":43.79,"lon":-71.55,"drive":"~4:50","acres":6791,"blurb":"The reference point. ≤$2.5M buys no usable compound here — but see the live 159 Rt-113 assemblage listings.","links":[["Squam Lakes Conservation Society","https://www.squamslandtrust.org/map-of-conserved-land/"]]},
]

EXISTING = [
 {"key":"kezar","name":"Kezar Lake","state":"ME","lat":44.20,"lon":-70.89,"acres":2665,"drive":"~5:35","tier":"t1","score":9.5,"blurb":"The truest Squam analog: oligotrophic, White Mtn backdrop, hushed. Thin market — and a live 16.6-ac Narrows parcel just surfaced.","links":[["Watershed assn","https://kezarwatershed.org/kezar-lake"],["Kezar Realty","https://www.kezarrealty.com/kezar-lake/kezar-lake-homes/"]]},
 {"key":"seymour","name":"Seymour Lake","state":"VT","lat":44.933,"lon":-71.956,"acres":1777,"drive":"~6:15","tier":"t1","score":9,"blurb":"Best odds of executing: oligotrophic, invasive-free, wakesports zone, compound-grade comps ~$1.25M.","links":[["Lake assn","https://seymourlake.org/water-quality-measurement/"],["Listings","https://www.lakehomes.com/vermont/lake-seymour"]]},
 {"key":"raquette","name":"Raquette Lake","state":"NY","lat":43.845,"lon":-74.655,"acres":5000,"drive":"~5:20","tier":"t1","score":8.5,"blurb":"Great Camp birthplace; wild bays, attainable entries, APA levers for a cabin cluster.","links":[["Listings","https://www.lakehouse.com/raquette-lake-new-york-lake-homes-for-sale-b4047.html"]]},
 {"key":"bigmoose","name":"Big Moose Lake","state":"NY","lat":43.822,"lon":-74.858,"acres":1286,"drive":"~5:15","tier":"t1","score":9,"blurb":"Dark-timber old camps, near-zero ramp traffic. Two live listings: $1.2M boat-access and $1.1M road-access.","links":[["Timm Associates","https://www.timmassociates.com/community/big-moose-twitchell-lake/"]]},
 {"key":"merrymeeting","name":"Merrymeeting Lake","state":"NH","lat":43.466,"lon":-71.125,"acres":1150,"drive":"~4:45","tier":"t2","score":8.5,"blurb":"Spring-fed clear, no big public ramp — quietest archetype water near the city.","links":[["Listings","https://www.lakehomes.com/new-hampshire/merrymeeting-lake"]]},
 {"key":"greateast","name":"Great East Lake","state":"NH/ME","lat":43.642,"lon":-70.975,"acres":1700,"drive":"~4:50","tier":"t2","score":8.5,"blurb":"Secchi ~10 m. Inventory currently dry (one pending camp) — set alerts; cyanobacteria counts are the watch item.","links":[["GELIA monitoring","https://www.greateastlake.org/water-quality-monitoring/"],["Listings","https://www.lakesregionmenh.com/great-east-nh/"]]},
 {"key":"caspian","name":"Caspian Lake","state":"VT","lat":44.594,"lon":-72.303,"acres":790,"drive":"~5:45","tier":"t2","score":8.5,"blurb":"Greensboro — the NEK's Squam-in-miniature. A rare $2.25M north-shore estate parcel is live now.","links":[["Jim Campbell RE","https://www.jimcampbellrealestate.com/lakes/caspian-lake/"]]},
 {"key":"maidstone","name":"Maidstone Lake","state":"VT","lat":44.640,"lon":-71.648,"acres":756,"drive":"~6:15","tier":"t2","score":8,"blurb":"State-forest ring, loons, one dirt road — the most Trout-Lake-WI place in New England.","links":[["Maidstone State Forest","https://fpr.vermont.gov/maidstone-state-forest"]]},
 {"key":"usaranac","name":"Upper Saranac Lake","state":"NY","lat":44.27,"lon":-74.27,"acres":5000,"drive":"~5:15","tier":"t2","score":8,"blurb":"The NY Squam. ≤$2.5M buys one camp, not a compound — tour Panther Cove to calibrate.","links":[["Milfoil program","https://usfoundation.net/programs/milfoil-control/"]]},
 {"key":"chateaugay","name":"Upper Chateaugay Lake","state":"NY","lat":44.755,"lon":-73.932,"acres":2300,"drive":"~5:50","tier":"t2","score":8,"blurb":"The value arbitrage: clear, cold, sleepy. $599K buys an 868-ft private cove.","links":[["LaPoint Realty","https://lapointrealty.com/chateaugay-lake/"]]},
 {"key":"piseco","name":"Piseco Lake","state":"NY","lat":43.453,"lon":-74.543,"acres":2900,"drive":"~4:00","tier":"t2","score":7.5,"blurb":"Best drive-to-wildness ratio on the list; Forest Preserve ring, thin inventory.","links":[["Area guide","https://www.adirondack.net/business/piseco-lake-12504/"]]},
 {"key":"webb","name":"Webb Lake","state":"ME","lat":44.688,"lon":-70.457,"acres":2146,"drive":"~6:20","tier":"t2","score":7.5,"blurb":"Mount Blue / Tumbledown wildness; the build-from-scratch canvas ($985K parcel live).","links":[["Webb Lake listings","https://www.land.com/Webb-Lake-in-ME/lakefront-property/"]]},
 {"key":"newfound","name":"Newfound Lake","state":"NH","lat":43.658,"lon":-71.792,"acres":4451,"drive":"~4:40","tier":"t2","score":8.5,"blurb":"PROMOTED to Tier 2: world-class clarity and now real inventory — the $2.6M ten-room Kelby lodge plus $799K–$1.5M owned waterfront. Watch the spiny water flea.","links":[["NLRA water quality","https://www.newfoundlake.org/water-quality/"]]},
 {"key":"conway","name":"Conway Lake","state":"NH","lat":43.942,"lon":-71.073,"acres":1298,"drive":"~5:20","tier":"watch","score":7.5,"blurb":"Sleeper: conserved eastern shore, tiny launch, cheaper than its neighbors; $1.25M camp live.","links":[["Overview","https://en.wikipedia.org/wiki/Conway_Lake"]]},
 {"key":"thompson","name":"Thompson Lake","state":"ME","lat":44.028,"lon":-70.489,"acres":4419,"drive":"~5:20","tier":"watch","score":7.8,"blurb":"Archetype water, frontage drought continues — only access-rights homes live; set an alert.","links":[["TLEA report","https://thompsonlake.org/wp-content/uploads/Thompson-Lake-2024-Water-Quality-Report.pdf"]]},
 {"key":"embden","name":"Embden Pond","state":"ME","lat":44.952,"lon":-69.958,"acres":1565,"drive":"~6:25","tier":"watch","score":7.4,"blurb":"Cheapest clear water found: camps in the $400Ks; two live sub-$450K options.","links":[["LandWatch Embden","https://www.landwatch.com/maine-land-for-sale/embden/waterfront-property"]]},
 {"key":"echo","name":"Echo Lake (Charleston)","state":"VT","lat":44.845,"lon":-71.940,"acres":547,"drive":"~6:15","tier":"watch","score":7.9,"blurb":"Clearest Secchi in the VT dataset (8.8 m); pair with Seymour. Current entry pending.","links":[["Lake assn","https://www.echolakeassociation.net/about-us/echo-lake/"]]},
 {"key":"willoughby","name":"Lake Willoughby","state":"VT","lat":44.728,"lon":-72.057,"acres":1734,"drive":"~6:00","tier":"watch","score":7.5,"blurb":"Spectacular fjord; frontage scarce — but the live combo ($929K 8BR waterfront lodge + LaCross parcels) is Vermont's best compound math.","links":[["Overview","https://farmandforest.com/willoughby-lake/"]]},
 {"key":"bonaparte","name":"Lake Bonaparte","state":"NY","lat":44.153,"lon":-75.363,"acres":1300,"drive":"~5:45","tier":"watch","score":7.3,"blurb":"Islands, granite, generational camps; compound money goes far.","links":[["Listings","https://www.lakehomes.com/new-york/lake-bonaparte"]]},
 {"key":"chazy","name":"Chazy Lake","state":"NY","lat":44.755,"lon":-73.826,"acres":1807,"drive":"~5:00","tier":"watch","score":7.4,"blurb":"Clear, cold, sparse under Lyon Mtn; $265K entry live now.","links":[["DEC page","https://dec.ny.gov/places/chazy-lake"]]},
 {"key":"averill","name":"Great Averill Pond","state":"VT","lat":44.993,"lon":-71.696,"acres":830,"drive":"~6:30","tier":"watch","score":7.6,"blurb":"The NEK's best-kept secret — oligotrophic, forested, near-zero market (Quimby Country sold).","links":[["VT public-waters rules","https://dec.vermont.gov/watershed/lakes-ponds/vermont-use-public-waters-rules"]]},
 {"key":"mooselook","name":"Mooselookmeguntic (edge)","state":"ME","lat":44.883,"lon":-70.800,"acres":16320,"drive":"~6:45–7:15","tier":"watch","score":7.8,"blurb":"Truest Trout Lake analog east of Wisconsin — 45 min over the drive line. Remarkable value.","links":[["Listings","https://www.lakehouse.com/mooselookmeguntic-lake-maine-lake-homes-for-sale-b1356.html"]]},
 {"key":"rangeley","name":"Rangeley Lake (edge)","state":"ME","lat":44.935,"lon":-70.680,"acres":6000,"drive":"~7:00","tier":"watch","score":7.2,"blurb":"Classic ski-camp town, over the drive cap; only if the rule softens.","links":[["Morton & Furbish","https://www.morton-furbish.com/waterfront-listings/rangeley-lake/"]]},
]

EXISTING_LISTINGS = [
 {"lakeKey":"webb","name":"Webb Lake build parcel — $985K","price":985000,"lat":44.664,"lon":-70.432,"detail":"43.9 ac · 596 ft frontage · no structures","status":"active","url":"https://www.landwatch.com/franklin-county-maine-timberland-property-for-sale/pid/423813299","fit":"Build the sketch from scratch; lodge near shore, cabins beyond the 250-ft zone"},
 {"lakeKey":"bigmoose","name":"215 Judson Rd — $1.2M","price":1200000,"lat":43.816,"lon":-74.832,"detail":"10.4 ac · 200 ft · 4BR + bunkhouse · boat-access-only","status":"active","url":"https://adkpp.com/properties/215-judson-road-eagle-bay-ny-13331/","fit":"Archetype lake; logistics are the debate"},
 {"lakeKey":"willoughby","name":"LaCross Ln compound — $1.2M","price":1200000,"lat":44.705,"lon":-72.043,"detail":"97.7 ac · 4 dwellings + barns · rehab needed","status":"active","url":"https://www.lakehomes.com/vermont/lake-willoughby/283-318-319-320-lacross-lane-westmore-vt-05860-lhrmls-04187776","fit":"Lake VIEWS confirmed, frontage NOT — pair with a frontage parcel below"},
 {"lakeKey":"raquette","name":"Two-cabin property — $649K","price":649000,"lat":43.812,"lon":-74.662,"detail":"4BR/4BA across 2 newer cabins, Raquette Shores","status":"active","url":"https://www.lakehouse.com/raquette-lake-new-york-lake-homes-for-sale-b4047.html","fit":"A compound seed on the Great Camp lake"},
 {"lakeKey":"chateaugay","name":"Private cove — $599K","price":599000,"lat":44.771,"lon":-73.947,"detail":"4.3 ac · 868 ft frontage · land","status":"active","url":"https://lapointrealty.com/homes-for-sale-2/","fit":"Pair with an adjacent camp for a sub-$2M compound"},
 {"lakeKey":"usaranac","name":"Pine Point Lodge, U. St. Regis — $2.6M","price":2600000,"lat":44.418,"lon":-74.263,"detail":"12.75 ac · 1,330 ft · 1904 Tiffany lodge + 2 boathouses","status":"active","url":"https://www.adirondackestates.com/properties/53-saint-regis-carry-road-lake-clear-ny-12945/","fit":"Turnkey stretch; guideboat culture, small lake for wake sports"},
 {"lakeKey":"tupper","name":"Hamlin Bay parcels — $1.38M","price":1380000,"lat":44.205,"lon":-74.505,"detail":"35.8 ac · 1,535 ft frontage · two parcels","status":"active","url":"https://www.landwatch.com/new-york-land-for-sale/lakefront-property","fit":"Passes APA math for lodge + 5 cabins outright; tea-stained water"},
 {"lakeKey":"sacandaga_great","name":"Six-cabin colony, Gt. Sacandaga — $2.5M","price":2500000,"lat":43.330,"lon":-73.885,"detail":"2.92 ac · 6 winterized 2BR cabins · ~3:15 drive","status":"active","url":"https://www.adirondack.net/real-estate/mls/details/224-north-shore-road-202618350/","fit":"Turnkey program, wrong-culture lake — the program-first fallback"},
 {"lakeKey":"usaranac","name":"Panther Cove — $3.7M (benchmark)","price":3700000,"lat":44.245,"lon":-74.335,"detail":"16.5 ac · 482 ft · 4 dwellings + 2 boathouses","status":"active","url":"https://adkpp.com/properties/144-county-rd-45panther-mt-road-tupper-lake-ny-12986/","fit":"Over budget — tour it to calibrate what done looks like"},
 {"lakeKey":"mooselook","name":"657 Bemis Rd — $725K (edge)","price":725000,"lat":44.858,"lon":-70.752,"detail":"53.9 ac · house + new barn · ~7 h drive","status":"active","url":"https://www.lakehouse.com/657-bemis-rd-rangeley-plt-maine-04970-p7592484.html","fit":"The over-the-line bargain; verify exact frontage"},
]

lakes = []
for L in EXISTING:
    L["cls"] = L["tier"]; L["new"] = False; lakes.append(L)
for src in (nh, me, ny, vt):
    for L in src["lakes"]:
        L["cls"] = L["tier"]; L["new"] = True; lakes.append(L)

listings = []
for x in EXISTING_LISTINGS:
    x["cls"] = "listing"; x["new"] = False; listings.append(x)
for src in (nh, me, ny, vt, spec):
    for x in src["listings"]:
        x["cls"] = "listing"; x["new"] = True; listings.append(x)

# sanity: bounds
bad = [p["name"] for p in lakes + listings if not (39.9 <= p["lat"] <= 45.96 and -77.7 <= p["lon"] <= -67.5)]
if bad: print("OUT OF BOUNDS:", bad)

# de-collide: jitter points sharing rounded coords
seen = {}
for p in lakes + listings + REFS:
    k = (round(p["lat"], 3), round(p["lon"], 3))
    n = seen.get(k, 0)
    if n:
        ang = 0.9 * n
        p["lat"] += 0.006 * math.sin(ang) * (1 + n * 0.25)
        p["lon"] += 0.008 * math.cos(ang) * (1 + n * 0.25)
    seen[k] = n + 1

excluded = {"New Hampshire": nh["excluded"], "Maine": me["excluded"], "New York": ny["excluded"],
            "Vermont + southern New England / PA / NJ / MD": vt["excluded"]}

out = {"refs": REFS, "lakes": lakes, "listings": listings, "excluded": excluded,
       "updated": "August 18, 2026"}
with open("map_data.json", "w") as f: json.dump(out, f, indent=1)

t1 = [l["name"] for l in lakes if l["cls"] == "t1"]
print("lakes:", len(lakes), "| t1:", len(t1), t1)
print("t2:", sum(1 for l in lakes if l["cls"] == "t2"), "| watch:", sum(1 for l in lakes if l["cls"] == "watch"))
print("listings:", len(listings), "| excluded:", sum(len(v) for v in excluded.values()))
