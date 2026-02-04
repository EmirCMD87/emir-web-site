from flask import Flask
import os

app = Flask(__name__)

# --- MODERN VE İHTİŞAMLI ANA SAYFA ---
ana_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Game Studio | Official</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;500&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            background-color: #050505; 
            color: #ffffff; 
            font-family: 'Inter', sans-serif; 
            overflow-x: hidden;
        }

        /* Arka Plan Animasyonu */
        .bg-glow {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #050505 100%);
            z-index: -1;
        }

        /* Ana Konteynır */
        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }

        h1 {
            font-family: 'Syncopate', sans-serif;
            font-size: clamp(2rem, 8vw, 5rem);
            font-weight: 700;
            letter-spacing: 15px;
            text-transform: uppercase;
            background: linear-gradient(to bottom, #fff 30%, #444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            animation: fadeIn 2s ease-out;
        }

        .line {
            width: 100px;
            height: 2px;
            background: #ff4500;
            margin: 20px 0;
            animation: scaleLine 1.5s forwards;
        }

        .subtitle {
            font-size: 1.2rem;
            color: #888;
            letter-spacing: 3px;
            margin-bottom: 50px;
            max-width: 600px;
        }

        /* Kart Yapısı */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            width: 100%;
            max-width: 1100px;
            padding: 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 40px;
            border-radius: 2px; /* Keskin köşeler daha profesyonel durur */
            cursor: pointer;
            transition: all 0.5s cubic-bezier(0.2, 1, 0.3, 1);
            position: relative;
        }

        .card:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-5px);
        }

        .card h2 {
            font-family: 'Syncopate', sans-serif;
            font-size: 1rem;
            letter-spacing: 4px;
            margin-bottom: 15px;
            color: #fff;
        }

        .card p {
            color: #555;
            font-size: 0.9rem;
            line-height: 1.6;
            transition: 0.3s;
        }

        .card:hover p {
            color: #aaa;
        }

        /* Animasyonlar */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes scaleLine {
            from { width: 0; }
            to { width: 100px; }
        }

        /* Alt Bilgi */
        footer {
            position: absolute;
            bottom: 30px;
            font-size: 0.7rem;
            letter-spacing: 2px;
            color: #333;
            text-transform: uppercase;
        }

    </style>
</head>
<body>
    <div class="bg-glow"></div>

    <section class="hero">
        <h1>CANO STUDIO</h1>
        <div class="line"></div>
        <p class="subtitle">GELECEĞİN DİJİTAL DÜNYASINI İNŞA EDİYORUZ</p>

        <div class="grid">
            <div class="card">
                <h2>PROJECTS</h2>
                <p>Geliştirdiğimiz oyunlar ve interaktif deneyimler kütüphanesi.</p>
            </div>
            <div class="card">
                <h2>LAB</h2>
                <p>Yeni teknolojiler, deneysel kodlar ve Ar-Ge çalışmaları.</p>
            </div>
            <div class="card">
                <h2>ABOUT</h2>
                <p>Vizyonumuz ve ekibimiz hakkında merak edilenler.</p>
            </div>
        </div>

        <footer>© 2026 EST. BY CANO</footer>
    </section>
</body>
</html>
"""

@app.route('/')
def home():
    return ana_sayfa_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
