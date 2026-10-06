/* =====================================================================
   Live world map for the sign-in page (instead of the clock).
   Turned on per company in config.js:  BRAND.loginVisual = 'map'

   Shows: the world with day and night as they are right now (moves every
   minute), the company's office, and the visitor's approximate location
   from their IP address (city level, can be wrong on VPN / mobile data),
   with the distance to the office and both local times.

   Libraries (d3-geo, topojson, world map) load from jsDelivr only when the
   map is switched on. The IP lookup uses ipwho.is (free, no key); if it fails
   the map simply shows the office.
   ===================================================================== */
(() => {
  const CDN = 'https://cdn.jsdelivr.net/npm/';
  const load = src => new Promise((ok, bad) => { const s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = bad; document.head.appendChild(s); });
  const NS = 'http://www.w3.org/2000/svg';
  const W = 640, H = 330;

  // sun position (good enough for a map): the point on Earth where the sun is overhead
  function subsolar(date) {
    const d = (date - Date.UTC(2000, 0, 1, 12)) / 864e5;                       // days since J2000
    const g = (357.529 + 0.98560028 * d) * Math.PI / 180;                       // mean anomaly
    const q = 280.459 + 0.98564736 * d;                                         // mean longitude
    const L = (q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * Math.PI / 180;
    const e = (23.439 - 0.00000036 * d) * Math.PI / 180;
    const dec = Math.asin(Math.sin(e) * Math.sin(L));
    const ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L));
    const gmst = (18.697374558 + 24.06570982441908 * d) % 24;                   // hours
    let lon = (ra * 180 / Math.PI) - gmst * 15;
    lon = ((lon + 540) % 360) - 180;
    return [lon, dec * 180 / Math.PI];
  }
  const km = (a, b) => Math.round(d3.geoDistance(a, b) * 6371);
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

  window.drawLoginMap = async function ({box, office, brand, accent, officeTz}) {
    await load(CDN + 'd3-array@3/dist/d3-array.min.js');
    await load(CDN + 'd3-geo@3/dist/d3-geo.min.js');
    await load(CDN + 'topojson-client@3/dist/topojson-client.min.js');
    const world = await fetch(CDN + 'world-atlas@2/countries-110m.json').then(r => r.json());
    const land = topojson.feature(world, world.objects.land);
    const borders = topojson.mesh(world, world.objects.countries, (a, b) => a !== b);
    const home = topojson.feature(world, world.objects.countries).features.find(f => +f.id === (office.countryId || 682));

    const proj = d3.geoEqualEarth().fitExtent([[8, 8], [W - 8, H - 8]], {type: 'Sphere'});
    const path = d3.geoPath(proj);
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.setAttribute('class', 'worldmap'); svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'World map with day and night, our office and your location');
    const add = (tag, attrs, parent = svg) => { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); parent.appendChild(n); return n; };

    const defs = add('defs', {});
    const clip = add('clipPath', {id: 'mapSphere'}, defs); add('path', {d: path({type: 'Sphere'})}, clip);
    add('path', {d: path({type: 'Sphere'}), fill: '#F4F8FA', stroke: brand, 'stroke-opacity': .18});
    add('path', {d: path(d3.geoGraticule10()), fill: 'none', stroke: brand, 'stroke-opacity': .07});
    add('path', {d: path(land), fill: '#CAD5DB'});
    add('path', {d: path(borders), fill: 'none', stroke: '#fff', 'stroke-width': .6});
    if (home) add('path', {d: path(home), fill: brand, 'fill-opacity': .28, stroke: brand, 'stroke-opacity': .5, 'stroke-width': .7});
    const night = add('path', {fill: '#0F1C2E', 'fill-opacity': .26, 'clip-path': 'url(#mapSphere)'});
    const sun = add('circle', {r: 5, fill: '#F2B33D', stroke: '#fff', 'stroke-width': 1.5});
    const arc = add('path', {fill: 'none', stroke: accent, 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-dasharray': '4 6', class: 'maparc'});
    const pin = (lonlat, color, label, big) => {
      const [x, y] = proj(lonlat), g = add('g', {transform: `translate(${x},${y})`});
      if (big) add('circle', {r: 9, fill: color, 'fill-opacity': .25, class: 'mappulse'}, g);
      add('circle', {r: big ? 5 : 4.5, fill: color, stroke: '#fff', 'stroke-width': 2}, g);
      const t = add('text', {x: x > W - 140 ? -10 : 10, y: -8, 'text-anchor': x > W - 140 ? 'end' : 'start', class: 'maplabel'}, g);
      t.textContent = label;
      return g;
    };
    const officePin = pin(office.lonlat, brand, office.label, true);

    function tick() {
      const s = subsolar(new Date());
      night.setAttribute('d', path(d3.geoCircle().center([s[0] + 180, -s[1]]).radius(90)()));
      const [x, y] = proj(s); sun.setAttribute('cx', x); sun.setAttribute('cy', y);
    }
    tick(); setInterval(tick, 60e3);
    box.querySelector('.mapsvg').replaceChildren(svg);

    // visitor location from IP (approximate)
    const info = box.querySelector('.mapinfo');
    const fmt = tz => new Intl.DateTimeFormat('en-GB', {timeZone: tz, hour: '2-digit', minute: '2-digit', hour12: false});
    try {
      const g = await fetch('https://ipwho.is/?fields=success,city,country,latitude,longitude,timezone').then(r => r.json());
      if (!g.success || g.latitude == null) throw 0;
      const you = [g.longitude, g.latitude], dist = km(you, office.lonlat);
      if (dist > 25) {
        const line = d3.geoInterpolate(you, office.lonlat);
        arc.setAttribute('d', path({type: 'LineString', coordinates: d3.range(0, 1.0001, .02).map(line)}));
      }
      if (dist > 25) pin(you, accent, 'You', false);
      else officePin.querySelector('text').textContent = office.label + ' · you are here';
      const yourTz = g.timezone && g.timezone.id;
      const sameTz = !yourTz || fmt(yourTz).format(new Date()) === fmt(officeTz).format(new Date());
      info.innerHTML = `<b>You are in ${esc([g.city, g.country].filter(Boolean).join(', '))}</b>
        <span>${dist > 25 ? `${dist.toLocaleString('en-US')} km from our office in ${esc(office.city)}` : `Near our office in ${esc(office.city)}`}${sameTz ? '' : ` · your time <i id="mapYou"></i>`}</span>`;
      if (!sameTz) { const t = () => { const e = document.getElementById('mapYou'); if (e) e.textContent = fmt(yourTz).format(new Date()); }; t(); setInterval(t, 30e3); }
    } catch (e) {
      info.innerHTML = `<b>Our office: ${esc(office.city)}</b><span>Day and night shown live</span>`;
    }
  };
})();
