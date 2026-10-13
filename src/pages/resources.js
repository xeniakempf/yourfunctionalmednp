/* Resources page photos: free Unsplash photos (Unsplash License). */
window.PAGE = {
  photos: {
    hero:    "https://images.unsplash.com/photo-1662038271111-5b1c0b4157e8?auto=format&fit=crop&q=80&w=1800", // steaming mug on a wooden table by a sunlit window
    closing: "https://images.unsplash.com/photo-1759220948579-aa4866af0f0d?auto=format&fit=crop&q=80&w=1800"  // misty morning over a green field with trees
  }
};

/* ---------- Quizzes: open/close panels ---------- */
(function () {
  function openQuiz(id, scroll) {
    var p = document.getElementById(id);
    if (!p) return;
    document.querySelectorAll(".quiz-panel").forEach(function (o) { if (o !== p) o.hidden = true; });
    p.hidden = false;
    if (scroll) p.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  document.querySelectorAll("[data-open-quiz]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      openQuiz(a.getAttribute("data-open-quiz"), true);
      if (history.replaceState) history.replaceState(null, "", "#" + a.getAttribute("data-open-quiz"));
    });
  });
  document.querySelectorAll("[data-close-quiz]").forEach(function (b) {
    b.addEventListener("click", function () {
      var p = b.closest(".quiz-panel");
      p.hidden = true;
      var q = document.getElementById("quizzes");
      if (q) q.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
  function fromHash() {
    var id = location.hash.slice(1);
    if (id && /-quiz$/.test(id)) openQuiz(id, true);
  }
  window.addEventListener("hashchange", fromHash);
  fromHash();
})();

/* ---------- Multi-step checklist quiz ---------- */
function setupQuiz(cfg) {
  var form = document.getElementById(cfg.form);
  if (!form) return;
  var steps = form.querySelectorAll(".q-step");
  var dots = form.querySelectorAll(".q-steps li");
  var result = document.getElementById(cfg.result);
  var panel = form.closest(".quiz-panel");
  var current = 0;

  function show(i, scroll) {
    current = i;
    steps.forEach(function (s, k) { s.hidden = k !== i; });
    dots.forEach(function (d, k) {
      d.classList.toggle("on", k === i);
      d.classList.toggle("done", k < i);
    });
    if (scroll !== false) panel.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  show(0, false);

  steps.forEach(function (s) {
    var count = s.querySelector(".q-count");
    if (count) s.addEventListener("change", function () {
      var n = s.querySelectorAll("input[type=checkbox]:checked").length;
      count.textContent = n + " selected";
    });
  });

  form.addEventListener("click", function (e) {
    var b = e.target.closest("[data-q]");
    if (!b) return;
    if (b.dataset.q === "next" && current < steps.length - 1) show(current + 1);
    if (b.dataset.q === "back" && current > 0) show(current - 1);
  });

  function checked(name) {
    return Array.prototype.map.call(form.querySelectorAll('input[name="' + name + '"]:checked'), function (c) { return c.value; });
  }

  var emailInput = form.querySelector('input[type="email"]');
  var err = form.querySelector(".q-err");
  emailInput.addEventListener("input", function () { err.hidden = true; });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = emailInput.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err.hidden = false; emailInput.focus(); return; }

    var r = cfg.score(checked);
    document.getElementById(cfg.ids.score).textContent = r.total;
    document.getElementById(cfg.ids.level).textContent = r.level;
    document.getElementById(cfg.ids.msg).textContent = r.message;
    result.className = "q-result " + r.tone;

    var note = document.getElementById(cfg.ids.note);
    var deployed = !!document.querySelector('script[src$="/assets/site.js"]');
    if (deployed) {
      r.data.email = email;
      fetch(cfg.endpoint, {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(r.data)
      }).catch(function () {});
      note.hidden = true;
    } else {
      note.textContent = "Preview only: answers are not sent from this preview. On the live site they go to Xenia by email.";
      note.hidden = false;
    }

    form.hidden = true;
    result.hidden = false;
    panel.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  result.addEventListener("click", function (e) {
    var b = e.target.closest('[data-q="restart"]');
    if (!b) return;
    form.reset();
    form.querySelectorAll(".q-count").forEach(function (c) { c.textContent = "0 selected"; });
    result.hidden = true;
    form.hidden = false;
    show(0);
  });
}

/* Mold illness quiz: scoring from Xenia's original questionnaire */
setupQuiz({
  form: "moldQuiz",
  result: "mq-result",
  endpoint: "https://formspree.io/f/xzzvjbqg",
  ids: { score: "mq-score", level: "mq-level", msg: "mq-msg", note: "mq-note" },
  score: function (checked) {
    var c1 = checked("cat1"), c2 = checked("cat2"), c3 = checked("cat3");
    var s1 = c1.length >= 16 ? 3 : c1.length >= 10 ? 2 : c1.length >= 5 ? 1 : 0;
    var s2 = c2.length >= 10 ? 3 : c2.length >= 6 ? 2 : c2.length >= 3 ? 1 : 0;
    var s3 = c3.length;
    var total = s1 + s2 + s3;
    var level, message, tone;
    if (total >= 10) {
      level = "Probable Mold or Biotoxin Sickness"; tone = "high";
      message = "Your answers point strongly toward mold or biotoxin illness. A mycotoxin test and a mold detox consult are the right next steps, so you can confirm it and start a plan.";
    } else if (total >= 5) {
      level = "Possible Mold Sickness"; tone = "mid";
      message = "Several of your symptoms fit a mold pattern. Testing can confirm or rule out mold so you can stop guessing. A consult helps you decide what to test first.";
    } else {
      level = "Not Likely Mold Sickness"; tone = "low";
      message = "Your answers don't point to mold illness right now. If your symptoms continue, a functional medicine visit can look for other root causes.";
    }
    return {
      total: total, level: level, message: message, tone: tone,
      data: {
        category_1_answers: c1.join(", "),
        category_2_answers: c2.join(", "),
        category_3_answers: c3.join(", "),
        category_1_score: s1,
        category_2_score: s2,
        category_3_score: s3,
        total_score: total,
        risk_level: level
      }
    };
  }
});

/* Thyroid quiz: scoring from Xenia's original quiz (no email capture) */
(function () {
  var form = document.getElementById("thyroidQuiz");
  if (!form) return;
  var result = document.getElementById("tq-result");
  var err = document.getElementById("tq-err");
  var panel = form.closest(".quiz-panel");
  form.addEventListener("change", function () { err.hidden = true; });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var counts = { A: 0, B: 0, C: 0 }, missing = 0;
    for (var i = 1; i <= 5; i++) {
      var c = form.querySelector('input[name="q' + i + '"]:checked');
      if (c) counts[c.value]++; else missing++;
    }
    if (missing) { err.hidden = false; return; }
    var level, msg, tone;
    if (counts.A >= 3) {
      level = "Your symptoms may suggest a thyroid imbalance"; tone = "high";
      msg = "Consider a deeper evaluation with functional testing. A full thyroid panel looks well beyond TSH alone.";
    } else if (counts.B >= 3 || (counts.A >= 1 && counts.B >= 2)) {
      level = "You may be showing early signs of thyroid dysfunction"; tone = "mid";
      msg = "Monitoring and lifestyle support could be helpful. A free call is a good way to talk through what to watch and when to test.";
    } else {
      level = "Thyroid imbalance seems less likely"; tone = "low";
      msg = "It's still good to stay tuned in to your body. If symptoms change or build up, it's worth a closer look.";
    }
    document.getElementById("tq-level").textContent = level;
    document.getElementById("tq-msg").textContent = msg;
    result.className = "q-result " + tone;
    form.hidden = true;
    result.hidden = false;
    panel.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  result.addEventListener("click", function (e) {
    if (!e.target.closest('[data-q="restart"]')) return;
    form.reset();
    result.hidden = true;
    form.hidden = false;
    panel.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
