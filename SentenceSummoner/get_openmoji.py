import re, os, urllib.request
JS = r"D:\strategy-space\ip\yanchu-fasui\yanchu-deck.js"
DST = r"D:\strategy-space\ip\yanchu-fasui\openmoji"
os.makedirs(DST, exist_ok=True)
emojis = set(re.findall(r'e:"([^"]+)"', open(JS, encoding="utf-8").read()))
emojis |= {"❤️","🗡️","🛡️","🦶"}   # 四維 icon 也換
def code(em): return "-".join(f"{ord(c):X}" for c in em if ord(c) != 0xFE0F)
base = "https://cdn.jsdelivr.net/gh/hfg-gmuend/openmoji@master/color/svg/"
ok, miss = [], []
for em in sorted(emojis):
    cp = code(em); url = base + cp + ".svg"; dst = os.path.join(DST, cp + ".svg")
    try:
        urllib.request.urlretrieve(url, dst)
        if os.path.getsize(dst) < 200: raise Exception("too small")
        ok.append(f"{em}->{cp}")
    except Exception as ex:
        miss.append(f"{em}->{cp}  {str(ex)[:40]}")
print("OK", len(ok), "/ total", len(emojis))
print("MISS", len(miss))
for m in miss: print("  ", m)
