# auto8-proposals

Auto8 Central Proposals & Client Growth Hub.

- Live hub: https://andrewauto8s.github.io/auto8-proposals/ (passcode-protected)
- Each client proposal lives in its own folder (e.g. `zeppelin-cleaning/index.html`) and is linked from the hub card in `index.html`. Use relative links (`zeppelin-cleaning/`), never absolute (`/zeppelin-cleaning/`), because the site is served under the `/auto8-proposals/` path.

## Deployment

Every push to `main` deploys the repo root to GitHub Pages via `.github/workflows/pages.yml`. The repo's Pages source must be set to "GitHub Actions" (Settings → Pages).
