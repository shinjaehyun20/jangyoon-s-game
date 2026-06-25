(() => {
  'use strict';

  const CONFIG = {
    durationMs: 45_000,
    tickMs: 100,
    maxQueue: 5,
    spawnEveryMs: 2_000,
    scoreBase: 10,
    comboBonusCap: 20,
    bestKey: 'queue-train_best',
    colors: ['red', 'blue', 'yellow'],
    cargoByColor: {
      red: ['🍎', '🍓', '🍒'],
      blue: ['🐟', '🫐', '🫧'],
      yellow: ['⭐', '🍋', '🐤']
    },
    stationParticle: {
      red: '🍎',
      blue: '🐟',
      yellow: '⭐'
    }
  };

  const state = {
    queue: [],
    score: 0,
    combo: 0,
    lives: 3,
    started: false,
    ended: false,
    timeLeftMs: CONFIG.durationMs,
    nextSpawnAt: CONFIG.spawnEveryMs,
    rafId: null,
    timerId: null,
    lastTickAt: 0,
    best: readBestScore(),
    message: '시작 버튼을 눌러 놀이를 시작해요!',
    dispatchLocked: false
  };

  const el = {
    score: document.getElementById('score'),
    combo: document.getElementById('combo'),
    time: document.getElementById('time'),
    lives: document.getElementById('lives'),
    queueSlots: document.getElementById('queueSlots'),
    message: document.getElementById('message'),
    engine: document.getElementById('engine'),
    startOverlay: document.getElementById('startOverlay'),
    endOverlay: document.getElementById('endOverlay'),
    startBtn: document.getElementById('startBtn'),
    restartBtn: document.getElementById('restartBtn'),
    endTitle: document.getElementById('endTitle'),
    finalScore: document.getElementById('finalScore'),
    endMessage: document.getElementById('endMessage'),
    stationButtons: Array.from(document.querySelectorAll('.station-btn')),
    trackBoard: document.querySelector('.track-board')
  };

  const QueueModel = {
    createCar() {
      const color = randomPick(CONFIG.colors);
      const cargo = randomPick(CONFIG.cargoByColor[color]);
      return {
        id: `${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
        color,
        cargo
      };
    },
    ensureQueueSeed() {
      while (state.queue.length < 3) {
        state.queue.push(this.createCar());
      }
    },
    enqueue() {
      if (state.queue.length >= CONFIG.maxQueue) {
        return false;
      }
      state.queue.push(this.createCar());
      return true;
    },
    dequeue() {
      return state.queue.shift() || null;
    },
    peek() {
      return state.queue[0] || null;
    }
  };

  const View = {
    renderHud() {
      el.score.textContent = state.score.toString();
      el.combo.textContent = state.combo.toString();
      el.time.textContent = Math.max(0, Math.ceil(state.timeLeftMs / 1000)).toString();
      el.lives.textContent = '♥'.repeat(Math.max(0, state.lives)) || '♡';
      el.message.textContent = state.message;
    },
    renderQueue() {
      el.queueSlots.innerHTML = '';
      state.queue.forEach((car, index) => {
        const carEl = document.createElement('div');
        carEl.className = `car car--${car.color}${index === 0 ? ' is-front' : ''}`;
        carEl.dataset.id = car.id;
        carEl.innerHTML = `
          <span class="car-label">${index === 0 ? '앞칸' : index + 1}</span>
          <span class="car-emoji">${car.cargo}</span>
        `;
        el.queueSlots.appendChild(carEl);
      });

      for (let i = state.queue.length; i < CONFIG.maxQueue; i += 1) {
        const ghost = document.createElement('div');
        ghost.className = 'car';
        ghost.style.opacity = '0.18';
        ghost.style.borderStyle = 'dashed';
        ghost.innerHTML = '<span class="car-emoji">➕</span>';
        el.queueSlots.appendChild(ghost);
      }
    },
    setButtonsEnabled(enabled) {
      el.stationButtons.forEach((button) => {
        button.disabled = !enabled;
        button.style.filter = enabled ? 'none' : 'grayscale(0.3)';
        button.style.opacity = enabled ? '1' : '0.72';
      });
    },
    showStart() {
      el.startOverlay.classList.remove('hidden');
      el.endOverlay.classList.add('hidden');
    },
    hideStart() {
      el.startOverlay.classList.add('hidden');
    },
    showEnd() {
      el.endOverlay.classList.remove('hidden');
    },
    animateDispatch(car, targetColor, wasCorrect) {
      const frontCar = el.queueSlots.querySelector('.car.is-front');
      if (!frontCar) return Promise.resolve();

      state.dispatchLocked = true;
      View.setButtonsEnabled(false);

      const button = el.stationButtons.find((item) => item.dataset.color === targetColor);
      const particleX = button ? button.offsetLeft + button.offsetWidth / 2 : 160;
      const particleY = button ? button.offsetTop + 12 : 300;

      return new Promise((resolve) => {
        frontCar.classList.add('is-exiting');
        frontCar.style.transform = `translate(${particleX - 120}px, 84px) scale(${wasCorrect ? 1.08 : 0.92})`;
        setTimeout(() => {
          View.spawnParticle(particleX, particleY, wasCorrect ? car.cargo : '💥');
          state.dispatchLocked = false;
          View.setButtonsEnabled(!state.ended);
          resolve();
        }, 260);
      });
    },
    spawnParticle(x, y, emoji) {
      const particle = document.createElement('span');
      particle.className = 'particle';
      particle.textContent = emoji;
      particle.style.left = `${x}px`;
      particle.style.top = `${y}px`;
      el.trackBoard.appendChild(particle);
      setTimeout(() => particle.remove(), 900);
    },
    renderEnd() {
      const bestText = state.score > state.best ? '최고 기록 갱신!' : `최고 기록 ${state.best}점`;
      el.endTitle.textContent = state.lives > 0 ? '참 잘했어요! 🎉' : '다음엔 더 잘할 수 있어요!';
      el.finalScore.textContent = `${state.score}점`;
      el.endMessage.textContent = `${bestText} 콤보 ${state.combo}까지 갔어요.`;
    }
  };

  const App = {
    startGame() {
      resetState();
      QueueModel.ensureQueueSeed();
      state.started = true;
      state.lastTickAt = performance.now();
      state.message = '맨 앞 칸을 보고 같은 색 역으로 보내요!';
      View.hideStart();
      el.endOverlay.classList.add('hidden');
      View.setButtonsEnabled(true);
      renderAll();
      this.loop(state.lastTickAt);
    },
    loop(now) {
      if (state.ended) return;
      const delta = now - state.lastTickAt;
      state.lastTickAt = now;
      state.timeLeftMs -= delta;
      state.nextSpawnAt -= delta;

      if (state.nextSpawnAt <= 0) {
        const spawned = QueueModel.enqueue();
        state.nextSpawnAt = CONFIG.spawnEveryMs;
        state.message = spawned ? '새 칸이 줄 뒤에 붙었어요!' : '줄이 가득 찼어요! 빨리 보내 주세요!';
      }

      if (state.queue.length === 0) {
        QueueModel.enqueue();
      }

      renderAll();

      if (state.timeLeftMs <= 0 || state.lives <= 0) {
        this.finishGame();
        return;
      }

      state.rafId = requestAnimationFrame((nextNow) => this.loop(nextNow));
    },
    async dispatch(color) {
      if (!state.started || state.ended || state.dispatchLocked) return;
      const front = QueueModel.peek();
      if (!front) return;

      const chosen = color;
      const car = QueueModel.dequeue();
      const correct = car.color === chosen;

      if (correct) {
        state.combo += 1;
        const gain = CONFIG.scoreBase + Math.min(CONFIG.comboBonusCap, (state.combo - 1) * 2);
        state.score += gain;
        state.message = `${car.cargo} 칸을 ${stationName(chosen)}에 착! +${gain}점`;
      } else {
        state.combo = 0;
        state.lives -= 1;
        state.message = `${car.cargo} 칸은 ${stationName(car.color)}으로 가야 해요!`;
      }

      QueueModel.enqueue();
      renderAll();
      await View.animateDispatch(car, chosen, correct);
      renderAll();

      if (state.lives <= 0) {
        this.finishGame();
      }
    },
    finishGame() {
      state.ended = true;
      state.started = false;
      View.setButtonsEnabled(false);
      if (state.rafId) cancelAnimationFrame(state.rafId);
      state.best = Math.max(state.best, state.score);
      persistBestScore(state.best);
      View.renderEnd();
      View.showEnd();
      renderAll();
    }
  };

  function renderAll() {
    View.renderHud();
    View.renderQueue();
  }

  function resetState() {
    state.queue = [];
    state.score = 0;
    state.combo = 0;
    state.lives = 3;
    state.started = false;
    state.ended = false;
    state.timeLeftMs = CONFIG.durationMs;
    state.nextSpawnAt = CONFIG.spawnEveryMs;
    state.message = '기차 칸이 줄을 서고 있어요!';
    state.dispatchLocked = false;
    if (state.rafId) cancelAnimationFrame(state.rafId);
    state.rafId = null;
  }

  function readBestScore() {
    try {
      return Number(localStorage.getItem(CONFIG.bestKey) || 0);
    } catch {
      return 0;
    }
  }

  function persistBestScore(score) {
    try {
      localStorage.setItem(CONFIG.bestKey, String(score));
    } catch {
      // noop
    }
  }

  function stationName(color) {
    return {
      red: '빨강역',
      blue: '파랑역',
      yellow: '노랑역'
    }[color] || '역';
  }

  function randomPick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function bindEvents() {
    el.startBtn.addEventListener('click', () => App.startGame());
    el.restartBtn.addEventListener('click', () => App.startGame());
    el.stationButtons.forEach((button) => {
      button.addEventListener('click', () => App.dispatch(button.dataset.color));
    });
    window.addEventListener('keydown', (event) => {
      const keyMap = {
        ArrowLeft: 'red',
        ArrowUp: 'blue',
        ArrowRight: 'yellow',
        a: 'red',
        s: 'blue',
        d: 'yellow'
      };
      const color = keyMap[event.key];
      if (color) {
        event.preventDefault();
        App.dispatch(color);
      }
    });
  }

  bindEvents();
  View.renderHud();
  View.renderQueue();
  View.showStart();
  View.setButtonsEnabled(false);
})();
