# ROM site template

This is the Rank On Maps client-site template. Forking it creates a complete, elite-tier marketing site for any local-trade business — schema markup, AI citability, full tracking infrastructure, Cloudflare Pages auto-deploy on push.

The reference build is **Austin Area Roofers** ([austinarearoofers.com](https://austinarearoofers.com)). Every value that changes per client lives in [data/client.json](data/client.json).

---

## How a new client site gets built (the whole process)

1. **Click "Use this template" → Create a new repository** under `RankOnMaps/<client-slug>`. The new repo is private by default. Add Mersad as a collaborator.
2. **Get the onboarding-call transcript** from Fathom. Drop it into Claude alongside [docs/transcript-to-client-json.md](docs/transcript-to-client-json.md). Claude returns a complete `data/client.json` (and optionally `services.json` + `areas.json`).
3. **Replace the placeholder JSON files** in the new repo with Claude's output. Commit via the GitHub web UI (no terminal needed).
4. **Run setup_client.py** from the Actions tab → "Configure new client" workflow → Run workflow. It rewrites build.py and the data files with the new client's brand strings.
5. **Upload client photos** to `site/assets/img/photos/` via the GitHub UI or GitHub Desktop. Naming follows [docs/photo-naming.md](docs/photo-naming.md).
6. **Set repo secrets**: Settings → Secrets → Actions. Add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` (values are in 1Password under "ROM Cloudflare").
7. **Push** (any commit to `main` triggers the build). Cloudflare Pages deploys the rendered site within 90 seconds.
8. **Point the domain** in Cloudflare Pages → Custom domains. Add the apex + `www`. DNS propagates in 5-15 minutes.

That's the whole loop. No terminal, no Python locally, no code edits beyond JSON.

---

## Repo structure

```
rom-site-template/
├── data/
│   ├── client.json          ← master config — EDIT THIS FIRST
│   ├── services.json        ← service catalog (Austin roofing example, replace per client)
│   ├── areas.json           ← service areas (Austin cities example, replace per client)
│   └── reviews.json         ← curated client reviews
├── site/
│   ├── _headers             ← Cloudflare Pages cache rules (keep as-is)
│   └── assets/              ← CSS, photos, fonts, SVG
├── scripts/
│   └── setup_client.py      ← rewrites build.py + data with client.json values
├── docs/
│   ├── mersad-runbook.md            ← step-by-step for Mersad
│   ├── transcript-to-client-json.md ← Claude prompt for Fathom transcript extraction
│   └── photo-naming.md              ← photo naming + spec for /site/assets/img/photos/
├── .github/workflows/
│   ├── deploy.yml                   ← build + deploy on every push to main
│   └── configure.yml                ← manually triggered: runs setup_client.py + commits
└── build.py                          ← the renderer (don't edit — it reads from data/)
```

---

## Client-onboarding sequence (manager view)

The ROM team handles client setup in this order. Mersad executes; Jonathan owns the client relationship.

| Phase | Owner | Where | What |
|---|---|---|---|
| Discovery call | Jonathan + Daniel | Fathom | Records the onboarding call. Transcript becomes the data source. |
| Site build | Mersad | This repo, per client | Steps 1-7 above. Site live within 24 hours of the call. |
| Tracking + GBP | Mersad | hello@rankonmaps.io | GA4, Search Console, WhatConverts, GBP optimization. See [docs/tracking-setup.md](docs/tracking-setup.md). |
| Citations + content | Link builder + Mersad | BrightLocal + manual | Citations submitted via BrightLocal. Blog cadence handled by content team. |
| Launch + monitor | Jonathan | Slack client channel | Confirms launch, schedules monthly delta review. |

---

## What's in this template that you don't have to think about

Every site built from this template inherits the elite-tier stack automatically:

- **Schema.org JSON-LD graph** — LocalBusiness, Organization, Service, FAQPage, BreadcrumbList, SpeakableSpecification, Review schemas on every page
- **AI citability** — 17/17 citation patterns built into rendering (direct-answer paragraphs, FAQ schema, speakable spec, citation-ready specifics, llms.txt)
- **Performance** — responsive `<picture>` with media-targeted preload, async font loading, lazy-loaded third-party JS via `requestIdleCallback`
- **Accessibility** — WCAG AA contrast on every text/background pair, proper heading order, sr-only landmarks, skip links
- **Tracking** — GA4 web stream + WhatConverts DNI + call tracking, wired to fire on form submit + phone click + email click events
- **Indexing** — Google Indexing API trigger + Bing IndexNow protocol + GSC sitemap submission on first push
- **Cache headers** — Cloudflare `_headers` file with year-long immutable cache on assets, 5-min revalidate on HTML

Mersad does not need to touch any of this. He fills `data/client.json`, replaces `services.json` + `areas.json`, drops photos, pushes.

---

## Versioning

- **v1 (current)** — clone, fill JSON, find/replace via setup_client.py, push. Same visual design across all clients. Designed for roofing + adjacent local-trade verticals.
- **v2 (planned)** — vertical-specific theme variants (HVAC, plumbing, landscaping, dental, legal). Component-level brand kit injection.
- **v3 (planned)** — generation from CRM/Fathom directly, no manual JSON editing.

---

## Support

- **Mersad**: post in the `#rom-builds` Slack channel if a build fails or the site renders incorrectly.
- **Daniel**: owns the template repo. Push improvements upstream — new features merged here benefit every future client.
