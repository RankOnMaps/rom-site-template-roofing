# Mersad runbook — spin up a new client site

This is the only doc you need. Every step is in GitHub's web UI. No terminal.

Estimated time: **45 minutes** for the first site, **15–25 minutes** once you've done a few.

---

## 1. Create the new repo from the template

1. Go to `https://github.com/RankOnMaps/rom-site-template`
2. Click the green **"Use this template"** button → **"Create a new repository"**
3. Owner: `RankOnMaps`
4. Repo name: client slug, lowercase + dashes (e.g. `nashville-elite-roofing`, `phoenix-hvac-pros`)
5. Visibility: **Private**
6. Click **Create repository from template**

You're now in the new repo.

---

## 2. Extract client data from the Fathom transcript

1. Open the Fathom recording for the onboarding call. Copy the share URL or the recording ID.
2. Open Claude (claude.ai or Claude Code).
3. Paste this prompt:

   > Read the Fathom transcript I'm about to share and produce a complete `data/client.json` file following the schema in [docs/transcript-to-client-json.md](transcript-to-client-json.md) in the rom-site-template repo. Also produce `data/services.json` and `data/areas.json` if there's enough info in the transcript. Wrap each file in a separate code block labelled with the filename.

4. Paste the Fathom transcript text (or the Fathom share URL — Claude can fetch it via the Fathom MCP).
5. Claude returns three code blocks: `client.json`, `services.json`, `areas.json`. Copy each.

---

## 3. Replace the JSON files in the new repo

In the GitHub web UI:

1. Open `data/client.json` → click the pencil icon → **delete everything** → paste Claude's `client.json` block → **Commit changes** to `main`.
2. Same for `data/services.json` and `data/areas.json`.

If Claude couldn't produce a complete `services.json` or `areas.json` (the transcript was thin on services or markets), leave them as-is for now and revisit after the discovery call.

---

## 4. Run "Configure client" to apply the changes across build.py

1. Go to the **Actions** tab.
2. Find **"Configure new client"** in the left sidebar → click it.
3. Click **Run workflow** → **Run workflow** (green button).
4. Wait ~30 seconds. The workflow:
   - reads `data/client.json`
   - runs `scripts/setup_client.py` which rewrites every Austin-specific string in `build.py`, `services.json`, `areas.json` with the new client's values
   - rewrites the Cloudflare project name in `deploy.yml`
   - writes the IndexNow keyfile
   - commits the changes back to `main`

This is the magic step. After this completes, the repo is ready to render the new client's site.

---

## 5. Upload client photos

1. Get the photo pack from the client (Google Drive, Dropbox, email). They should send 20+ photos: hero shot, team, recent jobs, before/after, vehicle/branding.
2. In the GitHub repo, navigate to `site/assets/img/photos/`.
3. Click **Add file → Upload files**.
4. Drag the photos in. Name them clearly:
   - `hero-bg.webp` — the homepage hero (will be preloaded)
   - `founder-portrait.webp` — founder/owner
   - `team-crew.webp` — team shot
   - `project-1.webp`, `project-2.webp`, etc. — recent jobs
5. Commit directly to `main`.

If client only sent JPGs and not WebPs, that's fine for v1 — just keep them as `.jpg` and reference them with the right extension. v2 will auto-convert.

For full photo naming spec, see [photo-naming.md](photo-naming.md).

---

## 6. Set Cloudflare secrets

1. In the repo: **Settings → Secrets and variables → Actions**.
2. Click **New repository secret** twice:
   - Name: `CLOUDFLARE_API_TOKEN` — value from 1Password entry "ROM Cloudflare → API Token"
   - Name: `CLOUDFLARE_ACCOUNT_ID` — value from 1Password entry "ROM Cloudflare → Account ID"
3. Click **Add secret** for each.

These are the same two values for every ROM client repo. (Later we can promote them to organization-level secrets so this step disappears.)

---

## 7. Push a trivial commit to trigger the first deploy

1. Open `README.md` → pencil icon → add a space at the end of any line → commit.
2. Go to **Actions** tab. The **"Build and deploy to Cloudflare Pages"** workflow runs.
3. Wait ~90 seconds. When green, the site is live at `https://<cloudflare-project-name>.pages.dev`.

The `cloudflare-project-name` is whatever you set in `data/client.json` → `site.cloudflare_project_name` (e.g. `nashville-elite-roofing`).

---

## 8. Point the custom domain

1. Log into Cloudflare → Pages → click the new project.
2. **Custom domains** tab → **Set up a custom domain**.
3. Enter the client's apex domain (e.g. `nashvilleeliteroofing.com`).
4. Cloudflare gives you DNS records to add. If the domain is registered at Cloudflare, it auto-adds them. If at GoDaddy/Namecheap, paste them into the registrar's DNS.
5. Add `www` as a second custom domain → set it to redirect to apex.
6. Wait 5-15 minutes for DNS to propagate. Site is now live at the custom domain.

---

## 9. Hand off to tracking phase

The site is built and live. Next phase (tracking, GBP, citations) is handled per [docs/tracking-setup.md](tracking-setup.md). For v1, ping Daniel and he'll wire up GA4 + GSC + WhatConverts. By v2, this will be runnable from a "Setup tracking" workflow button.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Configure client" workflow fails | Check the Actions log. Usually a JSON syntax error in `data/client.json` (missing comma, unclosed brace). Re-paste from Claude. |
| Build workflow fails on `KeyError` | A required field is missing from `data/client.json`. Compare to the schema in [transcript-to-client-json.md](transcript-to-client-json.md). |
| Site deploys but custom domain shows error | DNS hasn't propagated yet. Wait 15 min. If still broken, check Cloudflare Pages → Custom domains for a validation error. |
| Photos don't show on the live site | Filenames must match what `build.py` expects. Check `site/assets/img/photos/` — files must be named `hero-bg.webp`, `founder-portrait.webp`, etc. |
| Site looks like Austin Area Roofers (old brand showing) | "Configure client" workflow didn't run, or `data/client.json` still has the baseline Austin values. Re-edit and re-run. |
| Site is live but no leads coming in | Tracking phase hasn't been done yet. That's the next workflow, not this one. |

---

## When to ask Daniel

- The transcript is too thin for Claude to produce a complete `client.json` — ask Daniel to clarify the missing fields from the call.
- The client is in a vertical that's not roofing-adjacent and `services.json` doesn't transfer at all — ask Daniel for a vertical-specific data pack.
- Anything about Cloudflare account access, DNS, or GA4/GSC setup until the tracking-setup workflow is built out.
