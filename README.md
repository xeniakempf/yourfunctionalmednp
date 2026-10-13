# yourfunctionalmednp.com

Website for Your Functional Health (Healthify LLC), Xenia Kempf, FNP-C.
Hosted on Netlify, which publishes the `site/` folder automatically whenever this repository changes.

## Folders

| Folder | What it is |
|---|---|
| `site/` | The finished website, exactly as visitors see it. Generated; don't edit by hand. |
| `src/` | The source the site is built from. Make changes here. |
| `src/pages/` | The body of each page (`<page>.html`) and its photos/scripts (`<page>.js`). |
| `src/partials/` | Shared pieces used on every page: `header.html`, `footer.html`, `style.css`, `script.js`. |
| `src/blog/posts/` | The 64 blog articles, one text file each, named after the article's web address. |
| `src/blog/blog_posts.py` | Article list for the blog page: title, date, cover image, topic. |
| `src/blog/services.py` | Which service buttons appear at the end of each article. |
| `src/blog/render.py` | Turns the article files into article pages. |
| `src/legal/` | Privacy Policy (`privacy.txt`) and Terms of Use (`terms.txt`) text. |
| `src/assets/` | Logo, photos and product images used on the site. `originals/` holds unused source images (not published). |
| `src/build.py` | Builds `site/` from `src/`. Also holds the page list and the redirects from old Wix addresses. |
| `src/tools/archive/` | One-time scripts that first generated some pages. Kept for reference only; the files in `src/pages/` are now the source of truth, so don't rerun these. |

## Making a change

1. Edit files in `src/`.
2. Rebuild: `python3 src/build.py` (needs Python 3, nothing else). If you edited `src/legal/*.txt`, run `python3 src/legal/gen_legal.py` first.
3. Commit both `src/` and `site/` and push. Netlify deploys in about a minute.

## Notes

- Pages are served at their exact old Wix addresses (e.g. `/store`, `/post/brain-fog`); old addresses that no longer exist are redirected in `site/_redirects` (generated from `OLD_TO_NEW` in `src/build.py`).
- Blog images still load from Wix's image server and the Resources PDFs from Wix — both must be moved into this repository before the domain is switched away from Wix.
- Forms: the home page contact form uses Netlify Forms; the quizzes post to Formspree.
