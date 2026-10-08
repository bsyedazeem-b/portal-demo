-- Regression checks for module_on(). Run ONLY in a disposable/demo Supabase SQL Editor.
-- The transaction rolls back every change, including deliberate removal of a module row.
begin;

do $$
begin
  if public.module_on('not_a_module') is distinct from false then
    raise exception 'Unknown module must be disabled';
  end if;
end $$;

update public.portal_modules set enabled = true where module = 'docs';
do $$
begin
  if public.module_on('docs') is distinct from true then
    raise exception 'Enabled docs module must be accessible';
  end if;
end $$;

update public.portal_modules set enabled = false where module = 'docs';
do $$
begin
  if public.module_on('docs') is distinct from false then
    raise exception 'Disabled docs module must be inaccessible';
  end if;
end $$;

delete from public.portal_modules where module = 'kiosk';
do $$
begin
  if public.module_on('kiosk') is distinct from false then
    raise exception 'Missing kiosk module must be inaccessible';
  end if;
end $$;

rollback;
-- Expected: no exceptions; original module settings restored.
