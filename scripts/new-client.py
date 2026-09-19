#!/usr/bin/env python3
"""Generate a client proposal folder from _template/ and a brief JSON.

Usage:  python3 scripts/new-client.py path/to/<slug>.brief.json [--force]

Reads the brief, derives every number the pages need (totals, bar widths,
"x of y" strings, price total, sorted chart rows), fills the placeholders in
_template/index.html, _template/full-audit.html and _template/config.js, writes
<slug>/ and prints the hub card snippet to paste into index.html.
Any {{PLACEHOLDER}} left unfilled is reported and the run fails.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, '_template')

def n(v):  # 1996 -> "1,996"
    return f"{int(v):,}"

def pct(v, m):
    return f"{v / m * 100:.1f}%"

def chart(title, sub, rows, suffix):
    """rows: list of (name, value, is_client). Sorted ascending, client stays first."""
    client = [r for r in rows if r[2]]
    others = sorted([r for r in rows if not r[2]], key=lambda r: r[1])
    rows = client + others
    mx = max(r[1] for r in rows)
    out = [f'      <div class="cmp-figure">\n        <h3>{title}</h3>\n        <div class="sub">{sub}</div>\n        <div class="rows">\n']
    for name, v, you in rows:
        cls = ' you' if you else ''
        out.append(f'        <div class="cmp-row" title="{name}: {n(v)}{suffix}"><div class="cmp-label">{name}</div><div class="cmp-track"><div class="cmp-bar{cls}" style="width: {pct(v, mx)};"></div></div><div class="cmp-val">{n(v)}</div></div>\n')
    out.append('        </div>\n      </div>\n')
    return ''.join(out)

def derive(b):
    L1, L2 = b['locations'][0], b['locations'][1]
    C1, C2 = b['competitors'][0], b['competitors'][1]
    g1, g2 = L1['grid'], L2['grid']
    total_reviews = L1['reviews'] + L2['reviews']
    v = {
        'SLUG': b['slug'], 'BEACON_CLIENT_ID': b['beacon_client_id'],
        'CLIENT_NAME': b['client_name'], 'CLIENT_SHORT': b['client_short'], 'DOMAIN': b['domain'],
        'PREPARED': b['prepared'], 'INDUSTRY': b['industry'], 'SERVICE_KW': b['service_keyword'],
        'REGION': b['region'], 'COUNTY_PHRASE': b['county_phrase'],
        'CLIENT_RATING': b['client_rating'], 'CLIENT_TRAFFIC': n(b['client_traffic']), 'CLIENT_KEYWORDS': n(b['client_keywords']),
        'AI_HIT': b['ai_topics_hit'], 'GAP_RANGE_WORDS': b['gap_range_words'],
        'JOB_TYPES': b['job_types'], 'JOB_VALUE': b['job_value'],
        'PRICE_LOC': n(b['price_per_location']), 'PRICE_TOTAL': n(b['price_per_location'] * len(b['locations'])),
        'TOTAL_REVIEWS': n(total_reviews),
        'LOC1_NAME': L1['name'], 'LOC1_STREET': L1['street'], 'LOC1_REVIEWS': n(L1['reviews']), 'LOC1_SCORE': str(L1['health_score']),
        'LOC2_NAME': L2['name'], 'LOC2_STREET': L2['street'], 'LOC2_REVIEWS': n(L2['reviews']), 'LOC2_SCORE': str(L2['health_score']),
        'LOC1_FULL_ADDRESS': L1.get('full_address',''), 'LOC2_FULL_ADDRESS': L2.get('full_address',''),
        'LOC1_RIVAL': L1['rival']['name'], 'LOC1_RIVAL_REVIEWS': n(L1['rival']['reviews']),
        'LOC2_RIVAL': L2['rival']['name'], 'LOC2_RIVAL_REVIEWS': n(L2['rival']['reviews']),
        'COMP1_NAME': C1['name'], 'COMP2_NAME': C2['name'], 'COMP_RATING': C1['rating'],
    }
    for k, g in (('LOC1', g1), ('LOC2', g2)):
        v[f'{k}_PINS'] = str(g['pins']); v[f'{k}_RADIUS'] = str(g['radius_miles'])
        v[f'{k}_TOP3'] = str(g['top3']); v[f'{k}_MID'] = str(g['mid']); v[f'{k}_LOW'] = str(g['low']); v[f'{k}_NONE'] = str(g['none'])
        v[f'{k}_COMP_SPOTS'] = str(g['mid'] + g['low'])
        v[f'{k}_BAR'] = (f'<span class="seg-top3" style="width: {pct(g["top3"], g["pins"])};"></span><span class="seg-mid" style="width: {pct(g["mid"], g["pins"])};"></span>'
                         f'<span class="seg-low" style="width: {pct(g["low"], g["pins"])};"></span><span class="seg-none" style="width: {pct(g["none"], g["pins"])};"></span>')
    v['CHARTS'] = ('    <div class="cmp-grid">\n'
        + chart('Website visitors each month', "Estimated visits from Google search to each company's website.",
                [(b['client_short'], b['client_traffic'], True)] + [(c['name'], c['traffic'], False) for c in b['competitors']], ' visits per month')
        + chart('Google searches the website shows up for', "Number of different searches where each company's website appears in Google's results.",
                [(b['client_short'], b['client_keywords'], True)] + [(c['name'], c['keywords'], False) for c in b['competitors']], ' searches')
        + chart('Google reviews', f"{b['client_short']}'s two listings combined ({b['client_rating']} stars) against the two biggest names in the region ({C1['rating']} stars each).",
                [(b['client_short'], total_reviews, True)] + [(c['name'], c['reviews'], False) for c in b['competitors']], ' reviews')
        + '    </div>\n')
    return v

def render(text, v):
    out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: v.get(m.group(1), m.group(0)), text)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', out)))
    return out, left

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    brief = json.load(open(sys.argv[1], encoding='utf-8'))
    force = '--force' in sys.argv
    v = derive(brief)
    dest = os.path.join(ROOT, brief['slug'])
    if os.path.exists(dest) and not force: sys.exit(f'{dest} exists. Use --force to overwrite.')
    os.makedirs(dest, exist_ok=True)
    problems = []
    for f in ('index.html', 'full-audit.html', 'config.js'):
        text = open(os.path.join(TPL, f), encoding='utf-8').read()
        out, left = render(text, v)
        open(os.path.join(dest, f), 'w', encoding='utf-8').write(out)
        if left: problems.append((f, left))
        print(f'wrote {brief["slug"]}/{f}')
    fills = len(re.findall(r'<!-- FILL:', open(os.path.join(dest, 'full-audit.html'), encoding='utf-8').read()))
    print(f'\nfull-audit.html still has {fills} "<!-- FILL: ... -->" sections to complete from scans (see _template/CHECKLIST.md).')
    print('\nHub card to paste into index.html inside <div class="proposal-grid">:\n')
    print(f'''      <a href="{brief['slug']}/" class="proposal-card">
        <div class="card-top">
          <div class="client-name">{brief['client_name']}</div>
          <span class="status-badge">Active Proposal</span>
        </div>
        <p class="client-summary">Plain-English summary of where {brief['client_short']} shows up on Google today, where it doesn't, and how we close the gap across {len(brief['locations'])} locations. Full audit data linked from the summary.</p>
        <div class="card-meta-row">
          <div class="meta-chip">Retainer: <strong>${v['PRICE_TOTAL']} / mo</strong> (${v['PRICE_LOC']} / loc)</div>
          <div class="meta-chip">Locations: <strong>{len(brief['locations'])} Active Profiles</strong></div>
          <div class="meta-chip">Reviews: <strong>{v['TOTAL_REVIEWS']} ({brief['client_rating']} ★)</strong></div>
          <div class="cta-link">View Proposal <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></div>
        </div>
      </a>''')
    if problems:
        print('\nUNFILLED PLACEHOLDERS:')
        for f, left in problems: print(f'  {f}: {", ".join(left)}')
        sys.exit(1)
    print('\nAll placeholders filled. Next: complete the FILL sections in full-audit.html, run the QA sweep, add the hub card, commit, push.')

if __name__ == '__main__': main()
