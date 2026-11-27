# SEO & AI-visibility log

Weekly log kept by the scheduled SEO agent. Newest run first.

## 2026-11-27

### Technical audit
- Build is clean and reproducible; 82 URLs in sitemap.xml, all return 200 live. robots.txt fine. Live llms.txt matched the build.
- Titles/descriptions: none missing, duplicated or over length (only /404 has a short description, and it is noindex).
- JSON-LD parses on every page; one H1 per page.
- Internal links: no broken internal links. All 120+ old Wix redirects in `_redirects` resolve to 200 live.
- External links: all OK except 4 sites that block bots (ciceroinstitute.org, texas2036.org, ewg.org, ifm.org return 403 to scripts; they likely work in a browser) and PubMed (203, fine).
- Alt text: the only empty alts are decorative backgrounds, blog-index cards next to their titles, and the Healthgrades badge (its link has an aria-label). OK.
- Page speed: 18 blog images are over 300 KB (largest 768 KB, `understanding-the-functional-medicine-approach.webp`). They look losslessly encoded. Recompressed versions are on the draft branch.
- Internal linking gap: service pages (menopause, mold, peptides, GLP-1, functional medicine, primary care) linked to almost none of the 64 articles; most articles were only reachable from the blog index.

### AI visibility
- llms.txt listed services without prices, and left out /virtual-care-texas, /store, the blog and all lab-test prices.
- Schema had no prices for the Lab Testing page even though the page lists 28 prices.
- Patient questions not answered plainly as FAQs: lab testing page has no FAQ at all (insurance, ordering, who can order); GLP-1 and BHRT pages have prices but no "how much does it cost / does insurance cover it" Q&A.
- Peptide page has no prices anywhere (schema and llms.txt can't say what peptides cost). Needs Xenka's input; nothing changed.

### Published to main (safe fixes)
- llms.txt: added a "Quick facts" block (insurance/HSA/superbills, Texas-only, labs billed separately — restated from the home FAQ), prices on every service line, the virtual-care page, store, blog, and a full lab-test price list.
- schema.py: Lab Testing service now carries an OfferCatalog of every test and price, read directly from the page so it can't drift.
- Internal links: 20 links from existing wording on 6 service pages to related articles (no wording changed), e.g. "Bone loss and osteoporosis risk" → estrogen & bone health; "support bile flow" → bile flow before mold detox; BPC-157 / Ipamorelin / GHK-Cu / Epithalon → their articles.

### Waiting on draft branch `seo/2026-11-27` (not live)
1. Lab Testing page: new FAQ (5 questions) restating facts already on the page.
2. GLP-1 page: new FAQ "How much does the GLP-1 program cost? Is it covered by insurance?"
3. Menopause/BHRT page: new FAQ "How much does BHRT cost, and does insurance cover it?"
4. Recompressed 18 oversized blog images (same size and look, roughly 70–85% smaller files).

### Search check (US web search, 2026-11-27)
| Query | yourfunctionalmednp.com? | Who shows instead |
|---|---|---|
| functional medicine Austin TX | No | Forum Health Austin, IFM directory, healthprofs, Wild Fig |
| BHRT Texas virtual | No | BodyLogicMD, Forum Health, Midi, Optimize360, healthrx |
| direct primary care Texas price | No | DPC Frontier mapper, Zocdoc, news articles, freemarkethealthcareblog |
| integrative psychiatry Texas telehealth | No | Psychology Today listings dominate |
| mold toxicity doctor Texas | No | MoldCo, Forum Health, goop, Mayo Connect |
| GLP-1 telehealth Texas price | No | TrimRx, telehealthally, trytrimi (affiliate/comparison sites) |
| peptide therapy Austin | No | healingmaps.com "best peptide clinics in Austin" list, mypeptidematch, formblends |
| menopause clinic Austin | No | Austin Regional Clinic, Forum Health (Hormones by Design), BSW |
| functional medicine NP virtual Texas cash pay | Zocdoc profile only (#1) | Zocdoc, IFM directory |
| Xenia Kempf FNP | Zocdoc, Psychology Today, mypeptidematch, lantern — not the website | — |
| virtual primary care Midland Odessa | No | PlushCare, Zocdoc, MDVIP |

Takeaways: the website itself isn't surfacing in this search index even for Xenka's own name, while her third-party profiles (Zocdoc, Psychology Today, mypeptidematch, lantern.llc) do. Directory/listing sites (Psychology Today, healingmaps, telehealthally, DPC Frontier, IFM "find a practitioner") own most of these queries — getting listed/linked there is likely the fastest win. Suggest: (a) confirm in Google Search Console that the sitemap is submitted and pages are indexed; (b) if Xenka confirms, add her Zocdoc and Psychology Today profiles to `PROFILES_XENIA` in schema.py (sameAs) and make sure each of those profiles links to yourfunctionalmednp.com.
