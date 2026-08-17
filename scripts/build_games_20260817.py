import os

ROOT = r"D:\workspace\projects\active\jangyoon-s-game"

# 1. Star Whale Voyage
whale_dir = os.path.join(ROOT, "star-whale-voyage")
os.makedirs(whale_dir, exist_ok=True)

whale_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" role="img" aria-label="아기별고래 우주 유영">
<defs>
  <linearGradient id="spaceOcean" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#0f172a"/>
    <stop offset="60%" stop-color="#1e1b4b"/>
    <stop offset="100%" stop-color="#0369a1"/>
  </linearGradient>
  <linearGradient id="whaleGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#67e8f9"/>
    <stop offset="100%" stop-color="#3b82f6"/>
  </linearGradient>
  <filter id="glowW" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="320" height="180" rx="18" fill="url(#spaceOcean)"/>
<g fill="#ffffff" opacity="0.6">
  <circle cx="40" cy="30" r="1.5"/>
  <circle cx="95" cy="55" r="1"/>
  <circle cx="280" cy="35" r="1.5"/>
  <circle cx="250" cy="140" r="1"/>
  <circle cx="70" cy="150" r="1.5"/>
</g>
<!-- Aurora Stream -->
<path d="M-20 120 Q80 60 160 110 T340 70" fill="none" stroke="#a855f7" stroke-width="8" opacity="0.3" filter="url(#glowW)"/>
<path d="M-20 125 Q80 65 160 115 T340 75" fill="none" stroke="#38bdf8" stroke-width="4" opacity="0.5" filter="url(#glowW)"/>
<!-- Baby Star Whale -->
<g transform="translate(150, 85)">
  <!-- Whale Body -->
  <path d="M-40 0 C-40 -22 10 -25 35 -5 C45 2 55 12 60 10 C62 5 60 -10 68 -8 C72 -2 68 8 62 16 C55 22 40 20 25 18 C-5 18 -40 18 -40 0 Z" fill="url(#whaleGrad)" filter="url(#glowW)"/>
  <!-- Belly -->
  <path d="M-30 4 C-10 16 20 16 35 4 C15 10 -15 10 -30 4 Z" fill="#e0f2fe" opacity="0.8"/>
  <!-- Fin -->
  <path d="M-5 4 Q-12 18 5 12 Z" fill="#38bdf8"/>
  <!-- Eye -->
  <circle cx="-25" cy="-6" r="3" fill="#0f172a"/>
  <circle cx="-26" cy="-7" r="1" fill="#ffffff"/>
  <!-- Spout Stars -->
  <circle cx="-28" cy="-18" r="2.5" fill="#fde047" filter="url(#glowW)"/>
  <circle cx="-22" cy="-25" r="3" fill="#fbcfe8" filter="url(#glowW)"/>
  <circle cx="-32" cy="-28" r="2" fill="#67e8f9" filter="url(#glowW)"/>
</g>
<!-- Stardust Orbs -->
<circle cx="60" cy="80" r="8" fill="#fde047" filter="url(#glowW)"/>
<circle cx="260" cy="90" r="9" fill="#f472b6" filter="url(#glowW)"/>
<text x="296" y="148" text-anchor="end" font-family="Pretendard,Malgun Gothic,sans-serif" font-size="20" font-weight="900" fill="#67e8f9">아기별고래 우주 유영</text>
<text x="296" y="166" text-anchor="end" font-family="Pretendard,Arial,sans-serif" font-size="10" font-weight="700" fill="#bae6fd" letter-spacing="2">STAR WHALE VOYAGE</text>
<rect x="0.5" y="0.5" width="319" height="179" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.15"/>
</svg>"""

whale_html = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>아기별고래 우주 유영</title>
<link rel="icon" href="data:,">
<style>
:root{--navy:#0f172a;--cyan:#38bdf8;--gold:#fde047;--purple:#c084fc;--pink:#f472b6}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100vh;height:100dvh;margin:0;overflow:hidden;touch-action:manipulation;font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:#fff;background:#0b0f19}
body{background:radial-gradient(circle at 50% 20%,#1e1b4b 0,transparent 60%),linear-gradient(180deg,#0f172a 0%,#031d38 100%)}
.wrap{position:relative;width:100%;max-width:520px;height:100vh;height:100dvh;margin:auto;padding:12px;display:flex;flex-direction:column;gap:8px;overflow:hidden}
header{display:flex;align-items:center;justify-content:space-between}
h1{font-size:clamp(20px,5.5vw,26px);margin:0;color:#e0f2fe;text-shadow:0 2px 8px rgba(0,0,0,.4)}
.sub{font-size:11px;font-weight:700;color:#7dd3fc;margin-top:2px}
.hud{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.chip{padding:6px;text-align:center;border-radius:12px;background:rgba(255,255,255,.08);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.15);font-size:11px;color:#bae6fd}
.chip b{display:block;font-size:17px;color:#fff;margin-top:2px}
#canvas-box{position:relative;flex:1;min-height:0;border-radius:20px;overflow:hidden;border:1px solid rgba(56,189,248,.3);background:radial-gradient(circle at 50% 40%,rgba(56,189,248,.1),transparent 70%),rgba(10,15,30,.6);box-shadow:inset 0 0 20px rgba(0,0,0,.5)}
canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none}
.footer{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#7dd3fc}
.home-link{color:#fde047;font-weight:900;text-decoration:none;font-size:12px}
.overlay{position:fixed;z-index:10;inset:0;padding:20px;display:grid;place-items:center;background:rgba(11,15,25,.8);backdrop-filter:blur(8px)}
.overlay.hidden{display:none}
.card{width:min(380px,100%);padding:24px 20px;text-align:center;border-radius:24px;border:1px solid rgba(255,255,255,.2);background:linear-gradient(160deg,#1e1b4b,#0f172a);box-shadow:0 16px 40px rgba(0,0,0,.5)}
.card h2{margin:0 0 10px;font-size:24px;color:#fde047}
.card p{margin:0 0 16px;font-size:13px;line-height:1.6;color:#e0f2fe}
.btn{padding:12px 24px;border:0;border-radius:14px;background:linear-gradient(135deg,#38bdf8,#3b82f6);color:#fff;font-size:16px;font-weight:900;cursor:pointer;box-shadow:0 4px 12px rgba(59,130,246,.4)}
.btn:active{transform:scale(.96)}
</style>
</head>
<body>
<main class="wrap">
<header>
  <div><h1>🐳 아기별고래 우주 유영</h1><div class="sub">화면을 터치해 별고래를 유영시키고 별가루를 모아요!</div></div>
  <div class="chip" style="min-width:70px">최고 <b id="best">0</b></div>
</header>
<section class="hud">
  <div class="chip">별빛 점수<b id="score">0</b></div>
  <div class="chip">남은 시간<b id="timer">45초</b></div>
  <div class="chip">별가루<b id="stars">0개</b></div>
</section>
<div id="canvas-box"><canvas id="cvs"></canvas></div>
<footer class="footer"><span>✨ 화면을 드래그해 별고래를 부드럽게 헤엄치게 해요!</span><a class="home-link" href="../index.html">← 홈</a></footer>
</main>
<div class="overlay" id="startOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px">🐳✨🌌</div>
    <h2>아기별고래 우주 유영</h2>
    <p>은하수 바다를 자유롭게 헤엄쳐 보세요!<br>반짝이는 별가루를 먹으면 점수가 오르고<br>깜깜한 암석 장애물은 살짝 피해가요!</p>
    <button class="btn" id="startBtn">우주 유영 시작!</button>
  </div>
</div>
<div class="overlay hidden" id="endOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px" id="endEmoji">🌟</div>
    <h2 id="endTitle">유영 완료!</h2>
    <p id="endText"></p>
    <button class="btn" id="restartBtn">다시 유영하기</button>
  </div>
</div>
<script>
(()=>{'use strict';
const KEY='star_whale_voyage_best';
let canvas=document.getElementById('cvs'),ctx=canvas.getContext('2d');
let score=0,timeLeft=45,starsCollected=0,running=false,timerInterval=null;
let W=0,H=0;

function resize(){
  const rect=canvas.parentElement.getBoundingClientRect();
  W=canvas.width=rect.width;
  H=canvas.height=rect.height;
}
window.addEventListener('resize',resize);
resize();

const AUD=window.AudioContext||window.webkitAudioContext;
let actx=null;
function beep(f,type='sine',dur=0.15){
  try{
    if(!actx)actx=new AUD();
    let osc=actx.createOscillator(),g=actx.createGain();
    osc.type=type;osc.frequency.value=f;
    g.gain.setValueAtTime(0.2,actx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001,actx.currentTime+dur);
    osc.connect(g);g.connect(actx.destination);
    osc.start();osc.stop(actx.currentTime+dur);
  }catch(e){}
}

let whale={x:100,y:150,tx:100,ty:150,angle:0,tail:0};
let stars=[],rocks=[],particles=[];

function spawnItems(){
  if(!running)return;
  if(Math.random()<0.08){
    stars.push({
      x:W+30,y:Math.random()*(H-60)+30,
      r:14+Math.random()*6,
      color:['#fde047','#f472b6','#67e8f9','#a7f3d0'][Math.floor(Math.random()*4)],
      speed:2+Math.random()*1.5
    });
  }
  if(Math.random()<0.035){
    rocks.push({
      x:W+40,y:Math.random()*(H-60)+30,
      r:20+Math.random()*8,
      speed:1.5+Math.random()*1.2,
      angle:0,rotSpeed:(Math.random()-0.5)*0.05
    });
  }
}

canvas.addEventListener('pointermove',e=>{
  if(!running)return;
  let rect=canvas.getBoundingClientRect();
  whale.tx=e.clientX-rect.left;
  whale.ty=e.clientY-rect.top;
});
canvas.addEventListener('pointerdown',e=>{
  if(!running)return;
  let rect=canvas.getBoundingClientRect();
  whale.tx=e.clientX-rect.left;
  whale.ty=e.clientY-rect.top;
});

function spawnParticles(x,y,color,cnt){
  for(let i=0;i<cnt;i++){
    let ang=Math.random()*Math.PI*2,spd=1.5+Math.random()*3;
    particles.push({
      x,y,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd,
      r:2+Math.random()*3,color,alpha:1
    });
  }
}

function loop(){
  ctx.clearRect(0,0,W,H);

  // Smooth whale movement
  let dx=whale.tx-whale.x,dy=whale.ty-whale.y;
  whale.x+=dx*0.08;
  whale.y+=dy*0.08;
  whale.angle=Math.atan2(dy,dx+30)*0.3;
  whale.tail+=0.12;

  // Stardust trail
  if(Math.random()<0.4){
    particles.push({
      x:whale.x-25,y:whale.y+(Math.random()-0.5)*10,
      vx:-2,vy:(Math.random()-0.5)*1,
      r:2+Math.random()*2,color:'#67e8f9',alpha:0.8
    });
  }

  // Update & draw stars
  for(let i=stars.length-1;i>=0;i--){
    let s=stars[i];
    s.x-=s.speed;

    // Check collision
    let dist=Math.hypot(whale.x-s.x,whale.y-s.y);
    if(dist<s.r+24){
      stars.splice(i,1);
      score+=100;
      starsCollected++;
      beep(520+starsCollected*10,'sine',0.12);
      spawnParticles(s.x,s.y,s.color,10);
      document.getElementById('score').textContent=score;
      document.getElementById('stars').textContent=starsCollected+'개';
      continue;
    }

    ctx.save();
    ctx.translate(s.x,s.y);
    ctx.fillStyle=s.color;
    ctx.beginPath();
    ctx.arc(0,0,s.r,0,Math.PI*2);
    ctx.fill();
    ctx.fillStyle='#ffffff';
    ctx.beginPath();
    ctx.arc(-s.r*0.3,-s.r*0.3,s.r*0.3,0,Math.PI*2);
    ctx.fill();
    ctx.restore();

    if(s.x<-40)stars.splice(i,1);
  }

  // Update & draw rocks
  for(let i=rocks.length-1;i>=0;i--){
    let r=rocks[i];
    r.x-=r.speed;
    r.angle+=r.rotSpeed;

    // Check collision
    let dist=Math.hypot(whale.x-r.x,whale.y-r.y);
    if(dist<r.r+18){
      rocks.splice(i,1);
      score=Math.max(0,score-80);
      beep(180,'sawtooth',0.2);
      spawnParticles(r.x,r.y,'#64748b',8);
      document.getElementById('score').textContent=score;
      continue;
    }

    ctx.save();
    ctx.translate(r.x,r.y);
    ctx.rotate(r.angle);
    ctx.fillStyle='#334155';
    ctx.strokeStyle='#64748b';
    ctx.lineWidth=2;
    ctx.beginPath();
    ctx.arc(0,0,r.r,0,Math.PI*2);
    ctx.fill();
    ctx.stroke();
    ctx.restore();

    if(r.x<-50)rocks.splice(i,1);
  }

  // Draw particles
  for(let i=particles.length-1;i>=0;i--){
    let p=particles[i];
    p.x+=p.vx;p.y+=p.vy;p.alpha-=0.025;
    if(p.alpha<=0){particles.splice(i,1);continue;}
    ctx.beginPath();
    ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=p.color;
    ctx.globalAlpha=p.alpha;
    ctx.fill();
    ctx.globalAlpha=1;
  }

  // Draw Whale
  ctx.save();
  ctx.translate(whale.x,whale.y);
  ctx.rotate(whale.angle);

  // Whale body
  ctx.fillStyle='#38bdf8';
  ctx.beginPath();
  ctx.ellipse(0,0,28,18,0,0,Math.PI*2);
  ctx.fill();

  // Belly
  ctx.fillStyle='#e0f2fe';
  ctx.beginPath();
  ctx.ellipse(4,6,18,8,0,0,Math.PI*2);
  ctx.fill();

  // Tail fin
  let tailOff=Math.sin(whale.tail)*6;
  ctx.fillStyle='#38bdf8';
  ctx.beginPath();
  ctx.moveTo(-24,0);
  ctx.lineTo(-38,-10+tailOff);
  ctx.lineTo(-34,tailOff);
  ctx.lineTo(-38,10+tailOff);
  ctx.closePath();
  ctx.fill();

  // Side fin
  ctx.fillStyle='#0284c7';
  ctx.beginPath();
  ctx.ellipse(2,4,8,4,0.4,0,Math.PI*2);
  ctx.fill();

  // Eye
  ctx.fillStyle='#0f172a';
  ctx.beginPath();
  ctx.arc(14,-4,3,0,Math.PI*2);
  ctx.fill();
  ctx.fillStyle='#ffffff';
  ctx.beginPath();
  ctx.arc(15,-5,1,0,Math.PI*2);
  ctx.fill();

  ctx.restore();

  spawnItems();
  if(running)requestAnimationFrame(loop);
}

function start(){
  score=0;timeLeft=45;starsCollected=0;running=true;
  stars=[];rocks=[];particles=[];
  whale.x=W*0.25;whale.y=H*0.5;whale.tx=whale.x;whale.ty=whale.y;
  document.getElementById('score').textContent='0';
  document.getElementById('timer').textContent='45초';
  document.getElementById('stars').textContent='0개';
  document.getElementById('startOverlay').classList.add('hidden');
  document.getElementById('endOverlay').classList.add('hidden');
  resize();
  loop();

  if(timerInterval)clearInterval(timerInterval);
  timerInterval=setInterval(()=>{
    timeLeft--;
    document.getElementById('timer').textContent=timeLeft+'초';
    if(timeLeft<=0)end();
  },1000);
}

function end(){
  running=false;
  clearInterval(timerInterval);
  let best=Math.max(+localStorage.getItem(KEY)||0,score);
  localStorage.setItem(KEY,best);
  document.getElementById('best').textContent=best;

  document.getElementById('endTitle').textContent='우주 유영 완주!';
  document.getElementById('endText').textContent='총 '+starsCollected+'개의 별가루를 모아 '+score+'점을 획득했어요!';
  document.getElementById('endOverlay').classList.remove('hidden');
}

document.getElementById('best').textContent=localStorage.getItem(KEY)||0;
document.getElementById('startBtn').addEventListener('pointerdown',start);
document.getElementById('restartBtn').addEventListener('pointerdown',start);
})();
</script>
</body>
</html>"""

with open(os.path.join(whale_dir, "thumb.svg"), "w", encoding="utf-8") as f:
    f.write(whale_svg)
with open(os.path.join(whale_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(whale_html)
print("Created star-whale-voyage")

# 2. Potion Magic Shop
potion_dir = os.path.join(ROOT, "potion-magic-shop")
os.makedirs(potion_dir, exist_ok=True)

potion_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" role="img" aria-label="숲속 마법 물약방">
<defs>
  <linearGradient id="magicBg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#14532d"/>
    <stop offset="50%" stop-color="#064e3b"/>
    <stop offset="100%" stop-color="#022c22"/>
  </linearGradient>
  <linearGradient id="liquidGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ec4899"/>
    <stop offset="100%" stop-color="#a855f7"/>
  </linearGradient>
  <filter id="glowP" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="320" height="180" rx="18" fill="url(#magicBg)"/>
<!-- Sparkles in forest -->
<g fill="#ffffff" opacity="0.6">
  <circle cx="35" cy="40" r="1.5"/>
  <circle cx="75" cy="25" r="1"/>
  <circle cx="285" cy="45" r="1.5"/>
  <circle cx="255" cy="25" r="1"/>
  <circle cx="65" cy="150" r="1.5"/>
</g>
<!-- Wooden Shelf -->
<rect x="40" y="130" width="240" height="14" rx="4" fill="#78350f" stroke="#92400e" stroke-width="1.5"/>
<!-- Flask / Potion Bottle in Center -->
<g transform="translate(160, 85)">
  <!-- Flask Neck -->
  <rect x="-8" y="-45" width="16" height="20" rx="3" fill="#e0f2fe" opacity="0.7" stroke="#ffffff" stroke-width="1.5"/>
  <!-- Cork -->
  <rect x="-6" y="-52" width="12" height="9" rx="2" fill="#b45309"/>
  <!-- Flask Body -->
  <path d="M-8 -25 L-28 15 C-34 26 -26 38 -14 38 L14 38 C26 38 34 26 28 15 L8 -25 Z" fill="#e0f2fe" opacity="0.4" stroke="#ffffff" stroke-width="2"/>
  <!-- Magic Liquid -->
  <path d="M-22 18 C-10 24 10 24 22 18 L14 36 L-14 36 Z" fill="url(#liquidGrad)" filter="url(#glowP)"/>
  <!-- Liquid Bubbles -->
  <circle cx="-5" cy="28" r="3" fill="#ffffff" opacity="0.7"/>
  <circle cx="6" cy="24" r="2" fill="#ffffff" opacity="0.7"/>
</g>
<!-- Side Mini Potions -->
<circle cx="95" cy="115" r="14" fill="#38bdf8" filter="url(#glowP)"/>
<rect x="91" y="93" width="8" height="10" fill="#bae6fd" opacity="0.7"/>
<circle cx="225" cy="115" r="14" fill="#4ade80" filter="url(#glowP)"/>
<rect x="221" y="93" width="8" height="10" fill="#bbf7d0" opacity="0.7"/>
<text x="296" y="148" text-anchor="end" font-family="Pretendard,Malgun Gothic,sans-serif" font-size="20" font-weight="900" fill="#4ade80">숲속 마법 물약방</text>
<text x="296" y="166" text-anchor="end" font-family="Pretendard,Arial,sans-serif" font-size="10" font-weight="700" fill="#bbf7d0" letter-spacing="2">POTION MAGIC SHOP</text>
<rect x="0.5" y="0.5" width="319" height="179" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.15"/>
</svg>"""

potion_html = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>숲속 마법 물약방</title>
<link rel="icon" href="data:,">
<style>
:root{--forest:#064e3b;--mint:#34d399;--pink:#f472b6;--gold:#fde047;--cyan:#38bdf8;--purple:#c084fc}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100vh;height:100dvh;margin:0;overflow:hidden;touch-action:manipulation;font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:#fff;background:#022c22}
body{background:radial-gradient(circle at 50% 15%,#064e3b 0,transparent 55%),linear-gradient(180deg,#022c22 0%,#011710 100%)}
.wrap{position:relative;width:100%;max-width:520px;height:100vh;height:100dvh;margin:auto;padding:12px;display:flex;flex-direction:column;gap:8px;overflow:hidden}
header{display:flex;align-items:center;justify-content:space-between}
h1{font-size:clamp(20px,5.5vw,26px);margin:0;color:#a7f3d0;text-shadow:0 2px 10px rgba(0,0,0,.5)}
.sub{font-size:11px;font-weight:700;color:#6ee7b7;margin-top:2px}
.hud{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.chip{padding:6px;text-align:center;border-radius:12px;background:rgba(255,255,255,.08);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.15);font-size:11px;color:#a7f3d0}
.chip b{display:block;font-size:17px;color:#fff;margin-top:2px}
.order-card{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-radius:16px;background:linear-gradient(135deg,rgba(52,211,153,.2),rgba(56,189,248,.15));border:1px solid rgba(52,211,153,.4)}
.order-info{display:flex;align-items:center;gap:10px}
.order-emoji{font-size:32px}
.order-steps{display:flex;gap:6px;margin-top:4px}
.step-dot{padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700;background:rgba(255,255,255,.15);color:#fff}
.step-dot.done{background:#22c55e;color:#fff}
.workshop{flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;border-radius:20px;border:1px solid rgba(52,211,153,.25);background:rgba(6,78,59,.4);box-shadow:inset 0 0 30px rgba(0,0,0,.6)}
.cauldron{width:160px;height:160px;border-radius:50%;border:4px dashed rgba(52,211,153,.4);display:grid;place-items:center;position:relative;background:radial-gradient(circle,rgba(52,211,153,.15),transparent 70%)}
.cauldron-preview{font-size:68px;filter:drop-shadow(0 6px 12px rgba(0,0,0,.4));transition:transform .2s ease}
.controls{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.c-btn{padding:10px 4px;border-radius:14px;border:1px solid rgba(255,255,255,.2);background:linear-gradient(145deg,rgba(255,255,255,.12),rgba(255,255,255,.04));color:#fff;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;font-size:11px;font-weight:700}
.c-btn span{font-size:24px}
.c-btn:active{transform:scale(.94);background:rgba(52,211,153,.3)}
.footer{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#a7f3d0}
.home-link{color:#fde047;font-weight:900;text-decoration:none;font-size:12px}
.overlay{position:fixed;z-index:10;inset:0;padding:20px;display:grid;place-items:center;background:rgba(2,44,34,.8);backdrop-filter:blur(8px)}
.overlay.hidden{display:none}
.card{width:min(380px,100%);padding:24px 20px;text-align:center;border-radius:24px;border:1px solid rgba(52,211,153,.3);background:linear-gradient(160deg,#064e3b,#022c22);box-shadow:0 16px 40px rgba(0,0,0,.5)}
.card h2{margin:0 0 10px;font-size:24px;color:#fde047}
.card p{margin:0 0 16px;font-size:13px;line-height:1.6;color:#a7f3d0}
.btn{padding:12px 24px;border:0;border-radius:14px;background:linear-gradient(135deg,#34d399,#059669);color:#fff;font-size:16px;font-weight:900;cursor:pointer;box-shadow:0 4px 12px rgba(5,150,105,.4)}
.btn:active{transform:scale(.96)}
</style>
</head>
<body>
<main class="wrap">
<header>
  <div><h1>🧪 숲속 마법 물약방</h1><div class="sub">요정 손님의 레시피에 맞춰 신비한 마법 물약을 제조해요!</div></div>
  <div class="chip" style="min-width:70px">최고 <b id="best">0</b></div>
</header>
<section class="hud">
  <div class="chip">연금 점수<b id="score">0</b></div>
  <div class="chip">남은 시간<b id="timer">50초</b></div>
  <div class="chip">완성 물약<b id="served">0개</b></div>
</section>
<div class="order-card">
  <div class="order-info">
    <div class="order-emoji" id="orderGuest">🧚</div>
    <div>
      <div style="font-size:13px;font-weight:800" id="orderName">별빛 비행 물약</div>
      <div class="order-steps" id="orderSteps"></div>
    </div>
  </div>
  <button class="btn" id="mixBtn" style="padding:8px 14px;font-size:13px">✨ 물약 조제!</button>
</div>
<div class="workshop">
  <div class="cauldron"><div class="cauldron-preview" id="previewEmoji">🥣</div></div>
</div>
<div class="controls">
  <button class="c-btn" data-item="dew"><span>💧</span>이슬</button>
  <button class="c-btn" data-item="leaf"><span>🌿</span>풀잎</button>
  <button class="c-btn" data-item="star"><span>⭐</span>별가루</button>
  <button class="c-btn" data-item="bloom"><span>🌸</span>꽃잎</button>
</div>
<footer class="footer"><span>✨ 재료를 순서대로 넣고 물약 조제 버튼을 눌러요!</span><a class="home-link" href="../index.html">← 홈</a></footer>
</main>
<div class="overlay" id="startOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px">🧪🌿🧚</div>
    <h2>숲속 마법 물약방</h2>
    <p>신비한 숲속 연금술사가 되어보세요!<br>손님의 주문 순서대로 마법 재료를 넣고<br>물약 조제 버튼을 눌러 완성하세요!</p>
    <button class="btn" id="startBtn">물약방 열기!</button>
  </div>
</div>
<div class="overlay hidden" id="endOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px" id="endEmoji">🧪</div>
    <h2 id="endTitle">영업 종료!</h2>
    <p id="endText"></p>
    <button class="btn" id="restartBtn">다시 조제하기</button>
  </div>
</div>
<script>
(()=>{'use strict';
const KEY='potion_magic_shop_best';
let score=0,timeLeft=50,served=0,running=false,currentOrder=null,userItems=[],timerInterval=null;

const RECIPES=[
  {name:'별빛 비행 물약',guest:'🧚',steps:['dew','star','bloom'],emoji:'🧪',pts:120},
  {name:'숲속 치유 물약',guest:'🧝',steps:['dew','leaf'],emoji:'🍵',pts:90},
  {name:'오로라 변신 물약',guest:'🧙',steps:['dew','bloom','star'],emoji:'🍷',pts:130},
  {name:'요정의 황금 물약',guest:'🦄',steps:['dew','leaf','star'],emoji:'🏺',pts:140}
];

const ITEM_NAMES={dew:'이슬 💧',leaf:'풀잎 🌿',star:'별가루 ⭐',bloom:'꽃잎 🌸'};

const AUD=window.AudioContext||window.webkitAudioContext;
let actx=null;
function beep(f,type='sine',dur=0.12){
  try{
    if(!actx)actx=new AUD();
    let osc=actx.createOscillator(),g=actx.createGain();
    osc.type=type;osc.frequency.value=f;
    g.gain.setValueAtTime(0.2,actx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001,actx.currentTime+dur);
    osc.connect(g);g.connect(actx.destination);
    osc.start();osc.stop(actx.currentTime+dur);
  }catch(e){}
}

function nextOrder(){
  currentOrder=RECIPES[Math.floor(Math.random()*RECIPES.length)];
  userItems=[];
  document.getElementById('orderGuest').textContent=currentOrder.guest;
  document.getElementById('orderName').textContent=currentOrder.name;
  renderSteps();
  document.getElementById('previewEmoji').textContent='🥣';
}

function renderSteps(){
  let html='';
  currentOrder.steps.forEach((s,idx)=>{
    let isDone=userItems[idx]===s;
    html+='<span class="step-dot '+(isDone?'done':'')+'">'+ITEM_NAMES[s]+'</span>';
  });
  document.getElementById('orderSteps').innerHTML=html;
}

document.querySelectorAll('.c-btn').forEach(b=>{
  b.addEventListener('pointerdown',e=>{
    e.preventDefault();
    if(!running)return;
    let item=b.dataset.item;
    userItems.push(item);
    beep(450+userItems.length*70);
    renderSteps();

    if(userItems.length===1)document.getElementById('previewEmoji').textContent='💧';
    else if(userItems.length===2)document.getElementById('previewEmoji').textContent='🫧';
    else document.getElementById('previewEmoji').textContent='✨';
  });
});

document.getElementById('mixBtn').addEventListener('pointerdown',e=>{
  e.preventDefault();
  if(!running)return;
  let match=userItems.length===currentOrder.steps.length&&userItems.every((v,i)=>v===currentOrder.steps[i]);
  if(match){
    beep(880,'triangle',0.25);
    score+=currentOrder.pts;
    served++;
    document.getElementById('score').textContent=score;
    document.getElementById('served').textContent=served+'개';
    document.getElementById('previewEmoji').textContent=currentOrder.emoji;
    document.getElementById('previewEmoji').style.transform='scale(1.25)';
    setTimeout(()=>{
      document.getElementById('previewEmoji').style.transform='scale(1)';
      nextOrder();
    },350);
  }else{
    beep(200,'sawtooth',0.3);
    document.getElementById('previewEmoji').textContent='💥';
    userItems=[];
    setTimeout(()=>{
      renderSteps();
      document.getElementById('previewEmoji').textContent='🥣';
    },400);
  }
});

function start(){
  score=0;timeLeft=50;served=0;running=true;
  document.getElementById('score').textContent='0';
  document.getElementById('timer').textContent='50초';
  document.getElementById('served').textContent='0개';
  document.getElementById('startOverlay').classList.add('hidden');
  document.getElementById('endOverlay').classList.add('hidden');
  nextOrder();

  if(timerInterval)clearInterval(timerInterval);
  timerInterval=setInterval(()=>{
    timeLeft--;
    document.getElementById('timer').textContent=timeLeft+'초';
    if(timeLeft<=0)end();
  },1000);
}

function end(){
  running=false;
  clearInterval(timerInterval);
  let best=Math.max(+localStorage.getItem(KEY)||0,score);
  localStorage.setItem(KEY,best);
  document.getElementById('best').textContent=best;

  document.getElementById('endTitle').textContent='물약 조제 완료!';
  document.getElementById('endText').textContent='총 '+served+'개의 마법 물약을 완성하여 '+score+'점을 획득했어요!';
  document.getElementById('endOverlay').classList.remove('hidden');
}

document.getElementById('best').textContent=localStorage.getItem(KEY)||0;
document.getElementById('startBtn').addEventListener('pointerdown',start);
document.getElementById('restartBtn').addEventListener('pointerdown',start);
})();
</script>
</body>
</html>"""

with open(os.path.join(potion_dir, "thumb.svg"), "w", encoding="utf-8") as f:
    f.write(potion_svg)
with open(os.path.join(potion_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(potion_html)
print("Created potion-magic-shop")
