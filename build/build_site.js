const fs = require("fs");
const topojson = require("topojson-client");
const us = require("./node_modules/us-atlas/states-10m.json");
const { geoTransverseMercator, geoPath, geoCircle } = require("d3-geo");

const DATA = JSON.parse(fs.readFileSync("../data/map_data.json", "utf8"));

// ---------- basemap ----------
const KEEP = new Set(["23","33","50","36","25","09","44","34","42","10","24"]);
const states = topojson.feature(us, us.objects.states).features.filter(f => KEEP.has(f.id));
const borders = topojson.mesh(us, us.objects.states, (a, b) => a !== b && (KEEP.has(a.id) || KEEP.has(b.id)));
const W = 700, H = 780;
const frame = { type: "MultiPoint", coordinates: [
  [-77.6, 39.9], [-67.6, 39.9], [-67.6, 45.95], [-77.6, 45.95],
  [-72.6, 39.9], [-72.6, 45.95], [-77.6, 42.9], [-67.6, 42.9],
] };
const proj = geoTransverseMercator().rotate([72.6, 0]);
proj.fitExtent([[8, 8], [W - 8, H - 8]], frame);
const path = geoPath(proj);
const landPaths = states.map(f => path(f)).filter(Boolean);
const borderPath = path(borders);
const NYC = [-73.984, 40.755];
const rings = [
  { mi: 220, label: "≈ 4 h drive" }, { mi: 270, label: "≈ 5 h" }, { mi: 350, label: "≈ 6.5 h" },
].map(r => {
  const circ = geoCircle().center(NYC).radius(r.mi / 69.05)();
  const deg = r.mi / 69.05, brg = 46 * Math.PI / 180;
  const lat = 40.755 + deg * Math.cos(brg);
  const lon = NYC[0] + deg * Math.sin(brg) / Math.cos(lat * Math.PI / 180);
  const pt = proj([lon, lat]);
  return { d: path(circ), label: r.label, lx: pt[0], ly: pt[1] - 4 };
});

// ---------- points ----------
const fmtAc = a => a ? a.toLocaleString("en-US") : "";
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
  const hostLake = (lakeByKey[x.lakeKey] || {}).name || x.lakeName || (x.lakeKey === "squam" ? "Squam Lake" : "");
  pts.push({ id: "l" + i, cls: "listing", shape: "sq", name: x.name, lat: x.lat, lon: x.lon,
    meta: (hostLake ? hostLake + " · " : "") + (x.detail || "") + (x.status === "verify" ? " · status: confirm w/ broker" : ""),
    blurb: x.fit || "", links: [["Listing", x.url]], isNew: !!x.new });
});
for (const p of pts) { const xy = proj([p.lon, p.lat]); p.x = +xy[0].toFixed(1); p.y = +xy[1].toFixed(1); }

const CLS = {
  t1: { color: "#104281", r: 7.5 }, t2: { color: "#2a78d6", r: 5.5 },
  watch: { color: "#86b6ef", r: 4.5 }, listing: { color: "#eb6834", r: 5.5 }, ref: { color: "#52514e", r: 6 },
};
function markerSvg(p) {
  const c = CLS[p.cls];
  let shape;
  if (p.shape === "star") shape = `<path d="M0,-8 L2.2,-2.8 L8,-2.4 L3.6,1.4 L5,7 L0,3.8 L-5,7 L-3.6,1.4 L-8,-2.4 L-2.2,-2.8 Z" fill="#0b0b0b" stroke="#fcfcfb" stroke-width="1.4"/>`;
  else if (p.shape === "ring") shape = `<circle r="7" fill="none" stroke="#52514e" stroke-width="2.6"/><circle r="1.8" fill="#52514e"/>`;
  else if (p.shape === "sq") shape = `<rect x="-4.6" y="-4.6" width="9.2" height="9.2" rx="2" transform="rotate(45)" fill="${c.color}" stroke="#fcfcfb" stroke-width="1.4"/>`;
  else shape = `<circle r="${c.r}" fill="${c.color}" stroke="#fcfcfb" stroke-width="1.5"/>`;
  return `<g class="marker cls-${p.cls}" data-id="${p.id}" transform="translate(${p.x},${p.y})"><g class="mk">${shape}<circle class="hit" r="9" fill="transparent"/></g></g>`;
}
const zorder = { ref: 0, watch: 1, t2: 2, t1: 3, listing: 4 };
const markersSvg = [...pts].sort((a, b) => zorder[a.cls] - zorder[b.cls]).map(markerSvg).join("\n");

const LABELPOS = {
  kezar: { dx: 0, dy: -13, anchor: "middle" }, seymour: { dx: 0, dy: -13, anchor: "middle" },
  raquette: { dx: 11, dy: -8, anchor: "start" }, bigmoose: { dx: -11, dy: 14, anchor: "end" },
  silver_madison: { dx: 11, dy: 4, anchor: "start" }, parker_pond: { dx: 11, dy: -6, anchor: "start" },
  echo_lake_fayette: { dx: 11, dy: 13, anchor: "start" },
  squam: { dx: -13, dy: 4, anchor: "end" }, nyc: { dx: 0, dy: 19, anchor: "middle" },
};
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
function labelSvg(p) {
  const lp = LABELPOS[p.id]; if (!lp) return "";
  const txt = p.name.replace(/ \(the archetype\)/, " (archetype)").replace(/\s*\((Madison|Fayette)\)/, "").replace(/, (ME|VT|NY|NH)$/, "");
  return `<g class="lblg cls-${p.cls}" transform="translate(${p.x},${p.y})"><g class="mk"><text class="mlabel" x="${lp.dx}" y="${lp.dy}" text-anchor="${lp.anchor}">${esc(txt)}</text></g></g>`;
}
const labelsSvg = pts.map(labelSvg).join("");

// ---------- cards ----------
const nLakes = DATA.lakes.length, nList = DATA.listings.length;
const counts = { t1: DATA.lakes.filter(l => l.cls === "t1").length, t2: DATA.lakes.filter(l => l.cls === "t2").length,
  watch: DATA.lakes.filter(l => l.cls === "watch").length, listing: nList };
const GROUPS = [
  ["t1", `Tier 1 — pursue (${counts.t1})`],
  ["t2", `Tier 2 — strong (${counts.t2})`],
  ["listing", `Live listings (${counts.listing}) — snapshot Aug 18, 2026`],
  ["watch", `Watchlist / edge (${counts.watch})`],
  ["ref", "Reference points"],
];
function card(p) {
  const links = p.links.map(([t, u]) => `<a href="${u}" target="_blank" rel="noopener">${esc(t)} ↗</a>`).join(" · ");
  return `<div class="card cls-${p.cls}" data-id="${p.id}" tabindex="0">
    <div class="card-head"><span class="dot dot-${p.cls}${p.shape === "sq" ? " dot-sq" : ""}"></span><span class="card-name">${esc(p.name)}</span>${p.isNew ? '<span class="newpill">NEW</span>' : ""}</div>
    ${p.meta ? `<div class="card-meta">${esc(p.meta)}</div>` : ""}
    <div class="card-blurb">${esc(p.blurb)}</div>
    ${links ? `<div class="card-links">${links}</div>` : ""}
  </div>`;
}
const sections = GROUPS.map(([cls, title]) =>
  `<section class="grp grp-${cls}"><h2>${esc(title)}</h2>${pts.filter(p => p.cls === cls).map(card).join("\n")}</section>`
).join("\n");

// ---------- briefing + appendix ----------
let briefing = fs.readFileSync("briefing_content.html", "utf8");
const tierName = { t1: "Tier 1", t2: "Tier 2", watch: "Watch" };
const lakeRows = [...DATA.lakes].sort((a, b) => (zorder[b.cls] - zorder[a.cls]) || (b.score - a.score))
  .map(L => `<tr><td><strong>${esc(L.name)}</strong>${L.new ? ' <span class="newpill">NEW</span>' : ""}</td><td>${L.state}</td><td>${fmtAc(L.acres)}</td><td>${L.drive}</td><td>${tierName[L.cls]} · ${L.score}</td><td>${esc(L.blurb)}</td></tr>`).join("\n");
const exclBlocks = Object.entries(DATA.excluded).map(([region, items]) =>
  `<details><summary><strong>${esc(region)}</strong> — ${items.length} lakes evaluated and excluded (click to expand)</summary><ul>${items.map(e => `<li><strong>${esc(e.name)}:</strong> ${esc(e.reason)}</li>`).join("")}</ul></details>`).join("\n");
const appendix = `
<h2>Appendix — the full-region sweep (updated August 18, 2026)</h2>
<p>Four research passes evaluated every named lake of consequence in NH, ME (west/central/midcoast), NY, and VT — plus a certification pass over MA, CT, RI, PA, NJ and MD — against the archetype bar: ≤~6.5 h from Midtown, towsports legal and practical, ~450+ acres (rare exceptions justified), documented clear water, forested/quiet character, and private frontage that actually trades. <strong>${nLakes} lakes passed</strong> (${counts.t1} Tier 1, ${counts.t2} Tier 2, ${counts.watch} watchlist/edge) and <strong>${Object.values(DATA.excluded).reduce((a, b) => a + b.length, 0)} were evaluated and excluded</strong> with reasons below. The listings snapshot holds ${nList} live opportunities; the five most decision-relevant were re-verified individually on Aug 17–18 (Willoughby's $929K house-plus-four-cabins, the Winnecook lodge-and-cabins, the Tupper colony, Kezar's Blackberry Hill, Parker Pond's Dolloff estate). A note on honesty: a few standout <em>program</em> matches sit on lakes that failed the <em>water</em> bar (Unity Pond's lodge-and-six-cabins, Bomoseen's 60-acre golf-course parcel, Rainbow Lake's twin-lodge camp) — they're included with explicit caveats, never as recommendations.</p>
<p class="fine">New Hampshire nuance worth knowing: NH's "ski craft" bans are jet-ski bans — waterskiing behind boats remains legal on every passed lake, so PWC-banned lakes (Silver, Wentworth, Pleasant, Goose, Nubanusit, Waukewan) are actually the quietest Squam-like water in the state. Newfound Lake was promoted watch→Tier 2 on live-inventory evidence. Maine's four clarity standouts (Parker, Echo/Fayette, Peabody, Porter) all sit in the under-loved 30-Mile-River / western foothills belt — the sweep's biggest discovery.</p>
<h3>Every passing lake</h3>
<table class="btable"><thead><tr><th>Lake</th><th>St</th><th>Acres</th><th>Drive</th><th>Tier · fit</th><th>One-liner</th></tr></thead><tbody>
${lakeRows}
</tbody></table>
<h3>Evaluated and excluded — the honest ledger</h3>
${exclBlocks}
<p class="fine">Sources per lake are linked from the map popups (state monitoring programs: NHDES VLAP, Lakes of Maine / LEA / 30MRWA / 7 Lakes Alliance, NY DEC CSLAP/ALAP, VT DEC Lay Monitoring; motor rules: NH Marine Patrol restricted-waters list, Maine CMR ch.13 §07, NYS Navigation Law defaults, VT Use of Public Waters rules). Listing statuses move in days — re-confirm before touring.</p>`;
briefing = briefing.replace(/<\/div>\s*$/, appendix + "\n</div>");
briefing = briefing.replace('<h2 style="margin-top:6px">Executive summary</h2>',
  '<p class="fine" style="margin-top:4px">Updated August 18, 2026: the appendix below adds the full-region sweep — every qualifying lake and live listing in the Northeast. The original July analysis and recommendations stand.</p>\n<h2>Executive summary</h2>');

// ---------- html ----------
const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Finding Your Squam — Map & Briefing</title>
<style>
  :root{color-scheme:light;
    --page:#f9f9f7;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
    --hairline:#e1e0d9;--border:rgba(11,11,11,.10);
    --t1:#104281;--t2:#2a78d6;--watch:#86b6ef;--listing:#eb6834;--ref:#52514e;
    --ocean:#dbe8f4;--land:#f5f3ea;--stateline:#c2beb2}
  *{box-sizing:border-box}
  body{margin:0;background:var(--page);color:var(--ink);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
  header{padding:18px 22px 10px}
  header h1{margin:0;font-size:20px;letter-spacing:-.2px}
  header p{margin:4px 0 0;color:var(--ink2);font-size:13px}
  .tabs{display:flex;gap:8px;padding:2px 22px 0}
  .tab{padding:7px 18px;border:1px solid var(--border);border-radius:999px;background:var(--surface);color:var(--ink2);cursor:pointer;font-size:13px;font-weight:600}
  .tab.on{background:var(--t1);border-color:var(--t1);color:#fff}
  .tab:focus-visible{outline:2px solid var(--t2);outline-offset:2px}
  .legend{display:flex;flex-wrap:wrap;gap:8px;padding:10px 22px 12px;align-items:center}
  .chip{display:inline-flex;align-items:center;gap:7px;padding:5px 11px;border:1px solid var(--border);border-radius:999px;background:var(--surface);cursor:pointer;font-size:12.5px;color:var(--ink2);user-select:none}
  .chip .dot{width:10px;height:10px;border-radius:50%}
  .chip.off{opacity:.38}
  .legend .note{font-size:12px;color:var(--muted);margin-left:4px}
  .dot-t1{background:var(--t1)} .dot-t2{background:var(--t2)} .dot-watch{background:var(--watch)} .dot-ref{background:var(--ref)}
  .dot-listing{background:var(--listing)} .dot.dot-sq,.chip .dot.sq{border-radius:2px;transform:rotate(45deg)}
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
  #panel-brief{padding:16px 22px 30px}
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
  @media (max-width:900px){main{flex-direction:column}aside{flex:1 1 auto;max-height:none;max-width:none}.brief details ul{columns:1}}
</style></head>
<body>
<header>
  <h1>Finding Your Squam — the map</h1>
  <p>${nLakes} qualifying lakes across four states · ${nList} live listings · full-region sweep updated August 18, 2026 · click any marker to pin its info and links</p>
</header>
<div class="tabs" role="tablist">
  <button class="tab on" id="tab-map" role="tab" aria-selected="true">Map</button>
  <button class="tab" id="tab-brief" role="tab" aria-selected="false">Full briefing</button>
</div>
<div id="panel-map">
<div class="legend" id="legend">
  <span class="chip" data-cls="t1"><span class="dot dot-t1"></span>Tier 1 (${counts.t1})</span>
  <span class="chip" data-cls="t2"><span class="dot dot-t2"></span>Tier 2 (${counts.t2})</span>
  <span class="chip" data-cls="watch"><span class="dot dot-watch"></span>Watchlist (${counts.watch})</span>
  <span class="chip" data-cls="listing"><span class="dot dot-listing sq"></span>Listings (${counts.listing})</span>
  <span class="chip" data-cls="ref"><span class="dot dot-ref"></span>NYC ★ &amp; Squam ◎</span>
  <span class="note">dashed rings ≈ drive-time bands (rough) · scroll to zoom, drag to pan · search filters both map and list</span>
</div>
<main>
  <div class="mapwrap">
    <svg id="map" viewBox="0 0 ${W} ${H}" role="img" aria-label="Map of candidate lakes in the Northeast US">
      <g id="world">
        <g>${landPaths.map(d => `<path class="land" d="${d}"/>`).join("")}</g>
        <path class="stateline" d="${borderPath}"/>
        ${rings.map(r => `<path class="ring" d="${r.d}"/>`).join("")}
        ${rings.map(r => `<text class="ringlabel" x="${r.lx.toFixed(1)}" y="${r.ly.toFixed(1)}" text-anchor="middle">${r.label}</text>`).join("")}
        <g id="markers">${markersSvg}</g>
        <g id="labels">${labelsSvg}</g>
      </g>
    </svg>
    <div class="zoombtns">
      <button id="zin" aria-label="Zoom in">+</button>
      <button id="zout" aria-label="Zoom out">−</button>
      <button id="zreset" aria-label="Reset view" style="font-size:12px">⟲</button>
    </div>
    <div class="maptip" id="tip"></div>
    <div class="mappop" id="pop"><button class="close" id="popclose" aria-label="Close">✕</button><div id="popbody"></div></div>
    <div class="attribution">Basemap: US Census via us-atlas · locations approximate</div>
  </div>
  <aside id="cards">
    <div class="searchbox"><input id="q" type="search" placeholder="Search ${nLakes} lakes + ${nList} listings — try a lake, state, or price…" aria-label="Search"></div>
    ${sections}
  </aside>
</main>
<footer>Companion to the full briefing (second tab). Listing status changes fast — re-confirm with brokers before touring. Drive times are non-peak estimates from Midtown; rings are straight-line approximations, not isochrones. Trout Lake, WI — your other archetype — is off-map at ~17 hours' drive; its buildable stand-ins here are the state-forest-ringed lakes (Maidstone, Webb, Piseco, Mooselookmeguntic, Richardson).</footer>
</div>
<div id="panel-brief" hidden>${briefing}</div>
<script>
  const PTS = ${JSON.stringify(pts.map(({ id, name, meta, blurb, clarity, motors, cls, x, y, links }) => ({ id, name, meta, blurb, clarity, motors, cls, x, y, links })))};
  const byId = Object.fromEntries(PTS.map(p => [p.id, p]));
  const svg = document.getElementById("map"), world = document.getElementById("world"), tip = document.getElementById("tip");
  const wrap = document.querySelector(".mapwrap");
  const pop = document.getElementById("pop"), popbody = document.getElementById("popbody");
  let k = 1, tx = 0, ty = 0, pinned = null, moved = false;
  function apply() {
    world.setAttribute("transform", \`translate(\${tx},\${ty}) scale(\${k})\`);
    document.querySelectorAll(".mk").forEach(g => g.setAttribute("transform", \`scale(\${1 / Math.pow(k, 0.85)})\`));
    positionPop();
  }
  function markerScreen(id) {
    const p = byId[id], r = svg.getBoundingClientRect();
    return [(p.x * k + tx) * r.width / ${W}, (p.y * k + ty) * r.height / ${H}];
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
    const wq = (p.clarity ? '<div class="wq"><b2>Water:</b2> ' + p.clarity + "</div>" : "") +
               (p.motors ? '<div class="wq"><b2>Motors:</b2> ' + p.motors + "</div>" : "");
    popbody.innerHTML = "<b>" + p.name + "</b>" + (p.meta ? '<div class="m">' + p.meta + "</div>" : "") + '<div class="bl">' + p.blurb + "</div>" + wq + linksHtml;
    pop.style.display = "block"; tip.style.display = "none";
    positionPop();
  }
  function unpin() { pinned = null; pop.style.display = "none"; }
  document.getElementById("popclose").addEventListener("click", unpin);
  document.addEventListener("keydown", e => { if (e.key === "Escape") unpin(); });
  function zoomAt(f, cx, cy) {
    const nk = Math.min(14, Math.max(1, k * f)); f = nk / k;
    tx = cx - (cx - tx) * f; ty = cy - (cy - ty) * f; k = nk;
    if (k === 1) { tx = 0; ty = 0; }
    apply();
  }
  function svgPoint(e) {
    const r = svg.getBoundingClientRect();
    return [(e.clientX - r.left) * ${W} / r.width, (e.clientY - r.top) * ${H} / r.height];
  }
  svg.addEventListener("wheel", e => { e.preventDefault(); const [cx, cy] = svgPoint(e); zoomAt(e.deltaY < 0 ? 1.25 : 0.8, cx, cy); }, { passive: false });
  document.getElementById("zin").onclick = () => zoomAt(1.4, ${W / 2}, ${H / 2});
  document.getElementById("zout").onclick = () => zoomAt(0.71, ${W / 2}, ${H / 2});
  document.getElementById("zreset").onclick = () => { k = 1; tx = 0; ty = 0; apply(); };
  let drag = null;
  svg.addEventListener("pointerdown", e => { drag = { x: e.clientX, y: e.clientY, tx, ty }; moved = false; svg.classList.add("panning"); });
  window.addEventListener("pointermove", e => {
    if (!drag) return;
    if (Math.abs(e.clientX - drag.x) + Math.abs(e.clientY - drag.y) > 5) moved = true;
    if (!moved) return;
    const r = svg.getBoundingClientRect(), s = ${W} / r.width;
    tx = drag.tx + (e.clientX - drag.x) * s; ty = drag.ty + (e.clientY - drag.y) * s; apply();
  });
  window.addEventListener("pointerup", () => { drag = null; svg.classList.remove("panning"); });
  let activeId = null;
  function setActive(id, scroll) {
    activeId = id;
    document.querySelectorAll(".marker").forEach(m => m.classList.toggle("active", m.dataset.id === id));
    document.querySelectorAll(".card").forEach(c => {
      const on = c.dataset.id === id;
      c.classList.toggle("active", on);
      if (on && scroll) c.scrollIntoView({ block: "nearest", behavior: "smooth" });
    });
  }
  document.querySelectorAll(".marker").forEach(m => {
    m.addEventListener("pointerenter", e => {
      const p = byId[m.dataset.id]; if (!p || pinned === m.dataset.id) return;
      tip.innerHTML = "<b>" + p.name + "</b>" + (p.meta ? '<div class="m">' + p.meta + "</div>" : "") + '<div>' + p.blurb + "</div><div class='m'>click to pin info + links</div>";
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
  document.querySelectorAll(".card").forEach(c => {
    c.addEventListener("click", e => { if (e.target.tagName === "A") return; setActive(c.dataset.id, false); pinPopup(c.dataset.id); });
  });
  svg.addEventListener("click", () => { if (moved) { moved = false; return; } setActive(null, false); unpin(); });
  // visibility = chips ∩ search
  const off = new Set();
  let query = "";
  function matches(p) {
    if (!query) return true;
    return (p.name + " " + (p.meta || "") + " " + (p.blurb || "")).toLowerCase().includes(query);
  }
  function refresh() {
    document.querySelectorAll(".marker").forEach(m => {
      const p = byId[m.dataset.id];
      m.classList.toggle("dim", off.has(p.cls) || !matches(p));
    });
    document.querySelectorAll(".card").forEach(c => {
      const p = byId[c.dataset.id];
      c.classList.toggle("hidden", !matches(p));
    });
    document.querySelectorAll(".grp").forEach(g => {
      const c = [...g.classList].find(x => x.startsWith("grp-")).slice(4);
      const anyVisible = [...g.querySelectorAll(".card")].some(cd => !cd.classList.contains("hidden"));
      g.classList.toggle("hidden", off.has(c) || !anyVisible);
    });
    if (pinned && (off.has(byId[pinned].cls) || !matches(byId[pinned]))) unpin();
  }
  document.querySelectorAll(".chip").forEach(ch => {
    ch.addEventListener("click", () => {
      const cls = ch.dataset.cls;
      if (off.has(cls)) off.delete(cls); else off.add(cls);
      ch.classList.toggle("off", off.has(cls));
      refresh();
    });
  });
  document.getElementById("q").addEventListener("input", e => { query = e.target.value.trim().toLowerCase(); refresh(); });
  // tabs
  const tabMap = document.getElementById("tab-map"), tabBrief = document.getElementById("tab-brief");
  const panelMap = document.getElementById("panel-map"), panelBrief = document.getElementById("panel-brief");
  function showTab(which) {
    const mapOn = which === "map";
    tabMap.classList.toggle("on", mapOn); tabBrief.classList.toggle("on", !mapOn);
    tabMap.setAttribute("aria-selected", mapOn); tabBrief.setAttribute("aria-selected", !mapOn);
    panelMap.hidden = !mapOn; panelBrief.hidden = mapOn;
  }
  tabMap.addEventListener("click", () => showTab("map"));
  tabBrief.addEventListener("click", () => showTab("brief"));
  apply();
</script>
</body></html>`;
fs.writeFileSync("../index.html", html);
console.log("WROTE lake_map.html", html.length, "bytes,", pts.length, "points,", nLakes, "lakes,", nList, "listings");
