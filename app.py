from flask import Flask
import os

app = Flask(__name__)

# --- ORTAK FOOTER VE JS ---
footer_html = """
<footer style="background: #111; padding: 30px; border-top: 2px solid #333; text-align: center; margin-top: auto;">
    <div class="footer-btns">
        <button class="btn btn-bagis" style="background:#ff4500; color:white; padding:12px 25px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">☕ DESTEK OL</button>
        <button class="btn btn-iletisim" style="background:#444; color:white; padding:12px 25px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; margin-left:10px;" onclick="toggleContact()">✉️ İLETİŞİM</button>
    </div>
    <div id="contact-box" style="display:none; background:#1a1a1a; padding:15px; border-radius:8px; margin:15px auto; max-width:300px; color:#aaa; border:1px dashed #555;">
        <p>📧 iletisim@canostudio.com</p>
        <p>📸 @cano_game_studio</p>
    </div>
    <p style="color: #555; font-size: 12px; margin-top:15px;">&copy; 2026 Cano Game Studio. Tüm Hakları Saklıdır.</p>
</footer>
<script>
    function toggleContact() {
        var x = document.getElementById("contact-box");
        x.style.display = (x.style.display === "none" || x.style.display === "") ? "block" : "none";
    }
</script>
"""

# --- ANA SAYFA (KÜTÜPHANELER) ---
ana_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Game Studio | Portall</title>
    <style>
        :root {{ --survival: #2ecc71; --strategy: #f1c40f; --arcade: #00d4ff; --horror: #e74c3c; }}
        body {{ background: #0a0a0a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        nav {{ background: #151515; padding: 20px; border-bottom: 2px solid #333; text-align: center; }}
        .logo {{ font-size: 28px; font-weight: bold; color: #00d4ff; letter-spacing: 3px; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; padding: 40px; max-width: 1200px; margin: 0 auto; flex: 1; }}
        .lib-card {{ position: relative; height: 250px; border-radius: 15px; overflow: hidden; cursor: pointer; transition: 0.4s; border: 2px solid #222; display: flex; flex-direction: column; justify-content: flex-end; padding: 20px; }}
        .lib-card:hover {{ transform: translateY(-10px); }}
        .survival {{ border-color: var(--survival); }} .strategy {{ border-color: var(--strategy); }} 
        .arcade {{ border-color: var(--arcade); }} .horror {{ border-color: var(--horror); }}
        h2 {{ margin: 0; text-transform: uppercase; }}
    </style>
</head>
<body>
<nav><div class="logo">CANO GAME STUDIO</div></nav>
<div class="container">
    <div class="lib-card survival" onclick="alert('Survival Yakında!')"><h2 style="color:var(--survival)">Survival</h2><p>Hayatta kalma kütüphanesi.</p></div>
    <div class="lib-card strategy" onclick="alert('Strategy Yakında!')"><h2 style="color:var(--strategy)">Strategy</h2><p>Strateji kütüphanesi.</p></div>
    <div class="lib-card arcade" onclick="window.location.href='/neon-arcade'"><h2 style="color:var(--arcade)">Neon Arcade</h2><p>Uçan Kare burada!</p></div>
    <div class="lib-card horror" onclick="window.location.href='/horror'"><h2 style="color:var(--horror)">Horror</h2><p>Zihnin Karanlığı...</p></div>
</div>
{footer_html}
</body>
</html>
"""

# --- NEON ARCADE (UÇAN KARE) ---
arcade_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Arcade | Uçan Kare</title>
    <style>
        body {{ background: #0f0f0f; color: white; font-family: sans-serif; text-align: center; margin: 0; }}
        nav {{ background: #151515; padding: 15px; border-bottom: 2px solid #00d4ff; }}
        .back-btn {{ color: #00d4ff; text-decoration: none; font-weight: bold; float: left; }}
        #game-container {{ position: relative; width: 400px; height: 400px; margin: 20px auto; max-width: 95%; }}
        canvas {{ background: #000; border: 3px solid #00d4ff; width: 100%; height: 100%; box-shadow: 0 0 20px #00d4ff; }}
        #start-screen {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }}
        .btn-start {{ background: #00d4ff; color: #000; border: none; padding: 15px 40px; font-size: 20px; font-weight: bold; cursor: pointer; border-radius: 50px; }}
        .stats {{ font-size: 28px; margin: 10px; color: #00d4ff; font-weight: bold; }}
    </style>
</head>
<body>
<nav><a href="/" class="back-btn">⬅ GERİ</a><div style="color:#00d4ff; font-weight:bold;">NEON ARCADE</div></nav>
<div class="stats">SKOR: <span id="score">0</span></div>
<div id="game-container">
    <div id="start-screen"><button class="btn-start" onclick="startGame()">OYUNU BAŞLAT</button></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
</div>
{footer_html}
<script>
    const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d");
    let bird, pipes, frame, score, gameActive = false;
    function resetGame() {{ bird = {{ x: 50, y: 150, w: 25, h: 25, gravity: 0.6, lift: -9, velocity: 0 }}; pipes = []; frame = 0; score = 0; document.getElementById("score").innerHTML = 0; }}
    function startGame() {{ resetGame(); gameActive = true; document.getElementById("start-screen").style.display = "none"; draw(); }}
    function draw() {{
        if (!gameActive) return; ctx.clearRect(0, 0, canvas.width, canvas.height);
        bird.velocity += bird.gravity; bird.y += bird.velocity;
        ctx.fillStyle = "#00d4ff"; ctx.fillRect(bird.x, bird.y, bird.w, bird.h);
        if (frame % 90 === 0) {{ let h = Math.floor(Math.random() * 200) + 50; pipes.push({{ x: canvas.width, top: h, bottom: h + 130, passed: false }}); }}
        for (let i = pipes.length - 1; i >= 0; i--) {{
            pipes[i].x -= 3; ctx.fillStyle = "#333"; ctx.fillRect(pipes[i].x, 0, 50, pipes[i].top); ctx.fillRect(pipes[i].x, pipes[i].bottom, 50, canvas.height);
            if (bird.x < pipes[i].x + 50 && bird.x + bird.w > pipes[i].x && (bird.y < pipes[i].top || bird.y + bird.h > pipes[i].bottom)) {{ gameActive = false; document.getElementById("start-screen").style.display = "flex"; }}
            if (!pipes[i].passed && bird.x > pipes[i].x + 50) {{ score++; document.getElementById("score").innerHTML = score; pipes[i].passed = true; }}
            if (pipes[i].x + 50 < 0) pipes.splice(i, 1);
        }}
        if (bird.y + bird.h > canvas.height || bird.y < 0) {{ gameActive = false; document.getElementById("start-screen").style.display = "flex"; }}
        frame++; requestAnimationFrame(draw);
    }}
    window.addEventListener("keydown", (e) => {{ if(e.code === "Space") bird.velocity = bird.lift; }});
    canvas.addEventListener("mousedown", () => {{ if(gameActive) bird.velocity = bird.lift; }});
</script>
</body>
</html>
"""

# --- HORROR (ZİHNİN KARANLIĞI) ---
horror_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zihnin Karanlığı | Horror</title>
    <style>
        body {{ background: #000; color: #eee; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }}
        nav {{ background: #151515; padding: 10px; border-bottom: 1px solid #e74c3c; }}
        .back-btn {{ color: #e74c3c; text-decoration: none; font-weight: bold; float: left; }}
        #game-screen {{ position: relative; width: 100vw; height: 75vh; background: #050505; cursor: none; }}
        #flashlight {{ position: absolute; width: 100%; height: 100%; background: radial-gradient(circle 120px at 50% 50%, rgba(255,255,200,0.1) 0%, rgba(0,0,0,1) 100%); pointer-events: none; z-index: 10; }}
        #inventory {{ position: absolute; bottom: 20px; left: 20px; display: flex; gap: 10px; z-index: 20; background: rgba(0,0,0,0.7); padding: 10px; border: 1px solid #444; }}
        .inv-item {{ width: 40px; height: 40px; border: 1px solid #555; display: flex; align-items: center; justify-content: center; font-size: 20px; opacity: 0.8; }}
        #inner-voice {{ position: absolute; top: 20%; width: 100%; text-align: center; z-index: 20; font-size: 20px; color: #999; font-style: italic; text-shadow: 0 0 10px red; opacity: 0; transition: 1s; }}
        #spook-shadow {{ position: absolute; top: 40%; left: 60%; width: 80px; height: 160px; background: rgba(0,0,0,0.9); filter: blur(15px); display: none; z-index: 5; }}
    </style>
</head>
<body onmousemove="updateFlashlight(event)">
<nav><a href="/" class="back-btn">⬅ GERİ</a><div style="color:#e74c3c; font-weight:bold; text-align:center;">HORROR LIBRARY</div></nav>
<div id="game-screen">
    <div id="spook-shadow"></div><div id="flashlight"></div><div id="inner-voice">Biri mi var?</div>
    <div id="inventory"><div class="inv-item">🔦</div><div class="inv-item">🔪</div><div class="inv-item">📱</div></div>
</div>
{footer_html}
<script>
    const voiceBox = document.getElementById('inner-voice');
    const thoughts = ["Neden buradayım?", "Bu ses de neydi?", "İlacımı bulmalıyım...", "Beni izliyorlar!", "Oraya bakma..."];
    function updateFlashlight(e) {{ document.getElementById('flashlight').style.background = `radial-gradient(circle 140px at ${{e.clientX}}px ${{e.clientY}}px, rgba(255,255,220,0.15) 0%, rgba(0,0,0,1) 100%)`; }}
    function startMindGames() {{
        setTimeout(() => {{
            let r = Math.floor(Math.random() * 3);
            if(r === 0) {{ voiceBox.innerText = thoughts[Math.floor(Math.random()*thoughts.length)]; voiceBox.style.opacity = 1; setTimeout(()=>voiceBox.style.opacity=0, 2500); }}
            else if(r === 1) {{ document.getElementById('spook-shadow').style.display='block'; setTimeout(()=>document.getElementById('spook-shadow').style.display='none', 150); }}
            else {{ document.body.style.filter = "invert(1)"; setTimeout(()=>document.body.style.filter="none", 50); }}
            startMindGames();
        }}, Math.random() * 5000 + 3000);
    }}
    startMindGames();
</script>
</body>
</html>
"""

@app.route('/')
def home(): return ana_sayfa_html

@app.route('/neon-arcade')
def arcade(): return arcade_sayfa_html

@app.route('/horror')
def horror(): return horror_sayfa_html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
