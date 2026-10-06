/* =====================================================================
   LANDING PAGE SETTINGS — the product you are selling and how clients reach you.
   tools/build.py turns this into assets/config.js on the website.
   The list of demo companies is made from each company's config.js automatically.
   ===================================================================== */
window.PRODUCT = {
  name: 'Business Portal',
  tagline: 'Quotations, invoices, stock and staff for any company, in one simple web app.',
  contactName: 'Your Name',
  whatsapp: '9665XXXXXXXX',            // international format, digits only (used for the WhatsApp button)
  email: 'you@example.com',

  // what each demo company shows on its card (key = folder name in clients/)
  demoText: {
    trading: ['Price list → quotation → tax invoice with ZATCA QR',
              'Delivery notes with driver and van details',
              'Warehouse stock in cartons and bags, low-stock alerts',
              'Sales reps, drivers and loaders: attendance and overtime'],
    contracting: ['Job cards (work orders) for every site job',
                  'Material requests from site → purchase orders',
                  'Site store: cables, pipes, paint and PPE',
                  'Site crews check in at the kiosk, overtime worked out']
  }
};

// colours and logo of the landing page itself (not of a demo company)
window.BRAND = {
  name: 'Business Portal', short: 'Business Portal', portalName: 'Business Portal',
  phones: [''], colors: {brand: '#2B4C7E', accent: '#E8A33D'}, logo: 'assets/logo.svg'
};
