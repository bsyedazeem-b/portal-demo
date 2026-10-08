-- Pin the search path for known helper/trigger functions.
-- All table references in these functions are schema-qualified; pg_catalog
-- builtins remain available implicitly. Missing optional functions are skipped.
-- No table data is changed. Safe to rerun on demo databases.
do $fix$
declare fn text;
begin
  foreach fn in array array[
    'public.inv_protect_qty()',
    'public.hr_task_calc()',
    'public.demo_fill(text,date)',
    'public.hr_attendance_calc()',
    'public.portal_modules_touch()'
  ] loop
    if to_regprocedure(fn) is not null then
      execute format('alter function %s set search_path = public, pg_temp', fn);
    end if;
  end loop;
end $fix$;
