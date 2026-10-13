"""Generate src/pages/functional-medicine-blog.html/.js from blog_posts.py.
Cover images are hotlinked from Xenia's Wix media library for now; posts link to /post/<slug>."""
import sys, os, re
from html import escape
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_posts import POSTS

TOPICS = ["Hormones", "Mental health", "Gut & immune", "Mold & detox", "Peptides & longevity", "Weight & metabolism", "Functional medicine"]
COLOR = {"Hormones": "#985A60", "Mental health": "#5B5785", "Gut & immune": "#155863", "Mold & detox": "#80683A",
         "Peptides & longevity": "#3D6382", "Weight & metabolism": "#58744F", "Functional medicine": "#2F7178"}

def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def img(mid, w, h):
    base = re.sub(r"\.(jpe?g|png|webp)$", "", mid)
    return f"https://static.wixstatic.com/media/{mid}/v1/fill/w_{w},h_{h},fp_0.50_0.50,q_85,enc_avif,quality_auto/{base}.webp"

def nice(d):
    y, m, dd = map(int, d.split("-"))
    return date(y, m, dd).strftime("%b %-d, %Y")

def card(p, featured=False):
    slug, title, d, mid, topic = p
    w, h = (1200, 800) if featured else (640, 480)
    cls = "post feat" if featured else "post"
    return f'''      <a class="{cls}" href="/post/{slug}" data-topic="{slugify(topic)}" style="--tc:{COLOR[topic]}">
        <div class="post-img"><span>{escape(topic)}</span><img src="{img(mid, w, h)}" alt="" loading="{'eager' if featured else 'lazy'}" onerror="this.remove()"></div>
        <div class="post-body">
          <p class="post-meta"><b>{escape(topic)}</b><time datetime="{d}">{nice(d)}</time></p>
          <h3>{escape(title)}</h3>
          <span class="more">Read article &rarr;</span>
        </div>
      </a>'''

counts = {t: sum(1 for p in POSTS if p[4] == t) for t in TOPICS}
chips = [f'<button type="button" class="chip on" data-filter="all">All <span>{len(POSTS)}</span></button>']
chips += [f'<button type="button" class="chip" data-filter="{slugify(t)}" style="--tc:{COLOR[t]}">{escape(t)} <span>{counts[t]}</span></button>' for t in TOPICS]

html = f'''<!-- HERO -->
<section class="hero sub" aria-labelledby="hero-title">
  <div class="ph"><canvas class="art" data-art="mist" aria-hidden="true"></canvas><img data-photo="hero" alt=""></div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Blog &middot; Notes from the clinic</p>
    <h1 id="hero-title">Root-cause <em>reading</em></h1>
    <p class="lede">Articles on hormones, gut health, mental health, mold, peptides and metabolism, written to help you understand what's going on in your body and what you can do about it.</p>
    <div class="btn-row actions">
      <a class="btn btn-dark" href="#articles">Browse articles <span class="arrow">&rarr;</span></a>
      <a class="btn btn-line js-book" href="#" target="_blank" rel="noopener">Book a free call</a>
    </div>
  </div>
</section>

<!-- ARTICLES -->
<section id="articles" aria-labelledby="art-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">{len(POSTS)} articles</p>
        <h2 id="art-title">Latest from the <em>blog</em></h2>
      </div>
      <label class="blog-search"><span class="sr">Search articles</span><input type="search" id="blogSearch" placeholder="Search articles" autocomplete="off"></label>
    </div>
    <div class="chips-row" role="toolbar" aria-label="Filter by topic">
      {"".join(chips)}
    </div>
    <div class="post-feat-wrap">
{card(POSTS[0], True)}
    </div>
    <div class="post-grid">
{chr(10).join(card(p) for p in POSTS[1:])}
    </div>
    <p class="no-posts" id="noPosts" hidden>No articles match that search. Try another word or topic.</p>
  </div>
</section>

<!-- CLOSING -->
<section class="closing" aria-labelledby="closing-title">
  <div class="ph"><canvas class="art" data-art="mist" aria-hidden="true"></canvas><img data-photo="closing" alt="" loading="lazy"></div>
  <div class="wrap">
    <h2 id="closing-title">Ready to find <em>your</em> root cause?</h2>
    <p>Reading is a great start. For answers specific to you, book a free 15-minute call.</p>
    <div class="btn-row">
      <a class="btn btn-dark js-book" href="#" target="_blank" rel="noopener">Book a free call <span class="arrow">&rarr;</span></a>
    </div>
    <div class="btn-row svc-row">
      <a class="btn btn-line" href="/functional-medicine-austin">Functional medicine</a>
      <a class="btn btn-line" href="/integrative-primary-care">Integrative primary care</a>
      <a class="btn btn-line" href="/functional-integrative-psychiatry-texas">Integrative psychiatry</a>
      <a class="btn btn-line" href="/menopause-clinic-texas">BHRT &amp; hormones</a>
      <a class="btn btn-line" href="/glp1-weight-loss-texas">GLP-1 weight loss</a>
      <a class="btn btn-line" href="/peptide-therapy-austin">Peptide therapy</a>
      <a class="btn btn-line" href="/mold-detox-in-texas">Mold detox</a>
    </div>
  </div>
</section>
'''
open("../../pages/functional-medicine-blog.html", "w").write(html)

js = '''/* Blog page photos: free Unsplash photos (Unsplash License). Post covers load from Xenia's Wix media for now. */
window.PAGE = {
  photos: {
    hero:    "https://images.unsplash.com/photo-1516390118834-21602d501886?auto=format&fit=crop&q=80&w=1800", // mug and pencil on an open book
    closing: "https://images.unsplash.com/photo-1759220948579-aa4866af0f0d?auto=format&fit=crop&q=80&w=1800"  // misty morning over a green field
  }
};

/* Topic filter + search */
(function () {
  var posts = Array.prototype.slice.call(document.querySelectorAll("#articles .post"));
  var chips = document.querySelectorAll(".chips-row .chip");
  var search = document.getElementById("blogSearch");
  var none = document.getElementById("noPosts");
  var topic = "all";
  function apply() {
    var q = (search.value || "").trim().toLowerCase(), shown = 0;
    posts.forEach(function (p) {
      var ok = (topic === "all" || p.dataset.topic === topic) &&
               (!q || p.textContent.toLowerCase().indexOf(q) > -1);
      p.hidden = !ok; if (ok) shown++;
    });
    none.hidden = shown > 0;
  }
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      chips.forEach(function (x) { x.classList.toggle("on", x === c); });
      topic = c.dataset.filter; apply();
    });
  });
  search.addEventListener("input", apply);
})();

/* Open a topic from the address, e.g. /functional-medicine-blog#topic-hormones (old category links redirect here) */
(function () {
  var m = location.hash.match(/^#topic-([a-z-]+)$/);
  if (!m) return;
  var chip = document.querySelector('.chips-row .chip[data-filter="' + m[1] + '"]');
  if (chip) { chip.click(); document.getElementById("articles").scrollIntoView(); }
})();
'''
open("../../pages/functional-medicine-blog.js", "w").write(js)
print("ok", len(POSTS))
