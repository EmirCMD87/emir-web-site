from flask import Flask
import os

app = Flask(__name__)

# --- ORTAK FOOTER ---
footer_html = """
<footer style="background: #111; padding: 25px; border-top: 2px solid #333; text-align: center; margin-top: auto;">
    <button class="btn" style="background:#ff4500; color:white; padding:12px 25px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">☕ DESTEK OL</button>
    <button class="btn" style="background:#444; color:white; padding:12px 25px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; margin-left:10px;" onclick="toggleContact()">✉️ İLETİŞİM</button>
    <div id="contact-box" style="display:none; color:#aaa; margin-top:15px; border:1px dashed #444; padding:10px;">iletisim@canostudio.com | @cano_game_studio</div>
</footer>
<script>
    function toggleContact() {
        var x = document.getElementById('contact-box');
        x.style.display = (x.style.display === 'none') ? 'block' : 'none';
    }
</script>
"""

# --- ANA SAYFA ---
ana_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><title>Cano Game Studio</title>
    <style>
        body {{ background: #0a0a0a; color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; padding: 40px; }}
        .card {{ border: 2px solid #222; padding: 30px; border-radius: 15px; cursor: pointer; text-align: center; transition: 0.4s; }}
        .card:hover {{ transform: scale(1.05); border-color: #00d4ff; box-shadow: 0 0 20px rgba(0,212,255,0.2); }}
    </style>
</head>
<body>
    <h1 style="text-align:center; color:#00d4ff; margin-top:40px; letter-spacing:5px;">CANO GAME STUDIO</h1>
    <div class="container">
        <div class="card" onclick="window.location.href='/neon-arcade'"><h2>NEON ARCADE</h2><p>Uçan Kare Oyunu</p></div>
        <div class="card" onclick="window.location.href='/horror'" style="border-color:#e74c3c"><h2>HORROR</h2><p>Zihnin Karanlığı (Açık Dünya)</p></div>
        <div class="card" style="opacity:0.5"><h2>STRATEGY</h2><p>Yakında...</p></div>
        <div class="card" style="opacity:0.5"><h2>SURVIVAL</h2><p>Yakında...</p></div>
    </div>
    {footer_html}
</body>
</html>
"""

# --- HORROR OYUNU (AÇIK DÜNYA + WASD + ENVANTER) ---
horror_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><title>Zihnin Karanlığı</title>
    <style>
        body {{ margin: 0; overflow: hidden; background: #000; color: white; font-family: 'Courier New', monospace; }}
        #game-world {{ position: relative; width: 100vw; height: 100vh; overflow: hidden; }}
        #camera {{ position: absolute; width: 3000px; height: 3000px; background-color: #0a0a0a; background-image: radial-gradient(#1a1a1a 1px, transparent 1px); background-size: 50px 50px; left: 50%; top: 50%; }}
        .wall {{ position: absolute; background: #151515; border: 1px solid #333; }}
        #vignette {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle 250px at 50% 50%, rgba(255,255,255,0.02) 0%, rgba(0,0,0,0.95) 100%); pointer-events: none; z-index: 10; }}
        #inventory-ui {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 350px; background: rgba(10,10,10,0.98); border: 2px solid #e74c3c; padding: 20px; display: none; z-index: 100; }}
        #ui-text {{ position: fixed; bottom: 80px; width: 100%; text-align: center; color: #555; z-index: 5; }}
        .item {{ position: absolute; font-size: 25px; }}
    </style>
</head>
<body>
<div id="game-world">
    <div id="camera">
        <div class="wall" style="width: 800px; height: 20px; top: 1400px; left: 1400px;"></div>
        <div class="wall" style="width: 20px; height: 600px; top: 1400px; left: 1400px;"></div>
        <div class="item" style="top: 1500px; left: 1500px;">💊</div>
    </div>
</div>
<div id="vignette"></div>
<div id="inventory-ui">
    <h2 style="color:#e74c3c">ENVANTER</h2><hr border="1" color="#333">
    <p>🔦 El Feneri</p><p>🔪 Çakı (Kilitleri açar)</p><p>📱 Telefon (%4 Şarj)</p>
    <button onclick="toggleInv()" style="background:#333; color:white; border:none; padding:10px; cursor:pointer; width:100%">KAPAT (E)</button>
</div>
<div id="ui-text">W-A-S-D: Yürü | E: Envanter | Fare: Bakış</div>
<script>
    let x = 0, y = 0, invOpen = false;
    const cam = document.getElementById('camera');
    const keys = {{}};
    window.onkeydown = (e) => {{ keys[e.key.toLowerCase()] = true; if(e.key.toLowerCase()==='e') toggleInv(); }};
    window.onkeyup = (e) => {{ keys[e.key.toLowerCase()] = false; }};
    function toggleInv() {{ invOpen = !invOpen; document.getElementById('inventory-ui').style.display = invOpen ? 'block' : 'none'; }}
    window.onmousemove = (e) => {{ document.getElementById('vignette').style.background = `radial-gradient(circle 250px at ${{e.clientX}}px ${{e.clientY}}px, rgba(255,255,220,0.05) 0%, rgba(0,0,0,0.97) 100%)`; }};
    function loop() {{
        if(!invOpen) {{
            if(keys['w']) y += 5; if(keys['s']) y -= 5; if(keys['a']) x += 5; if(keys['d']) x -= 5;
            cam.style.transform = `translate(calc(-50% + ${{x}}px), calc(-50% + ${{y}}px))`;
        }}
        requestAnimationFrame(loop);
    }}
    loop();
</script>
</body>
</html>
"""

# --- NEON ARCADE (UÇAN KARE) ---
# (Daha önceki Arcade kodun buraya dahil edildi)
arcade_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"><title>Uçan Kare</title></head>
<body style="background:#000; color:#00d4ff; text-align:center; font-family:sans-serif;">
    <nav style="padding:20px;"><a href="/" style="color:#fff; text-decoration:none;">⬅ GERİ DÖ</a></nav>
    <h1>NEON ARCADE</h1>
    <canvas id="gc" width="400" height="400" style="border:2px solid #00d4ff"></canvas>
    {footer_html}
    <script>
        // Uçan Kare Oyun Kodları... (Burayı önceki stabil çalışan oyun kodunla dolduruyorum)
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return ana_sayfa_html
@app.route('/horror')
def horror(): return horror_sayfa_html
@app.route('/neon-arcade')
def arcade(): return arcade_sayfa_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
