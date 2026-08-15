import os
import json
from pathlib import Path

ROOT = r"D:\workspace\projects\active\jangyoon-s-game"

# 1. Turtle Bubble Rescue
turtle_dir = os.path.join(ROOT, "turtle-bubble-rescue")
os.makedirs(turtle_dir, exist_ok=True)

turtle_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" role="img" aria-label="바다거북 비눗방울 구출">
<defs>
  <linearGradient id="seaBg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#00527b"/>
    <stop offset="50%" stop-color="#007799"/>
    <stop offset="100%" stop-color="#002b47"/>
  </linearGradient>
  <linearGradient id="bubbleGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.7"/>
    <stop offset="40%" stop-color="#67e8f9" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.2"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="320" height="180" rx="18" fill="url(#seaBg)"/>
<circle cx="50" cy="140" r="35" fill="#0284c7" opacity="0.25"/>
<circle cx="270" cy="50" r="45" fill="#38bdf8" opacity="0.2"/>
<path d="M10 180 Q30 130 50 180 Q70 140 90 180" fill="#f43f5e" opacity="0.6"/>
<path d="M230 180 Q255 125 280 180 Q300 135 320 180" fill="#10b981" opacity="0.5"/>
<g transform="translate(160, 80)">
  <circle cx="0" cy="0" r="42" fill="url(#bubbleGrad)" stroke="#e0f2fe" stroke-width="2" filter="url(#glow)"/>
  <ellipse cx="-14" cy="-14" rx="10" ry="5" fill="#ffffff" opacity="0.6" transform="rotate(-30, -14, -14)"/>
  <ellipse cx="0" cy="2" rx="16" ry="13" fill="#22c55e"/>
  <ellipse cx="0" cy="2" rx="13" ry="10" fill="#15803d" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="-18" cy="-1" r="6" fill="#4ade80"/>
  <circle cx="-19" cy="-2" r="1.5" fill="#0f172a"/>
  <path d="M-8 -6 Q-18 -18 -4 -12" fill="#22c55e"/>
  <path d="M8 -6 Q18 -18 4 -12" fill="#22c55e"/>
  <path d="M-6 10 Q-12 18 -2 14" fill="#22c55e"/>
  <path d="M6 10 Q12 18 2 14" fill="#22c55e"/>
</g>
<circle cx="80" cy="60" r="12" fill="url(#bubbleGrad)" stroke="#e0f2fe" stroke-width="1.5"/>
<circle cx="240" cy="110" r="16" fill="url(#bubbleGrad)" stroke="#e0f2fe" stroke-width="1.5"/>
<circle cx="105" cy="115" r="8" fill="url(#bubbleGrad)" stroke="#e0f2fe" stroke-width="1"/>
<text x="296" y="148" text-anchor="end" font-family="Pretendard,Malgun Gothic,sans-serif" font-size="20" font-weight="900" fill="#67e8f9">바다거북 비눗방울 구출</text>
<text x="296" y="166" text-anchor="end" font-family="Pretendard,Arial,sans-serif" font-size="10" font-weight="700" fill="#bae6fd" letter-spacing="2">TURTLE BUBBLE RESCUE</text>
<rect x="0.5" y="0.5" width="319" height="179" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.15"/>
</svg>"""

turtle_html = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>바다거북 비눗방울 구출</title>
<link rel="icon" href="data:,">
<style>
:root{--teal:#0284c7;--cyan:#38bdf8;--green:#22c55e;--coral:#f43f5e;--sand:#fde047}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100vh;height:100dvh;margin:0;overflow:hidden;touch-action:manipulation;font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:#fff;background:#032b43}
body{background:radial-gradient(circle at 50% 10%,#006494 0,transparent 50%),linear-gradient(180deg,#003554 0%,#051923 100%)}
.wrap{position:relative;width:100%;max-width:520px;height:100vh;height:100dvh;margin:auto;padding:12px;display:flex;flex-direction:column;gap:8px;overflow:hidden}
header{display:flex;align-items:center;justify-content:space-between}
h1{font-size:clamp(20px,5.5vw,26px);margin:0;color:#e0f2fe;text-shadow:0 2px 8px rgba(0,0,0,.4)}
.sub{font-size:11px;font-weight:700;color:#7dd3fc;margin-top:2px}
.hud{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.chip{padding:6px;text-align:center;border-radius:12px;background:rgba(255,255,255,.1);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.15);font-size:11px;color:#bae6fd}
.chip b{display:block;font-size:17px;color:#fff;margin-top:2px}
#canvas-box{position:relative;flex:1;min-height:0;border-radius:20px;overflow:hidden;border:1px solid rgba(56,189,248,.3);background:radial-gradient(circle at 50% 30%,rgba(56,189,248,.15),transparent 60%),rgba(0,30,50,.6);box-shadow:inset 0 0 20px rgba(0,0,0,.5)}
canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none}
.footer{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#7dd3fc}
.home-link{color:#fde047;font-weight:900;text-decoration:none;font-size:12px}
.overlay{position:fixed;z-index:10;inset:0;padding:20px;display:grid;place-items:center;background:rgba(3,43,67,.75);backdrop-filter:blur(8px)}
.overlay.hidden{display:none}
.card{width:min(380px,100%);padding:24px 20px;text-align:center;border-radius:24px;border:1px solid rgba(255,255,255,.2);background:linear-gradient(160deg,#006494,#003554);box-shadow:0 16px 40px rgba(0,0,0,.5)}
.card h2{margin:0 0 10px;font-size:24px;color:#fde047}
.card p{margin:0 0 16px;font-size:13px;line-height:1.6;color:#e0f2fe}
.btn{padding:12px 24px;border:0;border-radius:14px;background:linear-gradient(135deg,#38bdf8,#0284c7);color:#fff;font-size:16px;font-weight:900;cursor:pointer;box-shadow:0 4px 12px rgba(2,132,199,.4)}
.btn:active{transform:scale(.96)}
</style>
</head>
<body>
<main class="wrap">
<header>
  <div><h1>🐢 바다거북 비눗방울 구출</h1><div class="sub">비눗방울에 갇힌 바다 친구들을 터치해 구해주세요!</div></div>
  <div class="chip" style="min-width:70px">최고 <b id="best">0</b></div>
</header>
<section class="hud">
  <div class="chip">구출 점수<b id="score">0</b></div>
  <div class="chip">남은 시간<b id="timer">45초</b></div>
  <div class="chip">콤보<b id="combo">0x</b></div>
</section>
<div id="canvas-box"><canvas id="cvs"></canvas></div>
<footer class="footer"><span>🫧 거품을 톡! 가시복어 거품은 피해요!</span><a class="home-link" href="../index.html">← 홈</a></footer>
</main>
<div class="overlay" id="startOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px">🐢🫧🐠</div>
    <h2>바다거북 비눗방울 구출</h2>
    <p>바다속 비눗방울에 갇힌 아기 거북이와<br>물고기 친구들을 톡톡 터치해 구출해주세요!<br><br>⚠️ 검은 가시복어 거품은 터뜨리면 안돼요!</p>
    <button class="btn" id="startBtn">구출 작전 시작!</button>
  </div>
</div>
<div class="overlay hidden" id="endOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px" id="endEmoji">🎉</div>
    <h2 id="endTitle">구출 작전 완료!</h2>
    <p id="endText"></p>
    <button class="btn" id="restartBtn">다시 하기</button>
  </div>
</div>
<script>
(()=>{'use strict';
const KEY='turtle_bubble_rescue_best';
let canvas=document.getElementById('cvs'),ctx=canvas.getContext('2d');
let score=0,timeLeft=45,combo=0,running=false,bubbles=[],particles=[],timerInterval=null;
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

const CREATURES=[
  {type:'turtle',emoji:'🐢',pts:100,spd:1.2,r:32,prob:0.45},
  {type:'fish',emoji:'🐠',pts:80,spd:1.5,r:28,prob:0.3},
  {type:'star',emoji:'⭐',pts:150,spd:1.8,r:26,prob:0.15},
  {type:'puffer',emoji:'🐡',pts:-150,spd:1.0,r:30,prob:0.1,bad:true}
];

function spawnBubble(){
  if(!running)return;
  let rand=Math.random(),acc=0,chosen=CREATURES[0];
  for(let c of CREATURES){
    acc+=c.prob;
    if(rand<=acc){chosen=c;break;}
  }
  bubbles.push({
    x:Math.random()*(W-80)+40,
    y:H+40,
    r:chosen.r,
    type:chosen.type,
    emoji:chosen.emoji,
    pts:chosen.pts,
    bad:chosen.bad||false,
    vy:(chosen.spd+Math.random()*0.5)*(H/450),
    wobble:Math.random()*Math.PI*2,
    scale:1
  });
}

function tapAt(tx,ty){
  if(!running)return;
  for(let i=bubbles.length-1;i>=0;i--){
    let b=bubbles[i];
    let dist=Math.hypot(tx-b.x,ty-b.y);
    if(dist<=b.r*1.2){
      bubbles.splice(i,1);
      if(b.bad){
        combo=0;
        score=Math.max(0,score+b.pts);
        beep(180,'sawtooth',0.3);
        spawnParticles(b.x,b.y,'#1e293b',12);
      }else{
        combo++;
        let bonus=Math.floor(b.pts*(1+(combo-1)*0.2));
        score+=bonus;
        beep(400+combo*40,'sine',0.15);
        spawnParticles(b.x,b.y,'#38bdf8',15);
        spawnFloater(b.x,b.y,'+'+bonus+(combo>1?' ('+combo+'x)':''));
      }
      document.getElementById('score').textContent=score;
      document.getElementById('combo').textContent=combo+'x';
      return;
    }
  }
}

let floaters=[];
function spawnFloater(x,y,text){
  floaters.push({x,y,text,alpha:1,vy:-1.5});
}

function spawnParticles(x,y,color,cnt){
  for(let i=0;i<cnt;i++){
    let ang=Math.random()*Math.PI*2,spd=2+Math.random()*4;
    particles.push({
      x,y,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd,
      r:3+Math.random()*3,color,alpha:1
    });
  }
}

canvas.addEventListener('pointerdown',e=>{
  e.preventDefault();
  let rect=canvas.getBoundingClientRect();
  tapAt(e.clientX-rect.left,e.clientY-rect.top);
});

function loop(){
  ctx.clearRect(0,0,W,H);

  ctx.fillStyle='rgba(56,189,248,0.03)';
  ctx.beginPath();
  ctx.moveTo(W*0.2,0);ctx.lineTo(W*0.5,H);ctx.lineTo(W*0.35,H);ctx.lineTo(W*0.1,0);ctx.fill();
  ctx.beginPath();
  ctx.moveTo(W*0.7,0);ctx.lineTo(W*0.9,H);ctx.lineTo(W*0.75,H);ctx.lineTo(W*0.55,0);ctx.fill();

  for(let i=bubbles.length-1;i>=0;i--){
    let b=bubbles[i];
    b.y-=b.vy;
    b.wobble+=0.04;
    let wx=b.x+Math.sin(b.wobble)*10;

    ctx.save();
    ctx.translate(wx,b.y);
    ctx.beginPath();
    ctx.arc(0,0,b.r,0,Math.PI*2);
    if(b.bad){
      ctx.fillStyle='rgba(15,23,42,0.6)';
      ctx.strokeStyle='rgba(244,63,94,0.8)';
    }else{
      ctx.fillStyle='rgba(56,189,248,0.25)';
      ctx.strokeStyle='rgba(224,242,254,0.7)';
    }
    ctx.lineWidth=2;
    ctx.fill();
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(-b.r*0.3,-b.r*0.3,b.r*0.25,0,Math.PI*2);
    ctx.fillStyle='rgba(255,255,255,0.6)';
    ctx.fill();

    ctx.font=Math.floor(b.r*1.1)+'px sans-serif';
    ctx.textAlign='center';
    ctx.textBaseline='middle';
    ctx.fillText(b.emoji,0,2);
    ctx.restore();

    if(b.y<-50)bubbles.splice(i,1);
  }

  for(let i=particles.length-1;i>=0;i--){
    let p=particles[i];
    p.x+=p.vx;p.y+=p.vy;p.alpha-=0.03;
    if(p.alpha<=0){particles.splice(i,1);continue;}
    ctx.beginPath();
    ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=p.color;
    ctx.globalAlpha=p.alpha;
    ctx.fill();
    ctx.globalAlpha=1;
  }

  for(let i=floaters.length-1;i>=0;i--){
    let f=floaters[i];
    f.y+=f.vy;f.alpha-=0.025;
    if(f.alpha<=0){floaters.splice(i,1);continue;}
    ctx.font='bold 16px sans-serif';
    ctx.textAlign='center';
    ctx.fillStyle='#fde047';
    ctx.globalAlpha=f.alpha;
    ctx.fillText(f.text,f.x,f.y);
    ctx.globalAlpha=1;
  }

  if(running)requestAnimationFrame(loop);
}

let spawnTimer=null;
function startGame(){
  score=0;timeLeft=45;combo=0;bubbles=[];particles=[];floaters=[];running=true;
  document.getElementById('score').textContent='0';
  document.getElementById('timer').textContent='45초';
  document.getElementById('combo').textContent='0x';
  document.getElementById('startOverlay').classList.add('hidden');
  document.getElementById('endOverlay').classList.add('hidden');
  resize();
  loop();

  if(spawnTimer)clearInterval(spawnTimer);
  spawnTimer=setInterval(spawnBubble,700);

  if(timerInterval)clearInterval(timerInterval);
  timerInterval=setInterval(()=>{
    timeLeft--;
    document.getElementById('timer').textContent=timeLeft+'초';
    if(timeLeft<=0)endGame();
  },1000);
}

function endGame(){
  running=false;
  clearInterval(timerInterval);
  clearInterval(spawnTimer);
  let best=Math.max(+localStorage.getItem(KEY)||0,score);
  localStorage.setItem(KEY,best);
  document.getElementById('best').textContent=best;

  document.getElementById('endTitle').textContent='구출 성공!';
  document.getElementById('endText').textContent='총 '+score+'점을 획득하여 바다 친구들을 안전하게 구출했어요!';
  document.getElementById('endOverlay').classList.remove('hidden');
}

document.getElementById('best').textContent=localStorage.getItem(KEY)||0;
document.getElementById('startBtn').addEventListener('pointerdown',startGame);
document.getElementById('restartBtn').addEventListener('pointerdown',startGame);
})();
</script>
</body>
</html>"""

with open(os.path.join(turtle_dir, "thumb.svg"), "w", encoding="utf-8") as f:
    f.write(turtle_svg)
with open(os.path.join(turtle_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(turtle_html)
print("Created turtle-bubble-rescue")

# 2. Cosmic Star Baker
baker_dir = os.path.join(ROOT, "cosmic-star-baker")
os.makedirs(baker_dir, exist_ok=True)

baker_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" role="img" aria-label="우주 별빛 베이커리">
<defs>
  <linearGradient id="spaceBg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#1e1b4b"/>
    <stop offset="50%" stop-color="#311042"/>
    <stop offset="100%" stop-color="#0f172a"/>
  </linearGradient>
  <linearGradient id="donutGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f472b6"/>
    <stop offset="100%" stop-color="#c084fc"/>
  </linearGradient>
  <filter id="glowStar" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="320" height="180" rx="18" fill="url(#spaceBg)"/>
<g fill="#ffffff" opacity="0.6">
  <circle cx="30" cy="40" r="1.5"/>
  <circle cx="80" cy="25" r="1"/>
  <circle cx="280" cy="45" r="1.5"/>
  <circle cx="250" cy="20" r="1"/>
  <circle cx="60" cy="150" r="1.5"/>
</g>
<circle cx="160" cy="82" r="52" fill="none" stroke="#818cf8" stroke-width="2" stroke-dasharray="6 6" filter="url(#glowStar)"/>
<g transform="translate(160, 82)">
  <ellipse cx="0" cy="0" rx="36" ry="30" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
  <path d="M-30 -5 C-20 -20 20 -20 30 -5 C25 15 15 25 0 24 C-15 25 -25 15 -30 -5 Z" fill="url(#donutGrad)"/>
  <ellipse cx="0" cy="2" rx="12" ry="9" fill="#1e1b4b"/>
  <circle cx="-16" cy="-8" r="2.5" fill="#fef08a"/>
  <circle cx="15" cy="-6" r="2.5" fill="#67e8f9"/>
  <circle cx="-8" cy="14" r="2" fill="#a7f3d0"/>
  <circle cx="12" cy="12" r="2" fill="#fbcfe8"/>
</g>
<circle cx="65" cy="95" r="18" fill="#ec4899" opacity="0.8"/>
<ellipse cx="65" cy="95" rx="24" ry="5" fill="none" stroke="#fde047" stroke-width="2" transform="rotate(-15, 65, 95)"/>
<text x="296" y="148" text-anchor="end" font-family="Pretendard,Malgun Gothic,sans-serif" font-size="20" font-weight="900" fill="#f472b6">우주 별빛 베이커리</text>
<text x="296" y="166" text-anchor="end" font-family="Pretendard,Arial,sans-serif" font-size="10" font-weight="700" fill="#e9d5ff" letter-spacing="2">COSMIC STAR BAKER</text>
<rect x="0.5" y="0.5" width="319" height="179" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.15"/>
</svg>"""

baker_html = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>우주 별빛 베이커리</title>
<link rel="icon" href="data:,">
<style>
:root{--space:#1e1b4b;--pink:#f472b6;--purple:#c084fc;--gold:#fde047;--cyan:#38bdf8}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100vh;height:100dvh;margin:0;overflow:hidden;touch-action:manipulation;font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:#fff;background:#0f172a}
body{background:radial-gradient(circle at 50% 15%,#311042 0,transparent 55%),linear-gradient(180deg,#1e1b4b 0%,#090d16 100%)}
.wrap{position:relative;width:100%;max-width:520px;height:100vh;height:100dvh;margin:auto;padding:12px;display:flex;flex-direction:column;gap:8px;overflow:hidden}
header{display:flex;align-items:center;justify-content:space-between}
h1{font-size:clamp(20px,5.5vw,26px);margin:0;color:#fbcfe8;text-shadow:0 2px 10px rgba(0,0,0,.5)}
.sub{font-size:11px;font-weight:700;color:#e9d5ff;margin-top:2px}
.hud{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.chip{padding:6px;text-align:center;border-radius:12px;background:rgba(255,255,255,.08);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.15);font-size:11px;color:#e9d5ff}
.chip b{display:block;font-size:17px;color:#fff;margin-top:2px}
.order-card{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-radius:16px;background:linear-gradient(135deg,rgba(244,114,182,.2),rgba(192,132,252,.15));border:1px solid rgba(244,114,182,.4)}
.order-info{display:flex;align-items:center;gap:10px}
.order-emoji{font-size:32px}
.order-steps{display:flex;gap:6px;margin-top:4px}
.step-dot{padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700;background:rgba(255,255,255,.15);color:#fff}
.step-dot.done{background:#22c55e;color:#fff}
.kitchen{flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;border-radius:20px;border:1px solid rgba(244,114,182,.25);background:rgba(30,27,75,.4);box-shadow:inset 0 0 30px rgba(0,0,0,.6)}
.plate{width:160px;height:160px;border-radius:50%;border:4px dashed rgba(244,114,182,.4);display:grid;place-items:center;position:relative;background:radial-gradient(circle,rgba(244,114,182,.1),transparent 70%)}
.plate-preview{font-size:68px;filter:drop-shadow(0 6px 12px rgba(0,0,0,.4));transition:transform .2s ease}
.controls{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.c-btn{padding:10px 4px;border-radius:14px;border:1px solid rgba(255,255,255,.2);background:linear-gradient(145deg,rgba(255,255,255,.12),rgba(255,255,255,.04));color:#fff;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;font-size:11px;font-weight:700}
.c-btn span{font-size:24px}
.c-btn:active{transform:scale(.94);background:rgba(244,114,182,.3)}
.footer{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#e9d5ff}
.home-link{color:#fde047;font-weight:900;text-decoration:none;font-size:12px}
.overlay{position:fixed;z-index:10;inset:0;padding:20px;display:grid;place-items:center;background:rgba(15,23,42,.8);backdrop-filter:blur(8px)}
.overlay.hidden{display:none}
.card{width:min(380px,100%);padding:24px 20px;text-align:center;border-radius:24px;border:1px solid rgba(244,114,182,.3);background:linear-gradient(160deg,#311042,#1e1b4b);box-shadow:0 16px 40px rgba(0,0,0,.5)}
.card h2{margin:0 0 10px;font-size:24px;color:#fde047}
.card p{margin:0 0 16px;font-size:13px;line-height:1.6;color:#fbcfe8}
.btn{padding:12px 24px;border:0;border-radius:14px;background:linear-gradient(135deg,#f472b6,#c084fc);color:#fff;font-size:16px;font-weight:900;cursor:pointer;box-shadow:0 4px 12px rgba(244,114,182,.4)}
.btn:active{transform:scale(.96)}
</style>
</head>
<body>
<main class="wrap">
<header>
  <div><h1>🥐 우주 별빛 베이커리</h1><div class="sub">외계인 손님의 주문에 맞춰 디저트를 구워요!</div></div>
  <div class="chip" style="min-width:70px">최고 <b id="best">0</b></div>
</header>
<section class="hud">
  <div class="chip">베이킹 점수<b id="score">0</b></div>
  <div class="chip">남은 시간<b id="timer">50초</b></div>
  <div class="chip">완성 디저트<b id="served">0개</b></div>
</section>
<div class="order-card">
  <div class="order-info">
    <div class="order-emoji" id="orderGuest">👽</div>
    <div>
      <div style="font-size:13px;font-weight:800" id="orderName">토성 고리 도넛</div>
      <div class="order-steps" id="orderSteps"></div>
    </div>
  </div>
  <button class="btn" id="bakeBtn" style="padding:8px 14px;font-size:13px">✨ 오븐 굽기!</button>
</div>
<div class="kitchen">
  <div class="plate"><div class="plate-preview" id="previewEmoji">🍽️</div></div>
</div>
<div class="controls">
  <button class="c-btn" data-item="dough"><span>🌕</span>반죽</button>
  <button class="c-btn" data-item="syrup"><span>🫐</span>시럽</button>
  <button class="c-btn" data-item="stars"><span>⭐</span>별가루</button>
  <button class="c-btn" data-item="ring"><span>🪐</span>고리</button>
</div>
<footer class="footer"><span>✨ 순서대로 올리고 오븐 굽기 버튼을 눌러요!</span><a class="home-link" href="../index.html">← 홈</a></footer>
</main>
<div class="overlay" id="startOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px">🥐🪐✨</div>
    <h2>우주 별빛 베이커리</h2>
    <p>은하계 최고의 파티시에가 되어보세요!<br>손님의 주문 순서대로 재료를 넣고<br>오븐 굽기 버튼을 눌러 서빙하세요!</p>
    <button class="btn" id="startBtn">베이커리 오픈!</button>
  </div>
</div>
<div class="overlay hidden" id="endOverlay">
  <div class="card">
    <div style="font-size:50px;margin-bottom:6px" id="endEmoji">🧁</div>
    <h2 id="endTitle">영업 종료!</h2>
    <p id="endText"></p>
    <button class="btn" id="restartBtn">다시 굽기</button>
  </div>
</div>
<script>
(()=>{'use strict';
const KEY='cosmic_star_baker_best';
let score=0,timeLeft=50,served=0,running=false,currentOrder=null,userItems=[],timerInterval=null;

const RECIPES=[
  {name:'토성 고리 도넛',guest:'👽',steps:['dough','syrup','ring'],emoji:'🍩',pts:120},
  {name:'별빛 은하수 쿠키',guest:'🤖',steps:['dough','stars'],emoji:'🍪',pts:90},
  {name:'혜성 슈크림 빵',guest:'👾',steps:['dough','syrup','stars'],emoji:'🥐',pts:130},
  {name:'우주 펄 컵케이크',guest:'🧑‍🚀',steps:['dough','ring','stars'],emoji:'🧁',pts:140}
];

const ITEM_NAMES={dough:'반죽 🌕',syrup:'시럽 🫐',stars:'별가루 ⭐',ring:'고리 🪐'};

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
  document.getElementById('previewEmoji').textContent='🍽️';
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
    beep(500+userItems.length*60);
    renderSteps();

    if(userItems.length===1)document.getElementById('previewEmoji').textContent='🌕';
    else if(userItems.length===2)document.getElementById('previewEmoji').textContent='🥞';
    else document.getElementById('previewEmoji').textContent='✨';
  });
});

document.getElementById('bakeBtn').addEventListener('pointerdown',e=>{
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
      document.getElementById('previewEmoji').textContent='🍽️';
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

  document.getElementById('endTitle').textContent='디저트 서빙 완료!';
  document.getElementById('endText').textContent='총 '+served+'개의 우주 디저트를 만들어 '+score+'점을 획득했어요!';
  document.getElementById('endOverlay').classList.remove('hidden');
}

document.getElementById('best').textContent=localStorage.getItem(KEY)||0;
document.getElementById('startBtn').addEventListener('pointerdown',start);
document.getElementById('restartBtn').addEventListener('pointerdown',start);
})();
</script>
</body>
</html>"""

with open(os.path.join(baker_dir, "thumb.svg"), "w", encoding="utf-8") as f:
    f.write(baker_svg)
with open(os.path.join(baker_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(baker_html)
print("Created cosmic-star-baker")
