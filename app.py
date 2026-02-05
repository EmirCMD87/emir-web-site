from flask import Flask
import os

app = Flask(__name__)

# --- 1. ANA SAYFA (PORTAL) ---
ana_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cano Studio | Portal</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;500&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; touch-action: manipulation; }
        body { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #050505 100%); z-index: -1; }
        
        .xp-container { position: fixed; top: 20px; right: 20px; background: rgba(255,69,0,0.1); border: 1px solid #ff4500; padding: 10px 20px; border-radius: 50px; z-index: 100; display: flex; align-items: center; gap: 10px; }
        .xp-val { color: #ff4500; font-weight: bold; font-family: 'Syncopate'; }

        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 60px 20px; }
        h1 { font-family: 'Syncopate', sans-serif; font-size: clamp(1.5rem, 6vw, 4rem); letter-spacing: 10px; text-transform: uppercase; margin-bottom: 40px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; width: 100%; max-width: 1100px; }
        .card { background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.05); padding: 40px 30px; border-radius: 4px; cursor: pointer; transition: 0.3s; text-decoration: none; }
        .card:hover { border-color: #ff4500; transform: translateY(-5px); background: rgba(255,69,0,0.02); }
        .card h2 { font-family: 'Syncopate'; font-size: 0.8rem; color: #fff; margin-bottom: 10px; letter-spacing: 3px; }
        .card p { color: #555; font-size: 0.75rem; }
        
        .store-card { border-color: #00d4ff !important; }
        .store-card:hover { box-shadow: 0 0 20px rgba(0,212,255,0.1); }
        
        footer { margin-top: 50px; font-size: 0.6rem; color: #222; text-align: center; letter-spacing: 3px; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="xp-container">
        <span style="font-size: 0.6rem; letter-spacing: 1px;">TOTAL XP:</span>
        <span class="xp-val" id="totalXP">0</span>
    </div>

    <section class="hero">
        <h1>CANO STUDIO</h1>
        <div class="grid">
            <a href="/neon-arcade" class="card"><h2>NEON ARCADE</h2><p>Hız ve Refleks Testi</p></a>
            <a href="/strateji" class="card"><h2>STRATEJI</h2><p>30 Seviye Fetih Modu</p></a>
            <a href="/horror" class="card"><h2>HORROR</h2><p>Karanlık Seçimler</p></a>
            <a href="/store" class="card store-card"><h2>MAĞAZA</h2><p style="color:#00d4ff">XP Harca & Skin Al</p></a>
        </div>
        <footer>© 2026 DESIGNED BY CANO</footer>
    </section>

    <script>
        let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
        document.getElementById('totalXP').innerText = xp;
    </script>
</body>
</html>
"""

# --- 2. MAĞAZA SAYFASI (YENİ) ---
store_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cano Store</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400&display=swap');
        body { background: #050505; color: #fff; font-family: 'Inter', sans-serif; margin: 0; padding: 40px 20px; text-align: center; }
        .xp-display { font-family: 'Syncopate'; color: #ff4500; font-size: 1.5rem; margin-bottom: 40px; }
        .store-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; max-width: 900px; margin: 0 auto; }
        .item { background: #0a0a0a; border: 1px solid #222; padding: 30px; border-radius: 8px; transition: 0.3s; }
        .item:hover { border-color: #00d4ff; }
        .item.owned { border-color: #00ff00; opacity: 0.6; }
        .price { font-family: 'Syncopate'; color: #ff4500; margin: 15px 0; }
        .buy-btn { background: #ff4500; color: #fff; border: none; padding: 12px 25px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; }
        .buy-btn:disabled { background: #222; color: #555; cursor: not-allowed; }
        .back { display: inline-block; margin-top: 50px; color: #444; text-decoration: none; font-size: 0.8rem; letter-spacing: 2px; }
    </style>
</head>
<body>
    <h1 style="font-family:'Syncopate'; letter-spacing:10px;">MAĞAZA</h1>
    <div class="xp-display">XP: <span id="currentXP">0</span></div>
    
    <div class="store-grid">
        <div class="item" id="item1">
            <h2>ALTIN KARE</h2>
            <p>Arcade karakterini altına dönüştürür.</p>
            <div class="price">500 XP</div>
            <button class="buy-btn" onclick="buy('item1', 500)">SATIN AL</button>
        </div>
        <div class="item" id="item2">
            <h2>KOZMIK MAVİ</h2>
            <p>Gezegenlerini neon maviye boyar.</p>
            <div class="price">1000 XP</div>
            <button class="buy-btn" onclick="buy('item2', 1000)">SATIN AL</button>
        </div>
    </div>
    
    <a href="/" class="back">← PORTALA DÖN</a>

    <script>
        let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
        let owned = JSON.parse(localStorage.getItem('cano_items')) || [];
        
        function updateUI() {
            document.getElementById('currentXP').innerText = xp;
            owned.forEach(id => {
                const el = document.getElementById(id);
                if(el) {
                    el.classList.add('owned');
                    const btn = el.querySelector('button');
                    btn.innerText = "ALINDI";
                    btn.disabled = true;
                }
            });
        }
        
        function buy(id, price) {
            if(xp >= price) {
                xp -= price;
                owned.push(id);
                localStorage.setItem('cano_xp', xp);
                localStorage.setItem('cano_items', JSON.stringify(owned));
                updateUI();
            } else { alert("XP Yetersiz!"); }
        }
        updateUI();
    </script>
</body>
</html>
"""

# --- 3. NEON ARCADE ---
# (Burada Game Over ekranı ve XP toplama var)
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
        body { background: #000; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; font-family: sans-serif; }
        canvas { border: 2px solid #ff4500; background: #050505; max-width: 90vw; }
        .back { position: fixed; bottom: 20px; color: #444; text-decoration: none; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div style="position:fixed; top:20px; color:#ff4500; font-size:2rem; font-weight:bold;" id="sc">0</div>
    <canvas id="gc" width="400" height="500"></canvas>
    <a href="/" class="back">← PORTALA DÖN</a>
    <script>
        const canvas = document.getElementById("gc"); const ctx = canvas.getContext("2d");
        let bird = { y: 250, v: 0, g: 0.5, jump: -8 };
        let pipes = []; let frames = 0; let score = 0; let isGameOver = false;

        function addXP(amt) { let xp = parseInt(localStorage.getItem('cano_xp')) || 0; localStorage.setItem('cano_xp', xp + amt); }

        function draw() {
            if(isGameOver) {
                ctx.fillStyle = "rgba(0,0,0,0.8)"; ctx.fillRect(0,0,400,500);
                ctx.fillStyle = "#ff4500"; ctx.font = "bold 30px sans-serif"; ctx.textAlign = "center";
                ctx.fillText("GAME OVER", 200, 230);
                ctx.fillStyle = "#fff"; ctx.font = "14px sans-serif"; ctx.fillText("DOKUN VE BAŞLA", 200, 270);
                return;
            }
            ctx.fillStyle = "#050505"; ctx.fillRect(0,0,400,500);
            let items = JSON.parse(localStorage.getItem('cano_items')) || [];
            ctx.fillStyle = items.includes('item1') ? "#FFD700" : "#fff";
            bird.v += bird.g; bird.y += bird.v; ctx.fillRect(60, bird.y, 25, 25);
            if(frames%100===0) pipes.push({x:400, h:Math.random()*250+50, gap:160});
            for(let i=pipes.length-1; i>=0; i--) {
                pipes[i].x -= 3; ctx.fillStyle = "#111"; ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.fillRect(pipes[i].x, pipes[i].h+160, 50, 500);
                if(60+25 > pipes[i].x && 60 < pipes[i].x+50 && (bird.y < pipes[i].h || bird.y+25 > pipes[i].h+160)) isGameOver = true;
                if(pipes[i].x === 58) { score++; document.getElementById("sc").innerText = score; addXP(10); }
                if(pipes[i].x < -50) pipes.splice(i,1);
            }
            if(bird.y > 500 || bird.y < 0) isGameOver = true;
            frames++; requestAnimationFrame(draw);
        }
        function reset() { bird.y=250; bird.v=0; pipes=[]; score=0; document.getElementById("sc").innerText="0"; isGameOver=false; frames=0; draw(); }
        const act = (e) => { if(isGameOver) reset(); else bird.v = bird.jump; e.preventDefault(); };
        canvas.addEventListener("touchstart", act); canvas.addEventListener("mousedown", act);
        draw();
    </script>
</body>
</html>
"""

# --- 4. STRATEJI (30 LEVEL + XP) ---
strateji_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: manipulation; }
        body { background: #050505; color: #fff; margin: 0; overflow: hidden; font-family: sans-serif; }
        .back { position: fixed; bottom: 20px; left: 20px; color: #444; text-decoration: none; font-size: 0.7rem; }
        .lvl { position: fixed; top: 15px; width: 100%; text-align: center; color: #ff4500; font-weight: bold; }
    </style>
</head>
<body>
    <div class="lvl" id="ld">LEVEL 1</div>
    <canvas id="sc"></canvas>
    <a href="/" class="back">← PORTALA DÖN</a>
    <script>
        const canvas = document.getElementById("sc"); const ctx = canvas.getContext("2d");
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let level = 1; let planets = []; let fleets = []; let selected = null;
        function addXP(amt) { let xp = parseInt(localStorage.getItem('cano_xp')) || 0; localStorage.setItem('cano_xp', xp + amt); }
        class Planet {
            constructor(x,y,s,o,c) { this.x=x; this.y=y; this.s=s; this.owner=o; this.count=c; this.t=0; }
            draw() {
                ctx.beginPath(); ctx.arc(this.x,this.y,this.s,0,Math.PI*2);
                let items = JSON.parse(localStorage.getItem('cano_items')) || [];
                ctx.fillStyle = this.owner===1 ? (items.includes('item2') ? "#00ffff" : "#00d4ff") : (this.owner===2 ? "#ff4500" : "#222");
                ctx.fill(); if(selected === this) { ctx.strokeStyle="#fff"; ctx.lineWidth=2; ctx.stroke(); }
                ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText(Math.floor(this.count), this.x, this.y+5);
            }
            update() { if(this.owner!==0) { this.t++; if(this.t>60) {this.count+=1; this.t=0;} } }
        }
        function init() {
            planets = []; fleets = []; document.getElementById("ld").innerText = "LEVEL " + level;
            planets.push(new Planet(80, canvas.height/2, 35, 1, 20));
            let ec = level > 5 ? 2 : 1;
            for(let i=0; i<ec; i++) planets.push(new Planet(canvas.width-80, (canvas.height/(ec+1))*(i+1), 35, 2, 15+level*5));
            for(let i=0; i<4; i++) planets.push(new Planet(Math.random()*(canvas.width-160)+80, Math.random()*(canvas.height-160)+80, 25, 0, 10));
        }
        function handle(x,y) {
            let p = planets.find(p => Math.sqrt((p.x-x)**2+(p.y-y)**2) < p.s);
            if(p) { if(p.owner===1) selected=p; else if(selected) { fleets.push({x:selected.x, y:selected.y, target:p, owner:1, amount:Math.floor(selected.count/2)}); selected.count/=2; selected=null; } } else selected=null;
        }
        canvas.addEventListener("touchstart", (e) => { handle(e.touches[0].clientX, e.touches[0].clientY); e.preventDefault(); });
        canvas.addEventListener("mousedown", (e) => handle(e.clientX, e.clientY));
        function loop() {
            ctx.fillStyle="#050505"; ctx.fillRect(0,0,canvas.width,canvas.height);
            fleets.forEach((f,i) => {
                let dx=f.target.x-f.x, dy=f.target.y-f.y, dist=Math.sqrt(dx*dx+dy*dy);
                if(dist<5) {
                    if(f.target.owner===f.owner) f.target.count+=f.amount;
                    else { f.target.count-=f.amount; if(f.target.count<0) {f.target.owner=f.owner; f.target.count=Math.abs(f.target.count); addXP(50);} }
                    fleets.splice(i,1);
                } else { f.x+=dx/dist*4; f.y+=dy/dist*4; ctx.fillStyle="#00d4ff"; ctx.fillRect(f.x,f.y,3,3); }
            });
            planets.forEach(p => { p.update(); p.draw(); });
            if(!planets.some(p => p.owner === 2)) { level++; addXP(200); init(); }
            requestAnimationFrame(loop);
        }
        init(); loop();
    </script>
</body>
</html>
"""

# --- 5. HORROR (XP FIX) ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { background: #000; color: #800; font-family: serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; padding: 20px; text-align:center; }
        .game-box { max-width: 500px; border: 1px solid #300; padding: 30px; background: #050000; }
        .text { color: #aaa; margin: 25px 0; font-style: italic; min-height: 80px; }
        .choices { display: flex; flex-direction: column; gap: 10px; }
        button { background: #1a0000; border: 1px solid #500; color: #888; padding: 12px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="game-box">
        <h2 id="t">KARANLIK YOL</h2>
        <p class="text" id="s">Araban bozuldu. İleride ürkütücü bir malikane var.</p>
        <div class="choices" id="c">
            <button onclick="step(1)">Malikaneye Gir</button>
            <button onclick="step(2)">Ormanda Bekle</button>
        </div>
    </div>
    <script>
        function addXP(amt) { 
            let xp = parseInt(localStorage.getItem('cano_xp')) || 0; 
            localStorage.setItem('cano_xp', xp + amt); 
        }
        const data = {
            1: { t: "GİRİŞ", s: "İçeride bir sandık var.", c: [{t:"Sandığı Aç", n:3}, {t:"Üst Kata Çık", n:4}] },
            2: { t: "ORMAN", s: "Vahşi hayvanlar geldi!", c: [{t:"Yeniden", n:"r", xp:20}] },
            3: { t: "HAZİNE", s: "Sandıktan altın fırladı! Kurtuldun.", c: [{t:"Ana Sayfa", n:"r", xp:150}] },
            4: { t: "TUZAK", s: "Zemin çöktü ve öldün.", c: [{t:"Yeniden", n:"r", xp:40}] }
        };
        function step(n) {
            if(n==="r") { location.reload(); return; }
            const s = data[n];
            // Eğer bu seçim bir XP veriyorsa (Son ise)
            if(s.c[0].xp) { addXP(s.c[0].xp); }
            
            document.getElementById("t").innerText = s.t;
            document.getElementById("s").innerText = s.s;
            let h = ""; s.c.forEach(x => {
                let xpText = x.xp ? ` (+${x.xp} XP)` : "";
                h += `<button onclick="step('${x.n}')">${x.t}${xpText}</button>`;
            });
            document.getElementById("c").innerHTML = h;
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
