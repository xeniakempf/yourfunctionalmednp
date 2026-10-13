import html
T = [
 ("gut","Gut Health","Gut Zoomer · Vibrant Wellness · Stool","Over 200 microbes plus inflammatory markers, gut antibodies and metabolic byproducts. For bloating, constipation, brain fog, cravings, skin issues and fatigue.",650,"https://l.bttr.to/5Qb33",750,"https://l.bttr.to/YU9ZR",None),
 ("mycotoxin","Mycotoxin Panel","RealTime Laboratories · Urine","16 mycotoxins, including aflatoxins, ochratoxins and 9 macrocyclic trichothecenes from black mold.",395,"https://l.bttr.to/wEW6K",495,"https://l.bttr.to/Fy9vv","/mold-detox-in-texas"),
 ("toxins","Environmental Toxins","TOXDetect · Mosaic Diagnostics · Urine","27 metabolites of everyday toxicants from food, water, plastics, personal care products and air pollution, including glyphosate.",450,"https://l.bttr.to/xqXDE",550,"https://l.bttr.to/sZeou",None),
 ("oat","Organic Acids","Diagnostic Solutions · Urine","Energy and mitochondrial function, B vitamins and nutrients, stress and mood markers, oxidative stress and detox, and gut and fungal metabolites. Ages 12 and up.",375,"https://l.bttr.to/wOout",475,"https://l.bttr.to/rdHK1",None),
 ("hormones","Hormone Health","Physician's Lab · Urine (4–5 samples)","Steroid hormones, their metabolites and how efficiently your body breaks them down. For menopause, PCOS, PMS, low libido, fatigue, sleep, mood, and BHRT monitoring.",425,"https://l.bttr.to/H1rzB",525,"https://l.bttr.to/S8Ue3","/menopause-clinic-texas"),
 ("food","Food Sensitivities","Alletess Medical Laboratory · Finger prick","IgG response to 204 common foods, to uncover hidden triggers behind headaches, digestive issues, skin problems, fatigue, joint pain and brain fog.",485,"https://l.bttr.to/wnknn",None,None,None),
 ("methylation","Methylation Genomics","Genova Diagnostics · Cheek swab","Genetic variants in the methylation pathway (MTHFR, COMT, MTR, MTRR, CBS and more) that affect energy, mood, detox and hormones.",500,"https://l.bttr.to/S0tdk",600,"https://l.bttr.to/q7y5Y",None),
 ("snp","Genetic SNP Testing","Nordic Laboratories · 6 DNA panels","How your genes shape nutrient needs, detox, inflammation, hormones, mood, stress resilience and skin. Choose the panel that fits your goals.",None,None,None,None,"#dna"),
 ("immunology","Full Immunology Panel","Genova Diagnostics · Blood draw","IgE and IgG panels for foods, molds and spices, a celiac profile, and Texas inhalant allergens. Texas only; blood draw included in Cedar Park.",550,"https://l.bttr.to/zt3nX",650,"https://l.bttr.to/8KTaF",None),
]
D = [
 ("DNA Core","The broadest overview: lipids, methylation, detox, inflammation, oxidative stress, insulin sensitivity, bone health, nutrient needs, food intolerances, weight and exercise response.",555,"https://l.bttr.to/Faied",655,"https://l.bttr.to/Busli","https://www.yourfunctionalmednp.com/_files/ugd/01b06b_96a7a70ec3b1405ca3bd3bbf8eee9d38.pdf"),
 ("DNA Health","35+ genes for personalized nutrition: lipids, methylation, detox, inflammation, insulin, bone, iron, vitamins, and responses to salt, alcohol, caffeine, lactose and gluten.",500,"https://l.bttr.to/QyHcC",600,"https://l.bttr.to/5eqp0","https://www.yourfunctionalmednp.com/_files/ugd/01b06b_aafeae4e3e204f5a94f0040fe3321323.pdf"),
 ("DNA Mind","30 genes tied to mental health, including serotonin, dopamine, inflammation and methylation pathways.",425,"https://l.bttr.to/KrmFR",525,"https://l.bttr.to/RP34A","https://www.yourfunctionalmednp.com/_files/ugd/01b06b_cccaeaf6f7c54dc6a8f7646d79e10791.pdf"),
 ("DNA Resilience","Seven areas behind stress coping and performance: neuropeptide Y, oxytocin, BDNF, the stress axis, norepinephrine, dopamine and serotonin.",480,"https://l.bttr.to/eezPH",580,"https://l.bttr.to/QOXbv","https://www.yourfunctionalmednp.com/_files/ugd/01b06b_f5014033b63846bf9b904362cfa7d733.pdf"),
 ("DNA Hormones","21 variants in sex hormone metabolism: production, binding and transport, Phase I and II detox, and clotting risk.",425,"https://l.bttr.to/TpJry",525,"https://l.bttr.to/1TyQE",None),
 ("DNA Skin","18 genes tied to collagen, UV protection, inflammation and oxidative stress, for a genetically informed approach to skin aging.",425,"https://l.bttr.to/XeIeM",525,"https://l.bttr.to/ppllz","https://www.yourfunctionalmednp.com/_files/ugd/01b06b_ae4bfe1bb4bb4dbfa64a8fb3a8f34147.pdf"),
]
def esc(s): return html.escape(s, quote=True)
def tile(t):
    i,name,meta,desc,p1,l1,p2,l2,more=t
    out=[f'      <div class="cond lab" id="{i}">',f'        <h3>{esc(name)}</h3>',f'        <p class="meta">{esc(meta)}</p>',f'        <p>{esc(desc)}</p>']
    if p1:
        out.append('        <ul class="prices">')
        out.append(f'          <li><span>Test only</span><b>${p1}</b></li>')
        if p2: out.append(f'          <li><span>Test + interpretation</span><b>${p2}</b></li>')
        out.append('        </ul>')
        out.append('        <div class="btn-row">')
        if p2: out.append(f'          <a class="btn btn-dark" href="{l2}" target="_blank" rel="noopener">Test + interpretation</a>')
        out.append(f'          <a class="btn {"btn-line" if p2 else "btn-dark"}" href="{l1}" target="_blank" rel="noopener">Test only</a>')
        out.append('        </div>')
    else:
        out.append('        <ul class="prices"><li><span>6 panels</span><b>from $425</b></li></ul>')
        out.append('        <div class="btn-row"><a class="btn btn-dark" href="#dna">Compare DNA panels <span class="arrow">&darr;</span></a></div>')
    if more and p1:
        label = "About mold detox" if "mold" in more else "About BHRT &amp; hormones"
        out.insert(4, f'        <a class="sample" href="{more}">{label} &rarr;</a>')
    out.append('      </div>')
    return "\n".join(out)
def dna(d):
    name,desc,p1,l1,p2,l2,rep=d
    out=[f'      <div class="cond lab">',f'        <h3>{esc(name)}</h3>',f'        <p>{esc(desc)}</p>']
    if rep: out.append(f'        <a class="sample" href="{rep}" target="_blank" rel="noopener">See a sample report &rarr;</a>')
    out+=['        <ul class="prices">',f'          <li><span>Test only</span><b>${p1}</b></li>',f'          <li><span>Test + interpretation</span><b>${p2}</b></li>','        </ul>','        <div class="btn-row">',
          f'          <a class="btn btn-dark" href="{l2}" target="_blank" rel="noopener">Test + interpretation</a>',f'          <a class="btn btn-line" href="{l1}" target="_blank" rel="noopener">Test only</a>','        </div>','      </div>']
    return "\n".join(out)
page = f'''<!-- HERO -->
<section class="hero sub" aria-labelledby="hero-title">
  <div class="ph"><canvas class="art" data-art="lake" aria-hidden="true"></canvas><img data-photo="hero" alt=""></div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Functional medicine lab testing &middot; At-home kits</p>
    <h1 id="hero-title">Advanced <em>lab</em> testing</h1>
    <p class="lede">Go beyond standard bloodwork. Order the test you need online, collect your sample at home, and choose results by email or a virtual review with Xenia.</p>
    <div class="btn-row actions">
      <a class="btn btn-dark" href="#tests">See all tests <span class="arrow">&rarr;</span></a>
      <a class="btn btn-line js-book" href="#" target="_blank" rel="noopener">Not sure which? Book a free call</a>
    </div>
    <div class="stats">
      <div><b>9 tests</b><span>Gut, toxins, hormones, genetics and more</span></div>
      <div><b>At-home kits</b><span>Mailed to your door</span></div>
      <div><b>Interpretation</b><span>Optional virtual review</span></div>
      <div><b>HSA/FSA</b><span>Eligible</span></div>
    </div>
  </div>
</section>

<!-- TESTS -->
<section class="conditions" id="tests" aria-labelledby="tests-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Choose your test</p>
        <h2 id="tests-title">Answers beyond <em>standard</em> labs</h2>
      </div>
      <p class="lede">Pick <b>test only</b> to get your results by email, or <b>test + interpretation</b> to review them with Xenia in a virtual visit.</p>
    </div>
    <div class="cond-grid three">
{chr(10).join(tile(t) for t in T)}
    </div>
  </div>
</section>

<!-- DNA PANELS -->
<section id="dna" aria-labelledby="dna-title">
  <div class="wrap">
    <div class="cond-head">
      <div>
        <p class="eyebrow">Genetic SNP testing &middot; Nordic Laboratories</p>
        <h2 id="dna-title">Choose your <em>DNA</em> panel</h2>
      </div>
      <p class="lede">A kit is mailed to you, you collect your sample at home and return it with a prepaid label. Interpretation includes a 30-minute virtual review.</p>
    </div>
    <div class="cond-grid three">
{chr(10).join(dna(d) for d in D)}
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section id="how" aria-labelledby="how-title" class="conditions">
  <div class="wrap">
    <div class="framework-head">
      <div>
        <p class="eyebrow">How it works</p>
        <h2 id="how-title">From your door to your <em>results</em></h2>
      </div>
      <p class="lede">Most tests are collected at home. The Full Immunology Panel needs a blood draw, included at a partner facility in Cedar Park.</p>
    </div>
    <ol class="fw">
      <li><div><h3>Order online</h3><p>Choose your test and whether you want interpretation.</p></div></li>
      <li><div><h3>Receive your kit</h3><p>The kit and instructions are mailed to your address.</p></div></li>
      <li><div><h3>Collect at home</h3><p>Collect your sample and send it to the lab with the prepaid label.</p></div></li>
      <li><div><h3>Get your results</h3><p>Results arrive by email. With interpretation, the email includes a link to book your review with Xenia.</p></div></li>
    </ol>
    <div class="notes">
      <div><b>Educational testing</b><p>Ordering a test on its own doesn't make you a patient and doesn't include diagnosis, prescriptions or treatment. You become a patient after a new patient visit.</p></div>
      <div><b>Payment</b><p>Insurance doesn't cover these tests, but you can use HSA or FSA funds.</p></div>
      <div><b>Availability</b><p>Not available in New York, New Jersey or Rhode Island, or outside the continental US. The immunology panel is for Texas only.</p></div>
    </div>
  </div>
</section>

<!-- CLOSING -->
<section class="closing" aria-labelledby="closing-title">
  <div class="ph"><canvas class="art" data-art="mist" aria-hidden="true"></canvas><img data-photo="closing" alt="" loading="lazy"></div>
  <div class="wrap">
    <h2 id="closing-title">Not sure where to <em>start?</em></h2>
    <p>Book a free 15-minute call and we'll talk through which test fits your symptoms, or start with a full functional medicine visit.</p>
    <div class="btn-row">
      <a class="btn btn-dark js-book" href="#" target="_blank" rel="noopener">Book a free call <span class="arrow">&rarr;</span></a>
      <a class="btn btn-line" href="/functional-medicine-austin">Functional medicine</a>
    </div>
  </div>
</section>
'''
open('../../pages/functional-medicine-lab-testing.html','w').write(page)
print("ok")
