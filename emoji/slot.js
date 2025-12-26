(() => {
  const SYMBOLS = ["🍎","🍌","🍇","🍓","🍍","🥝","🍒","🍑","🍉","🍊","🍐","🍋"];
  const REEL_COUNT = 5;
  const ROWS = 5;
  const CENTER_ROW = 2;
  const REPEAT = 70;

  const $reels = document.getElementById("reels");
  const $reelsWrap = document.getElementById("reelsWrap");
  const $score = document.getElementById("score");
  const $gain  = document.getElementById("gain");
  const $spins = document.getElementById("spins");
  const $msg   = document.getElementById("msg");
  const $btnSpin = document.getElementById("btnSpin");
  const $btnReset = document.getElementById("btnReset");

  const mod = (x, m) => ((x % m) + m) % m;
  const clamp01 = (x) => Math.max(0, Math.min(1, x));
  const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
  const rnd = (n) => Math.floor(Math.random() * n);

  const state = {
    score: 0,
    lastGain: 0,
    spins: 0,
    resultIdx: Array(REEL_COUNT).fill(0),
    spinning: false
  };

  const reels = [];

  function setMsg(text, mood=""){
    $msg.textContent = text;
    $msg.className = "msg" + (mood ? (" " + mood) : "");
  }

  function renderHUD(){
    $score.textContent = String(state.score);
    $gain.textContent  = String(state.lastGain);
    $spins.textContent = String(state.spins);
  }

  // ✅ 版型核心：用 reelsWrap 的可用寬高算出最適合的 symbol 尺寸，讓 5×3 盡量撐滿
  function computeBestSymbolPx(){
    const rect = $reelsWrap.getBoundingClientRect();
    const styles = getComputedStyle(document.documentElement);
    const gap = parseFloat(styles.getPropertyValue("--gap")) || 10;

    const usableW = rect.width  - gap * (REEL_COUNT - 1);
    const usableH = rect.height; // 高度全部留給 3 rows

    const symByW = usableW / REEL_COUNT; // 每輪寬度
    const symByH = usableH / ROWS;       // 每列高度

    // 取較小者，確保不爆版；再做合理 clamp
    const sym = Math.floor(Math.max(34, Math.min(92, Math.min(symByW, symByH))));
    return sym;
  }

  function setSymbolPx(px){
    document.documentElement.style.setProperty("--symbol", `${px}px`);
  }

  function symbolSize(){
    const v = getComputedStyle(document.documentElement).getPropertyValue("--symbol").trim();
    return parseFloat(v.replace("px","")) || 64;
  }

  function stripHeightPx(){
    const h = symbolSize();
    return SYMBOLS.length * REPEAT * h;
  }

  function updateTransform(reel){
    const H = stripHeightPx();
    const y = mod(reel.offsetPx, H);
    reel.stripEl.style.transform = `translateY(${-y}px)`;
  }

  function buildReels(){
    $reels.innerHTML = "";
    reels.length = 0;

    // ✅ 每個 reel 的高度要等於 reelsWrap 的高度（grid 會撐滿）
    for (let i=0; i<REEL_COUNT; i++){
      const reelEl = document.createElement("div");
      reelEl.className = "reel";

      const stripEl = document.createElement("div");
      stripEl.className = "strip";

      for (let r=0; r<REPEAT; r++){
        for (const s of SYMBOLS){
          const cell = document.createElement("div");
          cell.className = "sym";
          cell.textContent = s;
          stripEl.appendChild(cell);
        }
      }

      reelEl.appendChild(stripEl);
      $reels.appendChild(reelEl);

      reels.push({
        stripEl,
        offsetPx: 0,
        running: false,
        startOffsetPx: 0,
        targetOffsetPx: 0,
        startTime: 0,
        duration: 0
      });

      updateTransform(reels[i]);
    }
  }

  function computeTravelPx(startOffsetPx, targetSymbolIdx, loops){
    const N = SYMBOLS.length;
    const h = symbolSize();

    const startSteps = Math.round(startOffsetPx / h);
    const curMod = mod(startSteps, N);

    const wantOffsetMod = mod(targetSymbolIdx - CENTER_ROW, N);
    const deltaMod = mod(wantOffsetMod - curMod, N);

    const steps = loops * N + deltaMod;
    return steps * h;
  }

  function finishSpin(){
    const paylineSyms = state.resultIdx.map(i => SYMBOLS[i]);

    const freq = new Map();
    for (const s of paylineSyms) freq.set(s, (freq.get(s)||0)+1);
    let best = 1;
    for (const v of freq.values()) best = Math.max(best, v);

    let gain = 0;
    if (best === 5) gain = 500;
    else if (best === 4) gain = 200;
    else if (best === 3) gain = 60;
    else if (best === 2) gain = 10;

    state.lastGain = gain;
    state.score += gain;
    state.spins += 1;

    renderHUD();
    setMsg(
      gain > 0
        ? `✅ 停輪！最大 ${best} 連：+${gain}（${paylineSyms.join(" ")})`
        : `停輪～再來一次！（${paylineSyms.join(" ")})`,
      gain > 0 ? "good" : ""
    );

    state.spinning = false;
    $btnSpin.disabled = false;
  }

  function tick(t){
    let allDone = true;

    for (const reel of reels){
      if (!reel.running) continue;

      if (t < reel.startTime){
        allDone = false;
        continue;
      }

      const tt = clamp01((t - reel.startTime) / reel.duration);
      const eased = easeOutCubic(tt);

      reel.offsetPx = reel.startOffsetPx + (reel.targetOffsetPx - reel.startOffsetPx) * eased;
      updateTransform(reel);

      if (tt >= 1){
        const h = symbolSize();
        reel.offsetPx = Math.round(reel.offsetPx / h) * h;
        reel.offsetPx = mod(reel.offsetPx, stripHeightPx());
        updateTransform(reel);
        reel.running = false;
      } else {
        allDone = false;
      }
    }

    if (!allDone){
      requestAnimationFrame(tick);
      return;
    }

    finishSpin();
  }

  function spin(){
    if (state.spinning) return;
    state.spinning = true;
    $btnSpin.disabled = true;
    setMsg("轉輪中…");

    const now = performance.now();
    const baseDelay = 90;

    for (let i=0; i<REEL_COUNT; i++){
      const reel = reels[i];
      reel.running = true;
      reel.startOffsetPx = reel.offsetPx;

      const targetIdx = rnd(SYMBOLS.length);
      state.resultIdx[i] = targetIdx;

      const loops = 10 + i*3 + rnd(3);
      const travel = computeTravelPx(reel.startOffsetPx, targetIdx, loops);

      reel.targetOffsetPx = reel.startOffsetPx + travel;
      reel.duration = 900 + i*260 + rnd(160);
      reel.startTime = now + i * baseDelay;
    }

    requestAnimationFrame(tick);
  }

  function resetGame(){
    if (state.spinning) return;
    state.score = 0;
    state.lastGain = 0;
    state.spins = 0;
    state.resultIdx = Array(REEL_COUNT).fill(0);

    for (const r of reels){
      r.offsetPx = 0;
      r.running = false;
      updateTransform(r);
    }

    renderHUD();
    setMsg("已重置。按 A / Start 轉輪。");
  }

  // ✅ 版型重新計算：縮放時把 symbol 重新算一次並 rebuild（確保永遠撐滿）
  let lastSymbol = 0;
  function relayout(){
    const sym = computeBestSymbolPx();
    if (sym !== lastSymbol){
      lastSymbol = sym;
      setSymbolPx(sym);
      buildReels(); // 直接重建，確保每格高度一致、動畫不漂
    }
  }

  // Inputs
  document.addEventListener("keydown", (e) => {
    const k = (e.key || "").toLowerCase();
    if (k === "a" || e.key === " " || e.key === "enter") {
      e.preventDefault();
      spin();
    } else if (k === "b") {
      e.preventDefault();
      resetGame();
    }
  });
  $btnSpin.addEventListener("click", spin);
  $btnReset.addEventListener("click", resetGame);

  // Boot
  renderHUD();
  relayout();

  // Resize observe
  const ro = new ResizeObserver(() => relayout());
  ro.observe($reelsWrap);
})();
