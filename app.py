from flask import Flask
import os

app = Flask(__name__)

# --- GENEL TEMA VE FOOTER ---
footer_html = """
<footer style="background: #080808; padding: 30px; border-top: 1px solid #1a1a1a; text-align: center; margin-top: auto;">
    <p style="color: #444; font-size: 0.8rem; letter-spacing: 2px;">© 2026 CANO STUDIO - GLOBAL SYSTEMS</p>
</footer>
"""

# --- 1. ANA PORTAL SAYFASI ---
ana_sayfa_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Studio | Game Library</title>
    <style>
        * {{ box-sizing: border-box; transition: 0.3s ease; }}
        body {{ background: #020202; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .header {{ padding: 80px 20px; text-align: center; }}
        h1 {{ font-size: 3.5rem; letter-spacing: 12px; margin: 0; color: #fff; font-weight: 300; text-transform: uppercase; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; padding: 40px; max-width: 1100px; margin: 0 auto; width:100%; }}
        .game-card {{ background: #0a0a0a; border: 1px solid #1a1a1a; padding: 40px; border-radius: 8px; cursor: pointer; position: relative; overflow: hidden; }}
        .game-card:hover {{ border-color: #00ff88; transform: translateY(-5px); background: #0f0f0f; }}
        .game-card h2 {{ margin: 10px 0; letter-spacing: 2px; }}
        .status {{ font-size: 10px; color: #00ff88; letter-spacing: 2px; border: 1px solid #00ff88; display: inline-block; padding: 2px 8px; border-radius: 4px; }}
        .description {{ color: #666; font-size: 0.9rem; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CANO STUDIO</h1>
    </div>
    <div class="container">
        <div class="game-card" onclick="window.location.href='/neon-arcade'">
            <div class="status">ARCADE</div>
            <h2>NEON ARCADE</h2>
            <p class="description">High-speed reflex challenge. Navigate through neon barriers and break records.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/void-command'">
            <div class="status">STRATEGY</div>
            <h2 style="color: #00ff88;">VOID COMMAND</h2>
            <p class="description">Deep space expansion. Capture planets, manage energy, and dominate the void.</p>
        </div>
    </div>
    {footer_html}
</body>
</html>
"""

# --- 2. NEON ARCADE OYUN SAYFASI ---
arcade_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Neon Arcade | Cano Studio</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        #gc { border: 4px solid #00d4ff; box-shadow: 0 0 20px #00d4ff66; border-radius: 10px; cursor: pointer; }
        .ui { position: absolute; top: 20px; text-align: center; pointer-events: none; }
        .back-btn { position: fixed; top: 20px; left: 20px; color: #444; text-decoration: none; border: 1px solid #222; padding: 5px 15px; border-radius: 5px; }
        .back-btn:hover { color: #fff; border-color: #fff; }
    </style>
</head>
<body>
    <a href="/" class="back-btn">← EXIT</a>
    <div class="ui">
        <h1 style="color:#00d4ff; margin:0; letter-spacing:5px;">NEON ARCADE</h1>
        <div id="scoreDisplay" style="font-size: 2rem;">0</div>
    </div>
    <canvas id="gc" width="400" height="500"></canvas>
    <script>
        const canvas = document.getElementById("gc");
        const ctx = canvas.getContext("2d");
        let bird = { y: 250, v: 0, gravity: 0.5, jump: -8 };
        let pipes = [];
        let score = 0;
        let frames = 0;

        function draw() {
            ctx.fillStyle = "#000"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            bird.v += bird.gravity; bird.y += bird.v;
            ctx.fillStyle = "#00d4ff"; ctx.shadowBlur = 15; ctx.shadowColor = "#00d4ff";
            ctx.fillRect(50, bird.y, 30, 30); ctx.shadowBlur = 0;

            if (frames % 90 === 0) {
                let h = Math.random() * (canvas.height - 200) + 50;
                pipes.push({ x: canvas.width, h: h, scored: false });
            }
            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= 3.5;
                ctx.fillStyle = "#111"; ctx.strokeStyle = "#00d4ff";
                ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.fillRect(pipes[i].x, pipes[i].h + 150, 50, canvas.height);
                ctx.strokeRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.strokeRect(pipes[i].x, pipes[i].h + 150, 50, canvas.height);

                if (50 > pipes[i].x + 50 && !pipes[i].scored) { score++; pipes[i].scored = true; document.getElementById("scoreDisplay").innerText = score; }
                if (50 + 25 > pipes[i].x && 50 < pipes[i].x + 50 && (bird.y < pipes[i].h || bird.y + 30 > pipes[i].h + 150)) location.reload();
                if (pipes[i].x < -50) pipes.splice(i, 1);
            }
            if (bird.y > canvas.height || bird.y < 0) location.reload();
            frames++; requestAnimationFrame(draw);
        }
        window.onclick = () => bird.v = bird.jump;
        window.onkeydown = (e) => { if(e.code === 'Space') bird.v = bird.jump; };
        draw();
    </script>
</body>
</html>
"""

# --- 3. VOID COMMAND STRATEJİ SAYFASI ---
void_command_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Void Command | Cano Studio</title>
    <style>
        body { background: #050505; color: #00ff88; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; user-select: none; }
        .nav { padding: 20px; background: rgba(0,0,0,0.9); border-bottom: 1px solid #111; display: flex; justify-content: space-between; position: fixed; width: 100%; z-index: 100; }
        .back-btn { color: #444; text-decoration: none; border: 1px solid #222; padding: 2px 10px; border-radius: 4px; }
        #game-canvas { display: block; background: radial-gradient(circle, #0a0a0a 0%, #000 100%); }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/" class="back-btn">← EXIT</a>
        <span id="status">COMMAND CENTER: ACTIVE</span>
        <span id="fleet-info">SELECT ORIGIN PLANET</span>
    </div>
    <canvas id="game-canvas"></canvas>
    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let planets = []; let selectedPlanet = null;

        class Planet {
            constructor(x, y, radius, owner) {
                this.x = x; this.y = y; this.radius = radius; this.owner = owner;
                this.energy = owner === 'neutral' ? 5 : 20;
                this.color = owner === 'player' ? '#00ff88' : (owner === 'enemy' ? '#ff4500' : '#333');
            }
            draw() {
                if (selectedPlanet === this) {
                    ctx.beginPath(); ctx.arc(this.x, this.y, this.radius + 10, 0, Math.PI * 2);
                    ctx.strokeStyle = 'white'; ctx.setLineDash([5, 5]); ctx.stroke(); ctx.setLineDash([]);
                }
                ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = '#000'; ctx.fill();
                ctx.strokeStyle = this.color; ctx.lineWidth = 3; ctx.stroke();
                ctx.fillStyle = this.color; ctx.font = "14px Arial"; ctx.textAlign = "center";
                ctx.fillText(Math.floor(this.energy), this.x, this.y + 5);
            }
            update() { if (this.owner !== 'neutral') this.energy += 0.015; }
        }

        function init() {
            planets = [
                new Planet(150, canvas.height/2, 40, 'player'),
                new Planet(canvas.width - 150, canvas.height/2, 40, 'enemy')
            ];
            for(let i=0; i<6; i++) {
                planets.push(new Planet(300 + Math.random()*(canvas.width-600), 100 + Math.random()*(canvas.height-200), 25 + Math.random()*20, 'neutral'));
            }
        }

        canvas.onclick = (e) => {
            const mouseX = e.clientX; const mouseY = e.clientY;
            let clicked = planets.find(p => Math.hypot(p.x - mouseX, p.y - mouseY) < p.radius);
            if (clicked) {
                if (clicked.owner === 'player') selectedPlanet = clicked;
                else if (selectedPlanet && selectedPlanet.energy > 5) {
                    let force = selectedPlanet.energy / 2;
                    selectedPlanet.energy -= force;
                    clicked.energy -= force;
                    if (clicked.energy < 0) { clicked.owner = 'player'; clicked.energy = Math.abs(clicked.energy); clicked.color = '#00ff88'; }
                    selectedPlanet = null;
                }
            } else selectedPlanet = null;
        };

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            planets.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(animate);
        }
        init(); animate();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return ana_sayfa_html

@app.route('/neon-arcade')
def arcade():
    return arcade_html

@app.route('/void-command')
def strategy():
    return void_command_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
