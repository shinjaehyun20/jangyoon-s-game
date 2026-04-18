/* ========================================================================
   Ubongo - Renderer
   Canvas 2D 기반 렌더러. 보드, 배치된 조각, 드래그 중인 조각을 그린다.
   ======================================================================== */

class BoardRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.cellSize = 48;  // 동적 계산됨
    this.offsetX = 0;
    this.offsetY = 0;
    this.puzzle = null;
    this.placed = []; // [{pieceId, r, c, rotation, flipped, shape}]
    this.ghost = null; // 드래그 중 미리보기
    this.dpr = window.devicePixelRatio || 1;
  }

  setPuzzle(puzzle) {
    this.puzzle = puzzle;
    this.placed = [];
    this.resize();
  }

  setPlaced(placed) { this.placed = placed; }
  setGhost(ghost) { this.ghost = ghost; this.draw(); }

  resize() {
    if (!this.puzzle) return;
    const W = this.puzzle.shape[0].length;
    const H = this.puzzle.shape.length;
    // 캔버스 실제 크기를 CSS 크기에 맞춤
    const rect = this.canvas.getBoundingClientRect();
    const cssW = rect.width;
    const cssH = rect.height;
    this.canvas.width = cssW * this.dpr;
    this.canvas.height = cssH * this.dpr;
    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);

    // 셀 크기 = min(캔버스폭/W, 캔버스높이/H) × 0.9
    const maxCell = Math.min(cssW / (W + 1), cssH / (H + 1));
    this.cellSize = Math.floor(maxCell);
    this.offsetX = (cssW - this.cellSize * W) / 2;
    this.offsetY = (cssH - this.cellSize * H) / 2;
    this.draw();
  }

  // 보드 좌표 (r, c) → 캔버스 픽셀 좌표 (x, y)
  cellToPx(r, c) {
    return {
      x: this.offsetX + c * this.cellSize,
      y: this.offsetY + r * this.cellSize
    };
  }

  // 캔버스 픽셀 좌표 → 보드 셀 (가까운 셀). 바깥이면 음수 반환.
  pxToCell(x, y) {
    const c = Math.floor((x - this.offsetX) / this.cellSize);
    const r = Math.floor((y - this.offsetY) / this.cellSize);
    return { r, c };
  }

  draw() {
    const ctx = this.ctx;
    const rect = this.canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);
    if (!this.puzzle) return;

    const shape = this.puzzle.shape;
    const H = shape.length, W = shape[0].length;
    const cs = this.cellSize;

    // 1. 타겟 모양 (빈 슬롯 = 밝은 회색 홈)
    for (let r = 0; r < H; r++) {
      for (let c = 0; c < W; c++) {
        if (!shape[r][c]) continue;
        const { x, y } = this.cellToPx(r, c);
        // 배경 음각 효과
        ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
        ctx.fillRect(x + 2, y + 2, cs - 4, cs - 4);
        // 점선 테두리
        ctx.strokeStyle = 'rgba(234, 212, 160, 0.25)';
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 3]);
        ctx.strokeRect(x + 2, y + 2, cs - 4, cs - 4);
        ctx.setLineDash([]);
      }
    }

    // 2. 배치된 조각
    for (const piece of this.placed) {
      this.drawPiece(piece, 1.0);
    }

    // 3. 드래그 중인 고스트
    if (this.ghost) {
      this.drawPiece(this.ghost, this.ghost.valid ? 0.85 : 0.45,
                     this.ghost.valid ? null : '#ef4444');
    }
  }

  drawPiece(piece, alpha = 1.0, overrideColor = null) {
    const ctx = this.ctx;
    const cs = this.cellSize;
    const color = overrideColor || PIECES[piece.pieceId].color;
    const shape = piece.shape;
    ctx.save();
    ctx.globalAlpha = alpha;

    for (let r = 0; r < shape.length; r++) {
      for (let c = 0; c < shape[r].length; c++) {
        if (!shape[r][c]) continue;
        const { x, y } = this.cellToPx(piece.r + r, piece.c + c);
        // 셀 본체 — 그라디언트
        const grad = ctx.createLinearGradient(x, y, x, y + cs);
        grad.addColorStop(0, this.lighten(color, 0.15));
        grad.addColorStop(1, this.darken(color, 0.1));
        ctx.fillStyle = grad;
        ctx.fillRect(x + 1, y + 1, cs - 2, cs - 2);

        // 하이라이트
        ctx.fillStyle = 'rgba(255, 255, 255, 0.18)';
        ctx.fillRect(x + 2, y + 2, cs - 4, 2);

        // 경계선
        ctx.strokeStyle = this.darken(color, 0.3);
        ctx.lineWidth = 1;
        ctx.strokeRect(x + 1.5, y + 1.5, cs - 3, cs - 3);
      }
    }
    ctx.restore();
  }

  lighten(hex, amt) {
    const { r, g, b } = this.hex2rgb(hex);
    return `rgb(${Math.min(255, r + 255 * amt)}, ${Math.min(255, g + 255 * amt)}, ${Math.min(255, b + 255 * amt)})`;
  }
  darken(hex, amt) {
    const { r, g, b } = this.hex2rgb(hex);
    return `rgb(${Math.max(0, r - 255 * amt)}, ${Math.max(0, g - 255 * amt)}, ${Math.max(0, b - 255 * amt)})`;
  }
  hex2rgb(hex) {
    const m = hex.replace('#', '');
    return {
      r: parseInt(m.substring(0, 2), 16),
      g: parseInt(m.substring(2, 4), 16),
      b: parseInt(m.substring(4, 6), 16)
    };
  }
}

/* ------------------------------------------------------------------------
   타일 트레이 렌더러 (조각 팔레트 영역)
   각 조각을 개별 <canvas>로 그려서 DOM에 배치
   ------------------------------------------------------------------------ */
function renderTrayPiece(canvas, pieceId, rotation, flipped, selected) {
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const piece = PIECES[pieceId];
  const shape = PieceUtils.transform(piece.shape, rotation, flipped);
  const H = shape.length, W = shape[0].length;

  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, rect.width, rect.height);

  const maxCell = Math.min(rect.width / (W + 0.4), rect.height / (H + 0.4));
  const cs = Math.floor(maxCell);
  const offX = (rect.width - cs * W) / 2;
  const offY = (rect.height - cs * H) / 2;

  const color = piece.color;
  for (let r = 0; r < H; r++) {
    for (let c = 0; c < W; c++) {
      if (!shape[r][c]) continue;
      const x = offX + c * cs;
      const y = offY + r * cs;
      const grad = ctx.createLinearGradient(x, y, x, y + cs);
      grad.addColorStop(0, shade(color, 0.15));
      grad.addColorStop(1, shade(color, -0.1));
      ctx.fillStyle = grad;
      ctx.fillRect(x + 1, y + 1, cs - 2, cs - 2);
      ctx.fillStyle = 'rgba(255, 255, 255, 0.18)';
      ctx.fillRect(x + 2, y + 2, cs - 4, 2);
      ctx.strokeStyle = shade(color, -0.3);
      ctx.lineWidth = 1;
      ctx.strokeRect(x + 1.5, y + 1.5, cs - 3, cs - 3);
    }
  }

  if (selected) {
    ctx.strokeStyle = '#eab308';
    ctx.lineWidth = 2;
    ctx.strokeRect(1, 1, rect.width - 2, rect.height - 2);
  }
}

function shade(hex, amt) {
  const m = hex.replace('#', '');
  const r = parseInt(m.substring(0, 2), 16);
  const g = parseInt(m.substring(2, 4), 16);
  const b = parseInt(m.substring(4, 6), 16);
  const adj = (v) => Math.max(0, Math.min(255, v + 255 * amt));
  return `rgb(${adj(r)}, ${adj(g)}, ${adj(b)})`;
}

if (typeof window !== 'undefined') {
  window.BoardRenderer = BoardRenderer;
  window.renderTrayPiece = renderTrayPiece;
}
