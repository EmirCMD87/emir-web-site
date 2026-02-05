from flask import Flask
import os

app = Flask(__name__)

# --- ANA SAYFA (MAĞAZA VE XP SİSTEMİ) ---
ana_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cano Studio | Premium</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;500&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; touch-action: manipulation; }
        body { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #050505 100%); z-index: -1; }
        
        .xp-container { position: fixed; top: 20px; right: 20px; background: rgba(255,69,0,0.1); border: 1px solid #ff4500; padding: 10px 20px; border-radius: 50px; z-index: 100; display: flex; align-items: center; gap: 10px; }
        .xp-val { color: #ff4500; font-weight: bold; font-family: 'Syncopate'; }

        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 60px 20px; }
        h1 { font-family: 'Syncopate', sans-serif; font-size: clamp(1.5rem, 6vw, 4rem); letter-spacing: 10px; text-transform: uppercase; margin-bottom: 40px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; width: 100%; max-width: 1100px; margin-bottom: 50px; }
        .card { background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 4px; cursor: pointer; transition: 0.3s; text-decoration: none; }
        .card:hover { border-color: #ff4500; transform: translateY(-5px); }
        .card h2 { font-family: 'Syncopate'; font-size: 0.8rem; color: #fff; margin-bottom: 10px; }

        .store-section { width: 100%; max-width: 1000px; margin-top: 50px; border-top: 1px solid #111; padding-top: 50px; }
        .store-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 30px; }
        .store-item { background: #0a0a0a; border: 1px solid #222; padding: 20px; border-radius: 4px; text-align: center; }
        .store-item.owned { border-color: #00d4ff; opacity: 0.7; }
        .price { color: #ff4500; font-size: 0.9rem; margin: 10px 0; font-family: 'Syncopate'; }
        .buy-btn { background: #ff4500; border: none; padding: 10px 20px; color: #fff; cursor: pointer; border-radius: 2px; width: 100%; }
        .buy-btn:disabled { background: #333; cursor: not-allowed; }
        footer { padding: 40px; font-size: 0.6rem; color: #222; text-align: center; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="xp-container">
        <span style="font-size: 0.7rem; letter-spacing: 1px;">XP:</span>
        <span class="xp-val" id="totalXP">0</span>
    </div>

    <section class="hero">
        <h1>CANO STUDIO</h1>
        <div class="grid">
            <a href="/neon-arcade" class="card"><h2>NEON ARCADE</h2><p>Hız ve Refleks</p></a>
            <a href="/strateji" class="card"><h2>STRATEJI</h2><p>30 Seviye Fetih</p></a>
            <a href="/horror" class="card"><h2>HORROR</h2><p>Karanlık Seçimler</p></a>
        </div>

        <div class="store-section">
            <h2 style="font-family:'Syncopate'; letter-spacing:5px;">MAĞAZA</h2>
            <div class="store-grid">
                <div class="store-item" id="item1">
                    <h3>ALTIN KARE</h3>
                    <div class="price">500 XP</div>
                    <button class="buy-btn" onclick="buyItem('item1', 500)">SATIN AL</button>
                </div>
                <div class="store-item" id="item2">
                    <h3>GALAXY MOD</h3>
                    <div class="price">1000 XP</div>
                    <button class="buy-btn" onclick="buyItem('item2', 1000)">SATIN AL</button>
                </div>
            </div>
        </div>
        <footer>© 2026 DESIGNED BY CANO</footer>
    </section>

    <script>
        let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
        let ownedItems = JSON.parse(localStorage.getItem('cano_items')) || [];
        function updateUI() {
            document.getElementById('totalXP').innerText = xp;
            ownedItems.forEach(id => {
                const el = document.getElementById(id);
                if(el) { el.classList.add('owned'); el.querySelector('button').innerText = "ALINDI"; el.querySelector('button').disabled = true; }
            });
        }
        function buyItem(id, price) {
            if(xp >= price) { xp -= price; ownedItems.push(id); localStorage.setItem('cano_xp', xp); localStorage.setItem('cano_items', JSON.stringify(ownedItems)); updateUI(); }
        }
        updateUI();
    </script>
</body>
</html>
"""

# --- NEON ARCADE ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: manipulation; }
        body { background: #000; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: sans-serif; }
        canvas { border: 2px solid #ff4500; max-width: 90vw; background: #050505; }
        .back { position: fixed; bottom: 20px; color: #444; text-decoration: none; }
    </style>
</head>
<body>
    <div style="position:fixed; top:20px; color:#ff4500; font-size:1.5rem;" id="sc">0</div>
    <canvas id="gc" width="400" height="500"></canvas>
    <a href="/" class="back">← PORTALA DÖN</a>
    <script>
        const canvas = document.getElementById("gc"); const ctx = canvas.getContext("2d");
        let bird = { y: 250, v: 0, g: 0.5, jump: -8 };
        let pipes = []; let frames = 0; let score = 0;
        function draw() {
            ctx.fillStyle = "#050505"; ctx.fillRect(0,0,400,500);
            let items = JSON.parse(localStorage.getItem('cano_items')) || [];
            ctx.fillStyle = items.includes('item1') ? "#FFD700" : "#fff";
            bird.v += bird.g; bird.y += bird.v;
            ctx.fillRect(60, bird.y, 25, 25);
            if(frames%100===0) pipes.push({x:400, h:Math.random()*250+50, gap:160});
            for(let i=pipes.length-1; i>=0; i--) {
                pipes[i].x -= 3; ctx.fillStyle = "#111"; ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.fillRect(pipes[i].x, pipes[i].h+160, 50, 500);
                if(60+25 > pipes[i].x && 60 < pipes[i].x+50 && (bird.y < pipes[i].h || bird.y+25 > pipes[i].h+160)) reset();
                if(pipes[i].x === 58) { score++; document.getElementById("sc").innerText = score; addXP(10); }
                if(pipes[i].x < -50) pipes.splice(i,1);
            }
            if(bird.y > 500 || bird.y < 0) reset();
            frames++; requestAnimationFrame(draw);
        }
        function addXP(amt) { let xp = parseInt(localStorage.getItem('cano_xp')) || 0; localStorage.setItem('cano_xp', xp + amt); }
        function reset() { bird.y=250; bird.v=0; pipes=[]; score=0; document.getElementById("sc").innerText="0"; }
        const act = (e) => { bird.v = bird.jump; e.preventDefault(); };
        canvas.addEventListener("touchstart", act); canvas.addEventListener("mousedown", act);
        draw();
    </script>
</body>
</html>
"""

# --- STRATEJI (30 LEVEL + XP) ---
strateji_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: manipulation; }
        body { background: #050505; color: #fff; margin: 0; overflow: hidden; font-family: sans-serif; }
        .back { position: fixed; bottom: 20px; left: 20px; color: #444; text-decoration: none; font-size: 0.7rem; z-index: 10; }
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
        class Planet {
            constructor(x,y,s,o,c) { this.x=x; this.y=y; this.s=s; this.owner=o; this.count=c; this.t=0; }
            draw() {
                ctx.beginPath(); ctx.arc(this.x,this.y,this.s,0,Math.PI*2);
                ctx.fillStyle = this.owner===1 ? "#00d4ff" : (this.owner===2 ? "#ff4500" : "#222");
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
        function addXP(amt) { let xp = parseInt(localStorage.getItem('cano_xp')) || 0; localStorage.setItem('cano_xp', xp + amt); }
        function handle(x,y) {
            let p = planets.find(p => Math.sqrt((p.x-x)**2+(p.y-y)**2) < p.s);
            if(p) {
                if(p.owner===1) selected=p;
                else if(selected) {
                    fleets.push({x:selected.x, y:selected.y, target:p, owner:1, amount:Math.floor(selected.count/2)});
                    selected.count/=2; selected=null;
                }
            } else selected=null;
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
                } else { f.x+=dx/dist*4; f.y+=dy/dist*4; ctx.fillStyle="#00d4ff"; ctx.fillRect(f.x,f.y,4,4); }
            });
            planets.forEach(p => { p.update(); p.draw(); });
            if(!planets.some(p => p.owner === 2)) { level++; init(); addXP(200); }
            requestAnimationFrame(loop);
        }
        init(); loop();
    </script>
</body>
</html>
"""

# --- HORROR (GELİŞMİŞ HİKAYE + XP) ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { background: #000; color: #800; font-family: serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; padding: 20px; }
        .game-box { max-width: 500px; text-align: center; border: 1px solid #300; padding: 30px; background: #050000; }
        .text { color: #aaa; margin: 25px 0; font-style: italic; min-height: 80px; }
        .choices { display: flex; flex-direction: column; gap: 10px; }
        button { background: #1a0000; border: 1px solid #500; color: #888; padding: 12px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #500; color: #fff; }
    </style>
</head>
<body>
    <div class="game-box">
        <h2 id="t">KARANLIK YOL</h2>
        <p class="text" id="s">Arabanın motoru sustu. Ormanın içinden bir çığlık duydun. Ne yapacaksın?</p>
        <div class="choices" id="c">
            <button onclick="step(1)">Sesin Geldiği Yere Git</button>
            <button onclick="step(2)">Arabaya Kilitle Kendini</button>
        </div>
    </div>
    <script>
        function addXP(amt) { let xp = parseInt(localStorage.getItem('cano_xp')) || 0; localStorage.setItem('cano_xp', xp + amt); }
        const data = {
            1: { t: "ORMAN", s: "Çalıların arasında parlayan gözler gördün. Bir kurt sürüsü!", c: [{t:"Savaş", n:3}, {t:"Kaç", n:4}] },
            2: { t: "ARABA", s: "Camlar aniden buğulandı. Dışarıdan bir el izi belirdi. İçeride yalnız değilsin...", c: [{t:"Kapıyı Aç ve Fırla", n:1}, {t:"Dua Et", n:5}] },
            3: { t: "SON", s: "Kurtlarla başa çıkamadın. Karanlık seni yuttu. (+20 XP)", c: [{t:"Yeniden", n:"r"}] },
            4: { t: "KAÇIŞ", s: "Eski bir mahzen kapağı buldun. İçeri giriyor musun?", c: [{t:"Gir", n:6}, {t:"Dışarıda Kal", n:3}] },
            5: { t: "SON", s: "Görünmez bir el boğazına sarıldı... (+30 XP)", c: [{t:"Yeniden", n:"r"}] },
            6: { t: "MAHZEN", s: "Aşağıda bir ayin yapılıyor. Seni fark ettiler!", c: [{t:"Ayine Katıl", n:7}, {t:"Saldır", n:8}] },
            7: { t: "ZAFER", s: "Artık onlardan birisin. Galaksinin karanlık gücünü kazandın! (+100 XP)", c: [{t:"Başa Dön", n:"r"}] },
            8: { t: "ÖLÜM", s: "Fedai olarak kurban edildin... (+40 XP)", c: [{t:"Yeniden", n:"r"}] }
        };
        function step(n) {
            if(n==="r") { location.reload(); return; }
            addXP(10);
            const s = data[n];
            if(s.t === "SON" || s.t === "ZAFER" || s.t === "ÖLÜM") {
                 if(s.t === "ZAFER") addXP(100); else if(s.t === "ÖLÜM") addXP(40); else addXP(20);
            }
            document.getElementById("t").innerText = s.t;
            document.getElementById("s").innerText = s.s;
            let h = ""; s.c.forEach(x => h += `<button onclick="step('${x.n}')">${x.t}</button>`);
            document.getElementById("c").innerHTML = h;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return ana_sayfa_html
@app.route('/neon-arcade')
def arcade(): return arcade_html
@app.route('/strateji')
def strateji(): return strateji_html
@app.route('/horror')
def horror(): return horror_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
