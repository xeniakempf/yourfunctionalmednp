"""Generate src/pages/resources.html. PDF links point at the Wix-hosted files for now;
set BASE to "/downloads/" (and map names) once the PDFs are moved into the repo."""
from html import escape
import sys; sys.path.insert(0, ".")
import mold_quiz

W = "https://www.yourfunctionalmednp.com/_files/ugd/01b06b_"

def u(fid):
    return W + fid + ".pdf"

GUT = u("295922cb96514dddaa89c8b6aee41cb6")

NUTRITION = [
    ("Anti-Inflammatory Guide", "Foods, supplements and daily habits that calm inflammation.", "df83d6558b874defa53f04fcddf9d29b"),
    ("Antioxidants Guide", "Antioxidant-rich foods, spices and supplements that counter free radicals.", "e277130e80aa4acfaf1d3c09b41f3a8e"),
    ("Approved Food Brands", "Brands I trust, because quality varies and labels can mislead.", "440e64283f3849c8981fa9d4d4c86eb1"),
    ("Intermittent Fasting for Beginners", "The basics of time-restricted eating and how to start gently.", "944efbdcbf2245078555f15d14564c57"),
    ("Improving Bioavailability", "Food pairings and cooking methods that help you absorb more nutrients.", "743a9a5a948b4e4aaeb113f69210f57c"),
    ("Control Your Cravings", "Read hunger cues, steady blood sugar and choose with confidence.", "5f1b97ecdd524af5850b8ccdc688c670"),
]

WELLNESS = [
    ("Nervous System Regulation", "Simple tools to calm and balance your nervous system.", "7de31b9a95714aeaa93ebfe28199f0ca"),
    ("Sleep Optimization", "Habits and routines for deeper, more refreshing sleep.", "0327698a57a14e91992b77b238a497d0"),
    ("Thyroid Health Guide", "Everyday support for healthy thyroid function.", "e18cf4990be04b488cc07fe72a192bf7"),
    ("Toxin-Free Living", "Practical ways to lower your toxin burden at home.", "1bfe35b954c94282a2704a0c41ad8475"),
    ("Mindfulness Challenge", "A short daily practice to stay present and find calm.", "d496015804b348199d38c41d0f087dca"),
    ("Digital Detox", "Break the screen habit and take back your attention.", "9993188028864e1bb5c0ea4fa39b1712"),
    ("Mindset Mastery", "Identify and move past the beliefs that hold you back.", "c211683876de4e68a4e19b605af11e75"),
    ("Life Purpose Guide", "Clarify what matters and set goals that fit.", "4493c59eb3cd424b87703cedc47276a9"),
    ("Deepen Your Connection", "Build stronger relationships and emotional connection.", "67ade875f8fd461d9a2701e4c6e1943d"),
]

PRODUCTS = [
    ("Face Cream", "6fef797b3ec3457cbf355782cce08cf3"),
    ("Facial Cleanser & Scrub", "512356847202408fadbc484b2effc63d"),
    ("Makeup Remover", "f3d6b843d8e540c8bf7a04ac539bea63"),
    ("Foundation", "51eb484de6dd4e11abfbf801c087e8ef"),
    ("Blush", "851bf7e952334114a9b9deedafeefef6"),
    ("Bronzer", "f405b7ed53af4c16a863f5470581c112"),
    ("Mascara", "189a482eb43b41b59fdde3dbde5f5604"),
    ("Shampoo & Conditioner", "aab5fda2dfed48cf98ec7e049fdafa16"),
    ("Body Wash", "5c295bcbf0cd4345b61c827bd67c03c2"),
    ("Soap Bar", "20c4d3f7035449809f01ebfd4e2aeffc"),
    ("Hand Soap", "798108a46959434b8a00cfb504b7ccc8"),
    ("Body Lotion", "755400d3bc5248db9e2a5297be8b26b6"),
    ("Hand Cream", "f60cf25be0e74b158fb6c692d84cfac6"),
    ("Deodorant", "d57d20f5049648a690faa074942598fd"),
    ("Toothpaste", "0a1ac3fb38934dbcb8b9f03e029f63e1"),
    ("Baby & Child", "af58684bf4734122a13018076f664898"),
]

def guides(items):
    out = []
    for t, d, fid in items:
        out.append(
            f'      <div class="guide"><h3>{escape(t)}</h3><p>{escape(d)}</p>'
            f'<a class="dl" href="{u(fid)}" target="_blank" rel="noopener">Open guide (PDF) &rarr;</a></div>')
    return "\n".join(out)

chips = "\n".join(
    f'      <a href="{u(fid)}" target="_blank" rel="noopener">{escape(t)} <span aria-hidden="true">&rarr;</span></a>'
    for t, fid in PRODUCTS)

html = f'''<!-- HERO -->
<section class="hero sub" aria-labelledby="hero-title">
  <div class="ph"><canvas class="art" data-art="mist" aria-hidden="true"></canvas><img data-photo="hero" alt=""></div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Free resources &middot; Printable guides</p>
    <h1 id="hero-title">Small steps, <em>real</em> change</h1>
    <p class="lede">Free, printable guides on nutrition, sleep, stress and toxin-free living, plus two short quizzes to help you see where to start.</p>
    <div class="btn-row actions">
      <a class="btn btn-dark" href="#guides">Browse the guides <span class="arrow">&rarr;</span></a>
      <a class="btn btn-line" href="#quizzes">Take a quiz</a>
    </div>
    <div class="stats">
      <div><b>{1 + len(NUTRITION) + len(WELLNESS)} guides</b><span>Nutrition, gut and wellness</span></div>
      <div><b>{len(PRODUCTS)} product lists</b><span>Safer personal care</span></div>
      <div><b>2 quizzes</b><span>Thyroid and mold illness</span></div>
      <div><b>Free</b><span>Printable PDFs</span></div>
    </div>
  </div>
</section>

<!-- START HERE -->
<section class="conditions" id="quizzes" aria-labelledby="start-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Start here</p>
        <h2 id="start-title">Find your <em>starting point</em></h2>
      </div>
      <p class="lede">Each quiz takes a few minutes and points you to the symptoms worth a closer look.</p>
    </div>
    <div class="cond-grid three">
      <div class="cond">
        <h3>Thyroid health quiz</h3>
        <p>Tired, cold, foggy or losing hair? See whether your symptoms fit a thyroid pattern.</p>
        <div class="btn-row" style="margin-top:1.25rem"><a class="btn btn-dark" href="#thyroid-quiz" data-open-quiz="thyroid-quiz">Take the thyroid quiz <span class="arrow">&rarr;</span></a></div>
      </div>
      <div class="cond">
        <h3>Mold illness quiz</h3>
        <p>Symptoms that started after water damage or time in a musty space? Check your exposure risk.</p>
        <div class="btn-row" style="margin-top:1.25rem"><a class="btn btn-dark" href="#mold-quiz" data-open-quiz="mold-quiz">Take the mold quiz <span class="arrow">&rarr;</span></a></div>
      </div>
      <div class="cond feature">
        <h3>Restoring gut health</h3>
        <p>My step-by-step guide to calming bloating, rebuilding the gut lining and supporting a healthy microbiome.</p>
        <div class="btn-row" style="margin-top:1.25rem">
          <a class="btn btn-light" href="{GUT}" target="_blank" rel="noopener">Open the gut guide (PDF)</a>
        </div>
      </div>
    </div>
{mold_quiz.thyroid_panel(u("e18cf4990be04b488cc07fe72a192bf7"))}{mold_quiz.panel()}
  </div>
</section>

<!-- GUIDES -->
<section id="guides" aria-labelledby="guides-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Guides</p>
        <h2 id="guides-title">Printable <em>guides</em></h2>
      </div>
      <p class="lede">Each guide opens as a PDF you can save or print.</p>
    </div>
    <div class="group-head nut" id="nutrition"><div><h3>Nutrition</h3><p>Eat to lower inflammation, steady blood sugar and absorb more.</p></div><span>{len(NUTRITION)} guides</span></div>
    <div class="guide-grid">
{guides(NUTRITION)}
    </div>
    <div class="group-head well" id="wellness"><div><h3>Wellness</h3><p>Sleep, stress, mindset and a calmer nervous system.</p></div><span>{len(WELLNESS)} guides</span></div>
    <div class="guide-grid">
{guides(WELLNESS)}
    </div>
  </div>
</section>

<!-- SAFER PRODUCTS -->
<section class="conditions" id="products" aria-labelledby="prod-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Toxin-free living</p>
        <h2 id="prod-title">Safer <em>personal care</em></h2>
      </div>
      <p class="lede">"Natural" on a label doesn't mean safe. These lists name cleaner options by category. Each opens as a PDF.</p>
    </div>
    <div class="chips">
{chips}
    </div>
    <p class="fine" style="margin-top:1.5rem">These lists are a starting point, not an endorsement, and not every safe product is included. To check a product yourself, search the <a href="https://www.ewg.org/skindeep/" target="_blank" rel="noopener">EWG Skin Deep database</a>.</p>
  </div>
</section>

<!-- CLOSING -->
<section class="closing" aria-labelledby="closing-title">
  <div class="ph"><canvas class="art" data-art="mist" aria-hidden="true"></canvas><img data-photo="closing" alt="" loading="lazy"></div>
  <div class="wrap">
    <h2 id="closing-title">Ready for a plan built <em>for you?</em></h2>
    <p>Guides are a great start. For answers specific to your body, book a free 15-minute call.</p>
    <div class="btn-row">
      <a class="btn btn-dark js-book" href="#" target="_blank" rel="noopener">Book a free call <span class="arrow">&rarr;</span></a>
      <a class="btn btn-line" href="/functional-medicine-austin">Functional medicine</a>
    </div>
  </div>
</section>
'''
open("../../pages/resources.html", "w").write(html)
print("ok")
