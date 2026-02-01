from flask import Flask

app = Flask(__name__)

html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Game Studio</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; overflow-x: hidden; }
        nav { background: #1a1a1a; padding: 15px; border-bottom: 2px solid #00d4ff; display: flex; justify-content: space-around; align-items: center; }
        .logo { font-size: 24px; font-weight: bold; color: #00d4ff; text-transform: uppercase; letter-spacing: 2px; }
        
        canvas { background: #000; display: block; margin: 20px auto; border: 3px solid #00d4ff; box-shadow: 0 0 20px #00d4ff; max-width: 90%; }
        .stats { font-size: 24px; margin: 10px; color: #00d4ff; font-weight: bold; }
        
        .btn-container { margin-top: 20px; padding-bottom: 50px; }
        .btn { color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin: 10px; transition: 0.3s; cursor: pointer; border: none; }
        
        .btn-bagis { background: #ff4500; }
        .btn-bagis:hover { background: #ff6347; transform: scale(1.05); }
        
        .btn-iletisim { background: #00d4ff; color: #000; }
        .btn-iletisim:hover { background: #00b8e6; transform: scale(1.05); }

        #contact-info { display: none; background: #222; margin: 20px auto; padding: 20px; border-radius: 10px; width: 80%; max-width: 400px; border: 1px dashed #00d4ff; }
    </style>
</head>
<body>

<nav>
    <div class="logo">CANO GAME STUDIO</div>
</nav>

<div class="stats">SKOR: <span id="score">0</span></div>
<canvas id="gameCanvas" width="400" height="400"></canvas>
<p>Zıplamak için <b>TIKLA</b> veya <b>BOŞLUK</b> tuşuna bas!</p>

<div class="btn-container">
    <a href="#" class="btn btn-bagis">☕ DESTEK OL</a>
    
    <button class="btn btn-iletisim" onclick="toggleContact()">✉️ İLETİŞİM</button>
    
    <div id="contact-info">
        <h3>İletişim Kanalları</h3>
        <p>📧 E-posta: <b>look16564@gmail.com</b></p>
        <p>📸 Instagram: <b>@emirwr.17</b></p>
        <p>Yeni projeler ve iş birlikleri için yazabilirsiniz!</p>
    </div>
</div>

<script>
    // İletişim panelini aç-kapat fonksiyonu
    function toggleContact() {
        var x = document.getElementById("contact-info");
        if (x.style.display === "none" || x.style.display === "") {
            x.style.display = "block";
            x.scrollIntoView({behavior: "smooth"});
        } else {
            x.style.display = "none";
        }
    }

    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");

    let bird = { x: 50, y: 150, w: 20, h: 20, gravity: 0.6, lift: -10, velocity: 0 };
    let pipes = [];
    let frame = 0;
    let score = 0;
    let gameActive = true;

    function draw() {
        if (!gameActive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        bird.velocity += bird.gravity;
        bird.y += bird.velocity;
        ctx.fillStyle = "#00d4ff";
        ctx.fillRect(bird.x, bird.y, bird.w, bird.h);

        if (frame % 80 === 0) {
            let space = 120;
            let h = Math.floor(Math.random() * (canvas.height - space));
            pipes.push({ x: canvas.width, top: h, bottom: h + space });
        }

        for (let i = pipes.length - 1; i >= 0; i--) {
            pipes[i].x -= 3;
            ctx.fillStyle = "#333";
            ctx.fillRect(pipes[i].x, 0, 40, pipes[i].top);
            ctx.fillRect(pipes[i].x, pipes[i].bottom, 40, canvas.height);

            if (bird.x < pipes[i].x + 40 && bird.x + bird.w > pipes[i].x &&
                (bird.y < pipes[i].top || bird.y + bird.h > pipes[i].bottom)) {
                gameOver();
            }

            if (pipes[i].x === 50) { score++; scoreElement.innerHTML = score; }
            if (pipes[i].x + 40 < 0) pipes.splice(i, 1);
        }

        if (bird.y + bird.h > canvas.height || bird.y < 0) gameOver();
        frame++;
        requestAnimationFrame(draw);
    }

    function gameOver() {
        gameActive = false;
        alert("OYUN BİTTİ! Skorun: " + score);
        location.reload();
    }

    window.addEventListener("keydown", (e) => { if(e.code === "Space") bird.velocity = bird.lift; });
    canvas.addEventListener("touchstart", (e) => { e.preventDefault(); bird.velocity = bird.lift; }, {passive: false});
    canvas.addEventListener("mousedown", () => { bird.velocity = bird.lift; });

    draw();
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return html_icerik

if __name__ == '__main__':
    app.run(debug=True)
     


