/* ========================================================================
   Ubongo - Main Game Logic
   ======================================================================== */

const GameConfig = {
  ROUNDS: 9,
  TIME_EASY: 60,
  TIME_HARD: 90,
  GEM_POINTS: { red: 4, blue: 3, green: 2, brown: 1 }
};

class UbongoGame {
  constructor() {
    this.state = {
      round: 0,
      difficulty: 'easy',
      timeLeft: 0,
      puzzle: null,
      placed: [],       // [{pieceId, r, c, rotation, flipped, shape}]
      availablePieces: [], // 이 라운드에 사용해야 할 조각 ID들
      selectedPieceId: null,
      selectedRotation: 0,
      selectedFlipped: false,
      gems: { red: 0, blue: 0, green: 0, brown: 0 },
      score: 0,
      solvedRounds: 0,
      timer: null,
      inProgress: false
    };

    this.boardCanvas = document.getElementById('boardCanvas');
    this.renderer = new BoardRenderer(this.boardCanvas);

    this.dragState = null; // { pieceId, rotation, flipped, pointerId, offsetR, offsetC }

    this._bindUI();
    this._bindInput();
    window.addEventListener('resize', () => {
      this.renderer.resize();
      this._renderTray();
    });
  }

  /* -------------------- UI 바인딩 -------------------- */
  _bindUI() {
    document.getElementById('startBtn').addEventListener('click', () => this.startGame());
    document.getElementById('restartBtn').addEventListener('click', () => this.startGame());
    document.getElementById('nextRoundBtn').addEventListener('click', () => this.nextRound());
    document.getElementById('skipBtn').addEventListener('click', () => this.skipRound());
    document.querySelectorAll('.diff-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.state.difficulty = btn.dataset.diff;
      });
    });

    // 모바일 컨트롤
    document.getElementById('rotateBtn').addEventListener('click', () => this._rotateSelected());
    document.getElementById('flipBtn').addEventListener('click', () => this._flipSelected());
    document.getElementById('returnBtn').addEventListener('click', () => this._returnSelected());
  }

  _bindInput() {
    // 키보드 (데스크톱)
    window.addEventListener('keydown', (e) => {
      if (!this.state.inProgress) return;
      if (e.key === 'r' || e.key === 'R') this._rotateSelected();
      else if (e.key === 'f' || e.key === 'F') this._flipSelected();
      else if (e.key === 'Escape') this._returnSelected();
    });

    // 트레이에서 조각 선택 및 드래그 시작
    const tray = document.getElementById('trayArea');
    tray.addEventListener('pointerdown', (e) => this._onTrayPointerDown(e));

    // 보드에서 드래그 진행 및 종료
    this.boardCanvas.addEventListener('pointerdown', (e) => this._onBoardPointerDown(e));
    window.addEventListener('pointermove', (e) => this._onPointerMove(e));
    window.addEventListener('pointerup', (e) => this._onPointerUp(e));
    window.addEventListener('pointercancel', (e) => this._onPointerUp(e));

    // 스크롤/줌 방지 (모바일)
    this.boardCanvas.addEventListener('touchstart', (e) => e.preventDefault(), { passive: false });
    this.boardCanvas.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });
    tray.addEventListener('touchmove', (e) => {
      // 트레이 내부는 스크롤 허용하되, 드래그 중에는 차단
      if (this.dragState) e.preventDefault();
    }, { passive: false });
  }

  /* -------------------- 게임 플로우 -------------------- */
  startGame() {
    this.state.round = 0;
    this.state.gems = { red: 0, blue: 0, green: 0, brown: 0 };
    this.state.score = 0;
    this.state.solvedRounds = 0;
    document.getElementById('introScreen').classList.add('hidden');
    document.getElementById('endScreen').classList.add('hidden');
    document.getElementById('gameScreen').classList.remove('hidden');
    this.nextRound();
  }

  nextRound() {
    document.getElementById('roundEndModal').classList.add('hidden');
    this.state.round++;
    if (this.state.round > GameConfig.ROUNDS) {
      this._endGame();
      return;
    }

    // 퍼즐 선택
    const bank = PUZZLES[this.state.difficulty];
    const puzzle = bank[Math.floor(Math.random() * bank.length)];
    this.state.puzzle = puzzle;
    this.state.placed = [];
    this.state.availablePieces = [...puzzle.pieces];
    this.state.selectedPieceId = null;
    this.state.timeLeft = this.state.difficulty === 'easy'
      ? GameConfig.TIME_EASY : GameConfig.TIME_HARD;
    this.state.inProgress = true;

    this.renderer.setPuzzle(puzzle);
    this._renderTray();
    this._updateHUD();

    if (this.state.timer) clearInterval(this.state.timer);
    this.state.timer = setInterval(() => {
      this.state.timeLeft--;
      this._updateHUD();
      if (this.state.timeLeft <= 0) {
        this._onTimeout();
      }
    }, 1000);
  }

  skipRound() {
    if (!this.state.inProgress) return;
    this._showRoundEnd({ success: false, reason: 'skip' });
  }

  _onTimeout() {
    clearInterval(this.state.timer);
    this.state.inProgress = false;
    this._showRoundEnd({ success: false, reason: 'timeout' });
  }

  _onSolved() {
    clearInterval(this.state.timer);
    this.state.inProgress = false;
    // 점수: 잔여 시간 × 10 + 보석 랜덤
    const timeBonus = this.state.timeLeft * 10;
    const gemRoll = Math.random();
    let gemType;
    if (gemRoll < 0.15) gemType = 'red';
    else if (gemRoll < 0.4) gemType = 'blue';
    else if (gemRoll < 0.7) gemType = 'green';
    else gemType = 'brown';
    this.state.gems[gemType]++;
    this.state.score += timeBonus + GameConfig.GEM_POINTS[gemType];
    this.state.solvedRounds++;
    this._showRoundEnd({ success: true, timeBonus, gemType });
  }

  _showRoundEnd({ success, reason, timeBonus, gemType }) {
    const modal = document.getElementById('roundEndModal');
    const title = document.getElementById('roundEndTitle');
    const body = document.getElementById('roundEndBody');
    const btn = document.getElementById('nextRoundBtn');

    if (success) {
      title.textContent = '🎉 Ubongo!';
      body.innerHTML = `
        <p>라운드 ${this.state.round} 완성!</p>
        <p>시간 보너스: <strong>+${timeBonus}</strong></p>
        <p>획득 보석: <strong>${this._gemLabel(gemType)}</strong> (+${GameConfig.GEM_POINTS[gemType]})</p>
      `;
    } else if (reason === 'timeout') {
      title.textContent = '⏱ 시간 초과';
      body.innerHTML = `<p>라운드 ${this.state.round} 실패. 다음 퍼즐을 시도하세요.</p>`;
    } else {
      title.textContent = '⏭ 건너뜀';
      body.innerHTML = `<p>라운드 ${this.state.round} 건너뜀.</p>`;
    }
    btn.textContent = this.state.round >= GameConfig.ROUNDS ? '결과 보기' : '다음 라운드';
    modal.classList.remove('hidden');
  }

  _endGame() {
    document.getElementById('gameScreen').classList.add('hidden');
    const end = document.getElementById('endScreen');
    end.classList.remove('hidden');
    const g = this.state.gems;
    document.getElementById('finalScore').textContent = this.state.score;
    document.getElementById('finalSolved').textContent = `${this.state.solvedRounds}/${GameConfig.ROUNDS}`;
    document.getElementById('finalGems').innerHTML = `
      <span class="gem gem-red">💎 ${g.red}</span>
      <span class="gem gem-blue">💎 ${g.blue}</span>
      <span class="gem gem-green">💎 ${g.green}</span>
      <span class="gem gem-brown">💎 ${g.brown}</span>
    `;

    // 최고 기록 저장
    const key = 'ubongo_best_' + this.state.difficulty;
    const best = parseInt(localStorage.getItem(key) || '0', 10);
    if (this.state.score > best) {
      localStorage.setItem(key, this.state.score);
      document.getElementById('newRecord').classList.remove('hidden');
    } else {
      document.getElementById('newRecord').classList.add('hidden');
    }
    document.getElementById('bestScore').textContent =
      Math.max(best, this.state.score);
  }

  _gemLabel(type) {
    return { red: '🔴 레드(4점)', blue: '🔵 블루(3점)', green: '🟢 그린(2점)', brown: '🟤 브라운(1점)' }[type];
  }

  /* -------------------- HUD 업데이트 -------------------- */
  _updateHUD() {
    document.getElementById('roundLabel').textContent = `${this.state.round} / ${GameConfig.ROUNDS}`;
    document.getElementById('timerLabel').textContent =
      `${String(Math.floor(this.state.timeLeft / 60)).padStart(1, '0')}:${String(this.state.timeLeft % 60).padStart(2, '0')}`;
    document.getElementById('scoreLabel').textContent = this.state.score;
    const g = this.state.gems;
    document.getElementById('gemsLabel').innerHTML =
      `<span class="gem gem-red">💎${g.red}</span> ` +
      `<span class="gem gem-blue">💎${g.blue}</span> ` +
      `<span class="gem gem-green">💎${g.green}</span> ` +
      `<span class="gem gem-brown">💎${g.brown}</span>`;
    // 시간 부족 시 경고색
    const t = document.getElementById('timerLabel');
    if (this.state.timeLeft <= 10) t.classList.add('warn');
    else t.classList.remove('warn');
  }

  /* -------------------- 트레이 렌더링 -------------------- */
  _renderTray() {
    const tray = document.getElementById('trayArea');
    tray.innerHTML = '';
    // 아직 보드에 배치되지 않은 조각만 트레이에 표시
    const placedIds = new Set(this.state.placed.map(p => p.pieceId));
    for (const pid of this.state.availablePieces) {
      if (placedIds.has(pid)) continue;
      const slot = document.createElement('div');
      slot.className = 'tray-slot';
      slot.dataset.pieceId = pid;
      if (this.state.selectedPieceId === pid) slot.classList.add('selected');
      const c = document.createElement('canvas');
      c.className = 'tray-canvas';
      slot.appendChild(c);
      tray.appendChild(slot);
      // 다음 프레임에 렌더 (크기 측정 후)
      requestAnimationFrame(() => {
        const rot = this.state.selectedPieceId === pid ? this.state.selectedRotation : 0;
        const flp = this.state.selectedPieceId === pid ? this.state.selectedFlipped : false;
        renderTrayPiece(c, pid, rot, flp, this.state.selectedPieceId === pid);
      });
    }

    // 모바일 컨트롤 바 표시 여부
    const controls = document.getElementById('mobileControls');
    if (this.state.selectedPieceId) controls.classList.add('visible');
    else controls.classList.remove('visible');
  }

  /* -------------------- 조각 조작 -------------------- */
  _selectPiece(pieceId) {
    if (this.state.selectedPieceId === pieceId) return;
    this.state.selectedPieceId = pieceId;
    this.state.selectedRotation = 0;
    this.state.selectedFlipped = false;
    this._renderTray();
  }

  _rotateSelected() {
    if (!this.state.selectedPieceId) return;
    this.state.selectedRotation = (this.state.selectedRotation + 1) % 4;
    // 이미 보드에 배치된 경우, 회전을 적용하고 다시 검증
    const placed = this.state.placed.find(p => p.pieceId === this.state.selectedPieceId);
    if (placed) {
      placed.rotation = this.state.selectedRotation;
      placed.shape = PieceUtils.transform(PIECES[placed.pieceId].shape, placed.rotation, placed.flipped);
      // 충돌 시 트레이로 복귀
      if (!this._validatePlacement(placed, placed.r, placed.c)) {
        this._returnPlaced(placed);
      }
    }
    this._renderTray();
    this.renderer.setPlaced(this.state.placed);
    this.renderer.draw();
  }

  _flipSelected() {
    if (!this.state.selectedPieceId) return;
    this.state.selectedFlipped = !this.state.selectedFlipped;
    const placed = this.state.placed.find(p => p.pieceId === this.state.selectedPieceId);
    if (placed) {
      placed.flipped = this.state.selectedFlipped;
      placed.shape = PieceUtils.transform(PIECES[placed.pieceId].shape, placed.rotation, placed.flipped);
      if (!this._validatePlacement(placed, placed.r, placed.c)) {
        this._returnPlaced(placed);
      }
    }
    this._renderTray();
    this.renderer.setPlaced(this.state.placed);
    this.renderer.draw();
  }

  _returnSelected() {
    if (!this.state.selectedPieceId) return;
    const pid = this.state.selectedPieceId;
    const idx = this.state.placed.findIndex(p => p.pieceId === pid);
    if (idx >= 0) this.state.placed.splice(idx, 1);
    this.state.selectedPieceId = null;
    this._renderTray();
    this.renderer.setPlaced(this.state.placed);
    this.renderer.draw();
  }

  _returnPlaced(placed) {
    const idx = this.state.placed.indexOf(placed);
    if (idx >= 0) this.state.placed.splice(idx, 1);
    this._renderTray();
    this.renderer.setPlaced(this.state.placed);
    this.renderer.draw();
  }

  /* -------------------- 배치 검증 -------------------- */
  _validatePlacement(piece, r, c) {
    const shape = piece.shape;
    const H = this.state.puzzle.shape.length;
    const W = this.state.puzzle.shape[0].length;
    // 타겟 모양 내부에만 허용 + 다른 배치와 겹침 금지
    // 동일 pieceId는 자기 자신이므로 제외 (참조 비교 대신)
    const covered = new Set();
    for (const p of this.state.placed) {
      if (p === piece || p.pieceId === piece.pieceId) continue;
      for (let dr = 0; dr < p.shape.length; dr++) {
        for (let dc = 0; dc < p.shape[dr].length; dc++) {
          if (p.shape[dr][dc]) covered.add(`${p.r + dr},${p.c + dc}`);
        }
      }
    }
    for (let dr = 0; dr < shape.length; dr++) {
      for (let dc = 0; dc < shape[dr].length; dc++) {
        if (!shape[dr][dc]) continue;
        const nr = r + dr, nc = c + dc;
        if (nr < 0 || nr >= H || nc < 0 || nc >= W) return false;
        if (!this.state.puzzle.shape[nr][nc]) return false;
        if (covered.has(`${nr},${nc}`)) return false;
      }
    }
    return true;
  }

  _checkSolved() {
    const H = this.state.puzzle.shape.length;
    const W = this.state.puzzle.shape[0].length;
    const filled = new Set();
    for (const p of this.state.placed) {
      for (let dr = 0; dr < p.shape.length; dr++) {
        for (let dc = 0; dc < p.shape[dr].length; dc++) {
          if (p.shape[dr][dc]) filled.add(`${p.r + dr},${p.c + dc}`);
        }
      }
    }
    for (let r = 0; r < H; r++) {
      for (let c = 0; c < W; c++) {
        if (this.state.puzzle.shape[r][c] && !filled.has(`${r},${c}`)) return false;
      }
    }
    return true;
  }

  /* -------------------- 입력 핸들러 -------------------- */
  _onTrayPointerDown(e) {
    if (!this.state.inProgress) return;
    const slot = e.target.closest('.tray-slot');
    if (!slot) return;
    const pid = slot.dataset.pieceId;
    this._selectPiece(pid);
    // 드래그 시작
    const shape = PieceUtils.transform(
      PIECES[pid].shape,
      this.state.selectedRotation,
      this.state.selectedFlipped
    );
    this.dragState = {
      pieceId: pid,
      shape,
      fromTray: true,
      pointerId: e.pointerId,
      // 조각의 [0,0]을 포인터 위치에 둠 (단순화)
      offsetR: 0,
      offsetC: 0
    };
    e.preventDefault();
  }

  _onBoardPointerDown(e) {
    if (!this.state.inProgress) return;
    const rect = this.boardCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const { r, c } = this.renderer.pxToCell(x, y);
    // 해당 셀에 배치된 조각 찾기
    const placed = this._pieceAt(r, c);
    if (!placed) {
      // 빈 공간 클릭 시 선택 해제
      this.state.selectedPieceId = null;
      this._renderTray();
      return;
    }
    this._selectPiece(placed.pieceId);
    // 드래그 시작
    this.dragState = {
      pieceId: placed.pieceId,
      shape: placed.shape.map(r => [...r]),
      fromTray: false,
      pointerId: e.pointerId,
      offsetR: r - placed.r,
      offsetC: c - placed.c,
      originPlaced: placed
    };
    // 기존 배치 제거 (드래그 중에는 빠져있음)
    const idx = this.state.placed.indexOf(placed);
    if (idx >= 0) this.state.placed.splice(idx, 1);
    this.renderer.setPlaced(this.state.placed);
    this.renderer.draw();
    e.preventDefault();
  }

  _pieceAt(r, c) {
    for (const p of this.state.placed) {
      for (let dr = 0; dr < p.shape.length; dr++) {
        for (let dc = 0; dc < p.shape[dr].length; dc++) {
          if (p.shape[dr][dc] && p.r + dr === r && p.c + dc === c) return p;
        }
      }
    }
    return null;
  }

  _onPointerMove(e) {
    if (!this.dragState) return;
    if (e.pointerId !== this.dragState.pointerId) return;
    const rect = this.boardCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const { r, c } = this.renderer.pxToCell(x, y);
    const targetR = r - this.dragState.offsetR;
    const targetC = c - this.dragState.offsetC;
    // 고스트 렌더
    const ghost = {
      pieceId: this.dragState.pieceId,
      shape: this.dragState.shape,
      r: targetR,
      c: targetC,
      valid: this._validatePlacement(
        { shape: this.dragState.shape },
        targetR, targetC
      )
    };
    this.renderer.setGhost(ghost);
  }

  _onPointerUp(e) {
    if (!this.dragState) return;
    if (e.pointerId !== this.dragState.pointerId) return;
    const ds = this.dragState;
    this.dragState = null;
    const rect = this.boardCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const { r, c } = this.renderer.pxToCell(x, y);
    const targetR = r - ds.offsetR;
    const targetC = c - ds.offsetC;

    this.renderer.setGhost(null);

    // 보드 바깥이면: 배치 취소 (트레이로 복귀)
    const insideCanvas = x >= 0 && y >= 0 && x <= rect.width && y <= rect.height;
    if (!insideCanvas) {
      // 이미 제거된 상태이므로 아무것도 안 함 (트레이에서 자동 복귀)
      this._renderTray();
      this.renderer.setPlaced(this.state.placed);
      this.renderer.draw();
      return;
    }

    const placement = {
      pieceId: ds.pieceId,
      shape: ds.shape,
      r: targetR,
      c: targetC,
      rotation: this.state.selectedRotation,
      flipped: this.state.selectedFlipped
    };
    if (this._validatePlacement(placement, targetR, targetC)) {
      this.state.placed.push(placement);
      this.renderer.setPlaced(this.state.placed);
      this.renderer.draw();
      this._renderTray();
      // 해결 체크
      if (this._checkSolved()) {
        this._onSolved();
      }
    } else {
      // 유효하지 않음 → 트레이로 복귀 (이미 제거된 상태)
      this._renderTray();
      this.renderer.setPlaced(this.state.placed);
      this.renderer.draw();
    }
  }
}

// 부팅
document.addEventListener('DOMContentLoaded', () => {
  window.game = new UbongoGame();
});
