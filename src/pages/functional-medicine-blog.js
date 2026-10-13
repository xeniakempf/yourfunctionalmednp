/* Blog page photos: free Unsplash photos (Unsplash License). Post covers load from Xenia's Wix media for now. */
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
