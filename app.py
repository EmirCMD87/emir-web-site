from flask import Flask

app = Flask(__name__)

# Burası senin ana üssün
html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Game Studio | Ana Üs</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #121212; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
        
        /* Üst Menü */
        nav { background: #1f1f1f; padding: 20px; text-align: center; border-bottom: 3px solid #7289da; }
        h1 { font-size: 2.5em; letter-spacing: 2px; }

        /* Oyun Galerisi */
        .container { padding: 40px; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        
        .oyun-kart {
            background: #1f1f1f;
            border-radius: 15px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid #333;
        }

        .oyun-kart:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 30px rgba(114, 137, 218, 0.4);
            border-color: #7289da;
        }

        .oyun-resim { height: 180px; background: #333; display: flex; align-items: center; justify-content: center; font-size: 4em; }
        .oyun-detay { padding: 20px; }
        .btn { 
            display: inline-block; background: #7289da; color: white; padding: 10px 20px; 
            text-decoration: none; border-radius: 5px; margin-top: 15px; font-weight: bold;
        }
    </style>
</head>
<body>

<nav>
    <h1>CANO GAME STUDIO</h1>
    <p>Kendi dünyalarımı inşa ediyorum.</p>
</nav>

<div class="container">
    <div class="oyun-kart">
        <div class="oyun-resim">🎮</div>
        <div class="oyun-detay">
            <h3>Proje: Alpha</h3>
            <p>Sıfırdan başladığım ilk büyük oyun projem.</p>
            <a href="#" class="btn">GELİŞTİRİLİYOR</a>
        </div>
    </div>

    <div class="oyun-kart">
        <div class="oyun-resim">🚀</div>
        <div class="oyun-detay">
            <h3>Uzay Macerası</h3>
            <p>Henüz fikir aşamasında olan bir hayatta kalma oyunu.</p>
            <a href="#" class="btn" style="background: #444;">YAKINDA</a>
        </div>
    </div>

    <div class="oyun-kart" style="border: 2px dashed #444; background: transparent;">
        <div class="oyun-resim" style="background: transparent;">+</div>
        <div class="oyun-detay" style="text-align: center;">
            <h3>Yeni Proje Ekle</h3>
            <p>Buraya yeni bir oyun fikri gelecek.</p>
        </div>
    </div>
</div>

</body>
</html>
"""

@app.route('/')
def ana_sayfa():
    return html_icerik

if __name__ == '__main__':

    app.run(debug=True)
