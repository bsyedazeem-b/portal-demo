-- Read-only role/RLS regression checks for the demo Supabase databases.
-- This script uses transaction-local session impersonation; every test rolls back.
-- Requires one active test user for each HR role: viewer, supervisor, admin, null.
-- It does NOT prove writes, JWT signature validation, or end-to-end login.
BEGIN;
SELECT set_config('request.jwt.claim.sub',(
  SELECT id::text FROM public.portal_users WHERE active AND hr_role = 'viewer' LIMIT 1
),true);
SET LOCAL ROLE authenticated;
DO $test$ BEGIN
  IF public.my_role('hr') IS DISTINCT FROM 'viewer' THEN
    RAISE EXCEPTION 'Viewer identity not configured';
  END IF;
  IF (SELECT count(*) FROM public.hr_pay) <> 0 THEN
    RAISE EXCEPTION 'Viewer can read payroll';
  END IF;
END $test$;
ROLLBACK;

BEGIN;
SELECT set_config('request.jwt.claim.sub',(
  SELECT id::text FROM public.portal_users WHERE active AND hr_role = 'supervisor' LIMIT 1
),true);
SET LOCAL ROLE authenticated;
DO $test$ BEGIN
  IF public.my_role('hr') IS DISTINCT FROM 'supervisor' THEN
    RAISE EXCEPTION 'Supervisor identity not configured';
  END IF;
  IF (SELECT count(*) FROM public.hr_pay) <> 0 THEN
    RAISE EXCEPTION 'Supervisor can read payroll';
  END IF;
END $test$;
ROLLBACK;

BEGIN;
SELECT set_config('request.jwt.claim.sub',(
  SELECT id::text FROM public.portal_users WHERE active AND hr_role = 'admin' LIMIT 1
),true);
SET LOCAL ROLE authenticated;
DO $test$ BEGIN
  IF public.my_role('hr') IS DISTINCT FROM 'admin' THEN
    RAISE EXCEPTION 'HR admin identity not configured';
  END IF;
  IF (SELECT count(*) FROM public.hr_pay) = 0 THEN
    RAISE EXCEPTION 'HR admin cannot see seeded payroll or demo payroll missing';
  END IF;
END $test$;
ROLLBACK;

BEGIN;
SELECT set_config('request.jwt.claim.sub',(
  SELECT id::text FROM public.portal_users WHERE active AND hr_role IS NULL LIMIT 1
),true);
SET LOCAL ROLE authenticated;
DO $test$ BEGIN
  IF public.my_role('hr') IS NOT NULL THEN
    RAISE EXCEPTION 'User without HR role received HR role';
  END IF;
  IF (SELECT count(*) FROM public.hr_employees) <> 0
    OR (SELECT count(*) FROM public.hr_attendance) <> 0
    OR (SELECT count(*) FROM public.hr_pay) <> 0 THEN
    RAISE EXCEPTION 'User without HR role can read HR data';
  END IF;
END $test$;
ROLLBACK;
-- Success = SQL executes with no exception. Any exception indicates a failed check.
