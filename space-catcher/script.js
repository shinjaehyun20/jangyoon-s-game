/**
 * Space Catcher — 장윤이 잡기
 * 하늘에서 떨어지는 3D 장윤이 카드를 좌/우 이동으로 잡는 게임.
 * 제어: 키보드(←/→), 모바일 버튼(◀/▶), 드래그.
 */

(function () {
  'use strict';

  const CONFIG = {
    TOTAL_TIME: 60,
    SPAWN_INTERVAL: 820,
    POINT_PER_STAR: 10,
    PLAYER_PADDING: 6,
    MOVEMENT_SPEED: 0.016,
    STAR_SPEED_MIN: 1.05,
    STAR_SPEED_MAX: 3.7,
    STAR_SPEED_MULT: 4,
    FLASH_DURATION: 160,
  };

  const $ = (id) => document.getElementById(id);
  const gameArea = $('gameArea');
  const player = $('player');
  const scoreEl = $('score');
  const timeEl = $('time');
  const startBtn = $('startBtn');
  const leftBtn = $('leftBtn');
  const rightBtn = $('rightBtn');
  const message = $('message');

  const state = {
    score: 0,
    timeLeft: CONFIG.TOTAL_TIME,
    active: false,
    keys: { left: false, right: false },
    gameTimer: null,
    spawnTimer: null,
    drag: { isDragging: false, pointerId: null },
  };

  function getCenteredLeft() {
    return Math.max(CONFIG.PLAYER_PADDING, (gameArea.clientWidth - player.clientWidth) / 2);
  }

  function setPlayerLeft(left) {
    const maxLeft = gameArea.clientWidth - player.clientWidth - CONFIG.PLAYER_PADDING;
    const clamped = Math.max(CONFIG.PLAYER_PADDING, Math.min(maxLeft, left));
    player.style.left = `${clamped}px`;
  }

  function resetGame() {
    state.score = 0;
    state.timeLeft = CONFIG.TOTAL_TIME;
    state.active = false;
    scoreEl.textContent = state.score;
    timeEl.textContent = state.timeLeft;
    message.classList.add('hidden');
    document.querySelectorAll('.star').forEach((s) => s.remove());
    setPlayerLeft(getCenteredLeft());
    setPlayerTilt(0, 1);
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
    message.innerHTML = `
      <p style="font-size:18px;font-weight:700;margin-bottom:10px;">시간 종료! 점수: ${state.score}점 🎉</p>
      <p style="margin:0;color:#bcd6ff;">3D 장윤이 카드를 ${state.score / CONFIG.POINT_PER_STAR | 0}장 모았어요!</p>
      <a href="../index.html" style="display:flex;align-items:center;justify-content:center;margin-top:10px;padding:16px;border-radius:14px;background:#374151;color:#fff;text-decoration:none;font-size:17px;font-weight:700;min-height:56px;box-sizing:border-box;">🏠 게임 목록으로</a>`;
    message.classList.remove('hidden');
  }

  function tickTimer() {
    state.timeLeft -= 1;
    timeEl.textContent = state.timeLeft;
    if (state.timeLeft <= 0) endGame();
  }

  function spawnStar() {
    if (!state.active) return;
    const star = document.createElement('div');
    star.className = 'star';
    star.innerHTML = '<div class="star-shadow"></div><div class="star-card"><span class="star-face side"></span><span class="star-face front"></span></div>';
    star.style.left = `${Math.random() * Math.max(10, gameArea.clientWidth - 58)}px`;
    star.style.top = '-70px';
    const speed = CONFIG.STAR_SPEED_MIN + Math.random() * (CONFIG.STAR_SPEED_MAX - CONFIG.STAR_SPEED_MIN);
    const drift = (Math.random() - 0.5) * 1.2;
    const swing = 0.92 + Math.random() * 0.22;
    star.dataset.speed = speed.toFixed(3);
    star.dataset.drift = drift.toFixed(3);
    star.dataset.swing = swing.toFixed(3);
    gameArea.appendChild(star);
  }

  function updatePlayerPosition(rect) {
    if (!state.keys.left && !state.keys.right) {
      setPlayerTilt(0, 1);
      return;
    }
    const step = rect.width * CONFIG.MOVEMENT_SPEED;
    const curLeft = player.offsetLeft;
    if (state.keys.left) {
      setPlayerLeft(curLeft - step);
      setPlayerTilt(-12, 1.03);
    } else if (state.keys.right) {
      setPlayerLeft(curLeft + step);
      setPlayerTilt(12, 1.03);
    }
  }

  function updateStars(rect) {
    const pRect = player.getBoundingClientRect();
    document.querySelectorAll('.star').forEach((star) => {
      const top = parseFloat(star.style.top);
      const newTop = top + parseFloat(star.dataset.speed) * CONFIG.STAR_SPEED_MULT;
      const drift = parseFloat(star.dataset.drift || '0');
      const curLeft = parseFloat(star.style.left);
      star.style.top = `${newTop}px`;
      star.style.left = `${Math.max(-20, Math.min(rect.width - 28, curLeft + drift))}px`;
      const progress = Math.max(0, Math.min(1, newTop / rect.height));
      const scale = 0.84 + progress * 0.34;
      const rotate = progress * 24 - 12;
      star.style.transform = `translateZ(${progress * 16}px) scale(${scale}) rotateX(${rotate}deg)`;

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

      if (newTop > rect.height + 80) star.remove();
    });
  }

  function gameLoop() {
    if (!state.active) return;
    const rect = gameArea.getBoundingClientRect();
    updatePlayerPosition(rect);
    updateStars(rect);
    requestAnimationFrame(gameLoop);
  }

  function setPlayerTilt(tiltDeg, scale) {
    player.style.transform = `translateZ(0) rotateY(${tiltDeg}deg) scale(${scale})`;
  }

  function flashPlayer() {
    setPlayerTilt(0, 1.08);
    player.classList.add('is-catching');
    setTimeout(() => {
      player.classList.remove('is-catching');
      if (!state.keys.left && !state.keys.right) setPlayerTilt(0, 1);
    }, CONFIG.FLASH_DURATION);
  }

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
    btn.addEventListener('pointercancel', release);
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
      state.keys.left = false;
      state.keys.right = false;
      setPlayerTilt(0, 1);
    };
    const onMove = (evt) => {
      if (!state.drag.isDragging || evt.pointerId !== state.drag.pointerId) return;
      const rect = gameArea.getBoundingClientRect();
      const x = evt.clientX - rect.left;
      const left = x - player.clientWidth / 2;
      const prev = player.offsetLeft;
      setPlayerLeft(left);
      const next = player.offsetLeft;
      if (next < prev - 1) setPlayerTilt(-15, 1.03);
      else if (next > prev + 1) setPlayerTilt(15, 1.03);
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

  function decoratePlayer() {
    player.innerHTML = '<div class="ship-shadow"></div><div class="ship-ring"></div><div class="ship-card"><span class="ship-face ship-back"></span><span class="ship-glow"></span><span class="ship-face ship-front"></span></div>';
  }

  bindKeyboardControls();
  bindButtonControls(leftBtn, 'left');
  bindButtonControls(rightBtn, 'right');
  bindDragControls();
  bindStartButton();
  gameArea.addEventListener('click', () => gameArea.focus());
  decoratePlayer();
  resetGame();
  window.addEventListener('resize', () => {
    if (!state.active) setPlayerLeft(getCenteredLeft());
  });
})();
