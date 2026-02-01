from flask import Flask
import os

app = Flask(__name__)

html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Game Studio | Kütüphane</title>
    <style>
        :root {
            --survival: #2ecc71;
            --strategy: #f1c40f;
            --arcade: #00d4ff;
            --horror: #e74c3c;
        }
        body { 
            background: #0a0a0a; color: white; font-family: 'Segoe UI', sans-serif; 
            margin: 0; display: flex; flex-direction: column; min-height: 100vh;
        }
        
        /* Navbar */
        nav { background: #151515; padding: 20px; border-bottom: 2px solid #333; text-align: center; }
        .logo { font-size: 28px; font-weight: bold; color: #00d4ff; letter-spacing: 3px; }

        /* Kütüphane Kartları Konteynırı */
        .container { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 25px; padding: 40px; max-width: 1200px; margin: 0 auto; flex: 1;
        }

        /* Kart Tasarımı */
        .lib-card {
            position: relative; height: 300px; border-radius: 15px; overflow: hidden;
            cursor: pointer; transition: 0.4s; border: 2px solid #222;
            display: flex; flex-direction: column; justify-content: flex-end; padding: 20px;
        }
        .lib-card:hover { transform: translateY(-10px); }
        
        /* Renk Temaları */
        .survival { border-color: var(--survival); box-shadow: 0 0 15px rgba(46, 204, 113, 0.2); }
        .strategy { border-color: var(--strategy); box-shadow: 0 0 15px rgba(241, 196, 15, 0.2); }
        .arcade { border-color: var(--arcade); box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); }
        .horror { border-color: var(--horror); box-shadow: 0 0 15px rgba(231, 76, 60, 0.2); }

        .lib-card h2 { margin: 0; font-size: 24px; text-transform: uppercase; }
        .lib-card p { font-size: 14px; color: #ccc; }

        /* Sabit Alt Bölüm (Footer) */
        footer {
            background: #111; padding: 30px; border-top: 2px solid #333;
            text-align: center; margin-top: auto;
        }
        .footer-btns { margin-bottom: 20px; }
        .btn { 
            color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; 
            font-weight: bold; display: inline-block; margin: 5px; cursor: pointer; border: none; 
        }
        .btn-bagis { background: #ff4500; box-shadow: 0 0 10px rgba(255,69,0,0.4); }
        .btn-iletisim { background: #444; }
        #contact-box { 
            display: none; background: #1a1a1a; padding: 15px; 
            border: 1px dashed #555; border-radius: 8px; max-width: 400px; margin: 15px auto; 
        }
    </style>
</head>
<body>

<nav><div class="logo">CANO GAME STUDIO</div></nav>

<div class="container">
    <div class="lib-card survival" onclick="alert('Survival Kütüphanesi Yakında!')">
        <h2 style="color: var(--survival);">Survival</h2>
        <p>Zorlu şartlarda hayatta kalmaya hazır mısın?</p>
    </div>

    <div class="lib-card strategy" onclick="alert('Strategy Kütüphanesi Yakında!')">
        <h2 style="color: var(--strategy);">Strategy</h2>
        <p>Zekanı konuştur, ordunu yönet.</p>
    </div>

    <div class="lib-card arcade" onclick="window.location.href='/neon-arcade'">
        <h2 style="color: var(--arcade);">Neon Arcade</h2>
        <p>Reflekslerini test et! (Uçan Kare Burada)</p>
    </div>

    <div class="lib-card horror" onclick="alert('Horror Kütüphanesi Yakında!')">
        <h2 style="color: var(--horror);">Horror / Action</h2>
        <p>Karanlıkla yüzleşmeye cesaretin var mı?</p>
    </div>
</div>

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

</body>
</html>
"""

@app.route('/')
def home():
    return html_icerik

@app.route('/neon-arcade')
def arcade():
    return "<h1>Neon Arcade Kütüphanesi</h1><p>Uçan Kare oyunu buraya eklenecek. Geri dönmek için tarayıcıyı kullanın.</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)   
