from flask import Flask
import os

app = Flask(__name__)

# --- 1. ANA SAYFA (İHTİŞAMLI PORTAL + İLETİŞİM) ---
ana_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cano Game Studio | Official Portal</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;500&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; touch-action: manipulation; }
        body { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #050505 100%); z-index: -1; }
        
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 80px 20px; }
        h1 { font-family: 'Syncopate', sans-serif; font-size: clamp(2rem, 8vw, 4.5rem); font-weight: 700; letter-spacing: 12px; text-transform: uppercase; background: linear-gradient(to bottom, #fff 30%, #444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
        .line { width: 80px; height: 2px; background: #ff4500; margin: 20px 0; }
        .subtitle { font-size: 0.9rem; color: #666; letter-spacing: 4px; margin-bottom: 60px; text-transform: uppercase; }

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; width: 100%; max-width: 1100px; padding: 20px; margin-bottom: 80px; }
        .card { background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.05); padding: 45px 25px; border-radius: 4px; cursor: pointer; transition: 0.4s ease; text-decoration: none; }
        .card:hover { background: rgba(255, 255, 255, 0.03); border-color: #ff4500; transform: translateY(-10px); }
        .card h2 { font-family: 'Syncopate', sans-serif; font-size: 1rem; letter-spacing: 3px; margin-bottom: 12px; color: #fff; }
        .card p { color: #444; font-size: 0.8rem; line-height: 1.5; }

        .contact-section { width: 100%; max-width: 600px; padding: 80px 20px; margin: 0 auto; text-align: center; }
        .contact-section h2 { font-family: 'Syncopate', sans-serif; letter-spacing: 5px; font-size: 1.2rem; margin-bottom: 30px; color: #fff; }
        .contact-form { display: flex; flex-direction: column; gap: 12px; text-align: left; }
        input, textarea { background: #0a0a0a; border: 1px solid #222; padding: 14px; color: #fff; border-radius: 4px; outline: none; transition: 0.3s; }
        input:focus, textarea:focus { border-color: #ff4500; }
        .btn-send { background: #ff4500; color: white; border: none; padding: 14px; border-radius: 4px; font-weight: bold; cursor: pointer; letter-spacing: 2px; transition: 0.3s; }
        .btn-send:hover { background: #ff6600; box-shadow: 0 0 15px rgba(255,69,0,0.3); }

        footer { padding: 50px; font-size: 0.6rem; letter-spacing: 3px; color: #222; text-align: center; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <section class="hero">
        <h1>CANO STUDIO</h1>
        <div class="line"></div>
        <p class="subtitle">Premium Game Experience</p>
        <div class="grid">
            <a href="/neon-arcade" class="card"><h2>NEON ARCADE</h2><p>Reflekslerini test et. Uçan kare ile engelleri aş.</p></a>
            <a href="/strateji" class="card"><h2>STRATEJI</h2><p>Gezegenleri fethet. Galakside hakimiyet kur.</p></a>
            <a href="/horror" class="card"><h2>HORROR</h2><p>Karanlığın içindeki gizemi çöz. Yakında.</p></a>
        </div>
        <div class="contact-section">
            <h2>İLETİŞİM</h2>
            <form class="contact-form">
                <input type="text" placeholder="ADINIZ">
                <input type="email" placeholder="E-POSTA">
                <textarea rows="4" placeholder="MESAJINIZ"></textarea>
                <button type="submit" class="btn-send">GÖNDER</button>
            </form>
        </div>
        <footer>© 2026 DESIGNED BY CANO</footer>
    </section>
</body>
</html>
"""

# --- 2. NEON ARCADE OYUNU ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Neon Arcade</title>
    <style>
        * { touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
        body { background: #000; color: #fff; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; font-family: sans-serif; }
        canvas { border: 2px solid #ff4500; max-width: 95vw; background: #050505; border-radius: 4px; }
        .back { position: fixed; bottom: 20px; color: #444; text-decoration: none; font-size: 0.8rem; letter-spacing: 2px; }
        .score { position: fixed; top: 30px; font-size: 2.5rem; color: #ff4500; font-weight: bold; pointer-events: none; }
    </style>
</head>
<body>
    <div class="score" id="s">0</div>
    <canvas id="gc" width="400" height="500"></canvas>
    <a href="/" class="back">← PORTALA DÖN</a>
    <script>
        const canvas = document.getElementById("gc"); const ctx = canvas.getContext("2d");
        let bird = { y: 250, v: 0, g: 0.5, jump: -8 };
        let pipes = []; let frames = 0; let score = 0;
        function draw() {
            ctx.fillStyle = "#050505"; ctx.fillRect(0,0,400,500);
            bird.v += bird.g; bird.y += bird.v;
            ctx.fillStyle = "#fff"; ctx.fillRect(60, bird.y, 25, 25);
            if(frames%100===0) pipes.push({x:400, h:Math.random()*250+50, gap:160});
            for(let i=pipes.length-1; i>=0; i--) {
                pipes[i].x -= 3;
                ctx.fillStyle = "#111"; ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.fillRect(pipes[i].x, pipes[i].h+pipes[i].gap, 50, 500);
                if(60+25 > pipes[i].x && 60 < pipes[i].x+50 && (bird.y < pipes[i].h || bird.y+25 > pipes[i].h+pipes[i].gap)) reset();
                if(pipes[i].x === 58) { score++; document.getElementById("s").innerText = score; }
                if(pipes[i].x < -50) pipes.splice(i,1);
            }
            if(bird.y > 500 || bird.y < 0) reset();
            frames++; requestAnimationFrame(draw);
        }
        function reset() { bird.y=250; bird.v=0; pipes=[]; score=0; document.getElementById("s").innerText="0"; }
        const act = (e) => { e.preventDefault(); bird.v = bird.jump; };
        canvas.addEventListener("touchstart", act); canvas.addEventListener("mousedown", act);
        window.addEventListener("keydown", (e) => { if(e.code==="Space") bird.v = bird.jump; });
        draw();
    </script>
</body>
</html>
"""

# --- 3. STRATEJİ OYUNU ---
strateji_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Galaksi Fethi</title>
    <style>
        * { touch-action: manipulation; }
        body { background: #050505; color: #fff; margin: 0; overflow: hidden; font-family: sans-serif; }
        .back { position: fixed; bottom: 20px; left: 20px; color: #444; text-decoration: none; font-size: 0.7rem; z-index: 10; }
        .info { position: fixed; top: 15px; width: 100%; text-align: center; pointer-events: none; color: #ff4500; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="info">GALAXY CONQUEST</div>
    <canvas id="sc"></canvas>
    <a href="/" class="back">← PORTALA DÖN</a>
    <script>
        const canvas = document.getElementById("sc"); const ctx = canvas.getContext("2d");
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let planets = []; let fleets = []; let selected = null;
        class Planet {
            constructor(x,y,s,o,c) { this.x=x; this.y=y; this.s=s; this.owner=o; this.count=c; this.t=0; }
            draw() {
                ctx.beginPath(); ctx.arc(this.x,this.y,this.s,0,Math.PI*2);
                ctx.fillStyle = this.owner===1 ? "#00d4ff" : (this.owner===2 ? "#ff4500" : "#222");
                ctx.fill();
                if(selected === this) { ctx.strokeStyle="#fff"; ctx.lineWidth=3; ctx.stroke(); }
                ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.font="bold 14px Arial"; ctx.fillText(Math.floor(this.count), this.x, this.y+5);
            }
            update() { if(this.owner!==0) { this.t++; if(this.t>60) {this.count+=0.5; this.t=0;} } }
        }
        function init() {
            planets.push(new Planet(80, canvas.height/2, 35, 1, 20));
            planets.push(new Planet(canvas.width-80, canvas.height/2, 35, 2, 25));
            for(let i=0; i<5; i++) planets.push(new Planet(Math.random()*(canvas.width-160)+80, Math.random()*(canvas.height-160)+80, 25, 0, 10));
        }
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
                    else { f.target.count-=f.amount; if(f.target.count<0) {f.target.owner=f.owner; f.target.count=Math.abs(f.target.count);} }
                    fleets.splice(i,1);
                } else { f.x+=dx/dist*4; f.y+=dy/dist*4; ctx.fillStyle=f.owner===1?"#00d4ff":"#ff4500"; ctx.fillRect(f.x,f.y,4,4); }
            });
            planets.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(loop);
        }
        init(); loop();
    </script>
</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def home(): return ana_sayfa_html

@app.route('/neon-arcade')
def arcade(): return arcade_html

@app.route('/strateji')
def strateji(): return strateji_html

@app.route('/horror')
def horror(): return "<body style='background:#000;color:#333;display:flex;align-items:center;justify-content:center;height:100vh;font-family:Syncopate;letter-spacing:10px;'><h1>HORROR COMING SOON</h1></body>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
