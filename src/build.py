"""Build the site from src/ into two outputs:
  site/     deployable folder for Netlify (shared CSS/JS/images as files, pretty URLs)
  preview/  one self-contained HTML fragment per page for Claude artifact previews
Run: python3 src/build.py
"""
import base64, json, os, shutil, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog"))
from render import build_posts
from blog_posts import POSTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
ASSETS = os.path.join(SRC, "assets")
SITE = os.path.join(ROOT, "site")
PREVIEW = os.path.join(ROOT, "preview")

PAGES = [
    {"slug": "index", "path": "/", "out": "index.html", "name": "Your Functional Health",
     "title": "Functional Medicine & Integrative Psychiatry in Austin, TX | Your Functional Health",
     "desc": "Functional medicine, integrative psychiatry, BHRT and integrative primary care with Xenia Kempf, FNP-C. In person in Austin, TX, and by secure video anywhere in Texas."},
    {"slug": "functional-medicine-austin", "path": "/functional-medicine-austin",
     "out": "functional-medicine-austin.html", "name": "Functional Medicine Page",
     "title": "Functional Medicine in Austin, TX | Your Functional Health",
     "desc": "Root-cause functional medicine for gut, hormone, metabolic and energy problems. Advanced lab testing and a written plan. In person in Austin or by video across Texas."},
    {"slug": "integrative-primary-care", "path": "/integrative-primary-care",
     "out": "integrative-primary-care.html", "name": "Integrative Primary Care Page",
     "title": "Integrative Direct Primary Care in Texas | Your Functional Health",
     "desc": "Integrative direct primary care membership for adults across Texas. Same- or next-day virtual visits, unlimited messaging, urgent care, and labs twice a year, from $129/month."},    {"slug": "functional-integrative-psychiatry-texas", "path": "/functional-integrative-psychiatry-texas",
     "out": "functional-integrative-psychiatry-texas.html", "name": "Integrative Psychiatry Page",
     "title": "Integrative Psychiatry in Austin, TX | Your Functional Health",
     "desc": "Metabolic and integrative psychiatry for anxiety, depression and ADHD in Austin and by video across Texas. Lab-guided, root-cause care with medication only when needed."},    {"slug": "menopause-clinic-texas", "path": "/menopause-clinic-texas",
     "out": "menopause-clinic-texas.html", "name": "BHRT & Hormones Page",
     "title": "Menopause Clinic & BHRT in Austin, TX | Your Functional Health",
     "desc": "Bioidentical hormone therapy for perimenopause and menopause, plus natural hormone balancing. Labs first, FDA-approved hormones, no pellets. In person in Austin or by video across Texas."},    {"slug": "glp1-weight-loss-texas", "path": "/glp1-weight-loss-texas",
     "out": "glp1-weight-loss-texas.html", "name": "GLP-1 Weight Loss Page",
     "title": "GLP-1 Weight Loss in Texas | Semaglutide & Tirzepatide | Your Functional Health",
     "desc": "Virtual GLP-1 weight loss across Texas with semaglutide or tirzepatide from $30/week, paired with nutrition, strength and metabolic care. $45 consult."},    {"slug": "peptide-therapy-austin", "path": "/peptide-therapy-austin",
     "out": "peptide-therapy-austin.html", "name": "Peptide Therapy Page",
     "title": "Peptide Therapy in Austin, TX | Your Functional Health",
     "desc": "Clinician-supervised peptide therapy in Austin and across Texas for recovery, metabolism, sleep, gut health and healthy aging. Labs first, pharmaceutical grade, delivered to your door."},    {"slug": "mold-detox-in-texas", "path": "/mold-detox-in-texas",
     "out": "mold-detox-in-texas.html", "name": "Mold Detox Page",
     "title": "Mold Detox & Mold Illness Treatment in Texas | Your Functional Health",
     "desc": "Mold detox with a mold-literate provider: mycotoxin testing, a four-phase protocol and video visits anywhere in Texas. Clear brain fog, reduce sensitivities and restore energy."},
    {"slug": "functional-medicine-lab-testing", "path": "/functional-medicine-lab-testing",
     "out": "functional-medicine-lab-testing.html", "name": "Lab Testing Page",
     "title": "Functional Medicine Lab Testing | At-Home Kits | Your Functional Health",
     "desc": "At-home functional medicine lab tests: gut, mycotoxins, environmental toxins, organic acids, hormones, food sensitivity, methylation, DNA and immunology. Order with or without a results review."},
    {"slug": "resources", "path": "/resources",
     "out": "resources.html", "name": "Resources Page",
     "title": "Free Functional Medicine Guides & Resources | Your Functional Health",
     "desc": "Free printable guides on gut health, anti-inflammatory nutrition, sleep, stress and toxin-free living, safer personal care product lists, and thyroid and mold illness quizzes."},
    {"slug": "store", "path": "/store",
     "out": "store.html", "name": "Store Page",
     "title": "Store | Supplements, Mira Hormone Tracking & Wellness Picks | Your Functional Health",
     "desc": "Professional-grade supplements through Fullscript, Mira at-home hormone tracking with a discount code, and the everyday wellness products Xenia recommends."},
    {"slug": "clinicians", "path": "/clinicians", "out": "clinicians.html", "name": "Clinicians Page",
     "title": "BHRT Course & Clinical Reference App for Clinicians | Your Functional Health",
     "desc": "BHRT Navigator by Xenia Kempf, FNP-C: a point-of-care hormone therapy reference app and 184-page course for primary care, NP and PA prescribers."},
    {"slug": "pp", "path": "/pp", "out": "pp.html", "name": "Privacy Policy",
     "title": "Privacy Policy | Your Functional Health",
     "desc": "How the Your Functional Health website collects, uses and protects your information."},
    {"slug": "terms-of-use", "path": "/terms-of-use", "out": "terms-of-use.html", "name": "Terms of Use",
     "title": "Terms of Use | Your Functional Health",
     "desc": "Terms of use for the Your Functional Health website, yourfunctionalmednp.com."},
    {"slug": "404", "path": "/404", "out": "404.html", "name": "Page Not Found",
     "title": "Page not found | Your Functional Health", "noindex": True,
     "desc": "This page has moved or no longer exists."},
    {"slug": "functional-medicine-blog", "path": "/functional-medicine-blog",
     "out": "functional-medicine-blog.html", "name": "Blog Page",
     "title": "Functional Medicine Blog | Hormones, Gut, Mental Health & More | Your Functional Health",
     "desc": "Articles from Xenia Kempf, FNP-C on hormones and BHRT, gut health, integrative psychiatry, mold toxicity, peptides, GLP-1s and root-cause care in Austin and across Texas."},
]

# Old Wix addresses -> where that content lives now (permanent 301s; works on any domain).
OLD_TO_NEW = [
    # Wix's sitemap files (search engines have these on record)
    ("/blog-posts-sitemap.xml", "/sitemap.xml"), ("/blog-categories-sitemap.xml", "/sitemap.xml"),
    ("/pricing-plans-sitemap.xml", "/sitemap.xml"), ("/pages-sitemap.xml", "/sitemap.xml"),
    # services hub, booking and pricing pages
    ("/services-functional-medicine", "/#services"), ("/fees", "/#services"), ("/book-today", "/#services"),
    ("/pricing-plans/*", "/#services"), ("/plan-customization", "/#services"), ("/wellness-coaching", "/#services"),
    # about, faq, contact
    ("/about-functional-medicine", "/#about"), ("/about", "/#about"), ("/profile/*", "/#about"),
    ("/faq", "/#faq"), ("/contact-us", "/#contact"), ("/get-started", "/#contact"),
    # services that moved or merged
    ("/direct-primary-care-austin", "/integrative-primary-care"), ("/direct-primary-care-midland", "/integrative-primary-care"),
    ("/functional-psychiatry", "/functional-integrative-psychiatry-texas"),
    ("/hormone-balancing-in-functional-medicine", "/menopause-clinic-texas"),
    ("/bioidentical-hormone-replacement-texas", "/menopause-clinic-texas"),
    ("/weight-loss-with-peptides", "/glp1-weight-loss-texas"),
    ("/peptide-therapy", "/peptide-therapy-austin"),
    ("/mold-detoxification-in-texas", "/mold-detox-in-texas"), ("/general-4", "/mold-detox-in-texas"),
    ("/gut-health", "/functional-medicine-austin#gut"), ("/metabolic-health", "/functional-medicine-austin#metabolic"),
    ("/energy-regulation-through-functional-medicine", "/functional-medicine-austin#energy"),
    # individual lab test pages -> sections of the Functional Labs page
    ("/functional-medicine-packages", "/functional-medicine-lab-testing"),
    ("/gut-health-testing-gut-zoomer", "/functional-medicine-lab-testing#gut"),
    ("/mycotoxin-testing-mold-illness", "/functional-medicine-lab-testing#mycotoxin"),
    ("/environmental-toxin-testing", "/functional-medicine-lab-testing#toxins"),
    ("/organic-acid-testing-texas", "/functional-medicine-lab-testing#oat"),
    ("/hormone-testing-functional-medicine", "/functional-medicine-lab-testing#hormones"),
    ("/food-sensitivity-testing-at-home", "/functional-medicine-lab-testing#food"),
    ("/methylation-genomics-testing", "/functional-medicine-lab-testing#methylation"),
    ("/genetic-snp-testing", "/functional-medicine-lab-testing#snp"),
    ("/immunology-panel-texas", "/functional-medicine-lab-testing#immunology"),
    # quizzes and guides -> Resources
    ("/thyroid-health-quiz", "/resources#thyroid-quiz"), ("/mold-illness-quiz", "/resources#mold-quiz"),
    ("/wellness-tips-and-guides", "/resources#wellness"), ("/nutrition-tips-and-guides", "/resources#nutrition"),
    ("/toxin-free-resources", "/resources#products"), ("/about-1", "/resources"),
    ("/recipes", "/resources"), ("/challenges", "/resources"),
    # old blog category pages -> blog filtered to the matching topic
    *[(f"/functional-medicine-blog/categories/{c}", f"/functional-medicine-blog#topic-{t}") for c, t in [
        ("gut-health", "gut-immune"), ("immune-health", "gut-immune"), ("mcas", "gut-immune"),
        ("hormone-replacement", "hormones"), ("menopause", "hormones"), ("bhrt", "hormones"), ("hormone-health", "hormones"),
        ("mental-health", "mental-health"), ("functional-psychiatry", "mental-health"), ("integrative-psychiatry", "mental-health"),
        ("mold-toxicity", "mold-detox"),
        ("peptides", "peptides-longevity"), ("longevity", "peptides-longevity"), ("anti-aging", "peptides-longevity"),
        ("snp-testing", "peptides-longevity"), ("genetics", "peptides-longevity"),
        ("weight-loss", "weight-metabolism"), ("diabetes", "weight-metabolism"),
        ("austin-functional-medicine", "functional-medicine"), ("direct-primary-care", "functional-medicine"),
        ("skin-hair", "functional-medicine"), ("skin-health", "functional-medicine"), ("pans-pandas", "functional-medicine")]],
    ("/functional-medicine-blog/*", "/functional-medicine-blog"), ("/blog", "/functional-medicine-blog"),
    ("/post", "/functional-medicine-blog"),
]
# Old Wix PDF addresses (/_files/ugd/01b06b_<id>.pdf) -> the same file in /downloads
_wix = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "downloads", "wix-files.json")
if os.path.exists(_wix):
    OLD_TO_NEW += [(f"/_files/ugd/01b06b_{k}.pdf", v) for k, v in sorted(json.load(open(_wix)).items())]

REDIRECTS = ("# Old Wix addresses -> new pages\n"
             + "".join(f"{a:<62} {b:<52} 301\n" for a, b in OLD_TO_NEW)
             + "\n# Test site only: anything not built yet falls through to the current site.\n"
               "# This rule only applies on the netlify.app address, never on yourfunctionalmednp.com.\n"
               "https://yourfunctionalmednp.netlify.app/*  https://www.yourfunctionalmednp.com/:splat  302\n")

IMAGES = {"{{LOGO}}": ("logo.png", "image/png"), "{{LOGO_LIGHT}}": ("logo-light.png", "image/png"),
          "{{XENIA}}": ("xenia.jpg", "image/jpeg"), "{{HG}}": ("healthgrades.png", "image/png"),
          "{{FS_LOGO}}": ("fullscript-logo.png", "image/png")}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400'
         '&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">\n')


def read(*p):
    with open(os.path.join(SRC, *p), encoding="utf-8") as f:
        return f.read()


def fill_images(html, inline):
    for key, (fname, mime) in IMAGES.items():
        if inline:
            with open(os.path.join(ASSETS, fname), "rb") as f:
                val = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
        else:
            val = "/images/" + fname
        html = html.replace(key, val)
    return html


# Search-engine ownership tags carried over from the Wix site (Google, Pinterest, Bing, Yandex). Home page only.
VERIFY = ('<meta name="google-site-verification" content="zsnpuefPDw2QS2wUzFH67LZiZw0TM5LHiUMeHxZt4IM">\n'
          '<meta name="google-site-verification" content="LUKz2flSeiWMTerEvatBwjprpFbjcmmUHVW4cN_Cyq4">\n'
          '<meta name="p:domain_verify" content="05b5f6126281e3dd69f3eab43902cb96">\n'
          '<meta name="msvalidate.01" content="4B9A14AA7A7A35629E21825BBD708E29">\n'
          '<meta name="yandex-verification" content="c5550fdd30045b26">\n')
SITE_URL = "https://www.yourfunctionalmednp.com"


def build():
    css, js = read("partials", "style.css"), read("partials", "script.js")
    header, footer = read("partials", "header.html"), read("partials", "footer.html")
    built = json.dumps([p["path"] for p in PAGES])

    for d in (SITE, PREVIEW):
        shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(SITE, "images"))
    os.makedirs(os.path.join(SITE, "assets"))
    os.makedirs(PREVIEW)
    # Until launch: any path without a file here goes to the same path on the current (Wix) site.
    # Netlify serves real files first, so finished pages are never redirected.
    with open(os.path.join(SITE, "_redirects"), "w", encoding="utf-8") as f:
        f.write(REDIRECTS)
    for fname, _ in IMAGES.values():
        shutil.copy(os.path.join(ASSETS, fname), os.path.join(SITE, "images", fname))
    # Xenia's own photos, referenced from page configs as "/images/<name>"
    photo_dir = os.path.join(ASSETS, "photos")
    own_photos = sorted(os.listdir(photo_dir)) if os.path.isdir(photo_dir) else []
    for fname in own_photos:
        shutil.copy(os.path.join(photo_dir, fname), os.path.join(SITE, "images", fname))
    with open(os.path.join(SITE, "assets", "site.css"), "w", encoding="utf-8") as f:
        f.write(css)
    with open(os.path.join(SITE, "assets", "site.js"), "w", encoding="utf-8") as f:
        f.write(js)

    for p in PAGES:
        body = read("pages", p["slug"] + ".html")
        page_js = read("pages", p["slug"] + ".js") if os.path.exists(os.path.join(SRC, "pages", p["slug"] + ".js")) else ""
        config = f"<script>\n{page_js}</script>\n" if page_js else ""
        preview_cfg = config
        for fname in own_photos:  # previews can't load site files, so embed her photos
            ref = f'"/images/{fname}"'
            if ref in preview_cfg:
                with open(os.path.join(photo_dir, fname), "rb") as f:
                    mime = "image/png" if fname.lower().endswith(".png") else "image/jpeg"
                    preview_cfg = preview_cfg.replace(ref, '"data:' + mime + ';base64,' + base64.b64encode(f.read()).decode() + '"')
        content = f'{header}\n<main id="top">\n{body}\n</main>\n\n{footer}\n'

        # deployable page
        canonical = "https://www.yourfunctionalmednp.com" + ("" if p["path"] == "/" else p["path"])
        doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
               "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
               f"<title>{p['title']}</title>\n<meta name=\"description\" content=\"{p['desc']}\">\n"
               + ("<meta name=\"robots\" content=\"noindex\">\n" if p.get("noindex") else f"<link rel=\"canonical\" href=\"{canonical}\">\n")
               + (VERIFY if p["path"] == "/" else "")
               + "<link rel=\"icon\" type=\"image/png\" href=\"/images/logo.png\">\n"
               f"{FONTS}<link rel=\"stylesheet\" href=\"/assets/site.css\">\n</head>\n<body>\n"
               f"{fill_images(content, False)}{config}<script src=\"/assets/site.js\"></script>\n</body>\n</html>\n")
        out = os.path.join(SITE, p["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(doc)

        # self-contained preview fragment
        frag = (f"<title>{p['name']}</title>\n<meta name=\"description\" content=\"{p['desc']}\">\n{FONTS}"
                f"<style>\n{css}</style>\n\n{fill_images(content, True)}{preview_cfg}<script>\n{js}</script>\n")
        with open(os.path.join(PREVIEW, p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(frag)
        print("built", p["path"])

    # downloadable PDFs (guides, product lists) -> /downloads/...
    dl = os.path.join(ASSETS, "downloads")
    if os.path.isdir(dl):
        shutil.copytree(dl, os.path.join(SITE, "downloads"), ignore=shutil.ignore_patterns("*.json"))

    # blog posts: /post/<slug>, same URLs as on Wix
    blog_img_dir = os.path.join(ASSETS, "blog")
    if os.path.isdir(blog_img_dir):
        shutil.copytree(blog_img_dir, os.path.join(SITE, "images", "blog"), dirs_exist_ok=True)
    posts = build_posts()
    os.makedirs(os.path.join(PREVIEW, "post"), exist_ok=True)
    for p in posts:
        content = f'{header}\n<main id="top">\n{p["html"]}\n</main>\n\n{footer}\n'
        canonical = "https://www.yourfunctionalmednp.com" + p["path"]
        esc = lambda v: v.replace("&", "&amp;").replace('"', "&quot;")
        doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
               "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
               f"<title>{esc(p['title'])}</title>\n<meta name=\"description\" content=\"{esc(p['desc'])}\">\n"
               f"<link rel=\"canonical\" href=\"{canonical}\">\n"
               "<meta property=\"og:type\" content=\"article\">\n"
               f"<meta property=\"og:title\" content=\"{esc(p['name'])}\">\n"
               f"<meta property=\"og:description\" content=\"{esc(p['desc'])}\">\n"
               f"<meta property=\"og:url\" content=\"{canonical}\">\n"
               f"<meta property=\"og:image\" content=\"{esc(p['og_image'])}\">\n"
               "<link rel=\"icon\" type=\"image/png\" href=\"/images/logo.png\">\n"
               f"{FONTS}<link rel=\"stylesheet\" href=\"/assets/site.css\">\n"
               f"<script type=\"application/ld+json\">{p['jsonld']}</script>\n</head>\n<body>\n"
               f"{fill_images(content, False)}<script>window.PAGE={{photos:{{}}}};</script>\n"
               "<script src=\"/assets/site.js\"></script>\n</body>\n</html>\n")
        out = os.path.join(SITE, p["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(doc)
        frag = (f"<title>{p['name']}</title>\n{FONTS}<style>\n{css}</style>\n\n{fill_images(content, True)}"
                f"<script>window.PAGE={{photos:{{}}}};</script>\n<script>\n{js}</script>\n")
        with open(os.path.join(PREVIEW, "post", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(frag)
    print("built", len(posts), "blog posts")

    # sitemap.xml + robots.txt
    dates = {q[0]: q[2][:10] for q in POSTS}
    urls = [(SITE_URL + ("/" if p["path"] == "/" else p["path"]), None) for p in PAGES if not p.get("noindex")]
    urls += [(SITE_URL + p["path"], dates.get(p["slug"])) for p in posts]
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u, d in urls:
            f.write(f"  <url><loc>{u}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("sitemap:", len(urls), "URLs")


if __name__ == "__main__":
    build()
