# =====================================================================
# Sample data for the demo company "Bunyan Contracting & Maintenance Est."
# An MEP (electrical, plumbing, AC) and fit-out contractor in Jeddah that
# works on client sites and runs annual maintenance contracts.
# Everything here is invented.
#
# Dates are days from today (negative = past). After editing, run:
#     python3 tools/make_demo_seed.py contracting
# =====================================================================
Y = '@Y'
RANDOM_SEED = 3031

# ---------------------------------------------------------------- customers
CUSTOMERS = [
    ('C-001', 'Al Waha Residential Compound', 'مجمع الواحة السكني', 'Jeddah', 'Obhur North, Jeddah', 'Hassan Al-Ghamdi'),
    ('C-002', 'Horizon Real Estate Development', 'الأفق للتطوير العقاري', 'Jeddah', 'Prince Sultan Road, Jeddah', 'Omar Siddiqui'),
    ('C-003', 'Green Valley International School', 'مدرسة الوادي الأخضر العالمية', 'Jeddah', 'Al Faisaliyah, Jeddah', 'Sarah Al-Qahtani'),
    ('C-004', 'Summit Business Tower', 'برج القمة للأعمال', 'Jeddah', 'King Abdulaziz Road, Jeddah', 'Abdullah Al-Otaibi'),
    ('C-005', 'Blue Wave Medical Center', 'مركز الموجة الزرقاء الطبي', 'Jeddah', 'Al Safa District, Jeddah', 'Dr. Imran Qureshi'),
    ('C-006', 'Taiba Shopping Mall', 'طيبة مول', 'Madinah', 'King Abdullah Road, Madinah', 'Saeed Al-Harbi'),
    ('C-007', 'Coastline Hotel Apartments', 'شقق الساحل الفندقية', 'Jeddah', 'Corniche Road, Jeddah', 'Rashid Khan'),
    ('C-008', 'Al Bayan Training Institute', 'معهد البيان للتدريب', 'Makkah', 'Al Awali, Makkah', 'Majed Al-Zahrani'),
    ('C-009', 'Nova Logistics Warehouses', 'مستودعات نوفا اللوجستية', 'Jeddah', 'Industrial City Phase 3, Jeddah', 'Tariq Mehmood'),
    ('C-010', 'Asir Family Restaurants', 'مطاعم عسير العائلية', 'Jeddah', 'Al Tahlia Street, Jeddah', 'Nasser Al-Shehri'),
    ('C-011', 'Oasis Villas Project', 'مشروع فلل الواحة', 'Jeddah', 'Al Shati District, Jeddah', 'Lina Haddad'),
    ('C-012', 'Crescent Pharmacy Chain', 'سلسلة صيدليات الهلال', 'Jeddah', 'Al Zahra District, Jeddah', 'Khalid Al-Malki'),
]
CUSTOMER_TERMS = ['30% advance, balance on progress', '30 days', '45 days', 'Monthly (AMC)']

USERS = [
    {'username': 'demo', 'full_name': 'Demo Visitor', 'is_admin': True, 'docs_role': 'manager', 'inv_role': 'admin', 'hr_role': 'admin'},
    {'username': 'yousuf', 'full_name': 'Yousuf Rahman (Accounts)', 'is_admin': False, 'docs_role': 'staff', 'inv_role': 'viewer', 'hr_role': None},
    {'username': 'ali.store', 'full_name': 'Ali Haider (Site Store)', 'is_admin': False, 'docs_role': None, 'inv_role': 'storekeeper', 'hr_role': None},
    {'username': 'faraz', 'full_name': 'Eng. Faraz Ahmed (Projects)', 'is_admin': False, 'docs_role': 'staff', 'inv_role': 'viewer', 'hr_role': 'supervisor'},
    {'username': 'manager', 'full_name': 'Sami Al-Rashid (GM)', 'is_admin': True, 'docs_role': 'manager', 'inv_role': 'viewer', 'hr_role': 'viewer'},
]

# ---------------------------------------------------------------- employees
FIRST = ['Arshad', 'Bilal', 'Dilawar', 'Ejaz', 'Fayyaz', 'Gul', 'Habib', 'Imtiaz', 'Jamil', 'Khurram', 'Liaqat', 'Mukhtar', 'Nadeem',
         'Qasim', 'Rashid', 'Shakeel', 'Waqar', 'Yasir']
LAST = ['Khan', 'Ali', 'Hussain', 'Ahmed', 'Iqbal', 'Malik', 'Shah', 'Butt', 'Kumar', 'Das']
JOBS = [('Project Manager', 11000), ('Site Engineer (Electrical)', 7500), ('Site Engineer (Mechanical)', 7500), ('Foreman', 5200),
        ('Foreman', 5000), ('Electrician', 3200), ('Electrician', 3100), ('Electrician', 3000), ('Plumber', 3000), ('Plumber', 2900),
        ('AC Technician', 3400), ('AC Technician', 3300), ('Painter', 2600), ('Gypsum Fixer', 2700), ('Helper', 1800),
        ('Helper', 1800), ('Driver', 2800), ('Safety Officer', 5500)]
INACTIVE_EMP = {'emp_code': 'E-019', 'name': 'Anwar Baig', 'designation': 'Helper', 'phone': '0550000019', 'basic_pay': 1700, 'ot_rate': 10.63}
SHIFT_START, SHIFT_END = 7 * 60, 16 * 60          # sites start at 07:00

TASKS = [('Site visit – Summit Tower 12th floor snag list', 'high', 'in_progress', 2), ('Prepare progress claim no. 3 – Oasis Villas', 'normal', 'pending', 4),
         ('Emergency: water leak at Blue Wave Medical Center', 'urgent', 'pending', 1), ('DB panel testing – Nova warehouse', 'high', 'done', -1),
         ('Toolbox talk – working at height', 'normal', 'in_progress', 6), ('AC preventive maintenance – Coastline Hotel', 'high', 'pending', 3),
         ('Submit material approval – lighting fixtures', 'normal', 'done', -3), ('Weekly HSE inspection – all sites', 'low', 'pending', 10),
         ('Fix lights in Green Valley School corridors', 'urgent', 'in_progress', 0), ('Install water heaters – Villa 7', 'normal', 'done', -2),
         ('Gypsum ceiling – Crescent Pharmacy branch', 'normal', 'pending', 5), ('Painting touch-up after handover', 'low', 'cancelled', -4),
         ('As-built drawings – Al Waha Compound', 'high', 'done', -6), ('Collect site tools from Taiba Mall', 'normal', 'pending', 8)]
TASK_ASSIGNEES = [1, 0, 8, 5, 17, 10, 2, 17, 6, 9, 13, 12, 1, 16]
TASK_PAID = (3, 9, 12)

KIT = [('Coverall', 2), ('Safety helmet', 1), ('Safety shoes', 1), ('Reflective vest', 1), ('Work gloves (pairs)', 4), ('ID card & lanyard', 1)]
KIT_SIZED = ('Coverall',)
KIT_ONLY_FOR = {'Coverall': ('Foreman', 'Electrician', 'Plumber', 'AC Technician', 'Painter', 'Gypsum Fixer', 'Helper', 'Driver'),
                'Work gloves (pairs)': ('Foreman', 'Electrician', 'Plumber', 'AC Technician', 'Painter', 'Gypsum Fixer', 'Helper')}

ADJUSTMENTS = [('E-015', -12, 'violation', 100, 'Not wearing helmet on site (2nd warning)'),
               ('E-017', -20, 'deduction', 150, 'Traffic fine – company pickup'),
               ('E-006', -8, 'bonus', 400, 'Finished DB wiring ahead of schedule'),
               ('E-011', -25, 'bonus', 250, 'Weekend emergency AC call-out'),
               ('E-013', -5, 'deduction', 120, 'Lost drill machine')]
ADVANCES = [('E-009', -35, 2000, 500, 'Family emergency'), ('E-016', -15, 1000, 250, 'Iqama renewal')]

# ---------------------------------------------------------------- site store
SUPPLIERS = [('Gulf Cables & Electrical Trading', 'Khalid', '0126000201', 'sales@gulfcables.example'),
             ('Red Sea Plumbing Supplies', 'Imran', '0126000202', 'orders@rsplumbing.example'),
             ('Arabian Paints Distributor', 'Faisal', '0126000203', None),
             ('CoolAir HVAC Parts', 'Naseer', '0126000204', 'info@coolair.example'),
             ('SafeWork PPE Supplies', 'Joseph', '0126000205', 'sales@safework.example'),
             ('Al Bina Building Materials', 'Waleed', '0126000206', None)]

PRODUCTS = [
    ('EL-CBL-2.5', 'Cable 2.5 mm² (100 m roll)', 'Electrical', 'roll', 34, 15, 'Store A1', 0),
    ('EL-CBL-4', 'Cable 4 mm² (100 m roll)', 'Electrical', 'roll', 12, 10, 'Store A1', 0),
    ('EL-CND-20', 'PVC Conduit 20 mm (3 m)', 'Electrical', 'pcs', 260, 100, 'Yard 1', 0),
    ('EL-MCB-20', 'MCB 20 A single pole', 'Electrical', 'pcs', 45, 30, 'Store A2', 0),
    ('EL-SKT-13', 'Switch socket 13 A (twin)', 'Electrical', 'pcs', 120, 60, 'Store A2', 0),
    ('EL-LED-60', 'LED Panel 60x60 (40 W)', 'Electrical', 'pcs', 18, 30, 'Store A3', 0),
    ('EL-DB-12', 'Distribution Board 12-way', 'Electrical', 'pcs', 4, 3, 'Store A3', 0),
    ('PL-PPR-25', 'PPR Pipe 25 mm (4 m)', 'Plumbing', 'pcs', 140, 60, 'Yard 2', 1),
    ('PL-PPR-ELB', 'PPR Elbow 25 mm', 'Plumbing', 'pcs', 30, 80, 'Store B1', 1),
    ('PL-PVC-4', 'PVC Drain Pipe 4 in (6 m)', 'Plumbing', 'pcs', 26, 15, 'Yard 2', 1),
    ('PL-VLV-BALL', 'Ball Valve 3/4 in', 'Plumbing', 'pcs', 22, 20, 'Store B1', 1),
    ('PL-WH-50', 'Water Heater 50 L', 'Plumbing', 'pcs', 6, 4, 'Store B2', 1),
    ('AC-CU-12', 'Copper Pipe 1/2 in (15 m)', 'HVAC', 'roll', 9, 6, 'Store C1', 3),
    ('AC-INS-12', 'Pipe Insulation 1/2 in (2 m)', 'HVAC', 'pcs', 75, 40, 'Store C1', 3),
    ('AC-GAS-410', 'Refrigerant R410A (11.3 kg)', 'HVAC', 'cylinder', 3, 4, 'Store C2', 3),
    ('AC-BKT-SPL', 'Split AC Wall Bracket', 'HVAC', 'set', 14, 10, 'Store C2', 3),
    ('FN-GYP-12', 'Gypsum Board 12.5 mm', 'Finishing', 'sheet', 85, 50, 'Yard 3', 5),
    ('FN-PNT-18', 'Emulsion Paint 18 L (white)', 'Finishing', 'bucket', 24, 15, 'Store D1', 2),
    ('FN-PRM-18', 'Primer 18 L', 'Finishing', 'bucket', 11, 10, 'Store D1', 2),
    ('FN-ADH-20', 'Tile Adhesive 20 kg', 'Finishing', 'bag', 40, 25, 'Yard 3', 5),
    ('FN-CEM-50', 'Cement 50 kg', 'Finishing', 'bag', 60, 40, 'Yard 3', 5),
    ('FX-ANC-8', 'Anchor Bolts 8 mm (box of 100)', 'Fixings', 'box', 16, 10, 'Store E1', 5),
    ('FX-SIL-CLR', 'Silicone Sealant (clear)', 'Fixings', 'pcs', 48, 24, 'Store E1', 5),
    ('PP-HLM-WH', 'Safety Helmet (white)', 'PPE', 'pcs', 15, 10, 'PPE Cabinet', 4),
    ('PP-VST-RF', 'Reflective Vest', 'PPE', 'pcs', 22, 15, 'PPE Cabinet', 4),
    ('PP-GLV-WK', 'Work Gloves (pair)', 'PPE', 'pair', 8, 40, 'PPE Cabinet', 4),
    ('PP-SHO-42', 'Safety Shoes (size 42)', 'PPE', 'pair', 6, 5, 'PPE Cabinet', 4),
    ('PP-HRN-FB', 'Full Body Harness', 'PPE', 'pcs', 5, 4, 'PPE Cabinet', 4),
]
MOVE_IN_NOTES = ['Supplier delivery', 'Received at site store', 'Returned from site']
MOVE_OUT_NOTES = ['Issued to Summit Tower site', 'Issued to Oasis Villas site', 'Issued to Nova warehouse job', 'Issued for maintenance call']
MOVE_OUT_REF = 'MR'

# ---------------------------------------------------------------- rate list
CATALOG = [('Services', 'Electrical', 'Electrical point – wiring & accessories (per point)', 'point', 185),
           ('Services', 'Electrical', 'LED panel 60x60 – supply & install', 'pcs', 175),
           ('Services', 'Electrical', 'Distribution board 12-way – supply, install & test', 'pcs', 1450),
           ('Services', 'Plumbing', 'Plumbing point – PPR, supply & install (per point)', 'point', 240),
           ('Services', 'Plumbing', 'Water heater 50 L – supply & install', 'pcs', 780),
           ('Services', 'HVAC', 'Split AC installation (up to 2 ton)', 'unit', 450),
           ('Services', 'HVAC', 'Split AC preventive maintenance', 'unit', 95),
           ('Services', 'HVAC', 'Duct cleaning (per m)', 'm', 28),
           ('Services', 'Fit-out', 'Gypsum board ceiling – supply & install', 'm²', 68),
           ('Services', 'Fit-out', 'Painting – 1 primer + 2 coats emulsion', 'm²', 22),
           ('Services', 'Fit-out', 'Floor tiling – labour with adhesive', 'm²', 45),
           ('Services', 'Maintenance', 'Annual MEP maintenance contract – villa', 'year', 4800),
           ('Services', 'Maintenance', 'Annual MEP maintenance contract – commercial building', 'year', 38000),
           ('Services', 'Maintenance', 'Emergency call-out (within 4 hours)', 'visit', 450),
           ('Services', 'Manpower', 'Electrician (per hour)', 'hour', 55),
           ('Services', 'Manpower', 'Helper (per hour)', 'hour', 30),
           ('Products', 'Materials', 'Split AC 2 ton (inverter) – supply only', 'unit', 3150),
           ('Products', 'Materials', 'Water heater 50 L – supply only', 'pcs', 520)]

QUOTES = [
    (-62, 3, ['Electrical point – wiring & accessories (per point)', 'LED panel 60x60 – supply & install', 'Distribution board 12-way – supply, install & test'], [140, 90, 4]),
    (-50, 6, ['Annual MEP maintenance contract – commercial building'], [1]),
    (-44, 10, ['Plumbing point – PPR, supply & install (per point)', 'Water heater 50 L – supply & install', 'Electrical point – wiring & accessories (per point)'], [48, 8, 96]),
    (-31, 8, ['Electrical point – wiring & accessories (per point)', 'Distribution board 12-way – supply, install & test', 'LED panel 60x60 – supply & install'], [60, 3, 120]),
    (-22, 2, ['Split AC installation (up to 2 ton)', 'Split AC 2 ton (inverter) – supply only', 'Split AC preventive maintenance'], [12, 12, 30]),
    (-14, 11, ['Gypsum board ceiling – supply & install', 'Painting – 1 primer + 2 coats emulsion', 'LED panel 60x60 – supply & install'], [180, 420, 24]),
    (-8, 0, ['Annual MEP maintenance contract – villa', 'Emergency call-out (within 4 hours)'], [12, 4]),
    (-2, 4, ['Plumbing point – PPR, supply & install (per point)', 'Electrician (per hour)', 'Helper (per hour)'], [10, 40, 40]),
]
QUOTE_COMPLETION = ['3 weeks from site handover', '6-8 weeks', '10 working days', 'As per contract schedule']
QUOTE_PAYMENT = ['30% advance, 60% progress, 10% on handover', 'Monthly progress claims', '50% advance, 50% on completion']
QUOTE_NOTE = 'Prices in SAR. Scaffolding and civil works by others. Valid subject to site visit.'

INV = [(-58, 3, 0, 'paid'), (-46, 6, 1, 'paid'), (-40, 10, 2, 'part'), (-28, 8, 3, 'paid'), (-20, 2, 4, 'overdue'), (-12, 11, 5, 'part'), (-5, 4, None, 'unpaid')]
INV_EXTRA_ITEMS = (['Emergency call-out (within 4 hours)', 'Plumbing point – PPR, supply & install (per point)', 'Electrician (per hour)'], [2, 3, 6])
RECEIPTS = [('INV-00001', 3), ('INV-00003', 10), ('INV-00004', 8)]
WALKIN = ('Villa owner – Mr. Ahmed Saleh', 450, 'Emergency call-out', 'زيارة طارئة')

PC_ITEMS = [('Diesel for site generator', 'Fuel', 'Station 21', 240), ('Drinking water for site', 'Food & water', 'Nova Water', 120),
            ('Drill bits and blades', 'Tools & hardware', 'City Hardware', 165), ('Courier – documents to client', 'Courier', 'SMSA', 45),
            ('Iqama renewal fee', 'Government fees', 'Absher', 650), ('Site barricade tape', 'Safety', 'SafeWork PPE', 90),
            ('Pickup tyre puncture', 'Repairs & maintenance', 'Tyre shop', 60), ('Mobile recharge (foremen)', 'Mobile & internet', 'STC', 100),
            ('Municipality permit copy', 'Government fees', 'Balady', 200), ('Generator service', 'Repairs & maintenance', 'Power Tech', 380),
            ('Lunch for weekend crew', 'Food & water', 'Al Baik', 310), ('Parking at Summit Tower', 'Transport', 'Tower parking', 55)]
PETTY = {'custodian': 'Eng. Faraz Ahmed', 'received_from': 'Sami Al-Rashid (GM)', 'approver': 'Sami Al-Rashid'}

DRIVERS = ['Shahid Mehmood', 'Raju Kumar', 'Abdul Rehman', 'Mohammed Saleem']
DNS = [(-45, 3, [('LED Panel 60x60 (40 W)', 90), ('Distribution Board 12-way', 4)]),
       (-38, 6, [('AC filters (set)', 40), ('Refrigerant R410A (11.3 kg)', 1)]),
       (-26, 10, [('Water Heater 50 L', 8), ('PPR Pipe 25 mm (4 m)', 60)]),
       (-15, 8, [('LED Panel 60x60 (40 W)', 120), ('Cable 2.5 mm² (100 m roll)', 10)]),
       (-4, 2, [('Split AC 2 ton (inverter)', 12), ('Split AC Wall Bracket', 12)]),
       (0, 11, [('Gypsum Board 12.5 mm', 60), ('Emulsion Paint 18 L (white)', 14)])]

# job cards (work orders): (day, customer, job, assigned to (employee index or a name), status, description)
JOBCARDS = [(-40, 3, 'Summit Tower – 12th floor electrical', 3, 'Completed', 'Wiring, sockets and LED panels for the 12th floor offices.'),
            (-30, 6, 'Coastline Hotel – AC maintenance (AMC)', 10, 'Completed', 'Quarterly service of 64 split units, filter cleaning, gas top-up.'),
            (-18, 10, 'Oasis Villas – plumbing first fix', 8, 'In Progress', 'PPR water lines and drainage for villas 5 to 8.'),
            (-9, 2, 'Green Valley School – classroom lighting', 4, 'In Progress', 'Replace old fittings with LED panels in 18 classrooms.'),
            (-3, 0, 'Al Waha Compound – villa 22 snag list', 5, 'Open', 'Socket not working, bathroom leak, ceiling crack.'),
            (-1, 4, 'Blue Wave Medical – water leak', 9, 'On Hold', 'Leak above the pharmacy ceiling; waiting for access permit.')]
JOBCARD_ITEMS = [('PPR Elbow 25 mm', 12, 'pcs'), ('Silicone Sealant (clear)', 4, 'pcs'), ('Switch socket 13 A (twin)', 6, 'pcs')]

# material requests from site: (day, requested by (employee index or a name), department / site, job ref, [(item, qty, unit, purpose)])
MRS = [(-33, 3, 'Summit Tower site', f'JC-{Y}-001', [('LED Panel 60x60 (40 W)', 40, 'pcs', '12th floor'), ('Cable 2.5 mm² (100 m roll)', 6, 'roll', 'Socket circuits')]),
       (-20, 8, 'Oasis Villas site', f'JC-{Y}-003', [('PPR Pipe 25 mm (4 m)', 60, 'pcs', 'Water lines'), ('PPR Elbow 25 mm', 120, 'pcs', 'Fittings'), ('Ball Valve 3/4 in', 16, 'pcs', 'Isolation')]),
       (-10, 4, 'Green Valley School', f'JC-{Y}-004', [('LED Panel 60x60 (40 W)', 72, 'pcs', 'Classrooms'), ('Anchor Bolts 8 mm (box of 100)', 4, 'box', 'Fixing')]),
       (-2, 'Ali Haider', 'Site store', 'Stock', [('Work Gloves (pair)', 60, 'pair', 'Low stock'), ('Refrigerant R410A (11.3 kg)', 3, 'cylinder', 'Low stock')])]

POS = [(-52, 0, [('Cable 2.5 mm² (100 m roll)', 40, 245), ('LED Panel 60x60 (40 W)', 150, 62)]),
       (-34, 1, [('PPR Pipe 25 mm (4 m)', 200, 14.5), ('PPR Elbow 25 mm', 300, 1.8), ('Water Heater 50 L', 10, 410)]),
       (-21, 0, [('LED Panel 60x60 (40 W)', 100, 62), ('Anchor Bolts 8 mm (box of 100)', 10, 38)]),
       (-9, 4, [('Work Gloves (pair)', 120, 6.5), ('Safety Helmet (white)', 20, 22)]),
       (-1, 3, [('Refrigerant R410A (11.3 kg)', 4, 520), ('Copper Pipe 1/2 in (15 m)', 6, 340)])]
VENDOR_ADDRESS = 'Jeddah, Saudi Arabia'
PO_DELIVERY_TERMS = 'Delivered to site as per our MR'
