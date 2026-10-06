/* =====================================================================
   Added to the end of every company's config.js by tools/build.py.
   Works out colour shades and applies the brand to the page. No need to edit.
   ===================================================================== */
(function () {
  const B = window.BRAND;
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
  const fix = () => { document.title = document.title.replace(/\{portal\}/g, B.portalName).replace(/\{company\}/g, B.name).replace(/\{short\}/g, B.short); };
  fix(); document.addEventListener('DOMContentLoaded', () => {
    fix();
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
