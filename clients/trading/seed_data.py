# =====================================================================
# Sample data for the demo company "Safwa Trading & Distribution Co."
# A food & FMCG wholesaler in Jeddah that supplies restaurants, hotels,
# supermarkets and cafeterias. Everything here is invented.
#
# Dates are days from today (negative = past). After editing, run:
#     python3 tools/make_demo_seed.py trading
# =====================================================================
Y = '@Y'

# ---------------------------------------------------------------- customers
# (code, name, name in Arabic, city, address, contact person)
CUSTOMERS = [
    ('C-001', 'Al Rayyan Supermarket', 'سوبرماركت الريان', 'Jeddah', 'Al Naseem District, Jeddah', 'Hassan Al-Ghamdi'),
    ('C-002', 'Bayt Al Mandi Restaurants', 'مطاعم بيت المندي', 'Jeddah', 'Prince Sultan Road, Jeddah', 'Omar Siddiqui'),
    ('C-003', 'Golden Sands Hotel', 'فندق الرمال الذهبية', 'Jeddah', 'Corniche Road, Jeddah', 'Sarah Al-Qahtani'),
    ('C-004', 'Hayat Mini Markets', 'أسواق حياة الصغيرة', 'Makkah', 'Al Awali, Makkah', 'Abdullah Al-Otaibi'),
    ('C-005', 'Sunrise School Cafeteria Services', 'خدمات كافتيريا مدارس الشروق', 'Jeddah', 'Al Safa District, Jeddah', 'Imran Qureshi'),
    ('C-006', 'Taiba Family Hypermarket', 'هايبر ماركت طيبة العائلي', 'Madinah', 'Quba Road, Madinah', 'Saeed Al-Harbi'),
    ('C-007', 'Coastline Catering Co.', 'شركة الساحل للإعاشة', 'Rabigh', 'Industrial Area, Rabigh', 'Rashid Khan'),
    ('C-008', 'Al Bustan Bakery', 'مخبز البستان', 'Jeddah', 'Al Rawdah District, Jeddah', 'Majed Al-Zahrani'),
    ('C-009', 'Noor Hospital Kitchen', 'مطبخ مستشفى النور', 'Jeddah', 'Al Zahra District, Jeddah', 'Tariq Mehmood'),
    ('C-010', 'Asir Grill House', 'مشويات عسير', 'Taif', 'Shehar Road, Taif', 'Nasser Al-Shehri'),
    ('C-011', 'Oasis Coffee Corners', 'مقاهي الواحة', 'Jeddah', 'Al Malqa Street, Jeddah', 'Lina Haddad'),
    ('C-012', 'Crescent Grocery Stores', 'بقالات الهلال', 'Jeddah', 'Al Sharafiyah, Jeddah', 'Khalid Al-Malki'),
]
CUSTOMER_TERMS = ['Cash', '15 days', '30 days', '45 days']

# ---------------------------------------------------------------- users
# The usernames yousuf / ali.store / faraz / manager are fixed (the demo data refers to them);
# only "demo" can sign in. Change the full names freely.
USERS = [
    {'username': 'demo', 'full_name': 'Demo Visitor', 'is_admin': True, 'docs_role': 'manager', 'inv_role': 'admin', 'hr_role': 'admin'},
    {'username': 'yousuf', 'full_name': 'Yousuf Rahman (Accounts)', 'is_admin': False, 'docs_role': 'staff', 'inv_role': 'viewer', 'hr_role': None},
    {'username': 'ali.store', 'full_name': 'Ali Haider (Warehouse)', 'is_admin': False, 'docs_role': None, 'inv_role': 'storekeeper', 'hr_role': None},
    {'username': 'faraz', 'full_name': 'Faraz Ahmed (Sales Supervisor)', 'is_admin': False, 'docs_role': 'staff', 'inv_role': 'viewer', 'hr_role': 'supervisor'},
    {'username': 'manager', 'full_name': 'Sami Al-Rashid (GM)', 'is_admin': True, 'docs_role': 'manager', 'inv_role': 'viewer', 'hr_role': 'viewer'},
]

# ---------------------------------------------------------------- employees
FIRST = ['Adeel', 'Bashir', 'Danish', 'Ehsan', 'Farhan', 'Ghulam', 'Hamza', 'Irfan', 'Javed', 'Kamran', 'Latif', 'Mansoor', 'Naveed',
         'Rizwan', 'Salman', 'Tahir', 'Usman', 'Zubair']
LAST = ['Khan', 'Ali', 'Hussain', 'Ahmed', 'Iqbal', 'Malik', 'Shah', 'Raza']
JOBS = [('Sales Representative', 4500), ('Sales Representative', 4300), ('Sales Representative', 4200), ('Accountant', 5500),
        ('Merchandiser', 3200), ('Merchandiser', 3100), ('Delivery Driver', 3000), ('Delivery Driver', 2900), ('Delivery Driver', 2900),
        ('Delivery Driver', 2800), ('Warehouse Keeper', 3600), ('Warehouse Keeper', 3400), ('Forklift Operator', 3300),
        ('Loader', 2100), ('Loader', 2000), ('Purchasing Officer', 4800), ('Sales Supervisor', 6500), ('Operations Manager', 9500)]
INACTIVE_EMP = {'emp_code': 'E-019', 'name': 'Anwar Baig', 'designation': 'Loader', 'phone': '0550000019', 'basic_pay': 1900, 'ot_rate': 11.88}
SHIFT_START, SHIFT_END = 7 * 60, 16 * 60          # warehouse opens at 07:00

# (title, priority, status, due in days); TASK_ASSIGNEES = which employee (0 = first in JOBS)
TASKS = [('Visit Bayt Al Mandi – new menu items order', 'high', 'in_progress', 2), ('Weekly sales report by route', 'normal', 'pending', 4),
         ('Urgent delivery: Golden Sands Hotel banquet', 'urgent', 'pending', 1), ('Deliver order to Al Rayyan Supermarket', 'high', 'done', -1),
         ('Renew delivery van insurance', 'normal', 'in_progress', 6), ('Shelf arrangement at Taiba Hypermarket', 'high', 'pending', 3),
         ('Update price list for new supplier rates', 'normal', 'done', -3), ('Expiry check – beverages aisle (FEFO)', 'low', 'pending', 10),
         ('Collect cheque from Hayat Mini Markets', 'urgent', 'in_progress', 0), ('Route 3 deliveries – Makkah', 'normal', 'done', -2),
         ('Cycle count – rice & grains rack', 'normal', 'pending', 5), ('Forklift monthly service', 'low', 'cancelled', -4),
         ('Submit VAT return documents', 'high', 'done', -6), ('Follow up returned cartons with Crescent', 'normal', 'pending', 8)]
TASK_ASSIGNEES = [0, 1, 6, 7, 17, 4, 15, 10, 2, 8, 11, 12, 3, 5]
TASK_PAID = (3, 9, 12)

KIT = [('Uniform shirt', 2), ('Uniform trousers', 2), ('ID card & lanyard', 1), ('Safety shoes', 1), ('Mobile SIM', 1), ('Cap', 1)]
KIT_ONLY_FOR = {'Safety shoes': ('Delivery Driver', 'Warehouse Keeper', 'Forklift Operator', 'Loader'),
                'Mobile SIM': ('Sales Representative', 'Delivery Driver', 'Sales Supervisor', 'Merchandiser')}

# (employee code, day, kind, amount, reason)
ADJUSTMENTS = [('E-014', -12, 'violation', 50, 'Late 3 times this month'),
               ('E-008', -20, 'deduction', 150, 'Traffic fine – delivery van'),
               ('E-001', -8, 'bonus', 500, 'Best sales route of the month'),
               ('E-011', -25, 'bonus', 200, 'Night unloading of container'),
               ('E-015', -5, 'deduction', 80, 'Damaged cartons (negligence)')]
# (employee code, day, amount, monthly installment, note)
ADVANCES = [('E-007', -35, 1500, 500, 'Family emergency'), ('E-013', -15, 1000, 250, 'Iqama renewal')]

# ---------------------------------------------------------------- inventory
# (name, contact person, phone, e-mail)
SUPPLIERS = [('Gulf Rice Importers', 'Khalid', '0126000101', 'sales@gulfrice.example'),
             ('Red Sea Edible Oils Factory', 'Imran', '0126000102', 'orders@rsoils.example'),
             ('Arabian Beverages Co.', 'Faisal', '0126000103', None),
             ('Fresh Valley Dairy Wholesale', 'Naseer', '0126000104', 'info@freshvalley.example'),
             ('Al Madar Cleaning Products', 'Joseph', '0126000105', 'sales@almadar.example'),
             ('Star Packaging Industries', 'Waleed', '0126000106', None)]

# (sku, name, category, unit, qty now, minimum stock, location, supplier index, {extra})
PRODUCTS = [
    ('RG-BAS-10', 'Basmati Rice 10 kg', 'Rice & Grains', 'bag', 180, 80, 'Rack A1', 0),
    ('RG-BAS-40', 'Basmati Rice 40 kg', 'Rice & Grains', 'bag', 45, 30, 'Rack A1', 0),
    ('RG-SEL-05', 'Sella Rice 5 kg', 'Rice & Grains', 'bag', 22, 40, 'Rack A2', 0),
    ('RG-LEN-RED', 'Red Lentils 5 kg', 'Rice & Grains', 'bag', 60, 25, 'Rack A2', 0),
    ('OL-SUN-18', 'Sunflower Oil 18 L', 'Oils & Ghee', 'tin', 75, 30, 'Rack B1', 1),
    ('OL-COR-15', 'Corn Oil 1.5 L x 6', 'Oils & Ghee', 'carton', 18, 25, 'Rack B1', 1),
    ('OL-GHE-02', 'Vegetable Ghee 2 kg', 'Oils & Ghee', 'tin', 40, 20, 'Rack B2', 1),
    ('SF-SUG-50', 'White Sugar 50 kg', 'Sugar & Flour', 'bag', 30, 20, 'Rack C1', 0),
    ('SF-FLR-45', 'Flour No. 1 45 kg', 'Sugar & Flour', 'bag', 12, 20, 'Rack C1', 0),
    ('SF-SAL-01', 'Table Salt 1 kg x 20', 'Sugar & Flour', 'carton', 35, 10, 'Rack C2', 0),
    ('BV-WAT-330', 'Drinking Water 330 ml x 40', 'Beverages', 'carton', 420, 150, 'Floor D', 2),
    ('BV-WAT-15', 'Drinking Water 1.5 L x 12', 'Beverages', 'carton', 210, 100, 'Floor D', 2),
    ('BV-JUI-ORG', 'Orange Juice 200 ml x 24', 'Beverages', 'carton', 64, 40, 'Rack D2', 2),
    ('BV-SFT-CAN', 'Soft Drink Cans 330 ml x 24', 'Beverages', 'carton', 95, 50, 'Rack D2', 2),
    ('BV-TEA-100', 'Black Tea 100 bags x 12', 'Beverages', 'carton', 8, 15, 'Rack D3', 2),
    ('DY-MLK-1L', 'UHT Milk 1 L x 12', 'Dairy (UHT)', 'carton', 130, 60, 'Rack E1', 3),
    ('DY-CRM-200', 'Cooking Cream 200 ml x 24', 'Dairy (UHT)', 'carton', 26, 20, 'Rack E1', 3),
    ('DY-CHS-TIN', 'Processed Cheese Tin 500 g x 12', 'Dairy (UHT)', 'carton', 14, 15, 'Rack E2', 3),
    ('CN-TOM-400', 'Tomato Paste 400 g x 24', 'Canned Food', 'carton', 55, 25, 'Rack F1', 0),
    ('CN-TUN-185', 'Tuna Chunks 185 g x 48', 'Canned Food', 'carton', 33, 20, 'Rack F1', 0),
    ('CN-BEA-400', 'Fava Beans 400 g x 24', 'Canned Food', 'carton', 9, 20, 'Rack F2', 0),
    ('CL-DSH-5L', 'Dishwashing Liquid 5 L x 4', 'Cleaning', 'carton', 28, 10, 'Rack G1', 4),
    ('CL-BLC-4L', 'Bleach 4 L x 4', 'Cleaning', 'carton', 16, 10, 'Rack G1', 4),
    ('CL-TIS-ROL', 'Kitchen Roll x 6', 'Cleaning', 'pack', 70, 30, 'Rack G2', 4),
    ('PK-CUP-250', 'Paper Cups 250 ml x 1000', 'Disposables', 'carton', 40, 20, 'Rack H1', 5),
    ('PK-BOX-ALU', 'Aluminium Food Containers x 500', 'Disposables', 'carton', 6, 12, 'Rack H1', 5),
    ('PK-BAG-T', 'T-shirt Bags (large) x 1000', 'Disposables', 'carton', 52, 25, 'Rack H2', 5),
    ('PK-GLV-100', 'Food Gloves x 100 x 10', 'Disposables', 'carton', 24, 15, 'Rack H2', 5),
]
MOVE_IN_NOTES = ['Supplier delivery', 'Container unloaded', 'Received at warehouse']
MOVE_OUT_NOTES = ['Customer order', 'Van loading – route 1', 'Van loading – route 2', 'Delivered to customer']

# ---------------------------------------------------------------- price list
# (category, subcategory, name, unit, rate in SAR before VAT)
CATALOG = [('Products', 'Rice & grains', 'Basmati rice 10 kg', 'bag', 78),
           ('Products', 'Rice & grains', 'Basmati rice 40 kg', 'bag', 295),
           ('Products', 'Rice & grains', 'Red lentils 5 kg', 'bag', 42),
           ('Products', 'Oils & ghee', 'Sunflower oil 18 L', 'tin', 118),
           ('Products', 'Oils & ghee', 'Vegetable ghee 2 kg', 'tin', 39),
           ('Products', 'Sugar & flour', 'White sugar 50 kg', 'bag', 165),
           ('Products', 'Sugar & flour', 'Flour No. 1 45 kg', 'bag', 92),
           ('Products', 'Beverages', 'Drinking water 330 ml (carton of 40)', 'carton', 16.5),
           ('Products', 'Beverages', 'Drinking water 1.5 L (carton of 12)', 'carton', 14),
           ('Products', 'Beverages', 'Orange juice 200 ml (carton of 24)', 'carton', 31),
           ('Products', 'Beverages', 'Soft drink cans (carton of 24)', 'carton', 44),
           ('Products', 'Dairy', 'UHT milk 1 L (carton of 12)', 'carton', 58),
           ('Products', 'Dairy', 'Cooking cream 200 ml (carton of 24)', 'carton', 96),
           ('Products', 'Canned food', 'Tomato paste 400 g (carton of 24)', 'carton', 62),
           ('Products', 'Canned food', 'Tuna chunks 185 g (carton of 48)', 'carton', 285),
           ('Products', 'Disposables', 'Paper cups 250 ml (carton of 1000)', 'carton', 74),
           ('Products', 'Disposables', 'Aluminium food containers (carton of 500)', 'carton', 165),
           ('Services', 'Delivery', 'Delivery outside Jeddah (per trip)', 'trip', 350)]

# ---------------------------------------------------------------- documents
# quotations: (day, customer index, [price-list names], [quantities])
QUOTES = [
    (-62, 1, ['Basmati rice 40 kg', 'Sunflower oil 18 L', 'Tomato paste 400 g (carton of 24)'], [40, 30, 20]),
    (-50, 2, ['Drinking water 330 ml (carton of 40)', 'Orange juice 200 ml (carton of 24)', 'UHT milk 1 L (carton of 12)'], [300, 80, 60]),
    (-44, 0, ['Basmati rice 10 kg', 'White sugar 50 kg', 'Vegetable ghee 2 kg', 'Red lentils 5 kg'], [120, 25, 40, 30]),
    (-31, 6, ['Basmati rice 40 kg', 'Flour No. 1 45 kg', 'Sunflower oil 18 L', 'Delivery outside Jeddah (per trip)'], [60, 40, 45, 3]),
    (-22, 8, ['UHT milk 1 L (carton of 12)', 'Cooking cream 200 ml (carton of 24)', 'Tuna chunks 185 g (carton of 48)'], [90, 20, 10]),
    (-14, 10, ['Paper cups 250 ml (carton of 1000)', 'Soft drink cans (carton of 24)'], [30, 50]),
    (-8, 3, ['Drinking water 1.5 L (carton of 12)', 'Soft drink cans (carton of 24)', 'Delivery outside Jeddah (per trip)'], [200, 60, 1]),
    (-2, 9, ['Basmati rice 40 kg', 'Aluminium food containers (carton of 500)'], [25, 12]),
]
QUOTE_COMPLETION = ['Next day delivery', 'Within 48 hours', 'Weekly schedule']
QUOTE_PAYMENT = ['Cash on delivery', '30 days', '15 days']
QUOTE_NOTE = 'Prices in SAR, delivered to your store in Jeddah.'

# invoices: (day, customer, from quotation number (0 = QT-00001) or None, payment state)
INV = [(-58, 1, 0, 'paid'), (-46, 2, 1, 'paid'), (-40, 0, 2, 'part'), (-28, 6, 3, 'paid'), (-20, 8, 4, 'overdue'), (-12, 10, 5, 'part'), (-5, 11, None, 'unpaid')]
INV_EXTRA_ITEMS = (['Basmati rice 10 kg', 'Drinking water 330 ml (carton of 40)', 'Tomato paste 400 g (carton of 24)'], [20, 50, 10])
# cash receipts for invoice payments: (invoice number, customer index)
RECEIPTS = [('INV-00001', 1), ('INV-00003', 0), ('INV-00004', 6)]
WALKIN = ('Cash sale – Abu Fahad Grocery', 860, 'Cash sale at warehouse', 'بيع نقدي من المستودع')

PC_ITEMS = [('Fuel for delivery van', 'Fuel', 'Station 21', 180), ('Water & tea for warehouse', 'Food & water', 'Bin Dawood', 95),
            ('Pallet repair', 'Tools & hardware', 'City Hardware', 120), ('Courier documents to Riyadh', 'Courier', 'SMSA', 45),
            ('Iqama renewal fee', 'Government fees', 'Absher', 650), ('Stretch film rolls', 'Packing', 'Star Packaging', 240),
            ('Taxi for sales rep', 'Transport', 'Careem', 70), ('Mobile recharge (drivers)', 'Mobile & internet', 'STC', 100),
            ('Van tyre puncture', 'Repairs & maintenance', 'Tyre shop', 60), ('Reefer van AC repair', 'Repairs & maintenance', 'Cool Tech', 380),
            ('Lunch for unloading team', 'Food & water', 'Al Baik', 310), ('Parking fees – port', 'Transport', 'Port parking', 55)]
PETTY = {'custodian': 'Yousuf Rahman', 'received_from': 'Sami Al-Rashid (GM)', 'approver': 'Sami Al-Rashid'}

# delivery notes: (day, customer, [(item, qty)])
DRIVERS = ['Shahid Mehmood', 'Raju Kumar', 'Abdul Rehman', 'Mohammed Saleem']
DNS = [(-45, 1, [('Basmati Rice 40 kg', 40), ('Sunflower Oil 18 L', 30), ('Tomato Paste 400 g x 24', 20)]),
       (-38, 2, [('Drinking Water 330 ml x 40', 300), ('Orange Juice 200 ml x 24', 80), ('UHT Milk 1 L x 12', 60)]),
       (-26, 0, [('Basmati Rice 10 kg', 120), ('White Sugar 50 kg', 25), ('Vegetable Ghee 2 kg', 40)]),
       (-15, 6, [('Basmati Rice 40 kg', 60), ('Flour No. 1 45 kg', 40), ('Sunflower Oil 18 L', 45)]),
       (-4, 8, [('UHT Milk 1 L x 12', 90), ('Cooking Cream 200 ml x 24', 20)]),
       (0, 10, [('Paper Cups 250 ml x 1000', 30), ('Soft Drink Cans 330 ml x 24', 50)])]

# a trading company does not use job cards or material requests (switched off in config.js)
JOBCARDS = []
MRS = []

# purchase orders: (day, supplier index, [(item, qty, rate)])
POS = [(-52, 0, [('Basmati Rice 40 kg', 120, 238), ('Basmati Rice 10 kg', 300, 61)]),
       (-34, 1, [('Sunflower Oil 18 L', 150, 92), ('Vegetable Ghee 2 kg', 100, 29)]),
       (-21, 2, [('Drinking Water 330 ml x 40', 800, 11.5), ('Soft Drink Cans 330 ml x 24', 200, 33)]),
       (-9, 3, [('UHT Milk 1 L x 12', 250, 45), ('Cooking Cream 200 ml x 24', 60, 74)]),
       (-1, 5, [('Aluminium Food Containers x 500', 40, 118), ('Paper Cups 250 ml x 1000', 50, 52)])]
VENDOR_ADDRESS = 'Jeddah, Saudi Arabia'
PO_DELIVERY_TERMS = 'Delivered to our warehouse, Al Khumrah'
