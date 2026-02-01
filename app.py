from flask import Flask
import os

app = Flask(__name__)

# --- ORTAK FOOTER (HER SAYFADA GÖRÜNECEK) ---
footer_html = """
<footer>
    <div class="footer-btns">
        <button class="btn btn-bagis">☕ DESTEK OL</button>
        <button class="btn btn-iletisim" onclick="toggleContact()">✉️ İLETİŞİM</button>
    </div>
    <div id="contact-box">
        <p>📧 iletisim@canostudio.com</p>
        <p>📸 @cano_game_studio</p>
    </div>
    <p style="color: #555; font-size: 12px;">&copy; 2026 Cano Game Studio. Tüm Hakları Saklıdır.</p>
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
    <title>Cano Game Studio | Kütüphane</title>
    <style>
        :root {{ --survival: #2ecc71; --strategy: #f1c40f; --arcade: #00d4ff; --horror: #e74c3c; }}
        body {{ background: #0a0a0a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        nav {{ background: #151515; padding: 20px; border-bottom: 2px solid #333; text-align: center; }}
        .logo {{ font-size: 28px; font-weight: bold; color: #00d4ff; letter-spacing: 3px; cursor:pointer; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; padding: 40px; max-width: 1200px; margin: 0 auto; flex: 1; }}
        .lib-card {{ position: relative; height: 250px; border-radius: 15px; overflow: hidden; cursor: pointer; transition: 0.4s; border: 2px solid #222; display: flex; flex-direction: column; justify-content: flex-end; padding: 20px; }}
        .lib-card:hover {{ transform: translateY(-10px); }}
        .survival {{ border-color: var(--survival); }} .strategy {{ border-color: var(--strategy); }} 
        .arcade {{ border-color: var(--arcade); }} .horror {{ border-color: var(--horror); }}
        footer {{ background: #111; padding: 30px; border-top: 2px solid #333; text-align: center; }}
        .btn {{ color: white; padding: 12px 25px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; cursor: pointer; border: none; }}
        .btn-bagis {{ background: #ff4500; }} .btn-iletisim {{ background: #444; }}
        #contact-box {{ display: none; background: #1a1a1a; padding: 15px; border-radius: 8px; margin: 15px auto; }}
    </style>
</head>
<body>
<nav><div class="logo">CANO GAME STUDIO</div></nav>
<div class="container">
    <div class="lib-card survival" onclick="alert('Survival Kütüphanesi Yakında!')"><h2 style="color:var(--survival)">Survival</h2><p>Hayatta kal.</p></div>
    <div class="lib-card strategy" onclick="alert('Strategy Kütüphanesi Yakında!')"><h2 style="color:var(--strategy)">Strategy</h2><p>Zekanı kullan.</p></div>
    <div class="lib-card arcade" onclick="window.location.href='/neon-arcade'"><h2 style="color:var(--arcade)">Neon Arcade</h2><p>Reflekslerini test et! (Uçan Kare)</p></div>
    <div class="lib-card horror" onclick="alert('Horror Kütüphanesi Yakında!')"><h2 style="color:var(--horror)">Horror</h2><p>Korkuyla yüzleş.</p></div>
</div>
{footer_html}
</body>
</html>
"""

# --- NEON ARCADE SAYFASI (OYUNUN OLDUĞU YER) ---
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
        footer {{ background: #111; padding: 30px; border-top: 2px solid #333; text-align: center; margin-top: 20px; }}
        .btn {{ color: white; padding: 12px 25px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; cursor: pointer; border: none; }}
        .btn-bagis {{ background: #ff4500; }} .btn-iletisim {{ background: #444; }}
        #contact-box {{ display: none; background: #1a1a1a; padding: 15px; border-radius: 8px; margin: 15px auto; }}
    </style>
</head>
<body>
<nav>
    <a href="/" class="back-btn">⬅ GERİ DÖ</a>
    <div style="display:inline-block; font-weight:bold; color:#00d4ff;">NEON ARCADE</div>
</nav>
<div class="stats">SKOR: <span id="score">0</span></div>
<div id="game-container">
    <div id="start-screen">
        <button class="btn-start" onclick="startGame()">OYUNU BAŞLAT</button>
    </div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
</div>
{footer_html}
<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const startScreen = document.getElementById("start-screen");
    let bird, pipes, frame, score, gameActive = false;
    function resetGame() {{ bird = {{ x: 50, y: 150, w: 25, h: 25, gravity: 0.6, lift: -9, velocity: 0 }}; pipes = []; frame = 0; score = 0; scoreElement.innerHTML = score; }}
    function startGame() {{ resetGame(); gameActive = true; startScreen.style.display = "none"; draw(); }}
    function draw() {{
        if (!gameActive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        bird.velocity += bird.gravity; bird.y += bird.velocity;
        ctx.fillStyle = "#00d4ff"; ctx.fillRect(bird.x, bird.y, bird.w, bird.h);
        if (frame % 90 === 0) {{ let h = Math.floor(Math.random() * 200) + 50; pipes.push({{ x: canvas.width, top: h, bottom: h + 130, passed: false }}); }}
        for (let i = pipes.length - 1; i >= 0; i--) {{
            pipes[i].x -= 3;
            ctx.fillStyle = "#333"; ctx.fillRect(pipes[i].x, 0, 50, pipes[i].top); ctx.fillRect(pipes[i].x, pipes[i].bottom, 50, canvas.height);
            if (bird.x < pipes[i].x + 50 && bird.x + bird.w > pipes[i].x && (bird.y < pipes[i].top || bird.y + bird.h > pipes[i].bottom)) {{ gameActive = false; startScreen.style.display = "flex"; }}
            if (!pipes[i].passed && bird.x > pipes[i].x + 50) {{ score++; scoreElement.innerHTML = score; pipes[i].passed = true; }}
            if (pipes[i].x + 50 < 0) pipes.splice(i, 1);
        }}
        if (bird.y + bird.h > canvas.height || bird.y < 0) {{ gameActive = false; startScreen.style.display = "flex"; }}
        frame++; requestAnimationFrame(draw);
    }}
    window.addEventListener("keydown", (e) => {{ if(e.code === "Space") bird.velocity = bird.lift; }});
    canvas.addEventListener("mousedown", () => {{ if(gameActive) bird.velocity = bird.lift; }});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return ana_sayfa_html

@app.route('/neon-arcade')
def arcade():
    return arcade_sayfa_html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
