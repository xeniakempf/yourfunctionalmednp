"""Structured data (schema.org JSON-LD) for every page.

Search engines and AI assistants read this to learn who the practice is, where it serves, what each
service costs and who the clinician is. Edit the facts here (cities, services, prices, profiles);
the build adds the right pieces to each page. FAQ answers are read straight from each page's
<details> blocks, so they always match what visitors see.
"""
import html as _html
import json
import re

SITE_URL = "https://www.yourfunctionalmednp.com"
ORG = SITE_URL + "/#organization"
XENIA = SITE_URL + "/#xenia"
WEBSITE = SITE_URL + "/#website"

# Where patients can be seen (all services are available by video anywhere in Texas).
CITIES = [
    # greater Austin
    "Austin", "Round Rock", "Cedar Park", "Georgetown", "Pflugerville", "Leander", "Kyle", "Buda",
    "Dripping Springs", "San Marcos",
    # other metros
    "San Antonio", "Houston", "Dallas", "Fort Worth",
    # Permian Basin
    "Midland", "Odessa", "Big Spring", "Andrews", "Monahans", "Pecos", "Fort Stockton",
    # Southeast Texas
    "Beaumont", "Port Arthur", "Orange", "Nederland", "Port Neches", "Vidor", "Lumberton", "Jasper",
    # West Texas and the Panhandle
    "Lubbock", "Amarillo", "San Angelo", "Abilene", "El Paso",
    # East Texas
    "Tyler", "Longview", "Nacogdoches", "Lufkin",
    # Central Texas
    "Waco", "Temple", "Killeen", "Bryan", "College Station",
    # Coastal Bend and South Texas
    "Corpus Christi", "Victoria", "Rockport", "Laredo", "McAllen", "Harlingen", "Brownsville",
]
TEXAS = {"@type": "State", "name": "Texas", "sameAs": "https://en.wikipedia.org/wiki/Texas"}
AREA = [TEXAS] + [{"@type": "City", "name": c, "containedInPlace": {"@type": "State", "name": "Texas"}}
                  for c in CITIES]

PROFILES_ORG = [
    "https://www.instagram.com/your.fx.health",
    "https://www.facebook.com/your.fx.health/",
    "https://x.com/Your_FX_Health",
    "https://www.tiktok.com/@yourfunctionalhealth",
]
PROFILES_XENIA = [
    "https://www.linkedin.com/in/xeniakempf/",
    "https://www.healthgrades.com/providers/xenia-kempf-1qflxy1562",
]


def usd(name, price, desc=None):
    o = {"@type": "Offer", "name": name, "price": str(price), "priceCurrency": "USD"}
    if desc:
        o["description"] = desc
    return o


def usd_range(name, lo, hi, unit):
    return {"@type": "Offer", "name": name, "priceCurrency": "USD",
            "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": lo, "maxPrice": hi,
                                   "priceCurrency": "USD", "unitText": unit}}


# One entry per service page: page path -> service facts. Prices must match the page.
SERVICES = {
    "/functional-medicine-austin": {
        "name": "Functional Medicine", "serviceType": "Functional medicine",
        "description": "Root-cause functional medicine care for gut health, hormones, thyroid, metabolic health, "
                       "fatigue and autoimmunity, with advanced lab testing and a personalized plan.",
        "offers": [usd("New patient visit (60–75 min)", 500), usd("Follow-up visit (45–60 min)", 325),
                   usd("Brief follow-up (20–30 min)", 150)],
    },
    "/integrative-primary-care": {
        "name": "Integrative Direct Primary Care", "serviceType": "Direct primary care membership",
        "description": "Membership primary care for adults in Texas: virtual primary and urgent care visits, "
                       "unlimited messaging and extensive lab testing twice a year.",
        "offers": [usd("12-month membership (per month, billed annually at $1,908)", 159),
                   usd("6-month membership (per month, billed every 6 months at $1,074)", 179)],
    },
    "/functional-integrative-psychiatry-texas": {
        "name": "Integrative Psychiatry", "serviceType": "Metabolic and integrative psychiatry",
        "description": "Integrative and metabolic psychiatry for anxiety, depression and ADHD, combining medication "
                       "management with nutrition, lab testing and lifestyle care.",
        "offers": [usd("Initial evaluation (60–75 min)", 325), usd("Extended follow-up (50 min)", 175),
                   usd("Brief follow-up (25 min)", 100)],
    },
    "/menopause-clinic-texas": {
        "name": "Menopause Care and Bioidentical Hormone Replacement Therapy (BHRT)",
        "serviceType": "Bioidentical hormone replacement therapy",
        "description": "Menopause and perimenopause care with FDA-approved bioidentical hormones (no pellets), "
                       "lab testing before any prescription and regular monitoring.",
        "offers": [usd("New patient visit (30–45 min)", 250), usd("Follow-up visit (15–20 min)", 175)],
    },
    "/glp1-weight-loss-texas": {
        "name": "GLP-1 Weight Loss Program", "serviceType": "Medical weight loss",
        "description": "Semaglutide or tirzepatide at the lowest effective dose, with nutrition guidance and "
                       "metabolic care, by video anywhere in Texas.",
        "offers": [usd("GLP-1 consult (15 min)", 45),
                   usd_range("Semaglutide (dose dependent)", 30, 36, "week"),
                   usd_range("Tirzepatide (dose dependent)", 47, 57, "week")],
    },
    "/peptide-therapy-austin": {
        "name": "Peptide Therapy", "serviceType": "Peptide therapy",
        "description": "Clinician-supervised peptide therapy in Austin and by video across Texas.",
    },
    "/mold-detox-in-texas": {
        "name": "Mold Detox and Mold Illness Treatment", "serviceType": "Mold illness (biotoxin) treatment",
        "description": "Testing and phased treatment for mold illness and mycotoxin exposure, including binders, "
                       "gut and nutrient support and practical remediation guidance.",
        "offers": [usd("Mold detox consult (60–75 min)", 500), usd("Follow-up visit (45–60 min)", 325),
                   usd("Brief follow-up (20–30 min)", 150), usd("Mycotoxin test with interpretation", 495),
                   usd("Mycotoxin test only", 395)],
    },
    "/functional-medicine-lab-testing": {
        "name": "Functional Medicine Lab Testing", "serviceType": "Functional lab testing",
        "description": "At-home functional lab tests: gut, mycotoxins, environmental toxins, organic acids, "
                       "hormones, food sensitivities, methylation and genetics.",
    },
}


def organization():
    return {
        "@type": ["MedicalClinic", "MedicalBusiness"],
        "@id": ORG,
        "name": "Your Functional Health",
        "legalName": "Healthify LLC",
        "url": SITE_URL + "/",
        "logo": {"@type": "ImageObject", "url": SITE_URL + "/images/logo.png"},
        "image": SITE_URL + "/images/xenia.jpg",
        "description": ("Your Functional Health is a functional medicine practice in Austin, Texas, led by "
                        "Xenia Kempf, FNP-C. It offers functional medicine, integrative psychiatry, integrative "
                        "direct primary care, menopause care and BHRT, GLP-1 weight loss, peptide therapy and mold "
                        "detox, in person in Austin and by secure video anywhere in Texas."),
        "telephone": "+1-737-336-5959",
        "priceRange": "$45–$500",
        "currenciesAccepted": "USD",
        "paymentAccepted": "Credit card, HSA, FSA",
        "isAcceptingNewPatients": True,
        "address": {"@type": "PostalAddress", "streetAddress": "3807 E 51st St", "addressLocality": "Austin",
                    "addressRegion": "TX", "postalCode": "78723", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 30.2976, "longitude": -97.6858},
        "location": {
            "@type": "Place", "name": "In-person visits (inside Therapy Space)",
            "address": {"@type": "PostalAddress", "streetAddress": "6850 Austin Center Blvd, Bldg 2, Ste 320",
                        "addressLocality": "Austin", "addressRegion": "TX", "postalCode": "78731",
                        "addressCountry": "US"},
            "geo": {"@type": "GeoCoordinates", "latitude": 30.3517, "longitude": -97.7528},
        },
        "areaServed": AREA,
        "medicalSpecialty": ["https://schema.org/PrimaryCare", "https://schema.org/Psychiatric",
                             "https://schema.org/Endocrine", "https://schema.org/Gastroenterologic"],
        "knowsAbout": ["Functional medicine", "Integrative medicine", "Bioidentical hormone replacement therapy",
                       "Menopause", "Perimenopause", "Gut health", "SIBO", "Thyroid health", "Hashimoto's",
                       "Mold illness", "Mycotoxins", "Metabolic psychiatry", "GLP-1 medications",
                       "Peptide therapy", "Direct primary care"],
        "availableService": [{"@id": SITE_URL + path + "#service"} for path in SERVICES],
        "founder": {"@id": XENIA},
        "employee": {"@id": XENIA},
        "sameAs": PROFILES_ORG,
    }


def person():
    return {
        "@type": "Person",
        "@id": XENIA,
        "name": "Xenia Kempf",
        "honorificSuffix": "MSN, APRN, FNP-C",
        "jobTitle": "Family Nurse Practitioner",
        "description": "Board-certified family nurse practitioner practicing functional medicine, integrative "
                       "psychiatry and hormone care in Austin, Texas, and by video across Texas.",
        "image": SITE_URL + "/images/xenia.jpg",
        "url": SITE_URL + "/#about",
        "worksFor": {"@id": ORG},
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "FNP-C (Family Nurse Practitioner, Certified)",
             "credentialCategory": "certification"},
            {"@type": "EducationalOccupationalCredential", "name": "Master of Science in Nursing (MSN)",
             "credentialCategory": "degree"},
        ],
        "knowsAbout": ["Functional medicine", "Bioidentical hormone replacement therapy", "Menopause",
                       "Integrative psychiatry", "Gut health", "Mold illness", "GLP-1 weight loss"],
        "sameAs": PROFILES_XENIA,
    }


def website():
    return {"@type": "WebSite", "@id": WEBSITE, "url": SITE_URL + "/", "name": "Your Functional Health",
            "publisher": {"@id": ORG}, "inLanguage": "en-US"}


def faqs(page_html):
    """FAQPage from the page's visible <details><summary>Q</summary>A</details> blocks."""
    out = []
    for q, a in re.findall(r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>", page_html, re.S):
        q = _html.unescape(re.sub(r"<[^>]+>", "", q)).strip()
        a = _html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a))).strip()
        if q and a:
            out.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return out


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}


def page_graph(path, title, desc, page_html, name):
    """JSON-LD for a regular page."""
    url = SITE_URL + ("/" if path == "/" else path)
    graph = [organization(), person(), website()] if path == "/" else []
    svc = SERVICES.get(path)
    wp = {"@type": "MedicalWebPage" if svc else "WebPage", "@id": url + "#webpage", "url": url, "name": title,
          "description": desc, "isPartOf": {"@id": WEBSITE}, "about": {"@id": ORG}, "inLanguage": "en-US"}
    if svc:
        wp["about"] = {"@id": url + "#service"}
        wp["reviewedBy"] = {"@id": XENIA}
        s = {"@type": "Service", "@id": url + "#service", "url": url, "name": svc["name"],
             "serviceType": svc["serviceType"], "description": svc["description"],
             "provider": {"@id": ORG}, "areaServed": AREA,
             "availableChannel": {"@type": "ServiceChannel", "name": "In person in Austin or by secure video anywhere in Texas",
                                  "serviceUrl": url}}
        if svc.get("offers"):
            s["offers"] = svc["offers"]
        graph.append(s)
    if path != "/":
        wp["breadcrumb"] = crumbs([("Home", "/"), (re.sub(r"\s+Page$", "", name), path)])
        # every page refers to the practice; give non-home pages the core nodes too, so each page stands alone
        graph = [organization(), person(), website()] + graph
    graph.append(wp)
    q = faqs(page_html)
    if q:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": q})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def post_graph(post_jsonld, path, title, topic):
    """Wraps a blog post's BlogPosting with links to the practice, the author and a breadcrumb."""
    bp = json.loads(post_jsonld)
    bp.pop("@context", None)
    url = SITE_URL + path
    bp["@id"] = url + "#article"
    bp["author"] = {"@id": XENIA}
    bp["publisher"] = {"@id": ORG}
    bp["isPartOf"] = {"@id": WEBSITE}
    bp["inLanguage"] = "en-US"
    bc = crumbs([("Home", "/"), ("Blog", "/functional-medicine-blog"), (title, path)])
    return json.dumps({"@context": "https://schema.org",
                       "@graph": [organization(), person(), website(), bp, bc]}, ensure_ascii=False)
