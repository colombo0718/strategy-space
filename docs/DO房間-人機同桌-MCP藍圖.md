# DO 房間＝房號＝人機同桌：SS 對局層的傳輸藍圖

> 2026-07-12 colombo × 月衍卿。基於 MS 專案 hello-do spike（Worker+DO、已上線驗證
> `ll-hello-do.colombo0718.workers.dev`、兩分頁定向投遞零串線）。
> 關聯：`2026-07-11-LL-AI共感層`會議紀錄（note MM）、MD 對局模式、SS 演化第 4 階房間機制。

## 核心命題（colombo 拍題）

hello-do 的連線碼機制拓展到遊戲中＝**房主開的房號**；同一房間同時容納
**人類玩家（網頁 UI）**與 **Agent 玩家（MCP）**——包括任何支援 MCP 的 LLM 平台（如網頁版 Claude 的 Connectors）。

## 人機合作三場景（2026-07-12 colombo 定名、本藍圖的上位分類）

同一 DO 底座、三種方向：**教學**（AI 在上、看著你適時開口＝RR 家教）／**共編**（對等、共寫一份作品＝MS）／
**同遊**（AI 在旁、同桌玩家＝MD/大富翁/SP，BYO-AI 屬此）。
技術差異只在「共享物」與「寫入方向」；SP 玩家歷程依序走完三場景（見 SP 攻防全循環 §13）。

## 三層結構

1. **房號＝DO 名＝capability token**：`getByName(code)` 第一次呼叫房間即存在（「開房」不是動作）；
   DO 實例天然隔離＝房與房不串線（hello-do 已驗）。
2. **協定層人機對等**：房間只看到「席位 N 提交 action X」——
   ```
   人類 ─網頁UI─WebSocket─┐
                          ├→ DO 房間（權威遊戲狀態＋回合結算）
   Agent ─MCP工具─HTTP/WS─┘
   ```
   表現層用「動物=AI、人形=人」公約標席位。回合制×DO 請求排隊＝免寫鎖。
3. **MCP 端點與房間同一 Worker**：Cloudflare 有第一方 remote MCP（Agents SDK / McpAgent）。
   一個 Worker 三個門：頁面（人）、/ws（席位）、/mcp（任何 LLM 平台）。
   工具面極瘦：`join_room(code)` / `get_state()` / `submit_action(n)` / `say(text)`。
   → claude.ai 用戶加 connector 即可「join room 8218」同桌。

## 捅開的產品空間

- **自帶 AI 隊友（BYO AI）**：souls-hall＝我們供應的 AI；MCP＝玩家自己的 AI 進場的門。
  「你的 Claude 對上我的 GPT、在我們的規則裡」——市場無此物。
- **MD daemon 標準化**：claude vs codex 後台對戰的 bespoke harness → 兩個 MCP client 進同一房。
- **RR 靈寵 → SS 靈將的實體通道**：訓練好的 agent 走 MCP 進房出戰＝SS 演化第 4 階「比賽房間」。

## 工程要點（做的時候才動）

1. **引擎搬進 DO（server-authoritative）**：MCP 玩家無瀏覽器、結算不能留在前端。
   MD `resolve()` 當年即設計為純函式（MUST 規範）→ 搬家成本最低、舊決策兌現。
2. **席位令牌**：房號=入場券；入座後每席發自身 token（防搶位）＋「允許 AI 入座」opt-in
   （共感層筆記的「發現≠授權」原則照搬）。
3. 觀戰＝第三種連線（唯讀 observer）→ RR 家教模式同構。
4. 節奏適配：LLM 延遲 1-5s、只適合回合制（MUST 系全數適用；即時制不走此路）。

## 落地順序（2026-07-12 colombo 拍板）

**SP 對稱鏡像即時攻防＝BYO-AI 首發**（兩邊配置相同、同時互相攻防＝Attack-Defense CTF 賽制；
詳見 SP `docs/SP遊戲設計_攻防全循環.md` §12）→ MD 聯機（換 PeerJS）→ 大富翁四人房 → SS 賽事房間（正主）。
與 MS 共編分支（樂觀鎖）共用 Room DO 基底、動工前跟 MS 側分身對齊。
