from flask import Flask
import os

app = Flask(__name__)

# ============ ORTAK CSS ============
base_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
:root { --neon-orange: #ff4500; --neon-blue: #00d4ff; --neon-purple: #bf00ff; --dark-bg: #050505; }
* { margin: 0; padding: 0; box-sizing: border-box; touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
body { background: var(--dark-bg); color: #fff; font-family: 'Rajdhani', sans-serif; overflow-x: hidden; min-height: 100vh; }
#particles { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
.xp-container { position: fixed; top: 20px; right: 20px; background: rgba(255,69,0,0.15); border: 1px solid var(--neon-orange); padding: 12px 24px; border-radius: 50px; z-index: 1000; backdrop-filter: blur(10px); box-shadow: 0 0 20px rgba(255,69,0,0.3); font-family: 'Orbitron', sans-serif; }
.xp-val { color: var(--neon-orange); font-weight: 900; font-size: 1.2rem; }
.btn { background: linear-gradient(135deg, var(--neon-orange), #ff6b35); color: #fff; border: none; padding: 12px 24px; font-family: 'Orbitron', sans-serif; font-weight: 700; cursor: pointer; border-radius: 8px; transition: all 0.3s; text-transform: uppercase; letter-spacing: 1px; }
.btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(255,69,0,0.4); }
.btn:disabled { background: #333; cursor: not-allowed; transform: none; box-shadow: none; opacity: 0.6; }
.back-btn { position: fixed; bottom: 30px; left: 30px; color: #444; text-decoration: none; font-family: 'Orbitron', sans-serif; transition: all 0.3s; z-index: 100; font-size: 0.9rem; }
.back-btn:hover { color: var(--neon-orange); text-shadow: 0 0 10px rgba(255,69,0,0.5); }
"""

# ============ ANA SAYFA (GELİŞMİŞ) ============
ana_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CANO STUDIO | NEON PORTAL</title>
    <style>""" + base_css + """
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 80px 20px; position: relative; }
        h1 { font-family: 'Orbitron', sans-serif; font-size: clamp(2rem, 8vw, 5rem); letter-spacing: 15px; margin-bottom: 20px; color: #fff; text-shadow: 0 0 30px rgba(255,69,0,0.5); animation: glow 2s ease-in-out infinite alternate; }
        @keyframes glow { from { text-shadow: 0 0 30px rgba(255,69,0,0.5); } to { text-shadow: 0 0 50px rgba(255,69,0,0.8), 0 0 60px rgba(255,69,0,0.6); } }
        .subtitle { color: #666; font-size: 1.1rem; letter-spacing: 5px; margin-bottom: 60px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; width: 100%; max-width: 1200px; padding: 0 20px; }
        .card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 40px 30px; border-radius: 12px; cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); text-decoration: none; position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); transition: left 0.5s; }
        .card:hover::before { left: 100%; }
        .card:hover { border-color: var(--neon-orange); transform: translateY(-10px) scale(1.02); box-shadow: 0 20px 40px rgba(255,69,0,0.3); background: rgba(255,69,0,0.08); }
        .card h2 { font-family: 'Orbitron', sans-serif; font-size: 1rem; letter-spacing: 4px; margin-bottom: 10px; color: #fff; }
        .card p { color: #888; font-size: 0.9rem; }
        .store-card { border-color: var(--neon-blue) !important; }
        .store-card:hover { border-color: var(--neon-blue) !important; box-shadow: 0 20px 40px rgba(0,212,255,0.3); background: rgba(0,212,255,0.08); }
        .badge { position: absolute; top: 10px; right: 10px; background: var(--neon-orange); color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-family: 'Orbitron', sans-serif; }
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    <div class="xp-container"><span class="xp-val" id="totalXP">0</span> <small style="color:#ff4500">XP</small></div>
    <section class="hero">
        <h1>CANO STUDIO</h1>
        <p class="subtitle">NEON GAMING UNIVERSE</p>
        <div class="grid">
            <a href="/neon-arcade" class="card"><h2>🎮 NEON ARCADE</h2><p>Gece manzaralı hız oyunu</p></a>
            <a href="/strateji" class="card"><h2>🌍 GALAKTIK STRATEJI</h2><p>Gezegen fethetme simülasyonu</p></a>
            <a href="/horror" class="card"><h2>👻 DARK HORROR</h2><p>30 farklı son, karanlık yolculuk</p></a>
            <a href="/store" class="card store-card"><span class="badge">NEW</span><h2>🛒 NEON MARKET</h2><p style="color:#00d4ff">Skinler ve güçlendirmeler</p></a>
        </div>
    </section>
    <script>
        document.getElementById('totalXP').innerText = localStorage.getItem('cano_xp') || 0;
        const canvas = document.getElementById('particles'), ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const particles = Array.from({length: 60}, () => ({x: Math.random()*canvas.width, y: Math.random()*canvas.height, size: Math.random()*2, speedX: (Math.random()-0.5)*0.5, speedY: (Math.random()-0.5)*0.5, opacity: Math.random()}));
        function animate() { ctx.clearRect(0,0,canvas.width,canvas.height); particles.forEach(p => { p.x+=p.speedX; p.y+=p.speedY; if(p.x<0)p.x=canvas.width; if(p.x>canvas.width)p.x=0; if(p.y<0)p.y=canvas.height; if(p.y>canvas.height)p.y=0; ctx.fillStyle=`rgba(255,69,0,${p.opacity})`; ctx.beginPath(); ctx.arc(p.x,p.y,p.size,0,Math.PI*2); ctx.fill(); }); requestAnimationFrame(animate); }
        animate(); window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
    </script>
</body>
</html>
"""

# ============ MAĞAZA (GELİŞMİŞ) ============
store_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEON MARKET | Cano Studio</title>
    <style>""" + base_css + """
        .store-container { min-height: 100vh; padding: 100px 20px 40px; max-width: 1200px; margin: 0 auto; }
        .store-header { text-align: center; margin-bottom: 50px; }
        .store-header h1 { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; letter-spacing: 10px; margin-bottom: 20px; }
        .balance-display { background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(191,0,255,0.1)); border: 2px solid var(--neon-blue); padding: 20px 40px; border-radius: 50px; display: inline-block; font-size: 1.5rem; font-family: 'Orbitron', sans-serif; }
        .balance-display span { color: var(--neon-blue); font-weight: 900; }
        .store-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; }
        .item { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 30px; transition: all 0.3s; position: relative; overflow: hidden; text-align: center; }
        .item:hover { transform: translateY(-5px); border-color: var(--neon-orange); box-shadow: 0 15px 35px rgba(255,69,0,0.2); }
        .item.owned { border-color: #00ff00; background: rgba(0,255,0,0.05); }
        .item-icon { font-size: 3rem; margin-bottom: 15px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3)); }
        .item h3 { font-family: 'Orbitron', sans-serif; font-size: 1.1rem; margin-bottom: 10px; }
        .item p { color: #666; font-size: 0.85rem; margin-bottom: 15px; min-height: 40px; }
        .price { color: var(--neon-orange); font-size: 1.4rem; font-weight: 900; font-family: 'Orbitron', sans-serif; margin-bottom: 15px; }
        .item.owned .price { color: #00ff00; }
        .notification { position: fixed; top: 100px; right: -400px; background: linear-gradient(135deg, var(--neon-orange), #ff6b35); padding: 20px 30px; border-radius: 12px; font-family: 'Orbitron', sans-serif; transition: right 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55); z-index: 2000; box-shadow: 0 10px 30px rgba(255,69,0,0.4); }
        .notification.show { right: 20px; }
        .notification.error { background: linear-gradient(135deg, #ff0040, #ff0040); }
    </style>
</head>
<body>
    <div class="xp-container"><span class="xp-val" id="currentXP">0</span> <small style="color:#ff4500">XP</small></div>
    <div class="notification" id="notif">SATIN ALINDI!</div>
    <div class="store-container">
        <div class="store-header">
            <h1>NEON MARKET</h1>
            <div class="balance-display">BAKİYE: <span id="balance">0</span> XP</div>
        </div>
        <div class="store-grid" id="grid"></div>
    </div>
    <a href="/" class="back-btn">← GERİ DÖN</a>
    <script>
        let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
        let owned = JSON.parse(localStorage.getItem('cano_items')) || [];
        const items = [
            {id: 'item1', name: 'ALTIN KUŞ', icon: '🐦', price: 500, desc: 'Neon Arcade için altın renkli kuş skin.'},
            {id: 'item2', name: 'MAVİ GEZEGEN', icon: '🌍', price: 1000, desc: 'Strateji oyunu için mavi tema.'},
            {id: 'item3', name: 'HIZ MODU', icon: '⚡', price: 2000, desc: 'Arcade XP kazancını 2x yapar.'},
            {id: 'item4', name: 'HAYALET MODU', icon: '👻', price: 5000, desc: 'Horror oyununda gizli sonları açar.'},
            {id: 'item5', name: 'NEON PARILTI', icon: '✨', price: 8000, desc: 'Tüm oyunlarda particle efektleri.'},
            {id: 'item6', name: 'ZAMAN YOLCUSU', icon: '⏰', price: 10000, desc: 'Arcade\'de zaman yavaşlar.'}
        ];
        function updateDisplay() { document.getElementById('currentXP').innerText = xp; document.getElementById('balance').innerText = xp; }
        function showNotif(text, isError) { const n = document.getElementById('notif'); n.innerText = text; n.className = 'notification' + (isError ? ' error' : ''); n.classList.add('show'); setTimeout(() => n.classList.remove('show'), 2000); }
        function render() {
            updateDisplay();
            document.getElementById('grid').innerHTML = items.map(item => `
                <div class="item ${owned.includes(item.id) ? 'owned' : ''}">
                    <div class="item-icon">${item.icon}</div>
                    <h3>${item.name}</h3>
                    <p>${item.desc}</p>
                    <div class="price">${item.price} XP</div>
                    <button class="btn" onclick="buy('${item.id}', ${item.price})" ${owned.includes(item.id) ? 'disabled' : ''}>
                        ${owned.includes(item.id) ? '✓ SAHİPSİN' : 'SATIN AL'}
                    </button>
                </div>
            `).join('');
        }
        function buy(id, price) {
            if(xp >= price && !owned.includes(id)) {
                xp -= price; owned.push(id);
                localStorage.setItem('cano_xp', xp);
                localStorage.setItem('cano_items', JSON.stringify(owned));
                render(); showNotif('SATIN ALINDI!', false);
            } else if(xp < price) { showNotif('YETERSİZ XP!', true); }
        }
        render();
    </script>
</body>
</html>
"""

# ============ NEON ARCADE (GELİŞMİŞ) ============
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEON ARCADE | Cano Studio</title>
    <style>""" + base_css + """
        body { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; background: radial-gradient(ellipse at center, #0a0a1a 0%, #000 100%); }
        .game-ui { position: fixed; top: 20px; width: 100%; text-align: center; z-index: 10; }
        .score-display { font-family: 'Orbitron', sans-serif; font-size: 3rem; color: #fff; text-shadow: 0 0 20px rgba(255,69,0,0.8); }
        .high-score { color: #666; font-size: 0.9rem; margin-top: 5px; }
        canvas { border: 3px solid rgba(255,69,0,0.3); border-radius: 8px; box-shadow: 0 0 40px rgba(255,69,0,0.2); max-width: 95vw; background: #000; }
        .controls { position: fixed; bottom: 80px; text-align: center; color: #444; font-size: 0.8rem; }
        .game-over { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 100; }
        .game-over h2 { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: var(--neon-orange); margin-bottom: 20px; text-shadow: 0 0 30px rgba(255,69,0,0.8); }
        .game-over p { color: #888; margin-bottom: 30px; font-size: 1.2rem; }
        .final-score { color: #fff; font-family: 'Orbitron', sans-serif; font-size: 2rem; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="game-ui">
        <div class="score-display" id="sc">0</div>
        <div class="high-score">HIGH SCORE: <span id="hs">0</span></div>
    </div>
    <canvas id="gc" width="400" height="600"></canvas>
    <div class="controls">SPACE / TIKLA / YUKARI OK</div>
    <div class="game-over" id="go">
        <h2>GAME OVER</h2>
        <p>Neon şehir seni yuttu...</p>
        <div class="final-score">SKOR: <span id="fs">0</span></div>
        <button class="btn" onclick="resetGame()">TEKRAR DENE</button>
    </div>
    <a href="/" class="back-btn">← ÇIKIŞ</a>
    <script>
        const canvas = document.getElementById("gc"), ctx = canvas.getContext("2d");
        let bird = {y: 300, v: 0, g: 0.6, jump: -10, rot: 0};
        let pipes = [], particles = [], stars = [];
        let frames = 0, score = 0, highScore = parseInt(localStorage.getItem('arcade_hs')) || 0;
        let isGameOver = false, gameStarted = false;
        let items = JSON.parse(localStorage.getItem('cano_items')) || [];
        let hasTimeSlow = items.includes('item6'), hasGoldSkin = items.includes('item1');
        
        document.getElementById('hs').innerText = highScore;
        
        // Stars background
        for(let i=0; i<100; i++) stars.push({x: Math.random()*400, y: Math.random()*600, s: Math.random()*1.5, speed: Math.random()*0.5+0.1});
        
        function addXP(amt) {
            let mult = items.includes('item3') ? 2 : 1;
            let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
            localStorage.setItem('cano_xp', xp + (amt * mult));
        }
        
        function createParticles(x, y, color) {
            for(let i=0; i<5; i++) {
                particles.push({x: x, y: y, vx: (Math.random()-0.5)*4, vy: (Math.random()-0.5)*4, life: 30, color: color});
            }
        }
        
        function draw() {
            // Background
            let grad = ctx.createLinearGradient(0, 0, 0, 600);
            grad.addColorStop(0, "#0a0a2e"); grad.addColorStop(0.5, "#1a0a2e"); grad.addColorStop(1, "#000");
            ctx.fillStyle = grad; ctx.fillRect(0,0,400,600);
            
            // Stars
            ctx.fillStyle = "white";
            stars.forEach(s => { s.x -= s.speed; if(s.x<0) s.x=400; ctx.beginPath(); ctx.arc(s.x, s.y, s.s, 0, Math.PI*2); ctx.fill(); });
            
            if(!gameStarted) {
                ctx.fillStyle = "rgba(0,0,0,0.7)"; ctx.fillRect(0,0,400,600);
                ctx.fillStyle = "#ff4500"; ctx.font = "bold 24px Orbitron"; ctx.textAlign = "center";
                ctx.fillText("NEON ARCADE", 200, 250);
                ctx.font = "16px Rajdhani"; ctx.fillStyle = "#888";
                ctx.fillText("BAŞLAMAK İÇİN TIKLA", 200, 300);
                requestAnimationFrame(draw);
                return;
            }
            
            if(isGameOver) return;
            
            // Bird physics
            bird.v += bird.g; bird.y += bird.v; bird.rot = Math.min(Math.max(bird.v * 0.1, -0.5), 0.5);
            if(bird.y > 580 || bird.y < 0) gameOver();
            
            // Draw bird
            ctx.save(); ctx.translate(60, bird.y); ctx.rotate(bird.rot);
            ctx.fillStyle = hasGoldSkin ? "#FFD700" : "#fff";
            ctx.shadowBlur = 20; ctx.shadowColor = hasGoldSkin ? "#FFD700" : "#fff";
            ctx.fillRect(-15, -15, 30, 30);
            ctx.fillStyle = "#ff4500"; ctx.fillRect(5, -5, 10, 10);
            ctx.restore(); ctx.shadowBlur = 0;
            
            // Pipes
            let speed = hasTimeSlow ? 2.5 : 4;
            if(frames % (hasTimeSlow ? 120 : 90) === 0) {
                let h = Math.random()*250+80;
                pipes.push({x: 400, h: h, passed: false});
            }
            
            for(let i=pipes.length-1; i>=0; i--) {
                let p = pipes[i]; p.x -= speed;
                
                // Gradient pipes
                let pg = ctx.createLinearGradient(p.x, 0, p.x+60, 0);
                pg.addColorStop(0, "#ff4500"); pg.addColorStop(0.5, "#ff6b35"); pg.addColorStop(1, "#ff4500");
                ctx.fillStyle = pg; ctx.shadowBlur = 20; ctx.shadowColor = "#ff4500";
                ctx.fillRect(p.x, 0, 60, p.h); ctx.fillRect(p.x, p.h+140, 60, 600);
                ctx.shadowBlur = 0;
                
                // Collision
                if(60+20 > p.x && 40 < p.x+60 && (bird.y-15 < p.h || bird.y+15 > p.h+140)) {
                    createParticles(60, bird.y, "#ff4500"); gameOver();
                }
                
                // Score
                if(p.x < 40 && !p.passed) { 
                    p.passed = true; score++; document.getElementById("sc").innerText = score;
                    addXP(10); createParticles(p.x, p.h+70, "#00ff00");
                }
                
                if(p.x < -60) pipes.splice(i,1);
            }
            
            // Particles
            for(let i=particles.length-1; i>=0; i--) {
                let p = particles[i]; p.x += p.vx; p.y += p.vy; p.life--;
                ctx.fillStyle = p.color; ctx.globalAlpha = p.life/30;
                ctx.fillRect(p.x, p.y, 3, 3); ctx.globalAlpha = 1;
                if(p.life <= 0) particles.splice(i,1);
            }
            
            frames++; requestAnimationFrame(draw);
        }
        
        function gameOver() {
            isGameOver = true;
            if(score > highScore) { localStorage.setItem('arcade_hs', score); highScore = score; }
            document.getElementById('fs').innerText = score;
            document.getElementById('go').style.display = 'flex';
        }
        
        function resetGame() {
            bird = {y: 300, v: 0, g: 0.6, jump: -10, rot: 0};
            pipes = []; particles = []; frames = 0; score = 0;
            isGameOver = false; gameStarted = true;
            document.getElementById('sc').innerText = '0';
            document.getElementById('go').style.display = 'none';
            draw();
        }
        
        function jump() {
            if(isGameOver) { resetGame(); return; }
            if(!gameStarted) gameStarted = true;
            bird.v = bird.jump; createParticles(60, bird.y, "#fff");
        }
        
        canvas.addEventListener("mousedown", jump);
        canvas.addEventListener("touchstart", (e)=>{e.preventDefault(); jump();});
        document.addEventListener("keydown", (e)=>{ if(e.code==="Space"||e.code==="ArrowUp") jump(); });
        
        draw();
    </script>
</body>
</html>
"""

# ============ STRATEJI (GELİŞMİŞ) ============
strateji_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GALAKTIK STRATEJI | Cano Studio</title>
    <style>""" + base_css + """
        body { overflow: hidden; background: radial-gradient(ellipse at center, #0a0a1a 0%, #000 100%); }
        .ui-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; }
        .level-display { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: var(--neon-orange); text-shadow: 0 0 20px rgba(255,69,0,0.8); }
        .planet-count { position: absolute; top: 60px; left: 50%; transform: translateX(-50%); color: #666; font-size: 0.9rem; }
        .tutorial { position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); color: #444; text-align: center; font-size: 0.85rem; opacity: 0.8; }
        canvas { display: block; }
    </style>
</head>
<body>
    <div class="ui-layer">
        <div class="level-display">SEVIYE <span id="ld">1</span></div>
        <div class="planet-count">GEZEGENLER: <span id="pc">1</span> / <span id="tc">3</span></div>
        <div class="tutorial">GEZEGENE TIKLA → HEDEF SEÇ → FİLO GÖNDER</div>
    </div>
    <canvas id="sc"></canvas>
    <a href="/" class="back-btn">← GERİ</a>
    <script>
        const canvas = document.getElementById("sc"), ctx = canvas.getContext("2d");
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        
        let planets = [], fleets = [], particles = [], stars = [];
        let selected = null, level = 1, gameWon = false;
        let items = JSON.parse(localStorage.getItem('cano_items')) || [];
        let hasBlueTheme = items.includes('item2');
        
        // Stars
        for(let i=0; i<150; i++) stars.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, size: Math.random()*1.5, blink: Math.random()*0.1});
        
        class Planet {
            constructor(x, y, size, owner, count) {
                this.x = x; this.y = y; this.size = size; this.owner = owner; this.count = count;
                this.max = size * 0.8; this.growth = 0; this.pulse = 0;
            }
            draw() {
                this.pulse += 0.05;
                let glow = Math.sin(this.pulse) * 10 + 20;
                
                // Glow
                let g = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size + glow);
                if(this.owner === 1) { g.addColorStop(0, hasBlueTheme ? "rgba(0,212,255,0.8)" : "rgba(0,212,255,0.5)"); g.addColorStop(1, "transparent"); }
                else if(this.owner === 2) { g.addColorStop(0, "rgba(255,69,0,0.5)"); g.addColorStop(1, "transparent"); }
                else { g.addColorStop(0, "rgba(255,255,255,0.1)"); g.addColorStop(1, "transparent"); }
                ctx.fillStyle = g; ctx.beginPath(); ctx.arc(this.x, this.y, this.size + glow, 0, Math.PI*2); ctx.fill();
                
                // Planet body
                let pg = ctx.createRadialGradient(this.x - this.size*0.3, this.y - this.size*0.3, 0, this.x, this.y, this.size);
                if(this.owner === 1) { pg.addColorStop(0, hasBlueTheme ? "#55eaff" : "#00d4ff"); pg.addColorStop(1, hasBlueTheme ? "#0055aa" : "#003355"); }
                else if(this.owner === 2) { pg.addColorStop(0, "#ff6b35"); pg.addColorStop(1, "#882200"); }
                else { pg.addColorStop(0, "#666"); pg.addColorStop(1, "#222"); }
                ctx.fillStyle = pg; ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI*2); ctx.fill();
                
                // Ring for selected
                if(selected === this) {
                    ctx.strokeStyle = "#fff"; ctx.lineWidth = 3; ctx.setLineDash([5, 5]);
                    ctx.beginPath(); ctx.arc(this.x, this.y, this.size + 10, 0, Math.PI*2); ctx.stroke(); ctx.setLineDash([]);
                }
                
                // Count
                ctx.fillStyle = "#fff"; ctx.font = "bold 16px Orbitron"; ctx.textAlign = "center";
                ctx.fillText(Math.floor(this.count), this.x, this.y + 5);
            }
            update() {
                if(this.owner !== 0) {
                    this.growth++;
                    if(this.growth > 60) { this.count = Math.min(this.count + 1, this.max); this.growth = 0; }
                }
            }
        }
        
        function addXP(amt) {
            let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
            localStorage.setItem('cano_xp', xp + amt);
        }
        
        function init() {
            planets = []; fleets = []; gameWon = false;
            document.getElementById("ld").innerText = level;
            let playerPlanet = new Planet(100, canvas.height/2, 45, 1, 20);
            planets.push(playerPlanet);
            
            let enemyCount = level > 3 ? 2 : 1;
            for(let i=0; i<enemyCount; i++) {
                planets.push(new Planet(canvas.width-100 - i*150, (canvas.height/(enemyCount+1))*(i+1), 40, 2, 15 + level*5));
            }
            
            let neutralCount = 2 + Math.floor(level/2);
            for(let i=0; i<neutralCount; i++) {
                let x = 200 + Math.random()*(canvas.width-400);
                let y = 100 + Math.random()*(canvas.height-200);
                if(!planets.some(p => Math.hypot(p.x-x, p.y-y) < 100)) {
                    planets.push(new Planet(x, y, 30, 0, 10));
                }
            }
            updateCounts();
        }
        
        function updateCounts() {
            let player = planets.filter(p => p.owner === 1).length;
            let total = planets.length;
            document.getElementById('pc').innerText = player;
            document.getElementById('tc').innerText = total;
        }
        
        canvas.addEventListener("mousedown", (e) => {
            let p = planets.find(p => Math.hypot(p.x - e.clientX, p.y - e.clientY) < p.size);
            if(!p) { selected = null; return; }
            if(p.owner === 1) { selected = p; }
            else if(selected && selected.owner === 1) {
                let amount = Math.floor(selected.count / 2);
                if(amount > 0) {
                    selected.count -= amount;
                    fleets.push({x: selected.x, y: selected.y, target: p, owner: 1, amount: amount, progress: 0});
                    selected = null;
                }
            }
        });
        
        function loop() {
            ctx.fillStyle = "#050505"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Stars
            stars.forEach(s => { ctx.fillStyle = `rgba(255,255,255,${0.3 + Math.sin(Date.now()*0.001*s.blink)*0.3})`; ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, Math.PI*2); ctx.fill(); });
            
            // Connection lines
            if(selected) {
                planets.forEach(p => {
                    if(p !== selected && p.owner !== 1) {
                        ctx.strokeStyle = "rgba(0,212,255,0.2)"; ctx.lineWidth = 1;
                        ctx.beginPath(); ctx.moveTo(selected.x, selected.y); ctx.lineTo(p.x, p.y); ctx.stroke();
                    }
                });
            }
            
            // Fleets
            for(let i=fleets.length-1; i>=0; i--) {
                let f = fleets[i];
                let dx = f.target.x - f.x, dy = f.target.y - f.y, dist = Math.hypot(dx, dy);
                f.x += (dx/dist) * 5; f.y += (dy/dist) * 5;
                
                // Trail
                ctx.fillStyle = f.owner === 1 ? "#00d4ff" : "#ff4500";
                ctx.beginPath(); ctx.arc(f.x, f.y, 3, 0, Math.PI*2); ctx.fill();
                
                if(dist < 5) {
                    if(f.target.owner === f.owner) { f.target.count += f.amount; }
                    else {
                        f.target.count -= f.amount;
                        if(f.target.count < 0) {
                            f.target.owner = f.owner;
                            f.target.count = Math.abs(f.target.count);
                            addXP(50); createExplosion(f.target.x, f.target.y, "#00d4ff");
                        }
                    }
                    fleets.splice(i, 1); updateCounts();
                }
            }
            
            // AI
            if(frames % 120 === 0) {
                let enemyPlanets = planets.filter(p => p.owner === 2);
                let myPlanets = planets.filter(p => p.owner === 1);
                let neutralPlanets = planets.filter(p => p.owner === 0);
                
                enemyPlanets.forEach(ep => {
                    if(ep.count > 15) {
                        let targets = [...myPlanets, ...neutralPlanets].filter(p => p.count < ep.count);
                        if(targets.length > 0) {
                            let target = targets[Math.floor(Math.random()*targets.length)];
                            let amount = Math.floor(ep.count / 2);
                            ep.count -= amount;
                            fleets.push({x: ep.x, y: ep.y, target: target, owner: 2, amount: amount, progress: 0});
                        }
                    }
                });
            }
            
            planets.forEach(p => { p.update(); p.draw(); });
            
            // Win check
            if(!gameWon && !planets.some(p => p.owner === 2)) {
                gameWon = true; level++; addXP(100 + level*50);
                setTimeout(() => { alert("SEVIYE TAMAMLANDI! +" + (100 + level*50) + " XP"); init(); }, 500);
            }
            
            // Lose check
            if(!planets.some(p => p.owner === 1)) {
                setTimeout(() => { if(confirm("KAYBETTIN! Tekrar dene?")) { level = 1; init(); } }, 100);
            }
            
            frames++; requestAnimationFrame(loop);
        }
        
        let frames = 0;
        function createExplosion(x, y, color) {
            for(let i=0; i<20; i++) {
                particles.push({x: x, y: y, vx: (Math.random()-0.5)*8, vy: (Math.random()-0.5)*8, life: 40, color: color});
            }
        }
        
        window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; init(); });
        init(); loop();
    </script>
</body>
</html>
"""

# ============ HORROR (GELİŞMİŞ) ============
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DARK HORROR | Cano Studio</title>
    <style>""" + base_css + """
        body { background: #000; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; font-family: 'Courier New', monospace; }
        .game-container { max-width: 600px; width: 100%; border: 2px solid #300; border-radius: 8px; padding: 40px; background: linear-gradient(180deg, #0a0000 0%, #000 100%); position: relative; overflow: hidden; }
        .game-container::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,0,0,0.03) 2px, rgba(255,0,0,0.03) 4px); pointer-events: none; }
        .glitch-text { font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: #800; text-align: center; margin-bottom: 30px; text-shadow: 2px 2px 4px rgba(255,0,0,0.5); animation: glitch 3s infinite; position: relative; }
        @keyframes glitch { 0%, 100% { transform: translate(0); } 20% { transform: translate(-2px, 2px); } 40% { transform: translate(-2px, -2px); } 60% { transform: translate(2px, 2px); } 80% { transform: translate(2px, -2px); } }
        .story-text { color: #aaa; line-height: 1.8; margin-bottom: 30px; font-size: 1rem; min-height: 100px; border-left: 3px solid #300; padding-left: 20px; }
        .choices { display: flex; flex-direction: column; gap: 12px; }
        .choice-btn { background: transparent; border: 1px solid #500; color: #888; padding: 18px; cursor: pointer; font-family: 'Courier New', monospace; font-size: 0.95rem; transition: all 0.3s; text-align: left; position: relative; overflow: hidden; }
        .choice-btn::before { content: '>'; position: absolute; left: -20px; transition: left 0.3s; color: #f00; }
        .choice-btn:hover { border-color: #f00; color: #fff; background: rgba(255,0,0,0.1); padding-left: 30px; }
        .choice-btn:hover::before { left: 10px; }
        .ending { text-align: center; padding: 40px; }
        .ending h2 { font-family: 'Orbitron', sans-serif; color: #f00; font-size: 2rem; margin-bottom: 20px; text-shadow: 0 0 20px rgba(255,0,0,0.8); }
        .ending p { color: #666; margin-bottom: 30px; }
        .xp-gain { color: #ff4500; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 20px; }
        .progress-bar { width: 100%; height: 4px; background: #111; margin-bottom: 30px; border-radius: 2px; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #300, #f00); width: 0%; transition: width 0.5s; }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="progress-bar"><div class="progress-fill" id="prog"></div></div>
        <h1 class="glitch-text" id="title">KARANLIK YOL</h1>
        <p class="story-text" id="story">Yol ikiye ayrılıyor. Bir tarafta terk edilmiş bir akıl hastanesi, diğer tarafta ise sisli bir mezarlık var. Rüzgar çığlık gibi çıkıyor...</p>
        <div class="choices" id="choices">
            <button class="choice-btn" onclick="choose(1)">Hastaneye gir - Paslanmış kapı gıcırdıyor</button>
            <button class="choice-btn" onclick="choose(2)">Mezarlığa sap - Toprak nemli kokuyor</button>
        </div>
    </div>
    <a href="/" class="back-btn">← KAÇ</a>
    
    <script>
        let items = JSON.parse(localStorage.getItem('cano_items')) || [];
        let hasGhostMode = items.includes('item4');
        
        function addXP(amt) {
            let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
            localStorage.setItem('cano_xp', xp + amt);
        }
        
        const story = {
            1: { title: "HASTANE", text: "İçeride tekerlekli bir sandalye kendiliğinden hareket ediyor. Zeminde kan lekeleri var.", choices: [{text: "Sandalyeyi takip et", next: 31}, {text: "Aceleyle kaç", next: 4}] },
            2: { title: "MEZARLIK", text: "Topraktan bir el çıktı! Mezar taşlarında ismin yazıyor...", choices: [{text: "Elin üzerine bas", next: 32}, {text: "Teslim ol", next: 33}] },
            4: { title: "ORMAN", text: "Ormana girdin ama ağaçlar seni takip ediyor. Gözler her yerde.", choices: [{text: "Sadece yürü", next: 5}, {text: "Koşmaya çalış", next: 34}] },
            5: { title: "KAPKARANLIK", text: "Işık tamamen kayboldu. Sadece nefes alışını duyuyorsun.", choices: [{text: "Yürümeye devam et", next: 6}, {text: "Geri dön", next: 35}] },
            6: { title: "KULÜBE", text: "Eski bir kulübe. İçeriden fısıltılar geliyor.", choices: [{text: "Kapıyı aç", next: 7}, {text: "Pencereden bak", next: 36}] },
            7: { title: "KİTAPLIK", text: "Adının yazdığı bir kitap var. Son sayfa boş.", choices: [{text: "Kitabı oku", next: 8}, {text: "Kitabı yak", next: 37}] },
            8: { title: "AYNA", text: "Yansıman sana gülümsedi. Ama sen gülümsemedin.", choices: [{text: "Aynaya dokun", next: 9}, {text: "Aynayı kır", next: 38}] },
            9: { title: "BOŞLUK", text: "Aynanın içine çekildin. Yerçekimi yok.", choices: [{text: "Yüzeye doğru yüz", next: 10}, {text: "Derinlere dal", next: 39}] },
            10: { title: "SAAT KULESI", text: "Dev bir saat kulesi. Akrepler geriye dönüyor.", choices: [{text: "Kuleye tırman", next: 11}, {text: "Saati durdur", next: 40}] },
            11: { title: "ÇAN", text: "Çan çalıyor, kulakların kanıyor! Zaman daralıyor.", choices: [{text: "Kuleden atla", next: 12}, {text: "Kulaklarını kapat", next: 41}] },
            12: { title: "GÖL", text: "Siyah bir gölün kenarındasın. Yüzeyde yıldızlar yansıyor.", choices: [{text: "Göle gir", next: 13}, {text: "Ormana kaç", next: 42}] },
            13: { title: "SUALTI ŞEHRİ", text: "Suyun altında bir şehir var. Binalar tersten inşa edilmiş.", choices: [{text: "Şehre dal", next: 14}, {text: "Yüzeye çık", next: 43}] },
            14: { title: "MUHAFIZ", text: "Dev bir bekçi duruyor. Gözleri kapalı ama seni görüyor.", choices: [{text: "Saldır", next: 15}, {text: "Konuş", next: 44}] },
            15: { title: "TAHT", text: "Taht seni bekliyor. Oturursan hükümran olursun ama hapis de...", choices: [{text: "Tahta otur", next: 45}, {text: "Reddet ve kaç", next: 16}] },
            16: { title: "IŞIK", text: "Her şey dağılıyor. Beyaz bir ışık seni çağırıyor.", choices: [{text: "Işığa yürü", next: 46}, {text: "Karanlıkta kal", next: 17}] },
            17: { title: "LABİRENT", text: "Sonsuz koridordasın. Duvarlarda kendi yüzün var.", choices: [{text: "Sola dön", next: 18}, {text: "Sağa dön", next: 47}] },
            18: { title: "KASAP", text: "Önünde bir kasap duruyor. Bıçağında senin adın yazıyor.", choices: [{text: "Yanından geç", next: 19}, {text: "Bıçağı al", next: 48}] },
            19: { title: "KAPI", text: "30 kilitli bir kapı. Her kilidin üzerinde bir anın var.", choices: [{text: "Kilitleri kır", next: 20}, {text: "Anahtarları bul", next: 49}] },
            20: { title: "BOŞLUK", text: "Kapı açıldı, arkası boşluk. Ama aşağıda bir şey var.", choices: [{text: "Atla", next: 50}, {text: "Geri çekil", next: 21}] },
            21: { title: "HAYALETLER", text: "Eski dostlarını gördün. Onlar öldü, sen yaşıyorsun.", choices: [{text: "Onlarla kal", next: 51}, {text: "Koş", next: 22}] },
            22: { title: "MAĞARA", text: "Bir mağaraya sığındın. Duvarlarda mağara resimleri... gelecekten.", choices: [{text: "Ateş yak", next: 52}, {text: "Derinlere in", next: 23}] },
            23: { title: "FOSILLER", text: "Fosiller canlanıyor. Dinozorlar konuşuyor.", choices: [{text: "Dinle", next: 53}, {text: "Kaç", next: 24}] },
            24: { title: "TREN", text: "Bir tren bekliyor. Makinist sensin.", choices: [{text: "Trene bin", next: 54}, {text: "Yürümeye devam et", next: 25}] },
            25: { title: "HIZ", text: "Tren kendi gidiyor. Raylar olmayan yerlere.", choices: [{text: "Freni çek", next: 55}, {text: "Hızlan", next: 26}] },
            26: { title: "DAĞ", text: "Karların içindesin. Ayak izlerin geriye gitmiyor.", choices: [{text: "Zirveye tırman", next: 56}, {text: "Mağaraya gir", next: 27}] },
            27: { title: "KARTAL", text: "Dev kartal seni kaptı. Gökyüzünde özgürsün.", choices: [{text: "Kurtulmaya çalış", next: 57}, {text: "Uçmaya devam et", next: 28}] },
            28: { title: "SARAY", text: "Bulutların üzerinde bir saray. Her şey beyaz.", choices: [{text: "Saraya in", next: 58}, {text: "Düşmeye bırak kendini", next: 29}] },
            29: { title: "DALGA", text: "Dev dalga geliyor. Tsunami değil, zamanın kendisi.", choices: [{text: "Yüz", next: 59}, {text: "Dalganın altına gir", next: 30}] },
            30: { title: "SON KAPI", text: "İki kapı var. Soldaki cennet gibi, sağdaki cehennem gibi ama...", choices: [{text: "Sol kapı", next: 60}, {text: "Sağ kapı", next: 60}] },
            
            // SONLAR (30 farklı son)
            31: { title: "SON: AMELIYAT", text: "Ameliyat masasındasın. Başarısız olundu. Yeniden doğuyorsun...", ending: true, xp: 20 },
            32: { title: "SON: ZAFER", text: "Mezardan çıktın. Artık ölümsüzsün. Ama yalnızsın...", ending: true, xp: 150 },
            33: { title: "SON: BEKÇI", text: "Mezarlığın bekçisi oldun. Sonsuza dek...", ending: true, xp: 30 },
            34: { title: "SON: AV", text: "Ağaçlar seni yakaladı. Onların besini oldun...", ending: true, xp: 10 },
            35: { title: "SON: DÖNGÜ", text: "Başa döndün. Bu kaçıncı tur?", ending: true, xp: 5 },
            36: { title: "SON: DONDURMA", text: "Kulübede dondun. Buzdan bir heykel oldun...", ending: true, xp: 15 },
            37: { title: "SON: PATLAMA", text: "Kitap alev aldı. Her şey yanıyor...", ending: true, xp: 40 },
            38: { title: "SON: LANET", text: "Ayna kırıldı. Yedi yıl şanssızlık...", ending: true, xp: 20 },
            39: { title: "SON: HEYKEL", text: "Derinlerde taşlaştın. Denizaltı şehriinin yeni sakinisin...", ending: true, xp: 35 },
            40: { title: "SON: EZILME", text: "Saat kulesi çöktü. Zamansız öldün...", ending: true, xp: 10 },
            41: { title: "SON: SESSIZLIK", text: "Kulakların kanadı. Sonsuz sessizlik...", ending: true, xp: 50 },
            42: { title: "SON: SUSUZLUK", text: "Ormanda kayboldun. Susuzluktan...", ending: true, xp: 15 },
            43: { title: "SON: BALIK", text: "Deniz canavarı seni yedi. Sindirim süreci başladı...", ending: true, xp: 25 },
            44: { title: "SON: ZINDAN", text: "Bekçi seni hapse attı. Sonsuz karanlık...", ending: true, xp: 45 },
            45: { title: "SON: ZEHIR", text: "Taht zehirliymiş. Krallık hayal oldu...", ending: true, xp: 100 },
            46: { title: "SON: UYANIŞ", text: "Rüyaymış! Ama gerçek daha korkunç...", ending: true, xp: 200 },
            47: { title: "SON: DUVARLAR", text: "Labirentte hapsoldun. Duvarlar daralıyor...", ending: true, xp: 15 },
            48: { title: "SON: YEMEK", text: "Kasap seni doğradı. Akşam yemeği oldun...", ending: true, xp: 30 },
            49: { title: "SON: YAŞLILIK", text: "Anahtarları ararken yaşlandın. Ömrün yetmedi...", ending: true, xp: 60 },
            50: { title: "SON: BOŞLUK", text: "Boşluğa düştün. Düşüyorsun hala...", ending: true, xp: 80 },
            51: { title: "SON: RUH", text: "Hayaletlerle kaldın. Artık onlardan birisin...", ending: true, xp: 120 },
            52: { title: "SON: ATEŞ", text: "Ateş söndü. Soğuktan dondun...", ending: true, xp: 25 },
            53: { title: "SON: KUTSAL", text: "Dinozorlar sana bilgelik verdiler. Göğe yükseldin...", ending: true, xp: 180 },
            54: { title: "SON: KAZA", text: "Tren raydan çıktı. Son durak...", ending: true, xp: 40 },
            55: { title: "SON: YANLIŞ DURAK", text: "Yanlış yerde indin. Burası hiçbir yer...", ending: true, xp: 70 },
            56: { title: "SON: AYI", text: "Ayı seni parçaladı. Doğanın kuralları...", ending: true, xp: 10 },
            57: { title: "SON: KASABA", text: "Kartal seni bir kasabaya bıraktı. Hayatına devam ediyorsun...", ending: true, xp: 300 },
            58: { title: "SON: ÜTOPYA", text: "Bulut sarayında huzur buldun. Sonsuz barış...", ending: true, xp: 250 },
            59: { title: "SON: BOĞULMA", text: "Dalga seni yuttu. Denizin derinliklerindeyim...", ending: true, xp: 5 },
            60: { title: "SON: KIYAMET", text: "İki kapı da aynı yere çıktı. Kıyamet seninle başladı...", ending: true, xp: 500 }
        };
        
        let currentNode = 1;
        let path = [];
        
        function updateProgress() {
            let progress = (path.length / 10) * 100;
            document.getElementById('prog').style.width = progress + '%';
        }
        
        function choose(id) {
            path.push(id);
            let node = story[id];
            
            if(node.ending) {
                addXP(node.xp);
                document.querySelector('.game-container').innerHTML = `
                    <div class="ending">
                        <h2>${node.title}</h2>
                        <p>${node.text}</p>
                        <div class="xp-gain">+${node.xp} XP KAZANDIN</div>
                        <button class="btn" onclick="location.href='/'">PORTALA DÖN</button>
                    </div>
                `;
                return;
            }
            
            document.getElementById('title').innerText = node.title;
            document.getElementById('story').innerText = node.text;
            document.getElementById('choices').innerHTML = node.choices.map(c => 
                `<button class="choice-btn" onclick="choose(${c.next})">${c.text}</button>`
            ).join('');
            
            updateProgress();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return ana_sayfa_html
@app.route('/store')
def store(): return store_html
@app.route('/neon-arcade')
def arcade(): return arcade_html
@app.route('/strateji')
def strateji(): return strateji_html
@app.route('/horror')
def horror(): return horror_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
