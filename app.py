from flask import Flask
import os

app = Flask(__name__)

# --- ORTAK FOOTER ---
footer_html = """
<footer style="background: #0a0a0a; padding: 40px; border-top: 1px solid #222; text-align: center; margin-top: auto;">
    <div style="margin-bottom: 20px;">
        <button style="background:#ff4500; color:white; padding:12px 25px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; transition:0.3s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">☕ Bİ' KAHVE ISMARLA</button>
    </div>
    <p style="color: #444; font-size: 0.9rem;">© 2026 Cano Game Studio - Tüm Hakları Saklıdır.</p>
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
        body {{ background: #050505; color: white; font-family: 'Inter', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .header {{ padding: 60px 20px; text-align: center; background: linear-gradient(to bottom, #111, #050505); }}
        h1 {{ font-size: 3rem; letter-spacing: 8px; margin: 0; color: #fff; text-transform: uppercase; }}
        .subtitle {{ color: #666; margin-top: 10px; font-size: 1.1rem; }}
        
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; padding: 50px; max-width: 1200px; margin: 0 auto; width: 100%; }}
        
        .card {{ background: #0f0f0f; border: 1px solid #1a1a1a; padding: 40px; border-radius: 24px; cursor: pointer; text-align: left; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; overflow: hidden; }}
        .card:hover {{ transform: translateY(-10px); border-color: #333; background: #151515; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }}
        
        .card h2 {{ font-size: 1.8rem; margin: 0 0 10px 0; }}
        .card p {{ color: #888; line-height: 1.6; margin: 0; }}
        .card .badge {{ position: absolute; top: 20px; right: 20px; background: #222; padding: 5px 12px; border-radius: 20px; font-size: 0.7rem; color: #aaa; }}
        
        .neon-text {{ color: #00d4ff; text-shadow: 0 0 10px rgba(0,212,255,0.3); }}
        .horror-text {{ color: #e74c3c; text-shadow: 0 0 10px rgba(231,76,60,0.3); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CANO STUDIO</h1>
        <p class="subtitle">Oyun Kütüphanesi & Geliştirme Portalı</p>
    </div>

    <div class="container">
        <div class="card" onclick="window.location.href='/neon-arcade'">
            <div class="badge">AKTİF</div>
            <h2 class="neon-text">NEON ARCADE</h2>
            <p>Klasik uçan kare oyunu. Reflekslerini test et ve en yüksek skoru yap.</p>
        </div>

        <div class="card" style="opacity: 0.5; cursor: default;">
            <div class="badge">YAKINDA</div>
            <h2>STRATEJI</h2>
            <p>Kendi imparatorluğunu kur ve yönet. Çok yakında burada olacak.</p>
        </div>

        <div class="card" style="opacity: 0.5; cursor: default;">
            <div class="badge">PLANLANIYOR</div>
            <h2>SURVIVAL</h2>
            <p>Issız bir adada hayatta kalma mücadelesi. Tasarım aşamasında.</p>
        </div>
    </div>

    {footer_html}
</body>
</html>
"""

# --- NEON ARCADE OYUN SAYFASI ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Arcade | Cano Studio</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        #gc { border: 4px solid #00d4ff; box-shadow: 0 0 20px #00d4ff; border-radius: 10px; cursor: pointer; max-width: 90vw; max-height: 70vh; }
        .ui { margin-bottom: 20px; text-align: center; }
        .back-btn { position: fixed; top: 20px; left: 20px; color: #555; text-decoration: none; font-size: 0.9rem; }
        .back-btn:hover { color: #fff; }
    </style>
</head>
<body>
    <a href="/" class="back-btn">← KÜTÜPHANEYE DÖN</a>
    <div class="ui">
        <h1 style="color:#00d4ff; margin:0;">NEON ARCADE</h1>
        <p style="color:#444;">Zıplamak için Tıkla veya Boşluk Tuşuna Bas</p>
    </div>
    <canvas id="gc" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gc");
        const ctx = canvas.getContext("2d");
        let bird = { y: 200, v: 0, gravity: 0.6, jump: -9 };
        let pipes = [];
        let score = 0;
        let frames = 0;

        function draw() {
            // Arkaplan
            ctx.fillStyle = "#000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Kuş (Kare)
            bird.v += bird.gravity;
            bird.y += bird.v;
            ctx.fillStyle = "#00d4ff";
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#00d4ff";
            ctx.fillRect(50, bird.y, 30, 30);
            ctx.shadowBlur = 0;

            // Engeller
            if (frames % 90 === 0) {
                let pipeH = Math.random() * (canvas.height - 200) + 50;
                pipes.push({ x: canvas.width, h: pipeH });
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= 3;
                
                ctx.fillStyle = "#111";
                ctx.strokeStyle = "#00d4ff";
                ctx.lineWidth = 2;
                
                // Üst boru
                ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.strokeRect(pipes[i].x, 0, 50, pipes[i].h);
                
                // Alt boru
                ctx.fillRect(pipes[i].x, pipes[i].h + 140, 50, canvas.height);
                ctx.strokeRect(pipes[i].x, pipes[i].h + 140, 50, canvas.height);

                // Çarpışma
                if (50 + 30 > pipes[i].x && 50 < pipes[i].x + 50) {
                    if (bird.y < pipes[i].h || bird.y + 30 > pipes[i].h + 140) {
                        location.reload();
                    }
                }

                if (pipes[i].x < -50) pipes.splice(i, 1);
            }

            // Sınır kontrolü
            if (bird.y > canvas.height || bird.y < 0) location.reload();

            frames++;
            requestAnimationFrame(draw);
        }

        window.onclick = () => bird.v = bird.jump;
        window.onkeydown = (e) => { if(e.code === 'Space') bird.v = bird.jump; };
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
