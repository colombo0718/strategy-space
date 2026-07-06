# 造物森林 × RL：類魂作為強化學習逆風局 benchmark

> 2026-05-27 colombo 提出的洞察：類魂遊戲在 RL 領域是大命題、剛好對應造物森林。
> 本檔留作未來 RR 教學 / colombo 學術論文 / 公開 benchmark 的設計藍圖。

---

## 一、學術命題

> 「類魂遊戲在 RL 領域也是一個大命題。當原始 RL 不只是稀疏、而且還是多為懲罰、RL 系統面對這樣的逆風局該如何應對？」

→ **類魂 = sparse-reward + frequent-penalty + risk-return + skill ceiling 高**。
→ 這個組合是主流 benchmark 的盲區、未被學術界正式 benchmark。

## 二、為什麼類魂正好填這個盲區

| Benchmark | Reward 結構 | 跟真實世界距離 |
|---|---|---|
| Atari | dense、頻繁正向 | 遠 |
| MuJoCo | continuous dense | 中 |
| 圍棋 / Chess | binary outcome、終局才知 | 遠 |
| NetHack | sparse + retry-on-death | 中 |
| Crafter | sparse + open-ended | 中 |
| **造物森林（類魂）** | **稀疏正向 + 頻繁負向 + 死亡懲罰 + risk-return** | **近**（接近真實人類學習新技能 / 創業 / 做研究的體感）|

→ **造物森林之於 RL benchmark = NetHack 的進階版**、加上「**risk-return**」（死亡會掉撿來的垃圾、可重新撿）。

## 三、學術界處理稀疏 + 懲罰逆風局的既有招式

每招都可在造物森林設計出對應 mechanic 來訓練學生：

| 招式 | 學術引用 | 在造物森林的對位 |
|---|---|---|
| **Reward Shaping** | Ng et al. 1999 | 撿垃圾 = 小 reward、組裝武器 = 中 reward、打 boss = 大 reward、避開毒區 = 微 reward |
| **Curiosity-Driven** | ICM（Pathak 2017）/ RND（Burda 2018）| 探索新棲地、發現新物件 = intrinsic reward |
| **HER**（Hindsight Experience Replay）| OpenAI 2017 | 死了沒打贏 boss、但「逃離成功 5 步」可改寫成另個目標學 |
| **GAIL / Inverse RL** | Ho & Ermon 2016 | 玩家通關紀錄 → 訓練 NPC 隊友 / boss |
| **RLHF** | OpenAI / Anthropic | 戰鬥優雅度 / 創意度評分、玩家偏好替 reward |
| **Curriculum Learning** | Bengio 2009 | 三階 boss 進化（新手村蛇 → 中階狐 → 文明）= 天然 curriculum |
| **Distributional RL** | C51（Bellemare 2017）| 風險敏感：死了損失分布的學習 |
| **PER**（Prioritized Experience Replay）| Schaul 2015 | 死亡 trajectory 加權重學 |

→ **每一條都可以對應造物森林某個關卡或機制**、整個遊戲設計上就是 RL 進階技術活教材。

## 四、跟 RR 強化教室的對接

```
RR progression（推測 / 待跟 Edutainment 協理確認）：
  Lv1 dense reward 環境（cart pole / 走迷宮 / grid world）
  Lv2 continuous control（MuJoCo 類）
  Lv3 sparse reward 環境（圍棋 / Atari 後期）
  ─────────────────────────────────
  Lv4 ← **造物森林**：sparse + frequent penalty + risk-return
        學生在這層學 reward shaping / HER / curiosity / curriculum
        感受「逆風局」的 RL 是什麼樣
  Lv5 RLHF / human-in-the-loop
  Lv6 multi-agent（造物森林 5 角色團隊 RL？）
```

→ **造物森林剛好填 Lv4 進階場景**、且**有故事性 + 角色 IP**、不只是抽象環境。
→ 學生會記得「**那次教 reward shaping 的時候、是樹蛙撿瓶蓋的關**」、比講 grid world 印象深。

## 五、可能的學術發表角度

| 角度 | 標題粗胚 |
|---|---|
| 環境貢獻 | **Souls-Forge: A Souls-Like Environment for Sparse-Reward Risk-Return RL** |
| 教學貢獻 | **Using Souls-Like Game Mechanics to Teach Advanced RL Techniques** |
| 跨域貢獻 | **Environmental Narrative as Reward Signal: A Game-Based RL Curriculum** |
| 應用貢獻 | **多綱生物食物鏈作為 multi-agent RL 的 ecological benchmark** |

→ 不用立刻寫、留個技術文件記錄、未來 RR 教學或 colombo 自己學術 second paper 可用。

## 六、實作技術選擇（未來真要動工才定）

| 層 | 選項 |
|---|---|
| 遊戲引擎 | Godot（開源、輕、適合 voxel）/ Unity（成熟、學術界用得多）/ web（Three.js + voxel）|
| RL framework | Stable Baselines 3 / RLlib / PettingZoo（multi-agent）|
| 環境介面 | OpenAI Gym API（最通用）|
| 視覺資產重建 | MagicaVoxel / Goxel（5 年前檔案已失、要重做）|
| 文檔 | OpenAI Gym style + 範例 notebook |

## 七、跟 LL 既有 4 階梯任務成熟戰略對齊

```
LL 4 階梯（meeting 2026-05-22）：
  第 1 階：未知領域、開疆拓土 — 強 Agent
  第 2 階：略明確路徑、有 MCP — 中弱 Agent
  第 3 階：明確流程 — 通用 LLM
  第 4 階：純機械 — 腳本

對應造物森林作為 RL 教學的觀察：
  類魂玩家也走類似階梯：
    新手期 = 第 1 階（沒地圖、亂闖）
    熟悉期 = 第 2 階（學會基本套路）
    精通期 = 第 3 階（無腦推圖）
    速通期 = 第 4 階（rule-based 操作）
```

→ **類魂玩家學習曲線 = RL agent 學習曲線**——這個對位本身就是學術觀察。

## 八、現況 + 觸發條件

**現況**（2026-05-27）：
- 設定齊備、學術命題定型
- 沒實作、沒環境程式碼
- 純設計文件、等觸發

**啟動觸發條件**：
- RR Edutainment 協理需要 Lv4 進階教學場景
- colombo 學術論文 second paper 找題目
- 外部研究合作邀請（學界主動接觸）
- LL agent runtime 成熟、AA 協理願 spawn 此 vertical

**不啟動的時候做什麼**：
- 設計持續累積（角色 / boss / mechanic 補完）
- RR 教學談到 sparse-reward 時 cross-reference 本檔
- 偶爾看一眼業界有沒有人搶先做（NetHack benchmark 進展？）

---

## 九、結語

造物森林如果只是遊戲、值得做。
造物森林如果同時是 RL benchmark、**值得寫 paper**。
造物森林如果整套接 RR 教學 + 勁園教育 vertical、**是 LL AI 服務架構廠商的旗艦案例**。

但現在不動、種子先種、文件先收。
