/* =====================================================================
   Added to the end of every company's config.js by tools/build.py.
   Works out colour shades and applies the brand to the page. No need to edit.
   ===================================================================== */
(function () {
  const B = window.BRAND;
  const PROVIDER = window.RABTFLOW = Object.freeze({name: 'RabtFlow', website: 'https://portfolio.azeemsyedb.workers.dev/', logo: 'assets/rabtflow-logo.svg', pdfLogo: 'assets/rabtflow-logo.png'});
  const hex = h => { h = h.replace('#', ''); return [0, 2, 4].map(i => parseInt(h.substr(i, 2), 16)); };
  const toHex = a => '#' + a.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');
  const mix = (a, b, t) => toHex(hex(a).map((v, i) => v + (hex(b)[i] - v) * t));
  B.rgb = hex; B.mix = mix;
  const c = B.colors;
  c.brandDark = mix(c.brand, '#000000', .25);
  c.brandDeep = mix(c.brand, '#000000', .45);
  c.brandLight = mix(c.brand, '#FFFFFF', .88);
  c.brandSoft = mix(c.brand, '#FFFFFF', .7);
  c.accentLight = mix(c.accent, '#FFFFFF', .85);
  c.brandRgb = hex(c.brand).join(',');
  B.phone = B.phones[0];
  B.signature = `\n\nRegards,\n${B.name}\n${B.phone}`;
  // colour tokens for every page (pages that load their own CSS use these too)
  const css = `:root{--ah-brand:${c.brand};--ah-brand-d:${c.brandDark};--ah-brand-l:${c.brandLight};--ah-orange:${c.accent};
    --brand:${c.brand};--brand-d:${c.brandDark};--brand-deep:${c.brandDeep};--brand-l:${c.brandLight};--brand-rgb:${c.brandRgb};
    --accent:${c.accent};--accent-l:${c.accentLight};--steel:${c.brand};--steel2:${c.brandDark};--teal:${c.brand};--teal-dark:${c.brandDark}}`;
  const s = document.createElement('style'); s.id = 'brand-tokens'; s.textContent = css;
  (document.head || document.documentElement).appendChild(s);
  // the page <title> follows the brand: pages write "Section | {portal}"
  const fix = () => { document.title = document.title.replace(/\{portal\}/g, B.portalName).replace(/\{company\}/g, B.name).replace(/\{short\}/g, B.short);
    if (!document.title.includes('RabtFlow')) document.title += ' · RabtFlow';
  };
  fix(); document.addEventListener('DOMContentLoaded', () => {
    fix();
    // Default provider attribution is shared by every client build.
    if (!document.getElementById('rabtflow-credit')) {
      const css = document.createElement('style');
      css.textContent = '.rf-credit{display:flex;justify-content:center;align-items:center;gap:9px;flex-wrap:wrap;margin:24px 16px;padding:14px 8px;font:400 12px/1.5 system-ui,sans-serif;color:#53666e;text-align:center;direction:ltr}.rf-credit a{display:inline-flex;align-items:center;gap:9px;color:inherit;text-decoration:none;max-width:100%}.rf-credit a:hover{text-decoration:underline}.rf-credit img{display:block;width:108px;height:auto;background:#fff;padding:5px 7px;border-radius:5px;box-sizing:content-box}.card .rf-credit{margin:22px 0 0;padding:16px 0 0;border-top:1px solid var(--line,#dbe4e8)}@media print{.rf-credit{display:none}}';
      document.head.appendChild(css);
      const credit = document.createElement('footer'); credit.id = 'rabtflow-credit'; credit.className = 'rf-credit';
      const link = document.createElement('a'); link.href = PROVIDER.website; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.setAttribute('aria-label', 'Powered by RabtFlow — Business Systems & Automation');
      const label = document.createElement('span'); label.textContent = 'Powered by';
      const logo = document.createElement('img'); logo.src = PROVIDER.logo; logo.alt = PROVIDER.name; logo.width = 108; logo.height = 24;
      link.append(label, logo); credit.appendChild(link);
      const host = /(?:^|\/)login(?:\.html)?$/.test(location.pathname) ? document.querySelector('main.card') : document.body;
      (host || document.body).appendChild(credit);
    }
    // any element with data-brand="name|nameAr|short|tagline|portalName|..." gets that text
    document.querySelectorAll('[data-brand]').forEach(el => { const v = B[el.dataset.brand]; if (v != null) el.textContent = v; });
    document.querySelectorAll('img[data-brand-logo]').forEach(el => { el.src = B.logo; });
    // document types switched off above disappear from the Documents menu
    const T = B.docTypes || {};
    document.querySelectorAll('[data-t]').forEach(el => { if (T[el.dataset.t] === false) el.remove(); });
    document.querySelectorAll('[data-g]:not([data-t])').forEach(g => { const first = document.querySelector(`[data-t][data-g="${g.dataset.g}"]`);
      if (!first) g.remove(); else g.setAttribute('href', first.getAttribute('href')); });
  });
})();
