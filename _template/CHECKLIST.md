# New client proposal — checklist

## 1. Brief (Andrew fills, ~5 min)
Copy `_template/brief.example.json` to `<slug>.brief.json` at the repo root and fill every value.
Rules: plain service keywords (no city names); two biggest competitors in the region; price per location.

## 2. Scans (agent runs, ~1 hour) — where every number on the one-pager comes from
| Brief field | Source |
|---|---|
| locations[].reviews, health_score | `gbp_audit` / `gbp_get_audit_report` per location (business_urls = the Google Maps link) |
| locations[].grid (pins, top3, mid, low, none) | `local_seo_heatmaps_get_details view=heatmap` on the location's core-keyword grid (`position_distribution`) |
| locations[].rival | same heatmap `competitors` list — pick the highest-appearing **reviewed** business; skip listings with no rating/reviews |
| client_traffic, client_keywords | `se_list_sites` → `se_get_details` (monthly_traffic, keywords_count) |
| competitors[].traffic, keywords | `se_analyze_domain <competitor domain>` facets organic (competitors table gives traffic; keywords total_count) |
| competitors[].reviews, rating | `gbp_audit business_urls=[Google Maps URL]` per competitor, or the Google knowledge panel |
| ai_topics_hit | `llmv_get_overview view=brand` → platform_breakdown topics_label (e.g. "1/5") |
| gap_range_words | min and max of competitor ÷ client across traffic and keywords, written out |
Rank tracker: `krt_create_project` then `krt_add_keywords` once per location with `location="<City>, Michigan, United States"`. Never city names in keyword text.

## 3. Generate
`python3 scripts/new-client.py <slug>.brief.json` → writes `<slug>/index.html`, `full-audit.html`, `config.js` and prints the hub card.
Then complete every `<!-- FILL: ... -->` block in `<slug>/full-audit.html` from the scans above (delete the comment when done).

## 4. Copy pass (agent, then Andrew reads once as the client)
- No vendor names (Search Atlas, Merchynt, Paige). No "office"; say "location".
- No itemized deliverables, counts, or cadences on the one-pager. Sell the gap and how it closes.
- Same competitors in every chart. No junk/unreviewed listings named anywhere.
- Headline is the outcome, not a city.

## 5. Config + hub
- Paste the client's payment link into `<slug>/config.js`; the GHL webhook URL can be reused (page sends `client`).
- Paste the printed hub card into `index.html`.

## 6. QA (agent)
Phone widths 360/390 and desktop: no overflow, no script errors, pay buttons show and open the link, dark mode clean.
Then commit, push, wait for the Pages deploy, verify the live URL.

## 7. Send
`https://andrewauto8s.github.io/auto8-proposals/<slug>/` — the one-pager, not the hub.
