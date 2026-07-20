# TT 領土保衛戰 — 封面 key art 出圖 prompt

> 用途：AI 生成封面 key art（狼王對村長、魔獸盒繪致敬、晝夜斜切）。
> 成品由 Gemini 出圖、已入官網 `covers/territory-trials.jpg`。
> 規格：橫版 16:9／3:2；標題由模型直接寫；prompt 用流暢敘述、忌孤立大寫詞（會被畫成雜字）。

---

## 正式 prompt（Gemini 定稿版·橫版）

```
A wide landscape early-1990s fantasy game box-art cover, painted oil
illustration in the style of the classic Warcraft: Orcs & Humans cover and
Frank Frazetta — dramatic, richly textured, cinematic chiaroscuro lighting,
epic and painterly with high detail.

Two heads in profile fill the frame, facing each other in a tense stand-off
across the center of the image, their eyes locked. They are two worthy
adversaries and equals — mutual respect and tension, and neither of them looks
evil and neither looks heroic; both are dignified.

On the left, a fierce and noble battle-scarred grey wolf king seen in profile:
intelligent piercing amber eyes, a dignified calm alpha presence, weathered fur
with a few faded old scars, breath misting faintly in the cold air — a shrewd,
commanding pack leader rather than a slavering monster. His side of the scene is
a moonlit night of deep cool blues and shadow, with a dark pine forest, a full
moon and stars behind him.

On the right, a weathered and resourceful human village chief seen in profile:
an older frontier settler with a careworn determined face, wise strategic eyes,
a short grey beard, and a simple rugged hooded cloak of a working village leader
— not a shining knight or a noble lord, but a protective, cunning elder. His
side of the scene is a warm golden dawn, with a small village of thatched roofs,
smoking chimneys and plowed farmland fields nestled in the valley below him.

Down the middle, where the two halves meet, runs the edge of the forest where
night gives way to day and the wild land meets the settled land.

Across the top, an ornate fantasy game-logo title banner reads "Territory
Trials" in bold, golden, embossed serif lettering.

The mood is survival, territory and grey morality: two leaders each defending
their own kind under the pressure of one shared land. It must not look like a
cartoon, emoji, or flat modern vector art, and there is no gore. Do not place
any other words, labels, letters or captions anywhere in the image — the only
text is the title "Territory Trials" at the top.
```

## 迭代教訓
- 舊版用大寫結構標籤（LEFT/RIGHT/NIGHT/DAWN/FOREST EDGE）→ 被模型當文字畫進圖裡；改流暢敘述後消除。
- 直式盒繪 → 改橫版 16:9（貼 itch）。
- 標題交模型直接寫 "Territory Trials"（英文最穩；中文字易糊）。

## 給 SDXL/Flux 類（若走 ComfyUI，可拆負向提示）
- Negative：`text, watermark, extra letters, gibberish text, cartoon, emoji, flat vector art, chibi, cute, gore, blood, deformed, glowing red evil eyes`
- 註：SDXL/Flux 類文字渲染多半糟（標題易糊）——這正是與 Gemini/Imagen 最可能拉開差距之處。
