/**
 * Space Catcher — 장윤이 잡기
 * 하늘에서 떨어지는 별을 좌/우 이동으로 잡는 간단한 게임.
 * 제어: 키보드(←/→), 모바일 버튼(◀/▶), 드래그.
 */

(function () {
  'use strict';

  // ================== 설정 ==================
  const CONFIG = {
    TOTAL_TIME: 60,           // 초
    SPAWN_INTERVAL: 900,      // ms
    POINT_PER_STAR: 10,
    PLAYER_PADDING: 6,        // 좌우 가장자리 여백(px)
    MOVEMENT_SPEED: 0.016,    // 게임 영역 폭 대비 프레임당 이동 비율
    STAR_SPEED_MIN: 1,
    STAR_SPEED_MAX: 3.6,
    STAR_SPEED_MULT: 4,       // 프레임당 추가 가속
    FLASH_DURATION: 120,      // 캐치 피드백 ms
  };

  // ================== DOM 참조 ==================
  const $ = (id) => document.getElementById(id);
  const gameArea = $('gameArea');
  const player = $('player');
  const scoreEl = $('score');
  const timeEl = $('time');
  const startBtn = $('startBtn');
  const leftBtn = $('leftBtn');
  const rightBtn = $('rightBtn');
  const message = $('message');

  // ================== 상태 ==================
  const state = {
    score: 0,
    timeLeft: CONFIG.TOTAL_TIME,
    active: false,
    keys: { left: false, right: false },
    gameTimer: null,
    spawnTimer: null,
    drag: { isDragging: false, pointerId: null },
  };

  // ================== 게임 플로우 ==================
  function resetGame() {
    state.score = 0;
    state.timeLeft = CONFIG.TOTAL_TIME;
    state.active = false;
    scoreEl.textContent = state.score;
    timeEl.textContent = state.timeLeft;
    message.classList.add('hidden');
    document.querySelectorAll('.star').forEach(s => s.remove());
    player.style.left = '50%';
  }

  function startGame() {
    resetGame();
    state.active = true;
    startBtn.textContent = '재시작';

    state.gameTimer = setInterval(tickTimer, 1000);
    state.spawnTimer = setInterval(spawnStar, CONFIG.SPAWN_INTERVAL);
    requestAnimationFrame(gameLoop);
  }

  function endGame() {
    state.active = false;
    clearInterval(state.gameTimer);
    clearInterval(state.spawnTimer);
    message.textContent = `시간 종료! 점수: ${state.score}점 🎉`;
    message.classList.remove('hidden');
  }

  function tickTimer() {
    state.timeLeft -= 1;
    timeEl.textContent = state.timeLeft;
    if (state.timeLeft <= 0) endGame();
  }

  // ================== 별 생성/이동 ==================
  function spawnStar() {
    const star = document.createElement('div');
    star.className = 'star';
    star.style.left = Math.random() * (gameArea.clientWidth - 42) + 'px';
    star.style.top = '-50px';
    const speed = CONFIG.STAR_SPEED_MIN +
                  Math.random() * (CONFIG.STAR_SPEED_MAX - CONFIG.STAR_SPEED_MIN);
    star.dataset.speed = speed;
    gameArea.appendChild(star);
  }

  function updatePlayerPosition(rect) {
    if (!state.keys.left && !state.keys.right) return;
    const step = rect.width * CONFIG.MOVEMENT_SPEED;
    const curLeft = player.offsetLeft;
    const maxLeft = rect.width - player.clientWidth - CONFIG.PLAYER_PADDING;
    if (state.keys.left) {
      player.style.left = Math.max(CONFIG.PLAYER_PADDING, curLeft - step) + 'px';
    } else if (state.keys.right) {
      player.style.left = Math.min(maxLeft, curLeft + step) + 'px';
    }
  }

  function updateStars(rect) {
    const pRect = player.getBoundingClientRect();
    document.querySelectorAll('.star').forEach(star => {
      const top = parseFloat(star.style.top);
      const newTop = top + parseFloat(star.dataset.speed) * CONFIG.STAR_SPEED_MULT;
      star.style.top = newTop + 'px';

      // 플레이어 충돌 판정
      const sRect = star.getBoundingClientRect();
      const overlapping = !(sRect.right < pRect.left ||
                            sRect.left > pRect.right ||
                            sRect.bottom < pRect.top ||
                            sRect.top > pRect.bottom);
      if (overlapping) {
        star.remove();
        state.score += CONFIG.POINT_PER_STAR;
        scoreEl.textContent = state.score;
        flashPlayer();
        return;
      }

      // 화면 바깥으로 떨어지면 제거
      if (newTop > rect.height + 60) star.remove();
    });
  }

  function gameLoop() {
    if (!state.active) return;
    const rect = gameArea.getBoundingClientRect();
    updatePlayerPosition(rect);
    updateStars(rect);
    requestAnimationFrame(gameLoop);
  }

  function flashPlayer() {
    player.style.transform = 'translateX(-50%) scale(1.07)';
    setTimeout(() => { player.style.transform = 'translateX(-50%)'; }, CONFIG.FLASH_DURATION);
  }

  // ================== 입력 ==================
  function bindKeyboardControls() {
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') state.keys.left = true;
      if (e.key === 'ArrowRight') state.keys.right = true;
    });
    window.addEventListener('keyup', (e) => {
      if (e.key === 'ArrowLeft') state.keys.left = false;
      if (e.key === 'ArrowRight') state.keys.right = false;
    });
  }

  function bindButtonControls(btn, key) {
    const press = () => { state.keys[key] = true; };
    const release = () => { state.keys[key] = false; };
    btn.addEventListener('pointerdown', press);
    btn.addEventListener('pointerup', release);
    btn.addEventListener('pointerleave', release);
  }

  function bindDragControls() {
    const startDrag = (evt) => {
      try { gameArea.focus(); } catch (_) {}
      state.drag.isDragging = true;
      state.drag.pointerId = evt.pointerId;
      try { gameArea.setPointerCapture(evt.pointerId); } catch (_) {}
    };
    const stopDrag = () => {
      if (!state.drag.isDragging) return;
      state.drag.isDragging = false;
      try { gameArea.releasePointerCapture(state.drag.pointerId); } catch (_) {}
      state.drag.pointerId = null;
    };
    const onMove = (evt) => {
      if (!state.drag.isDragging || evt.pointerId !== state.drag.pointerId) return;
      const rect = gameArea.getBoundingClientRect();
      const x = evt.clientX - rect.left;
      const clamped = Math.max(
        CONFIG.PLAYER_PADDING,
        Math.min(rect.width - player.clientWidth - CONFIG.PLAYER_PADDING,
                 x - player.clientWidth / 2)
      );
      player.style.left = clamped + 'px';
    };

    player.addEventListener('pointerdown', startDrag);
    gameArea.addEventListener('pointerdown', (e) => {
      if (e.target === gameArea) { startDrag(e); onMove(e); }
    });
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', stopDrag);
    window.addEventListener('pointercancel', stopDrag);
  }

  function bindStartButton() {
    startBtn.addEventListener('click', () => {
      if (state.active) {
        endGame();
        resetGame();
      }
      startGame();
    });
  }

  // ================== 초기화 ==================
  function decoratePlayer() {
    const eye = document.createElement('div');
    eye.className = 'player-eye';
    player.appendChild(eye);
  }

  bindKeyboardControls();
  bindButtonControls(leftBtn, 'left');
  bindButtonControls(rightBtn, 'right');
  bindDragControls();
  bindStartButton();
  gameArea.addEventListener('click', () => gameArea.focus());
  decoratePlayer();
  resetGame();
})();
