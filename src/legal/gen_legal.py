"""Build src/pages/pp.html and src/pages/terms-of-use.html from privacy.txt / terms.txt.
Format: '## ' heading, '- ' list item, any other line a paragraph; **bold** and [text](url) inline."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "blog"))
from render import inline as _inline

def inline(t):  # no automatic "contact us" links in legal text
    return re.sub(r'<a href="/#contact">([Cc]ontact (?:us|me))</a>', r"\1", _inline(t))

def body(txt):
    out, ul = [], []
    for ln in open(os.path.join(HERE, txt), encoding="utf-8").read().splitlines():
        ln = ln.strip()
        if ln.startswith("- "):
            ul.append(f"<li>{inline(ln[2:])}</li>"); continue
        if ul:
            out.append("<ul>" + "".join(ul) + "</ul>"); ul = []
        if not ln:
            continue
        if ln.startswith("## "):
            out.append(f"<h2>{inline(ln[3:])}</h2>")
        else:
            out.append(f"<p>{inline(ln)}</p>")
    if ul:
        out.append("<ul>" + "".join(ul) + "</ul>")
    return "\n".join(out)

def page(eyebrow, title, updated, intro, txt):
    return f'''<article class="article legal-page">
  <header class="art-head">
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p class="art-meta">Healthify LLC dba Your Functional Health <span aria-hidden="true">&middot;</span> Last updated {updated}</p>
    </div>
  </header>
  <div class="wrap">
    <div class="prose">
{intro}
{body(txt)}
    </div>
  </div>
</article>
'''

UPDATED = "October 13, 2026"
pages = os.path.join(HERE, "..", "pages")
open(os.path.join(pages, "pp.html"), "w", encoding="utf-8").write(page("Legal", "Privacy <em>Policy</em>", UPDATED,
    '<p class="lead">This policy explains what information this website collects, why, and the choices you have.</p>', "privacy.txt"))
open(os.path.join(pages, "terms-of-use.html"), "w", encoding="utf-8").write(page("Legal", "Terms of <em>Use</em>", UPDATED, "", "terms.txt"))
print("ok")
