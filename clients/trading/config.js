/* =====================================================================
   SAFWA TRADING (demo) — settings for this demo company.
   This is the only file that is different between companies: the portal code
   is shared (app/), and tools/build.py adds the colour helpers at the end.
   ===================================================================== */

// 1) Supabase: Project Settings > API > Project URL and the anon / publishable key.
//    These two values are safe in a public site; the database rules protect the data.
window.PORTAL_CONFIG = {
  SUPABASE_URL: 'https://cogifqmdvwididdkjsfy.supabase.co',
  SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNvZ2lmcW1kdndpZGlkZGtqc2Z5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTExMTk1OTIsImV4cCI6MjEwNjY5NTU5Mn0.TSrkf75C4SChjoZhhwmiP7ud1boyzYJGPIPwCs-0rKE',
  LOGIN_DOMAIN: 'safwa.local',        // user "ahmed" signs in as ahmed@safwa.local

  // 2) Demo mode: shows the "Try demo" button and blocks risky actions
  //    (changing passwords, creating users, real WhatsApp / push sends).
  DEMO: {
    enabled: true,
    username: 'demo',                   // the shared demo account (created by supabase_install.sql)
    password: 'demo1234',
    resetNote: 'Demo data resets every night at 3:00 AM (Riyadh time).'
  }
};

// 3) Company and brand
window.BRAND = {
  name:      'Safwa Trading & Distribution Co.',     // full legal name, used on PDFs and emails
  nameAr:    'شركة الصفوة للتجارة والتوزيع',
  short:     'Safwa Trading',                        // top bar, phone app name
  tagline:   'Food & FMCG wholesale · Distribution',
  taglineAr: 'تجارة الجملة للمواد الغذائية · التوزيع',
  portalName: 'Safwa Portal',
  industry:  'Trading & distribution',               // shown on the demo landing page

  city: 'Jeddah', cityAr: 'جدة', country: 'Kingdom of Saudi Arabia', countryAr: 'المملكة العربية السعودية',
  address:   'Warehouse 14, Al Khumrah Industrial Area, Jeddah 22414, Saudi Arabia',
  addressAr: 'مستودع 14، المنطقة الصناعية بالخمرة، جدة',
  lat: 21.4858, lon: 39.1925,                        // weather and prayer times on the sign-in page

  phones:  ['0500000101', '0500000102'],             // first one is used in email / WhatsApp signatures
  email:   'sales@safwatrading.example',
  website: 'www.safwatrading.example',

  crNo:  '7000000101',                               // commercial registration (fake for the demo)
  vatNo: '300000000000003',                          // ZATCA sample VAT number
  bank: [['Bank Name', 'Demo Bank'], ['Account No', '000000000000101'], ['IBAN', 'SA00 0000 0000 0000 0000 0101']],

  // colours: main brand colour + accent. Everything else is worked out from these two.
  colors: {brand: '#1F6F5C', accent: '#E3A72F'},
  logo: 'assets/logo.svg',
  letterhead: {header: null, footer: null, stamp: null},

  // modules: set any to false to hide it everywhere (home, top bar, search)
  modules: {documents: true, inventory: true, employees: true, kiosk: true},

  // document types: a trading company does not need job cards or material requests
  docTypes: {
    quotation: true, invoice: true, receipt: true, petty: true, dn: true, catalog: true /* price list */, customers: true,
    jobcard: false, mr: false, po: true
  },

  // inventory: product categories (with the short code that starts new SKUs) and units
  inventory: {
    categories: {'Rice & Grains': 'RG', 'Oils & Ghee': 'OL', 'Sugar & Flour': 'SF', 'Beverages': 'BV', 'Dairy (UHT)': 'DY',
                 'Canned Food': 'CN', 'Cleaning': 'CL', 'Disposables': 'PK'},
    units: ['carton', 'bag', 'tin', 'pack', 'pcs', 'kg', 'ltr']
  }
};
