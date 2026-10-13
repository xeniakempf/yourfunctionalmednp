/* Clinicians page photos: free Unsplash photos (Unsplash License). App and course screenshots are in /images/bhrt-*.webp */
window.PAGE = {
  photos: {
    hero:    "https://images.unsplash.com/photo-1516390118834-21602d501886?auto=format&fit=crop&q=80&w=1800", // mug and pencil on an open book
    closing: "https://images.unsplash.com/photo-1759220948579-aa4866af0f0d?auto=format&fit=crop&q=80&w=1800"  // misty morning over a green field
  }
};

/* Free estradiol chart: emails the PDF via the chart-request function (Resend) */
(function () {
  var f = document.getElementById("chartForm"); if (!f) return;
  var msg = document.getElementById("chartMsg"), btn = f.querySelector("button");
  function say(t, err) { msg.textContent = t; msg.className = "chart-msg" + (err ? " err" : " ok"); msg.hidden = false; }
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = f.email.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { say("Please enter a valid email address.", true); f.email.focus(); return; }
    btn.disabled = true; btn.firstChild.nodeValue = "Sending… ";
    fetch("/.netlify/functions/chart-request", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, website: f.website.value })
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        if (res.ok) { say("Sent. Check your inbox (and spam folder) for the chart."); f.reset(); btn.firstChild.nodeValue = "Sent "; }
        else { say(res.d.error || "Something went wrong. Please try again.", true); btn.disabled = false; btn.firstChild.nodeValue = "Email me the chart "; }
      })
      .catch(function () { say("Network error. Please try again.", true); btn.disabled = false; btn.firstChild.nodeValue = "Email me the chart "; });
  });
})();

/* Course sample pages: click/tap opens the page full size in a viewer */
(function () {
  var items = document.querySelectorAll(".zoomable"), dlg = document.getElementById("pageViewer");
  if (!items.length) return;
  items.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var img = btn.querySelector("img");
      if (!dlg || !dlg.showModal) { window.open(btn.dataset.full, "_blank"); return; }
      var d = dlg.querySelector("img"); d.src = btn.dataset.full; d.alt = img.alt; dlg.showModal();
    });
  });
  if (dlg) {
    dlg.querySelector(".pv-close").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  }
})();
