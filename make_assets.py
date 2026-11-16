"""Makes og.png (the link preview card) and resume.pdf (the page's print layout) from index.html.
Usage: python make_assets.py [og] [resume]      (no argument = both; run build.py first)"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).resolve().parent

OG = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box;margin:0}body{width:1200px;height:630px;background:#f3f1eb;color:#111110;font-family:Archivo,sans-serif;padding:54px 60px 46px;display:flex;flex-direction:column}
h1{font-stretch:68%;font-weight:800;text-transform:uppercase;font-size:106px;line-height:.9;letter-spacing:-.012em;text-wrap:balance}h1 span{color:#1f3fff}
.b{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;border-top:3px solid #111110;padding-top:20px}
.n b{display:block;font-size:30px;font-weight:700}.n span{font-size:22px;color:#55534d}
.s{display:flex;gap:34px;font-stretch:68%;font-weight:800;font-size:44px;text-transform:uppercase;line-height:1}.s i{font-style:normal;color:#1f3fff}.s s{color:#a9a59b}</style></head>
<body><h1>Six years of making sure the number in the meeting is <span>the right one.</span></h1>
<div class="b"><div class="n"><b>Bhavan Mehta</b><span>Senior Data Engineer, Finance Data Engineering</span></div>
<div class="s"><span><s>25</s> <i>1</i></span><span><s>3 h</s> <i>30 min</i></span><span>50+</span><span>200+</span></div></div></body></html>"""

async def main(what):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if "og" in what:
            pg = await b.new_page(viewport={"width": 1200, "height": 630})
            await pg.set_content(OG); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=str(HERE / "og.png")); print("og.png", (HERE / "og.png").stat().st_size // 1024, "KB")
        if "resume" in what:
            pg = await b.new_page(viewport={"width": 1100, "height": 1400})
            await pg.goto((HERE / "index.html").as_uri()); await pg.wait_for_timeout(1500)
            await pg.emulate_media(media="print")
            await pg.pdf(path=str(HERE / "resume.pdf"), format="Letter", print_background=False, prefer_css_page_size=False,
                         margin={"top": "12mm", "bottom": "12mm", "left": "13mm", "right": "13mm"})
            print("resume.pdf", (HERE / "resume.pdf").stat().st_size // 1024, "KB")
        await b.close()
asyncio.run(main(sys.argv[1:] or ["og", "resume"]))
