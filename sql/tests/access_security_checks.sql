-- Phase 2: read-only security smoke checks for a demo Supabase project.
-- Run in SQL Editor AFTER installing the generated company SQL.
-- This checks database grants, NOT live user-session RLS behavior.
-- No data is inserted, updated or deleted.
do $audit$
begin
  -- Employee PIN hashes and lockout state must never be queryable by web clients.
  if has_column_privilege('authenticated', 'public.hr_employees', 'pin_hash', 'SELECT')
     or has_column_privilege('authenticated', 'public.hr_employees', 'pin_hash', 'UPDATE')
     or has_column_privilege('authenticated', 'public.hr_employees', 'failed_attempts', 'SELECT')
     or has_column_privilege('authenticated', 'public.hr_employees', 'locked_until', 'SELECT') then
    raise exception 'FAIL: employee PIN/lockout fields exposed to authenticated clients';
  end if;
  if has_table_privilege('anon', 'public.hr_employees', 'SELECT') then
    raise exception 'FAIL: anonymous users can select employees';
  end if;
  -- Privileged RPCs must not be callable anonymously.
  if has_function_privilege('anon', 'public.set_employee_pin(uuid,text)', 'EXECUTE') then
    raise exception 'FAIL: anonymous users can invoke set_employee_pin';
  end if;
  if has_function_privilege('anon', 'public.portal_backup_now(text)', 'EXECUTE') then
    raise exception 'FAIL: anonymous users can invoke portal_backup_now';
  end if;
  if has_function_privilege('authenticated', 'public.portal_push(uuid[],text,text,text,text)', 'EXECUTE') then
    raise exception 'FAIL: clients can invoke internal push function';
  end if;
  -- Explicitly flag environments where module-switch migration has not been installed.
  if to_regclass('public.portal_modules') is null then
    raise notice 'NOT INSTALLED: portal_modules — module-switch tests skipped; apply only after reviewing demo migration';
  else
  -- Module switches must be readable but not editable by signed-in users.
  if has_table_privilege('authenticated', 'public.portal_modules', 'UPDATE')
     or has_table_privilege('authenticated', 'public.portal_modules', 'INSERT')
     or has_table_privilege('authenticated', 'public.portal_modules', 'DELETE') then
    raise exception 'FAIL: portal users can modify module switches';
  end if;
  end if;
  -- RLS must remain enabled on the tables most sensitive to privilege errors.
  if exists (
    select 1 from pg_class c join pg_namespace n on n.oid = c.relnamespace
     where n.nspname = 'public'
       and c.relname in ('portal_users','hr_employees','hr_pay','hr_attendance','portal_modules','portal_backups')
       and c.relkind = 'r' and not c.relrowsecurity
  ) then
    raise exception 'FAIL: RLS disabled on a sensitive table';
  end if;
  raise notice 'PASS: baseline privilege and RLS configuration checks';
end
$audit$;

-- Follow-up manual tests (not covered by this script):
-- 1) Sign in as viewer / supervisor / HR admin in a disposable project.
-- 2) Verify role-specific select, insert, update, delete via the real API.
-- 3) Verify an unprivileged user cannot fetch payroll or backups.
-- 4) Verify kiosk PIN lockout and module-disabled RPC behavior.
