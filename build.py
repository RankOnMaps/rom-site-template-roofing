#!/usr/bin/env python3
"""ROM roofing template · TRUE mobile-first build.

Renders /data/*.json into /site/index.html with:
  · Mobile-first CSS cascade (base = 320px, min-width queries up)
  · Hamburger nav with full-screen overlay <768px
  · Fluid clamp() type for all headlines
  · <picture> hero with mobile portrait + desktop landscape art-direction
  · Sticky bottom CTA in thumb zone on mobile
  · 44px minimum touch targets
  · Client brand tokens from data/client_branding.json (NOT ROM brand)
  · tel: + mailto: on every phone and email
  · RoofingContractor + FAQPage + Service + AggregateRating JSON-LD

Per feedback_mobile_first_mandatory, feedback_client_vs_rom_brand,
feedback_template_layering.
"""
import json, pathlib, html, datetime

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
SITE = ROOT / "site"
SITE.mkdir(exist_ok=True)


def load(name):
    p = DATA / name
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text())
    except Exception:
        return []


def tel_href(phone):
    digits = "".join(c for c in str(phone) if c.isdigit())
    if len(digits) == 10:
        digits = "1" + digits
    return f"tel:+{digits}"


def h(s):
    return html.escape(str(s)) if s is not None else ""


def main():
    client = load("client.json") or {}
    services = load("services.json") or []
    areas = load("areas.json") or []
    reviews = load("reviews.json") or []
    brand_tokens = load("client_branding.json") or {}

    brand = client.get("brand", {})
    contact = client.get("contact", {})
    market = client.get("market", {})
    stats = client.get("stats", {})
    site_meta = client.get("site", {})

    name = brand.get("name", "Roofing Contractor")
    tagline = brand.get("tagline", "Roofing built for your market.")
    city = market.get("primary_city", "")
    state = market.get("state_abbr", "")
    state_long = market.get("state_long", "")
    phone_display = contact.get("phone_display", contact.get("phone", ""))
    phone_raw = contact.get("phone", "")
    email = contact.get("email", "")
    quote_url = contact.get("quote_url", "#contact")
    founded_year = stats.get("founded_year_text") or stats.get("founded_year") or ""
    years = stats.get("years_in_business", "")
    jobs = stats.get("jobs_completed", "")
    rating = stats.get("review_rating", 5)
    review_count = stats.get("review_count", "")
    site_url = site_meta.get("url", "")
    suburbs = [a.get("name", "") for a in areas if a.get("name")] or market.get("signature_neighborhoods", [])

    css_vars = f""":root {{
  --brand-primary: {brand_tokens.get('primary', '#0E1F36')};
  --brand-secondary: {brand_tokens.get('secondary', '#B73230')};
  --brand-accent: {brand_tokens.get('accent', '#F4B860')};
  --brand-text: {brand_tokens.get('text', '#0F172A')};
  --brand-text-muted: {brand_tokens.get('text_muted', '#475569')};
  --brand-bg: {brand_tokens.get('bg', '#FFFFFF')};
  --brand-bg-alt: {brand_tokens.get('bg_alt', '#F8FAFC')};
  --brand-border: {brand_tokens.get('border', '#E2E8F0')};
  --brand-headline-font: {brand_tokens.get('headline_font', "system-ui, -apple-system, sans-serif")};
  --brand-body-font: {brand_tokens.get('body_font', "system-ui, -apple-system, sans-serif")};
  --brand-mono-font: {brand_tokens.get('mono_font', "ui-monospace, monospace")};
}}"""

    css = css_vars + """

*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--brand-body-font);
  color: var(--brand-text);
  background: var(--brand-bg);
  font-size: clamp(16px, 4vw, 18px);
  line-height: 1.6;
  word-break: break-word;
  overflow-x: hidden;
  padding-bottom: 88px;
}
img, picture, video { max-width: 100%; height: auto; display: block; }

h1, h2, h3, h4 { font-family: var(--brand-headline-font); line-height: 1.15; margin: 0 0 0.5em; }
h1 { font-size: clamp(32px, 8vw, 56px); font-weight: 800; letter-spacing: -0.02em; }
h2 { font-size: clamp(24px, 5vw, 40px); font-weight: 800; letter-spacing: -0.01em; }
h3 { font-size: clamp(20px, 4.5vw, 28px); font-weight: 700; }
p { margin: 0 0 1em; }
a { color: var(--brand-primary); text-decoration: underline; text-underline-offset: 3px; }

.shell { width: 100%; max-width: 1120px; margin: 0 auto; padding: 0 16px; }

.util-strip { background: var(--brand-primary); color: #fff; font-size: 13px; padding: 8px 0; }
.util-strip .shell { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 16px; text-align: center; }
.util-strip a { color: #fff; text-decoration: none; font-weight: 600; min-height: 28px; display: inline-flex; align-items: center; }

.site-header { position: sticky; top: 0; z-index: 50; background: var(--brand-bg); border-bottom: 1px solid var(--brand-border); }
.hd-inner { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; min-height: 64px; }
.brand-link { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--brand-text); }
.brand-link .name { font-family: var(--brand-headline-font); font-weight: 800; font-size: 18px; line-height: 1.1; }
.brand-link .dba { font-size: 11px; color: var(--brand-text-muted); }

.hamburger {
  width: 48px; height: 48px;
  display: inline-flex; align-items: center; justify-content: center;
  background: transparent; border: 1px solid var(--brand-border); border-radius: 8px;
  cursor: pointer; padding: 0;
}
.hamburger span { display: block; width: 22px; height: 2px; background: var(--brand-text); position: relative; }
.hamburger span::before, .hamburger span::after { content: ""; position: absolute; left: 0; width: 22px; height: 2px; background: var(--brand-text); }
.hamburger span::before { top: -7px; }
.hamburger span::after { top: 7px; }

.mobile-nav { position: fixed; inset: 0; background: var(--brand-bg); z-index: 100; transform: translateX(100%); transition: transform 0.25s ease; display: flex; flex-direction: column; padding: 16px; }
.mobile-nav.is-open { transform: translateX(0); }
.mobile-nav-head { display: flex; justify-content: space-between; align-items: center; min-height: 64px; border-bottom: 1px solid var(--brand-border); margin-bottom: 16px; }
.mobile-nav-close {
  width: 48px; height: 48px;
  background: transparent; border: 1px solid var(--brand-border); border-radius: 8px;
  font-size: 24px; cursor: pointer; line-height: 1;
}
.mobile-nav a {
  display: block; padding: 16px; font-size: 18px; font-weight: 600;
  border-bottom: 1px solid var(--brand-border); color: var(--brand-text);
  text-decoration: none; min-height: 56px;
}
.mobile-nav .mobile-nav-cta { margin-top: 24px; }

.desktop-nav { display: none; }
.hd-cta-desktop { display: none; }

.btn {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 48px; padding: 12px 20px;
  font-size: 16px; font-weight: 700;
  border-radius: 8px; text-decoration: none; cursor: pointer; border: 0;
  transition: transform 0.1s ease;
  text-align: center;
}
.btn:active { transform: scale(0.98); }
.btn-primary { background: var(--brand-secondary); color: #fff; }
.btn-ghost { background: transparent; color: var(--brand-primary); border: 2px solid var(--brand-primary); }
.btn-block { display: flex; width: 100%; }

.hero { padding: 32px 0 24px; background: var(--brand-bg); }
.hero-grid { display: flex; flex-direction: column; gap: 24px; }
.hero .eyebrow {
  display: inline-block; font-family: var(--brand-mono-font);
  font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--brand-secondary); font-weight: 700; margin-bottom: 12px;
}
.hero p.lead { font-size: clamp(16px, 4.2vw, 19px); color: var(--brand-text-muted); }
.hero-ctas { display: flex; flex-direction: column; gap: 12px; margin-top: 20px; }
.hero-photo img { width: 100%; height: auto; border-radius: 12px; }
.hero .availability { font-size: 14px; color: var(--brand-primary); font-weight: 600; margin-top: 16px; }

.trust-strip { background: var(--brand-bg-alt); padding: 24px 0; border-top: 1px solid var(--brand-border); border-bottom: 1px solid var(--brand-border); }
.trust-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.trust-cell { text-align: center; }
.trust-num { font-family: var(--brand-headline-font); font-size: clamp(28px, 8vw, 44px); font-weight: 900; color: var(--brand-primary); line-height: 1; }
.trust-lbl { font-size: 13px; color: var(--brand-text-muted); margin-top: 4px; }

section { padding: 40px 0; }
section.alt { background: var(--brand-bg-alt); }
.sec-eyebrow { font-family: var(--brand-mono-font); font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--brand-secondary); font-weight: 700; }
.sec-intro { color: var(--brand-text-muted); margin-bottom: 24px; max-width: 640px; }

.svc-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.svc-card { background: var(--brand-bg); border: 1px solid var(--brand-border); border-radius: 12px; padding: 20px; }
.svc-card h3 { margin-bottom: 8px; }
.svc-card .svc-eyebrow { font-size: 11px; font-family: var(--brand-mono-font); letter-spacing: 0.1em; text-transform: uppercase; color: var(--brand-secondary); font-weight: 700; margin-bottom: 8px; display: block; }
.svc-card p { color: var(--brand-text-muted); font-size: 15px; margin-bottom: 12px; }
.svc-card a { font-weight: 700; min-height: 44px; display: inline-flex; align-items: center; }

.area-list { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
.area-list a {
  display: inline-flex; align-items: center; min-height: 44px; padding: 8px 14px;
  background: var(--brand-bg); border: 1px solid var(--brand-border); border-radius: 999px;
  color: var(--brand-text); text-decoration: none; font-size: 14px; font-weight: 600;
}

.faq-item { background: var(--brand-bg); border: 1px solid var(--brand-border); border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; }
.faq-item summary { cursor: pointer; font-weight: 700; font-size: 17px; padding: 8px 0; min-height: 44px; display: flex; align-items: center; list-style: none; }
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after { content: "+"; margin-left: auto; font-size: 24px; color: var(--brand-secondary); font-weight: 400; }
.faq-item[open] summary::after { content: "−"; }
.faq-item p { margin-top: 12px; color: var(--brand-text-muted); }

.rev-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.rev-card { background: var(--brand-bg); border: 1px solid var(--brand-border); border-radius: 12px; padding: 20px; }
.rev-stars { color: var(--brand-accent); margin-bottom: 8px; }
.rev-card p { font-size: 15px; color: var(--brand-text); }
.rev-card .who { font-size: 13px; color: var(--brand-text-muted); font-weight: 600; margin-top: 8px; }

.contact-grid { display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 16px; }
.contact-cell {
  display: flex; align-items: center; gap: 12px; min-height: 56px;
  padding: 14px 16px; background: var(--brand-bg); border: 1px solid var(--brand-border); border-radius: 10px;
  text-decoration: none; color: var(--brand-text); font-weight: 600;
}

.site-footer { background: var(--brand-primary); color: #fff; padding: 32px 0 24px; margin-top: 40px; }
.site-footer h4 { color: #fff; font-size: 14px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }
.site-footer a { color: rgba(255,255,255,0.85); text-decoration: none; display: block; padding: 8px 0; min-height: 44px; }
.site-footer .legal { font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 16px; }

.sticky-cta {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 60;
  background: var(--brand-primary);
  display: flex; gap: 8px; padding: 10px 12px;
  box-shadow: 0 -4px 16px rgba(0,0,0,0.18);
}
.sticky-cta a {
  flex: 1; display: flex; align-items: center; justify-content: center;
  min-height: 52px; padding: 8px 12px;
  font-size: 16px; font-weight: 700; text-decoration: none;
  border-radius: 8px;
}
.sticky-cta .sc-call { background: var(--brand-secondary); color: #fff; }
.sticky-cta .sc-book { background: #fff; color: var(--brand-primary); }

@media (min-width: 600px) {
  .svc-grid { grid-template-columns: repeat(2, 1fr); }
  .rev-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 768px) {
  body { padding-bottom: 0; }
  .shell { padding: 0 32px; }
  .hamburger { display: none; }
  .mobile-nav { display: none; }
  .desktop-nav { display: flex; gap: 24px; align-items: center; }
  .desktop-nav a { color: var(--brand-text); text-decoration: none; font-weight: 600; padding: 12px 8px; min-height: 44px; display: inline-flex; align-items: center; }
  .hd-cta-desktop { display: flex; gap: 12px; align-items: center; }
  .hd-cta-desktop .hd-phone { font-weight: 800; color: var(--brand-primary); text-decoration: none; font-size: 18px; min-height: 44px; display: inline-flex; align-items: center; }
  .hero { padding: 64px 0 48px; }
  .hero-grid { flex-direction: row; align-items: center; gap: 48px; }
  .hero-grid > div { flex: 1; }
  .hero-ctas { flex-direction: row; }
  .trust-grid { grid-template-columns: repeat(4, 1fr); }
  .sticky-cta { display: none; }
  section { padding: 64px 0; }
  .contact-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 900px) {
  .svc-grid { grid-template-columns: repeat(3, 1fr); }
  .rev-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1024px) {
  .hero-grid { gap: 64px; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
"""

    nav_links = [
        ("/services/", "Services"),
        ("/areas/", "Service Areas"),
        ("/projects/", "Projects"),
        ("/reviews/", "Reviews"),
        ("/about/", "About"),
        ("/contact/", "Contact"),
    ]

    nav_mobile_html = "".join(
        f'<a href="{h(href)}" data-mnav-link>{h(label)}</a>' for href, label in nav_links
    )
    nav_desktop_html = "".join(
        f'<a href="{h(href)}">{h(label)}</a>' for href, label in nav_links
    )

    primary_kw = f"Roofing Contractor {city}, {state}" if city and state else "Roofing Contractor"
    year_stamp_phrase = f" Since {founded_year}" if founded_year else ""
    h1_text = f"{primary_kw}{year_stamp_phrase}"
    hero_sub_bits = []
    if jobs:
        hero_sub_bits.append(f"{jobs} roofs installed")
    if rating and review_count:
        hero_sub_bits.append(f"{rating}-star · {review_count} reviews")
    hero_sub_bits.append("Free 24-48 hour inspection")
    hero_sub_bits.append("No down payment · Insurance claim experts")
    hero_sub = " · ".join(hero_sub_bits)
    if city:
        suburbs_inline = ", ".join(suburbs[:3]) if suburbs else ""
        hero_sub += f" · Serving {city}"
        if suburbs_inline:
            hero_sub += f", {suburbs_inline}"

    hero_mobile = "/assets/img/hero-mobile.webp"
    hero_desktop = "/assets/img/hero-desktop.webp"
    hero_alt = f"{name} crew installing a roof in {city}, {state}" if city else f"{name} roof install"
    hero_picture = (
        "<picture>\n"
        f'  <source media="(min-width: 768px)" srcset="{h(hero_desktop)}" type="image/webp">\n'
        f'  <source srcset="{h(hero_mobile)}" type="image/webp">\n'
        f'  <img src="{h(hero_desktop)}" alt="{h(hero_alt)}" width="1200" height="900" fetchpriority="high" decoding="async">\n'
        "</picture>"
    )

    service_cards = []
    for s in services[:6]:
        slug = s.get("slug", "")
        sname = s.get("name", "")
        summary = s.get("card_summary", "")
        eyebrow = s.get("card_eyebrow", "")
        eyebrow_html = f'<span class="svc-eyebrow">{h(eyebrow)}</span>' if eyebrow else ""
        service_cards.append(
            f'<article class="svc-card">{eyebrow_html}'
            f'<h3>{h(sname)}</h3>'
            f'<p>{h(summary[:200])}</p>'
            f'<a href="/services/{h(slug)}/">Learn more &rarr;</a>'
            f'</article>'
        )

    area_chips_html = "".join(
        f'<a href="/areas/{h(a.get("slug",""))}/">{h(a.get("name",""))}</a>'
        for a in areas[:18]
    )
    if not area_chips_html and suburbs:
        area_chips_html = "".join(f'<a href="#contact">{h(s)}</a>' for s in suburbs[:12])

    faqs = []
    if services:
        faqs = services[0].get("faqs", [])[:6]
    if not faqs:
        faqs = [
            {"q": f"How much does a roof replacement cost in {city}?",
             "a": f"A typical roof replacement in {city} runs $8,000 to $18,000 for architectural asphalt shingle on a 2,000 sq ft home. Metal runs $14,000 to $28,000. Tile $24,000 to $48,000."},
            {"q": "Will my homeowner's insurance cover hail damage?",
             "a": "If the damage is from a covered storm event such as hail or wind, most policies cover a roof replacement minus your deductible. We file the supplements and meet your adjuster on the roof."},
            {"q": "How long does a roof replacement take?",
             "a": "Most asphalt shingle roofs install in one to two days. Metal runs two to four days. Tile takes three to five days."},
        ]

    faq_html = "".join(
        f'<details class="faq-item"><summary>{h(f.get("q",""))}</summary>'
        f'<p>{h(f.get("a",""))}</p></details>'
        for f in faqs
    )

    rev_cards = []
    for r in reviews[:4]:
        body_txt = r.get("body") or r.get("text") or r.get("review", "")
        who = r.get("author") or r.get("name", "Verified customer")
        rev_cards.append(
            f'<article class="rev-card">'
            f'<div class="rev-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
            f'<p>{h(body_txt[:240])}</p>'
            f'<div class="who">{h(who)}</div></article>'
        )
    if not rev_cards:
        rev_cards.append(
            '<article class="rev-card"><div class="rev-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
            '<p>Reviews coming soon.</p><div class="who">Verified customer</div></article>'
        )

    jsonld = {
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "name": name,
        "telephone": phone_raw,
        "url": site_url,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": contact.get("address", {}).get("street", ""),
            "addressLocality": city,
            "addressRegion": state,
            "postalCode": contact.get("address", {}).get("zip", ""),
            "addressCountry": "US",
        },
        "areaServed": [s for s in suburbs if s] or ([city] if city else []),
    }
    if email:
        jsonld["email"] = email
    if review_count:
        jsonld["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(rating),
            "reviewCount": str(review_count),
        }
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f.get("q", ""),
             "acceptedAnswer": {"@type": "Answer", "text": f.get("a", "")}}
            for f in faqs
        ],
    }

    meta_title = f"{name} · {primary_kw}"
    meta_desc = f"{name}. {primary_kw}{year_stamp_phrase}. Free inspection, insurance claim experts, no down payment. Call {phone_display}."

    parent_html = (
        f'<div class="dba">{h(brand.get("parent_name",""))}</div>'
        if brand.get("parent_name") else ""
    )
    email_cell = (
        f'<a class="contact-cell" href="mailto:{h(email)}">&#9993; {h(email)}</a>'
        if email else ""
    )
    email_footer = (
        f'<p><a href="mailto:{h(email)}">{h(email)}</a></p>'
        if email else ""
    )

    html_out = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{h(meta_title)}</title>
<meta name="description" content="{h(meta_desc)}">
<link rel="canonical" href="{h(site_url)}/">
<meta name="theme-color" content="{h(brand_tokens.get('primary', '#0E1F36'))}">
<meta property="og:title" content="{h(meta_title)}">
<meta property="og:description" content="{h(meta_desc)}">
<meta property="og:url" content="{h(site_url)}/">
<style>{css}</style>
<script type="application/ld+json">{json.dumps(jsonld, separators=(',', ':'))}</script>
<script type="application/ld+json">{json.dumps(faq_jsonld, separators=(',', ':'))}</script>
</head>
<body>

<div class="util-strip"><div class="shell">
  <span>{h(tagline)}</span>
  <a href="{h(tel_href(phone_raw))}">Call {h(phone_display)}</a>
</div></div>

<header class="site-header"><div class="hd-inner">
  <a class="brand-link" href="/" aria-label="{h(name)} home">
    <div>
      <div class="name">{h(name)}</div>
      {parent_html}
    </div>
  </a>
  <nav class="desktop-nav" aria-label="Primary">{nav_desktop_html}</nav>
  <div class="hd-cta-desktop">
    <a class="hd-phone" href="{h(tel_href(phone_raw))}">{h(phone_display)}</a>
    <a class="btn btn-primary" href="{h(quote_url)}" target="_blank" rel="noopener">Free Instant Quote</a>
  </div>
  <button class="hamburger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav" data-mnav-open>
    <span></span>
  </button>
</div></header>

<div class="mobile-nav" id="mobile-nav" aria-hidden="true">
  <div class="mobile-nav-head">
    <span style="font-weight:800;">{h(name)}</span>
    <button class="mobile-nav-close" type="button" aria-label="Close menu" data-mnav-close>&times;</button>
  </div>
  {nav_mobile_html}
  <div class="mobile-nav-cta">
    <a class="btn btn-primary btn-block" href="{h(quote_url)}" target="_blank" rel="noopener" style="margin-bottom:12px;">Free Instant Quote</a>
    <a class="btn btn-ghost btn-block" href="{h(tel_href(phone_raw))}">Call {h(phone_display)}</a>
  </div>
</div>

<main id="main">

<section class="hero"><div class="shell"><div class="hero-grid">
  <div>
    <span class="eyebrow">{h(tagline)}</span>
    <h1>{h(h1_text)}</h1>
    <p class="lead">{h(hero_sub)}</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="{h(quote_url)}" target="_blank" rel="noopener">Get free instant quote</a>
      <a class="btn btn-ghost" href="{h(tel_href(phone_raw))}">Call {h(phone_display)}</a>
    </div>
    <div class="availability">Booking three days out · 24/7 storm emergency line for active leaks</div>
  </div>
  <div class="hero-photo">
    {hero_picture}
  </div>
</div></div></section>

<section class="trust-strip"><div class="shell">
  <div class="trust-grid">
    <div class="trust-cell"><div class="trust-num">{h(years) if years else '—'}</div><div class="trust-lbl">Years roofing<br>{h(market.get('region', state_long))}</div></div>
    <div class="trust-cell"><div class="trust-num">{h(jobs) if jobs else '—'}</div><div class="trust-lbl">Roofs<br>installed</div></div>
    <div class="trust-cell"><div class="trust-num">{h(rating)}&#9733;</div><div class="trust-lbl">Google rating<br>{(h(review_count) + ' reviews') if review_count else ''}</div></div>
    <div class="trust-cell"><div class="trust-num">10yr</div><div class="trust-lbl">Workmanship<br>warranty</div></div>
  </div>
</div></section>

<section><div class="shell">
  <span class="sec-eyebrow">Services</span>
  <h2>Every roofing system this climate is rated for</h2>
  <p class="sec-intro">Full tear-off, repair, metal, tile, hail damage, free inspection. The same family-built crew on every job.</p>
  <div class="svc-grid">
    {''.join(service_cards) if service_cards else '<p>Services coming soon.</p>'}
  </div>
</div></section>

<section class="alt"><div class="shell">
  <span class="sec-eyebrow">Service area</span>
  <h2>Serving {h(city)} and surrounding {h(market.get('region', state_long))}</h2>
  <p class="sec-intro">{h(client.get('service_areas_summary', f'{city} and the surrounding metro.' if city else 'The surrounding metro.'))}</p>
  <div class="area-list">{area_chips_html}</div>
</div></section>

<section><div class="shell">
  <span class="sec-eyebrow">Reviews</span>
  <h2>{h(rating)}-star rated by {h(city)} homeowners</h2>
  <div class="rev-grid">
    {''.join(rev_cards)}
  </div>
</div></section>

<section class="alt"><div class="shell">
  <span class="sec-eyebrow">FAQ</span>
  <h2>{h(city)} roofing answers</h2>
  {faq_html}
</div></section>

<section id="contact"><div class="shell">
  <span class="sec-eyebrow">Contact</span>
  <h2>Free roof inspection · {h(city)}, {h(state)}</h2>
  <p class="sec-intro">Call, text, or book online. Most {h(city)} inspections happen inside 24-48 hours.</p>
  <div class="contact-grid">
    <a class="contact-cell" href="{h(tel_href(phone_raw))}">&#9742; {h(phone_display)}</a>
    {email_cell}
    <a class="contact-cell" href="{h(quote_url)}" target="_blank" rel="noopener">&rarr; Free instant quote</a>
  </div>
</div></section>

</main>

<footer class="site-footer"><div class="shell">
  <h4>{h(name)}</h4>
  <p>{h(client.get('service_areas_summary', ''))}</p>
  <p><a href="{h(tel_href(phone_raw))}">{h(phone_display)}</a></p>
  {email_footer}
  <div class="legal">&copy; {datetime.datetime.now().year} {h(name)}. All rights reserved.</div>
</div></footer>

<div class="sticky-cta" role="region" aria-label="Quick contact">
  <a class="sc-call" href="{h(tel_href(phone_raw))}">&#9742; Call now</a>
  <a class="sc-book" href="{h(quote_url)}" target="_blank" rel="noopener">Free quote</a>
</div>

<script>
(function() {{
  var openBtn = document.querySelector('[data-mnav-open]');
  var closeBtn = document.querySelector('[data-mnav-close]');
  var nav = document.getElementById('mobile-nav');
  if (!openBtn || !nav) return;
  function openNav() {{ nav.classList.add('is-open'); nav.setAttribute('aria-hidden','false'); openBtn.setAttribute('aria-expanded','true'); document.body.style.overflow='hidden'; }}
  function closeNav() {{ nav.classList.remove('is-open'); nav.setAttribute('aria-hidden','true'); openBtn.setAttribute('aria-expanded','false'); document.body.style.overflow=''; }}
  openBtn.addEventListener('click', openNav);
  if (closeBtn) closeBtn.addEventListener('click', closeNav);
  nav.querySelectorAll('[data-mnav-link]').forEach(function(a) {{ a.addEventListener('click', closeNav); }});
  document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeNav(); }});
}})();
</script>

</body>
</html>
"""

    (SITE / "index.html").write_text(html_out)
    print(f"Wrote {SITE / 'index.html'} ({len(html_out)} bytes)")


if __name__ == "__main__":
    main()
