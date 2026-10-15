/* =====================================================================
   LANDING PAGE SETTINGS — the product you are selling and how clients reach you.
   tools/build.py turns this into assets/config.js on the website.
   The list of demo companies is made from each company's config.js automatically.
   ===================================================================== */
window.PRODUCT = {
  name: 'RabtFlow',
  tagline: 'Quotations, invoices, stock and staff for any company, in one simple web app.',
  contactName: 'Azeem Bukhari',
  whatsapp: '966531566837',            // international format, digits only (used for the WhatsApp button)
  email: 'syed.azeemb@gmail.com',

  // what each demo company shows on its card (key = folder name in clients/)
  demoText: {
    trading: ['Customer records', 'Create and save quotations', 'Generate quotation PDFs', 'Review quotation history'],
    contracting: ['Customer records', 'Create and save quotations', 'Generate quotation PDFs', 'Review quotation history']
  }
};

// colours and logo of the landing page itself (not of a demo company)
window.BRAND = {
  name: 'RabtFlow', short: 'Business Portal', portalName: 'Business Portal',
  phones: [''], colors: {brand: '#2B4C7E', accent: '#E8A33D'}, logo: 'assets/logo.svg'
};
