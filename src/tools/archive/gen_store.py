"""Generate src/pages/store.html and store.js. Product images are hotlinked from Wix for now."""
from html import escape
import json

WIX = "https://static.wixstatic.com/media/"

def wix(path):
    return WIX + path

MIRA_IMG = wix("01b06b_b058bb56edc24d6ca4ecd3283987b3fe~mv2.png/v1/fill/w_980,h_816,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/01b06b_b058bb56edc24d6ca4ecd3283987b3fe~mv2.png")
MIRA_LOGO = wix("01b06b_ce0a932936b14436808af047385cd4c8~mv2.png/v1/fill/w_528,h_232,al_c,q_85,enc_auto/mira%20logo.png")

# (slot, name, category, blurb, amazon link, wix image path with crop, scaled to 2x)
PRODUCTS = [
    ("yonanas", "Yonanas Soft Serve Maker", "Kitchen", "Turns frozen fruit into creamy soft serve. Dessert with no added sugar or dairy.", "https://amzn.to/4hWL0zZ", ""),
    ("ninja", "Ninja Blast Portable Blender", "Kitchen", "Protein shakes and smoothies anywhere. Rechargeable and easy to clean.", "https://amzn.to/47cZZRs", ""),
    ("pans", "Sensarte Ceramic Cookware Set", "Kitchen", "Non-toxic ceramic nonstick pots and pans with detachable handles that stack to save space.", "https://amzn.to/4zncZjs", ""),
    ("ring", "RingConn Smart Ring", "Wellness tech", "Tracks sleep, heart rate, HRV and recovery, with up to 14 days of battery. Works with iOS and Android.", "https://amzn.to/4ebUfLx", ""),
    ("scale", "RENPHO MorphoScan Smart Scale", "Wellness tech", "Body composition with hand electrodes, including muscle and fat by body segment, synced to your phone.", "https://amzn.to/4ym6Xi7", ""),
    ("pad", "Walking Pad with Incline", "Movement", "A compact under-desk treadmill with up to 7% incline, for steps during work or calls.", "https://amzn.to/4s4O6GO", ""),
    ("sauna", "Portable Sauna Blanket", "Recovery", "Adjustable heat from 86 to 158\u00b0F at home to relax, ease soreness and support sweating as part of detox.", "https://amzn.to/3Wm3TVI", ""),
    ("eye", "RENPHO Heated Eye Massager", "Recovery", "Gentle heat and massage for tired eyes, tension headaches and winding down.", "https://amzn.to/47gIpMo", ""),
    ("wand", "NuDerma Professional Skin Wand", "Skin", "A high-frequency skin wand with neon and argon applicators for at-home skin care.", "https://amzn.to/4zquMWN", ""),
]

FULLSCRIPT = "https://us.fullscript.com/welcome/xkempf?utm_medium=webreferral&amp;utm_source=other&amp;utm_campaign=abmwebbuttons_light_200x200.svg&amp;signup_source=website_buttons"
MIRA = "https://mira-fertility.pxf.io/c/6728056/1985822/12979"

cards = "\n".join(f'''      <a class="prod" href="{link}" target="_blank" rel="noopener sponsored">
        <div class="prod-img{' bleed' if slot in ('ring', 'sauna') else ''}"><span>{escape(name)}</span><img data-photo="{slot}" alt="{escape(name)}" loading="lazy"></div>
        <p class="meta">{escape(cat)}</p>
        <h3>{escape(name)}</h3>
        <p>{escape(blurb)}</p>
        <span class="more">View on Amazon &#8599;</span>
      </a>''' for slot, name, cat, blurb, link, _ in PRODUCTS)

html = f'''<!-- HERO -->
<section class="hero sub" aria-labelledby="hero-title">
  <div class="ph"><canvas class="art" data-art="mist" aria-hidden="true"></canvas><img data-photo="hero" alt=""></div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Store &middot; Practitioner-grade picks</p>
    <h1 id="hero-title">Tools I <em>trust</em></h1>
    <p class="lede">Professional-grade supplements, at-home hormone tracking, and the everyday products I recommend to patients.</p>
    <div class="btn-row actions">
      <a class="btn btn-dark" href="{FULLSCRIPT}" target="_blank" rel="noopener">Visit my supplement store <span class="arrow">&rarr;</span></a>
      <a class="btn btn-line" href="#mira">Track hormones at home</a>
    </div>
    <div class="stats">
      <div><b>Fullscript</b><span>Professional-grade supplements</span></div>
      <div><b>Client discounts</b><span>On supplements and Mira</span></div>
      <div><b>Mira</b><span>At-home hormone tracking</span></div>
      <div><b>{len(PRODUCTS)} picks</b><span>For kitchen, sleep and recovery</span></div>
    </div>
  </div>
</section>

<!-- SUPPLEMENTS + LABS -->
<section class="conditions" id="supplements" aria-labelledby="sup-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Supplements</p>
        <h2 id="sup-title">Quality you can <em>count on</em></h2>
      </div>
      <p class="lede">Supplements work best when they're chosen for you. I source through Fullscript so every product is the real thing.</p>
    </div>
    <div class="cond-grid three store-top">
      <div class="cond feature">
        <h3 class="fs-head"><img src="{{{{FS_LOGO}}}}" alt="Fullscript" width="197" height="34"><span>My supplement dispensary</span></h3>
        <ul class="ticks">
          <li>Professional-grade brands, tested for potency and purity</li>
          <li>Never expired or counterfeit, unlike many marketplace listings</li>
          <li>Ongoing discounts for Your Functional Health clients</li>
          <li>Shipped straight to your door</li>
        </ul>
        <div class="btn-row"><a class="btn btn-light" href="{FULLSCRIPT}" target="_blank" rel="noopener">Visit my store <span class="arrow">&rarr;</span></a></div>
      </div>
      <div class="cond">
        <h3>Just here for labs?</h3>
        <ol class="mini-steps">
          <li><b>Order your test</b>Choose a test and complete a short intake.</li>
          <li><b>Get your results</b>Read against functional, optimal ranges.</li>
          <li><b>Get your plan</b>Add interpretation for a personalized plan.</li>
        </ol>
        <div class="btn-row"><a class="btn btn-dark" href="https://us.fullscript.com/j/xkempf" target="_blank" rel="noopener">See lab tests <span class="arrow">&rarr;</span></a></div>
      </div>
      <div class="cond">
        <h3>Not sure what you need?</h3>
        <p>More isn't better. A functional medicine visit looks at your labs, history and current supplements, and builds a plan that fits.</p>
        <div class="btn-row"><a class="btn btn-dark js-book" href="#" target="_blank" rel="noopener">Book a free call <span class="arrow">&rarr;</span></a></div>
      </div>
    </div>
  </div>
</section>

<!-- MIRA -->
<section class="detail" id="mira" aria-labelledby="mira-title">
  <div class="wrap">
    <div class="detail-row">
      <div class="mira-img"><img data-photo="mira" alt="Mira hormone analyzer with test wands and app" loading="lazy"></div>
      <div>
        <p class="eyebrow">Hormone tracking at home</p>
        <h2 id="mira-title">See your <em>hormones</em> in real time</h2>
        <p>The Mira 4-in-1 kit measures LH, FSH, estrogen (E3G) and progesterone (PdG) from a morning urine sample, with lab-grade results in minutes. Helpful for fertility, PCOS, perimenopause and menopause, and for tracking how your hormones respond to treatment.</p>
        <div class="code-box">
          <div><span>Code for 20% off your first order</span><b>2XEMPF20</b></div>
          <p>Your Functional Health clients get an ongoing 30% off. Ask me for your client code.</p>
        </div>
        <div class="btn-row" style="margin-top:1.5rem">
          <a class="btn btn-dark" href="{MIRA}" target="_blank" rel="noopener sponsored">Get your Mira kit <span class="arrow">&rarr;</span></a>
          <a class="btn btn-line" href="/menopause-clinic-texas">BHRT &amp; hormones</a>
        </div>
      </div>
    </div>
    <div class="mira-steps">
      <h3>How testing works</h3>
      <div class="mira-steps-img"><img data-photo="miraSteps" alt="Four steps: dip the Mira wand in urine, insert it in the analyzer, read your result, track it in the app" loading="lazy"></div>
      <ol>
        <li><b>Dip</b>Hold the wand in first-morning urine for 10&ndash;15 seconds.</li>
        <li><b>Insert</b>Place the wand in the analyzer while it runs.</li>
        <li><b>Read</b>See your hormone level on screen in 15&ndash;20 minutes.</li>
        <li><b>Track</b>Results sync to the Mira app so you can follow your cycle.</li>
      </ol>
    </div>
  </div>
</section>

<!-- AMAZON PICKS -->
<section class="conditions" id="picks" aria-labelledby="picks-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Everyday wellness</p>
        <h2 id="picks-title">My <em>lifestyle</em> picks</h2>
      </div>
      <p class="lede">Products I use or recommend for cooking, sleep, movement and recovery. Each opens on Amazon.</p>
    </div>
    <div class="shop-grid">
{cards}
    </div>
  </div>
</section>

<!-- CLOSING -->
<section class="closing" aria-labelledby="closing-title">
  <div class="ph"><canvas class="art" data-art="mist" aria-hidden="true"></canvas><img data-photo="closing" alt="" loading="lazy"></div>
  <div class="wrap">
    <h2 id="closing-title">The right support, <em>for you.</em></h2>
    <p>Not sure which supplements or tools fit your goals? Start with a free 15-minute call.</p>
    <div class="btn-row">
      <a class="btn btn-dark js-book" href="#" target="_blank" rel="noopener">Book a free call <span class="arrow">&rarr;</span></a>
      <a class="btn btn-line" href="/functional-medicine-austin">Functional medicine</a>
    </div>
  </div>
</section>
'''
open("../../pages/store.html", "w").write(html)

photos = {
    "hero": "https://images.unsplash.com/photo-1596343621063-c7a7aaf37aa6?auto=format&fit=crop&q=80&w=1800",
    "closing": "https://images.unsplash.com/photo-1691220550627-35f03d7ce1f7?auto=format&fit=crop&q=80&w=1800",
    "mira": "/images/mira-device.jpg",
    "miraSteps": "/images/mira-steps.jpg",
}
for slot, *_rest in PRODUCTS:
    photos[slot] = "/images/shop-" + slot + ".jpg"
js = ("/* Store page photos. Hero and closing: free Unsplash photos (Unsplash License).\n"
      "   Mira images: Xenia's own (in /images). Amazon product images: Xenia's own (in /images). */\n"
      "window.PAGE = {\n  photos: " + json.dumps(photos, indent=4).replace("\n", "\n  ") + "\n};\n")
open("../../pages/store.js", "w").write(js)
print("ok")
