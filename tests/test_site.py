"""Checks the built page in real browsers. Exits non-zero on any failure.
Usage: python tests/test_site.py [chromium] [firefox] [webkit]     (no argument = all three)
The live data request is answered by the test itself, so results do not depend on the network."""
import asyncio, re, sys
from pathlib import Path
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").as_uri()
SIZES = {"desktop": (1440, 900), "laptop": (1280, 680), "tablet": (820, 1100), "phone": (390, 844),
         "phone-desktop-mode": (980, 2176), "big-monitor": (2560, 1340)}
FAKE = '{"generated_at":"2026-01-02T03:04:05+00:00","as_of_date":"2026-01-01","source":"test","count":1234,'
fails = []

def check(ok, label):
    if not ok: fails.append(label)
    return ok

async def one(browser, name, size, theme):
    w, h = SIZES[size]; tag = f"{name}/{size}/{theme}"
    ctx = await browser.new_context(viewport={"width": w, "height": h}, color_scheme=theme)
    await ctx.route("**/gc.zgo.at/**", lambda r: r.fulfill(status=200, body="", content_type="application/javascript"))
    await ctx.route("**/raw.githubusercontent.com/**", lambda r: r.fulfill(status=206, body=FAKE, content_type="text/plain", headers={"access-control-allow-origin": "*"}))
    pg = await ctx.new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text[:140]) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)[:140]))
    await pg.goto(PAGE); await pg.wait_for_timeout(1800)
    info = await pg.evaluate(r"""() => {
      const vis = s => [...document.querySelectorAll(s)].some(a => { const r = a.getBoundingClientRect(); return r.width > 0 && r.top >= 0 && r.bottom <= innerHeight; });
      const t = document.body.innerText;
      return { title: document.title, overflow: document.documentElement.scrollWidth - innerWidth, dashes: (t.match(/[–—·]/g) || []).length,
        name: /Bhavan Mehta/i.test(t.slice(0, 600)), h1: !!document.querySelector('h1') && vis('h1'),
        links: [vis('.hero a[href="resume.pdf"]'), vis('.hero a[href*="github.com/Bhavanmehta"]'), vis('.hero a[href*="linkedin.com/in/bhavan-mehta"]'), vis('.hero a[href^="mailto:"]')],
        broken: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(x => x.length > 1 && !document.querySelector(x)),
        imgs: [...document.images].filter(i => !i.naturalWidth).length, theme: document.documentElement.getAttribute('data-theme'),
        gap: Math.round(document.querySelector('.hero .tiles').getBoundingClientRect().top - document.querySelector('.hero .id').getBoundingClientRect().bottom),
        phone: /\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}/.test(t), live: document.querySelector('#lv-us').textContent, pill: document.querySelector('#live-s').textContent };
    }""")
    check(info["title"] == "Bhavan Mehta - Senior Data Engineer", f"{tag}: title")
    check(info["overflow"] <= 0, f"{tag}: sideways scroll of {info['overflow']}px")
    check(info["dashes"] == 0, f"{tag}: {info['dashes']} en/em dashes or middle dots")
    check(info["name"] and info["h1"], f"{tag}: name and headline on the first screen")
    check(all(info["links"]), f"{tag}: hero links on the first screen {info['links']}")
    check(not info["broken"], f"{tag}: broken in-page links {info['broken']}")
    check(info["imgs"] == 0, f"{tag}: {info['imgs']} images failed to load")
    check(info["theme"] == theme, f"{tag}: theme follows the system setting")
    check(info["gap"] <= 160, f"{tag}: {info['gap']}px of empty space between the intro and the number tiles")
    check(not info["phone"], f"{tag}: a phone number is on the page")
    check(info["live"] == "1,234" and info["pill"] == "Live", f"{tag}: live card shows fetched data ({info['live']}, {info['pill']})")
    if size == "desktop":
        # data flow: clicking a stage shows exactly its panel
        await pg.locator("#st4").scroll_into_view_if_needed(); await pg.click("#st4"); await pg.wait_for_timeout(200)
        shown = await pg.evaluate("[...document.querySelectorAll('.pn')].filter(p => !p.hidden).map(p => p.id)")
        check(shown == ["pn4"], f"{tag}: data flow shows the clicked stage {shown}")
        # the night it broke / now
        await pg.locator("#night").scroll_into_view_if_needed(); await pg.click('#night .tog button[data-s="now"]')
        check(await pg.locator("#night .now").first.is_visible() and not await pg.locator("#night .then").first.is_visible(), f"{tag}: incident switch")
        # theme button
        await pg.evaluate("scrollTo(0,0)"); await pg.click("#theme")
        check(await pg.evaluate("document.documentElement.getAttribute('data-theme')") != theme, f"{tag}: theme button")
        # command menu: open, filter, run, close
        await pg.keyboard.press("Control+k"); check(await pg.locator("#pal").is_visible(), f"{tag}: command menu opens")
        await pg.keyboard.type("contact"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(300)
        check(not await pg.locator("#pal").is_visible() and (await pg.evaluate("location.hash")) == "#contact", f"{tag}: command menu runs a command")
    check(not errs, f"{tag}: console errors {errs[:2]}")
    await ctx.close()

async def offline(browser, name):
    """With the data file unreachable, the card must fall back quietly."""
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
    await ctx.route("**/raw.githubusercontent.com/**", lambda r: r.fulfill(status=200, body="not json", content_type="text/plain", headers={"access-control-allow-origin": "*"}))
    pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:140]))
    await pg.goto(PAGE); await pg.wait_for_timeout(1500)
    check(await pg.locator("#live-s").text_content() == "Last known run" and not errs, f"{name}: fallback when the data file can't be read {errs[:1]}")
    await ctx.close()

async def main(names):
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    check(len(html.encode()) < 400_000, "page is over 400 KB")
    check(not re.search(r"lorem ipsum", html, re.I), "placeholder text")
    async with async_playwright() as p:
        for name in names:
            browser = await getattr(p, name).launch(); n0 = len(fails)
            for size in SIZES:
                for theme in ("light", "dark"): await one(browser, name, size, theme)
            await offline(browser, name); await browser.close()
            print(f"{name:<9} {'PASS' if len(fails) == n0 else 'FAIL'}  ({len(SIZES) * 2 + 1} runs)")
    for f in fails: print("  FAIL", f)
    sys.exit(1 if fails else 0)

asyncio.run(main(sys.argv[1:] or ["chromium", "firefox", "webkit"]))
