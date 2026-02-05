from flask import Flask
import os

app = Flask(__name__)

# --- ANA SAYFA (MAĞAZA VE XP SİSTEMİ EKLENDİ) ---
ana_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cano Studio | XP & Store</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;500&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; touch-action: manipulation; }
        body { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #050505 100%); z-index: -1; }
        
        /* XP BAR */
        .xp-container { position: fixed; top: 20px; right: 20px; background: rgba(255,69,0,0.1); border: 1px solid #ff4500; padding: 10px 20px; border-radius: 50px; z-index: 100; display: flex; align-items: center; gap: 10px; }
        .xp-val { color: #ff4500; font-weight: bold; font-family: 'Syncopate'; }

        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 60px 20px; }
        h1 { font-family: 'Syncopate', sans-serif; font-size: clamp(1.5rem, 6vw, 4rem); letter-spacing: 10px; text-transform: uppercase; margin-bottom: 40px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; width: 100%; max-width: 1100px; margin-bottom: 50px; }
        .card { background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 4px; cursor: pointer; transition: 0.3s; text-decoration: none; }
        .card:hover { border-color: #ff4500; transform: translateY(-5px); }
        .card h2 { font-family: 'Syncopate'; font-size: 0.8rem; color: #fff; margin-bottom: 10px; }

        /* MAĞAZA STİLİ */
        .store-section { width: 100%; max-width: 1000px; margin-top: 50px; border-top: 1px solid #111; padding-top: 50px; }
        .store-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 30px; }
        .store-item { background: #0a0a0a; border: 1px solid #222; padding: 20px; border-radius: 4px; text-align: center; }
        .store-item.owned { border-color: #00d4ff; opacity: 0.7; }
        .price { color: #ff4500; font-size: 0.9rem; margin: 10px 0; font-family: 'Syncopate'; }
        .buy-btn { background: #ff4500; border: none; padding: 10px 20px; color: #fff; cursor: pointer; border-radius: 2px; width: 100%; }
        .buy-btn:disabled { background: #333; cursor: not-allowed; }

        footer { padding: 40px; font-size: 0.6rem; color: #222; text-align: center; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="xp-container">
        <span style="font-size: 0.7rem; letter-spacing: 1px;">TOTAL XP:</span>
        <span class="xp-val" id="totalXP">0</span>
    </div>

    <section class="hero">
        <h1>CANO STUDIO</h1>
        <div class="grid">
            <a href="/neon-arcade" class="card"><h2>NEON ARCADE</h2><p>Puan = XP</p></a>
            <a href="/strateji" class="card"><h2>STRATEJI</h2><p>Level = XP</p></a>
            <a href="/horror" class="card"><h2>HORROR</h2><p>Yeni: Seçimli Hikaye</p></a>
        </div>

        <div class="store-section">
            <h2 style="font-family:'Syncopate'; letter-spacing:5px; font-size:1.2rem;">MAĞAZA (STORE)</h2>
            <div class="store-grid">
                <div class="store-item" id="item1">
                    <h3>ALTIN KARE</h3>
                    <p style="font-size:0.7rem; color:#444;">Arcade için özel skin</p>
                    <div class="price">500 XP</div>
                    <button class="buy-btn" onclick="buyItem('item1', 500)">SATIN AL</button>
                </div>
                <div class="store-item" id="item2">
                    <h3>NEON MAVİ</h3>
                    <p style="font-size:0.7rem; color:#444;">Strateji Gezegen Rengi</p>
                    <div class="price">1000 XP</div>
                    <button class="buy-btn" onclick="buyItem('item2', 1000)">SATIN AL</button>
                </div>
            </div>
        </div>
        <footer>© 2026 DESIGNED BY CANO</footer>
    </section>

    <script>
        // XP ve Mağaza Mantığı
        let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
        let ownedItems = JSON.parse(localStorage.getItem('cano_items')) || [];

        function updateUI() {
            document.getElementById('totalXP').innerText = xp;
            ownedItems.forEach(id => {
                const el = document.getElementById(id);
                if(el) {
                    el.classList.add('owned');
                    el.querySelector('button').innerText = "SAHİPSİN";
                    el.querySelector('button').disabled = true;
                }
            });
        }

        function buyItem(id, price) {
            if(xp >= price) {
                xp -= price;
                ownedItems.push(id);
                localStorage.setItem('cano_xp', xp);
                localStorage.setItem('cano_items', JSON.stringify(ownedItems));
                updateUI();
                alert("Başarıyla satın alındı!");
            } else {
                alert("Yetersiz XP!");
            }
        }

        updateUI();
    </script>
</body>
</html>
"""

# --- OYUN: NEON ARCADE (XP KAZANDIRAN) ---
arcade_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { touch-action: manipulation; }
        body { background: #000; margin: 0; overflow: hidden; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        canvas { border: 2px solid #ff4500; background: #050505; max-width: 90vw; }
        .back { position: fixed; bottom: 20px; color: #444; text-decoration: none; }
    </style>
</head>
<body>
    <div style="position:fixed; top:20px; color:#ff4500; font-size:1.5rem;" id="sc">0</div>
    <canvas id="gc" width="400" height="500"></canvas>
    <a href="/" class="back">← PORTALA DÖN</a>
    <script>
        const canvas = document.getElementById("gc"); const ctx = canvas.getContext("2d");
        let bird = { y: 250, v: 0, g: 0.5, jump: -8 };
        let pipes = []; let frames = 0; let score = 0;
        
        function draw() {
            ctx.fillStyle = "#050505"; ctx.fillRect(0,0,400,500);
            bird.v += bird.g; bird.y += bird.v;
            // EĞER ALTIN KARE SATIN ALINDI MI?
            let items = JSON.parse(localStorage.getItem('cano_items')) || [];
            ctx.fillStyle = items.includes('item1') ? "#FFD700" : "#fff";
            ctx.fillRect(60, bird.y, 25, 25);
            
            if(frames%100===0) pipes.push({x:400, h:Math.random()*250+50, gap:160});
            for(let i=pipes.length-1; i>=0; i--) {
                pipes[i].x -= 3;
                ctx.fillStyle = "#111"; ctx.fillRect(pipes[i].x, 0, 50, pipes[i].h);
                ctx.fillRect(pipes[i].x, pipes[i].h+160, 50, 500);
                if(60+25 > pipes[i].x && 60 < pipes[i].x+50 && (bird.y < pipes[i].h || bird.y+25 > pipes[i].h+160)) reset();
                if(pipes[i].x === 58) { score++; document.getElementById("sc").innerText = score; addXP(10); }
                if(pipes[i].x < -50) pipes.splice(i,1);
            }
            if(bird.y > 500 || bird.y < 0) reset();
            frames++; requestAnimationFrame(draw);
        }
        function addXP(amt) {
            let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
            localStorage.setItem('cano_xp', xp + amt);
        }
        function reset() { bird.y=250; bird.v=0; pipes=[]; score=0; document.getElementById("sc").innerText="0"; }
        canvas.addEventListener("touchstart", (e) => { bird.v = bird.jump; e.preventDefault(); });
        canvas.addEventListener("mousedown", () => bird.v = bird.jump);
        draw();
    </script>
</body>
</html>
"""

# --- OYUN: SEÇİMLİ KORKU (HORROR PREVIEW) ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Horror | Cano Studio</title>
    <style>
        body { background: #000; color: #600; font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; padding: 20px; }
        .game-box { max-width: 600px; text-align: center; border: 1px solid #200; padding: 40px; }
        h2 { letter-spacing: 5px; color: #900; }
        .text { color: #888; margin: 30px 0; line-height: 1.6; min-height: 100px; }
        .choices { display: flex; flex-direction: column; gap: 10px; }
        button { background: #100; border: 1px solid #300; color: #888; padding: 15px; cursor: pointer; transition: 0.3s; text-transform: uppercase; letter-spacing: 2px; }
        button:hover { background: #300; color: #fff; }
    </style>
</head>
<body>
    <div class="game-box">
        <h2 id="title">ORMAN YOLU</h2>
        <p class="text" id="story">Gecenin bir yarısı, arabanın benzini bitti. Karşında karanlık bir orman yolu ve terk edilmiş bir kulübe var...</p>
        <div class="choices" id="choices">
            <button onclick="nextStep(1)">Kulübeye Gir</button>
            <button onclick="nextStep(2)">Ormana Doğru Yürü</button>
        </div>
    </div>

    <script>
        const story = {
            1: { t: "KULÜBE", s: "İçerisi küf kokuyor. Masanın üzerinde hala dumanı tüten bir çay var... Ama kimse yok.", c: [{t: "Çayı iç", n: 3}, {t: "Kaç", n: 0}] },
            2: { t: "ORMAN", s: "Ağaçların arasından fısıltılar geliyor. Arkanda bir dal kırılma sesi duydun!", c: [{t: "Arkanı dön", n: 4}, {t: "Koş!", n: 5}] },
            0: { t: "KORKAK", s: "Korkuna yenik düştün ve arabaya geri döndün. Oyun bitti.", c: [{t: "Yeniden Başla", n: 'reset'}] }
        };

        function nextStep(n) {
            if(n === 'reset') location.reload();
            const step = story[n];
            if(!step) {
                document.getElementById('story').innerText = "Karanlık seni yuttu... (XP Kazandın: 50)";
                addXP(50);
                document.getElementById('choices').innerHTML = '<button onclick="location.reload()">BAŞA DÖN</button>';
                return;
            }
            document.getElementById('title').innerText = step.t;
            document.getElementById('story').innerText = step.s;
            let btnHtml = "";
            step.c.forEach(choice => {
                btnHtml += `<button onclick="nextStep(${choice.n})">${choice.t}</button>`;
            });
            document.getElementById('choices').innerHTML = btnHtml;
        }

        function addXP(amt) {
            let xp = parseInt(localStorage.getItem('cano_xp')) || 0;
            localStorage.setItem('cano_xp', xp + amt);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return ana_sayfa_html

@app.route('/neon-arcade')
def arcade(): return arcade_html

@app.route('/strateji')
def strateji(): return "<h1>Strateji Koduna XP ekleniyor...</h1>" # Önceki mesajdaki koda addXP ekleyerek kullanabilirsin

@app.route('/horror')
def horror(): return horror_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
