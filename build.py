#!/usr/bin/env python3
"""Builds the website: one shared portal (app/) for every company in clients/.

    python3 tools/build.py                   -> dist/           landing page + every company in a folder (GitHub Pages demo site)
    python3 tools/build.py --only trading    -> dist/           just that company's portal, at the root of the site
                                                                (one Cloudflare Pages site per client, each with its own domain)

dist/
  index.html, assets/, samples/       the product landing page (from landing/)
  demos.js                            list of demo companies, read by the landing page
  <company>/                          the full portal for that company:
      every file from app/
      assets/config.js                = clients/<company>/config.js + app/assets/config-derived.js
      assets/logo.svg, icons          from clients/<company>/
      manifest.webmanifest            app name and colour of that company

GitHub Actions runs this on every push (.github/workflows/pages.yml) and publishes dist/.
Nothing in dist/ is edited by hand.
"""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
APP, LANDING, CLIENTS = (os.path.join(ROOT, d) for d in ('app', 'landing', 'clients'))


def read_brand(config_js):
    """Reads the few BRAND values the landing page and manifest need (without running JavaScript)."""
    brand = config_js.split('window.BRAND', 1)[1]
    s = lambda k: (re.search(r'\b' + k + r"\s*:\s*'([^']*)'", brand) or [None, ''])[1]
    colors = re.search(r"colors\s*:\s*\{brand:\s*'([^']+)',\s*accent:\s*'([^']+)'", brand)
    url = re.search(r"SUPABASE_URL\s*:\s*'([^']*)'", config_js).group(1)
    key = re.search(r"SUPABASE_ANON_KEY\s*:\s*'([^']*)'", config_js).group(1)
    return {'name': s('name'), 'nameAr': s('nameAr'), 'short': s('short'), 'tagline': s('tagline'), 'industry': s('industry'),
            'portalName': s('portalName'), 'brand': colors.group(1), 'accent': colors.group(2),
            'ready': bool(url) and 'YOUR-PROJECT' not in url and key.startswith(('eyJ', 'sb_publishable_'))}


def build_company(c, out, derived):
    """Copies the shared portal into out/ and applies company c's settings, logo and app name."""
    cdir = os.path.join(CLIENTS, c)
    shutil.copytree(APP, out, ignore=shutil.ignore_patterns('config-derived.js'), dirs_exist_ok=True)
    cfg = open(os.path.join(cdir, 'config.js'), encoding='utf-8').read()
    open(os.path.join(out, 'assets', 'config.js'), 'w', encoding='utf-8').write(cfg.rstrip() + '\n\n' + derived)
    for f in ('logo.svg', 'icon-192.png', 'icon-512.png', 'favicon.png'):
        src = os.path.join(cdir, f)
        if os.path.exists(src): shutil.copy(src, os.path.join(out, 'assets', f))
    b = read_brand(cfg)
    man = json.load(open(os.path.join(APP, 'manifest.webmanifest'), encoding='utf-8'))
    man.update(name=b['portalName'] or b['name'], short_name=b['short'] or b['name'], theme_color=b['brand'],
               description=f"Documents, inventory and employees for {b['name']}")
    json.dump(man, open(os.path.join(out, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    sw = os.path.join(out, 'sw.js')
    open(sw, 'w', encoding='utf-8').write(open(sw, encoding='utf-8').read().replace('__CLIENT__', c))
    return b


def build_only(c):
    """One company's portal at the root of dist/ (for its own site and domain)."""
    if not os.path.isfile(os.path.join(CLIENTS, c, 'config.js')):
        raise SystemExit(f'No company "{c}": expected clients/{c}/config.js')
    if os.path.exists(DIST): shutil.rmtree(DIST)
    derived = open(os.path.join(APP, 'assets', 'config-derived.js'), encoding='utf-8').read()
    b = build_company(c, DIST, derived)
    # the site root opens the portal (index.html sends signed-out visitors to the login page)
    open(os.path.join(DIST, '.nojekyll'), 'w').close()
    print(f'dist/ built for {c}: {b["name"]}' + ('' if b['ready'] else '  (WARNING: Supabase URL/key not set in config.js)'))


def build():
    if os.path.exists(DIST): shutil.rmtree(DIST)
    shutil.copytree(LANDING, DIST)
    derived = open(os.path.join(APP, 'assets', 'config-derived.js'), encoding='utf-8').read()
    # the landing page's own settings + the same colour helpers the portal uses
    product = os.path.join(DIST, 'assets', 'product.js')
    open(os.path.join(DIST, 'assets', 'config.js'), 'w', encoding='utf-8').write(open(product, encoding='utf-8').read().rstrip() + '\n\n' + derived)
    os.remove(product)
    demos = []
    for c in sorted(os.listdir(CLIENTS)):
        cdir = os.path.join(CLIENTS, c)
        if not os.path.isfile(os.path.join(cdir, 'config.js')): continue
        b = build_company(c, os.path.join(DIST, c), derived)
        demos.append(dict(b, id=c, link=f'{c}/login.html?demo=1', logo=f'{c}/assets/logo.svg'))
        print(f'  {c:14s} {b["name"]}  ({"ready" if b["ready"] else "Supabase not set yet - shown as coming soon"})')
    demos.sort(key=lambda d: (not d['ready'], d['id']))          # ready demos first
    open(os.path.join(DIST, 'demos.js'), 'w', encoding='utf-8').write(
        '// generated by tools/build.py from clients/*/config.js\nwindow.DEMOS = ' + json.dumps(demos, ensure_ascii=False, indent=1) + ';\n')
    open(os.path.join(DIST, '.nojekyll'), 'w').close()
    print('dist/ built:', len(demos), 'companies')


if __name__ == '__main__':
    import sys
    a = sys.argv[1:]
    if a[:1] == ['--only'] and len(a) == 2: build_only(a[1])
    elif not a: build()
    else: sys.exit(__doc__)
