from flask import Flask
import os

app = Flask(__name__)

# --- GENEL TEMA VE FOOTER ---
footer_html = """
<footer style="background: #080808; padding: 30px; border-top: 1px solid #1a1a1a; text-align: center; margin-top: auto;">
    <p style="color: #444; font-size: 0.8rem; letter-spacing: 2px;">© 2026 CANO STUDIO - CREATIVE LABS</p>
</footer>
"""

# --- 1. ANA PORTAL SAYFASI ---
ana_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Studio | Dashboard</title>
    <style>
        * {{ box-sizing: border-box; transition: 0.3s ease; }}
        body {{ background: #020202; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .header {{ padding: 60px 20px; text-align: center; }}
        h1 {{ font-size: 3rem; letter-spacing: 10px; margin: 0; color: #fff; font-weight: 200; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 40px; max-width: 1200px; margin: 0 auto; width:100%; }}
        .game-card {{ background: #0a0a0a; border: 1px solid #1a1a1a; padding: 30px; border-radius: 4px; cursor: pointer; }}
        .game-card:hover {{ border-color: #fff; background: #111; transform: translateY(-5px); }}
        .status {{ font-size: 9px; letter-spacing: 2px; border: 1px solid; display: inline-block; padding: 2px 8px; margin-bottom: 15px; }}
        .arcade {{ color: #00d4ff; border-color: #00d4ff; }}
        .strategy {{ color: #00ff88; border-color: #00ff88; }}
        .horror {{ color: #ff4500; border-color: #ff4500; }}
        .description {{ color: #555; font-size: 0.85rem; line-height: 1.5; }}
    </style>
</head>
<body>
    <div class="header"><h1>CANO STUDIO</h1></div>
    <div class="container">
        <div class="game-card" onclick="window.location.href='/neon-arcade'">
            <div class="status arcade">ARCADE</div>
            <h2>NEON ARCADE</h2>
            <p class="description">Ultra hızlı refleks testi. Çarpma anında anlık resetleme özelliği eklendi.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/void-command'">
            <div class="status strategy">STRATEGY</div>
            <h2>VOID COMMAND</h2>
            <p class="description">Level bazlı genişleme. Her bölümde daha agresif yapay zeka ve daha çok gezegen.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/the-basement'">
            <div class="status horror">HORROR</div>
            <h2 style="color:#ff4500">THE BASEMENT</h2>
            <p class="description">Karanlık koridorlarda hayatta kal. Sadece fenerin ve şansın var.</p>
        </div>
    </div>
    {footer_html}
</body>
</html>
"""

# --- 2. NEON ARCADE (ANLIK RESETLEME) ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Neon Arcade | Instant Reset</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        canvas { border: 2px solid #00d4ff; box-shadow: 0 0 20px #00d4ff33; cursor: pointer; }
        .score { position: absolute; top: 20px; font-size: 3rem; font-weight: bold; color: #00d4ff; pointer-events: none; opacity: 0.5; }
    </style>
</head>
<body>
    <div class="score" id="s">0</div>
    <canvas id="c" width="400" height="500"></canvas>
    <script>
        const canvas = document.getElementById("c"), ctx = canvas.getContext("2d");
        let bird, pipes, frames, score;

        function reset() {
            bird = {y: 250, v: 0, g: 0.5, j: -8};
            pipes = []; frames = 0; score = 0;
            document.getElementById("s").innerText = "0";
        }

        function draw() {
            ctx.fillStyle = "#000"; ctx.fillRect(0,0,400,500);
            bird.v += bird.g; bird.y += bird.v;
            ctx.fillStyle = "#00d4ff"; ctx.fillRect(50, bird.y, 30, 30);

            if(frames % 100 === 0) pipes.push({x: 400, h: Math.random()*250+50, s: false});
            for(let i=pipes.length-1; i>=0; i--) {
                pipes[i].x -= 4;
                ctx.fillStyle = "#111"; ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.fillRect(pipes[i].x, pipes[i].h+150, 50, 500);
                if(50+30 > pipes[i].x && 50 < pipes[i].x+50 && (bird.y < pipes[i].h || bird.y+30 > pipes[i].h+150)) reset();
                if(pipes[i].x < 50 && !pipes[i].s) { score++; pipes[i].s = true; document.getElementById("s").innerText = score; }
                if(pipes[i].x < -50) pipes.splice(i,1);
            }
            if(bird.y > 500 || bird.y < 0) reset();
            frames++; requestAnimationFrame(draw);
        }
        window.onclick = () => bird.v = bird.j;
        reset(); draw();
    </script>
</body>
</html>
"""

# --- 3. VOID COMMAND (LEVEL SİSTEMLİ STRATEJİ) ---
void_command_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Void Command | Levels</title>
    <style>
        body { background: #050505; color: #00ff88; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        .ui { position: fixed; width: 100%; padding: 20px; display: flex; justify-content: space-between; background: rgba(0,0,0,0.8); z-index: 10; }
        #game { display: block; background: #000; }
    </style>
</head>
<body>
    <div class="ui">
        <span id="lvl">LEVEL: 1</span>
        <span id="info">TÜM GEZEGENLERİ ELE GEÇİR!</span>
    </div>
    <canvas id="game"></canvas>
    <script>
        const canvas = document.getElementById('game');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        
        let level = 1, planets = [], selected = null;

        class Planet {
            constructor(x, y, r, owner) {
                this.x = x; this.y = y; this.r = r; this.owner = owner;
                this.energy = owner === 'neutral' ? 5 : 20;
            }
            draw() {
                ctx.beginPath(); ctx.arc(this.x, this.y, this.r, 0, Math.PI*2);
                ctx.strokeStyle = this.owner === 'player' ? '#00ff88' : (this.owner === 'enemy' ? '#ff4500' : '#333');
                ctx.lineWidth = selected === this ? 5 : 2; ctx.stroke();
                ctx.fillStyle = ctx.strokeStyle; ctx.textAlign = "center";
                ctx.fillText(Math.floor(this.energy), this.x, this.y+5);
            }
        }

        function initLevel() {
            planets = [new Planet(100, canvas.height/2, 40, 'player')];
            // Level arttıkça düşman sayısı artar
            for(let i=0; i < level; i++) {
                planets.push(new Planet(canvas.width - 100, (canvas.height/(level+1))*(i+1), 35, 'enemy'));
            }
            for(let i=0; i<5; i++) {
                planets.push(new Planet(300+Math.random()*(canvas.width-600), Math.random()*canvas.height, 25, 'neutral'));
            }
        }

        canvas.onclick = (e) => {
            let p = planets.find(p => Math.hypot(p.x-e.clientX, p.y-e.clientY) < p.r);
            if(p) {
                if(p.owner === 'player') selected = p;
                else if(selected) {
                    let f = selected.energy/2; selected.energy -= f; p.energy -= f;
                    if(p.energy < 0) { p.owner = 'player'; p.energy = Math.abs(p.energy); }
                    selected = null;
                }
            }
            if(!planets.some(p => p.owner === 'enemy')) { level++; document.getElementById('lvl').innerText = "LEVEL: " + level; initLevel(); }
        };

        function loop() {
            ctx.fillStyle = "black"; ctx.fillRect(0,0,canvas.width,canvas.height);
            planets.forEach(p => { if(p.owner !== 'neutral') p.energy += 0.01 * level; p.draw(); });
            requestAnimationFrame(loop);
        }
        initLevel(); loop();
    </script>
</body>
</html>
"""

# --- 4. THE BASEMENT (KORKU OYUNU) ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>The Basement | Horror</title>
    <style>
        body { background: #000; color: #fff; margin: 0; overflow: hidden; font-family: serif; }
        #flashlight { position: fixed; width: 100vw; height: 100vh; background: radial-gradient(circle at center, transparent 10%, rgba(0,0,0,0.98) 30%); pointer-events: none; }
        .message { position: fixed; bottom: 50px; width: 100%; text-align: center; color: #300; font-size: 1.2rem; }
    </style>
</head>
<body>
    <div id="flashlight"></div>
    <div class="message" id="m">BURADAN ÇIKMALIYIM...</div>
    <canvas id="h"></canvas>
    <script>
        const c = document.getElementById("h"), ctx = c.getContext("2d");
        c.width = window.innerWidth; c.height = window.innerHeight;
        let ghost = {x: -100, y: -100}, frame = 0;

        window.onmousemove = (e) => {
            document.getElementById("flashlight").style.background = `radial-gradient(circle at ${e.clientX}px ${e.clientY}px, transparent 0%, rgba(0,0,0,0.99) 25%)`;
            if(Math.hypot(ghost.x-e.clientX, ghost.y-e.clientY) < 50) {
                document.getElementById("m").innerText = "O BURADA!";
                document.getElementById("m").style.color = "red";
            }
        };

        function spawnGhost() {
            ghost.x = Math.random() * c.width; ghost.y = Math.random() * c.height;
        }

        function draw() {
            ctx.fillStyle = "#050505"; ctx.fillRect(0,0,c.width,c.height);
            // Hayalet sadece çok yakındayken titrek bir şekilde görünür
            ctx.fillStyle = "rgba(255,255,255,0.02)";
            ctx.beginPath(); ctx.arc(ghost.x, ghost.y, 20, 0, Math.PI*2); ctx.fill();
            if(frame % 200 === 0) spawnGhost();
            frame++; requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return ana_sayfa_html

@app.route('/neon-arcade')
def arcade(): return arcade_html

@app.route('/void-command')
def strategy(): return void_command_html

@app.route('/the-basement')
def horror(): return horror_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
