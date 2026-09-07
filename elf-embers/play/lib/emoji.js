// emoji.js —— OpenMoji 素材載入與 canvas 繪製（沿用 cat_volley 同款手法）
// 用法：drawEmoji(ctx, '🧝', x, y, size, { flip, rotate, alpha, dx, dy })
//   以 (x,y) 為中心畫；flip=水平翻轉、rotate=弧度、alpha=透明度、dx/dy=中心偏移
//   dx/dy 可用來把旋轉軸心從畫布中心挪到握把/箭尾等位置，不用動 SVG 本身
(function (root) {
  const BASE = 'assets/openmoji/';
  const MAP = {
    '🧝': '1F9DD.svg',   // 精靈（主角）
    '🗡️': '1F5E1.svg',   // 匕首（揮劍動畫用）
    '🏹': '1F3F9.svg',   // 弓（拉弓/箭矢動畫用）
    '🎯': '1F3AF.svg',   // 靶（遠程測試目標）
    '🗿': '1F5FF.svg',   // 摩艾石像（近戰測試假人）
    '🪵': '1FAB5.svg',   // 木樁（場景可踩物件，不可攻擊）
  };
  const images = {};
  let loaded = 0, total = 0;

  for (const [ch, file] of Object.entries(MAP)) {
    total++;
    const img = new Image();
    img.onload = () => { loaded++; };
    img.src = BASE + file;
    images[ch] = img;
  }

  function ready() { return loaded === total; }
  function src(ch) { return BASE + MAP[ch]; }

  function drawEmoji(ctx, ch, x, y, size, opts) {
    opts = opts || {};
    const img = images[ch];
    if (!img || !img.complete || img.naturalWidth === 0) return false;
    ctx.save();
    ctx.translate(x, y);
    if (opts.rotate) ctx.rotate(opts.rotate);
    if (opts.flip) ctx.scale(-1, 1);
    if (opts.alpha != null) ctx.globalAlpha = opts.alpha;
    const dx = opts.dx || 0, dy = opts.dy || 0;
    ctx.drawImage(img, -size / 2 + dx, -size / 2 + dy, size, size);
    ctx.restore();
    return true;
  }

  root.drawEmoji = drawEmoji;
  root.EMOJI_SRC = src;
  root.EMOJI_READY = ready;
})(window);
