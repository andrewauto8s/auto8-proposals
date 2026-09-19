# auto8-proposals

Auto8 Central Proposals & Client Growth Hub.

- Live hub: https://andrewauto8s.github.io/auto8-proposals/ (passcode-protected)
- Each client proposal lives in its own folder (e.g. `zeppelin-cleaning/index.html`) and is linked from the hub card in `index.html`. Use relative links (`zeppelin-cleaning/`), never absolute (`/zeppelin-cleaning/`), because the site is served under the `/auto8-proposals/` path.

## Deployment

Every push to `main` deploys the repo root to GitHub Pages via `.github/workflows/pages.yml`. The repo's Pages source must be set to "GitHub Actions" (Settings → Pages).

## Starting a new client

1. Copy `_template/brief.example.json` to `<slug>.brief.json` and fill it in.
2. Run `python3 scripts/new-client.py <slug>.brief.json`.
3. Complete the `<!-- FILL: ... -->` sections in `<slug>/full-audit.html`, paste the printed hub card into `index.html`, set the payment link in `<slug>/config.js`.
4. Follow `_template/CHECKLIST.md` for the scans, copy rules and QA, then push.
