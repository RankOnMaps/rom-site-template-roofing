# Transcript to client.json extraction prompt

This is the Claude prompt to convert a Fathom onboarding-call transcript into the three JSON files the rom-site-template needs. The template is now vertical-agnostic, so the same prompt works for roofing, plumbing, HVAC, dental, legal, restoration, landscaping, wellness, med spa, finance, security, moving, and appliance repair clients.

---

## How to use

1. Open Claude (claude.ai or Claude Code).
2. Paste the entire **PROMPT** block below as a single message.
3. Either paste the Fathom transcript text, or give Claude the Fathom recording URL so it can fetch via the Fathom MCP tool.
4. Claude returns three code blocks. Copy each into `data/client.json`, `data/services.json`, `data/areas.json` in the new client repo.

---

## Critical: vertical_label drives everything

The two fields `brand.vertical_label_singular` and `brand.vertical_label_plural` drive every templated phrase across the site. Get these right or the whole site reads wrong.

Examples:
- Roofing client: `"Roofer"` / `"Roofers"`
- Plumbing client: `"Plumber"` / `"Plumbers"`
- HVAC client: `"HVAC Technician"` / `"HVAC Technicians"`
- Dental client: `"Dentist"` / `"Dentists"`
- Legal client: `"Attorney"` / `"Attorneys"`
- Restoration client: `"Restoration Specialist"` / `"Restoration Specialists"`
- Wellness client: `"Wellness Provider"` / `"Wellness Providers"`
- Med spa client: `"Med Spa Provider"` / `"Med Spa Providers"`
- Landscaping client: `"Landscaper"` / `"Landscapers"`
- Moving client: `"Mover"` / `"Movers"`
- Appliance repair client: `"Appliance Technician"` / `"Appliance Technicians"`

The renderer uses these in H1s, breadcrumbs, schema `@type` selection, founder credentialing copy, and area page intros. A mismatch (e.g. setting `"Roofer"` for a dental practice) produces nonsense copy on 40+ rendered pages.

---

## PROMPT

> You are extracting structured data from a Fathom onboarding-call transcript for a new Rank On Maps client. Your output will be committed verbatim to a static-site repo and rendered into a marketing website. The template is vertical-agnostic and works for any local trade.
>
> Read the transcript I share next and produce three JSON files. Wrap each in a separate ` ```json ` code block labelled with the filename as the first comment line.
>
> ### Required output 1: `data/client.json`
>
> Follow this schema exactly. Every field is required unless marked optional. Use sensible inferred values where the transcript is silent, but flag anything inferred with `"_inferred": true` at the relevant block level. Never fabricate addresses, license numbers, founder names, or named testimonials. Use `"[TBC]"` if the value isn't in the transcript.
>
> ```json
> {
>   "brand": {
>     "name": "<full business name>",
>     "name_short": "<short version for nav>",
>     "parent_name": "<parent company or DBA, or empty string>",
>     "tagline": "<one-line positioning, 6-10 words>",
>     "vertical": "<roofing|plumbing|hvac|landscaping|dental|legal|restoration|wellness|medspa|finance|security|moving|appliance|other>",
>     "vertical_label_singular": "<Roofer|Plumber|Dentist|Attorney|Wellness Provider|etc>",
>     "vertical_label_plural": "<Roofers|Plumbers|Dentists|Attorneys|Wellness Providers|etc>"
>   },
>   "site": {
>     "url": "<https://primarydomain.com>",
>     "domain_apex": "<primarydomain.com>",
>     "cloudflare_project_name": "<lowercase-with-dashes slug>"
>   },
>   "contact": {
>     "phone": "<555-555-5555>",
>     "phone_display": "<(555) 555-5555>",
>     "email": "<contact email>",
>     "address": {"street":"...","city":"...","state":"<TX|FL|WI|etc>","zip":"...","country":"US"},
>     "geo": {"lat":0,"lng":0},
>     "hours": {"mon":"07:00-18:00","tue":"...","wed":"...","thu":"...","fri":"...","sat":"...","sun":"closed"},
>     "quote_url": "<external instant-quote URL, or empty string>"
>   },
>   "market": {
>     "primary_city": "<main city served>",
>     "region": "<regional descriptor e.g. Central Texas, North Phoenix Metro, Greater Milwaukee>",
>     "region_descriptor": "<sub-region e.g. Hill Country, North Shore, Lakefront>",
>     "state_long": "<Texas|Florida|Wisconsin|etc>",
>     "state_abbr": "<TX|FL|WI|etc>",
>     "metro_label": "<Austin Metro|Phoenix Metro|Milwaukee Metro|etc>",
>     "service_radius_miles": 75,
>     "primary_counties": ["County A","County B"],
>     "signature_neighborhoods": ["Suburb 1","Suburb 2","Suburb 3"]
>   },
>   "stats": {
>     "years_in_business": "<integer or string like 36+>",
>     "jobs_completed": "<5,000+ or empty>",
>     "patients_served": "<for wellness/dental/medspa: 10,000+ or empty>",
>     "cases_handled": "<for legal: 500+ or empty>",
>     "review_rating": "<0-5 decimal or [TBC]>",
>     "review_count": "<count as string>",
>     "founded_year_text": "<e.g. 1998>"
>   },
>   "founder": {
>     "name": "<First name only, the public-face founder>",
>     "first_name": "<same>",
>     "title": "<vertical-appropriate title, e.g. Master Plumber and Founder, DDS and Owner, Managing Partner, Licensed Wellness Practitioner>",
>     "years_experience": "<integer>",
>     "bio_short": "<60-80 words in direct-answer voice>",
>     "bio_long": "<150-220 words on the founder's full story: first job, the trade or clinical detail they're known for, what separates them from competitors>",
>     "signature_skills": ["Skill 1","Skill 2","Skill 3","Skill 4","Skill 5","Skill 6"]
>   },
>   "second_founder": {
>     "name": "<full name>",
>     "first_name": "<first only>",
>     "title": "<Co-Founder and Operations, Practice Manager, etc>",
>     "bio_short": "<40-60 words>",
>     "background": "<one sentence>"
>   },
>   "company_story": {
>     "headline": "<one-line story tagline>",
>     "narrative": "<80-120 words on the founding story>",
>     "family_of_companies": [{"name":"...","role":"...","url":"..."}]
>   },
>   "certifications": [
>     {"name": "<Cert or license name, e.g. ABO Board Certified, LEED AP, Master Plumber TX License #12345>", "tier": "<premium|trust>", "note": "<one-line note>"}
>   ],
>   "signature_specialties": [
>     {"name":"<Specialty headline>","summary":"<40-60 word summary>","anchor":"<kebab-case-anchor>"}
>   ],
>   "social": {
>     "google": "<https://maps.google.com/?cid=...>",
>     "facebook": "<https://facebook.com/...>",
>     "instagram": "<https://instagram.com/...>"
>   },
>   "links": {
>     "bbb_profile": "<full BBB profile URL or empty>",
>     "bbb_seal_image": "<BBB seal image URL or empty>"
>   },
>   "tracking": {
>     "ga4_measurement_id": "<G-XXXXXXXXXX or empty>",
>     "wc_account_id": "<WC account id or empty>",
>     "wc_profile_id": "<WC profile id or empty>",
>     "wc_tracker_host": "<s.xxxxxxxxxxxx.com or empty>",
>     "indexnow_key": "<32-char hex string, generate fresh per client via uuid4().hex>",
>     "_note": "Tracking IDs are usually empty at first. Daniel wires them in during the tracking-setup phase."
>   },
>   "deploy": {
>     "cloudflare_account_id_secret": "CLOUDFLARE_ACCOUNT_ID",
>     "cloudflare_api_token_secret": "CLOUDFLARE_API_TOKEN"
>   },
>   "service_areas_summary": "<one sentence summarizing the service area>"
> }
> ```
>
> ### Required output 2: `data/services.json`
>
> An array of service objects. Produce 5-10 entries for the new client. Each entry needs:
>
> ```json
> {
>   "slug": "<kebab-case-slug>",
>   "name": "<service display name>",
>   "h1": "<page H1 with primary city baked in>",
>   "description": "<40-60 word direct-answer summary>",
>   "process_steps": [{"title":"...","detail":"..."}],
>   "schema_offers": [{"name":"...","description":"..."}],
>   "faqs": [{"q":"...","a":"<40-60 word answer>"}]
> }
> ```
>
> Service examples by vertical:
> - Roofing: `roof-replacement`, `metal-roofing`, `hail-damage`, `free-roof-inspection`, `asphalt-shingle`
> - Plumbing: `drain-cleaning`, `water-heater-replacement`, `slab-leak-repair`, `sewer-line-repair`, `emergency-plumbing`
> - HVAC: `ac-repair`, `furnace-installation`, `heat-pump-replacement`, `duct-cleaning`, `mini-split-install`
> - Dental: `dental-implants`, `invisalign`, `cosmetic-dentistry`, `emergency-dental`, `teeth-whitening`
> - Legal: `personal-injury`, `family-law`, `estate-planning`, `criminal-defense`, `business-formation`
> - Restoration: `water-damage-restoration`, `mold-remediation`, `fire-damage-cleanup`, `storm-damage-repair`, `smoke-odor-removal`
> - Wellness: `hormone-replacement-therapy`, `iv-therapy`, `peptide-therapy`, `weight-management`, `medical-aesthetics`
>
> ### Required output 3: `data/areas.json`
>
> An array of service-area objects (one per city the client serves). 3-8 entries. Each entry needs:
>
> ```json
> {
>   "slug": "<kebab-case-slug>",
>   "name": "<City Name>",
>   "county": "<County Name>",
>   "zip_primary": "<55555>",
>   "h1": "<page H1>",
>   "card_summary": "<one-sentence summary for the areas-served grid>",
>   "search_volume": "<estimated monthly searches for {city} {vertical}>",
>   "tier": "<1|2|3>",
>   "lat": 0,
>   "lng": 0,
>   "landmarks": ["Landmark 1","Landmark 2"],
>   "neighborhoods": ["Neighborhood 1","Neighborhood 2","Neighborhood 3"],
>   "climate_note": "<one sentence on local climate or conditions that affect the trade>",
>   "intro_paragraphs": ["<para 1>","<para 2>","<para 3>"],
>   "what_we_do_locally": "<60-80 word summary of work in this city>",
>   "featured_services": ["<service-slug-1>","<service-slug-2>","<service-slug-3>"],
>   "faqs": [{"q":"...","a":"..."}]
> }
> ```
>
> The `featured_services` array references slugs from `services.json` and tells the renderer which service cards to surface on each area page. List the 3-4 highest-intent services for that specific city.
>
> ### Voice rules (apply to all generated copy)
>
> - **No em-dashes.** Use commas, semicolons, or new sentences.
> - **No AI flourishes.** No "moreover," "furthermore," "as we navigate," "elevate your," "unlock the power of."
> - **Direct-answer voice.** 40-60 word paragraphs that answer the question in the first sentence.
> - **Dollar-specific.** "$8,500 average bathroom replumb in Travis County" beats "affordable plumbing options."
> - **Named entities.** "Carrier Infinity 26 heat pump" beats "high-efficiency unit." "Dr. Sarah Chen, ABO Board Certified" beats "our experienced doctor."
> - **No fabricated specifics.** If the transcript doesn't say it, mark as `"[TBC]"` rather than invent. Never invent addresses, phone numbers, license numbers, founder names, named testimonials, or pricing.
> - **Trade-specific vocabulary.** Use the language an actual practitioner would use. If the transcript reveals technical depth (e.g. "22-gauge G90 galvalume," "20-gauge stainless cannula," "1031 exchange"), preserve it.
>
> Begin extraction now. Output the three code blocks back-to-back, nothing else.

---

## After Claude responds

1. Verify each block parses as JSON. Copy into a JSON validator if unsure (jsonlint.com).
2. Open the three files in the GitHub web UI, replace contents, commit.
3. Run the "Configure new client" workflow to apply.
4. Run the validation checklist in [docs/vertical-agnostic-checklist.md](vertical-agnostic-checklist.md) before triggering setup_client.py.

## When the transcript is thin

If the call didn't cover everything (often the case on first calls):

- `client.json`: fill what you have, leave `[TBC]` for what you don't. Mersad fills via follow-up email with the client before pushing.
- `services.json`: start from the vertical examples above. Only swap in the new client's services if the transcript names them.
- `areas.json`: if the transcript names 2 cities but the client serves 8, start with the 2 and add the rest after a follow-up.

The site renders fine with partial data and `[TBC]` placeholders. They show up as obvious gaps the client can review and approve before launch.
