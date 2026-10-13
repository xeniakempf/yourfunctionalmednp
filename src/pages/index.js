/* Homepage photos: free Unsplash photos (Unsplash License). Swap any for your own, e.g. "/images/hero.jpg".
   Leave one empty ("") to show the painted landscape instead. */
window.PAGE = {
  photos: {
    hero:    "https://images.unsplash.com/photo-1784655597870-ac76256865a9?auto=format&fit=crop&q=80&w=1800", // morning mist over a forest lake (Paul Wuthrich)
    band:    "https://images.unsplash.com/photo-1776595900864-674b5c4b7b79?auto=format&fit=crop&q=80&w=1800", // misty lake, trees reflected (Sam Burrough)
    steps:   "https://images.unsplash.com/photo-1558724041-f4de24818f17?auto=format&fit=crop&q=80&w=1400",    // woman walking between flower fields (Matt Flores)
    closing: "https://images.unsplash.com/photo-1734386011664-a17cc4ef6755?auto=format&fit=crop&q=80&w=1800"  // sunlight through forest trees (Joyce G)
  },
  symptoms: [
    ["Fatigue","Bloating","Brain fog","Weight gain","Hot flashes","Poor sleep","Anxiety","Low libido","Hashimoto's","Sugar cravings","IBS","Burnout"],
    ["Depression","SIBO","PCOS","Night sweats","Mold exposure","Hair thinning","Reflux","Irregular cycles","Insulin resistance","Food sensitivities","Joint aches","Feeling flat"]
  ]
};

/* Root-cause health assessment: 10 questions -> top pattern. Lead goes to Formspree (emails Xenia). */
(function () {
  var LEAD_URL = "https://formspree.io/f/mgojgbqa";
  var BOOKING_URL = "https://l.bttr.to/MLk8a";
  var panel = document.getElementById("rca"), app = document.getElementById("rcaApp");
  var openBtn = document.getElementById("rcaOpen"), closeBtn = document.getElementById("rcaClose");
  if (!panel) return;

  var QUESTIONS = [
    { q: "How would you describe your energy through a typical day?", opts: [
      { t: "Steady and consistent", s: {} },
      { t: "Fine in the morning, crash by afternoon", s: { thyroid: 1, adrenal: 2 } },
      { t: "Wired in the morning, exhausted by evening", s: { adrenal: 2 } },
      { t: "Low most of the day, no matter how I sleep", s: { thyroid: 2 } } ]},
    { q: "How does your digestion feel after a typical meal?", opts: [
      { t: "Comfortable, no issues", s: {} },
      { t: "Bloated or gassy within an hour", s: { gut: 2 } },
      { t: "Fine at first, sluggish or heavy later", s: { gut: 1, metabolic: 1 } },
      { t: "Unpredictable — varies day to day", s: { gut: 2 } } ]},
    { q: "Do you notice bloating, irregularity, or discomfort on a regular basis?", opts: [
      { t: "Rarely, if ever", s: {} },
      { t: "Occasionally, tied to certain foods", s: { gut: 1 } },
      { t: "Frequently, several times a week", s: { gut: 2 } },
      { t: "Daily — it affects how I plan my day", s: { gut: 3 } } ]},
    { q: "How do you feel 2–3 hours after a carb-heavy meal?", opts: [
      { t: "Steady and clear-headed", s: {} },
      { t: "A little sleepy, nothing major", s: { metabolic: 1 } },
      { t: "Shaky, foggy, or craving more food", s: { metabolic: 2 } },
      { t: "Crash hard — I need caffeine or sugar to recover", s: { metabolic: 3 } } ]},
    { q: "Have you noticed weight changes that feel hard to explain or manage?", opts: [
      { t: "No, my weight is stable and predictable", s: {} },
      { t: "Slow, gradual gain despite no real changes", s: { metabolic: 2 } },
      { t: "Weight holds on stubbornly around my midsection", s: { metabolic: 2, thyroid: 1 } },
      { t: "Fluctuates a lot for no clear reason", s: { metabolic: 1, adrenal: 1 } } ]},
    { q: "How would you rate your sleep quality most nights?", opts: [
      { t: "I fall asleep easily and wake rested", s: {} },
      { t: "I fall asleep fine but wake during the night", s: { adrenal: 2 } },
      { t: "I feel 'tired but wired' at bedtime", s: { adrenal: 2 } },
      { t: "I wake up feeling unrested no matter how long I sleep", s: { thyroid: 1, adrenal: 1 } } ]},
    { q: "Do you feel anxious, on edge, or unable to fully relax, even when nothing's wrong?", opts: [
      { t: "Not really — I feel fairly calm", s: {} },
      { t: "Sometimes, during stressful weeks", s: { adrenal: 1 } },
      { t: "Often — it's become my baseline", s: { adrenal: 2 } },
      { t: "Constantly — it's hard to switch off", s: { adrenal: 3 } } ]},
    { q: "Have you noticed hair thinning, dry skin, brittle nails, or feeling cold often?", opts: [
      { t: "No, not really", s: {} },
      { t: "One of these, mildly", s: { thyroid: 1 } },
      { t: "A couple of these regularly", s: { thyroid: 2 } },
      { t: "Several of these, and they're getting more noticeable", s: { thyroid: 3 } } ]},
    { q: "Do you seem to react to things others don't — mold, fragrances, certain foods — or get sick often?", opts: [
      { t: "No, my system feels resilient", s: {} },
      { t: "A little more sensitive than most people", s: { toxin: 1 } },
      { t: "Yes, noticeably — certain environments affect me", s: { toxin: 2 } },
      { t: "Very much — I've had to change how I live because of it", s: { toxin: 3 } } ]},
    { q: "How would you describe joint aches, skin flare-ups, or seasonal allergy symptoms?", opts: [
      { t: "Minimal to none", s: {} },
      { t: "Occasional and mild", s: { toxin: 1 } },
      { t: "Noticeable and recurring", s: { toxin: 2 } },
      { t: "Frequent enough to affect my daily comfort", s: { toxin: 2, gut: 1 } } ]}
  ];

  var ARCHETYPES = {
    gut: { name: "Digestive Root Pattern",
      desc: "Your answers point toward your gut as a central piece of the puzzle. Digestive imbalances — whether it's bacterial overgrowth, low stomach acid, or food sensitivities — often sit upstream of energy, mood, and even hormone symptoms, since so much of your immune and nervous system activity starts in the gut.",
      clusters: ["Bloating or irregularity tied to meals", "Digestive discomfort that varies day to day", "Possible downstream effects on energy or skin"] },
    metabolic: { name: "Blood Sugar & Metabolic Pattern",
      desc: "Your answers suggest your body may be working harder than it should to manage blood sugar. This often shows up as energy crashes, cravings, and stubborn weight — and over time, unaddressed blood sugar swings can affect hormones, inflammation, and long-term metabolic health.",
      clusters: ["Energy dips or crashes after meals", "Cravings or shakiness between meals", "Weight that holds on despite effort"] },
    adrenal: { name: "Stress-Adrenal Pattern",
      desc: "Your answers point to a nervous system that's been running in overdrive. Chronic stress response — even when it feels 'normal' by now — can disrupt sleep, energy, digestion, and hormone balance, since your body prioritizes short-term survival signals over long-term repair.",
      clusters: ["Wired-but-tired energy pattern", "Trouble fully relaxing or switching off", "Sleep that doesn't leave you feeling rested"] },
    thyroid: { name: "Low Energy & Thyroid Pattern",
      desc: "Your answers suggest a pattern often associated with sluggish thyroid or mitochondrial function — low, flat energy that doesn't respond to more sleep, along with physical signs like dry skin, hair thinning, or feeling cold. This pattern benefits from a closer look at thyroid and metabolic markers.",
      clusters: ["Persistent low energy regardless of rest", "Physical signs like cold intolerance or hair thinning", "Weight that's hard to shift"] },
    toxin: { name: "Inflammatory & Toxin Load Pattern",
      desc: "Your answers point toward a body that may be carrying a higher inflammatory or toxic burden than it can comfortably clear — whether from mold, environmental exposures, or immune reactivity. This pattern often shows up as sensitivities, joint or skin symptoms, and a general sense of being 'reactive.'",
      clusters: ["Sensitivity to environment or certain foods", "Joint, skin, or allergy symptoms", "A system that feels like it's working overtime"] }
  };

  var step = 0, answers = [], leadName = "", leadEmail = "";
  function reset() { step = 0; answers = QUESTIONS.map(function () { return null; }); }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function scores() {
    var sc = { gut: 0, metabolic: 0, adrenal: 0, thyroid: 0, toxin: 0 };
    answers.forEach(function (a, qi) { if (a === null) return; var s = QUESTIONS[qi].opts[a].s; for (var k in s) sc[k] += s[k]; });
    return sc;
  }
  function topKey() { var sc = scores(), best = "gut", v = -1; for (var k in sc) if (sc[k] > v) { v = sc[k]; best = k; } return best; }
  function bar(frac) {
    var n = QUESTIONS.length, h = "";
    for (var i = 0; i < n; i++) h += '<span class="' + (i < Math.round(frac * n) ? "on" : "") + '"></span>';
    return '<div class="rca-bar" aria-hidden="true">' + h + "</div>";
  }

  function render() {
    if (step < QUESTIONS.length) return renderQ(step);
    if (step === QUESTIONS.length) return renderGate();
    renderReport();
  }
  function renderQ(i) {
    var chosen = answers[i];
    app.innerHTML = bar(i / QUESTIONS.length) +
      '<p class="rca-step">Question ' + (i + 1) + " of " + QUESTIONS.length + "</p>" +
      '<h3 class="rca-q">' + esc(QUESTIONS[i].q) + "</h3>" +
      '<div class="rca-opts">' + QUESTIONS[i].opts.map(function (o, k) {
        return '<button type="button" class="rca-opt' + (chosen === k ? " on" : "") + '" data-k="' + k + '" aria-pressed="' + (chosen === k) + '">' + esc(o.t) + "</button>";
      }).join("") + "</div>" +
      '<div class="rca-nav"><button type="button" class="rca-back"' + (i === 0 ? " hidden" : "") + '>&larr; Back</button>' +
      '<button type="button" class="btn btn-dark rca-next"' + (chosen === null ? " disabled" : "") + ">" + (i === QUESTIONS.length - 1 ? "See my results" : "Next") + ' <span class="arrow">&rarr;</span></button></div>';
    app.querySelectorAll(".rca-opt").forEach(function (b) {
      b.addEventListener("click", function () { answers[i] = +b.dataset.k; render(); app.querySelector(".rca-next").focus(); });
    });
    app.querySelector(".rca-back").addEventListener("click", function () { step--; render(); });
    app.querySelector(".rca-next").addEventListener("click", function () { step++; render(); });
  }
  function renderGate() {
    app.innerHTML = bar(1) +
      '<h3 class="rca-q">Your root-cause pattern is ready.</h3>' +
      '<p class="rca-sub">Enter your name and email to see your personalized results.</p>' +
      '<form class="rca-gate" novalidate>' +
        '<label><span>First name</span><input type="text" name="name" autocomplete="given-name" required></label>' +
        '<label><span>Email address</span><input type="email" name="email" autocomplete="email" required></label>' +
        '<p class="rca-err" hidden>Please enter your first name and a valid email.</p>' +
        '<button type="submit" class="btn btn-dark">Show my results <span class="arrow">&rarr;</span></button>' +
        '<p class="rca-fine">Your results are educational and not a medical diagnosis. We\'ll only use your email to send your report and relevant follow-up.</p>' +
      "</form>" +
      '<div class="rca-nav"><button type="button" class="rca-back">&larr; Back</button><span></span></div>';
    var f = app.querySelector("form"), err = app.querySelector(".rca-err");
    app.querySelector(".rca-back").addEventListener("click", function () { step--; render(); });
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      leadName = f.name.value.trim(); leadEmail = f.email.value.trim();
      var ok = leadName && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(leadEmail);
      f.name.classList.toggle("bad", !leadName); f.email.classList.toggle("bad", !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(leadEmail));
      err.hidden = !!ok; if (!ok) return;
      var btn = f.querySelector("button[type=submit]"); btn.disabled = true; btn.firstChild.nodeValue = "One moment… ";
      sendLead().then(function () { step++; render(); });
    });
    f.name.focus();
  }
  function sendLead() {
    var a = ARCHETYPES[topKey()];
    var payload = {
      _subject: "Root cause assessment: " + a.name,
      name: leadName, email: leadEmail, pattern: a.name,
      submitted_at: new Date().toISOString(),
      answers_summary: QUESTIONS.map(function (q, i) { return q.q + " → " + (answers[i] !== null ? q.opts[answers[i]].t : ""); }).join(" | ")
    };
    var t = new Promise(function (r) { setTimeout(r, 6000); });   // never keep someone waiting on a slow network
    var req = fetch(LEAD_URL, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(payload) })
      .catch(function (e) { console.error("Assessment submission failed:", e); });
    return Promise.race([req, t]);
  }
  function renderReport() {
    var a = ARCHETYPES[topKey()];
    app.innerHTML = '<div class="rca-report">' +
      '<span class="rca-badge">Your pattern</span>' +
      '<h3 class="rca-title">' + esc(a.name) + "</h3>" +
      '<p class="rca-sub">' + esc(a.desc) + "</p>" +
      '<p class="rca-h">What this often looks like</p>' +
      '<ul class="rca-list">' + a.clusters.map(function (c) { return "<li>" + esc(c) + "</li>"; }).join("") + "</ul>" +
      '<p class="rca-sub">This kind of pattern is exactly what a root-cause, whole-person approach is built to untangle — with lab testing and a personalized plan, not guesswork.</p>' +
      '<div class="btn-row"><a class="btn btn-dark" href="' + BOOKING_URL + '" target="_blank" rel="noopener">Book a free discovery call <span class="arrow">&rarr;</span></a>' +
      '<a class="btn btn-line" href="/functional-medicine-lab-testing">See functional labs</a></div>' +
      '<p class="rca-disclaimer">This assessment is for general educational purposes only and is not a medical diagnosis. It does not replace a consultation with a licensed clinician. Individual results may vary and a full evaluation is needed to confirm any underlying condition.</p>' +
      '<button type="button" class="rca-back rca-again">Start over</button>' +
      "</div>";
    app.querySelector(".rca-again").addEventListener("click", function () { reset(); render(); });
  }

  function open() {
    panel.hidden = false; openBtn.setAttribute("aria-expanded", "true");
    if (step === 0 && answers.every(function (a) { return a === null; })) render();
    panel.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  reset(); render();
  openBtn.addEventListener("click", open);
  document.querySelectorAll("[data-rca-open]").forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); open(); }); });
  closeBtn.addEventListener("click", function () { panel.hidden = true; openBtn.setAttribute("aria-expanded", "false"); openBtn.focus(); });
  if (location.hash === "#assessment-start") open();
})();
