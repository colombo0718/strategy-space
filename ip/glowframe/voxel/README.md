# GlowFrame voxel 資產

## 現況

- **2021 年 colombo 製作的 .vox 檔案保存狀態未知**（請 colombo 確認）
- 截圖已保留（colombo 提供 2-3 張紫影初號機 voxel 視角）
- 製作工具：MagicaVoxel + BlockBench

## 已知 voxel 截圖

從 colombo 2026-05-27 分享：

1. **紫影初號機 坐姿 / 蹲姿**（手持單頭鋸刃武器）
2. **紫影初號機 站姿 + 雙端鋸刃旋斬棍**（雙手平展持武器）
3. **紫影初號機 站姿 + 雙頭武器另一視角**

→ 三張都是同一個戰甲、不同 pose / 武器配置。

## 待補

- [ ] colombo 確認原 .vox 檔案有沒有 backup
- [ ] 將 colombo 分享的截圖正式存進本資料夾（如 prototype-01.png / -02.png / -03.png）
- [ ] 其他系列戰甲（朱劍 / 青弓 / 金禪 ...）**從未製作、未來新製**

## 工具流（colombo 既有經驗）

| 工具 | 用途 | 已驗證 | 限制 |
|---|---|---|---|
| MagicaVoxel | 戰甲 voxel 本體 | ✅ | 純靜態、無動畫 |
| BlockBench | 動作 / 動畫 | ✅ | **動作不能重複利用**——每個動作從頭做、效率低 |
| Blender | 流光特效 + 動畫複用 | ⚠️ 未驗證、推測需要 | 學習曲線 |

## 未來重做選項

**選項 A：純沿用 5 年前工作流**
- MagicaVoxel + BlockBench
- 適合靜態 voxel 模型 + 簡單動作
- 不適合大量戰甲 + 複雜流光

**選項 B：升級到 Blender voxel pipeline**
- MagicaVoxel 模型導出 → Blender 加流光 + 動畫
- 動畫可以複用（解 BB 限制）
- 學習曲線中等

**選項 C：純 Blender low-poly**
- 直接用 Blender 建 voxel-like 模型
- 流光用 Blender shader / emission material
- 跟 MagicaVoxel 質感略不同

**推薦**：未來真要動工、走 **B**——保留 MagicaVoxel 美術風格、Blender 補動畫 + 流光。

## 風格定錨（重做時不要偏離）

從 2021 截圖萃取的視覺共識：

- **純黑底色**（不是深灰、不是其他色、就是黑）
- **單色光條**（純色、不混色、不漸層）
- **光條描繪輪廓 / 關節 / 武器邊緣**——不畫實心物件
- **人型比例正常**（不是 chibi、不是寫實、是 1:1 正常人型）
- **武器特化**（每副戰甲一個簽名武器、佔畫面顯著面積）

→ 這個風格定錨**比角色細節更重要**——是 GlowFrame IP 的視覺 DNA。

## 法律 / 版權

- IP 完全歸 colombo / 葉與月工作室
- voxel 重做檔案歸 SS repo
- 不引用任何商業 IP（戰甲設計、武術招式、世界觀都是 colombo 原創）
- 參考靈感（Warframe / 創 / 樂園追放）**不抄、只借美學語言**
