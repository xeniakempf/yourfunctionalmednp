"""Render the 64 blog posts (src/blog/posts/<slug>.md) to /post/<slug>/index.html.

Markdown here is the text exported from the Wix blog, so the converter is small and
tailored to it: headings, paragraphs, bullet lists (incl. flattened nested lists),
pipe tables, images and links. Images: if a local copy exists in
src/assets/blog/<media id>, it is used; otherwise the Wix media URL is used.
"""
import os, re, json, math
from html import escape
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
LOCAL_IMG_DIR = os.path.join(SRC, "assets", "blog")
SITE_URL = "https://www.yourfunctionalmednp.com"

import sys
sys.path.insert(0, HERE)
from blog_posts import POSTS
from services import SERVICES, POST_SERVICES
CURRENT = {"primary": None}  # primary service of the post being rendered  # (slug, title, date, cover media id, topic), newest first

TOPIC_COLOR = {"Hormones": "#985A60", "Mental health": "#5B5785", "Gut & immune": "#155863", "Mold & detox": "#80683A",
               "Peptides & longevity": "#3D6382", "Weight & metabolism": "#58744F", "Functional medicine": "#2F7178"}
TOPIC_PAGE = {"Hormones": "/menopause-clinic-texas", "Mental health": "/functional-integrative-psychiatry-texas",
              "Gut & immune": "/functional-medicine-austin", "Mold & detox": "/mold-detox-in-texas",
              "Peptides & longevity": "/peptide-therapy-austin", "Weight & metabolism": "/glp1-weight-loss-texas",
              "Functional medicine": "/functional-medicine-austin"}
TOPIC_SERVICE = {"Hormones": "BHRT & hormones", "Mental health": "Integrative psychiatry", "Gut & immune": "Functional medicine",
                 "Mold & detox": "Mold detox", "Peptides & longevity": "Peptide therapy", "Weight & metabolism": "GLP-1 weight loss",
                 "Functional medicine": "Functional medicine"}

# Old Wix pages linked from inside posts -> where that content lives now
LINK_MAP = {
    "/gut-health-testing-gut-zoomer": "/functional-medicine-lab-testing#gut",
    "/mycotoxin-testing-mold-illness": "/functional-medicine-lab-testing#mycotoxin",
    "/environmental-toxin-testing": "/functional-medicine-lab-testing#toxins",
    "/organic-acid-testing-texas": "/functional-medicine-lab-testing#oat",
    "/hormone-testing-functional-medicine": "/functional-medicine-lab-testing#hormones",
    "/food-sensitivity-testing-at-home": "/functional-medicine-lab-testing#food",
    "/methylation-genomics-testing": "/functional-medicine-lab-testing#methylation",
    "/genetic-snp-testing": "/functional-medicine-lab-testing#snp",
    "/weight-loss-with-peptides": "/glp1-weight-loss-texas",
    "/bioidentical-hormone-replacement-texas": "/menopause-clinic-texas",
    "/general-4": "/mold-detox-in-texas",
    "/get-started": "/#contact",
    "/contact-us": "/#contact",
}
BOOK_PATHS = {"/book-today"}


def local_image(mid):
    p = os.path.join(LOCAL_IMG_DIR, mid)
    return "/images/blog/" + mid if os.path.exists(p) else None


def img_url(mid, w=1400, fill=None):
    loc = local_image(mid)
    if loc:
        return loc
    base = re.sub(r"\.(jpe?g|png|webp|gif)$", "", mid, flags=re.I)
    if fill:
        return (f"https://static.wixstatic.com/media/{mid}/v1/fill/w_{fill[0]},h_{fill[1]},fp_0.50_0.50,q_85,"
                f"enc_avif,quality_auto/{base}.webp")
    return f"https://static.wixstatic.com/media/{mid}/v1/fit/w_{w},h_{w},q_90,enc_avif,quality_auto/{base}.webp"


def nice(d):
    y, m, dd = map(int, d[:10].split("-"))
    return date(y, m, dd).strftime("%B %-d, %Y")


def map_href(url):
    url = url.strip()
    url = url.replace("https://pubmed.ncbi.nlm.nih.gov/https://", "https://")
    if re.match(r"https?://l\.bttr\.to/MLk8a", url) or "bookings?r=677a0788" in url:
        return "DISCOVERY"   # free discovery call (same link as the site's "Book a free call" buttons)
    if re.match(r"https?://l\.bttr\.to/", url) or "practicebetter.io" in url and "/bookings" in url:
        return "BOOK"        # appointment booking -> the post's main service page instead
    m = re.match(r"https?://(www\.)?yourfunctionalmednp\.com(/[^?#]*)?(\?[^#]*)?(#.*)?$", url, re.I)
    if m:
        path = (m.group(2) or "/").rstrip("/") or "/"
        if path in BOOK_PATHS:
            return "BOOK"
        return LINK_MAP.get(path, path) + (m.group(4) or "")
    return url


# ---------- inline ----------
def inline(text):
    # Wix export glitches
    text = re.sub(r"\[([^\]]*)\]\(http://[\w-]+\.By\)", r"\1", text)          # bogus auto-links "word.By"
    text = re.sub(r"\s*\.By\b", ". By", text)
    text = re.sub(r"\[\s*\]\([^)]*\)", "", text)                                # empty links
    text = re.sub(r"(\*\*\*|\*\*|\*) ([,.;:!?)])", r"\1\2", text)             # "**bold** ," -> "**bold**,"
    text = re.sub(r"\( (\*+)", r"(\1", text)
    text = re.sub(r"(\*+) \)", r"\1)", text)

    text = re.sub(r"\bat \[https?://[^\]]*\]\(", "[here](", text)  # "...today at https://..." -> "...today here"
    links = []

    def keep_link(m):
        label, href = m.group(1), map_href(m.group(2))
        links.append((label, href))
        return f"\x00{len(links)-1}\x00"
    text = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)\)", keep_link, text)
    text = escape(text, quote=False)
    text = fmt(text)

    def put_link(m):
        label, href = links[int(m.group(1))]
        if re.search(r"\bcontact\b", label, re.I):
            href = "/#contact"
        if href == "BOOK" and re.fullmatch(r"[\s*→]*", label):
            return label.replace("*", "")  # stray arrow that linked to the old booking page
        if href == "BOOK":
            name, href = SERVICES[CURRENT["primary"]]
            if re.match(r"\s*https?://", label):
                label = name
        if re.match(r"\s*https?://", label) and href == "DISCOVERY":
            label = "Book a free discovery call"
        lab = fmt(escape(label, quote=False))
        if href == "DISCOVERY":
            return f'<a class="js-book" href="#" target="_blank" rel="noopener">{lab}</a>'
        ext = href.startswith("http")
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{escape(href)}"{attrs}>{lab}</a>'
    text = re.sub(r"\x00(\d+)\x00", put_link, text)
    return link_contact(text)


CONTACT_RE = re.compile(r"\b([Cc]ontact (?:Xenia|us|me|Us))\b")


def link_contact(html):
    """Wrap plain-text 'Contact Xenia/us/me' (outside existing links) in a link to the home page contact box."""
    parts = re.split(r"(<a\b.*?</a>)", html)
    for i in range(0, len(parts), 2):
        parts[i] = CONTACT_RE.sub(r'<a href="/#contact">\1</a>', parts[i])
    return "".join(parts)


def fmt(t):
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = t.replace("</strong><strong>", "").replace("<strong></strong>", "")
    t = re.sub(r"<strong>\s*</strong>", " ", t)
    return t


# ---------- blocks ----------
IMG_RE = re.compile(r"^!\[(.*?)\]\(wix:([^)]+)\)\s*(?:\{cap:\s*(.*)\})?\s*$")


def list_item(s):
    s = s.strip()
    parts = s.split(" - ")
    if len(parts) >= 3:  # flattened nested list: "Lead - sub - sub"
        lead = parts[0].rstrip(" :")
        lead_html = inline(lead) + (":" if parts[0].rstrip().endswith(":") else "")
        subs = "".join(f"<li>{inline(p)}</li>" for p in parts[1:] if p.strip())
        return f"<li>{lead_html}<ul>{subs}</ul></li>"
    return f"<li>{inline(s)}</li>"


def render_body(md, skip_first_image=None):
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)
    images = []
    first_block = True
    while i < n:
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1; continue
        m = IMG_RE.match(ln)
        if m:
            alt, mid, cap = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
            images.append(mid)
            if first_block and skip_first_image and mid == skip_first_image:
                first_block = False; i += 1; continue
            fig = (f'<figure><img src="{img_url(mid)}" alt="{escape(alt)}" loading="lazy" decoding="async">'
                   + (f"<figcaption>{inline(cap)}</figcaption>" if cap else "") + "</figure>")
            out.append(fig); first_block = False; i += 1; continue
        first_block = False
        h = re.match(r"^(#{1,6})\s+(.*)$", ln) or re.match(r"^-\s+(#{1,6})\s+(.*)$", ln)
        if h:
            lvl = min(max(len(h.group(1)), 2), 4)
            txt = h.group(2).strip()
            # headings that are wholly bold/italic: drop the markers, the heading style is enough
            txt = re.sub(r"^\*{1,3}(.*?)\*{1,3}$", r"\1", txt)
            if txt:
                out.append(f"<h{lvl}>{inline(txt)}</h{lvl}>")
            i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < n and (lines[i].startswith("|") or not lines[i].strip()):
                if lines[i].startswith("|"):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                        rows.append(cells)
                i += 1
            head, body = rows[0], rows[1:]
            th = "".join(f"<th>{inline(re.sub(r'^\*\*(.*)\*\*$', r'\1', c))}</th>" for c in head)
            tb = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
            continue
        if re.match(r"^[-*]\s+", ln) and not re.match(r"^\*[^\s*]", ln):
            items = []
            while i < n:
                l2 = lines[i].rstrip()
                if not l2.strip():
                    # list continues if next non-blank line is another item
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and re.match(r"^-\s+(?!#)", lines[j]):
                        i = j; continue
                    break
                if re.match(r"^-\s+#", l2) or not re.match(r"^-\s+", l2):
                    break
                items.append(list_item(re.sub(r"^-\s+", "", l2)))
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        # paragraph (each Wix paragraph is one line)
        cls = ' class="tick"' if re.match(r"^(✅|✔️|⭐|❗|⚠️|👉|📍|❌)", ln) else ""
        out.append(f"<p{cls}>{inline(ln.strip())}</p>")
        i += 1
    return "\n".join(out), images


def parse(path):
    raw = open(path, encoding="utf-8").read()
    head, _, body = raw.partition("\n\n")
    meta = {}
    for l in head.split("\n"):
        k, _, v = l.partition(":")
        meta[k.strip()] = v.strip()
    return meta, body


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def related(slug, topic, k=3):
    same = [p for p in POSTS if p[4] == topic and p[0] != slug]
    other = [p for p in POSTS if p[4] != topic and p[0] != slug]
    return (same + other)[:k]


def cover_url(slug, mid):
    """Cover image for cards: local file in src/assets/blog/covers/<slug>.webp, else the Wix original."""
    if os.path.exists(os.path.join(LOCAL_IMG_DIR, "covers", slug + ".webp")):
        return f"/images/blog/covers/{slug}.webp"
    return img_url(mid, fill=(640, 480))


def card(p):
    slug, title, d, mid, topic = p
    return f'''      <a class="post" href="/post/{slug}" style="--tc:{TOPIC_COLOR[topic]}">
        <div class="post-img"><span>{escape(topic)}</span><img src="{cover_url(slug, mid)}" alt="" loading="lazy" onerror="this.remove()"></div>
        <div class="post-body">
          <p class="post-meta"><b>{escape(topic)}</b><time datetime="{d}">{nice(d)[:3] + nice(d)[nice(d).index(' '):]}</time></p>
          <h3>{escape(title)}</h3>
          <span class="more">Read article &rarr;</span>
        </div>
      </a>'''


def strip_signoff(html):
    """Remove trailing sign-off lines ('Your Functional Med NP, Xenia', 'in Austin, Texas', 'Yours in health,'...);
    the author box replaces them."""
    blocks = html.rstrip().split("\n")
    sign = re.compile(r"^(xenia[,.]?|yours in health,?|your functional med(icine)? np[,.]?( xenia[,.]?)?|"
                      r"xenia, your functional med(icine)? np|in austin,? (texas|tx)\.?)$", re.I)
    while blocks:
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", blocks[-1])).strip()
        if sign.match(txt):
            blocks.pop()
        else:
            break
    return "\n".join(blocks)

def build_posts():
    """Returns list of dicts: slug, path, out, title, desc, html_body, jsonld, og_image."""
    pages = []
    info = {p[0]: p for p in POSTS}
    for p in POSTS:
        slug, title, d, mid, topic = p
        meta, body_md = parse(os.path.join(HERE, "posts", slug + ".md"))
        cover = meta.get("cover") or mid
        cap = ""
        first = IMG_RE.match(body_md.lstrip().split("\n", 1)[0])
        if first:  # the post opens with a photo: use it as the header image instead of a second, separate cover
            cover, cap = first.group(2).strip(), (first.group(3) or "").strip()
        CURRENT["primary"] = POST_SERVICES[slug][0]
        body_html, imgs = render_body(body_md, skip_first_image=cover)
        if cover not in imgs:
            imgs = [cover] + imgs
        body_html = strip_signoff(body_html)
        mins = max(1, math.ceil(words(body_html) / 230))
        desc = meta.get("desc") or re.sub(r"<[^>]+>", "", body_html)[:155]
        color = TOPIC_COLOR[topic]
        hero_img = img_url(cover, w=1600)
        tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        rel = "\n".join(card(r) for r in related(slug, topic))
        svc_btns = "\n".join(
            f'        <a class="btn {"btn-dark" if i == 0 else "btn-line"}" href="{SERVICES[k][1]}">{escape(SERVICES[k][0])} <span class="arrow">&rarr;</span></a>'
            for i, k in enumerate(POST_SERVICES[slug]))
        canonical = f"{SITE_URL}/post/{slug}"
        jsonld = {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": title, "description": desc, "datePublished": meta.get("date") or d,
            "image": [hero_img if hero_img.startswith("http") else SITE_URL + hero_img],
            "mainEntityOfPage": canonical,
            "author": {"@type": "Person", "name": "Xenia Kempf, FNP-C", "url": SITE_URL},
            "publisher": {"@type": "MedicalBusiness", "name": "Your Functional Health", "url": SITE_URL},
        }
        if tags:
            jsonld["keywords"] = ", ".join(tags)
        html = f'''<!-- ARTICLE -->
<article class="article" style="--tc:{color}">
  <header class="art-head">
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/functional-medicine-blog">Blog</a><span aria-hidden="true">/</span><span>{escape(topic)}</span></nav>
      <p class="art-topic">{escape(topic)}</p>
      <h1>{escape(title)}</h1>
      <p class="art-meta">By Xenia Kempf, FNP-C <span aria-hidden="true">&middot;</span> <time datetime="{(meta.get('date') or d)[:10]}">{nice(d)}</time> <span aria-hidden="true">&middot;</span> {mins} min read</p>
    </div>
  </header>
  <div class="wrap">
    <figure class="art-cover"><img src="{hero_img}" alt="{escape(first.group(1)) if first else ''}" fetchpriority="high" onerror="this.parentNode.remove()"></figure>{f'<p class="art-cap">{inline(cap)}</p>' if cap else ''}
    <div class="prose">
{body_html}
    </div>
    <nav class="svc-links" aria-label="Related services">
      <p class="eyebrow">Explore care</p>
      <div class="btn-row">
{svc_btns}
      </div>
    </nav>
    <aside class="author-box" aria-label="About the author">
      <img src="{{{{XENIA}}}}" alt="Xenia Kempf, FNP-C" width="96" height="96" loading="lazy">
      <div>
        <p class="eyebrow">Written by</p>
        <h2>Xenia Kempf, FNP-C</h2>
        <p>Board-certified family nurse practitioner practicing functional medicine, integrative psychiatry and hormone care in Austin, TX, and by video across Texas.</p>
        <div class="btn-row">
          <a class="btn btn-dark js-book" href="#" target="_blank" rel="noopener">Book a free call <span class="arrow">&rarr;</span></a>
        </div>
      </div>
    </aside>
    <p class="art-note">This article is for education only and isn't medical advice. Talk with your own clinician before changing medications or supplements.</p>
  </div>
</article>

<!-- RELATED -->
<section class="related" aria-labelledby="rel-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Keep reading</p>
        <h2 id="rel-title">More on <em>{escape(topic.lower())}</em></h2>
      </div>
      <a class="btn btn-line" href="/functional-medicine-blog">All articles</a>
    </div>
    <div class="post-grid">
{rel}
    </div>
  </div>
</section>
'''
        pages.append({"slug": slug, "path": f"/post/{slug}", "out": f"post/{slug}.html",
                      "title": f"{title} | Your Functional Health", "desc": desc, "html": html,
                      "jsonld": json.dumps(jsonld, ensure_ascii=False), "og_image": jsonld["image"][0],
                      "images": imgs, "name": title})
    return pages


if __name__ == "__main__":
    ps = build_posts()
    print(len(ps), sum(len(p["images"]) for p in ps))
