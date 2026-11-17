// Quote delivery for N.B. Arch Co.
//
// formEndpoint is public. This file is copied into the published site.
// It is a destination for quote requests, not a place for a secret.
//
// Set formEndpoint to either:
//   "https://formspree.io/f/xxxxxxxx"   a form service that accepts a POST
//   "hello@nbarchcompany.com"           opens the visitor's email app
//
// hello@nbarchcompany.com is the main public inbox for quotes, custom
// orders, and general inquiries. help@nbarchcompany.com is for existing
// orders. That support address is shown on the page; this form does not
// send there.
//
// An empty string turns the submit button off and stores nothing.
// See the README for Formspree setup, file attachments, and redeploying.

window.NBARCH_CONFIG = {
  formEndpoint: "hello@nbarchcompany.com",
};
