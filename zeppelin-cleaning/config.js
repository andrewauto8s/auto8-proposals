// ============================================================
//  Zeppelin proposal settings — edit this file, nothing else.
//
//  PAYMENT_URL: paste your checkout / invoice link between the quotes.
//  While it is empty, the "Put me on the map" buttons stay hidden.
//
//  OPEN_WEBHOOK: paste an inbound-webhook URL (GoHighLevel workflow,
//  Zapier, Make...) and the page will POST a small JSON event whenever a
//  visitor opens it or taps the pay button. Your workflow can then text
//  you. Leave empty to disable. Events sent:
//    { "client": "zeppelin", "page": "summary" | "audit",
//      "event": "opened" | "pay_click", "when": ISO time,
//      "device": "phone" | "desktop", "referrer": "...", "url": "..." }
//
//  To stop your OWN visits from pinging you, open the page once with
//  ?me=1 on the end of the address on each device you use. That device
//  is then ignored for good (it's stored in the browser).
// ============================================================
window.AUTO8_PAYMENT_URL = "https://go.auto8.ai/payment-link/6a83f11bc8cc9a2ce72687cc";
window.AUTO8_OPEN_WEBHOOK = "https://services.leadconnectorhq.com/hooks/bgJlG66yBBWsAdgtyFep/webhook-trigger/602ee0b7-84e8-46b0-b8cc-d30a608c2678";
