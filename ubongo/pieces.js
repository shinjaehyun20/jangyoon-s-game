/* ========================================================================
   Ubongo - Polyomino Pieces
   12개 표준 폴리오미노 타일 정의. 원작 Ubongo Classic 세트를 참고해
   2~5칸으로 구성된 고유 조각 12종을 선정.
   각 매트릭스는 [row][col] 형태이며 1=채움, 0=빈칸.
   ======================================================================== */

const PIECES = {
  // 4칸 (테트로미노)
  P1: { // 정사각형 (O)
    color: '#f59e0b',
    shape: [
      [1, 1],
      [1, 1]
    ]
  },
  P2: { // I 테트로미노
    color: '#60a5fa',
    shape: [
      [1, 1, 1, 1]
    ]
  },
  P3: { // L 테트로미노
    color: '#34d399',
    shape: [
      [1, 0],
      [1, 0],
      [1, 1]
    ]
  },
  P4: { // T 테트로미노
    color: '#f472b6',
    shape: [
      [1, 1, 1],
      [0, 1, 0]
    ]
  },
  P5: { // S 테트로미노
    color: '#a78bfa',
    shape: [
      [0, 1, 1],
      [1, 1, 0]
    ]
  },
  P6: { // J 테트로미노
    color: '#fb923c',
    shape: [
      [0, 1],
      [0, 1],
      [1, 1]
    ]
  },

  // 5칸 (펜토미노)
  P7: { // L 펜토미노
    color: '#fbbf24',
    shape: [
      [1, 0],
      [1, 0],
      [1, 0],
      [1, 1]
    ]
  },
  P8: { // P 펜토미노
    color: '#22d3ee',
    shape: [
      [1, 1],
      [1, 1],
      [1, 0]
    ]
  },
  P9: { // Y 펜토미노
    color: '#c084fc',
    shape: [
      [0, 1],
      [1, 1],
      [0, 1],
      [0, 1]
    ]
  },
  P10: { // N 펜토미노
    color: '#f87171',
    shape: [
      [0, 1],
      [1, 1],
      [1, 0],
      [1, 0]
    ]
  },
  P11: { // Z 펜토미노
    color: '#4ade80',
    shape: [
      [1, 1, 0],
      [0, 1, 0],
      [0, 1, 1]
    ]
  },
  P12: { // + (Plus) 펜토미노
    color: '#fb7185',
    shape: [
      [0, 1, 0],
      [1, 1, 1],
      [0, 1, 0]
    ]
  }
};

/* ------------------------------------------------------------------------
   매트릭스 변환 유틸
   ------------------------------------------------------------------------ */

// 90도 시계방향 회전
function rotateCW(mat) {
  const rows = mat.length;
  const cols = mat[0].length;
  const out = Array.from({ length: cols }, () => Array(rows).fill(0));
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      out[c][rows - 1 - r] = mat[r][c];
    }
  }
  return out;
}

// 좌우 반전
function flipH(mat) {
  return mat.map(row => [...row].reverse());
}

// 회전 횟수(0~3)와 반전 여부를 적용
function transform(shape, rotation, flipped) {
  let m = shape.map(r => [...r]);
  if (flipped) m = flipH(m);
  for (let i = 0; i < (rotation % 4 + 4) % 4; i++) m = rotateCW(m);
  return m;
}

// 모든 고유 orientation 생성 (중복 제거)
function allOrientations(shape) {
  const seen = new Set();
  const out = [];
  for (let f = 0; f < 2; f++) {
    for (let r = 0; r < 4; r++) {
      const m = transform(shape, r, f === 1);
      const key = JSON.stringify(m);
      if (!seen.has(key)) {
        seen.add(key);
        out.push({ rotation: r, flipped: f === 1, shape: m });
      }
    }
  }
  return out;
}

// 채워진 셀의 좌표 목록 반환
function cellsOf(shape) {
  const cells = [];
  for (let r = 0; r < shape.length; r++) {
    for (let c = 0; c < shape[r].length; c++) {
      if (shape[r][c]) cells.push([r, c]);
    }
  }
  return cells;
}

// 브라우저 전역으로 노출
if (typeof window !== 'undefined') {
  window.PIECES = PIECES;
  window.PieceUtils = { rotateCW, flipH, transform, allOrientations, cellsOf };
}
