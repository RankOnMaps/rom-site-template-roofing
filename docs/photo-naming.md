# Photo naming + spec

All client photos live in `site/assets/img/photos/`. The build references specific filenames — if a file is missing, the site falls back to a placeholder.

## Naming convention

| Filename | What it is | Used where |
|---|---|---|
| `hero-bg.webp` | Homepage hero background | Top of index.html, preloaded |
| `hero-bg.jpg` | JPG fallback for hero | Browsers without WebP support |
| `founder-portrait.webp` | Founder face shot | About page, Reviews block |
| `team-crew.webp` | Group photo of the team | About page |
| `project-1.webp` through `project-6.webp` | Recent jobs | Projects gallery, home page tiles |
| `service-card-1.webp` through `service-card-N.webp` | Per-service hero | Service pages (one per service in `services.json`) |
| `vehicle.webp` | Branded truck/van | About page, footer |
| `service-area-hero.webp` | Aerial of primary city | Area landing pages |

## Spec

- **Format:** WebP preferred. JPG acceptable as fallback. PNG only for logos with transparency.
- **Dimensions:**
  - Hero: 1920 × 1080 minimum, 2560 × 1440 ideal
  - Founder portrait: 800 × 1000 (portrait orientation)
  - Project tiles: 1600 × 1200
  - Service cards: 1200 × 800
- **File size:** Hero under 300KB, others under 150KB. Use Squoosh or `cwebp -q 78` to compress.
- **Color:** Native daylight, no heavy filters. If client sends Instagram-filtered photos, request originals.
- **Composition:** Show the work. People-in-action beats hero shots of finished projects. Logos visible on shirts/trucks is a plus.

## What NOT to include

- Stock photography (Google reverse-image-search before using anything that looks polished)
- Photos with visible competitor logos
- Photos with watermarks from a previous website
- Anything the client doesn't have rights to (model releases for people-in-shot etc.)
- Receipt photos, mid-conversation candids, blurry phone shots

## If the client sent JPGs only

Keep them as JPGs for v1. Update the references in `build.py` if needed (search for `.webp` and change to `.jpg` for the specific files). v2 will auto-convert on push.
