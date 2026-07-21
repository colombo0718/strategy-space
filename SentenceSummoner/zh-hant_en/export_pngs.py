from playwright.sync_api import sync_playwright
import pathlib, os
url = pathlib.Path(r'D:/strategy-space/SentenceSummoner/zh-hant_en/deck.html').as_uri()
outdir = r'D:\strategy-space\SentenceSummoner\zh-hant_en\cards'
os.makedirs(outdir, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page(viewport={'width':1380,'height':900}, device_scale_factor=4)
    p.goto(url); p.wait_for_timeout(800)
    p.add_style_tag(content="body{background:transparent!important} .card{box-shadow:none!important}")
    p.evaluate("document.body.style.background='transparent'")
    cards = p.query_selector_all('.card')
    n = 0
    for c in cards[:64]:
        cid = c.get_attribute("data-id")           # 用編號命名 A01..A64
        c.scroll_into_view_if_needed()
        c.screenshot(path=os.path.join(outdir, f"{cid}.png"), omit_background=True)
        n += 1
    b.close()
print("exported", n, "PNGs ->", outdir)
