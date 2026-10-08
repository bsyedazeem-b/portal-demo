# Business Portal — product + live demos

A business portal for any company: quotations, invoices with ZATCA QR, cash receipts, delivery notes, job cards,
purchase orders, stock with barcode scanning, check-in kiosk, attendance, overtime, tasks and payroll. It runs on
**GitHub Pages** (the website) and **Supabase** (database and logins), so there is no server to run.

**One code, many companies.** The portal code lives once in `app/`. Each company only has its own settings
(`clients/<company>/config.js`), logo and sample data, and its own Supabase project. A fix or new feature in `app/`
reaches every company at the next build.

## Demo companies

| Folder | Company | Industry | Supabase |
|---|---|---|---|
| `clients/trading/` | Safwa Trading & Distribution Co. | Food & FMCG wholesale | the existing demo project |
| `clients/contracting/` | Bunyan Contracting & Maintenance Est. | MEP, fit-out, maintenance | new project (see below) |

All companies, people, numbers and documents are invented. Every demo resets itself every night.

## What is where

```
app/                     the portal (shared by every company) — html pages, assets/, sw.js, manifest
clients/<company>/
    config.js            name, Arabic name, colours, modules, document types, inventory categories, Supabase keys
    logo.svg, icons      logo and phone-app icons
    seed_data.py         sample data: customers, products, employees, documents (edit this to change the demo)
    supabase_install.sql GENERATED: paste in that company's Supabase SQL Editor (schema + sample data)
landing/                 product landing page (index.html) + assets/product.js (your name, WhatsApp, card texts)
sql/                     database schema, shared by every company
tools/make_demo_seed.py  seed_data.py -> supabase_install.sql      python3 tools/make_demo_seed.py --all
tools/build.py           builds the website into dist/              python3 tools/build.py
.github/workflows/       on every push: build + publish on GitHub Pages
```

Website after publishing:

```
https://<user>.github.io/portal-demo/               landing page with a card per demo company
https://<user>.github.io/portal-demo/trading/       Safwa Trading portal
https://<user>.github.io/portal-demo/contracting/   Bunyan Contracting portal
```

## One-time setup

### GitHub Pages
**Settings → Pages → Build and deployment → Source: GitHub Actions.** After that every push publishes the site
(Actions tab shows progress, ~1 minute).

### Supabase — one project per company
1. supabase.com → **New project** (region close to your clients).
2. **Integrations → Cron** → enable (needed for the nightly reset).
3. **SQL Editor → New query** → paste the whole of `clients/<company>/supabase_install.sql` → **Run**.
   Last line: *Demo data loaded: … documents, … employees …*. Safe to run again.
4. **Authentication → Sign In / Providers**: keep Email on, turn **Allow new users to sign up** off.
5. **Project Settings → API**: copy the **Project URL** and the **anon / publishable key** into
   `clients/<company>/config.js` (`SUPABASE_URL`, `SUPABASE_ANON_KEY`), then push.

Until a company has its keys, its card on the landing page says **Coming soon**.

**Security fix** — also run once in each project (hides PIN hashes from logged-in users):
```sql
revoke select on public.hr_employees from authenticated;
grant select (id, emp_code, name, designation, phone, active, pin_set, created_at) on public.hr_employees to authenticated;
```

**Security hardening (October 2026):** The shared `sql/supabase_modules.sql` now defaults a missing or unknown module switch to **off** rather than on. Existing Supabase projects must re-run `sql/supabase_modules.sql` in the SQL Editor to apply the updated function. Generated `clients/<company>/supabase_install.sql` snapshots also need regenerating with `python3 tools/make_demo_seed.py --all` before a fresh database install. This change is not deployed to Supabase simply by merging GitHub code.

**Safwa demo upgrade verified (2026-10-08):** `sql/supabase_modules.sql` was applied transactionally to Safwa Trading (`cogifqmdvwididdkjsfy`). All four module rows are enabled. The access security smoke test and rollback-safe module-switch regression test both passed. Live end-user workflows and full role-based RLS behavior remain untested. No production database was modified.

## Security audit and trigger RPC hardening

After installing the demo schema, run `sql/tests/access_security_checks.sql` in the **demo** Supabase SQL Editor. The checks are read-only and raise an exception if baseline privileges are unsafe. They do not replace real API tests with separate viewer, supervisor, and admin logins.

`sql/security_revoke_trigger_rpc.sql` revokes direct `EXECUTE` access from trigger-only `SECURITY DEFINER` functions. Database triggers stay installed and enabled. This was applied to the Safwa Trading and Bunyan Contracting **demo** Supabase projects on 2026-10-08 and validated by checking function grants and enabled trigger registrations; end-to-end document/inventory workflows have not yet been retested.

`sql/security_pin_function_search_path.sql` sets explicit function search paths on supported helper/trigger functions. Applied on both demo projects on 2026-10-08; subsequent Security Advisor scans show **zero `function_search_path_mutable` notices**. This changes function configuration, not table data.

Fresh installers generated via `python3 tools/make_demo_seed.py --all` now include both hardening scripts. Existing `clients/*/supabase_install.sql` snapshots are not automatically regenerated by committing the build-script change. Re-run the generator before installing a fresh project.

**Module schema status (2026-10-08):** Both demo databases now have `public.portal_modules`; Safwa Trading was upgraded and baseline checks passed. Production still requires a separate, reviewed upgrade plan.


`sql/tests/hr_role_read_checks.sql` and `sql/tests/kiosk_write_security_checks.sql` cover read-only role simulations and kiosk/write-policy configuration. Full browser/API write-path and kiosk abuse tests remain necessary.

## Switching a part of the portal on or off (per company)

The switch is in the database, so a part that is off is closed everywhere: menu, pages, data, PDF files,
kiosk and notifications. Only the project owner can change it (the company's portal admin cannot).
Nothing is deleted: switching a part back on brings everything back.

Once per project: run `sql/supabase_modules.sql` in that company's Supabase SQL Editor
(new projects get it inside `supabase_install.sql`). Then, in the SQL Editor:

```sql
update public.portal_modules set enabled = false where module = 'docs';   -- off
update public.portal_modules set enabled = true  where module = 'docs';   -- on again
select * from public.portal_modules order by module;                      -- see all switches
```

Modules: `docs` (Documents + Certificates), `inventory`, `hr` (Employees), `kiosk` (also needs `hr`).

## Everyday changes

| I want to… | Edit | Then |
|---|---|---|
| change a company's name, colours, modules, document types | `clients/<company>/config.js` | push |
| change the demo data | `clients/<company>/seed_data.py` | `python3 tools/make_demo_seed.py <company>`, run the new `supabase_install.sql` in Supabase, push |
| fix a bug / add a feature for everyone | `app/…` | push |
| change the landing page, my contact details | `landing/…`, `landing/assets/product.js` | push |
| add a new demo company | copy `clients/trading/` to `clients/<new>/`, edit the 3 files | make the SQL, new Supabase project, push |

Test the site on your computer before pushing: `python3 tools/build.py`, then `cd dist && python3 -m http.server`
and open http://localhost:8000.

## Using it for a real client
1. New folder `clients/<client>/` with their `config.js` (set `DEMO.enabled: false`) and logo.
2. New Supabase project **in the client's own account**; run the four files in `sql/` in order (not the demo data).
3. First admin login: Authentication → Users → **Add user** (`admin@<LOGIN_DOMAIN>`), then in SQL Editor:
   ```sql
   insert into public.portal_users (id, username, full_name, is_admin, docs_role, inv_role, hr_role)
   select id, 'admin', 'Administrator', true, 'manager', 'admin', 'admin' from auth.users where email = 'admin@client.local';
   ```
4. Deploy the Edge Function `supabase/functions/admin-users` with the secret `LOGIN_DOMAIN`, so the admin can add users.
5. Publish: either a folder in this site, or a separate site/domain built from the same code.

## How the demos stay clean

| | |
|---|---|
| Nightly reset | `demo_reset()` runs every night at **03:00 Riyadh**: wipes the data and reloads the samples, with dates moved so the demo always looks current. |
| Reset button | The demo bar has **Reset sample data now** (once every 10 minutes, demo login only). |
| Login repair | Every hour `demo_fix_login()` puts the demo password back. |
| Read-only users | Users & Access cannot save in the demo. |
| Kiosk | PIN **1234** for every sample employee. |

Free plan: Supabase may pause a free project after a period with no use; open the demos now and then.
PDF links sent on WhatsApp stay in Storage: empty the `docs` and `certs` buckets once in a while.


