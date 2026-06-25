/**
 * 달리는 장윤이 (Runner)
 * 3D 장윤이 카드를 모으며 위/아래로 이동하는 러너 게임.
 * 제어: 키보드(↑↓ / WS), 버튼(▲▼), 드래그, 스페이스바로 시작.
 */

(function () {
  'use strict';

  const CONFIG = {
    TOTAL_TIME: 30,
    SPAWN_INTERVAL: 760,
    SPAWN_PROBABILITY: 0.74,
    POINT_PER_ITEM: 10,
    ITEM_SPEED: 6,
    PLAYER_STEP: 10,
    PLAYER_MIN_Y: 10,
    PLAYER_MAX_Y: 90,
    HOLD_INTERVAL: 50,
    SCORE_POPUP_DURATION: 600,
    STORAGE_KEY: 'runnerHighScore'
  };

  const $ = (id) => document.getElementById(id);
  const gameArea = $('gameArea');
  const player = $('player');
  const scoreEl = $('score');
  const timeEl = $('time');
  const startBtn = $('startBtn');
  const upBtn = $('upBtn');
  const downBtn = $('downBtn');
  const message = $('message');

  const state = {
    score: 0,
    timeLeft: CONFIG.TOTAL_TIME,
    active: false,
    playerY: 50,
    items: new Set(),
    gameTimer: null,
    spawnTimer: null,
    animationId: null,
    drag: { isDragging: false, pointerId: null },
  };

  function setPlayerVisual(direction = 0, scale = 1) {
    player.style.transform = `translate3d(0,-50%,0) rotateY(${direction * 16}deg) rotateX(${Math.abs(direction) * 2}deg) scale(${scale})`;
  }

  function resetGame() {
    state.score = 0;
    state.timeLeft = CONFIG.TOTAL_TIME;
    state.active = false;
    state.playerY = 50;
    scoreEl.textContent = state.score;
    timeEl.textContent = state.timeLeft;
    message.classList.add('hidden');
    state.items.forEach((item) => item.remove());
    state.items.clear();
    player.style.top = `${state.playerY}%`;
    setPlayerVisual(0, 1);
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
    let resultText;
    if (state.score > highScore) {
      localStorage.setItem(CONFIG.STORAGE_KEY, state.score);
      resultText = `새로운 기록! ${state.score}점 달성! 🎉`;
    } else {
      resultText = `게임 종료! ${state.score}점 획득! 🏁`;
    }
    message.innerHTML = `
      <p style="font-size:18px;font-weight:700;margin-bottom:10px;">${resultText}</p>
      <p style="margin:0;color:#9fb5d5;">3D 장윤이 카드를 최대한 많이 모아보세요!</p>
      <a href="../index.html" style="display:flex;align-items:center;justify-content:center;margin-top:10px;padding:16px;border-radius:14px;background:#374151;color:#fff;text-decoration:none;font-size:17px;font-weight:700;min-height:56px;box-sizing:border-box;">🏠 게임 목록으로</a>`;
    message.classList.remove('hidden');
    startBtn.textContent = '다시 시작';
  }

  function tickTimer() {
    state.timeLeft--;
    timeEl.textContent = state.timeLeft;
    if (state.timeLeft <= 0) endGame();
  }

  function spawnItem() {
    if (!state.active) return;
    const item = document.createElement('div');
    item.className = 'item';
    item.innerHTML = '<div class="item-shadow"></div><div class="item-card"><span class="item-face side"></span><span class="item-face front"></span></div>';
    const y = CONFIG.PLAYER_MIN_Y + Math.random() * (CONFIG.PLAYER_MAX_Y - CONFIG.PLAYER_MIN_Y);
    item.style.top = `${y}%`;
    item.dataset.depth = (0.86 + Math.random() * 0.28).toFixed(3);
    gameArea.appendChild(item);
    state.items.add(item);
  }

  function createScorePopup(x, y) {
    const popup = document.createElement('div');
    popup.className = 'score-popup';
    popup.textContent = `+${CONFIG.POINT_PER_ITEM}`;
    popup.style.left = `${x}px`;
    popup.style.top = `${y}px`;
    gameArea.appendChild(popup);
    setTimeout(() => popup.remove(), CONFIG.SCORE_POPUP_DURATION);
  }

  function collidesWithPlayer(itemRect, playerRect) {
    return !(itemRect.right < playerRect.left ||
             itemRect.left > playerRect.right ||
             itemRect.bottom < playerRect.top ||
             itemRect.top > playerRect.bottom);
  }

  function bumpPlayer() {
    setPlayerVisual(0, 1.08);
    setTimeout(() => {
      if (!state.active) return;
      setPlayerVisual(0, 1);
    }, 130);
  }

  function gameLoop() {
    if (!state.active) return;
    const playerRect = player.getBoundingClientRect();

    state.items.forEach((item) => {
      const newX = item.offsetLeft - CONFIG.ITEM_SPEED;
      if (newX < -70) {
        state.items.delete(item);
        item.remove();
        return;
      }
      item.style.left = `${newX}px`;
      const depth = parseFloat(item.dataset.depth || '1');
      item.style.transform = `translateZ(${(1.2 - depth) * 20}px) scale(${depth}) rotateY(${(newX % 36) - 18}deg)`;

      const itemRect = item.getBoundingClientRect();
      if (collidesWithPlayer(itemRect, playerRect)) {
        state.items.delete(item);
        item.remove();
        state.score += CONFIG.POINT_PER_ITEM;
        scoreEl.textContent = state.score;
        createScorePopup(itemRect.left, itemRect.top);
        bumpPlayer();
      }
    });

    state.animationId = requestAnimationFrame(gameLoop);
  }

  function movePlayer(direction) {
    if (!state.active) return;
    const newPos = direction === 'up'
      ? Math.max(CONFIG.PLAYER_MIN_Y, state.playerY - CONFIG.PLAYER_STEP)
      : Math.min(CONFIG.PLAYER_MAX_Y, state.playerY + CONFIG.PLAYER_STEP);
    if (newPos !== state.playerY) {
      state.playerY = newPos;
      player.style.top = `${state.playerY}%`;
      setPlayerVisual(direction === 'up' ? -1 : 1, 1.02);
      setTimeout(() => {
        if (state.active) setPlayerVisual(0, 1);
      }, 120);
    }
  }

  function bindKeyboard() {
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') movePlayer('up');
      else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') movePlayer('down');
      else if (e.key === ' ' && !state.active) startGame();
    });
  }

  function bindHoldButton(btn, direction) {
    let intervalId = null;
    const start = () => {
      movePlayer(direction);
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
      setPlayerVisual(0, 1);
    };
    const onMove = (e) => {
      if (!state.drag.isDragging || e.pointerId !== state.drag.pointerId) return;
      const rect = gameArea.getBoundingClientRect();
      const y = e.clientY - rect.top;
      const pct = (y / rect.height) * 100;
      const prev = state.playerY;
      state.playerY = Math.max(CONFIG.PLAYER_MIN_Y, Math.min(CONFIG.PLAYER_MAX_Y, pct));
      player.style.top = `${state.playerY}%`;
      if (state.playerY < prev - 0.5) setPlayerVisual(-1, 1.02);
      else if (state.playerY > prev + 0.5) setPlayerVisual(1, 1.02);
    };

    player.addEventListener('pointerdown', startDrag);
    gameArea.addEventListener('pointerdown', (e) => {
      if (e.target === gameArea) { startDrag(e); onMove(e); }
    });
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', stopDrag);
    window.addEventListener('pointercancel', stopDrag);
  }

  function decoratePlayer() {
    player.innerHTML = '<div class="runner-shadow"></div><div class="runner-card"><div class="runner-side"></div><div class="runner-glow"></div><div class="player-img" aria-hidden="true"></div></div>';
  }

  bindKeyboard();
  bindHoldButton(upBtn, 'up');
  bindHoldButton(downBtn, 'down');
  bindDrag();
  startBtn.addEventListener('click', startGame);
  gameArea.addEventListener('click', () => gameArea.focus());
  decoratePlayer();
  resetGame();
})();
