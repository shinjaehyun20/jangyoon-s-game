import os
import json
import re
import subprocess
from pathlib import Path

ROOT = r"D:\workspace\projects\active\jangyoon-s-game"

# ==========================================
# 1. NEON CIRCUIT CONNECT
# ==========================================
neon_dir = os.path.join(ROOT, "neon-circuit-connect")
os.makedirs(neon_dir, exist_ok=True)

neon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" role="img" aria-label="네온 회로 연결사">
<defs>
  <linearGradient id="neonBg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#090d16"/>
    <stop offset="60%" stop-color="#0c1a30"/>
    <stop offset="100%" stop-color="#050b14"/>
  </linearGradient>
  <linearGradient id="wireGlow" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#00f0ff"/>
    <stop offset="100%" stop-color="#39ff14"/>
  </linearGradient>
  <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3.5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="320" height="180" rx="18" fill="url(#neonBg)"/>
<!-- Background Circuit Grid Lines -->
<path d="M20 40 H120 V90 H220 V140 H300" stroke="#1e293b" stroke-width="2" fill="none" opacity="0.6"/>
<path d="M40 160 V100 H160 V30 H280" stroke="#1e293b" stroke-width="2" fill="none" opacity="0.6"/>
<!-- Glowing Circuit Paths -->
<g filter="url(#neonGlow)">
  <path d="M50 90 H110 V50 H170 V110 H230" stroke="url(#wireGlow)" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Energy Nodes -->
  <circle cx="50" cy="90" r="10" fill="#00f0ff"/>
  <circle cx="110" cy="50" r="6" fill="#39ff14"/>
  <circle cx="170" cy="110" r="6" fill="#00f0ff"/>
  <circle cx="230" cy="110" r="12" fill="#a855f7"/>
  <!-- Sparks -->
  <circle cx="80" cy="90" r="3" fill="#ffffff"/>
  <circle cx="140" cy="50" r="3" fill="#ffffff"/>
  <circle cx="200" cy="110" r="3" fill="#ffffff"/>
</g>
<!-- Power & Robot Icons -->
<text x="50" y="95" text-anchor="middle" font-size="12" fill="#000">⚡</text>
<text x="230" y="116" text-anchor="middle" font-size="14" fill="#fff">🤖</text>
<!-- Corner accents -->
<path d="M12 24 V12 H24" stroke="#00f0ff" stroke-width="2" fill="none"/>
<path d="M308 24 V12 H296" stroke="#39ff14" stroke-width="2" fill="none"/>
<!-- Text Labels -->
<text x="296" y="148" text-anchor="end" font-family="Pretendard,Malgun Gothic,sans-serif" font-size="20" font-weight="900" fill="#00f0ff">네온 회로 연결사</text>
<text x="296" y="166" text-anchor="end" font-family="Pretendard,Arial,sans-serif" font-size="10" font-weight="700" fill="#a5f3fc" letter-spacing="2">NEON CIRCUIT CONNECT</text>
<rect x="0.5" y="0.5" width="319" height="179" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.15"/>
</svg>"""

neon_html = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>네온 회로 연결사</title>
<link rel="icon" href="data:,">
<style>
:root {
  --cyan: #00f0ff;
  --lime: #39ff14;
  --purple: #c084fc;
  --bg: #090d16;
  --panel: rgba(15, 23, 42, 0.85);
  --border: rgba(0, 240, 255, 0.25);
}
* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; margin: 0; padding: 0; }
html, body {
  height: 100vh; height: 100dvh;
  overflow: hidden;
  touch-action: manipulation;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
  color: #fff;
  background: var(--bg);
}
body {
  background: radial-gradient(circle at 50% 20%, #111d38 0%, #080c14 100%);
}
.wrap {
  position: relative;
  width: 100%;
  max-width: 480px;
  height: 100vh; height: 100dvh;
  margin: auto;
  padding: 10px 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
h1 {
  font-size: clamp(19px, 5vw, 24px);
  color: #e0f2fe;
  text-shadow: 0 0 12px rgba(0, 240, 255, 0.6);
  display: flex;
  align-items: center;
  gap: 6px;
}
.sub {
  font-size: 11px;
  font-weight: 700;
  color: #7dd3fc;
  margin-top: 2px;
}
.hud {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}
.chip {
  padding: 6px 4px;
  text-align: center;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(6px);
  border: 1px solid var(--border);
  font-size: 11px;
  color: #a5f3fc;
}
.chip b {
  display: block;
  font-size: 16px;
  color: #fff;
  margin-top: 2px;
}
.board-container {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.05), transparent 70%), rgba(10, 16, 30, 0.7);
  box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.7);
  padding: 12px;
}
.grid {
  display: grid;
  gap: 8px;
  width: 100%;
  max-width: 320px;
  aspect-ratio: 1 / 1;
  place-items: center;
  position: relative;
}
.tile {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  background: rgba(30, 41, 59, 0.7);
  border: 2px solid rgba(255, 255, 255, 0.1);
  display: grid;
  place-items: center;
  position: relative;
  cursor: pointer;
  touch-action: manipulation;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.2s, border-color 0.2s;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.tile:active {
  transform: scale(0.92);
}
.tile.powered {
  border-color: var(--cyan);
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.5), inset 0 0 10px rgba(0, 240, 255, 0.2);
  background: rgba(0, 240, 255, 0.15);
}
.tile.source-tile {
  background: radial-gradient(circle, rgba(0, 240, 255, 0.4), rgba(15, 23, 42, 0.8));
  border-color: var(--cyan);
}
.tile.target-tile {
  background: radial-gradient(circle, rgba(192, 132, 252, 0.4), rgba(15, 23, 42, 0.8));
  border-color: var(--purple);
}
.tile-svg {
  width: 80%;
  height: 80%;
  transition: transform 0.22s ease-out;
  pointer-events: none;
}
.badge-node {
  position: absolute;
  font-size: 24px;
  pointer-events: none;
  filter: drop-shadow(0 0 8px rgba(0, 240, 255, 0.8));
}
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: #7dd3fc;
  padding: 0 4px;
}
.home-link {
  color: #39ff14;
  font-weight: 900;
  text-decoration: none;
  font-size: 12px;
}
.overlay {
  position: fixed;
  z-index: 20;
  inset: 0;
  padding: 20px;
  display: grid;
  place-items: center;
  background: rgba(8, 12, 20, 0.85);
  backdrop-filter: blur(10px);
}
.overlay.hidden { display: none; }
.card {
  width: min(380px, 100%);
  padding: 24px 20px;
  text-align: center;
  border-radius: 24px;
  border: 1px solid var(--cyan);
  background: linear-gradient(160deg, #111d38, #090d16);
  box-shadow: 0 16px 40px rgba(0, 240, 255, 0.2);
}
.card h2 {
  margin: 0 0 10px;
  font-size: 22px;
  color: #39ff14;
  text-shadow: 0 0 10px rgba(57, 255, 20, 0.5);
}
.card p {
  margin: 0 0 16px;
  font-size: 13px;
  line-height: 1.6;
  color: #e0f2fe;
}
.btn {
  padding: 12px 26px;
  border: 0;
  border-radius: 14px;
  background: linear-gradient(135deg, #00f0ff, #3b82f6);
  color: #000;
  font-size: 16px;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 240, 255, 0.4);
}
.btn:active { transform: scale(0.96); }
/* Particle floating canvas */
#spark-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10;
}
</style>
</head>
<body>
<main class="wrap">
  <header>
    <div>
      <h1>⚡ 네온 회로 연결사</h1>
      <div class="sub">타일을 탭해 회전시켜 로봇까지 에너지를 연결하세요!</div>
    </div>
    <div class="chip" style="min-width:65px">최고 <b id="best">0</b></div>
  </header>
  <section class="hud">
    <div class="chip">스테이지<b id="stage">1</b></div>
    <div class="chip">점수<b id="score">0</b></div>
    <div class="chip">시간<b id="timer">45초</b></div>
    <div class="chip">콤보<b id="combo">0x</b></div>
  </section>
  <div class="board-container">
    <canvas id="spark-canvas"></canvas>
    <div class="grid" id="grid"></div>
  </div>
  <footer class="footer">
    <span>💡 ⚡발전소에서 🤖로봇까지 전선이 이어지면 충전 성공!</span>
    <a class="home-link" href="../index.html">← 홈</a>
  </footer>
</main>

<div class="overlay" id="startOverlay">
  <div class="card">
    <div style="font-size:48px;margin-bottom:8px">⚡🧩🤖</div>
    <h2>네온 회로 연결사</h2>
    <p>어두운 메가시티에 에너지를 공급해주세요!<br>회로 타일을 톡톡 터치해 회전시키면<br>⚡발전소에서 🤖아기 로봇까지 네온 불빛이 켜져요!<br><br>연결할 때마다 보너스 시간 +3초 지급!</p>
    <button class="btn" id="startBtn">회로 연결 시작!</button>
  </div>
</div>

<div class="overlay hidden" id="endOverlay">
  <div class="card">
    <div style="font-size:48px;margin-bottom:8px" id="endEmoji">🎉</div>
    <h2 id="endTitle">충전 완료!</h2>
    <p id="endText"></p>
    <button class="btn" id="restartBtn">다시 도전</button>
  </div>
</div>

<script>
(()=>{'use strict';
const KEY = 'neon_circuit_connect_best';
const AUD = window.AudioContext || window.webkitAudioContext;
let actx = null;

function playSound(type) {
  try {
    if (!actx) actx = new AUD();
    if (actx.state === 'suspended') actx.resume();
    let now = actx.currentTime;
    if (type === 'click') {
      let osc = actx.createOscillator(), g = actx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.05);
      g.gain.setValueAtTime(0.15, now);
      g.gain.linearRampToValueAtTime(0.001, now + 0.05);
      osc.connect(g); g.connect(actx.destination);
      osc.start(now); osc.stop(now + 0.05);
    } else if (type === 'win') {
      [523.25, 659.25, 783.99, 1046.5].forEach((freq, i) => {
        let osc = actx.createOscillator(), g = actx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + i * 0.07);
        g.gain.setValueAtTime(0.2, now + i * 0.07);
        g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.07 + 0.25);
        osc.connect(g); g.connect(actx.destination);
        osc.start(now + i * 0.07); osc.stop(now + i * 0.07 + 0.25);
      });
    }
  } catch(e) {}
}

const TILE_TYPES = {
  line:   [1, 0, 1, 0], // Top, Right, Bottom, Left
  corner: [1, 1, 0, 0],
  tee:    [1, 1, 1, 0],
  cross:  [1, 1, 1, 1]
};

let stage = 1, score = 0, timeLeft = 45, combo = 0, running = false, timerInterval = null;
let GRID_SIZE = 3;
let board = []; // 2D array: { type, rot: 0..3, powered: false }

const cvs = document.getElementById('spark-canvas');
const ctx = cvs.getContext('2d');
let particles = [];

function resizeCanvas() {
  const rect = cvs.getBoundingClientRect();
  cvs.width = rect.width;
  cvs.height = rect.height;
}
window.addEventListener('resize', resizeCanvas);

function spawnSparks(x, y, color = '#00f0ff', count = 18) {
  for (let i = 0; i < count; i++) {
    let ang = Math.random() * Math.PI * 2;
    let spd = 2 + Math.random() * 5;
    particles.push({
      x, y,
      vx: Math.cos(ang) * spd,
      vy: Math.sin(ang) * spd,
      r: 2 + Math.random() * 3,
      alpha: 1,
      color
    });
  }
}

function updateParticles() {
  ctx.clearRect(0, 0, cvs.width, cvs.height);
  for (let i = particles.length - 1; i >= 0; i--) {
    let p = particles[i];
    p.x += p.vx; p.y += p.vy;
    p.alpha -= 0.035;
    if (p.alpha <= 0) {
      particles.splice(i, 1);
      continue;
    }
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.globalAlpha = p.alpha;
    ctx.fill();
    ctx.globalAlpha = 1;
  }
  if (running || particles.length > 0) {
    requestAnimationFrame(updateParticles);
  }
}

function getOpenings(tile) {
  let base = TILE_TYPES[tile.type];
  let rot = tile.rot % 4;
  let op = [0, 0, 0, 0];
  for (let i = 0; i < 4; i++) {
    op[(i + rot) % 4] = base[i];
  }
  return op; // [Top, Right, Bottom, Left]
}

function generateSolvableLevel() {
  GRID_SIZE = stage >= 5 ? 4 : 3;
  const gridEl = document.getElementById('grid');
  gridEl.style.gridTemplateColumns = `repeat(${GRID_SIZE}, 1fr)`;
  gridEl.style.gridTemplateRows = `repeat(${GRID_SIZE}, 1fr)`;

  let maxAttempts = 50;
  while (maxAttempts-- > 0) {
    board = [];
    for (let r = 0; r < GRID_SIZE; r++) {
      let row = [];
      for (let c = 0; c < GRID_SIZE; c++) {
        let types = ['line', 'corner', 'corner', 'tee'];
        if (stage >= 3) types.push('cross');
        let t = types[Math.floor(Math.random() * types.length)];
        let correctRot = Math.floor(Math.random() * 4);
        row.push({ r, c, type: t, rot: correctRot, powered: false });
      }
      board.push(row);
    }

    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        board[r][c].rot = Math.floor(Math.random() * 4);
      }
    }

    checkPowerFlow();
    if (!board[GRID_SIZE - 1][GRID_SIZE - 1].powered) {
      break;
    }
  }
  renderGrid();
}

function checkPowerFlow() {
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      board[r][c].powered = false;
    }
  }

  let queue = [{ r: 0, c: 0 }];
  board[0][0].powered = true;
  let visited = new Set(['0,0']);

  const dr = [-1, 0, 1, 0];
  const dc = [0, 1, 0, -1];
  const opp = [2, 3, 0, 1];

  while (queue.length > 0) {
    let curr = queue.shift();
    let op = getOpenings(board[curr.r][curr.c]);

    for (let d = 0; d < 4; d++) {
      if (op[d] === 1) {
        let nr = curr.r + dr[d];
        let nc = curr.c + dc[d];
        if (nr >= 0 && nr < GRID_SIZE && nc >= 0 && nc < GRID_SIZE) {
          let neighbor = board[nr][nc];
          let nop = getOpenings(neighbor);
          if (nop[opp[d]] === 1) {
            let key = `${nr},${nc}`;
            if (!visited.has(key)) {
              visited.add(key);
              neighbor.powered = true;
              queue.push({ r: nr, c: nc });
            }
          }
        }
      }
    }
  }
}

function renderGrid() {
  const gridEl = document.getElementById('grid');
  gridEl.innerHTML = '';

  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      const tile = board[r][c];
      const div = document.createElement('div');
      div.className = 'tile' + (tile.powered ? ' powered' : '');
      if (r === 0 && c === 0) div.classList.add('source-tile');
      if (r === GRID_SIZE - 1 && c === GRID_SIZE - 1) div.classList.add('target-tile');

      div.innerHTML = getTileSVG(tile.type, tile.rot, tile.powered);

      if (r === 0 && c === 0) {
        let badge = document.createElement('span');
        badge.className = 'badge-node';
        badge.textContent = '⚡';
        div.appendChild(badge);
      } else if (r === GRID_SIZE - 1 && c === GRID_SIZE - 1) {
        let badge = document.createElement('span');
        badge.className = 'badge-node';
        badge.textContent = tile.powered ? '🤖✨' : '🤖';
        div.appendChild(badge);
      }

      div.addEventListener('pointerdown', (e) => {
        e.preventDefault();
        if (!running) return;
        tile.rot = (tile.rot + 1) % 4;
        playSound('click');
        checkPowerFlow();
        renderGrid();

        let rect = div.getBoundingClientRect();
        let cRect = cvs.getBoundingClientRect();
        spawnSparks(rect.left + rect.width / 2 - cRect.left, rect.top + rect.height / 2 - cRect.top, tile.powered ? '#00f0ff' : '#64748b', 6);

        if (board[GRID_SIZE - 1][GRID_SIZE - 1].powered) {
          handleWin();
        }
      });

      gridEl.appendChild(div);
    }
  }
}

function getTileSVG(type, rot, powered) {
  let stroke = powered ? '#00f0ff' : '#475569';
  let glow = powered ? 'filter="drop-shadow(0 0 6px #00f0ff)"' : '';
  let width = powered ? '8' : '6';

  let pathData = '';
  if (type === 'line') {
    pathData = '<line x1="50" y1="0" x2="50" y2="100" />';
  } else if (type === 'corner') {
    pathData = '<path d="M50 0 V50 H100" fill="none" />';
  } else if (type === 'tee') {
    pathData = '<path d="M50 0 V100 M50 50 H100" fill="none" />';
  } else if (type === 'cross') {
    pathData = '<line x1="50" y1="0" x2="50" y2="100" /><line x1="0" y1="50" x2="100" y2="50" />';
  }

  let deg = rot * 90;
  return `
    <svg class="tile-svg" viewBox="0 0 100 100" style="transform: rotate(${deg}deg)">
      <g stroke="${stroke}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${glow}>
        ${pathData}
      </g>
    </svg>
  `;
}

function handleWin() {
  playSound('win');
  combo++;
  let addScore = 100 + (combo - 1) * 25;
  score += addScore;
  timeLeft = Math.min(60, timeLeft + 3);

  document.getElementById('score').textContent = score;
  document.getElementById('combo').textContent = combo + 'x';
  document.getElementById('timer').textContent = timeLeft + '초';

  let cRect = cvs.getBoundingClientRect();
  spawnSparks(cRect.width / 2, cRect.height / 2, '#39ff14', 35);
  spawnSparks(cRect.width / 2, cRect.height / 2, '#c084fc', 25);

  setTimeout(() => {
    stage++;
    document.getElementById('stage').textContent = stage;
    generateSolvableLevel();
  }, 450);
}

function startGame() {
  stage = 1; score = 0; timeLeft = 45; combo = 0; running = true;
  document.getElementById('stage').textContent = '1';
  document.getElementById('score').textContent = '0';
  document.getElementById('timer').textContent = '45초';
  document.getElementById('combo').textContent = '0x';
  document.getElementById('startOverlay').classList.add('hidden');
  document.getElementById('endOverlay').classList.add('hidden');

  resizeCanvas();
  updateParticles();
  generateSolvableLevel();

  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById('timer').textContent = timeLeft + '초';
    if (timeLeft <= 0) endGame();
  }, 1000);
}

function endGame() {
  running = false;
  clearInterval(timerInterval);
  let best = Math.max(+localStorage.getItem(KEY) || 0, score);
  localStorage.setItem(KEY, best);
  document.getElementById('best').textContent = best;

  document.getElementById('endTitle').textContent = '에너지 충전 완료!';
  document.getElementById('endText').textContent = `총 ${score}점을 획득하고 ${stage - 1}개의 회로를 완벽하게 연결했어요!`;
  document.getElementById('endOverlay').classList.remove('hidden');
}

document.getElementById('best').textContent = localStorage.getItem(KEY) || 0;
document.getElementById('startBtn').addEventListener('pointerdown', startGame);
document.getElementById('restartBtn').addEventListener('pointerdown', startGame);
})();
</script>
</body>
</html>"""

with open(os.path.join(neon_dir, "thumb.svg"), "w", encoding="utf-8") as f:
    f.write(neon_svg)
with open(os.path.join(neon_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(neon_html)
print("Created neon-circuit-connect")

# ==========================================
# 2. JUNGLE VINE SWINGER
# ==========================================
jungle_dir = os.path.join(ROOT, "jungle-vine-swinger")
os.makedirs(jungle_dir, exist_ok=True)

jungle_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" role="img" aria-label="정글 덩굴 스윙 타잔">
<defs>
  <linearGradient id="jungleBg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#064e3b"/>
    <stop offset="60%" stop-color="#022c22"/>
    <stop offset="100%" stop-color="#061f17"/>
  </linearGradient>
  <linearGradient id="bananaGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#fef08a"/>
    <stop offset="100%" stop-color="#eab308"/>
  </linearGradient>
  <filter id="jungleGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3.5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="320" height="180" rx="18" fill="url(#jungleBg)"/>
<!-- Jungle Canopy Leaves -->
<path d="M-10 0 Q40 60 90 0 Q140 70 190 0 Q240 65 300 0 Q330 40 340 0 V-10 H-10 Z" fill="#047857" opacity="0.7"/>
<path d="M0 180 Q60 140 120 180 Q180 130 240 180 Q290 145 330 180 Z" fill="#065f46" opacity="0.8"/>
<!-- Vines -->
<path d="M80 0 Q95 50 110 90" stroke="#15803d" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M220 0 Q205 45 190 85" stroke="#15803d" stroke-width="4" fill="none" stroke-linecap="round"/>
<!-- Monkey Swinger -->
<g transform="translate(110, 90)">
  <!-- Tail -->
  <path d="M-12 10 Q-25 18 -20 28 Q-15 35 -6 28" fill="none" stroke="#b45309" stroke-width="4" stroke-linecap="round"/>
  <!-- Body -->
  <ellipse cx="0" cy="12" rx="14" ry="16" fill="#b45309"/>
  <ellipse cx="0" cy="14" rx="9" ry="11" fill="#fde68a"/>
  <!-- Head -->
  <circle cx="0" cy="-4" r="14" fill="#b45309"/>
  <circle cx="-14" cy="-4" r="5" fill="#fde68a"/>
  <circle cx="14" cy="-4" r="5" fill="#fde68a"/>
  <ellipse cx="0" cy="-1" rx="10" ry="8" fill="#fde68a"/>
  <!-- Eyes -->
  <circle cx="-4" cy="-4" r="2.5" fill="#0f172a"/>
  <circle cx="4" cy="-4" r="2.5" fill="#0f172a"/>
  <circle cx="-5" cy="-5" r="1" fill="#ffffff"/>
  <circle cx="3" cy="-5" r="1" fill="#ffffff"/>
  <!-- Smile -->
  <path d="M-3 2 Q0 5 3 2" fill="none" stroke="#78350f" stroke-width="1.5" stroke-linecap="round"/>
  <!-- Arms holding vine -->
  <path d="M-8 4 Q0 -15 0 -4" fill="none" stroke="#b45309" stroke-width="4" stroke-linecap="round"/>
</g>
<!-- Flying Bananas and Stars -->
<g filter="url(#jungleGlow)">
  <path d="M170 65 Q180 50 195 55 Q185 65 170 65 Z" fill="url(#bananaGrad)"/>
  <path d="M190 40 Q200 25 215 30 Q205 40 190 40 Z" fill="url(#bananaGrad)"/>
  <polygon points="160,110 163,117 170,117 165,122 167,129 160,125 153,129 155,122 150,117 157,117" fill="#fde047"/>
</g>
<!-- Text Labels -->
<text x="296" y="148" text-anchor="end" font-family="Pretendard,Malgun Gothic,sans-serif" font-size="20" font-weight="900" fill="#4ade80">정글 덩굴 스윙 타잔</text>
<text x="296" y="166" text-anchor="end" font-family="Pretendard,Arial,sans-serif" font-size="10" font-weight="700" fill="#a7f3d0" letter-spacing="2">JUNGLE VINE SWINGER</text>
<rect x="0.5" y="0.5" width="319" height="179" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.15"/>
</svg>"""

jungle_html = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>정글 덩굴 스윙 타잔</title>
<link rel="icon" href="data:,">
<style>
:root {
  --emerald: #10b981;
  --green: #22c55e;
  --gold: #fde047;
  --bg: #062e1c;
  --border: rgba(34, 197, 94, 0.3);
}
* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; margin: 0; padding: 0; }
html, body {
  height: 100vh; height: 100dvh;
  margin: 0;
  overflow: hidden;
  touch-action: manipulation;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
  color: #fff;
  background: var(--bg);
}
body {
  background: radial-gradient(circle at 50% 10%, #064e3b 0%, #022c22 100%);
}
.wrap {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 100vh; height: 100dvh;
  margin: auto;
  padding: 10px 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
h1 {
  font-size: clamp(19px, 5vw, 24px);
  color: #d1fae5;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  gap: 6px;
}
.sub {
  font-size: 11px;
  font-weight: 700;
  color: #6ee7b7;
  margin-top: 2px;
}
.hud {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}
.chip {
  padding: 6px 4px;
  text-align: center;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(6px);
  border: 1px solid var(--border);
  font-size: 11px;
  color: #a7f3d0;
}
.chip b {
  display: block;
  font-size: 16px;
  color: #fff;
  margin-top: 2px;
}
#game-box {
  position: relative;
  flex: 1;
  min-height: 0;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--border);
  background: radial-gradient(circle at 50% 20%, rgba(34, 197, 94, 0.15), transparent 70%), rgba(2, 44, 34, 0.7);
  box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.6);
}
canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  touch-action: none;
}
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: #6ee7b7;
  padding: 0 4px;
}
.home-link {
  color: #fde047;
  font-weight: 900;
  text-decoration: none;
  font-size: 12px;
}
.overlay {
  position: fixed;
  z-index: 20;
  inset: 0;
  padding: 20px;
  display: grid;
  place-items: center;
  background: rgba(2, 44, 34, 0.85);
  backdrop-filter: blur(10px);
}
.overlay.hidden { display: none; }
.card {
  width: min(380px, 100%);
  padding: 24px 20px;
  text-align: center;
  border-radius: 24px;
  border: 1px solid var(--green);
  background: linear-gradient(160deg, #064e3b, #022c22);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
}
.card h2 {
  margin: 0 0 10px;
  font-size: 22px;
  color: #fde047;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}
.card p {
  margin: 0 0 16px;
  font-size: 13px;
  line-height: 1.6;
  color: #d1fae5;
}
.btn {
  padding: 12px 26px;
  border: 0;
  border-radius: 14px;
  background: linear-gradient(135deg, #22c55e, #10b981);
  color: #062e1c;
  font-size: 16px;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
}
.btn:active { transform: scale(0.96); }
</style>
</head>
<body>
<main class="wrap">
  <header>
    <div>
      <h1>🐒 정글 덩굴 스윙 타잔</h1>
      <div class="sub">화면을 터치해 덩굴을 잡고 날아가 바나나를 모으세요!</div>
    </div>
    <div class="chip" style="min-width:65px">최고 <b id="best">0</b></div>
  </header>
  <section class="hud">
    <div class="chip">점수<b id="score">0</b></div>
    <div class="chip">남은 시간<b id="timer">45초</b></div>
    <div class="chip">바나나<b id="bananas">0개</b></div>
    <div class="chip">콤보<b id="combo">0x</b></div>
  </section>
  <div id="game-box">
    <canvas id="cvs"></canvas>
  </div>
  <footer class="footer">
    <span>🌴 덩굴 흔들릴 때 탭하면 점프! 다음 덩굴 근처에서 착지!</span>
    <a class="home-link" href="../index.html">← 홈</a>
  </footer>
</main>

<div class="overlay" id="startOverlay">
  <div class="card">
    <div style="font-size:48px;margin-bottom:8px">🐒🌴🍌</div>
    <h2>정글 덩굴 스윙 타잔</h2>
    <p>아기 원숭이와 함께 신나는 정글 여행을 떠나요!<br>덩굴이 앞뒤로 흔들릴 때 화면을 톡! 탭하면<br>바람을 타고 시원하게 점프해요!<br><br>공중에 뜬 바나나와 별을 모으고 다음 덩굴을 잡으세요!</p>
    <button class="btn" id="startBtn">정글 탐험 출발!</button>
  </div>
</div>

<div class="overlay hidden" id="endOverlay">
  <div class="card">
    <div style="font-size:48px;margin-bottom:8px" id="endEmoji">🍌</div>
    <h2 id="endTitle">정글 탐험 완료!</h2>
    <p id="endText"></p>
    <button class="btn" id="restartBtn">다시 달리기</button>
  </div>
</div>

<script>
(()=>{'use strict';
const KEY = 'jungle_vine_swinger_best';
const AUD = window.AudioContext || window.webkitAudioContext;
let actx = null;

function playSound(type) {
  try {
    if (!actx) actx = new AUD();
    if (actx.state === 'suspended') actx.resume();
    let now = actx.currentTime;
    if (type === 'jump') {
      let osc = actx.createOscillator(), g = actx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(300, now);
      osc.frequency.exponentialRampToValueAtTime(700, now + 0.15);
      g.gain.setValueAtTime(0.2, now);
      g.gain.linearRampToValueAtTime(0.001, now + 0.15);
      osc.connect(g); g.connect(actx.destination);
      osc.start(now); osc.stop(now + 0.15);
    } else if (type === 'collect') {
      let osc = actx.createOscillator(), g = actx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.setValueAtTime(1200, now + 0.06);
      g.gain.setValueAtTime(0.2, now);
      g.gain.linearRampToValueAtTime(0.001, now + 0.12);
      osc.connect(g); g.connect(actx.destination);
      osc.start(now); osc.stop(now + 0.12);
    } else if (type === 'catch') {
      let osc = actx.createOscillator(), g = actx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(500, now);
      g.gain.setValueAtTime(0.2, now);
      g.gain.linearRampToValueAtTime(0.001, now + 0.08);
      osc.connect(g); g.connect(actx.destination);
      osc.start(now); osc.stop(now + 0.08);
    } else if (type === 'bounce') {
      let osc = actx.createOscillator(), g = actx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(550, now + 0.2);
      g.gain.setValueAtTime(0.25, now);
      g.gain.linearRampToValueAtTime(0.001, now + 0.2);
      osc.connect(g); g.connect(actx.destination);
      osc.start(now); osc.stop(now + 0.2);
    }
  } catch(e) {}
}

const canvas = document.getElementById('cvs');
const ctx = canvas.getContext('2d');
let W = 0, H = 0;

function resize() {
  const rect = canvas.parentElement.getBoundingClientRect();
  W = canvas.width = rect.width;
  H = canvas.height = rect.height;
}
window.addEventListener('resize', resize);
resize();

let score = 0, timeLeft = 45, bananasCount = 0, combo = 0, running = false, timerInterval = null;
let cameraX = 0;

let monkey = {
  x: 0, y: 0,
  vx: 0, vy: 0,
  onVine: true,
  vineIdx: 0,
  angle: 0,
  angVel: 0.05,
  state: 'swing'
};

let vines = [];
let items = [];
let particles = [];
let floaters = [];

function initWorld() {
  cameraX = 0;
  vines = [];
  items = [];
  particles = [];
  floaters = [];

  let curX = W * 0.3;
  for (let i = 0; i < 20; i++) {
    let len = H * (0.45 + Math.random() * 0.15);
    vines.push({
      x: curX,
      y: 0,
      len: len,
      angle: -0.6 + Math.random() * 0.3,
      angVel: 0.045
    });

    if (i > 0) {
      let midX = curX - (curX - vines[i-1].x) / 2;
      let types = ['banana', 'banana', 'star', 'star', 'pineapple'];
      let chosen = types[Math.floor(Math.random() * types.length)];
      items.push({
        x: midX + (Math.random() - 0.5) * 40,
        y: H * (0.35 + Math.random() * 0.3),
        type: chosen,
        r: 18,
        collected: false
      });
    }
    curX += W * (0.55 + Math.random() * 0.15);
  }

  monkey.vineIdx = 0;
  monkey.onVine = true;
  monkey.state = 'swing';
  monkey.angle = -0.5;
  monkey.angVel = 0.04;
  updateMonkeyOnVine();
}

function updateMonkeyOnVine() {
  let v = vines[monkey.vineIdx];
  if (!v) return;
  monkey.x = v.x + Math.sin(v.angle) * v.len;
  monkey.y = v.y + Math.cos(v.angle) * v.len;
}

function handleTap() {
  if (!running) return;

  if (monkey.onVine) {
    let v = vines[monkey.vineIdx];
    let spd = v.angVel * v.len * 1.35;
    let tx = Math.cos(v.angle) * spd;
    let ty = -Math.sin(v.angle) * spd;

    monkey.vx = Math.max(3.5, tx + 4.5);
    monkey.vy = ty - 4.5;
    monkey.onVine = false;
    monkey.state = 'flying';
    playSound('jump');
    spawnBurst(monkey.x, monkey.y, '#4ade80', 10);
  }
}

function spawnBurst(x, y, color, count = 12) {
  for (let i = 0; i < count; i++) {
    let a = Math.random() * Math.PI * 2;
    let s = 1.5 + Math.random() * 4;
    particles.push({
      x, y,
      vx: Math.cos(a) * s,
      vy: Math.sin(a) * s,
      r: 3 + Math.random() * 3,
      color,
      alpha: 1
    });
  }
}

function spawnFloater(x, y, text, color = '#fde047') {
  floaters.push({ x, y, text, color, alpha: 1, vy: -1.2 });
}

function loop() {
  ctx.clearRect(0, 0, W, H);

  let bgOffset = (cameraX * 0.2) % W;
  ctx.fillStyle = 'rgba(4, 120, 87, 0.15)';
  ctx.beginPath();
  ctx.arc(W * 0.2 - bgOffset, H * 0.3, 80, 0, Math.PI * 2);
  ctx.arc(W * 0.7 - bgOffset, H * 0.4, 100, 0, Math.PI * 2);
  ctx.arc(W * 1.2 - bgOffset, H * 0.3, 80, 0, Math.PI * 2);
  ctx.fill();

  let targetCamX = monkey.x - W * 0.3;
  cameraX += (targetCamX - cameraX) * 0.1;

  ctx.save();
  ctx.translate(-cameraX, 0);

  for (let i = 0; i < vines.length; i++) {
    let v = vines[i];
    v.angle += v.angVel;
    if (Math.abs(v.angle) > 0.75) {
      v.angVel = -v.angVel;
    }

    let endX = v.x + Math.sin(v.angle) * v.len;
    let endY = v.y + Math.cos(v.angle) * v.len;

    ctx.strokeStyle = '#15803d';
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(v.x, v.y);
    ctx.quadraticCurveTo(v.x + Math.sin(v.angle * 0.5) * (v.len * 0.5), v.len * 0.5, endX, endY);
    ctx.stroke();

    ctx.fillStyle = '#166534';
    ctx.beginPath();
    ctx.arc(endX, endY, 6, 0, Math.PI * 2);
    ctx.fill();
  }

  for (let item of items) {
    if (item.collected) continue;
    ctx.save();
    ctx.translate(item.x, item.y);
    ctx.font = '24px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    let emoji = item.type === 'banana' ? '🍌' : item.type === 'star' ? '⭐' : '🍍';
    ctx.fillText(emoji, 0, 0);
    ctx.restore();

    if (!item.collected) {
      let dist = Math.hypot(monkey.x - item.x, monkey.y - item.y);
      if (dist < item.r + 20) {
        item.collected = true;
        let pts = item.type === 'banana' ? 50 : item.type === 'star' ? 100 : 150;
        let finalPts = pts + combo * 10;
        score += finalPts;
        if (item.type === 'banana') bananasCount++;
        playSound('collect');
        spawnBurst(item.x, item.y, item.type === 'star' ? '#fde047' : '#22c55e', 14);
        spawnFloater(item.x, item.y, `+${finalPts}`);
        document.getElementById('score').textContent = score;
        document.getElementById('bananas').textContent = bananasCount + '개';
      }
    }
  }

  if (monkey.onVine) {
    let v = vines[monkey.vineIdx];
    monkey.angle = v.angle;
    updateMonkeyOnVine();
  } else {
    monkey.vy += 0.24;
    monkey.x += monkey.vx;
    monkey.y += monkey.vy;

    for (let i = monkey.vineIdx + 1; i < vines.length; i++) {
      let v = vines[i];
      let endX = v.x + Math.sin(v.angle) * v.len;
      let endY = v.y + Math.cos(v.angle) * v.len;
      let dist = Math.hypot(monkey.x - endX, monkey.y - endY);

      if (dist < 42 && monkey.vy > -1) {
        monkey.onVine = true;
        monkey.vineIdx = i;
        monkey.state = 'swing';
        combo++;
        score += 80 * combo;
        document.getElementById('score').textContent = score;
        document.getElementById('combo').textContent = combo + 'x';
        playSound('catch');
        spawnBurst(endX, endY, '#fde047', 16);
        spawnFloater(endX, endY - 20, `연속 스윙 ${combo}x!`, '#4ade80');
        break;
      }
    }

    if (monkey.y > H * 0.85) {
      monkey.vy = -8.5;
      monkey.y = H * 0.85;
      combo = 0;
      document.getElementById('combo').textContent = '0x';
      playSound('bounce');
      spawnBurst(monkey.x, monkey.y, '#10b981', 16);
      spawnFloater(monkey.x, monkey.y - 15, '통통 점프!', '#6ee7b7');
    }
  }

  let lastVine = vines[vines.length - 1];
  if (lastVine && lastVine.x - cameraX < W * 2) {
    let newX = lastVine.x + W * (0.55 + Math.random() * 0.15);
    let len = H * (0.45 + Math.random() * 0.15);
    vines.push({
      x: newX,
      y: 0,
      len: len,
      angle: -0.6 + Math.random() * 0.3,
      angVel: 0.045
    });
    items.push({
      x: newX - W * 0.25,
      y: H * (0.35 + Math.random() * 0.3),
      type: Math.random() > 0.4 ? 'banana' : 'star',
      r: 18,
      collected: false
    });
  }

  ctx.save();
  ctx.translate(monkey.x, monkey.y);
  let rot = monkey.onVine ? monkey.angle : Math.atan2(monkey.vy, monkey.vx);
  ctx.rotate(rot);

  // Tail
  ctx.strokeStyle = '#b45309';
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(-10, 8);
  ctx.quadraticCurveTo(-22, 16, -18, 26);
  ctx.stroke();

  // Body
  ctx.fillStyle = '#b45309';
  ctx.beginPath();
  ctx.ellipse(0, 10, 13, 15, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#fde68a';
  ctx.beginPath();
  ctx.ellipse(0, 12, 8, 10, 0, 0, Math.PI * 2);
  ctx.fill();

  // Head
  ctx.fillStyle = '#b45309';
  ctx.beginPath();
  ctx.arc(0, -6, 13, 0, Math.PI * 2);
  ctx.fill();

  // Ears
  ctx.fillStyle = '#fde68a';
  ctx.beginPath();
  ctx.arc(-13, -6, 5, 0, Math.PI * 2);
  ctx.arc(13, -6, 5, 0, Math.PI * 2);
  ctx.fill();

  // Face
  ctx.beginPath();
  ctx.ellipse(0, -3, 9, 7, 0, 0, Math.PI * 2);
  ctx.fill();

  // Eyes & Smile
  ctx.fillStyle = '#0f172a';
  ctx.beginPath();
  ctx.arc(-4, -5, 2.5, 0, Math.PI * 2);
  ctx.arc(4, -5, 2.5, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = '#78350f';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(0, -1, 3, 0.2, Math.PI - 0.2);
  ctx.stroke();

  ctx.restore();

  for (let i = particles.length - 1; i >= 0; i--) {
    let p = particles[i];
    p.x += p.vx; p.y += p.vy;
    p.alpha -= 0.035;
    if (p.alpha <= 0) {
      particles.splice(i, 1);
      continue;
    }
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.globalAlpha = p.alpha;
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  for (let i = floaters.length - 1; i >= 0; i--) {
    let f = floaters[i];
    f.y += f.vy;
    f.alpha -= 0.025;
    if (f.alpha <= 0) {
      floaters.splice(i, 1);
      continue;
    }
    ctx.font = 'bold 15px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = f.color;
    ctx.globalAlpha = f.alpha;
    ctx.fillText(f.text, f.x, f.y);
    ctx.globalAlpha = 1;
  }

  ctx.restore();

  if (running) requestAnimationFrame(loop);
}

function startGame() {
  score = 0; timeLeft = 45; bananasCount = 0; combo = 0; running = true;
  document.getElementById('score').textContent = '0';
  document.getElementById('timer').textContent = '45초';
  document.getElementById('bananas').textContent = '0개';
  document.getElementById('combo').textContent = '0x';
  document.getElementById('startOverlay').classList.add('hidden');
  document.getElementById('endOverlay').classList.add('hidden');

  resize();
  initWorld();
  loop();

  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById('timer').textContent = timeLeft + '초';
    if (timeLeft <= 0) endGame();
  }, 1000);
}

function endGame() {
  running = false;
  clearInterval(timerInterval);
  let best = Math.max(+localStorage.getItem(KEY) || 0, score);
  localStorage.setItem(KEY, best);
  document.getElementById('best').textContent = best;

  document.getElementById('endTitle').textContent = '탐험 완료!';
  document.getElementById('endText').textContent = `총 ${score}점을 얻고 바나나 ${bananasCount}개를 획득했어요!`;
  document.getElementById('endOverlay').classList.remove('hidden');
}

canvas.addEventListener('pointerdown', (e) => {
  e.preventDefault();
  handleTap();
});

document.getElementById('best').textContent = localStorage.getItem(KEY) || 0;
document.getElementById('startBtn').addEventListener('pointerdown', startGame);
document.getElementById('restartBtn').addEventListener('pointerdown', startGame);
})();
</script>
</body>
</html>"""

with open(os.path.join(jungle_dir, "thumb.svg"), "w", encoding="utf-8") as f:
    f.write(jungle_svg)
with open(os.path.join(jungle_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(jungle_html)
print("Created jungle-vine-swinger")

print("All game files generated successfully!")
