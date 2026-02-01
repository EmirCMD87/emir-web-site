from flask import Flask
import os

app = Flask(__name__)

# --- ORTAK FOOTER (Sabitlendi) ---
footer_html = """
<footer style="background: #0a0a0a; padding: 40px; border-top: 1px solid #222; text-align: center; margin-top: auto;">
    <div style="margin-bottom: 20px;">
        <button style="background:#ff4500; color:white; padding:12px 25px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; transition:0.3s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">☕ Bİ' KAHVE ISMARLA</button>
    </div>
    <p style="color: #444; font-size: 0.9rem;">© 2026 Cano Game Studio - Diyarbakır</p>
</footer>
"""

# --- ANA KÜTÜPHANE SAYFASI ---
ana_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Game Studio | Kütüphane</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background: #050505; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .header {{ padding: 80px 20px; text-align: center; background: linear-gradient(to bottom, #111, #050505); }}
        h1 {{ font-size: 3.5rem; letter-spacing: 10px; margin: 0; color: #fff; text-transform: uppercase; }}
        .subtitle {{ color: #00d4ff; margin-top: 10px; font-size: 1.1rem; opacity: 0.8; }}
        
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; padding: 50px; max-width: 1200px; margin: 0 auto; width: 100%; }}
        
        .card {{ background: #0f0f0f; border: 1px solid #1a1a1a; padding: 40px; border-radius: 24px; cursor: pointer; text-align: left; transition: all 0.4s ease; position: relative; overflow: hidden; }}
        .card:hover {{ transform: translateY(-10px); border-color: #00d4ff; background: #151515; box-shadow: 0 0 30px rgba(0,212,255,0.1); }}
        
        .card h2 {{ font-size: 1.8rem; margin: 0 0 10px 0; }}
        .card p {{ color: #888; line-height: 1.6; margin: 0; }}
        .card .badge {{ position: absolute; top: 20px; right: 20px; background: #00d4ff22; border: 1px solid #00d4ff; padding: 5px 12px; border-radius: 20px; font-size: 0.7rem; color: #00d4ff; }}
        
        .neon-text {{ color: #00d4ff; text-shadow: 0 0 10px rgba(0,212,255,0.3); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CANO STUDIO</h1>
        <p class="subtitle">Premium Oyun Kütüphanesi</p>
    </div>

    <div class="container">
        <div class="card" onclick="window.location.href='/neon-arcade'">
            <div class="badge">HEMEN OYNA</div>
            <h2 class="neon-text">NEON ARCADE</h2>
            <p>Reflekslerini test et. Engellerden kaç ve en yüksek skora ulaş!</p>
        </div>

        <div class="card" style="opacity: 0.4; cursor: not-allowed;">
            <div class="badge" style="border-color: #555; color: #555;">YAKINDA</div>
            <h2>STRATEJİ</h2>
            <p>Diyarbakır merkezli bir imparatorluk kurmaya hazır mısın? Geliştiriliyor...</p>
        </div>
    </div>

    {footer_html}
</body>
</html>
"""

# --- NEON ARCADE OYUN SAYFASI (GELİŞTİRİLMİŞ) ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Arcade | Cano Studio</title>
    <style>
        body { background: #000; color: #fff; font-family: 'Courier New', Courier, monospace; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        #gc { border: 4px solid #00d4ff; box-shadow: 0 0 30px #00d4ff66; border-radius: 10px; cursor: pointer; }
        .ui { position: absolute; top: 20px; text-align: center; z-index: 10; pointer-events: none; }
        .score-box { font-size: 2rem; color: #00d4ff; font-weight: bold; }
        .high-score { color: #ff4500; font-size: 1rem; }
        .back-btn { position: fixed; top: 20px; left: 20px; color: #555; text-decoration: none; border: 1px solid #222; padding: 5px 15px; border-radius: 5px; }
        .back-btn:hover { color: #fff; border-color: #fff; }
        #game-over { display: none; position: absolute; background: rgba(0,0,0,0.9); padding: 30px; border: 2px solid #ff4500; border-radius: 15px; text-align: center; }
    </style>
</head>
<body>
    <a href="/" class="back-btn">← KÜTÜPHANEYE DÖN</a>
    
    <div class="ui">
        <div class="score-box" id="scoreDisplay">0</div>
        <div class="high-score" id="highScoreDisplay">EN YÜKSEK: 0</div>
    </div>

    <div id="game-over">
        <h1 style="color:#ff4500">OYUN BİTTİ</h1>
        <p id="finalScore"></p>
        <button onclick="location.reload()" style="background:#00d4ff; border:none; padding:10px 20px; cursor:pointer; font-weight:bold; border-radius:5px;">TEKRAR DENE</button>
    </div>

    <canvas id="gc" width="400" height="500"></canvas>

    <script>
        const canvas = document.getElementById("gc");
        const ctx = canvas.getContext("2d");
        const scoreDisplay = document.getElementById("scoreDisplay");
        const highScoreDisplay = document.getElementById("highScoreDisplay");
        const gameOverScreen = document.getElementById("game-over");

        let bird = { y: 250, v: 0, gravity: 0.5, jump: -8 };
        let pipes = [];
        let score = 0;
        let frames = 0;
        let gameActive = true;
        let speed = 3;

        // Yerel depolamadan yüksek skoru al
        let highScore = localStorage.getItem("canoHighScore") || 0;
        highScoreDisplay.innerText = "EN YÜKSEK: " + highScore;

        function draw() {
            if (!gameActive) return;

            ctx.fillStyle = "#000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Kuş
            bird.v += bird.gravity;
            bird.y += bird.v;
            ctx.fillStyle = "#00d4ff";
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#00d4ff";
            ctx.fillRect(50, bird.y, 30, 30);
            ctx.shadowBlur = 0;

            // Engeller
            if (frames % 100 === 0) {
                let gap = 150; // Geçiş boşluğu
                let pipeH = Math.random() * (canvas.height - gap - 100) + 50;
                pipes.push({ x: canvas.width, h: pipeH, scored: false });
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= speed;
                
                ctx.fillStyle = "#111";
                ctx.strokeStyle = "#00d4ff";
                ctx.lineWidth = 2;
                
                // Boruları çiz
                ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.strokeRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.fillRect(pipes[i].x, pipes[i].h + 150, 50, canvas.height);
                ctx.strokeRect(pipes[i].x, pipes[i].h + 150, 50, canvas.height);

                // Skor Artışı
                if (pipes[i].x < 50 && !pipes[i].scored) {
                    score++;
                    pipes[i].scored = true;
                    scoreDisplay.innerText = score;
                    if(score % 5 === 0) speed += 0.2; // Her 5 skorda hızlanır
                }

                // Çarpışma
                if (50 + 25 > pipes[i].x && 50 < pipes[i].x + 50) {
                    if (bird.y < pipes[i].h || bird.y + 30 > pipes[i].h + 150) {
                        endGame();
                    }
                }

                if (pipes[i].x < -50) pipes.splice(i, 1);
            }

            if (bird.y > canvas.height || bird.y < 0) endGame();

            frames++;
            requestAnimationFrame(draw);
        }

        function endGame() {
            gameActive = false;
            if (score > highScore) {
                localStorage.setItem("canoHighScore", score);
            }
            document.getElementById("finalScore").innerText = "Skorun: " + score;
            gameOverScreen.style.display = "block";
        }

        const handleJump = () => { if(gameActive) bird.v = bird.jump; };
        window.onclick = handleJump;
        window.onkeydown = (e) => { if(e.code === 'Space') handleJump(); };
        
        draw();
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
