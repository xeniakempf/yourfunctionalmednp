/* ===== EDIT HERE (shared by every page) ===== */
const SITE = "https://www.yourfunctionalmednp.com";   // current site, used for pages not built yet
const BOOKING_URL = "https://l.bttr.to/MLk8a";        // free 15-min discovery call
const PORTAL_URL  = "https://yourfunctionalhealth.practicebetter.io/#/signin";
const ASSESSMENT_URL = "";                             // the assessment widget mounts in /#assessment
/* ============================================= */

/* Each page sets window.PAGE = { photos: {...}, symptoms: [[...],[...]] } before this script. */
const PAGE = window.PAGE || {};
const BUILT = window.BUILT_PAGES || ["/"];
const onSite = /yourfunctionalmednp\.com$|netlify\.app$|^localhost$|^127\./.test(location.hostname);

/* Links to pages that exist in the new site stay local; everything else opens the current site. */
document.querySelectorAll('a[href^="/"]').forEach(a => {
  const href = a.getAttribute("href"), path = href.split("#")[0] || "/";
  if (onSite && BUILT.includes(path)) return;
  a.href = SITE + href; a.target = "_blank"; a.rel = "noopener";
});
document.querySelectorAll(".js-book").forEach(a => a.href = BOOKING_URL);
document.querySelectorAll(".js-portal").forEach(a => a.href = PORTAL_URL);
if (ASSESSMENT_URL) document.querySelectorAll(".js-assess").forEach(a => { a.href = ASSESSMENT_URL; });
document.getElementById("yr").textContent = new Date().getFullYear();

const PHOTOS = PAGE.photos || {};
document.querySelectorAll("img[data-photo]").forEach(img => {
  const src = PHOTOS[img.dataset.photo];
  if (!src) { img.remove(); return; }
  img.addEventListener("error", () => img.remove());
  img.src = src;
});

/* ---- painted landscapes ---- */
const ART = {
  hero: { seed: 7, sky: [["#D6E4E3",0],["#E9EDE7",.42],["#F3E5D4",.74]], sun:[.76,.5,"246,224,196"], mist:"247,248,246",
    layers: [["#C9D9D6",.58,.05],["#AEC7C4",.66,.055],["#85A8A8",.74,.06],["#4E888F",.84,.05],["#24636D",.93,.04]] },
  lake: { seed: 21, sky: [["#B9CFCF",0],["#DDE3DC",.45],["#EEDDC8",.7]], sun:[.34,.5,"248,226,198"], mist:"240,241,236",
    layers: [["#A9C1BF",.47,.06],["#7C9FA0",.53,.045],["#3E727A",.58,.03]], water:.6, waterTop:"#7C9C9D", waterBot:"#2E5F68" },
  mist: { seed: 3, sky: [["#E3ECEA",0],["#F3F1EA",.75]], sun:[.5,.42,"250,236,214"], mist:"247,248,246",
    layers: [["#D4E1DE",.54,.04],["#C0D3D0",.63,.045],["#A6C0BE",.73,.05],["#8AAEAE",.85,.045]] }
};
function rng(a){ return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function paint(cv){
  const v = ART[cv.dataset.art]; if (!v) return;
  const r = cv.getBoundingClientRect(), d = Math.min(2, window.devicePixelRatio || 1);
  const W = Math.round(r.width * d), H = Math.round(r.height * d); if (!W || !H) return;
  cv.width = W; cv.height = H; const c = cv.getContext("2d"); const rand = rng(v.seed);
  const horizon = v.water ? H * v.water : H;
  let g = c.createLinearGradient(0, 0, 0, horizon); v.sky.forEach(([col, s]) => g.addColorStop(s, col));
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  const [sx, sy, sc] = v.sun, R = Math.max(W, H) * .42;
  g = c.createRadialGradient(W*sx, H*sy, 0, W*sx, H*sy, R);
  g.addColorStop(0, `rgba(${sc},.75)`); g.addColorStop(.12, `rgba(${sc},.45)`); g.addColorStop(1, `rgba(${sc},0)`);
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  c.fillStyle = `rgba(${sc},.9)`; c.beginPath(); c.arc(W*sx, H*sy, Math.min(W,H)*.035, 0, Math.PI*2); c.fill();
  v.layers.forEach(([col, base, amp], i) => {
    const waves = [0,1,2].map(k => ({ f: (1.2 + rand()*1.6) * (k+1) * Math.PI / W, p: rand()*Math.PI*2, a: amp * H / (k*1.8+1) }));
    const y0 = base * H;
    c.beginPath(); c.moveTo(0, horizon + 2);
    for (let x = 0; x <= W; x += Math.max(2, W/240)) c.lineTo(x, y0 + waves.reduce((s,w) => s + w.a*Math.sin(x*w.f + w.p), 0));
    c.lineTo(W, horizon + 2); c.closePath(); c.fillStyle = col; c.fill();
    if (i < v.layers.length - 1){
      g = c.createLinearGradient(0, y0 - amp*H, 0, y0 + H*.12);
      g.addColorStop(0, `rgba(${v.mist},0)`); g.addColorStop(1, `rgba(${v.mist},.38)`);
      c.fillStyle = g; c.fillRect(0, y0 - amp*H, W, H*.12 + amp*H);
    }
  });
  if (v.water){
    c.save(); c.translate(0, horizon*2); c.scale(1, -1); c.globalAlpha = .45; c.drawImage(cv, 0, 0, W, horizon, 0, 0, W, horizon); c.restore();
    g = c.createLinearGradient(0, horizon, 0, H); g.addColorStop(0, v.waterTop); g.addColorStop(1, v.waterBot);
    c.globalAlpha = .62; c.fillStyle = g; c.fillRect(0, horizon, W, H - horizon); c.globalAlpha = 1;
    c.strokeStyle = "rgba(255,255,255,.28)"; c.lineWidth = Math.max(1, d);
    for (let k = 0; k < 26; k++){ const y = horizon + (H - horizon) * Math.pow(rand(), 1.6), x = rand()*W, l = W*(.03 + rand()*.12);
      c.beginPath(); c.moveTo(x, y); c.lineTo(x + l, y); c.stroke(); }
  }
}
const arts = [...document.querySelectorAll("canvas.art")];
arts.forEach(paint);
if ("ResizeObserver" in window){
  let raf; const ro = new ResizeObserver(es => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => es.forEach(e => paint(e.target))); });
  arts.forEach(cv => ro.observe(cv));
}

/* ---- marquee (pages with symptom rows) ---- */
if (document.getElementById("t1") && PAGE.symptoms){
function fill(el, items){
  const html = items.map((t,i) => `<span class="${i%3===0?'g':''}">${t}</span>`).join("");
  el.innerHTML = matchMedia("(prefers-reduced-motion: reduce)").matches ? html : html + html;
}
fill(document.getElementById("t1"), PAGE.symptoms[0]);
fill(document.getElementById("t2"), PAGE.symptoms[1]);
const mq = document.querySelector(".marquee"), pb = document.getElementById("pauseBtn");
let paused = false;
pb.addEventListener("click", () => { paused = !paused; pb.textContent = paused ? "Play motion" : "Pause motion"; });
if (!matchMedia("(prefers-reduced-motion: reduce)").matches){
  /* each row moves at a steady speed in px/second; the second row runs the other way */
  const rows = [{ el: document.getElementById("t1"), speed: 28, dir: -1, x: 0 }, { el: document.getElementById("t2"), speed: 24, dir: 1, x: 0 }];
  let last = performance.now();
  const step = now => {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    rows.forEach(r => {
      const half = r.el.scrollWidth / 2; if (!half) return;
      if (!paused) r.x += r.dir * r.speed * dt;
      if (r.x <= -half) r.x += half;
      if (r.x > 0) r.x -= half;
      r.el.style.transform = `translate3d(${r.x}px,0,0)`;
    });
    requestAnimationFrame(step);
  };
  rows[1].x = -rows[1].el.scrollWidth / 4;
  requestAnimationFrame(step);
}
}

/* ---- contact form (Netlify Forms) ---- */
if (document.getElementById("contactForm")){
const cf = document.getElementById("contactForm"), cfStatus = document.getElementById("cfStatus");
cf.addEventListener("submit", async e => {
  e.preventDefault();
  const say = (msg, err) => { cfStatus.textContent = msg; cfStatus.classList.toggle("err", !!err); cfStatus.hidden = false; };
  if (!onSite){ say("Preview only: messages will be delivered once the site is live on Netlify."); return; }
  try {
    const r = await fetch("/", { method:"POST", headers:{ "Content-Type":"application/x-www-form-urlencoded" }, body: new URLSearchParams(new FormData(cf)).toString() });
    if (!r.ok) throw new Error(r.status);
    cf.reset(); say("Thank you. Your message was sent, and I'll reply by email within one business day.");
  } catch { say("The message didn't send. Please try again, or email xenia@yourfunctionalmednp.com.", true); }
});
}

/* ---- header, menu, services dropdown ---- */
const header = document.getElementById("header");
const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 40);
onScroll(); window.addEventListener("scroll", onScroll, {passive:true});

const toggle = document.getElementById("menuToggle"), nav = document.getElementById("nav");
const drop = document.getElementById("svcDrop"), dropBtn = document.getElementById("svcBtn");
const setDrop = open => { drop.classList.toggle("open", open); dropBtn.setAttribute("aria-expanded", open); };
const closeMenu = () => { nav.classList.remove("open"); header.classList.remove("open-menu"); toggle.setAttribute("aria-expanded", false); toggle.textContent = "Menu"; setDrop(false); };
toggle.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  header.classList.toggle("open-menu", open);
  toggle.setAttribute("aria-expanded", open);
  toggle.textContent = open ? "Close" : "Menu";
});
dropBtn.addEventListener("click", e => { e.stopPropagation(); setDrop(!drop.classList.contains("open")); });
const desktop = matchMedia("(min-width:1081px) and (hover:hover)");
let dropTimer;
drop.addEventListener("mouseenter", () => { if (desktop.matches){ clearTimeout(dropTimer); setDrop(true); } });
drop.addEventListener("mouseleave", () => { if (desktop.matches){ clearTimeout(dropTimer); dropTimer = setTimeout(() => setDrop(false), 250); } });
document.addEventListener("click", e => { if (!drop.contains(e.target) && desktop.matches) setDrop(false); });
document.addEventListener("keydown", e => { if (e.key === "Escape" && drop.classList.contains("open")){ setDrop(false); dropBtn.focus(); } });
nav.querySelectorAll("a").forEach(a => a.addEventListener("click", closeMenu));
