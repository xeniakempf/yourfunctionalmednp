/* Clinicians page photos: free Unsplash photos (Unsplash License). App and course screenshots are in /images/bhrt-*.webp */
window.PAGE = {
  photos: {
    hero:    "https://images.unsplash.com/photo-1516390118834-21602d501886?auto=format&fit=crop&q=80&w=1800", // mug and pencil on an open book
    closing: "https://images.unsplash.com/photo-1759220948579-aa4866af0f0d?auto=format&fit=crop&q=80&w=1800"  // misty morning over a green field
  }
};

/* Old links like /clinicians#pricing or #abx now live on the app pages */
(function () {
  var h = location.hash;
  var bhrt = ["#bhrt", "#inside", "#pricing", "#free-chart", "#faq", "#course", "#how"];
  if (h === "#abx") location.replace("/antibiotic-guide");
  else if (bhrt.indexOf(h) > -1) location.replace("/bhrt-navigator" + (h === "#bhrt" ? "" : h));
})();
