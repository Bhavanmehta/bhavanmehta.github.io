# bhavanmehta.github.io

Source for my portfolio site: https://bhavanmehta.github.io

I'm a Senior Data Engineer working on finance data. The site is one static HTML page with no framework and no build tooling beyond a short Python script.

## How it is put together

| File | What it is |
|---|---|
| `index.html` | The published page. Generated, so don't edit it by hand. |
| `build.py` | Holds the content and writes `index.html`. |
| `style.css`, `app.js` | Styles and behaviour, inlined into the page by `build.py`. |
| `make_assets.py` | Makes `og.png` (the link preview card) and `resume.pdf` (the page's print layout). |
| `tests/test_site.py` | Opens the page in Chromium, Firefox and WebKit at four screen sizes, in light and dark. |

## Run it

```
pip install playwright
playwright install chromium firefox webkit
python build.py
python make_assets.py
python tests/test_site.py
```

The tests run on every push (see `.github/workflows/check.yml`). They check for console errors, sideways scroll, broken in-page links, that the name and contact links are on the first screen, and that the live data card falls back quietly when its data file can't be read.

## The live card

The "Last nightly run" card reads the first 400 bytes of a public JSON file published by BreakoutAI, a personal project, and shows the stock counts from the latest run. If the request fails it shows the last known values.
