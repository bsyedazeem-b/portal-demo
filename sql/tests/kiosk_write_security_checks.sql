-- Read-only checks for the public attendance kiosk and HR write permissions.
-- Run against demo Supabase projects after applying the module switch schema.
-- Verifies configuration only; not a penetration test or a real attendance punch.
DO $audit$
DECLARE
  kiosk_fn text;
  emp_fn text;
BEGIN
  SELECT pg_get_functiondef(to_regprocedure('public.kiosk_punch(uuid,text,text)')) INTO kiosk_fn;
  SELECT pg_get_functiondef(to_regprocedure('public.kiosk_employees()')) INTO emp_fn;
  IF kiosk_fn IS NULL OR emp_fn IS NULL THEN
    RAISE EXCEPTION 'FAIL: kiosk functions not installed';
  END IF;
  IF position('locked_until' in kiosk_fn) = 0 OR position('failed_attempts' in kiosk_fn) = 0 THEN
    RAISE EXCEPTION 'FAIL: kiosk PIN lockout logic not detected';
  END IF;
  IF position('module_on(' in kiosk_fn) = 0 OR position('module_on(' in emp_fn) = 0 THEN
    RAISE EXCEPTION 'FAIL: kiosk module access guard missing';
  END IF;
  IF NOT has_function_privilege('anon','public.kiosk_punch(uuid,text,text)','EXECUTE') THEN
    RAISE EXCEPTION 'FAIL: expected public kiosk check-in function is inaccessible';
  END IF;
  IF has_table_privilege('anon','public.hr_attendance','INSERT')
     OR has_table_privilege('anon','public.hr_attendance','UPDATE') THEN
    RAISE EXCEPTION 'FAIL: anonymous direct attendance writes are possible';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
     WHERE schemaname='public' AND tablename='hr_attendance'
       AND policyname='hr_attendance_write'
       AND qual LIKE '%my_role%'
       AND with_check LIKE '%my_role%'
  ) THEN
    RAISE EXCEPTION 'FAIL: attendance write policy missing role checks';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
     WHERE schemaname='public' AND tablename='hr_pay'
       AND policyname='hr_pay_admin' AND qual LIKE '%my_role%'
  ) THEN
    RAISE EXCEPTION 'FAIL: payroll admin-only policy missing';
  END IF;
  RAISE NOTICE 'PASS: kiosk guards and write policy configuration';
END $audit$;

-- Remaining concerns to test separately:
-- Public kiosk_employees() intentionally exposes employee names and identifiers.
-- Per-employee PIN lockout limits guessing, but also permits targeted lockout abuse.
-- Add edge rate limiting, request monitoring, and (ideally) device trust at the API edge.
-- Verify staff cannot edit attendance and payroll through real signed-in API sessions.
