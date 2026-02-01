from flask import Flask
import os

app = Flask(__name__)

html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Game Studio</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: sans-serif; text-align: center; margin: 0; overflow-x: hidden; }
        nav { background: #1a1a1a; padding: 15px; border-bottom: 2px solid #00d4ff; }
        .logo { font-size: 24px; font-weight: bold; color: #00d4ff; }
        #game-container { position: relative; width: 400px; height: 400px; margin: 20px auto; max-width: 95%; }
        canvas { background: #000; border: 3px solid #00d4ff; width: 100%; height: 100%; }
        #start-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
        .btn-start { background: #00d4ff; color: #000; border: none; padding: 15px 40px; font-size: 20px; font-weight: bold; cursor: pointer; border-radius: 50px; }
        .stats { font-size: 24px; margin: 10px; color: #00d4ff; }
        .btn-container { margin-top: 20px; }
        .btn { color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin: 10px; cursor: pointer; border: none; }
        .btn-bagis { background: #ff4500; }
        .btn-iletisim { background: #555; }
        #contact-info { display: none; background: #222; margin: 20px auto; padding: 20px; border-radius: 10px; width: 80%; max-width: 400px; border: 1px dashed #00d4ff; }
    </style>
</head>
<body>
<nav><div class="logo">CANO GAME STUDIO</div></nav>
<div class="stats">SKOR: <span id="score">0</span></div>
<div id="game-container">
    <div id="start-screen">
        <h2 style="color:#00d4ff;">Uçan Kare</h2>
        <button class="btn-start" onclick="startGame()">OYUNU BAŞLAT</button>
    </div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
</div>
<div class="btn-container">
    <button class="btn btn-bagis">☕ DESTEK OL</button>
    <button class="btn btn-iletisim" onclick="toggleContact()">✉️ İLETİŞİM</button>
    <div id="contact-info">
        <h3>İletişim</h3>
        <p>📧 E-posta: iletisim@canostudio.com</p>
    </div>
</div>
<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const startScreen = document.getElementById("start-screen");
    let bird, pipes, frame, score, gameActive = false;
    function resetGame() {
        bird = { x: 50, y: 150, w: 20, h: 20, gravity: 0.6, lift: -10, velocity: 0 };
        pipes = []; frame = 0; score = 0; scoreElement.innerHTML = score;
    }
    function startGame() { resetGame(); gameActive = true; startScreen.style.display = "none"; draw(); }
    function toggleContact() { var x = document.getElementById("contact-info"); x.style.display = (x.style.display === "none") ? "block" : "none"; }
    function draw() {
        if (!gameActive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        bird.velocity += bird.gravity; bird.y += bird.velocity;
        ctx.fillStyle = "#00d4ff"; ctx.fillRect(bird.x, bird.y, bird.w, bird.h);
        if (frame % 80 === 0) {
            let space = 120; let h = Math.floor(Math.random() * (canvas.height - space));
            pipes.push({ x: canvas.width, top: h, bottom: h + space });
        }
        for (let i = pipes.length - 1; i >= 0; i--) {
            pipes[i].x -= 3;
            ctx.fillStyle = "#333"; ctx.fillRect(pipes[i].x, 0, 40, pipes[i].top);
            ctx.fillRect(pipes[i].x, pipes[i].bottom, 40, canvas.height);
            if (bird.x < pipes[i].x + 40 && bird.x + bird.w > pipes[i].x && (bird.y < pipes[i].top || bird.y + bird.h > pipes[i].bottom)) {
                gameActive = false; startScreen.style.display = "flex"; alert("OYUN BİTTİ! Skorun: " + score);
            }
            if (pipes[i].x === 50) { score++; scoreElement.innerHTML = score; }
            if (pipes[i].x + 40 < 0) pipes.splice(i, 1);
        }
        if (bird.y + bird.h > canvas.height || bird.y < 0) { gameActive = false; startScreen.style.display = "flex"; alert("DÜŞTÜN! Skor: " + score); }
        frame++; requestAnimationFrame(draw);
    }
    window.addEventListener("keydown", (e) => { if(e.code === "Space") bird.velocity = bird.lift; });
    canvas.addEventListener("mousedown", () => { if(gameActive) bird.velocity = bird.lift; });
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return html_icerik

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
