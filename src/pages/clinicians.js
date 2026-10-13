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

/* Course sample pages: on hover (mouse) the whole page enlarges to 125% of the printed page size;
   on click/tap it opens full size in a viewer. */
(function () {
  var items = document.querySelectorAll(".zoomable"), dlg = document.getElementById("pageViewer");
  if (!items.length) return;
  var PAGE_W = 816 * 1.25;          // a US-letter PDF page is 816 CSS px wide at 100%; show it at 125%
  var big = document.createElement("img");
  big.className = "page-magnified"; big.alt = ""; big.setAttribute("aria-hidden", "true");
  document.body.appendChild(big);
  var active = null;

  function place(e) {
    if (!active) return;
    var r = active.getBoundingClientRect(), vw = innerWidth, vh = innerHeight, pad = 16;
    var w = Math.min(PAGE_W, vw - pad * 2), h = w * (active.naturalHeight / active.naturalWidth);
    var left = Math.min(Math.max(r.left + r.width / 2 - w / 2, pad), vw - w - pad);
    var top;
    if (h <= vh - pad * 2) top = Math.min(Math.max(r.top + r.height / 2 - h / 2, pad), vh - h - pad);
    else {                            // taller than the screen: pan with the mouse
      var fy = Math.min(Math.max((e.clientY - r.top) / r.height, 0), 1);
      top = pad - (h - (vh - pad * 2)) * fy;
    }
    big.style.width = w + "px"; big.style.left = left + "px"; big.style.top = top + "px";
  }
  items.forEach(function (btn) {
    var img = btn.querySelector("img");
    btn.addEventListener("pointerenter", function (e) {
      if (e.pointerType !== "mouse" || !img.naturalWidth) return;
      active = img; big.src = img.currentSrc; place(e);
      requestAnimationFrame(function () { big.classList.add("on"); btn.classList.add("zoomed"); });
    });
    btn.addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") place(e); });
    btn.addEventListener("pointerleave", function () { active = null; big.classList.remove("on"); btn.classList.remove("zoomed"); });
    btn.addEventListener("click", function () {
      active = null; big.classList.remove("on"); btn.classList.remove("zoomed");
      if (!dlg || !dlg.showModal) { window.open(btn.dataset.full, "_blank"); return; }
      var d = dlg.querySelector("img"); d.src = btn.dataset.full; d.alt = img.alt; dlg.showModal();
    });
  });
  addEventListener("scroll", function () { if (active) { big.classList.remove("on"); active = null; } }, { passive: true });
  if (dlg) {
    dlg.querySelector(".pv-close").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  }
})();
