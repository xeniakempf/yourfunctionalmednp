"""Builds the social share images (1200x630) for every page and blog post.

Run after changing a page's social title, hero photo or a post's cover:
    python3 src/tools/make_share_images.py            # only missing images
    python3 src/tools/make_share_images.py --all      # rebuild everything
    python3 src/tools/make_share_images.py /store     # one page (path) or post (slug)

Output: src/assets/share/<name>.jpg  (published at /images/share/<name>.jpg)
Photos: the page's hero photo (from src/pages/<page>.js), or the post's cover image.
Downloaded hero photos are cached in src/assets/share/_photos/ (not published).
"""
import io
import json
import os
import re
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
ASSETS = os.path.join(SRC, "assets")
OUT = os.path.join(ASSETS, "share")
CACHE = os.path.join(OUT, "_photos")
FONTS = os.path.join(ASSETS, "fonts")
sys.path.insert(0, os.path.join(SRC, "blog"))
from blog_posts import POSTS  # noqa: E402

W, H = 1200, 630
PHOTO_W = 600
TEAL = (21, 88, 99)
ON_DARK = (244, 243, 238)
SOFT = (207, 223, 223)
ACCENT = (186, 185, 180)

# Pages without a hero photo, or where a different picture shares better.
PAGE_PHOTO = {
    "/": os.path.join(ASSETS, "xenia.jpg"),
    "/functional-medicine-austin": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",  # mountain ridges at sunrise
    "/store": os.path.join(ASSETS, "photos", "mira-device.jpg"),
    "/clinicians": "app-screens",
    "/pp": "index", "/terms-of-use": "index", "/404": "index",
}
PAGE_LINE = {
    "/clinicians": "For NPs, PAs and prescribers",
    "/functional-medicine-blog": "By Xenia Kempf, FNP-C",
    "/resources": "Free downloads",
    "/store": "Recommended by Xenia Kempf, FNP-C",
    "/pp": "Healthify LLC", "/terms-of-use": "Healthify LLC", "/404": "",
}
DEFAULT_LINE = "Austin  ·  Virtual across Texas"


def font(name, size, weight):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fetch(url, dest):
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        url = re.sub(r"[?&]w=\d+", "", url)
        url += ("&" if "?" in url else "?") + "w=1400"
        with urllib.request.urlopen(url, timeout=60) as r:
            open(dest, "wb").write(r.read())
    return dest


def page_photo(page):
    p = PAGE_PHOTO.get(page["path"])
    if p and p.startswith("https://"):
        pid = re.search(r"photo-[\w-]+", p).group(0)
        return fetch(p, os.path.join(CACHE, pid + ".jpg"))
    if p == "app-screens":
        return app_screens()
    if p == "index":
        return hero_from_js("index")
    if p:
        return p
    return hero_from_js(page["slug"])


def app_screens():
    """Two BHRT app screens as phones on a light background (Clinicians card)."""
    from PIL import ImageFilter
    bg = Image.new("RGB", (PHOTO_W, H), (231, 238, 236))
    for name, x, y in (("bhrt-app-candidacy.webp", 70, 70), ("bhrt-app-rx-card.webp", 300, 40)):
        sc = Image.open(os.path.join(ASSETS, "photos", name)).convert("RGB")
        h = 540
        sc = sc.resize((round(sc.width * h / sc.height), h), Image.LANCZOS)
        mask = Image.new("L", sc.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, sc.width - 1, sc.height - 1), 26, fill=255)
        sh = Image.new("L", (sc.width + 60, sc.height + 60), 0)
        ImageDraw.Draw(sh).rounded_rectangle((30, 38, sc.width + 30, sc.height + 38), 26, fill=90)
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        bg.paste((40, 70, 75), (x - 30, y - 30), sh)
        frame = Image.new("RGB", (sc.width + 16, sc.height + 16), (22, 48, 58))
        fmask = Image.new("L", frame.size, 0)
        ImageDraw.Draw(fmask).rounded_rectangle((0, 0, frame.width - 1, frame.height - 1), 32, fill=255)
        bg.paste(frame, (x - 8, y - 8), fmask)
        bg.paste(sc, (x, y), mask)
    out = os.path.join(CACHE, "_clinicians-app.png")
    os.makedirs(CACHE, exist_ok=True)
    bg.save(out)
    return out


def hero_from_js(slug):
    js = os.path.join(SRC, "pages", slug + ".js")
    m = re.search(r'hero:\s*"(https://[^"]+)"', open(js, encoding="utf-8").read()) if os.path.exists(js) else None
    if not m:
        return os.path.join(ASSETS, "photos", "xenia-sunflowers.jpg")
    pid = re.search(r"photo-[\w-]+", m.group(1)).group(0)
    return fetch(m.group(1), os.path.join(CACHE, pid + ".jpg"))


def card(photo_path, title, eyebrow, line, out_path):
    img = Image.new("RGB", (W, H), TEAL)
    ph = Image.open(photo_path).convert("RGB")
    ph = ImageOps.fit(ph, (PHOTO_W, H), Image.LANCZOS, centering=(0.5, 0.45))
    img.paste(ph, (0, 0))
    d = ImageDraw.Draw(img)
    x0, x1 = PHOTO_W + 64, W - 60

    logo = Image.open(os.path.join(ASSETS, "logo-light.png")).convert("RGBA")
    lw = 250
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    img.paste(logo, (x0, 56), logo)

    f_eye = font("Jost[wght].ttf", 20, 500)
    f_line = font("Jost[wght].ttf", 23, 400)
    f_url = font("Jost[wght].ttf", 19, 400)
    # title: largest size that fits in 4 lines
    for size in (60, 56, 52, 48, 44, 40, 36):
        f_title = font("CormorantGaramond[wght].ttf", size, 500)
        lines = wrap(d, title, f_title, x1 - x0)
        if len(lines) <= 4:
            break
    lh = round(size * 1.08)
    block = (32 if eyebrow else 0) + lh * len(lines) + (58 if line else 0)
    y = max(200, (H - block) // 2 + 30)
    if eyebrow:
        d.text((x0, y), eyebrow.upper(), font=f_eye, fill=SOFT, spacing=0)
        y += 34
    for ln in lines:
        d.text((x0, y), ln, font=f_title, fill=ON_DARK)
        y += lh
    if line:
        y += 18
        d.line((x0, y, x0 + 44, y), fill=ACCENT, width=2)
        d.text((x0, y + 14), line, font=f_line, fill=SOFT)
    d.text((x0, H - 56), "yourfunctionalmednp.com", font=f_url, fill=ACCENT)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "JPEG", quality=84, optimize=True, progressive=True)


def main(args):
    rebuild = "--all" in args
    only = [a for a in args if not a.startswith("--")]
    seo = json.load(open(os.path.join(SRC, "seo.json"), encoding="utf-8"))
    pages = []
    src = open(os.path.join(SRC, "build.py"), encoding="utf-8").read()
    for m in re.finditer(r'\{"slug": "([^"]+)", "path": "([^"]+)"', src):
        pages.append({"slug": m.group(1), "path": m.group(2)})
    n = 0
    for p in pages:
        if only and p["path"] not in only:
            continue
        s = seo["pages"].get(p["path"], {})
        if s.get("index") is False:
            continue
        out = os.path.join(OUT, ("home" if p["path"] == "/" else p["slug"]) + ".jpg")
        if os.path.exists(out) and not rebuild and not only:
            continue
        card(page_photo(p), s.get("og_title") or s["title"], "", PAGE_LINE.get(p["path"], DEFAULT_LINE), out)
        n += 1
    topics = {q[0]: q[4] for q in POSTS}
    for q in POSTS:
        slug, title = q[0], q[1]
        if only and slug not in only:
            continue
        out = os.path.join(OUT, "post", slug + ".jpg")
        if os.path.exists(out) and not rebuild and not only:
            continue
        cover = os.path.join(ASSETS, "blog", "covers", slug + ".webp")
        card(cover, title, topics[slug], "By Xenia Kempf, FNP-C", out)
        n += 1
    print("share images written:", n)


if __name__ == "__main__":
    main(sys.argv[1:])
