const fs = require("fs");
const topojson = require("topojson-client");
const us = require("./node_modules/us-atlas/states-10m.json");
const { geoTransverseMercator, geoPath, geoCircle } = require("d3-geo");

const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const fmtAc = a => a ? a.toLocaleString("en-US") : "";

// =============================================================== regions ===
// Each region is a self-contained sweep: its own dataset, basemap window,
// origin city, drive-time rings and written briefing. Everything below this
// block is shared machinery.

const NORTHEAST = {
  id: "ne",
  tab: "Northeast",
  tabNote: "from NYC · ≤6.5 h",
  h1: "Finding Your Squam",
  data: "../data/map_data.json",
  briefing: "briefing_content.html",
  updated: "August 18, 2026",
  states: ["23","33","50","36","25","09","44","34","42","10","24"],
  W: 700, H: 780,
  rotate: 72.6,
  frame: [
    [-77.6, 39.9], [-67.6, 39.9], [-67.6, 45.95], [-77.6, 45.95],
    [-72.6, 39.9], [-72.6, 45.95], [-77.6, 42.9], [-67.6, 42.9],
  ],
  origin: [-73.984, 40.755],
  labelBearing: 46,
  rings: [
    { mi: 220, label: "≈ 4 h drive" }, { mi: 270, label: "≈ 5 h" }, { mi: 350, label: "≈ 6.5 h" },
  ],
  refChipLabel: "NYC ★ &amp; Squam ◎",
  listingsGroupNote: "snapshot Aug 18, 2026",
  labels: {
    kezar: { dx: 0, dy: -13, anchor: "middle" }, seymour: { dx: 0, dy: -13, anchor: "middle" },
    raquette: { dx: 11, dy: -8, anchor: "start" }, bigmoose: { dx: -11, dy: 14, anchor: "end" },
    silver_madison: { dx: 11, dy: 4, anchor: "start" }, parker_pond: { dx: 11, dy: -6, anchor: "start" },
    echo_lake_fayette: { dx: 11, dy: 13, anchor: "start" },
    squam: { dx: -13, dy: 4, anchor: "end" }, nyc: { dx: 0, dy: 19, anchor: "middle" },
  },
  sub: (s) => `${s.nLakes} qualifying lakes across four states · ${s.nList} live listings · full-region sweep updated August 18, 2026 · click any marker to pin its info and links`,
  subBrief: (s) => `The written briefing, with the complete sweep appendix: ${s.nLakes} passing lakes and ${s.nExcl} evaluated and excluded, with reasons`,
  legendNote: "dashed rings ≈ drive-time bands (rough) · scroll to zoom, drag to pan · search filters both map and list",
  searchPlaceholder: (s) => `Search ${s.nLakes} lakes + ${s.nList} listings — try a lake, state, or price…`,
  footer: "Companion to the full briefing (second tab). Listing status changes fast — re-confirm with brokers before touring. Drive times are non-peak estimates from Midtown; rings are straight-line approximations, not isochrones. Trout Lake, WI — your other archetype — is off-map at ~17 hours' drive; its buildable stand-ins here are the state-forest-ringed lakes (Maidstone, Webb, Piseco, Mooselookmeguntic, Richardson). For the Wisconsin/Michigan version of this search, see the Midwest tab.",
  briefNote: '<p class="fine" style="margin-top:4px">Updated August 18, 2026: the appendix below adds the full-region sweep — every qualifying lake and live listing in the Northeast. The original July analysis and recommendations stand.</p>',
  briefNoteAnchor: '<h2 style="margin-top:6px">Executive summary</h2>',
  appendixTitle: "Appendix — the full-region sweep (updated August 18, 2026)",
  appendixIntro: (s) => `Four research passes evaluated every named lake of consequence in NH, ME (west/central/midcoast), NY, and VT — plus a certification pass over MA, CT, RI, PA, NJ and MD — against the archetype bar: ≤~6.5 h from Midtown, towsports legal and practical, ~450+ acres (rare exceptions justified), documented clear water, forested/quiet character, and private frontage that actually trades. <strong>${s.nLakes} lakes passed</strong> (${s.t1} Tier 1, ${s.t2} Tier 2, ${s.watch} watchlist/edge) and <strong>${s.nExcl} were evaluated and excluded</strong> with reasons below. The listings snapshot holds ${s.nList} live opportunities; the five most decision-relevant were re-verified individually on Aug 17–18 (Willoughby's $929K house-plus-four-cabins, the Winnecook lodge-and-cabins, the Tupper colony, Kezar's Blackberry Hill, Parker Pond's Dolloff estate). A note on honesty: a few standout <em>program</em> matches sit on lakes that failed the <em>water</em> bar (Unity Pond's lodge-and-six-cabins, Bomoseen's 60-acre golf-course parcel, Rainbow Lake's twin-lodge camp) — they're included with explicit caveats, never as recommendations.`,
  appendixFine: `New Hampshire nuance worth knowing: NH's "ski craft" bans are jet-ski bans — waterskiing behind boats remains legal on every passed lake, so PWC-banned lakes (Silver, Wentworth, Pleasant, Goose, Nubanusit, Waukewan) are actually the quietest Squam-like water in the state. Newfound Lake was promoted watch→Tier 2 on live-inventory evidence. Maine's four clarity standouts (Parker, Echo/Fayette, Peabody, Porter) all sit in the under-loved 30-Mile-River / western foothills belt — the sweep's biggest discovery.`,
  appendixSources: `Sources per lake are linked from the map popups (state monitoring programs: NHDES VLAP, Lakes of Maine / LEA / 30MRWA / 7 Lakes Alliance, NY DEC CSLAP/ALAP, VT DEC Lay Monitoring; motor rules: NH Marine Patrol restricted-waters list, Maine CMR ch.13 §07, NYS Navigation Law defaults, VT Use of Public Waters rules). Listing statuses move in days — re-confirm before touring.`,
};

const MIDWEST = {
  id: "mw",
  tab: "Midwest",
  tabNote: "from Chicago · 4–8 h",
  h1: "Finding Your Trout Lake",
  data: "../data/midwest_map_data.json",
  briefing: "midwest_briefing_content.html",
  updated: "September 1, 2026",
  states: ["55","26","17","18","27","19","39","21"],
  W: 780, H: 668,
  rotate: 88.2,
  frame: [
    [-94.5, 41.0], [-82.0, 41.0], [-82.0, 48.6], [-94.5, 48.6],
    [-88.2, 41.0], [-88.2, 48.6], [-94.5, 44.8], [-82.0, 44.8],
  ],
  origin: [-87.628, 41.882],
  labelBearing: 330,
  rings: [
    { mi: 260, label: "≈ 4 h drive" }, { mi: 390, label: "≈ 6 h" }, { mi: 520, label: "≈ 8 h" },
  ],
  refChipLabel: "Chicago ★ &amp; Trout ◎",
  listingsGroupNote: "snapshot Sep 1, 2026",
  labels: {
    chicago: { dx: 0, dy: 19, anchor: "middle" },
    trout: { dx: 0, dy: -13, anchor: "middle" },
    lake_owen: { dx: -12, dy: -6, anchor: "end" },
    grindstone: { dx: -12, dy: 17, anchor: "end" },
    tomahawk_lake: { dx: 0, dy: 17, anchor: "middle" },
    metonga: { dx: 11, dy: 13, anchor: "start" },
    chicaugon: { dx: 11, dy: -8, anchor: "start" },
    les_cheneaux: { dx: 11, dy: 11, anchor: "start" },
    walloon_lake: { dx: 11, dy: -9, anchor: "start" },
    elk_lake: { dx: 11, dy: -10, anchor: "start" },
    big_glen: { dx: -12, dy: -3, anchor: "end" },
    crystal_lake_benzie: { dx: -12, dy: 13, anchor: "end" },
    higgins_lake: { dx: 11, dy: 11, anchor: "start" },
    hubbard_lake: { dx: 11, dy: 4, anchor: "start" },
  },
  labelText: {
    les_cheneaux: "Les Cheneaux",
    crystal_lake_benzie: "Crystal Lake",
    tomahawk_lake: "Lake Tomahawk",
  },
  sub: (s) => `${s.nLakes} qualifying lakes in Wisconsin & Michigan · ${s.nList} live listings · 4–8 hours from the Loop · sweep updated September 1, 2026 · click any marker to pin its info and links`,
  subBrief: (s) => `The written briefing, with the complete sweep appendix: ${s.nLakes} passing lakes and ${s.nExcl} evaluated and excluded, with reasons`,
  legendNote: "dashed rings ≈ drive-time bands (rough) · scroll to zoom, drag to pan · search filters both map and list",
  searchPlaceholder: (s) => `Search ${s.nLakes} WI/MI lakes + ${s.nList} listings — try a lake, county, or price…`,
  footer: "Companion to the Midwest briefing. Listing status changes fast — re-confirm with brokers before touring. Drive times are non-peak estimates from the Loop; rings are straight-line approximations, not isochrones. Everything inside the 4-hour ring (Lake Geneva, Green Lake, the Chain O'Lakes) was excluded by the brief, not overlooked — see the exclusion ledger in the briefing. For the original Northeast search, see the Northeast tab.",
  briefNote: '<p class="fine" style="margin-top:4px">Compiled September 1, 2026 as the Midwest companion to the Northeast search. Same bar, same method, new origin: the Loop instead of Midtown, and a 4-hour floor as well as an 8-hour ceiling.</p>',
  briefNoteAnchor: '<h2 style="margin-top:6px">Executive summary</h2>',
  appendixTitle: "Appendix — the full Wisconsin/Michigan sweep (September 1, 2026)",
  appendixIntro: (s) => `County-by-county passes evaluated every named lake of consequence in northern Wisconsin (Vilas, Oneida, Iron, Forest, Sawyer, Bayfield, Douglas, Price, Marinette/Oconto), the northern Lower Peninsula and the Upper Peninsula of Michigan — plus a certification pass over Minnesota, Indiana, Ohio and Iowa — against the archetype bar: 4–8 h from the Loop, towsports legal and practical, ~450+ acres (exceptions justified on water quality), documented clarity, forested and substantially conserved shoreline, and private frontage that actually trades. <strong>${s.nLakes} lakes passed</strong> (${s.t1} Tier 1, ${s.t2} Tier 2, ${s.watch} watchlist/edge) and <strong>${s.nExcl} were evaluated and excluded</strong> with reasons below. The listings snapshot holds ${s.nList} live opportunities. The honesty rule from the Northeast report carries over: several of the best <em>program</em> matches sit on lakes that fail the <em>water</em> bar (Halfway Lake's eight cabins on a no-motor pond, the Herendeene lodge-and-six-cabins on a 40-acre puddle, two complete Houghton Lake clusters) — they are listed with explicit caveats, never as recommendations.`,
  appendixFine: `Two structural facts shape everything here. First, Wisconsin shoreland zoning (NR 115 plus county ordinances) generally permits one principal dwelling plus one <em>non-rental</em> guest house per lot — so the lodge-plus-five-cabins sketch is not buildable on a single residential parcel, and the practical routes are a grandfathered resort, a multi-lot assemblage, or a condominium plat. Second, that is exactly why the Northwoods resort market is the opportunity: aging owners are selling and buyers are demolishing the cabins to build one house. The decline is sixty years old — Oneida County lost 23.4% of its resort-type establishments between 1961 and 1968 alone, against 13.9% statewide, and about 98% of the losses were seasonal cottage places — and it has not reversed. Five couples buying a whole resort and <em>keeping</em> the cabins is the arbitrage this report is built on. Michigan has no statewide shoreland zoning at all — density is a township question, which cuts both ways.`,
  appendixSources: `Sources per lake are linked from the map popups (monitoring programs: Wisconsin DNR Citizen Lake Monitoring Network and the DNR lake pages; Michigan's MiCorps Cooperative Lakes Monitoring Program; Tip of the Mitt Watershed Council; Leelanau Conservancy; Grindstone, Crystal Lake and Higgins Lake associations. Boating rules: Wis. Stat. 30.66 speed restrictions; Michigan's 100-ft/3-ft no-wake rule under MCL 324.80209; wake-boat bills pending in both states). Listing statuses move in days — re-confirm before touring.`,
};

const REGIONS = [NORTHEAST, MIDWEST];

// ============================================================ shared code ===
const CLS = {
  t1: { color: "#104281", r: 7.5 }, t2: { color: "#2a78d6", r: 5.5 },
  watch: { color: "#86b6ef", r: 4.5 }, listing: { color: "#eb6834", r: 5.5 }, ref: { color: "#52514e", r: 6 },
  rental: { color: "#2f8f5b", r: 5.5 },
};
const zorder = { ref: 0, watch: 1, t2: 2, t1: 3, listing: 4, rental: 5 };

function buildRegion(cfg) {
  const DATA = JSON.parse(fs.readFileSync(cfg.data, "utf8"));

  // ---------- basemap ----------
  const KEEP = new Set(cfg.states);
  const states = topojson.feature(us, us.objects.states).features.filter(f => KEEP.has(f.id));
  const borders = topojson.mesh(us, us.objects.states, (a, b) => a !== b && (KEEP.has(a.id) || KEEP.has(b.id)));
  const { W, H } = cfg;
  const proj = geoTransverseMercator().rotate([cfg.rotate, 0]);
  proj.fitExtent([[8, 8], [W - 8, H - 8]], { type: "MultiPoint", coordinates: cfg.frame });
  const path = geoPath(proj);
  const landPaths = states.map(f => path(f)).filter(Boolean);
  const borderPath = path(borders);

  const [oLon, oLat] = cfg.origin;
  const brg = cfg.labelBearing * Math.PI / 180;
  const rings = cfg.rings.map(r => {
    const circ = geoCircle().center(cfg.origin).radius(r.mi / 69.05)();
    const deg = r.mi / 69.05;
    const lat = oLat + deg * Math.cos(brg);
    const lon = oLon + deg * Math.sin(brg) / Math.cos(lat * Math.PI / 180);
    const pt = proj([lon, lat]);
    return { d: path(circ), label: r.label, lx: pt[0], ly: pt[1] - 4 };
  });

  // ---------- points ----------
  const pts = [];
  for (const r of DATA.refs) {
    pts.push({ id: r.key, cls: "ref", shape: r.shape, name: r.name, lat: r.lat, lon: r.lon,
      meta: r.drive ? `${r.drive}${r.acres ? " · " + fmtAc(r.acres) + " ac" : ""}` : "",
      blurb: r.blurb, links: r.links || [], isNew: false });
  }
  for (const L of DATA.lakes) {
    pts.push({ id: L.key, cls: L.cls, name: L.name, lat: L.lat, lon: L.lon,
      meta: `${L.state} · ${L.drive} · ${fmtAc(L.acres)} ac · fit ${L.score}`,
      blurb: L.blurb, clarity: L.clarity || "", motors: L.motors || "",
      links: L.links || [], isNew: !!L.new });
  }
  const lakeByKey = Object.fromEntries(DATA.lakes.map(L => [L.key, L]));
  DATA.listings.forEach((x, i) => {
    const hostLake = (lakeByKey[x.lakeKey] || {}).name || x.lakeName || "";
    pts.push({ id: "l" + i, cls: "listing", shape: "sq", name: x.name, lat: x.lat, lon: x.lon,
      meta: (hostLake ? hostLake + " · " : "") + (x.detail || "") + (x.status === "verify" ? " · status: confirm w/ broker" : ""),
      blurb: x.fit || "", links: [["Listing", x.url]], isNew: !!x.new });
  });
  const fmtRate = r => r == null ? "" : ("$" + r.toLocaleString("en-US"));
  (DATA.rentals || []).forEach((x, i) => {
    const hostLake = (lakeByKey[x.lakeKey] || {}).name || x.lakeName || "";
    const cap = [x.bedrooms ? x.bedrooms + " BR" : null, x.baths ? x.baths + " BA" : null, x.sleeps ? "sleeps " + x.sleeps : null].filter(Boolean).join(" / ");
    const rate = x.rate ? fmtRate(x.rate) + (x.rateUnit || "/wk") : (x.rateNote || "rate on request");
    const links = [];
    if (x.direct) links.push(["Book direct", x.direct]);
    if (x.url) links.push([x.platform || "Listing", x.url]);
    pts.push({ id: "r" + i, cls: "rental", shape: "tri", name: x.name, lat: x.lat, lon: x.lon,
      meta: [hostLake, cap, rate, x.kind === "buyout" ? "resort buyout" : null,
             x.status === "verify" ? "status: confirm w/ host" : null].filter(Boolean).join(" · "),
      blurb: (x.detail ? x.detail + " — " : "") + (x.fit || ""), links, isNew: !!x.new,
      clarity: x.season ? "Season: " + x.season : "", motors: x.dock ? "Dock: " + x.dock : "" });
  });
  for (const p of pts) { const xy = proj([p.lon, p.lat]); p.x = +xy[0].toFixed(1); p.y = +xy[1].toFixed(1); }

  function markerSvg(p) {
    const c = CLS[p.cls];
    let shape;
    if (p.shape === "star") shape = `<path d="M0,-8 L2.2,-2.8 L8,-2.4 L3.6,1.4 L5,7 L0,3.8 L-5,7 L-3.6,1.4 L-8,-2.4 L-2.2,-2.8 Z" fill="#0b0b0b" stroke="#fcfcfb" stroke-width="1.4"/>`;
    else if (p.shape === "ring") shape = `<circle r="7" fill="none" stroke="#52514e" stroke-width="2.6"/><circle r="1.8" fill="#52514e"/>`;
    else if (p.shape === "sq") shape = `<rect x="-4.6" y="-4.6" width="9.2" height="9.2" rx="2" transform="rotate(45)" fill="${c.color}" stroke="#fcfcfb" stroke-width="1.4"/>`;
    else if (p.shape === "tri") shape = `<path d="M0,-7 L6.5,5 L-6.5,5 Z" fill="${c.color}" stroke="#fcfcfb" stroke-width="1.4" stroke-linejoin="round"/>`;
    else shape = `<circle r="${c.r}" fill="${c.color}" stroke="#fcfcfb" stroke-width="1.5"/>`;
    return `<g class="marker cls-${p.cls}" data-id="${p.id}" transform="translate(${p.x},${p.y})"><g class="mk">${shape}<circle class="hit" r="9" fill="transparent"/></g></g>`;
  }
  const markersSvg = [...pts].sort((a, b) => zorder[a.cls] - zorder[b.cls]).map(markerSvg).join("\n");

  function labelSvg(p) {
    const lp = cfg.labels[p.id]; if (!lp) return "";
    const txt = (cfg.labelText || {})[p.id] || p.name.replace(/ \(the archetype\)/, " (archetype)").replace(/\s*\((?!archetype)[^)]*\)$/, "").replace(/, (ME|VT|NY|NH|WI|MI)$/, "");
    return `<g class="lblg cls-${p.cls}" transform="translate(${p.x},${p.y})"><g class="mk"><text class="mlabel" x="${lp.dx}" y="${lp.dy}" text-anchor="${lp.anchor}">${esc(txt)}</text></g></g>`;
  }
  const labelsSvg = pts.map(labelSvg).join("");

  // ---------- cards ----------
  const nLakes = DATA.lakes.length, nList = DATA.listings.length;
  const counts = { t1: DATA.lakes.filter(l => l.cls === "t1").length, t2: DATA.lakes.filter(l => l.cls === "t2").length,
    watch: DATA.lakes.filter(l => l.cls === "watch").length, listing: nList,
    rental: (DATA.rentals || []).length };
  const nExcl = Object.values(DATA.excluded).reduce((a, b) => a + b.length, 0);
  const stats = { nLakes, nList, nExcl, t1: counts.t1, t2: counts.t2, watch: counts.watch, nRent: counts.rental };

  const GROUPS = [
    ["t1", `Tier 1 — pursue (${counts.t1})`],
    ["t2", `Tier 2 — strong (${counts.t2})`],
    ["listing", `Live listings (${counts.listing}) — ${cfg.listingsGroupNote}`],
    ["rental", `Summer rentals for 8 couples (${counts.rental}) — 7+ bedrooms, waterfront + dock, Tier 1 lakes`],
    ["watch", `Watchlist / edge (${counts.watch})`],
    ["ref", "Reference points"],
  ];
  function card(p) {
    const links = p.links.map(([t, u]) => `<a href="${u}" target="_blank" rel="noopener">${esc(t)} ↗</a>`).join(" · ");
    return `<div class="card cls-${p.cls}" data-id="${p.id}" tabindex="0">
    <div class="card-head"><span class="dot dot-${p.cls}${p.shape === "sq" ? " dot-sq" : ""}${p.shape === "tri" ? " dot-tri" : ""}"></span><span class="card-name">${esc(p.name)}</span>${p.isNew ? '<span class="newpill">NEW</span>' : ""}</div>
    ${p.meta ? `<div class="card-meta">${esc(p.meta)}</div>` : ""}
    <div class="card-blurb">${esc(p.blurb)}</div>
    ${links ? `<div class="card-links">${links}</div>` : ""}
  </div>`;
  }
  const sections = GROUPS.map(([cls, title]) =>
    `<section class="grp grp-${cls}"><h2>${esc(title)}</h2>${pts.filter(p => p.cls === cls).map(card).join("\n")}</section>`
  ).join("\n");

  // ---------- briefing + appendix ----------
  let briefing = fs.readFileSync(cfg.briefing, "utf8");
  const tierName = { t1: "Tier 1", t2: "Tier 2", watch: "Watch" };
  const lakeRows = [...DATA.lakes].sort((a, b) => (zorder[b.cls] - zorder[a.cls]) || (b.score - a.score))
    .map(L => `<tr><td><strong>${esc(L.name)}</strong>${L.new ? ' <span class="newpill">NEW</span>' : ""}</td><td>${L.state}</td><td>${fmtAc(L.acres)}</td><td>${L.drive}</td><td>${tierName[L.cls]} · ${L.score}</td><td>${esc(L.blurb)}</td></tr>`).join("\n");
  const exclBlocks = Object.entries(DATA.excluded).map(([region, items]) =>
    `<details><summary><strong>${esc(region)}</strong> — ${items.length} lakes evaluated and excluded (click to expand)</summary><ul>${items.map(e => `<li><strong>${esc(e.name)}:</strong> ${esc(e.reason)}</li>`).join("")}</ul></details>`).join("\n");
  const appendix = `
<h2>${cfg.appendixTitle}</h2>
<p>${cfg.appendixIntro(stats)}</p>
<p class="fine">${cfg.appendixFine}</p>
<h3>Every passing lake</h3>
<table class="btable"><thead><tr><th>Lake</th><th>St</th><th>Acres</th><th>Drive</th><th>Tier · fit</th><th>One-liner</th></tr></thead><tbody>
${lakeRows}
</tbody></table>
<h3>Evaluated and excluded — the honest ledger</h3>
${exclBlocks}
<p class="fine">${cfg.appendixSources}</p>`;
  briefing = briefing.replace(/<\/div>\s*$/, appendix + "\n</div>");
  briefing = briefing.replace(cfg.briefNoteAnchor, cfg.briefNote + "\n<h2>Executive summary</h2>");

  // ---------- panels ----------
  const id = cfg.id;
  const mapPanel = `
<div class="legend" id="legend-${id}" data-region="${id}">
  <span class="chip" data-cls="t1"><span class="dot dot-t1"></span>Tier 1 (${counts.t1})</span>
  <span class="chip" data-cls="t2"><span class="dot dot-t2"></span>Tier 2 (${counts.t2})</span>
  <span class="chip" data-cls="watch"><span class="dot dot-watch"></span>Watchlist (${counts.watch})</span>
  <span class="chip" data-cls="listing"><span class="dot dot-listing sq"></span>Listings (${counts.listing})</span>
  <span class="chip" data-cls="rental"><span class="dot dot-rental tri"></span>Rentals · 8 couples (${counts.rental})</span>
  <span class="chip" data-cls="ref"><span class="dot dot-ref"></span>${cfg.refChipLabel}</span>
  <span class="note">${cfg.legendNote}</span>
</div>
<main>
  <div class="mapwrap" id="wrap-${id}">
    <svg id="map-${id}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Map of candidate lakes">
      <g id="world-${id}">
        <g>${landPaths.map(d => `<path class="land" d="${d}"/>`).join("")}</g>
        <path class="stateline" d="${borderPath}"/>
        ${rings.map(r => `<path class="ring" d="${r.d}"/>`).join("")}
        ${rings.map(r => `<text class="ringlabel" x="${r.lx.toFixed(1)}" y="${r.ly.toFixed(1)}" text-anchor="middle">${r.label}</text>`).join("")}
        <g id="markers-${id}">${markersSvg}</g>
        <g id="labels-${id}">${labelsSvg}</g>
      </g>
    </svg>
    <div class="zoombtns">
      <button data-zoom="in" aria-label="Zoom in">+</button>
      <button data-zoom="out" aria-label="Zoom out">−</button>
      <button data-zoom="reset" aria-label="Reset view" style="font-size:12px">⟲</button>
    </div>
    <div class="maptip" id="tip-${id}"></div>
    <div class="mappop" id="pop-${id}"><button class="close" aria-label="Close">✕</button><div class="popbody"></div></div>
    <div class="attribution">Basemap: US Census via us-atlas · locations approximate</div>
  </div>
  <aside class="cards">
    <div class="searchbox"><input class="q" type="search" placeholder="${esc(cfg.searchPlaceholder(stats))}" aria-label="Search"></div>
    ${sections}
  </aside>
</main>
<footer>${cfg.footer}</footer>`;

  const clientPts = pts.map(({ id, name, meta, blurb, clarity, motors, cls, x, y, links }) =>
    ({ id, name, meta, blurb, clarity, motors, cls, x, y, links }));

  return { cfg, id, stats, mapPanel, briefing, clientPts, W, H };
}

const built = REGIONS.map(buildRegion);

// ---------------------------------------------------------------- html ----
const regionTabs = built.map((b, i) =>
  `<button class="tab${i === 0 ? " on" : ""}" data-region="${b.id}" role="tab" aria-selected="${i === 0}">${esc(b.cfg.tab)}<span class="tabnote">${b.cfg.tabNote}</span></button>`
).join("\n  ");

const regionPanels = built.map((b, i) => `<div class="region" id="region-${b.id}"${i === 0 ? "" : " hidden"}>
<div class="panel-map" id="panel-map-${b.id}">${b.mapPanel}</div>
<div class="panel-brief" id="panel-brief-${b.id}" hidden>${b.briefing}</div>
</div>`).join("\n");

const META = Object.fromEntries(built.map(b => [b.id, { h1: b.cfg.h1, sub: b.cfg.sub(b.stats), subBrief: b.cfg.subBrief(b.stats), W: b.W, H: b.H }]));
const PTSBYREGION = Object.fromEntries(built.map(b => [b.id, b.clientPts]));

const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Finding Your Squam — Northeast &amp; Midwest lake search</title>
<style>
  :root{color-scheme:light;
    --page:#f9f9f7;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
    --hairline:#e1e0d9;--border:rgba(11,11,11,.10);
    --t1:#104281;--t2:#2a78d6;--watch:#86b6ef;--listing:#eb6834;--ref:#52514e;--rental:#2f8f5b;
    --ocean:#dbe8f4;--land:#f5f3ea;--stateline:#c2beb2}
  *{box-sizing:border-box}
  body{margin:0;background:var(--page);color:var(--ink);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
  header{padding:18px 22px 10px}
  header h1{margin:0;font-size:20px;letter-spacing:-.2px}
  header p{margin:4px 0 0;color:var(--ink2);font-size:13px}
  .tabs{display:flex;flex-wrap:wrap;gap:8px;padding:2px 22px 0}
  .tabs.regiontabs{padding-bottom:2px}
  .tab{display:flex;flex-direction:column;align-items:flex-start;line-height:1.25;padding:7px 18px;border:1px solid var(--border);border-radius:12px;background:var(--surface);color:var(--ink2);cursor:pointer;font-size:13.5px;font-weight:700;text-align:left}
  .tab .tabnote{font-size:10.5px;font-weight:600;letter-spacing:.02em;color:var(--muted);text-transform:uppercase}
  .tab.on{background:var(--t1);border-color:var(--t1);color:#fff}
  .tab.on .tabnote{color:rgba(255,255,255,.72)}
  .tab:focus-visible,.tab2:focus-visible{outline:2px solid var(--t2);outline-offset:2px}
  .viewtabs{padding-top:10px}
  .tab2{padding:6px 16px;border:1px solid var(--border);border-radius:999px;background:var(--surface);color:var(--ink2);cursor:pointer;font-size:12.5px;font-weight:600}
  .tab2.on{background:var(--ink);border-color:var(--ink);color:#fff}
  .legend{display:flex;flex-wrap:wrap;gap:8px;padding:10px 22px 12px;align-items:center}
  .chip{display:inline-flex;align-items:center;gap:7px;padding:5px 11px;border:1px solid var(--border);border-radius:999px;background:var(--surface);cursor:pointer;font-size:12.5px;color:var(--ink2);user-select:none}
  .chip .dot{width:10px;height:10px;border-radius:50%}
  .chip.off{opacity:.38}
  .legend .note{font-size:12px;color:var(--muted);margin-left:4px}
  .dot-t1{background:var(--t1)} .dot-t2{background:var(--t2)} .dot-watch{background:var(--watch)} .dot-ref{background:var(--ref)}
  .dot-listing{background:var(--listing)} .dot.dot-sq,.chip .dot.sq{border-radius:2px;transform:rotate(45deg)}
  .dot-rental{background:var(--rental)}
  .dot.dot-tri,.chip .dot.tri{background:transparent;border-radius:0;width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:10px solid var(--rental)}
  main{display:flex;gap:14px;padding:0 22px 22px;align-items:stretch}
  .mapwrap{position:relative;flex:1 1 62%;min-width:0;background:var(--ocean);border:1px solid var(--border);border-radius:12px;overflow:hidden;align-self:flex-start}
  svg{display:block;width:100%;height:auto;touch-action:none;cursor:grab}
  svg.panning{cursor:grabbing}
  .land{fill:var(--land);stroke:#d5d1c4;stroke-width:.5;vector-effect:non-scaling-stroke}
  .stateline{fill:none;stroke:var(--stateline);stroke-width:.7;vector-effect:non-scaling-stroke}
  .lblg{pointer-events:none}
  .ring{fill:none;stroke:var(--muted);stroke-width:1;stroke-dasharray:3 5;vector-effect:non-scaling-stroke;opacity:.75}
  .ringlabel{font-size:10.5px;fill:var(--muted);paint-order:stroke;stroke:var(--ocean);stroke-width:3px;font-weight:600}
  .mlabel{font-size:10.5px;font-weight:650;fill:var(--ink2);paint-order:stroke;stroke:rgba(252,252,251,.9);stroke-width:3px}
  .marker{cursor:pointer}
  .marker.dim{opacity:.12;pointer-events:none}
  .marker.active .mk>*:first-child{filter:drop-shadow(0 0 4px rgba(235,104,52,.9))}
  .zoombtns{position:absolute;top:10px;right:10px;display:flex;flex-direction:column;gap:6px;z-index:4}
  .zoombtns button{width:30px;height:30px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--ink2);font-size:16px;cursor:pointer;line-height:1}
  .maptip{position:absolute;pointer-events:none;background:var(--surface);border:1px solid var(--border);border-radius:8px;box-shadow:0 4px 14px rgba(11,11,11,.12);padding:8px 10px;font-size:12px;max-width:250px;display:none;z-index:7}
  .maptip b{display:block;font-size:12.5px}
  .maptip .m{color:var(--muted);margin:2px 0}
  .mappop{position:absolute;background:var(--surface);border:1px solid var(--border);border-radius:10px;box-shadow:0 8px 24px rgba(11,11,11,.18);padding:11px 30px 11px 13px;font-size:12.5px;max-width:290px;display:none;z-index:6}
  .mappop b{display:block;font-size:13.5px;line-height:1.3}
  .mappop .m{color:var(--muted);margin:3px 0 2px}
  .mappop .bl{color:var(--ink2);margin-top:2px}
  .mappop .wq{color:var(--ink2);margin-top:5px;font-size:11.5px}
  .mappop .wq b2{font-weight:650}
  .mappop .links{margin-top:8px}
  .mappop .links a{display:inline-block;margin:0 6px 5px 0;padding:4px 10px;border:1px solid rgba(16,66,129,.4);border-radius:7px;font-weight:600;border-bottom-width:1px}
  .mappop .close{position:absolute;top:3px;right:3px;border:none;background:none;cursor:pointer;color:var(--muted);font-size:13px;padding:5px;line-height:1}
  .mappop .close:hover{color:var(--ink)}
  .attribution{position:absolute;left:10px;bottom:8px;font-size:10.5px;color:var(--muted)}
  aside{flex:0 0 372px;max-width:410px;overflow-y:auto;max-height:calc(100vh - 40px);padding-right:2px}
  .searchbox{position:sticky;top:0;background:var(--page);padding:2px 2px 8px;z-index:3}
  .searchbox input{width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:9px;background:var(--surface);font:13px system-ui;color:var(--ink)}
  .searchbox input:focus{outline:2px solid var(--t2);outline-offset:1px}
  aside h2{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:16px 2px 8px}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 12px;margin-bottom:8px;cursor:pointer}
  .card:hover{border-color:rgba(11,11,11,.25)}
  .card.active{border-color:var(--listing);box-shadow:0 0 0 2px rgba(235,104,52,.25)}
  .card.hidden{display:none}
  .card-head{display:flex;align-items:center;gap:8px}
  .card .dot{width:9px;height:9px;border-radius:50%;flex:none}
  .card-name{font-weight:650;font-size:13.5px}
  .newpill{font-size:9.5px;font-weight:700;letter-spacing:.05em;background:#eb6834;color:#fff;border-radius:99px;padding:2px 7px;margin-left:auto;flex:none}
  .card-meta{color:var(--muted);font-size:12px;margin:3px 0 2px}
  .card-blurb{color:var(--ink2);font-size:12.5px;margin-top:2px}
  .card-links{margin-top:6px;font-size:12.5px}
  a{color:#1c5cab;text-decoration:none;border-bottom:1px solid rgba(28,92,171,.3)}
  a:hover{border-bottom-color:#1c5cab}
  footer{padding:0 22px 20px;color:var(--muted);font-size:11.5px;max-width:900px}
  .grp.hidden{display:none}
  .panel-brief{padding:16px 22px 30px}
  .brief{max-width:960px;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:26px 34px;margin:0 auto}
  .brief h2{font-size:17px;margin:28px 0 10px;color:var(--t1);letter-spacing:-.1px}
  .brief h3{font-size:14.5px;margin:18px 0 6px}
  .brief p{font-size:13.5px;line-height:1.62;margin:8px 0;color:var(--ink)}
  .brief ul{margin:6px 0 14px;padding-left:22px}
  .brief li{margin:6px 0;font-size:13.5px;line-height:1.55;color:var(--ink)}
  .brief .fine{font-size:11.5px;color:var(--muted);font-style:italic}
  .brief details{margin:8px 0;font-size:13px}
  .brief details ul{columns:2;column-gap:28px}
  .brief summary{cursor:pointer;padding:4px 0}
  .btable{width:100%;border-collapse:collapse;margin:12px 0 6px;font-size:12.5px}
  .btable th{background:var(--t1);color:#fff;text-align:left;padding:7px 9px;font-size:11.5px;border:1px solid var(--t1)}
  .btable td{border:1px solid var(--hairline);padding:7px 9px;vertical-align:top;line-height:1.5}
  .btable tbody tr:nth-child(even){background:#f3f6fa}
  .tablewrap{overflow-x:auto}
  @media (max-width:900px){main{flex-direction:column}aside{flex:1 1 auto;max-height:none;max-width:none}.brief details ul{columns:1}.brief{padding:20px 16px}}
</style></head>
<body>
<header>
  <h1 id="hd-title">${esc(built[0].cfg.h1)} — the map</h1>
  <p id="hd-sub">${esc(built[0].cfg.sub(built[0].stats))}</p>
</header>
<div class="tabs regiontabs" role="tablist" aria-label="Region">
  ${regionTabs}
</div>
<div class="tabs viewtabs" role="tablist" aria-label="View">
  <button class="tab2 on" data-view="map" role="tab" aria-selected="true">Map</button>
  <button class="tab2" data-view="brief" role="tab" aria-selected="false">Full briefing</button>
</div>
${regionPanels}
<script>
  const META = ${JSON.stringify(META)};
  const PTS_BY_REGION = ${JSON.stringify(PTSBYREGION)};

  function initRegion(rid) {
    const W = META[rid].W, H = META[rid].H;
    const PTS = PTS_BY_REGION[rid];
    const byId = Object.fromEntries(PTS.map(p => [p.id, p]));
    const root = document.getElementById("region-" + rid);
    const svg = document.getElementById("map-" + rid), world = document.getElementById("world-" + rid);
    const tip = document.getElementById("tip-" + rid);
    const wrap = document.getElementById("wrap-" + rid);
    const pop = document.getElementById("pop-" + rid), popbody = pop.querySelector(".popbody");
    const markers = [...root.querySelectorAll(".marker")];
    const cards = [...root.querySelectorAll(".card")];
    let k = 1, tx = 0, ty = 0, pinned = null, moved = false;

    function apply() {
      world.setAttribute("transform", "translate(" + tx + "," + ty + ") scale(" + k + ")");
      root.querySelectorAll(".mk").forEach(g => g.setAttribute("transform", "scale(" + (1 / Math.pow(k, 0.85)) + ")"));
      positionPop();
    }
    function markerScreen(id) {
      const p = byId[id], r = svg.getBoundingClientRect();
      return [(p.x * k + tx) * r.width / W, (p.y * k + ty) * r.height / H];
    }
    function positionPop() {
      if (!pinned) return;
      const [sx, sy] = markerScreen(pinned), wr = wrap.getBoundingClientRect();
      const pw = pop.offsetWidth || 270, ph = pop.offsetHeight || 130;
      let x = sx + 16, y = sy - ph / 2;
      if (x + pw > wr.width - 8) x = sx - pw - 16;
      x = Math.max(8, x);
      y = Math.max(8, Math.min(y, wr.height - ph - 8));
      pop.style.left = x + "px"; pop.style.top = y + "px";
    }
    function pinPopup(id) {
      const p = byId[id]; if (!p) return;
      pinned = id;
      const linksHtml = (p.links && p.links.length)
        ? '<div class="links">' + p.links.map(l => '<a href="' + l[1] + '" target="_blank" rel="noopener">' + l[0] + ' ↗</a>').join("") + "</div>" : "";
      const isR = p.cls === "rental";
      const wq = (p.clarity ? '<div class="wq">' + (isR ? "" : "<b2>Water:</b2> ") + p.clarity + "</div>" : "") +
                 (p.motors ? '<div class="wq">' + (isR ? "" : "<b2>Motors:</b2> ") + p.motors + "</div>" : "");
      popbody.innerHTML = "<b>" + p.name + "</b>" + (p.meta ? '<div class="m">' + p.meta + "</div>" : "") + '<div class="bl">' + p.blurb + "</div>" + wq + linksHtml;
      pop.style.display = "block"; tip.style.display = "none";
      positionPop();
    }
    function unpin() { pinned = null; pop.style.display = "none"; }
    pop.querySelector(".close").addEventListener("click", unpin);
    document.addEventListener("keydown", e => { if (e.key === "Escape") unpin(); });

    function zoomAt(f, cx, cy) {
      const nk = Math.min(14, Math.max(1, k * f)); f = nk / k;
      tx = cx - (cx - tx) * f; ty = cy - (cy - ty) * f; k = nk;
      if (k === 1) { tx = 0; ty = 0; }
      apply();
    }
    function svgPoint(e) {
      const r = svg.getBoundingClientRect();
      return [(e.clientX - r.left) * W / r.width, (e.clientY - r.top) * H / r.height];
    }
    svg.addEventListener("wheel", e => { e.preventDefault(); const [cx, cy] = svgPoint(e); zoomAt(e.deltaY < 0 ? 1.25 : 0.8, cx, cy); }, { passive: false });
    root.querySelector('[data-zoom="in"]').onclick = () => zoomAt(1.4, W / 2, H / 2);
    root.querySelector('[data-zoom="out"]').onclick = () => zoomAt(0.71, W / 2, H / 2);
    root.querySelector('[data-zoom="reset"]').onclick = () => { k = 1; tx = 0; ty = 0; apply(); };

    let drag = null;
    svg.addEventListener("pointerdown", e => { drag = { x: e.clientX, y: e.clientY, tx, ty }; moved = false; svg.classList.add("panning"); });
    window.addEventListener("pointermove", e => {
      if (!drag) return;
      if (Math.abs(e.clientX - drag.x) + Math.abs(e.clientY - drag.y) > 5) moved = true;
      if (!moved) return;
      const r = svg.getBoundingClientRect(), s = W / r.width;
      tx = drag.tx + (e.clientX - drag.x) * s; ty = drag.ty + (e.clientY - drag.y) * s; apply();
    });
    window.addEventListener("pointerup", () => { if (drag) { drag = null; svg.classList.remove("panning"); } });

    function setActive(id, scroll) {
      markers.forEach(m => m.classList.toggle("active", m.dataset.id === id));
      cards.forEach(c => {
        const on = c.dataset.id === id;
        c.classList.toggle("active", on);
        if (on && scroll) c.scrollIntoView({ block: "nearest", behavior: "smooth" });
      });
    }
    markers.forEach(m => {
      m.addEventListener("pointerenter", () => {
        const p = byId[m.dataset.id]; if (!p || pinned === m.dataset.id) return;
        tip.innerHTML = "<b>" + p.name + "</b>" + (p.meta ? '<div class="m">' + p.meta + "</div>" : "") + "<div>" + p.blurb + "</div><div class='m'>click to pin info + links</div>";
        tip.style.display = "block";
      });
      m.addEventListener("pointermove", e => {
        const r = wrap.getBoundingClientRect();
        let x = e.clientX - r.left + 14, y = e.clientY - r.top + 12;
        if (x + 260 > r.width) x -= 280; if (y + 90 > r.height) y -= 100;
        tip.style.left = x + "px"; tip.style.top = y + "px";
      });
      m.addEventListener("pointerleave", () => tip.style.display = "none");
      m.addEventListener("click", e => { e.stopPropagation(); setActive(m.dataset.id, true); pinPopup(m.dataset.id); });
    });
    cards.forEach(c => {
      c.addEventListener("click", e => { if (e.target.tagName === "A") return; setActive(c.dataset.id, false); pinPopup(c.dataset.id); });
    });
    svg.addEventListener("click", () => { if (moved) { moved = false; return; } setActive(null, false); unpin(); });

    // visibility = chips ∩ search
    const off = new Set();
    let query = "";
    const matches = p => !query || (p.name + " " + (p.meta || "") + " " + (p.blurb || "")).toLowerCase().includes(query);
    function refresh() {
      markers.forEach(m => { const p = byId[m.dataset.id]; m.classList.toggle("dim", off.has(p.cls) || !matches(p)); });
      cards.forEach(c => { const p = byId[c.dataset.id]; c.classList.toggle("hidden", !matches(p)); });
      root.querySelectorAll(".grp").forEach(g => {
        const c = [...g.classList].find(x => x.startsWith("grp-")).slice(4);
        const anyVisible = [...g.querySelectorAll(".card")].some(cd => !cd.classList.contains("hidden"));
        g.classList.toggle("hidden", off.has(c) || !anyVisible);
      });
      if (pinned && (off.has(byId[pinned].cls) || !matches(byId[pinned]))) unpin();
    }
    root.querySelectorAll(".chip").forEach(ch => {
      ch.addEventListener("click", () => {
        const cls = ch.dataset.cls;
        if (off.has(cls)) off.delete(cls); else off.add(cls);
        ch.classList.toggle("off", off.has(cls));
        refresh();
      });
    });
    root.querySelector(".q").addEventListener("input", e => { query = e.target.value.trim().toLowerCase(); refresh(); });

    apply();
    return { relayout: apply };
  }

  const REGION_IDS = ${JSON.stringify(built.map(b => b.id))};
  const regions = Object.fromEntries(REGION_IDS.map(r => [r, initRegion(r)]));
  let curRegion = REGION_IDS[0], curView = "map";

  function render() {
    document.getElementById("hd-title").textContent =
      META[curRegion].h1 + (curView === "map" ? " — the map" : " — the full briefing");
    document.getElementById("hd-sub").textContent =
      curView === "map" ? META[curRegion].sub : META[curRegion].subBrief;
    document.querySelectorAll(".regiontabs .tab").forEach(t => {
      const on = t.dataset.region === curRegion;
      t.classList.toggle("on", on); t.setAttribute("aria-selected", on);
    });
    document.querySelectorAll(".viewtabs .tab2").forEach(t => {
      const on = t.dataset.view === curView;
      t.classList.toggle("on", on); t.setAttribute("aria-selected", on);
    });
    REGION_IDS.forEach(r => {
      document.getElementById("region-" + r).hidden = (r !== curRegion);
      document.getElementById("panel-map-" + r).hidden = !(r === curRegion && curView === "map");
      document.getElementById("panel-brief-" + r).hidden = !(r === curRegion && curView === "brief");
    });
    if (curView === "map") regions[curRegion].relayout();
    if (history.replaceState) history.replaceState(null, "", "#" + curRegion + "/" + curView);
  }
  document.querySelectorAll(".regiontabs .tab").forEach(t =>
    t.addEventListener("click", () => { curRegion = t.dataset.region; render(); }));
  document.querySelectorAll(".viewtabs .tab2").forEach(t =>
    t.addEventListener("click", () => { curView = t.dataset.view; render(); }));

  const hash = (location.hash || "").replace("#", "").split("/");
  if (REGION_IDS.includes(hash[0])) curRegion = hash[0];
  if (hash[1] === "brief" || hash[1] === "map") curView = hash[1];
  render();
</script>
</body></html>`;
fs.writeFileSync("../index.html", html);
const tot = built.reduce((a, b) => a + b.stats.nLakes, 0), totL = built.reduce((a, b) => a + b.stats.nList, 0);
console.log("WROTE index.html", html.length, "bytes ·", built.length, "regions ·", tot, "lakes ·", totL, "listings");
built.forEach(b => console.log("  ·", b.id, b.stats));
