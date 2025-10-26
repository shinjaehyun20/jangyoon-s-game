// 달리는 장윤이 - 게임 로직
const gameArea = document.getElementById('gameArea');
const player = document.getElementById('player');
const scoreEl = document.getElementById('score');
const timeEl = document.getElementById('time');
const startBtn = document.getElementById('startBtn');
const upBtn = document.getElementById('upBtn');
const downBtn = document.getElementById('downBtn');
const message = document.getElementById('message');

let score = 0;
let timeLeft = 30;
let gameTimer = null;
let spawnTimer = null;
let gameActive = false;
let playerPos = 50; // 퍼센트 단위
let items = new Set();
let animationId = null;

function resetGame() {
    score = 0;
    timeLeft = 30;
    gameActive = false;
    playerPos = 50;
    scoreEl.textContent = score;
    timeEl.textContent = timeLeft;
    message.classList.add('hidden');
    items.forEach(item => item.remove());
    items.clear();
    player.style.top = `${playerPos}%`;
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
}

function startGame() {
    if (gameActive) return;
    
    resetGame();
    gameActive = true;
    startBtn.textContent = '다시 시작';
    message.classList.add('hidden');
    
    // 타이머 시작
    gameTimer = setInterval(() => {
        timeLeft--;
        timeEl.textContent = timeLeft;
        if (timeLeft <= 0) endGame();
    }, 1000);

    // 아이템 생성 시작
    spawnTimer = setInterval(() => {
        // 더 자주 아이템 생성
        if (Math.random() < 0.7) spawnItem();
    }, 800);

    // 게임 루프 시작
    gameLoop();
}

function endGame() {
    gameActive = false;
    clearInterval(gameTimer);
    clearInterval(spawnTimer);
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
    
    const highScore = localStorage.getItem('runnerHighScore') || 0;
    if (score > highScore) {
        localStorage.setItem('runnerHighScore', score);
        message.textContent = `새로운 기록! ${score}점 달성! 🎉`;
    } else {
        message.textContent = `게임 종료! ${score}점 획득! �`;
    }
    message.classList.remove('hidden');
    startBtn.textContent = '다시 시작';
}

function spawnItem() {
    if (!gameActive) return;
    
    const item = document.createElement('div');
    item.className = 'item';
    
    // 아이템 세로 위치 (10%-90%)
    const y = 10 + Math.random() * 80;
    item.style.top = `${y}%`;
    
    // 게임 영역에 추가
    gameArea.appendChild(item);
    items.add(item);
}

function createScorePopup(x, y) {
    const popup = document.createElement('div');
    popup.className = 'score-popup';
    popup.textContent = '+10';
    popup.style.left = x + 'px';
    popup.style.top = y + 'px';
    gameArea.appendChild(popup);
    
    // 애니메이션 끝나면 제거
    setTimeout(() => popup.remove(), 600);
}

function gameLoop() {
    if (!gameActive) return;

    // 아이템 이동 및 충돌 검사
    items.forEach(item => {
        const x = item.offsetLeft - 6; // 더 빠른 이동
        
        if (x < -50) {
            items.delete(item);
            item.remove();
        } else {
            item.style.left = x + 'px';
            
            // 충돌 검사
            const itemRect = item.getBoundingClientRect();
            const playerRect = player.getBoundingClientRect();
            
            if (!(itemRect.right < playerRect.left || 
                itemRect.left > playerRect.right || 
                itemRect.bottom < playerRect.top || 
                itemRect.top > playerRect.bottom)) {
                
                // 아이템 획득!
                items.delete(item);
                item.remove();
                score += 10;
                scoreEl.textContent = score;
                createScorePopup(itemRect.left, itemRect.top);
            }
        }
    });

    animationId = requestAnimationFrame(gameLoop);
}

// 플레이어 이동
function movePlayer(direction) {
    if (!gameActive) return;
    
    const step = 10;
    const newPos = direction === 'up' 
        ? Math.max(10, playerPos - step)
        : Math.min(90, playerPos + step);
    
    if (newPos !== playerPos) {
        playerPos = newPos;
        player.style.top = `${playerPos}%`;
    }
}

// 키보드 컨트롤
window.addEventListener('keydown', e => {
    if (e.key === 'ArrowUp' || e.key === 'w') movePlayer('up');
    if (e.key === 'ArrowDown' || e.key === 's') movePlayer('down');
    if (e.key === ' ' && !gameActive) startGame();
});

// 터치/마우스 컨트롤
upBtn.addEventListener('pointerdown', () => {
    const interval = setInterval(() => movePlayer('up'), 50);
    const stopMoving = () => clearInterval(interval);
    upBtn.addEventListener('pointerup', stopMoving, {once: true});
    upBtn.addEventListener('pointerleave', stopMoving, {once: true});
});

downBtn.addEventListener('pointerdown', () => {
    const interval = setInterval(() => movePlayer('down'), 50);
    const stopMoving = () => clearInterval(interval);
    downBtn.addEventListener('pointerup', stopMoving, {once: true});
    downBtn.addEventListener('pointerleave', stopMoving, {once: true});
});

// 시작 버튼
startBtn.addEventListener('click', startGame);

// 게임 영역 포커스 (키보드 컨트롤용)
gameArea.addEventListener('click', () => gameArea.focus());

// 초기화
resetGame();

// --- Mobile hold-and-drag support (vertical) ---
let dragging = false;
let dragPointerId = null;

function startVerticalDrag(e) {
    // ensure keyboard focus remains on the game area so arrow keys still work
    try { gameArea.focus(); } catch (err) {}
    dragging = true;
    dragPointerId = e.pointerId;
    gameArea.setPointerCapture(dragPointerId);
}

function stopVerticalDrag(e) {
    if (!dragging) return;
    dragging = false;
    try { gameArea.releasePointerCapture(dragPointerId); } catch (er) {}
    dragPointerId = null;
}

function onVerticalMove(e) {
    if (!dragging || e.pointerId !== dragPointerId) return;
    const rect = gameArea.getBoundingClientRect();
    // calculate percentage position (10%..90%)
    const y = e.clientY - rect.top;
    const pct = (y / rect.height) * 100;
    const clamped = Math.max(10, Math.min(90, pct));
    playerPos = clamped;
    player.style.top = `${playerPos}%`;
}

// attach to player and area
player.addEventListener('pointerdown', startVerticalDrag);
gameArea.addEventListener('pointerdown', (e) => {
    if (e.target === gameArea) {
        startVerticalDrag(e);
        onVerticalMove(e);
    }
});
window.addEventListener('pointermove', onVerticalMove);
window.addEventListener('pointerup', stopVerticalDrag);
window.addEventListener('pointercancel', stopVerticalDrag);