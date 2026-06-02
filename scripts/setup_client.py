#!/usr/bin/env python3
"""setup_client.py — validate + normalize a ROM site template for a new client.

This script no longer does shallow find/replace on the legacy Austin Area Roofers
strings. After the build.py refactor, every vertical-specific and city-specific
value is derived from data/client.json, data/services.json, and data/areas.json.
The only job of setup_client.py now is:

    1. Validate data/client.json has the keys build.py needs. Fail loud if not.
    2. Coerce + normalize a few fields (years_in_business, phone, primary_city)
       so build.py never has to deal with "36+" vs 36 ambiguity.
    3. Rewrite .github/workflows/deploy.yml to use the client's
       cloudflare_project_name.
    4. Rewrite .github/workflows/configure.yml to grant workflows: write so the
       configure job can update workflow files in place.
    5. Write the IndexNow keyfile.
    6. Print a clear next-steps list.

USAGE
    python3 scripts/setup_client.py

OUT OF SCOPE
    - Photos. Drop them in site/assets/img/photos/.
    - Service catalog + area pages. Fill data/services.json and data/areas.json
      with the client's actual catalog (or paste the Claude-extracted JSON over
      the existing structure).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"
WORKFLOWS = ROOT / ".github" / "workflows"
DEPLOY_YML = WORKFLOWS / "deploy.yml"
CONFIGURE_YML = WORKFLOWS / "configure.yml"
CLIENT_JSON = DATA / "client.json"


# --------------------------------------------------------------------
# Required schema for data/client.json. Every key listed here must be
# present and non-empty for build.py to render the site without crashing.
# Format: list of dot-paths.
# --------------------------------------------------------------------
REQUIRED_FIELDS = [
    "brand.name",
    "brand.vertical",
    "brand.vertical_label_singular",
    "brand.vertical_label_plural",
    "site.url",
    "site.domain_apex",
    "site.cloudflare_project_name",
    "market.primary_city",
    "market.state_long",
    "market.state_abbr",
]


class ValidationError(Exception):
    pass


def get_path(d: dict, dotted: str):
    """Walk a dict by dotted key path. Returns None if any segment is missing."""
    cur = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def validate_client(raw: dict) -> list:
    """Check every required field is present and non-empty. Returns list of missing paths."""
    missing = []
    for path in REQUIRED_FIELDS:
        val = get_path(raw, path)
        if val is None or (isinstance(val, str) and not val.strip()):
            missing.append(path)
    return missing


# --------------------------------------------------------------------
# Coercion helpers. build.py wants math on years_in_business, so we parse
# any reasonable form ("27", 27, "36+", "20 years") into an integer and
# store it alongside the raw display string.
# --------------------------------------------------------------------
_YEARS_INT_RE = re.compile(r"\d+")


def coerce_years_int(val) -> int:
    """Extract the leading integer from any years_in_business representation."""
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    if isinstance(val, str):
        m = _YEARS_INT_RE.search(val)
        if m:
            return int(m.group(0))
    return 0


# E.164: leading + then country code + subscriber number, digits only.
def normalize_phone_e164(phone: str, default_country: str = "1") -> str:
    """Return phone in E.164 form. Strips spaces, dots, parens, dashes."""
    if not phone:
        return ""
    if phone.startswith("+"):
        digits = re.sub(r"\D", "", phone)
        return "+" + digits
    digits = re.sub(r"\D", "", phone)
    if not digits:
        return ""
    # US/CA default. Eleven digits starting with 1 already includes country code.
    if len(digits) == 10:
        return "+" + default_country + digits
    if len(digits) == 11 and digits.startswith(default_country):
        return "+" + digits
    return "+" + digits


def title_case_city(name: str) -> str:
    """Title-case a city name without breaking common connectors."""
    if not name:
        return ""
    small = {"of", "the", "and", "de", "del", "la", "le"}
    parts = name.strip().split()
    out = []
    for i, p in enumerate(parts):
        lower = p.lower()
        if i > 0 and lower in small:
            out.append(lower)
        else:
            out.append(p[:1].upper() + p[1:].lower() if p else p)
    return " ".join(out)


def normalize_client(raw: dict) -> dict:
    """Mutate the loaded client dict in place with coerced + normalized values."""
    stats = raw.setdefault("stats", {})
    raw_years = stats.get("years_in_business", 0)
    stats["_years_int"] = coerce_years_int(raw_years)
    # Preserve the original string for display ("36+" stays "36+").
    if not isinstance(raw_years, (str, int)):
        stats["years_in_business"] = str(raw_years)

    contact = raw.setdefault("contact", {})
    phone = contact.get("phone", "")
    if phone:
        contact["phone_e164"] = normalize_phone_e164(phone)

    market = raw.setdefault("market", {})
    if market.get("primary_city"):
        market["primary_city"] = title_case_city(market["primary_city"])

    return raw


# --------------------------------------------------------------------
# Workflow file rewrites. These are surgical regex replacements against
# known keys, not blanket find/replace on city/brand strings.
# --------------------------------------------------------------------
def update_deploy_yml(cf_project: str) -> bool:
    """Replace --project-name=<old> with the client's cloudflare_project_name."""
    if not DEPLOY_YML.exists():
        return False
    text = DEPLOY_YML.read_text()
    updated = re.sub(
        r"--project-name=[A-Za-z0-9_\-]+",
        f"--project-name={cf_project}",
        text,
    )
    if updated != text:
        DEPLOY_YML.write_text(updated)
        return True
    return False


def update_configure_yml() -> bool:
    """Ensure permissions block includes workflows: write so configure can edit workflow files."""
    if not CONFIGURE_YML.exists():
        return False
    text = CONFIGURE_YML.read_text()
    if re.search(r"^\s*workflows:\s*write", text, re.MULTILINE):
        return False
    # Inject workflows: write into the existing top-level permissions block.
    updated, n = re.subn(
        r"(^permissions:\s*\n(?:[ \t]+[A-Za-z_\-]+:[ \t]*[A-Za-z]+\s*\n)*)",
        lambda m: m.group(1) + "  workflows: write\n",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n == 0:
        # No permissions block found. Add one after the `on:` block.
        updated = re.sub(
            r"(^on:\s*\n(?:[ \t]+.*\n)*)",
            lambda m: m.group(1) + "\npermissions:\n  contents: write\n  workflows: write\n",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    if updated != text:
        CONFIGURE_YML.write_text(updated)
        return True
    return False


def write_indexnow_keyfile(key: str) -> bool:
    """IndexNow protocol: key must be served at /<KEY>.txt with the key as body."""
    if not key:
        return False
    SITE.mkdir(parents=True, exist_ok=True)
    for stale in SITE.glob("*.txt"):
        if re.match(r"^[a-f0-9]{32,64}\.txt$", stale.name) and stale.name != f"{key}.txt":
            stale.unlink()
    (SITE / f"{key}.txt").write_text(key)
    (SITE / ".indexnow-key.txt").write_text(key)
    return True


def main() -> int:
    print("ROM site template — setup_client.py")
    print()

    if not CLIENT_JSON.exists():
        print(f"  ERROR: {CLIENT_JSON} not found. Cannot continue.", file=sys.stderr)
        return 1

    try:
        raw = json.loads(CLIENT_JSON.read_text())
    except json.JSONDecodeError as e:
        print(f"  ERROR: data/client.json is not valid JSON: {e}", file=sys.stderr)
        return 1

    # 1. Validate.
    missing = validate_client(raw)
    if missing:
        print("  ERROR: data/client.json is missing required fields:", file=sys.stderr)
        for path in missing:
            print(f"    - {path}", file=sys.stderr)
        print(file=sys.stderr)
        print("  Fix data/client.json then re-run.", file=sys.stderr)
        return 1

    # 2. Coerce + normalize.
    raw = normalize_client(raw)
    CLIENT_JSON.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n")

    brand_name = raw["brand"]["name"]
    cf_project = raw["site"]["cloudflare_project_name"]
    primary_city = raw["market"]["primary_city"]
    years_int = raw["stats"]["_years_int"]
    phone_e164 = raw.get("contact", {}).get("phone_e164", "")
    indexnow_key = (raw.get("tracking", {}) or {}).get("indexnow_key", "")

    print(f"  Brand:          {brand_name}")
    print(f"  Primary city:   {primary_city}")
    print(f"  CF project:     {cf_project}")
    print(f"  Years (int):    {years_int}")
    if phone_e164:
        print(f"  Phone (E.164):  {phone_e164}")
    print()

    # 3. Rewrite workflow files.
    deploy_changed = update_deploy_yml(cf_project)
    configure_changed = update_configure_yml()

    if deploy_changed:
        print("  rewrote   .github/workflows/deploy.yml (CLOUDFLARE_PROJECT_NAME)")
    else:
        print("  no change .github/workflows/deploy.yml")

    if configure_changed:
        print("  rewrote   .github/workflows/configure.yml (added workflows: write)")
    else:
        print("  no change .github/workflows/configure.yml")

    # 4. IndexNow keyfile.
    if indexnow_key:
        write_indexnow_keyfile(indexnow_key)
        print(f"  wrote     site/{indexnow_key}.txt + site/.indexnow-key.txt")
    else:
        print("  skipped   IndexNow keyfile (tracking.indexnow_key not set)")

    print()
    print("  data files validated ✓")
    print("  workflow files updated ✓")
    print()
    print("Next:")
    print("  1. Fill data/services.json + data/areas.json with the client's actual catalog.")
    print("  2. Drop client photos in site/assets/img/photos/.")
    print("  3. git add -A && git commit -m 'Configure client' && git push origin main.")
    print("  4. Cloudflare Pages will auto-deploy via .github/workflows/deploy.yml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
