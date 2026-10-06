/* Letterhead, footer and stamp for every PDF.
   If assets/config.js gives image files (BRAND.letterhead.header / footer / stamp) those are used.
   Otherwise they are drawn here from the company details and colours in assets/config.js,
   so a re-brand never needs new image files.
   Usage: const {header, footer, stamp} = await window.brandLetterhead();
          each one is {dataUrl, url, w, h}  (header/footer are JPEG, stamp is PNG) */
(function () {
  const B = window.BRAND;
  let cache = null;

  const loadImg = src => new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => no(new Error(src + ' not found')); i.src = src; });
  const toData = (cv, type) => { const d = cv.toDataURL(type, .93); return {dataUrl: d, url: d, w: cv.width, h: cv.height}; };
  // your own image file: redrawn so the PDF code always gets JPEG for header/footer and PNG for the stamp
  const fromFile = async (src, type) => {
    const i = await loadImg(src), c = document.createElement('canvas'); c.width = i.naturalWidth; c.height = i.naturalHeight;
    const x = c.getContext('2d'); if (type === 'image/jpeg') { x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); }
    x.drawImage(i, 0, 0); return toData(c, type);
  };
  const canvas = (w, h, bg) => { const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d');
    if (bg) { x.fillStyle = bg; x.fillRect(0, 0, w, h); } return [c, x]; };
  const EN = '"IBM Plex Sans", "Segoe UI", Arial, sans-serif', AR = '"IBM Plex Sans Arabic", "Segoe UI", Tahoma, Arial, sans-serif';
  const fit = (x, text, font, size, max) => { let s = size; do { x.font = font.replace('{s}', s); s -= 1; } while (x.measureText(text).width > max && s > 10); };

  async function fonts() {
    if (!document.fonts) return;
    try { await Promise.race([Promise.all(['600 40px "IBM Plex Sans"', '400 30px "IBM Plex Sans"', '600 40px "IBM Plex Sans Arabic"']
      .map(f => document.fonts.load(f, 'Aب'))), new Promise(r => setTimeout(r, 2500))]); } catch (e) {}
  }

  async function drawHeader(logo) {
    const W = 1600, H = 234, c = B.colors, [cv, x] = canvas(W, H, '#FFFFFF');
    // logo in the middle
    const lh = 150, lw = logo ? lh * logo.naturalWidth / logo.naturalHeight : 0;
    if (logo) x.drawImage(logo, (W - lw) / 2, 18, lw, lh);
    // English name, left: first word in the accent colour, rest in the brand colour
    const words = B.name.split(' '), first = words.shift(), rest = words.join(' ');
    x.textBaseline = 'alphabetic'; x.textAlign = 'left';
    fit(x, first, `600 {s}px ${EN}`, 52, 560); x.fillStyle = c.accent; x.fillText(first.toUpperCase(), 58, 82);
    fit(x, rest, `600 {s}px ${EN}`, 50, 560); x.fillStyle = c.brand; x.fillText(rest.toUpperCase(), 58, 140);
    // Arabic name, right
    x.textAlign = 'right'; x.direction = 'rtl';
    fit(x, B.nameAr, `600 {s}px ${AR}`, 54, 560); x.fillStyle = c.brand; x.fillText(B.nameAr, W - 58, 92);
    fit(x, B.taglineAr, `400 {s}px ${AR}`, 30, 560); x.fillStyle = c.accent; x.fillText(B.taglineAr, W - 58, 140);
    x.direction = 'ltr';
    // rule with a gap for the logo
    x.fillStyle = c.accent; const gap = Math.max(lw, 120) / 2 + 40;
    x.fillRect(0, 186, W / 2 - gap, 6); x.fillRect(W / 2 + gap, 186, W / 2 - gap, 6);
    x.textAlign = 'center'; fit(x, B.short, `600 {s}px ${EN}`, 34, 2 * gap - 20); x.fillStyle = c.brand;
    x.fillText(B.short.toUpperCase(), W / 2, 210);
    return toData(cv, 'image/jpeg');
  }

  function icon(x, kind, cx, cy, r, color) {
    x.fillStyle = color; x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill();
    x.strokeStyle = '#fff'; x.fillStyle = '#fff'; x.lineWidth = 3; x.lineCap = 'round'; x.lineJoin = 'round';
    x.beginPath();
    if (kind === 'phone') { x.roundRect(cx - 8, cy - 13, 16, 26, 3); x.stroke(); x.beginPath(); x.arc(cx, cy + 8, 1.6, 0, 7); x.fill(); }
    if (kind === 'mail') { x.rect(cx - 12, cy - 8, 24, 16); x.moveTo(cx - 12, cy - 8); x.lineTo(cx, cy + 2); x.lineTo(cx + 12, cy - 8); x.stroke(); }
    if (kind === 'web') { x.arc(cx, cy, 12, 0, 7); x.moveTo(cx - 12, cy); x.lineTo(cx + 12, cy); x.ellipse(cx, cy, 5, 12, 0, 0, 7); x.stroke(); }
    if (kind === 'pin') { x.arc(cx, cy - 3, 9, Math.PI * .8, Math.PI * 2.2); x.lineTo(cx, cy + 13); x.closePath(); x.fill();
      x.fillStyle = color; x.beginPath(); x.arc(cx, cy - 3, 3.5, 0, 7); x.fill(); }
  }

  function drawFooter() {
    const W = 1600, H = 212, c = B.colors, [cv, x] = canvas(W, H, '#FFFFFF');
    x.fillStyle = c.accent; x.fillRect(28, 0, W - 56, 4);
    x.fillStyle = c.brand; x.fillRect(0, 178, W, 34);
    const cols = [['phone', B.phones.slice(0, 3)], ['mail', [B.email]], ['web', [B.website]], ['pin', ['Address', ...wrap(B.address, 30)]]];
    const cw = (W - 120) / cols.length;
    cols.forEach(([k, lines], i) => {
      const x0 = 70 + i * cw; icon(x, k, x0 + 22, 52, 22, c.accent);
      x.fillStyle = '#1F2D35'; x.textAlign = 'left'; x.textBaseline = 'middle';
      lines.forEach((t, j) => { fit(x, t, `${k === 'pin' && j === 0 ? 600 : 400} {s}px ${EN}`, k === 'pin' && j ? 22 : 27, cw - 80); x.fillText(t, x0 + 60, 54 + j * (k === 'pin' ? 30 : 36)); });
    });
    return toData(cv, 'image/jpeg');
  }
  function wrap(t, n) { const out = []; let line = ''; String(t).split(/\s+/).forEach(w => { if ((line + ' ' + w).trim().length > n) { out.push(line.trim()); line = w; } else line += ' ' + w; }); if (line.trim()) out.push(line.trim()); return out.slice(0, 3); }

  function drawStamp() {
    // a rubber stamp in blue ink: double border, Arabic + English name, CR number
    const W = 565, H = 229, [cv, x] = canvas(W, H), ink = '#28368C';
    x.translate(W / 2, H / 2); x.rotate(-0.035); x.translate(-W / 2, -H / 2);
    x.globalAlpha = .9; x.strokeStyle = ink; x.fillStyle = ink;
    x.lineWidth = 6; x.beginPath(); x.roundRect(10, 10, W - 20, H - 20, 40); x.stroke();
    x.lineWidth = 2.5; x.beginPath(); x.roundRect(24, 24, W - 48, H - 48, 30); x.stroke();
    x.textAlign = 'center'; x.textBaseline = 'middle';
    x.direction = 'rtl'; fit(x, B.nameAr, `600 {s}px ${AR}`, 46, W - 90); x.fillText(B.nameAr, W / 2, 70); x.direction = 'ltr';
    fit(x, B.name.toUpperCase(), `600 {s}px ${EN}`, 40, W - 90); x.fillText(B.name.toUpperCase(), W / 2, 122);
    x.fillRect(70, 148, W - 140, 2.5);
    fit(x, `C.R. ${B.crNo}  ·  ${B.city.toUpperCase()}`, `500 {s}px ${EN}`, 26, W - 120); x.fillText(`C.R. ${B.crNo}  ·  ${B.city.toUpperCase()}`, W / 2, 178);
    // a little ink wear so it looks stamped, not printed
    x.globalCompositeOperation = 'destination-out';
    let seed = 7; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
    for (let i = 0; i < 900; i++) { x.globalAlpha = rnd() * .5; x.beginPath(); x.arc(rnd() * W, rnd() * H, rnd() * 2.2, 0, 7); x.fill(); }
    return toData(cv, 'image/png');
  }

  window.brandLetterhead = () => cache || (cache = (async () => {
    const L = B.letterhead || {};
    await fonts();
    let logo = null; try { logo = await loadImg(B.logo); } catch (e) {}
    const [header, footer, stamp] = await Promise.all([
      L.header ? fromFile(L.header, 'image/jpeg') : drawHeader(logo),
      L.footer ? fromFile(L.footer, 'image/jpeg') : drawFooter(),
      L.stamp ? fromFile(L.stamp, 'image/png') : drawStamp()]);
    return {header, footer, stamp};
  })().catch(e => { cache = null; throw e; }));
})();
