-- =====================================================================
-- MODULE SWITCHES: which parts of the portal this company has.
-- Run AFTER supabase_setup / docs / hr / extras. Safe to re-run.
--
-- The switch lives in the database, so a part that is off is closed
-- everywhere: the screens, the data (RLS), the files (storage), the kiosk
-- and the notifications. Only the project owner can change it (SQL Editor);
-- the company's own portal admin cannot.
--
--   switch a part off:  update public.portal_modules set enabled = false where module = 'docs';
--   switch it back on:  update public.portal_modules set enabled = true  where module = 'docs';
--   see all switches:   select * from public.portal_modules order by module;
--
-- modules: 'docs' (Documents + Certificates), 'inventory', 'hr' (Employees),
--          'kiosk' (check-in tablet; also needs 'hr' on)
-- Data is never deleted: switching a part back on brings everything back.
-- =====================================================================

create table if not exists public.portal_modules (
  module     text primary key check (module in ('docs','inventory','hr','kiosk')),
  enabled    boolean not null default true,
  updated_at timestamptz not null default now()
);
insert into public.portal_modules (module) values ('docs'), ('inventory'), ('hr'), ('kiosk') on conflict do nothing;

alter table public.portal_modules enable row level security;
drop policy if exists portal_modules_read on public.portal_modules;
-- signed-in users may read the switches (the portal hides closed parts); nobody may change them from the portal
create policy portal_modules_read on public.portal_modules for select to authenticated using (true);
revoke all on public.portal_modules from anon;
revoke insert, update, delete, truncate on public.portal_modules from authenticated;

create or replace function public.portal_modules_touch()
returns trigger language plpgsql as $$ begin new.updated_at := now(); return new; end $$;
drop trigger if exists portal_modules_touch on public.portal_modules;
create trigger portal_modules_touch before update on public.portal_modules for each row execute function public.portal_modules_touch();

-- Fail closed: missing/unknown module records must not accidentally grant access.
-- The install script seeds all four known modules before creating this function.
create or replace function public.module_on(p_module text)
returns boolean language sql stable security definer set search_path = public as $body$
  select coalesce((
    select enabled from public.portal_modules
     where module = p_module
       and module in ('docs', 'inventory', 'hr', 'kiosk')
  ), false);
$body$;
revoke all on function public.module_on(text) from public;
grant execute on function public.module_on(text) to anon, authenticated;

-- role of the signed-in user for one part of the portal: none when that part is switched off.
-- Every table and storage rule asks my_role(), so this one change closes the data as well.
create or replace function public.my_role(p_module text)
returns text language sql stable security definer set search_path = public as $$
  select case when not public.module_on(p_module) then null
              else case p_module
                     when 'docs'      then docs_role
                     when 'inventory' then inv_role
                     when 'hr'        then hr_role
                   end
         end
    from public.portal_users
   where id = auth.uid() and active;
$$;

-- notifications only go to people in parts that are switched on
create or replace function public.portal_users_with(p_module text, p_roles text[] default null)
returns uuid[] language sql stable security definer set search_path = public as $$
  select coalesce(array_agg(id), '{}') from public.portal_users
   where active and public.module_on(p_module) and case p_module when 'docs' then docs_role when 'inventory' then inv_role when 'hr' then hr_role when 'admin' then case when is_admin then 'admin' end end
         = any(coalesce(p_roles, array['manager','staff','viewer','admin','storekeeper','supervisor']));
$$;

-- the morning summary skips parts that are switched off
create or replace function public.portal_daily_digest()
returns int language plpgsql security definer set search_path = public as $$
declare u record; lines text[]; n int := 0; d date := (now() at time zone 'Asia/Riyadh')::date; v int; s public.hr_settings;
begin
  select * into s from public.hr_settings where id = 1;
  for u in select * from public.portal_users where active and exists (select 1 from public.push_subscriptions ps where ps.user_id = portal_users.id) loop
    lines := '{}';
    if public.module_on('docs') and u.docs_role in ('manager','staff') then
      select count(*) into v from public.docs_documents x where x.doc_type = 'invoice' and (x.data->>'due_date') < d::text and (x.data->>'due_date') > '1900'
        and coalesce((x.data->>'grand_total')::numeric, 0) - coalesce((select sum(amount) from public.docs_payments p where p.document_id = x.id), 0) > 0.005;
      if v > 0 then lines := lines || (v || ' overdue invoice' || case when v > 1 then 's' else '' end); end if;
      if u.docs_role = 'manager' then
        select count(*) into v from public.docs_documents where status = 'draft';
        if v > 0 then lines := lines || (v || ' waiting for approval'); end if;
      end if;
    end if;
    if public.module_on('inventory') and u.inv_role in ('admin','storekeeper') then
      select count(*) into v from public.inv_products where min_stock > 0 and qty <= min_stock;
      if v > 0 then lines := lines || (v || ' product' || case when v > 1 then 's' else '' end || ' low on stock'); end if;
    end if;
    if public.module_on('hr') and u.hr_role in ('admin','supervisor') then
      select count(*) into v from public.hr_tasks where status in ('pending','in_progress') and due_date < d;
      if v > 0 then lines := lines || (v || ' overdue task' || case when v > 1 then 's' else '' end); end if;
      if to_regclass('public.hr_kit') is not null and exists (select 1 from public.hr_kit where batch is not null) then
        select count(*) into v from public.hr_employees e where e.active and coalesce(
          (select max(issued_on) from public.hr_kit k where k.employee_id = e.id and k.batch is not null) + make_interval(months => coalesce(s.kit_cycle_months, 4)), '1900-01-01'::date) <= d;
        if v > 0 then lines := lines || (v || ' employee' || case when v > 1 then 's' else '' end || ' due for working kit'); end if;
      end if;
    end if;
    if cardinality(lines) > 0 then
      perform public.portal_push(array[u.id], 'Good morning, ' || split_part(coalesce(u.full_name, u.username), ' ', 1), array_to_string(lines, ' · '), 'index.html', 'digest');
      n := n + 1;
    end if;
  end loop;
  return n;
end $$;

-- kiosk: no employee list and no check-in while the kiosk (or Employees) is off
create or replace function public.kiosk_employees()
returns table (id uuid, emp_code text, name text, state text)
language sql stable security definer set search_path = public as $$
  select e.id, e.emp_code, e.name,
         case when a.check_out is not null then 'done'
              when a.check_in  is not null then 'in'
              else 'out' end
    from public.hr_employees e
    left join public.hr_attendance a
      on a.employee_id = e.id and a.work_date = (now() at time zone 'Asia/Riyadh')::date
   where e.active and e.pin_hash is not null
     and public.module_on('kiosk') and public.module_on('hr')
   order by e.emp_code;
$$;

create or replace function public.kiosk_punch(p_employee uuid, p_pin text, p_photo text default null)
returns json language plpgsql security definer set search_path = public, extensions as $$
declare
  e       public.hr_employees%rowtype;
  a       public.hr_attendance%rowtype;
  v_today date := (now() at time zone 'Asia/Riyadh')::date;
  v_act   text;
  v_tasks json;
  v_att   uuid;
begin
  if not (public.module_on('kiosk') and public.module_on('hr')) then
    return json_build_object('ok', false, 'error', 'Kiosk is switched off');
  end if;
  select * into e from public.hr_employees where id = p_employee and active for update;
  if not found then
    return json_build_object('ok', false, 'error', 'Employee not found');
  end if;
  if e.locked_until is not null and e.locked_until > now() then
    return json_build_object('ok', false, 'error',
      'Too many wrong PINs. Try again after ' || to_char(e.locked_until at time zone 'Asia/Riyadh', 'HH24:MI'));
  end if;
  if e.pin_hash is null or p_pin is null or e.pin_hash is distinct from crypt(p_pin, e.pin_hash) then
    update public.hr_employees
       set failed_attempts = case when failed_attempts + 1 >= 5 then 0 else failed_attempts + 1 end,
           locked_until    = case when failed_attempts + 1 >= 5 then now() + interval '10 minutes' else null end
     where id = e.id;
    return json_build_object('ok', false, 'error', 'Wrong PIN');
  end if;
  update public.hr_employees set failed_attempts = 0, locked_until = null where id = e.id;

  select * into a from public.hr_attendance where employee_id = e.id and work_date = v_today for update;
  if not found then
    insert into public.hr_attendance (employee_id, work_date, status, check_in, source)
    values (e.id, v_today, 'present', now(), 'kiosk');
    v_act := 'in';
  elsif a.check_in is null then
    update public.hr_attendance set check_in = now(), status = 'present', source = 'kiosk' where id = a.id;
    v_act := 'in';
  elsif a.check_out is null then
    if now() - a.check_in < interval '2 minutes' then
      return json_build_object('ok', false, 'error',
        'Already checked in at ' || to_char(a.check_in at time zone 'Asia/Riyadh', 'HH24:MI'));
    end if;
    update public.hr_attendance set check_out = now(), source = 'kiosk' where id = a.id;
    v_act := 'out';
  else
    return json_build_object('ok', false, 'error', 'Already checked out today');
  end if;

  -- photo taken by the kiosk camera (small JPEG), kept for 60 days
  if p_photo is not null and length(p_photo) < 300000 and p_photo like 'data:image/jpeg;base64,%' then
    begin
      select id into v_att from public.hr_attendance where employee_id = e.id and work_date = v_today;
      insert into public.hr_punch_photos (attendance_id, employee_id, kind, photo) values (v_att, e.id, v_act, p_photo);
      delete from public.hr_punch_photos where taken_at < now() - interval '60 days';
    exception when undefined_table then null;
    end;
  end if;

  select coalesce(json_agg(json_build_object('title', t.title, 'details', t.details, 'due', t.due_date,
                                             'priority', t.priority) order by t.due_date nulls last), '[]'::json)
    into v_tasks
    from public.hr_tasks t
   where t.employee_id = e.id and t.status in ('pending','in_progress');

  return json_build_object('ok', true, 'action', v_act, 'name', e.name, 'time', now(), 'tasks', v_tasks);
end $$;
