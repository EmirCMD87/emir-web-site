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
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Studio | Dashboard</title>
    <style>
        * {{ box-sizing: border-box; transition: 0.3s ease; }}
        body {{ background: #020202; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .header {{ padding: 60px 20px; text-align: center; }}
        h1 {{ font-size: 3rem; letter-spacing: 12px; margin: 0; color: #fff; font-weight: 200; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 40px; max-width: 1200px; margin: 0 auto; width:100%; }}
        .game-card {{ background: #0a0a0a; border: 1px solid #1a1a1a; padding: 30px; border-radius: 8px; cursor: pointer; }}
        .game-card:hover {{ border-color: #fff; background: #111; transform: translateY(-5px); }}
        .status {{ font-size: 9px; letter-spacing: 2px; border: 1px solid; display: inline-block; padding: 2px 8px; margin-bottom: 15px; border-radius: 4px; }}
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
            <p class="description">Ultra hızlı refleks testi. Anlık sıfırlama ile kesintisiz aksiyon.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/void-command'">
            <div class="status strategy">STRATEGY</div>
            <h2>VOID COMMAND</h2>
            <p class="description">Gezegenleri feth et. Her seviyede artan zorluk ve daha agresif rakipler.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/lost-forest'">
            <div class="status horror">HORROR</div>
            <h2 style="color:#ff4500">THE LOST FOREST</h2>
            <p class="description">WASD ve Mobil destekli korku. Ormandaki gizemli kapıyı bul ve kaç.</p>
        </div>
    </div>
    {footer_html}
</body>
</html>
"""

# --- 2. NEON ARCADE (ANLIK RESET) ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Neon Arcade | Instant</title>
    <style>
        body { background: #000; color: #fff; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        canvas { border: 2px solid #00d4ff; box-shadow: 0 0 20px #00d4ff33; cursor: pointer; }
        #s { position: absolute; top: 20px; font-size: 3rem; color: #00d4ff; opacity: 0.5; font-family: sans-serif; }
    </style>
</head>
<body>
    <div id="s">0</div>
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

# --- 3. VOID COMMAND (LEVEL SİSTEMİ) ---
void_command_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Void Command | Strategic</title>
    <style>
        body { background: #050505; color: #00ff88; font-family: monospace; margin: 0; overflow: hidden; }
        .ui { position: fixed; width: 100%; padding: 20px; display: flex; justify-content: space-between; background: rgba(0,0,0,0.8); z-index: 10; }
    </style>
</head>
<body>
    <div class="ui"><span id="lvl">LEVEL: 1</span><span>HEDEF: TÜM DÜŞMANLARI YOK ET</span></div>
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
        function init() {
            planets = [new Planet(100, canvas.height/2, 40, 'player')];
            for(let i=0; i<level; i++) planets.push(new Planet(canvas.width-100, (canvas.height/(level+1))*(i+1), 35, 'enemy'));
            for(let i=0; i<6; i++) planets.push(new Planet(Math.random()*canvas.width, Math.random()*canvas.height, 25, 'neutral'));
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
            if(!planets.some(p => p.owner === 'enemy')) { level++; document.getElementById('lvl').innerText = "LEVEL: " + level; init(); }
        };
        function loop() {
            ctx.fillStyle = "black"; ctx.fillRect(0,0,canvas.width,canvas.height);
            planets.forEach(p => { if(p.owner !== 'neutral') p.energy += 0.01 * level; p.draw(); });
            requestAnimationFrame(loop);
        }
        init(); loop();
    </script>
</body>
</html>
"""

# --- 4. THE LOST FOREST (WASD + MOBİL + SES) ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>The Lost Forest | Horror</title>
    <style>
        body { background: #000; color: #fff; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; }
        #joystick-zone { position: fixed; bottom: 40px; left: 40px; width: 100px; height: 100px; background: rgba(255,255,255,0.1); border-radius: 50%; display: none; touch-action: none; z-index: 100; }
        #joystick-stick { position: absolute; top: 30px; left: 30px; width: 40px; height: 40px; background: rgba(255,255,255,0.3); border-radius: 50%; }
        @media (max-width: 768px) { #joystick-zone { display: block; } }
        #msg { position: fixed; top: 20px; width: 100%; text-align: center; color: #500; font-weight: bold; pointer-events: none; }
    </style>
</head>
<body>
    <div id="msg">ORMANIN İÇİNDEKİ BEYAZ KAPIYI BUL...</div>
    <div id="joystick-zone"><div id="joystick-stick"></div></div>
    <canvas id="h"></canvas>
    <script>
        const c = document.getElementById("h"), ctx = c.getContext("2d");
        c.width = window.innerWidth; c.height = window.innerHeight;
        let player = { x: 0, y: 0, s: 3 }, door = { x: 1200, y: 800 }, camera = { x: 0, y: 0 }, keys = {}, audioCtx = null;
        let joystick = { active: false, x: 0, y: 0 };

        function playSound(f, d) {
            if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain();
            o.type = 'sine'; o.frequency.setValueAtTime(f, audioCtx.currentTime);
            g.gain.setValueAtTime(0.05, audioCtx.currentTime); g.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + d);
            o.connect(g); g.connect(audioCtx.destination); o.start(); o.stop(audioCtx.currentTime + d);
        }

        window.onkeydown = (e) => keys[e.code] = true; window.onkeyup = (e) => keys[e.code] = false;
        const jZone = document.getElementById("joystick-zone"), jStick = document.getElementById("joystick-stick");
        jZone.ontouchmove = (e) => {
            joystick.active = true; let touch = e.touches[0], rect = jZone.getBoundingClientRect();
            let dx = touch.clientX - (rect.left + 50), dy = touch.clientY - (rect.top + 50);
            let dist = Math.min(Math.hypot(dx, dy), 40); let angle = Math.atan2(dy, dx);
            joystick.x = Math.cos(angle) * (dist/40); joystick.y = Math.sin(angle) * (dist/40);
            jStick.style.transform = `translate(${joystick.x * 30}px, ${joystick.y * 30}px)`;
        };
        jZone.ontouchend = () => { joystick.active = false; joystick.x = 0; joystick.y = 0; jStick.style.transform = "translate(0,0)"; };

        function draw() {
            ctx.fillStyle = "#010501"; ctx.fillRect(0,0,c.width,c.height);
            let moved = false;
            if(keys['KeyW'] || joystick.y < -0.2) { player.y -= player.s; moved = true; }
            if(keys['KeyS'] || joystick.y > 0.2) { player.y += player.s; moved = true; }
            if(keys['KeyA'] || joystick.x < -0.2) { player.x -= player.s; moved = true; }
            if(keys['KeyD'] || joystick.x > 0.2) { player.x += player.s; moved = true; }
            if(moved && Math.random() < 0.05) playSound(100, 0.1);
            
            camera.x = player.x - c.width/2; camera.y = player.y - c.height/2;
            
            // Ağaçlar
            ctx.fillStyle = "#051005";
            for(let i=-5; i<15; i++) for(let j=-5; j<15; j++) ctx.fillRect(i*400-camera.x, j*400-camera.y, 10, 80);
            
            // Kapı
            ctx.fillStyle = "#fff"; ctx.shadowBlur = 30; ctx.shadowColor = "#fff";
            ctx.fillRect(door.x-camera.x, door.y-camera.y, 40, 60); ctx.shadowBlur = 0;
            
            // Fener
            let g = ctx.createRadialGradient(c.width/2, c.height/2, 0, c.width/2, c.height/2, 200);
            g.addColorStop(0, "transparent"); g.addColorStop(1, "rgba(0,0,0,0.99)");
            ctx.fillStyle = g; ctx.fillRect(0,0,c.width,c.height);
            
            if(Math.hypot(player.x-door.x, player.y-door.y) < 50) { playSound(600, 0.5); alert("KURTULDUN!"); location.href="/"; }
            requestAnimationFrame(draw);
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
@app.route('/lost-forest')
def horror(): return horror_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
