from flask import Flask
import os

app = Flask(__name__)

html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>Cano Game Studio</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; overflow: hidden; }
        nav { background: #1a1a1a; padding: 15px; border-bottom: 2px solid #00d4ff; box-shadow: 0 2px 10px rgba(0,212,255,0.3); }
        .logo { font-size: 24px; font-weight: bold; color: #00d4ff; text-transform: uppercase; letter-spacing: 2px; }
        
        #game-container { position: relative; width: 400px; height: 400px; margin: 20px auto; max-width: 95%; touch-action: none; }
        canvas { background: #000; display: block; border: 3px solid #00d4ff; box-shadow: 0 0 20px #00d4ff; width: 100%; height: 100%; border-radius: 8px; }
        
        #start-screen { 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            background: rgba(0, 0, 0, 0.85); display: flex; flex-direction: column; 
            justify-content: center; align-items: center; z-index: 10; border-radius: 5px;
        }
        
        .btn-start { 
            background: #00d4ff; color: #000; border: none; padding: 15px 40px; 
            font-size: 22px; font-weight: bold; cursor: pointer; border-radius: 50px;
            box-shadow: 0 0 20px #00d4ff; transition: 0.3s;
        }
        .btn-start:hover { transform: scale(1.1); background: #fff; }

        .stats { font-size: 28px; margin: 15px; color: #00d4ff; font-weight: bold; text-shadow: 0 0 10px #00d4ff; }
        
        .btn-container { margin-top: 10px; }
        .btn { color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin: 10px; cursor: pointer; border: none; transition: 0.3s; }
        .btn-bagis { background: #ff4500; }
        .btn-iletisim { background: #555; }
        .btn:hover { opacity: 0.8; transform: translateY(-2px); }

        #contact-info { display: none; background: #222; margin: 15px auto; padding: 20px; border-radius: 10px; width: 85%; max-width: 350px; border: 1px dashed #00d4ff; }
    </style>
</head>
<body>

<nav><div class="logo">CANO GAME STUDIO</div></nav>

<div class="stats">SKOR: <span id="score">0</span></div>

<div id="game-container">
    <div id="start-screen">
        <h1 style="color:#00d4ff; margin-bottom:10px;">UÇAN KARE</h1>
        <button class="btn-start" onclick="startGame()">OYUNU BAŞLAT</button>
        <p style="margin-top:20px; color:#aaa; font-size:14px;">Zıplamak için Ekrana Tıkla veya Boşluk Tuşuna Bas</p>
    </div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
</div>

<div class="btn-container">
    <button class="btn btn-bagis">☕ DESTEK OL</button>
    <button class="btn btn-iletisim" onclick="toggleContact()">✉️ İLETİŞİM</button>
    <div id="contact-info">
        <h3 style="color:#00d4ff; margin-top:0;">İletişim Kanalları</h3>
        <p>📧 E-posta: <b>iletisim@canostudio.com</b></p>
        <p>📸 Instagram: <b>@cano_game_studio</b></p>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const startScreen = document.getElementById("start-screen");

    let bird, pipes, frame, score, gameActive = false;

    function resetGame() {
        bird = { x: 50, y: 150, w: 25, h: 25, gravity: 0.6, lift: -9, velocity: 0 };
        pipes = [];
        frame = 0;
        score = 0;
        scoreElement.innerHTML = score;
    }

    function startGame() {
        resetGame();
        gameActive = true;
        startScreen.style.display = "none";
        draw();
    }

    function toggleContact() {
        var x = document.getElementById("contact-info");
        x.style.display = (x.style.display === "none" || x.style.display === "") ? "block" : "none";
        if(x.style.display === "block") x.scrollIntoView({behavior: "smooth"});
    }

    function draw() {
        if (!gameActive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Kuş Hareketleri
        bird.velocity += bird.gravity;
        bird.y += bird.velocity;
        
        // Kuş Çizimi (Glow Efekti)
        ctx.fillStyle = "#00d4ff";
        ctx.shadowBlur = 10;
        ctx.shadowColor = "#00d4ff";
        ctx.fillRect(bird.x, bird.y, bird.w, bird.h);
        ctx.shadowBlur = 0; // Diğer çizimler parlamasın

        // Boru Oluşturma
        if (frame % 90 === 0) {
            let space = 130;
            let h = Math.floor(Math.random() * (canvas.height - space - 100)) + 50;
            pipes.push({ x: canvas.width, top: h, bottom: h + space, passed: false });
        }

        // Boruları Çiz ve Hareket Ettir
        for (let i = pipes.length - 1; i >= 0; i--) {
            pipes[i].x -= 2.5; // Hız dengelendi
            
            ctx.fillStyle = "#333";
            // Üst Boru
            ctx.fillRect(pipes[i].x, 0, 50, pipes[i].top);
            // Alt Boru
            ctx.fillRect(pipes[i].x, pipes[i].bottom, 50, canvas.height);

            // Çarpışma Kontrolü
            if (bird.x < pipes[i].x + 50 && bird.x + bird.w > pipes[i].x &&
                (bird.y < pipes[i].top || bird.y + bird.h > pipes[i].bottom)) {
                gameOver();
            }

            // SKOR SAYMA (Kesin Çözüm)
            if (!pipes[i].passed && bird.x > pipes[i].x + 50) {
                score++;
                scoreElement.innerHTML = score;
                pipes[i].passed = true;
            }

            // Ekrandan çıkan boruları sil
            if (pipes[i].x + 50 < 0) pipes.splice(i, 1);
        }

        // Sınır Kontrolleri
        if (bird.y + bird.h > canvas.height || bird.y < 0) gameOver();

        frame++;
        requestAnimationFrame(draw);
    }

    function gameOver() {
        gameActive = false;
        startScreen.style.display = "flex";
        startScreen.innerHTML = `
            <h1 style="color:#ff4500;">OYUN BİTTİ</h1>
            <h2 style="color:#fff;">SKORUN: ${score}</h2>
            <button class="btn-start" onclick="startGame()">TEKRAR DENE</button>
        `;
    }

    // Kontroller
    window.addEventListener("keydown", (e) => { 
        if(e.code === "Space") {
            bird.velocity = bird.lift;
            if(!gameActive && startScreen.style.display !== "none") startGame();
        }
    });
    
    canvas.addEventListener("mousedown", () => { if(gameActive) bird.velocity = bird.lift; });
    
    canvas.addEventListener("touchstart", (e) => { 
        if(gameActive) {
            e.preventDefault();
            bird.velocity = bird.lift;
        }
    }, {passive: false});

    resetGame(); // Başlangıçta objeleri hazırla
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return html_icerik

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
