from flask import Flask
import os

app = Flask(__name__)

# --- ANA SAYFA ŞABLONU (DEĞİŞTİRİLEMEZ İHTİŞAMLI TASARIM) ---
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
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        .bg-glow {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #050505 100%);
            z-index: -1;
        }

        .hero {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 80px 20px;
        }

        h1 {
            font-family: 'Syncopate', sans-serif;
            font-size: clamp(2.5rem, 8vw, 5rem);
            font-weight: 700;
            letter-spacing: 15px;
            text-transform: uppercase;
            background: linear-gradient(to bottom, #fff 30%, #444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }

        .line {
            width: 100px;
            height: 2px;
            background: #ff4500;
            margin: 20px 0;
        }

        .subtitle {
            font-size: 1rem;
            color: #666;
            letter-spacing: 4px;
            margin-bottom: 60px;
            text-transform: uppercase;
        }

        /* KÜTÜPHANE GRID SİSTEMİ */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            width: 100%;
            max-width: 1200px;
            padding: 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 50px 30px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.4s ease;
            position: relative;
            text-decoration: none;
        }

        .card:hover {
            background: rgba(255, 255, 255, 0.03);
            border-color: #ff4500;
            transform: translateY(-10px);
        }

        .card h2 {
            font-family: 'Syncopate', sans-serif;
            font-size: 1.1rem;
            letter-spacing: 3px;
            margin-bottom: 15px;
            color: #fff;
            transition: 0.3s;
        }

        .card:hover h2 {
            color: #ff4500;
        }

        .card p {
            color: #444;
            font-size: 0.85rem;
            line-height: 1.6;
            letter-spacing: 1px;
        }

        .card:hover p {
            color: #888;
        }

        footer {
            padding: 40px;
            font-size: 0.7rem;
            letter-spacing: 3px;
            color: #222;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="bg-glow"></div>

    <section class="hero">
        <h1>CANO STUDIO</h1>
        <div class="line"></div>
        <p class="subtitle">Kütüphane Portalı</p>

        <div class="grid">
            <a href="/neon-arcade" class="card">
                <h2>NEON ARCADE</h2>
                <p>Yüksek tempo, neon ışıklar ve bitmeyen bir aksiyon. Reflekslerini hazırla.</p>
            </a>

            <a href="/strateji" class="card">
                <h2>STRATEJI</h2>
                <p>Zeka ve planlama. Kendi dünyanı kur ve imparatorluğunu yönet.</p>
            </a>

            <a href="/horror" class="card">
                <h2>HORROR</h2>
                <p>Karanlığın derinliklerine yolculuk. Cesaretin varsa içeri gir.</p>
            </a>
        </div>
    </section>

    <footer>© 2026 DESIGNED BY CANO STUDIO</footer>
</body>
</html>
"""

@app.route('/')
def home():
    return ana_sayfa_html

@app.route('/neon-arcade')
def arcade():
    return "<body style='background:#000;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;'><h1>Neon Arcade Kütüphanesi Çok Yakında</h1></body>"

@app.route('/strateji')
def strateji():
    return "<body style='background:#000;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;'><h1>Strateji Kütüphanesi Çok Yakında</h1></body>"

@app.route('/horror')
def horror():
    return "<body style='background:#000;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;'><h1>Horror Kütüphanesi Çok Yakında</h1></body>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
