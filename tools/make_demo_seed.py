#!/usr/bin/env python3
"""Builds the sample data for one demo company and writes its SQL.

    python3 tools/make_demo_seed.py trading        -> clients/trading/supabase_install.sql
    python3 tools/make_demo_seed.py --all          -> every folder in clients/ that has a seed_data.py

The *data* (customers, products, employees, documents ...) lives in clients/<name>/seed_data.py.
This file is only the engine that turns that data into the JSON the database loads, so every
demo company is built the same way.

All names, numbers and companies are invented. Dates are written as @D<offset>
(days from "today" in Riyadh) and are filled in by demo_reset() every night,
so the demo always looks current.
"""
import importlib.util, json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = ['supabase_setup.sql', 'supabase_docs.sql', 'supabase_hr.sql', 'supabase_extras.sql', 'supabase_modules.sql']


def words(n):
    a = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen',
         'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    t = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    def chunk(x):
        out = []
        if x >= 100: out.append(a[x // 100] + ' Hundred'); x %= 100
        if x >= 20: out.append(t[x // 10] + ('-' + a[x % 10] if x % 10 else ''))
        elif x: out.append(a[x])
        return ' '.join(out)
    if not n: return 'Zero'
    out = []
    for u, name in [(10**9, 'Billion'), (10**6, 'Million'), (1000, 'Thousand')]:
        if n >= u: out.append(chunk(n // u) + ' ' + name); n %= u
    if n: out.append(chunk(n))
    return ' '.join(out)


def sar_words(total):
    h = round(total * 100); r, hal = h // 100, h % 100
    return f"Saudi Riyals {words(r)}{' and ' + words(hal) + ' Halalas' if hal else ''} Only"


def totals(items):
    sub = vat = 0
    for it in items:
        line = float(it['qty']) * float(it['rate']); tp = float(it.get('tax_pct') or 15)
        sub += line; vat += line * tp / 100
    sub, vat = round(sub, 2), round(vat, 2)
    return {'sub_total': sub, 'vat_total': vat, 'grand_total': round(sub + vat, 2), 'total_in_words': sar_words(round(sub + vat, 2))}


def load_data(path):
    spec = importlib.util.spec_from_file_location('seed_data', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def build(S, config_js):
    """S = the client's seed_data module. Returns the seed dict."""
    R = random.Random(getattr(S, 'RANDOM_SEED', 2026))
    D = lambda n: f'@D{n}'                     # a date n days from today (negative = past)
    Y = '@Y'
    g = lambda name, default=None: getattr(S, name, default)

    def vat_no():
        return '3' + ''.join(str(R.randint(0, 9)) for _ in range(13)) + '3'

    # -------------------------------------------------------------- customers
    customers = []
    for code, name, ar, city, addr, person in S.CUSTOMERS:
        customers.append({'code': code, 'name': name, 'name_ar': ar, 'contact_person': person, 'city': city,
                          'phone': f'01{R.randint(10000000, 79999999)}', 'mobile': f'05{R.randint(10000000, 99999999)}',
                          'email': f"accounts@{name.split()[0].lower().replace('.', '')}{R.randint(1, 9)}.example",
                          'vat_no': vat_no(), 'address': f'{addr}, Saudi Arabia', 'payment_terms': R.choice(g('CUSTOMER_TERMS', ['Cash', '30 days', '45 days', '50% advance'])),
                          'buyer_id': f'CR {R.randint(1010000000, 4039999999)}'})
    CN = [c['name'] for c in customers]
    ADDR = {c['name']: c['address'] for c in customers}
    TRN = {c['name']: c['vat_no'] for c in customers}

    # -------------------------------------------------------------- employees
    employees = []
    for i, (job, pay) in enumerate(S.JOBS):
        employees.append({'emp_code': f'E-{i + 1:03d}', 'name': f'{S.FIRST[i]} {R.choice(S.LAST)}',
                          'designation': job, 'phone': f'05{R.randint(30000000, 99999999)}', 'basic_pay': pay,
                          'ot_rate': round(pay / 30 / 8 * 1.5, 2)})
    if g('INACTIVE_EMP'): employees.append(dict(S.INACTIVE_EMP, active=False))

    start, end = g('SHIFT_START', 8 * 60), g('SHIFT_END', 17 * 60)
    attendance = []
    for d in range(-42, 1):
        for e in employees:
            if e.get('active') is False: continue
            rnd = R.random(); att = {'emp': e['emp_code'], 'date': D(d)}
            if rnd < 0.03: att.update(status='absent')
            elif rnd < 0.06: att.update(status='leave', note=R.choice(['Annual leave', 'Sick leave', 'Emergency leave']))
            else:
                cin = start + R.randint(-12, 14)
                cout = None if d == 0 else end + R.choice([0, 0, 0, 0, 30, 60, 90, 120]) + R.randint(-8, 8)
                att.update(status='present', cin=cin, cout=cout, source=R.choice(['kiosk'] * 4 + ['admin']))
                if R.random() < 0.02: att.update(status='half_day', cout=start + 4 * 60 + R.randint(0, 40))
            attendance.append(att)

    tasks = []
    paid_idx = g('TASK_PAID', (3, 9, 12))
    for i, (title, pr, st, due) in enumerate(S.TASKS):
        e = employees[S.TASK_ASSIGNEES[i]]
        paid = i in paid_idx
        tasks.append({'emp': e['emp_code'], 'title': title, 'priority': pr, 'status': st, 'assigned_on': D(due - 7), 'due_date': D(due),
                      'paid': paid, 'amount': R.choice([100, 150, 200]) if paid else 0, 'remarks': 'Checked by supervisor' if st == 'done' else None})

    kit = []
    only_for = g('KIT_ONLY_FOR', {})
    sized = g('KIT_SIZED', ())
    for e in employees[:len(S.JOBS)]:
        issued = R.choice([-110, -95, -70, -40, -20])
        for item, q in S.KIT:
            if item in only_for and e['designation'] not in only_for[item]: continue
            if R.random() < 0.85:
                if item.startswith('Uniform') or item in sized: size = R.choice(['M', 'L', 'XL'])
                elif 'shoes' in item.lower(): size = '42'
                else: size = None
                kit.append({'emp': e['emp_code'], 'item': item, 'qty': q, 'issued_on': D(issued), 'size': size})
    kit_template = [{'item': i, 'qty': q} for i, q in S.KIT]

    adjustments = [{'emp': e, 'date': D(d), 'kind': k, 'amount': a, 'reason': r} for e, d, k, a, r in S.ADJUSTMENTS]
    advances = [{'emp': e, 'date': D(d), 'amount': a, 'installment': n, 'note': t} for e, d, a, n, t in S.ADVANCES]

    # -------------------------------------------------------------- inventory
    P = []
    for p in S.PRODUCTS:
        sku, name, cat, unit, qty, mn, loc, sup = p[:8]
        P.append(dict(sku=sku, name=name, category=cat, unit=unit, qty=qty, min_stock=mn, location=loc, supplier=sup, **(p[8] if len(p) > 8 else {})))

    movements = []
    in_notes, out_notes = g('MOVE_IN_NOTES', ['Supplier delivery', 'Received at store']), g('MOVE_OUT_NOTES', ['Customer order', 'Issued to office', 'Delivered to site', 'Internal use'])
    out_ref = g('MOVE_OUT_REF', 'DN')
    for p in P:
        final = p['qty']; big = max(final, 6)
        seq = [('IN', max(1, round(big * R.uniform(.3, .7)))) if R.random() < .45 else ('OUT', max(1, round(big * R.uniform(.1, .35))))
               for _ in range(R.randint(3, 7))]
        run, low = 0, 0
        for t, q in seq: run += q if t == 'IN' else -q; low = min(low, run)
        opening = max(final - run, -low)
        extra = opening + run - final
        if extra > 0: seq.append(('OUT', extra))
        days = sorted(R.sample(range(-58, -1), len(seq)))
        movements.append({'sku': p['sku'], 'type': 'IN', 'qty': opening, 'day': -60, 'reference': 'Opening stock', 'note': 'Stock take'})
        for (t, q), d in zip(seq, days):
            movements.append({'sku': p['sku'], 'type': t, 'qty': q, 'day': d,
                              'reference': f'PO-{R.randint(1, 5):05d}' if t == 'IN' else f'{out_ref}-@Y-{R.randint(1, 6):03d}',
                              'note': R.choice(in_notes) if t == 'IN' else R.choice(out_notes)})

    catalog = [{'category': c, 'subcategory': s, 'name': n, 'unit': u, 'rate': r} for c, s, n, u, r in S.CATALOG]
    RATE = {c[2]: c[4] for c in S.CATALOG}

    # -------------------------------------------------------------- documents
    docs = []
    def doc(t, no, day, party, data, status='approved', by='yousuf', files=None):
        docs.append({'doc_type': t, 'doc_no': no, 'day': day, 'party_name': party, 'data': data, 'status': status, 'by': by, 'files': files or {}})
    VEH = lambda: f"{R.choice('ABDHJKLMNRSTUVX')}{R.choice('ABDHJKLMNRSTUVX')}{R.choice('ABDHJKLMNRSTUVX')} {R.randint(1000, 9999)}"
    def items_from(names, qtys):
        return [{'description': n, 'qty': str(q), 'rate': f'{RATE[n]:.2f}', 'tax_pct': '15'} for n, q in zip(names, qtys)]

    n_draft_quotes = g('QUOTES_DRAFT_FROM', 6)
    for i, (day, cust, names, qtys) in enumerate(S.QUOTES):
        its = items_from(names, qtys)
        doc('quotation', f'QT-{i + 1:05d}', day, CN[cust], {'customer_address': ADDR[CN[cust]], 'customer_trn': TRN[CN[cust]], 'items': its,
            'completion_time': R.choice(g('QUOTE_COMPLETION', ['Within 1 week', '2-3 weeks', '5 working days'])),
            'payment_terms': R.choice(g('QUOTE_PAYMENT', ['50% advance, 50% on delivery', '30 days', 'Cash'])),
            'validity': '30 days', 'notes': g('QUOTE_NOTE', 'Prices in SAR.'), **totals(its)}, status='draft' if i >= n_draft_quotes else 'approved')

    invoices = []
    for i, (day, cust, q, state) in enumerate(S.INV):
        if q is None: its = items_from(*S.INV_EXTRA_ITEMS)
        else: its = [dict(x) for x in docs[[d['doc_no'] for d in docs].index(f'QT-{q + 1:05d}')]['data']['items']]
        t = totals(its); no = f'INV-{i + 1:05d}'
        due = day + (15 if state == 'overdue' else 30)
        doc('invoice', no, day, CN[cust], {'customer_address': ADDR[CN[cust]], 'customer_trn': TRN[CN[cust]], 'items': its,
            'quote_ref': f'QT-{q + 1:05d}' if q is not None else '', 'customer_po': f'PO-{R.randint(2000, 9999)}', 'payment_terms': '30 days',
            'due_date': D(due), 'notes': '', **t}, status='draft' if state == 'unpaid' else 'approved')
        pays = []
        if state == 'paid': pays = [(day + 10, t['grand_total'], 'Bank transfer')]
        if state == 'part': pays = [(day + 6, round(t['grand_total'] * .5, 2), 'Cheque')]
        invoices.append({'doc_no': no, 'payments': [{'day': d, 'amount': a, 'method': m, 'reference': f'TRX-{R.randint(100000, 999999)}'} for d, a, m in pays]})

    for i, (inv, cust) in enumerate(S.RECEIPTS):
        docs.append({'doc_type': 'receipt', 'doc_no': f'CR-{Y}-{i + 1:03d}', 'link_invoice': inv, 'party_name': CN[cust], 'status': 'approved', 'by': 'yousuf', 'files': {},
                     'data': {'method': 'Bank transfer' if i != 1 else 'Cheque', 'reference': '', 'bank': 'Demo Bank' if i != 1 else 'Sample Bank',
                              'purpose': 'Payment', 'purpose_ar': 'دفعة', 'payment_id': None}})
    if g('WALKIN'):
        party, amount, purpose, purpose_ar = S.WALKIN
        docs.append({'doc_type': 'receipt', 'doc_no': f'CR-{Y}-{len(S.RECEIPTS) + 1:03d}', 'day': -3, 'party_name': party, 'status': 'approved', 'by': 'yousuf', 'files': {},
                     'data': {'amount': amount, 'method': 'Cash', 'reference': '', 'bank': '', 'purpose': purpose, 'purpose_ar': purpose_ar,
                              'due_total': None, 'paid_before': None, 'invoice_id': None, 'invoice_no': None, 'payment_id': None}})

    pc = S.PETTY
    opening = 500.0
    for i, day in enumerate([-50, -36, -21, -6]):
        its = []
        for j in range(R.randint(4, 6)):
            n, c, to, a = R.choice(S.PC_ITEMS)
            its.append({'date': D(day + j), 'description': n, 'category': c, 'paid_to': to, 'bill_no': f'B{R.randint(1000, 9999)}', 'amount': str(a)})
        spent = round(sum(float(x['amount']) for x in its), 2); received = 2000 if i != 3 else 1500
        doc('petty', f'PC-{Y}-{i + 1:03d}', day, pc['custodian'], {'opening': opening, 'opening_auto': True, 'received': received, 'received_from': pc['received_from'],
            'items': its, 'spent': spent, 'note': '', 'prepared_by': pc['custodian'], 'approver': pc['approver'], 'checker': 'Accounts'},
            status='draft' if i == 3 else 'approved')
        opening = round(opening + received - spent, 2)

    for i, (day, cust, its) in enumerate(S.DNS):
        doc('dn', f'DN-{Y}-{i + 1:03d}', day, CN[cust], {'invoice_no': f'INV-{i + 1:05d}', 'po_no': f'PO-{R.randint(2000, 9999)}',
            'customer_address': ADDR[CN[cust]], 'customer_id': customers[cust]['code'],
            'items': [{'description': a, 'qty': str(q), 'delivered': str(q), 'received': str(q) if day < 0 else ''} for a, q in its],
            'driver_name': R.choice(S.DRIVERS), 'driver_iqama': f'2{R.randint(100000000, 999999999)}',
            'truck_no': VEH(), 'remarks': ''}, status='draft' if day == 0 else 'approved')

    who_name = lambda w: employees[w]['name'] if isinstance(w, int) else w      # an index means "that employee"
    for i, (day, cust, eq, who, st, desc) in enumerate(g('JOBCARDS', [])):
        who = who_name(who)
        doc('jobcard', f'JC-{Y}-{i + 1:03d}', day, CN[cust], {'equipment': eq, 'assigned_to': who, 'job_status': st, 'target_date': D(day + 10), 'description': desc,
            'items': [{'description': a, 'qty': str(q), 'unit': u} for a, q, u in S.JOBCARD_ITEMS] if i % 2 == 0 else [],
            'remarks': ''}, status='approved' if st == 'Completed' else 'draft', by='faraz')

    MRS = g('MRS', [])
    for i, (day, who, dept, job, its) in enumerate(MRS):
        who = who_name(who)
        doc('mr', f'MR-{Y}-{i + 1:03d}', day, who, {'job_ref': job, 'required_by': D(day + 3), 'department': dept,
            'items': [{'description': a, 'qty': str(b), 'unit': c, 'purpose': d} for a, b, c, d in its], 'remarks': ''},
            status='draft' if i == len(MRS) - 1 else 'approved', by='ali.store')

    for i, (day, sup, its) in enumerate(S.POS):
        lines = [{'description': a, 'qty': str(b), 'rate': f'{c:.2f}', 'tax_pct': '15'} for a, b, c in its]
        doc('po', f'PO-{i + 1:05d}', day, S.SUPPLIERS[sup][0], {'ref_number': f'MR-{Y}-{i + 1:03d}' if i < len(MRS) else '', 'vendor_address': g('VENDOR_ADDRESS', 'Jeddah, Saudi Arabia'),
            'vendor_trn': vat_no(), 'items': lines, 'delivery_date': D(day + 7), 'delivery_terms': g('PO_DELIVERY_TERMS', 'Delivered to our store'),
            'payment_terms': '30 days', 'notes': '', **totals(lines)}, status='draft' if i == len(S.POS) - 1 else 'approved')

    seed = {'users': S.USERS, 'customers': customers, 'employees': employees, 'attendance': attendance, 'tasks': tasks, 'kit': kit,
            'adjustments': adjustments, 'advances': advances, 'suppliers': [dict(zip(['name', 'contact_person', 'phone', 'email'], s)) for s in S.SUPPLIERS],
            'products': P, 'movements': movements, 'catalog': catalog, 'docs': docs, 'invoices': invoices, 'kit_template': kit_template}

    get = lambda k: re.search(k + r"\s*:\s*'([^']*)'", config_js).group(1)
    seed['settings'] = {'domain': get('LOGIN_DOMAIN'), 'demo_user': get('username'), 'demo_password': get('password'),
                        'company': re.search(r"name:\s*'([^']*)'", config_js.split('window.BRAND')[1]).group(1)}
    return seed


def make(client):
    cdir = os.path.join(ROOT, 'clients', client)
    S = load_data(os.path.join(cdir, 'seed_data.py'))
    cfg = open(os.path.join(cdir, 'config.js'), encoding='utf-8').read()
    seed = build(S, cfg)
    for need in ('yousuf', 'ali.store', 'faraz', 'manager', seed['settings']['demo_user']):
        assert any(u['username'] == need for u in seed['users']), f'{client}: USERS must include "{need}"'

    tpl = open(os.path.join(HERE, 'demo_template.sql'), encoding='utf-8').read()
    js = json.dumps(seed, ensure_ascii=False, separators=(',', ':'))
    assert '$seed$' not in js
    demo = tpl.replace('__SEED_JSON__', js)

    # one file to paste in the SQL Editor: schema + this company's demo data
    parts = [f'-- =====================================================================\n'
             f'-- PORTAL — COMPLETE INSTALL for demo company "{seed["settings"]["company"]}" (one file)\n'
             f'-- Paste this whole file in Supabase > SQL Editor > New query > Run.\n'
             f'-- Generated by tools/make_demo_seed.py — do not edit by hand. Safe to run again.\n'
             f'-- =====================================================================\n']
    for f in SCHEMA:
        parts.append(f'\n-- >>>>>>>>>>>>>>>>>>>>>>>> {f}\n' + open(os.path.join(ROOT, 'sql', f), encoding='utf-8').read())
    parts.append('\n-- >>>>>>>>>>>>>>>>>>>>>>>> demo data\n' + demo)
    open(os.path.join(cdir, 'supabase_install.sql'), 'w', encoding='utf-8').write(''.join(parts))
    print(f'{client}: supabase_install.sql written ({len("".join(parts)) // 1024} KB);',
          {k: len(v) for k, v in seed.items() if isinstance(v, list)})


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args == ['--all']:
        args = sorted(c for c in os.listdir(os.path.join(ROOT, 'clients')) if os.path.exists(os.path.join(ROOT, 'clients', c, 'seed_data.py')))
    for c in args:
        make(c)
