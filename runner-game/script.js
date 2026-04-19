/**
 * 달리는 장윤이 (Runner)
 * 좌/우 스크롤 방식에서 위/아래로 이동해 떨어지는 아이템을 모은다.
 * 제어: 키보드(↑↓ / WS), 버튼(▲▼), 드래그, 스페이스바로 시작.
 */

(function () {
  'use strict';

  // ================== 설정 ==================
  const CONFIG = {
    TOTAL_TIME: 30,              // 초
    SPAWN_INTERVAL: 800,         // ms
    SPAWN_PROBABILITY: 0.7,      // 스폰 주기마다 실제 생성 확률
    POINT_PER_ITEM: 10,
    ITEM_SPEED: 6,               // px/frame (좌측 이동)
    PLAYER_STEP: 10,             // 이동 단위 (%)
    PLAYER_MIN_Y: 10,            // %
    PLAYER_MAX_Y: 90,            // %
    HOLD_INTERVAL: 50,           // 버튼 홀드 시 반복 이동 간격 (ms)
    SCORE_POPUP_DURATION: 600,   // ms
    STORAGE_KEY: 'runnerHighScore'
  };

  // ================== DOM ==================
  const $ = (id) => document.getElementById(id);
  const gameArea = $('gameArea');
  const player = $('player');
  const scoreEl = $('score');
  const timeEl = $('time');
  const startBtn = $('startBtn');
  const upBtn = $('upBtn');
  const downBtn = $('downBtn');
  const message = $('message');

  // ================== 상태 ==================
  const state = {
    score: 0,
    timeLeft: CONFIG.TOTAL_TIME,
    active: false,
    playerY: 50,           // 세로 위치 (%)
    items: new Set(),
    gameTimer: null,
    spawnTimer: null,
    animationId: null,
    drag: { isDragging: false, pointerId: null },
  };

  // ================== 게임 플로우 ==================
  function resetGame() {
    state.score = 0;
    state.timeLeft = CONFIG.TOTAL_TIME;
    state.active = false;
    state.playerY = 50;
    scoreEl.textContent = state.score;
    timeEl.textContent = state.timeLeft;
    message.classList.add('hidden');
    state.items.forEach(item => item.remove());
    state.items.clear();
    player.style.top = `${state.playerY}%`;
    if (state.animationId) {
      cancelAnimationFrame(state.animationId);
      state.animationId = null;
    }
  }

  function startGame() {
    if (state.active) return;
    resetGame();
    state.active = true;
    startBtn.textContent = '다시 시작';

    state.gameTimer = setInterval(tickTimer, 1000);
    state.spawnTimer = setInterval(() => {
      if (Math.random() < CONFIG.SPAWN_PROBABILITY) spawnItem();
    }, CONFIG.SPAWN_INTERVAL);
    gameLoop();
  }

  function endGame() {
    state.active = false;
    clearInterval(state.gameTimer);
    clearInterval(state.spawnTimer);
    if (state.animationId) {
      cancelAnimationFrame(state.animationId);
      state.animationId = null;
    }

    const highScore = parseInt(localStorage.getItem(CONFIG.STORAGE_KEY) || '0', 10);
    if (state.score > highScore) {
      localStorage.setItem(CONFIG.STORAGE_KEY, state.score);
      message.textContent = `새로운 기록! ${state.score}점 달성! 🎉`;
    } else {
      message.textContent = `게임 종료! ${state.score}점 획득! 🏁`;
    }
    message.classList.remove('hidden');
    startBtn.textContent = '다시 시작';
  }

  function tickTimer() {
    state.timeLeft--;
    timeEl.textContent = state.timeLeft;
    if (state.timeLeft <= 0) endGame();
  }

  // ================== 아이템 ==================
  function spawnItem() {
    if (!state.active) return;
    const item = document.createElement('div');
    item.className = 'item';
    // 세로 위치 10%~90%
    const y = CONFIG.PLAYER_MIN_Y + Math.random() * (CONFIG.PLAYER_MAX_Y - CONFIG.PLAYER_MIN_Y);
    item.style.top = `${y}%`;
    gameArea.appendChild(item);
    state.items.add(item);
  }

  function createScorePopup(x, y) {
    const popup = document.createElement('div');
    popup.className = 'score-popup';
    popup.textContent = `+${CONFIG.POINT_PER_ITEM}`;
    popup.style.left = x + 'px';
    popup.style.top = y + 'px';
    gameArea.appendChild(popup);
    setTimeout(() => popup.remove(), CONFIG.SCORE_POPUP_DURATION);
  }

  function collidesWithPlayer(itemRect, playerRect) {
    return !(itemRect.right < playerRect.left ||
             itemRect.left > playerRect.right ||
             itemRect.bottom < playerRect.top ||
             itemRect.top > playerRect.bottom);
  }

  function gameLoop() {
    if (!state.active) return;
    const playerRect = player.getBoundingClientRect();

    state.items.forEach(item => {
      const newX = item.offsetLeft - CONFIG.ITEM_SPEED;
      if (newX < -50) {
        state.items.delete(item);
        item.remove();
        return;
      }
      item.style.left = newX + 'px';

      const itemRect = item.getBoundingClientRect();
      if (collidesWithPlayer(itemRect, playerRect)) {
        state.items.delete(item);
        item.remove();
        state.score += CONFIG.POINT_PER_ITEM;
        scoreEl.textContent = state.score;
        createScorePopup(itemRect.left, itemRect.top);
      }
    });

    state.animationId = requestAnimationFrame(gameLoop);
  }

  // ================== 플레이어 이동 ==================
  function movePlayer(direction) {
    if (!state.active) return;
    const newPos = direction === 'up'
      ? Math.max(CONFIG.PLAYER_MIN_Y, state.playerY - CONFIG.PLAYER_STEP)
      : Math.min(CONFIG.PLAYER_MAX_Y, state.playerY + CONFIG.PLAYER_STEP);
    if (newPos !== state.playerY) {
      state.playerY = newPos;
      player.style.top = `${state.playerY}%`;
    }
  }

  // ================== 입력 ==================
  function bindKeyboard() {
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowUp' || e.key === 'w') movePlayer('up');
      else if (e.key === 'ArrowDown' || e.key === 's') movePlayer('down');
      else if (e.key === ' ' && !state.active) startGame();
    });
  }

  function bindHoldButton(btn, direction) {
    let intervalId = null;
    const start = () => {
      movePlayer(direction); // 즉시 한 번
      intervalId = setInterval(() => movePlayer(direction), CONFIG.HOLD_INTERVAL);
    };
    const stop = () => {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    };
    btn.addEventListener('pointerdown', start);
    btn.addEventListener('pointerup', stop);
    btn.addEventListener('pointerleave', stop);
    btn.addEventListener('pointercancel', stop);
  }

  function bindDrag() {
    const startDrag = (e) => {
      try { gameArea.focus(); } catch (_) {}
      state.drag.isDragging = true;
      state.drag.pointerId = e.pointerId;
      try { gameArea.setPointerCapture(e.pointerId); } catch (_) {}
    };
    const stopDrag = () => {
      if (!state.drag.isDragging) return;
      state.drag.isDragging = false;
      try { gameArea.releasePointerCapture(state.drag.pointerId); } catch (_) {}
      state.drag.pointerId = null;
    };
    const onMove = (e) => {
      if (!state.drag.isDragging || e.pointerId !== state.drag.pointerId) return;
      const rect = gameArea.getBoundingClientRect();
      const y = e.clientY - rect.top;
      const pct = (y / rect.height) * 100;
      state.playerY = Math.max(CONFIG.PLAYER_MIN_Y, Math.min(CONFIG.PLAYER_MAX_Y, pct));
      player.style.top = `${state.playerY}%`;
    };

    player.addEventListener('pointerdown', startDrag);
    gameArea.addEventListener('pointerdown', (e) => {
      if (e.target === gameArea) { startDrag(e); onMove(e); }
    });
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', stopDrag);
    window.addEventListener('pointercancel', stopDrag);
  }

  // ================== 초기화 ==================
  bindKeyboard();
  bindHoldButton(upBtn, 'up');
  bindHoldButton(downBtn, 'down');
  bindDrag();
  startBtn.addEventListener('click', startGame);
  gameArea.addEventListener('click', () => gameArea.focus());
  resetGame();
})();
