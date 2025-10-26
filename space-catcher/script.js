// Simple 'Space Catcher' game for kids
// Controls: left/right arrow or touch buttons. Collect stars for points within the timer.

const gameArea = document.getElementById('gameArea');
const player = document.getElementById('player');
const scoreEl = document.getElementById('score');
const timeEl = document.getElementById('time');
const startBtn = document.getElementById('startBtn');
const leftBtn = document.getElementById('leftBtn');
const rightBtn = document.getElementById('rightBtn');
const message = document.getElementById('message');

let score = 0;
let timeLeft = 60;
let gameTimer = null;
let spawnTimer = null;
let keys = {left:false,right:false};
let gameActive = false;
let playerX = 0; // percentage

function resetGame(){
  score = 0; timeLeft = 60; gameActive=false;
  scoreEl.textContent = score; timeEl.textContent = timeLeft;
  message.classList.add('hidden');
  // remove existing stars
  document.querySelectorAll('.star').forEach(s=>s.remove());
  // reset player
  player.style.left = '50%';
}

function startGame(){
  resetGame();
  gameActive = true;
  startBtn.textContent = '재시작';
  // timers
  gameTimer = setInterval(()=>{
    timeLeft -= 1;
    timeEl.textContent = timeLeft;
    if(timeLeft<=0){endGame()}
  },1000);

  spawnTimer = setInterval(spawnStar, 900);
  // start movement loop
  requestAnimationFrame(gameLoop);
}

function endGame(){
  gameActive=false;
  clearInterval(gameTimer); clearInterval(spawnTimer);
  message.textContent = `시간 종료! 점수: ${score}점 🎉`;
  message.classList.remove('hidden');
}

function spawnStar(){
  const star = document.createElement('div');
  star.className = 'star';
  // random x
  const x = Math.random()* (gameArea.clientWidth - 42);
  star.style.left = x + 'px';
  star.style.top = '-50px';
  // falling speed
  star.dataset.speed = 1 + Math.random()*2.6; // px per frame-ish
  gameArea.appendChild(star);
}

function gameLoop(){
  if(!gameActive) return;
  // move player
  const rect = gameArea.getBoundingClientRect();
  const step = rect.width * 0.016; // movement per frame
  const curLeft = player.offsetLeft;
  if(keys.left){
    player.style.left = Math.max(6, curLeft - step) + 'px';
  } else if(keys.right){
    player.style.left = Math.min(rect.width - player.clientWidth - 6, curLeft + step) + 'px';
  }

  // move stars
  document.querySelectorAll('.star').forEach(star=>{
    const top = parseFloat(star.style.top);
    star.style.top = (top + parseFloat(star.dataset.speed)*4) + 'px';

    // collision with player
    const sRect = star.getBoundingClientRect();
    const pRect = player.getBoundingClientRect();
    if(!(sRect.right < pRect.left || sRect.left > pRect.right || sRect.bottom < pRect.top || sRect.top > pRect.bottom)){
      // caught
      star.remove();
      score += 10;
      scoreEl.textContent = score;
      // small celebration
      flashPlayer();
    }

    // remove if out of bottom
    if(parseFloat(star.style.top) > rect.height + 60){
      star.remove();
    }
  });

  requestAnimationFrame(gameLoop);
}

function flashPlayer(){
  player.style.transform = 'translateX(-50%) scale(1.07)';
  setTimeout(()=>{player.style.transform='translateX(-50%)'},120);
}

// controls
window.addEventListener('keydown', e=>{
  if(e.key === 'ArrowLeft') keys.left = true;
  if(e.key === 'ArrowRight') keys.right = true;
});
window.addEventListener('keyup', e=>{
  if(e.key === 'ArrowLeft') keys.left = false;
  if(e.key === 'ArrowRight') keys.right = false;
});

leftBtn.addEventListener('pointerdown', ()=>{keys.left=true});
leftBtn.addEventListener('pointerup', ()=>{keys.left=false});
leftBtn.addEventListener('pointerleave', ()=>{keys.left=false});
rightBtn.addEventListener('pointerdown', ()=>{keys.right=true});
rightBtn.addEventListener('pointerup', ()=>{keys.right=false});
rightBtn.addEventListener('pointerleave', ()=>{keys.right=false});

startBtn.addEventListener('click', ()=>{
  if(gameActive) {endGame(); resetGame();}
  startGame();
});

// focus game area so keyboard works
gameArea.addEventListener('click', ()=>gameArea.focus());

// initial setup: add small decorative eye on player
(function decorate(){
  const eye = document.createElement('div');
  eye.className = 'player-eye';
  player.appendChild(eye);
})();

// friendly hint: on mobile, press buttons to move

resetGame();

// --- Mobile drag (hold-and-drag) support ---
let dragging = false;
let pointerId = null;

function startDrag(evt){
  // preventDefault isn't needed because touch-action is set in CSS;
  // ensure the game area has keyboard focus so arrow keys keep working
  try { gameArea.focus(); } catch(e){}
  dragging = true;
  pointerId = evt.pointerId;
  gameArea.setPointerCapture(pointerId);
}

function stopDrag(evt){
  if(!dragging) return;
  dragging = false;
  try{ gameArea.releasePointerCapture(pointerId); }catch(e){}
  pointerId = null;
}

function onDragMove(evt){
  if(!dragging || evt.pointerId !== pointerId) return;
  // calculate new left position constrained to game area
  const rect = gameArea.getBoundingClientRect();
  const x = evt.clientX - rect.left; // px from left
  const clamped = Math.max(6, Math.min(rect.width - player.clientWidth - 6, x - player.clientWidth/2));
  player.style.left = clamped + 'px';
}

// Start drag when the player element is pressed, or when touching game area (optional)
player.addEventListener('pointerdown', startDrag);
gameArea.addEventListener('pointerdown', (e)=>{
  // if touching outside the player, allow dragging by moving player to pointer
  if(e.target === gameArea){
    startDrag(e);
    onDragMove(e);
  }
});
window.addEventListener('pointermove', onDragMove);
window.addEventListener('pointerup', stopDrag);
window.addEventListener('pointercancel', stopDrag);
