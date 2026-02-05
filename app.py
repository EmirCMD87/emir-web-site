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
        .xp-container { position: fixed; top: 20px; right: 20px; background: rgba(255,69,0,0.1); border: 1px solid #ff4500; padding: 10px 20px; border-radius: 50px; z-index: 100; }
        .xp-val { color: #ff4500; font-weight: bold; font-family: 'Syncopate'; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 60px 20px; }
        h1 { font-family: 'Syncopate', sans-serif; font-size: clamp(1.5rem, 6vw, 4rem); letter-spacing: 10px; text-transform: uppercase; margin-bottom: 40px; color: #fff; text-shadow: 0 0 20px rgba(255,255,255,0.2); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; width: 100%; max-width: 1100px; }
        .card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 40px 30px; border-radius: 4px; cursor: pointer; transition: 0.3s; text-decoration: none; }
        .card:hover { border-color: #ff4500; transform: translateY(-5px); background: rgba(255,69,0,0.05); }
        .card h2 { font-family: 'Syncopate'; font-size: 0.8rem; color: #fff; margin-bottom: 10px; letter-spacing: 3px; }
        .store-card { border-color: #00d4ff !important; }
        footer { margin-top: 50px; font-size: 0.6rem; color: #333; letter-spacing: 3px; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="xp-container"><span class="xp-val" id="totalXP">0</span> <small style="color:#ff4500">XP</small></div>
    <section class="hero">
        <h1>CANO STUDIO</h1>
        <div class="grid">
            <a href="/neon-arcade" class="card"><h2>NEON ARCADE</h2><p>Gece Manzaralı & Hız</p></a>
            <a href="/strateji" class="card"><h2>STRATEJI</h2><p>Gezegen Fethetme</p></a>
            <a href="/horror" class="card"><h2>HORROR</h2><p>Kabusun Başlangıcı</p></a>
            <a href="/store" class="card store-card"><h2>MAĞAZA</h2><p style="color:#00d4ff">Market & Skinler</p></a>
        </div>
        <footer>© 2026 PREMIUM GAMING</footer>
    </section>
    <script>document.getElementById('totalXP').innerText = localStorage.getItem('cano_xp') || 0;</script>
</body>
</html>
"""

# --- 2. MAĞAZA ---
store_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Store</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400&display=swap');
        body { background: #050505; color: #fff; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; text-align: center; }
        .xp-display { font-family: 'Syncopate'; color: #ff4500; font-size: 1.5rem; margin: 20px; }
        .store-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; max-width: 1000px; margin: 0 auto; }
        .item { background: #0a0a0a; border: 1px solid #222; padding: 20px; border-radius: 8px; }
        .item.owned { border-color: #00ff00; opacity: 0.7; }
        button { background: #ff4500; color: #fff; border: none; padding: 10px; width: 100%; cursor: pointer; font-weight: bold; margin-top:10px; }
        button:disabled { background: #222; }
    </style>
</head>
<body>
    <h1 style="font-family:'Syncopate';">STORE</h1>
    <div class="xp-display">BAKİYE: <span id="currentXP">0</span></div>
    <div class="store-grid" id="grid"></div>
    <a href="/" style="color:#444; text-decoration:none; display:block; margin-top:30px;">← GERİ DÖN</a>
    <script>
        let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
        let owned = JSON.parse(localStorage.getItem('cano_items')) || [];
        const items = [
            {id: 'item1', name: 'ALTIN KARE', p: 500, d: 'Arcade skin.'},
            {id: 'item2', name: 'NEON MAVİ', p: 1000, d: 'Strateji skin.'},
            {id: 'item3', name: 'HIZ BOTU', p: 2000, d: 'Arcade çarpanı x2.'},
            {id: 'item4', name: 'HAYALET MOD', p: 5000, d: 'Horror gizli son açar.'}
        ];
        function render() {
            document.getElementById('currentXP').innerText = xp;
            document.getElementById('grid').innerHTML = items.map(i => `
                <div class="item ${owned.includes(i.id)?'owned':''}">
                    <h3>${i.name}</h3><p style="font-size:0.7rem; color:#666">${i.d}</p>
                    <div style="color:#ff4500">${i.p} XP</div>
                    <button onclick="buy('${i.id}', ${i.p})" ${owned.includes(i.id)?'disabled':''}>
                        ${owned.includes(i.id)?'ALINDI':'SATIN AL'}
                    </button>
                </div>
            `).join('');
        }
        function buy(id, price) {
            if(xp >= price) { 
                xp -= price; owned.push(id); 
                localStorage.setItem('cano_xp', xp); 
                localStorage.setItem('cano_items', JSON.stringify(owned)); 
                render(); 
            }
        }
        render();
    </script>
</body>
</html>
"""

# --- 3. NEON ARCADE (YILDIZLI GECE GÖKYÜZÜ) ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: manipulation; }
        body { background: #000; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        canvas { border: 2px solid #333; background: #050505; max-width: 95vw; }
    </style>
</head>
<body>
    <div style="position:fixed; top:20px; color:#ff4500; font-size:2rem; font-family:sans-serif; z-index:10;" id="sc">0</div>
    <canvas id="gc" width="400" height="500"></canvas>
    <a href="/" style="position:fixed; bottom:20px; color:#444; text-decoration:none;">← ÇIKIŞ</a>
    <script>
        const canvas = document.getElementById("gc"); const ctx = canvas.getContext("2d");
        let bird = { y: 250, v: 0, g: 0.5, jump: -8 };
        let pipes = []; let frames = 0; let score = 0; let isGameOver = false; let gameStarted = false;
        
        const stars = Array.from({length: 60}, () => ({ x: Math.random()*400, y: Math.random()*500, s: Math.random()*1.5 }));

        function addXP(amt) { 
            let items = JSON.parse(localStorage.getItem('cano_items')) || [];
            let mult = items.includes('item3') ? 2 : 1;
            let xp = parseInt(localStorage.getItem('cano_xp')) || 0; 
            localStorage.setItem('cano_xp', xp + (amt * mult)); 
        }

        function drawBackground() {
            let grad = ctx.createLinearGradient(0, 0, 0, 500);
            grad.addColorStop(0, "#000018"); grad.addColorStop(1, "#050505");
            ctx.fillStyle = grad; ctx.fillRect(0,0,400,500);
            ctx.fillStyle = "white";
            stars.forEach(s => { ctx.beginPath(); ctx.arc(s.x, s.y, s.s, 0, Math.PI*2); ctx.fill(); });
        }

        function draw() {
            drawBackground();
            let items = JSON.parse(localStorage.getItem('cano_items')) || [];
            ctx.fillStyle = items.includes('item1') ? "#FFD700" : "#fff";

            if(!gameStarted || isGameOver) {
                ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(0,0,400,500);
                ctx.fillStyle = "#ff4500"; ctx.textAlign = "center";
                ctx.fillText(isGameOver ? "GAME OVER" : "DOKUN VE BAŞLA", 200, 250);
                if(!isGameOver) requestAnimationFrame(draw);
                return;
            }

            bird.v += bird.g; bird.y += bird.v; ctx.fillRect(60, bird.y, 25, 25);
            if(frames%90===0) pipes.push({x:400, h:Math.random()*250+50});
            for(let i=pipes.length-1; i>=0; i--) {
                pipes[i].x -= 3.5;
                ctx.strokeStyle = "#ff4500"; ctx.strokeRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.strokeRect(pipes[i].x, pipes[i].h+150, 50, 500);
                if(60+25 > pipes[i].x && 60 < pipes[i].x+50 && (bird.y < pipes[i].h || bird.y+25 > pipes[i].h+150)) isGameOver = true;
                if(pipes[i].x < 60 && !pipes[i].passed) { score++; pipes[i].passed=true; document.getElementById("sc").innerText = score; addXP(10); }
                if(pipes[i].x < -50) pipes.splice(i,1);
            }
            if(bird.y > 500 || bird.y < 0) isGameOver = true;
            frames++; requestAnimationFrame(draw);
        }

        const act = () => { if(isGameOver) location.reload(); if(!gameStarted) gameStarted=true; bird.v = bird.jump; };
        canvas.addEventListener("mousedown", act); canvas.addEventListener("touchstart", (e)=>{e.preventDefault(); act();});
        draw();
    </script>
</body>
</html>
"""

# --- 4. STRATEJI (GRADYANLI GEZEGENLER) ---
strateji_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: manipulation; }
        body { background: #050505; color: #fff; margin: 0; overflow: hidden; font-family: sans-serif; }
    </style>
</head>
<body>
    <div style="position:fixed; top:15px; width:100%; text-align:center; color:#ff4500; font-weight:bold;">STRATEJİ</div>
    <canvas id="sc"></canvas>
    <a href="/" style="position:fixed; bottom:20px; left:20px; color:#444; text-decoration:none;">← GERİ</a>
    <script>
        const canvas = document.getElementById("sc"); const ctx = canvas.getContext("2d");
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let planets = []; let fleets = []; let selected = null;

        class Planet {
            constructor(x,y,s,o,c) { this.x=x; this.y=y; this.s=s; this.owner=o; this.count=c; this.t=0; }
            draw() {
                // Atmosfer
                ctx.beginPath(); ctx.arc(this.x, this.y, this.s + 6, 0, Math.PI*2);
                ctx.fillStyle = this.owner===1 ? "rgba(0,212,255,0.08)" : (this.owner===2 ? "rgba(255,69,0,0.08)" : "rgba(255,255,255,0.03)");
                ctx.fill();

                // Gövde
                let g = ctx.createRadialGradient(this.x-10, this.y-10, 2, this.x, this.y, this.s);
                if(this.owner===1) { g.addColorStop(0,"#55eaff"); g.addColorStop(1,"#0055aa"); }
                else if(this.owner===2) { g.addColorStop(0,"#ffaa88"); g.addColorStop(1,"#882200"); }
                else { g.addColorStop(0,"#666"); g.addColorStop(1,"#222"); }
                
                ctx.beginPath(); ctx.arc(this.x,this.y,this.s,0,Math.PI*2);
                ctx.fillStyle=g; ctx.fill();
                if(selected===this) { ctx.strokeStyle="#fff"; ctx.lineWidth=3; ctx.stroke(); }
                ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText(Math.floor(this.count), this.x, this.y+5);
            }
            update() { if(this.owner!==0) { this.t++; if(this.t>60) {this.count++; this.t=0;} } }
        }

        function init() {
            planets.push(new Planet(100, canvas.height/2, 40, 1, 20));
            planets.push(new Planet(canvas.width-100, canvas.height/2, 40, 2, 20));
            for(let i=0; i<4; i++) planets.push(new Planet(Math.random()*(canvas.width-200)+100, Math.random()*(canvas.height-200)+100, 25, 0, 10));
        }

        canvas.addEventListener("mousedown", (e) => {
            let p = planets.find(p => Math.sqrt((p.x-e.clientX)**2+(p.y-e.clientY)**2) < p.s);
            if(p) { if(p.owner===1) selected=p; else if(selected) { fleets.push({x:selected.x, y:selected.y, target:p, owner:1, amount:Math.floor(selected.count/2)}); selected.count/=2; selected=null; } }
        });

        function loop() {
            ctx.fillStyle="#050505"; ctx.fillRect(0,0,canvas.width,canvas.height);
            fleets.forEach((f,i) => {
                let dx=f.target.x-f.x, dy=f.target.y-f.y, dist=Math.sqrt(dx*dx+dy*dy);
                if(dist<5) {
                    if(f.target.owner===f.owner) f.target.count+=f.amount;
                    else { f.target.count-=f.amount; if(f.target.count<0) {f.target.owner=f.owner; f.target.count=Math.abs(f.target.count);} }
                    fleets.splice(i,1);
                } else { f.x+=dx/dist*4; f.y+=dy/dist*4; ctx.fillStyle="#00d4ff"; ctx.fillRect(f.x,f.y,3,3); }
            });
            planets.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(loop);
        }
        init(); loop();
    </script>
</body>
</html>
"""

# --- 5. HORROR (DEĞİŞMEDİ) ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { background: #000; color: #800; font-family: serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; text-align:center; }
        .game-box { max-width: 400px; border: 1px solid #300; padding: 30px; background: #050000; }
        button { background: #1a0000; border: 1px solid #500; color: #888; padding: 15px; cursor: pointer; width: 100%; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="game-box">
        <h2 id="t">KARANLIK YOL</h2>
        <p id="s">Yol ikiye ayrılıyor...</p>
        <div id="c">
            <button onclick="handle(1)">Hastaneye Gir</button>
            <button onclick="handle(2)">Mezarlığa Sap</button>
        </div>
        <a href="/" style="color:#444; display:block; margin-top:20px;">← KAÇ</a>
    </div>
    <script>
        function handle(n) {
            if(n===1) { document.getElementById("s").innerText="İçerisi çok soğuk..."; }
            if(n===2) { document.getElementById("s").innerText="Toprak canlanıyor!"; }
            document.getElementById("c").innerHTML = '<button onclick="location.reload()">TEKRAR DENE</button>';
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
