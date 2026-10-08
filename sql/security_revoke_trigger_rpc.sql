-- Phase 2 security hardening: revoke direct RPC exposure of trigger-only functions.
-- PostgreSQL triggers already bound to these functions continue to execute.
-- Standalone RPC calls to a trigger function are invalid and should not be exposed.
-- Safe to re-run. Run on DEMO projects first.
do $hardening$
declare f record;
begin
  for f in
    select p.oid::regprocedure as signature
    from pg_proc p join pg_namespace n on n.oid=p.pronamespace
    where n.nspname='public'
      and p.prorettype='pg_catalog.trigger'::regtype
      and p.prosecdef
  loop
    execute format('revoke execute on function %s from public, anon, authenticated',f.signature);
  end loop;
end $hardening$;

-- Optional verification:
-- select p.proname, has_function_privilege('anon',p.oid,'execute') anon_execute,
--        has_function_privilege('authenticated',p.oid,'execute') authenticated_execute
-- from pg_proc p join pg_namespace n on n.oid=p.pronamespace
-- where n.nspname='public' and p.prorettype='pg_catalog.trigger'::regtype and p.prosecdef;
