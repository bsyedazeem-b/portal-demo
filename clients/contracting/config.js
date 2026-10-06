/* =====================================================================
   BUNYAN CONTRACTING (demo) — settings for this demo company.
   This is the only file that is different between companies: the portal code
   is shared (app/), and tools/build.py adds the colour helpers at the end.
   ===================================================================== */

// 1) Supabase: Project Settings > API > Project URL and the anon / publishable key.
//    These two values are safe in a public site; the database rules protect the data.
window.PORTAL_CONFIG = {
  SUPABASE_URL: 'https://apjkgpjdmxmxrpgtpflz.supabase.co',
  SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwamtncGpkbXhteHJwZ3RwZmx6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTEyODQ0NjEsImV4cCI6MjEwNjg2MDQ2MX0.EEvWe10xIB3Dy5wQetOOVDVcw2qGl3eTVU26FnV_-Ak',
  LOGIN_DOMAIN: 'bunyan.local',       // user "ahmed" signs in as ahmed@bunyan.local

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
  name:      'Bunyan Contracting & Maintenance Est.',  // full legal name, used on PDFs and emails
  nameAr:    'مؤسسة البنيان للمقاولات والصيانة',
  short:     'Bunyan Contracting',                     // top bar, phone app name
  tagline:   'MEP works · Fit-out · Maintenance',
  taglineAr: 'أعمال الكهرباء والميكانيكا · التشطيبات · الصيانة',
  portalName: 'Bunyan Portal',
  industry:  'Contracting & services',                 // shown on the demo landing page

  city: 'Jeddah', cityAr: 'جدة', country: 'Kingdom of Saudi Arabia', countryAr: 'المملكة العربية السعودية',
  address:   'Office 7, Al Rawdah Business Center, Jeddah 23435, Saudi Arabia',
  addressAr: 'مكتب 7، مركز الروضة للأعمال، جدة',
  lat: 21.4858, lon: 39.1925,

  phones:  ['0500000201', '0500000202'],
  email:   'projects@bunyancontracting.example',
  website: 'www.bunyancontracting.example',

  crNo:  '7000000201',
  vatNo: '300000000000003',
  bank: [['Bank Name', 'Demo Bank'], ['Account No', '000000000000201'], ['IBAN', 'SA00 0000 0000 0000 0000 0201']],

  colors: {brand: '#2F3E5C', accent: '#EE7B22'},
  logo: 'assets/logo.svg',
  letterhead: {header: null, footer: null, stamp: null},

  // sign-in page: 'clock' (default) or 'map' = live world map with day/night, our office and the visitor's location
  loginVisual: 'map',

  modules: {documents: true, inventory: true, employees: true, kiosk: true},

  // document types: everything on (job cards = site work orders, material requests from sites)
  docTypes: {
    quotation: true, invoice: true, receipt: true, petty: true, dn: true, catalog: true /* price list */, customers: true,
    jobcard: true, mr: true, po: true
  },

  inventory: {
    categories: {'Electrical': 'EL', 'Plumbing': 'PL', 'HVAC': 'AC', 'Finishing': 'FN', 'Fixings': 'FX', 'PPE': 'PP', 'Tools': 'TL'},
    units: ['pcs', 'roll', 'box', 'bag', 'bucket', 'sheet', 'pair', 'set', 'cylinder', 'm', 'kg']
  }
};
