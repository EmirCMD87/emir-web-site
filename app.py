from flask import Flask
import os

app = Flask(__name__)

# ============ ORTAK CSS (Neon Teması) ============
base_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
:root { --neon-orange: #ff4500; --neon-blue: #00d4ff; --neon-purple: #bf00ff; --neon-green: #00ff88; --dark-bg: #050505; }
* { margin: 0; padding: 0; box-sizing: border-box; touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
body { background: var(--dark-bg); color: #fff; font-family: 'Rajdhani', sans-serif; overflow-x: hidden; min-height: 100vh; }

/* Parçacık arka plan */
#particles { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }

/* XP Göstergesi */
.xp-container {
    position: fixed; top: 20px; right: 20px;
    background: rgba(255,69,0,0.15);
    border: 1px solid var(--neon-orange);
    padding: 10px 20px; border-radius: 50px;
    z-index: 1000; backdrop-filter: blur(10px);
    display: flex; align-items: center; gap: 8px;
}
.xp-val { color: var(--neon-orange); font-weight: 900; font-size: 1.1rem; font-family: 'Orbitron'; }
.xp-label { color: #aaa; font-size: 0.8rem; }

/* Seviye göstergesi */
.level-badge {
    position: fixed; top: 20px; left: 20px;
    background: rgba(0,212,255,0.15);
    border: 1px solid var(--neon-blue);
    padding: 10px 20px; border-radius: 50px;
    z-index: 1000; backdrop-filter: blur(10px);
    font-family: 'Orbitron'; font-size: 0.85rem; color: var(--neon-blue);
}

/* Genel buton */
.btn {
    background: linear-gradient(135deg, var(--neon-orange), #ff6b35);
    color: #fff; border: none; padding: 12px 28px;
    font-family: 'Orbitron'; font-size: 0.85rem;
    cursor: pointer; border-radius: 8px;
    transition: all 0.3s; letter-spacing: 1px;
}
.btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(255,69,0,0.5); }
.btn:active { transform: scale(0.97); }
.btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

.btn-blue {
    background: linear-gradient(135deg, var(--neon-blue), #0099cc);
}
.btn-blue:hover { box-shadow: 0 8px 25px rgba(0,212,255,0.5); }

.btn-purple {
    background: linear-gradient(135deg, var(--neon-purple), #8800cc);
}
.btn-purple:hover { box-shadow: 0 8px 25px rgba(191,0,255,0.5); }

/* Geri butonu */
.back-btn {
    position: fixed; bottom: 30px; left: 30px;
    color: #666; text-decoration: none;
    font-family: 'Orbitron'; font-size: 0.8rem;
    z-index: 100; transition: color 0.3s;
    padding: 10px 20px; border: 1px solid #333; border-radius: 50px;
}
.back-btn:hover { color: var(--neon-orange); border-color: var(--neon-orange); }

/* XP kazanma animasyonu */
@keyframes xpPop {
    0% { transform: scale(1); }
    50% { transform: scale(1.3); color: #fff; }
    100% { transform: scale(1); }
}
.xp-anim { animation: xpPop 0.4s ease; }

/* Bildirim toast */
.toast {
    position: fixed; bottom: 80px; right: 20px;
    background: rgba(0,255,136,0.15);
    border: 1px solid var(--neon-green);
    color: var(--neon-green);
    padding: 12px 20px; border-radius: 10px;
    font-family: 'Orbitron'; font-size: 0.75rem;
    z-index: 9999; opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}
.toast.show { opacity: 1; }
"""

# ============ ORTAK JS ============
base_js = """
function getXP() { return parseInt(localStorage.getItem('cano_xp')) || 0; }
function setXP(v) { localStorage.setItem('cano_xp', v); updateXPDisplay(); }
function addXP(amount, label) {
    let xp = getXP() + amount;
    setXP(xp);
    showToast("+" + amount + " XP — " + (label || ""));
    let el = document.getElementById('xpVal');
    if(el) { el.classList.remove('xp-anim'); void el.offsetWidth; el.classList.add('xp-anim'); }
}
function updateXPDisplay() {
    let xp = getXP();
    let el = document.getElementById('xpVal');
    if(el) el.innerText = xp.toLocaleString();
    let lvlEl = document.getElementById('levelBadge');
    if(lvlEl) lvlEl.innerText = "SEV " + Math.floor(xp / 500 + 1);
}
function showToast(msg) {
    let t = document.getElementById('toast');
    if(!t) return;
    t.innerText = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
}
function getItems() { return JSON.parse(localStorage.getItem('cano_items')) || []; }
window.onload = updateXPDisplay;
"""

# ============ PARÇACIK JS ============
particles_js = """
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth; canvas.height = window.innerHeight;
window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
const pts = Array.from({length: 60}, () => ({
    x: Math.random()*canvas.width, y: Math.random()*canvas.height,
    vx: (Math.random()-0.5)*0.5, vy: (Math.random()-0.5)*0.5,
    r: Math.random()*2+0.5,
    c: ['#ff4500','#00d4ff','#bf00ff'][Math.floor(Math.random()*3)]
}));
function drawPts() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    pts.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if(p.x<0||p.x>canvas.width) p.vx*=-1;
        if(p.y<0||p.y>canvas.height) p.vy*=-1;
        ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fillStyle = p.c; ctx.fill();
    });
    requestAnimationFrame(drawPts);
}
drawPts();
"""

# ============ 1. ANA SAYFA ============
ana_sayfa_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CANO STUDIO | PORTAL</title>
    <style>{base_css}
    .hero {{
        min-height: 100vh; display: flex; flex-direction: column;
        align-items: center; justify-content: center; text-align: center;
        padding: 20px;
    }}
    .logo {{
        font-family: 'Orbitron'; font-size: clamp(2rem, 6vw, 4rem);
        font-weight: 900; letter-spacing: 4px;
        background: linear-gradient(90deg, var(--neon-orange), var(--neon-blue));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }}
    .tagline {{ color: #666; font-size: 0.9rem; letter-spacing: 3px; margin-bottom: 60px; }}
    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px; width: 90%; max-width: 1000px;
    }}
    .card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 30px 20px; border-radius: 16px;
        text-decoration: none; color: #fff;
        transition: all 0.3s; cursor: pointer;
        position: relative; overflow: hidden;
    }}
    .card::before {{
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(circle at 50% 0%, rgba(255,69,0,0.1), transparent 70%);
        opacity: 0; transition: opacity 0.3s;
    }}
    .card:hover {{ border-color: var(--neon-orange); transform: translateY(-6px); background: rgba(255,69,0,0.08); }}
    .card:hover::before {{ opacity: 1; }}
    .card-icon {{ font-size: 2.5rem; margin-bottom: 12px; display: block; }}
    .card h2 {{ font-family: 'Orbitron'; font-size: 1rem; margin-bottom: 6px; letter-spacing: 2px; }}
    .card p {{ color: #888; font-size: 0.85rem; }}
    .card.blue {{ border-color: rgba(0,212,255,0.3); }}
    .card.blue:hover {{ border-color: var(--neon-blue); background: rgba(0,212,255,0.08); }}
    .stats-bar {{
        display: flex; gap: 30px; margin-bottom: 40px;
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
        padding: 16px 30px; border-radius: 12px;
    }}
    .stat {{ text-align: center; }}
    .stat-val {{ font-family: 'Orbitron'; font-size: 1.2rem; color: var(--neon-orange); }}
    .stat-lbl {{ font-size: 0.7rem; color: #666; letter-spacing: 2px; }}
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    <div class="xp-container">
        <span class="xp-val" id="xpVal">0</span>
        <span class="xp-label">XP</span>
    </div>
    <div class="level-badge" id="levelBadge">SEV 1</div>
    <div id="toast" class="toast"></div>

    <section class="hero">
        <div class="logo">CANO STUDIO</div>
        <div class="tagline">OYUN · STRATEJI · KORKU · MARKET</div>

        <div class="stats-bar">
            <div class="stat"><div class="stat-val" id="statXP">0</div><div class="stat-lbl">TOPLAM XP</div></div>
            <div class="stat"><div class="stat-val" id="statLvl">1</div><div class="stat-lbl">SEVİYE</div></div>
            <div class="stat"><div class="stat-val" id="statItems">0</div><div class="stat-lbl">EŞYA</div></div>
        </div>

        <div class="grid">
            <a href="/neon-arcade" class="card">
                <span class="card-icon">🎮</span>
                <h2>ARCADE</h2>
                <p>Hız ve Refleks</p>
            </a>
            <a href="/strateji" class="card">
                <span class="card-icon">🌍</span>
                <h2>STRATEJİ</h2>
                <p>Gezegen Yönetimi</p>
            </a>
            <a href="/horror" class="card">
                <span class="card-icon">👻</span>
                <h2>HORROR</h2>
                <p>Korku Hikayesi</p>
            </a>
            <a href="/store" class="card blue">
                <span class="card-icon">🛒</span>
                <h2>MARKET</h2>
                <p>XP Harca</p>
            </a>
        </div>
    </section>

    <script>
        {base_js}
        {particles_js}
        window.onload = function() {{
            updateXPDisplay();
            document.getElementById('statXP').innerText = getXP().toLocaleString();
            document.getElementById('statLvl').innerText = Math.floor(getXP() / 500 + 1);
            document.getElementById('statItems').innerText = getItems().length;
        }};
    </script>
</body>
</html>"""

# ============ 2. STRATEJİ OYUNU ============
strateji_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>STRATEJİ | Cano Studio</title>
    <style>{base_css}
    .game-wrap {{
        min-height: 100vh; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        text-align: center; padding: 80px 20px;
    }}
    h1 {{ font-family: 'Orbitron'; font-size: clamp(1.2rem, 4vw, 2rem); margin-bottom: 8px; color: var(--neon-blue); }}
    .subtitle {{ color: #555; font-size: 0.85rem; letter-spacing: 2px; margin-bottom: 30px; }}

    .planet-wrap {{ position: relative; width: 180px; height: 180px; margin: 0 auto 30px; }}
    .planet {{
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #00eeff, #003a6e);
        box-shadow: 0 0 60px rgba(0,212,255,0.6), 0 0 120px rgba(0,212,255,0.2);
        animation: spin 12s linear infinite;
        cursor: pointer; transition: transform 0.2s;
    }}
    .planet:hover {{ transform: scale(1.05); }}
    .planet:active {{ transform: scale(0.95); }}
    .planet-ring {{
        position: absolute; top: 50%; left: 50%;
        width: 240px; height: 60px;
        border: 2px solid rgba(0,212,255,0.3);
        border-radius: 50%; transform: translate(-50%,-50%) rotateX(75deg);
        pointer-events: none;
    }}
    @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    .resources {{
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 15px; width: 100%; max-width: 500px; margin-bottom: 30px;
    }}
    .res-card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 15px 10px; border-radius: 12px;
    }}
    .res-icon {{ font-size: 1.5rem; }}
    .res-name {{ font-size: 0.7rem; color: #666; letter-spacing: 1px; margin-top: 4px; }}
    .res-val {{ font-family: 'Orbitron'; font-size: 1.1rem; color: #fff; margin-top: 4px; }}

    .actions {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-bottom: 20px; }}

    .progress-bar {{
        width: 100%; max-width: 400px;
        background: #111; border-radius: 50px; height: 8px;
        margin-bottom: 20px; overflow: hidden;
    }}
    .progress-fill {{
        height: 100%; border-radius: 50px;
        background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
        transition: width 0.5s; width: 0%;
    }}
    .level-info {{ color: #666; font-size: 0.8rem; margin-bottom: 30px; }}

    .upgrade-box {{
        background: rgba(191,0,255,0.08);
        border: 1px solid rgba(191,0,255,0.3);
        border-radius: 12px; padding: 20px;
        width: 100%; max-width: 500px; margin-bottom: 20px;
    }}
    .upgrade-box h3 {{ font-family: 'Orbitron'; color: var(--neon-purple); font-size: 0.85rem; margin-bottom: 12px; }}
    .upgrade-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    .upg-item {{ background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; text-align: left; }}
    .upg-name {{ font-size: 0.8rem; color: #aaa; }}
    .upg-cost {{ font-size: 0.75rem; color: var(--neon-purple); }}
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    <div class="xp-container"><span class="xp-val" id="xpVal">0</span><span class="xp-label">XP</span></div>
    <div class="level-badge" id="levelBadge">SEV 1</div>
    <div id="toast" class="toast"></div>

    <div class="game-wrap">
        <h1>GALAKTİK YÖNETİM</h1>
        <div class="subtitle">GEZEGENİNİ YÖNET · KAYNAK TOPLA · EVRENİ FETHET</div>

        <div class="planet-wrap">
            <div class="planet" id="planet" onclick="mine()" title="Tıkla — Maden Çıkar"></div>
            <div class="planet-ring"></div>
        </div>

        <div class="progress-bar"><div class="progress-fill" id="progBar"></div></div>
        <div class="level-info" id="lvlInfo">Gezegen Seviyesi: 1 · Sonraki seviye için 100 maden gerekli</div>

        <div class="resources">
            <div class="res-card"><div class="res-icon">⛏️</div><div class="res-name">MADEN</div><div class="res-val" id="rMaden">0</div></div>
            <div class="res-card"><div class="res-icon">⚡</div><div class="res-name">ENERJİ</div><div class="res-val" id="rEnerji">0</div></div>
            <div class="res-card"><div class="res-icon">💎</div><div class="res-name">KRİSTAL</div><div class="res-val" id="rKristal">0</div></div>
        </div>

        <div class="actions">
            <button class="btn" onclick="mine()">⛏️ MADEN (+10 XP)</button>
            <button class="btn btn-blue" onclick="generateEnergy()">⚡ ENERJİ (+5 XP)</button>
            <button class="btn btn-purple" id="crystalBtn" onclick="makeCrystal()" disabled>💎 KRİSTAL (50 Maden)</button>
        </div>

        <div class="upgrade-box">
            <h3>🔬 GELİŞTİRMELER</h3>
            <div class="upgrade-grid">
                <div class="upg-item">
                    <div class="upg-name">Maden Kazması x<span id="upMaden">1</span></div>
                    <div class="upg-cost">Maliyet: <span id="upMadenCost">100</span> XP</div>
                    <button class="btn" style="margin-top:8px;padding:6px 12px;font-size:0.7rem;" onclick="upgrade('maden')">YÜKSELT</button>
                </div>
                <div class="upg-item">
                    <div class="upg-name">Enerji Jeneratörü x<span id="upEnerji">1</span></div>
                    <div class="upg-cost">Maliyet: <span id="upEnerjiCost">150</span> XP</div>
                    <button class="btn btn-blue" style="margin-top:8px;padding:6px 12px;font-size:0.7rem;" onclick="upgrade('enerji')">YÜKSELT</button>
                </div>
            </div>
        </div>
    </div>

    <a href="/" class="back-btn">← GERİ</a>

    <script>
        {base_js}
        {particles_js}

        let state = JSON.parse(localStorage.getItem('cano_strateji')) || {{
            maden: 0, enerji: 0, kristal: 0,
            gezegenLvl: 1, gezegenXP: 0,
            upgMaden: 1, upgEnerji: 1,
            upgMadenCost: 100, upgEnerjiCost: 150
        }};

        function saveState() {{ localStorage.setItem('cano_strateji', JSON.stringify(state)); }}

        function render() {{
            document.getElementById('rMaden').innerText = state.maden;
            document.getElementById('rEnerji').innerText = state.enerji;
            document.getElementById('rKristal').innerText = state.kristal;
            document.getElementById('crystalBtn').disabled = state.maden < 50;
            document.getElementById('upMaden').innerText = state.upgMaden;
            document.getElementById('upEnerji').innerText = state.upgEnerji;
            document.getElementById('upMadenCost').innerText = state.upgMadenCost;
            document.getElementById('upEnerjiCost').innerText = state.upgEnerjiCost;
            let needed = state.gezegenLvl * 100;
            let pct = Math.min(100, (state.gezegenXP / needed) * 100);
            document.getElementById('progBar').style.width = pct + '%';
            document.getElementById('lvlInfo').innerText =
                'Gezegen Seviyesi: ' + state.gezegenLvl + ' · Sonraki seviye için ' + (needed - state.gezegenXP) + ' maden gerekli';
            updateXPDisplay();
        }}

        function mine() {{
            let gain = 10 * state.upgMaden;
            state.maden += state.upgMaden;
            state.gezegenXP += state.upgMaden;
            let needed = state.gezegenLvl * 100;
            if(state.gezegenXP >= needed) {{
                state.gezegenXP = 0; state.gezegenLvl++;
                showToast("🪐 GEZEGEN SEVİYE " + state.gezegenLvl + "!");
            }}
            addXP(gain, "Maden");
            saveState(); render();
        }}

        function generateEnergy() {{
            let gain = 5 * state.upgEnerji;
            state.enerji += state.upgEnerji;
            addXP(gain, "Enerji");
            saveState(); render();
        }}

        function makeCrystal() {{
            if(state.maden < 50) return;
            state.maden -= 50; state.kristal++;
            addXP(30, "Kristal");
            saveState(); render();
        }}

        function upgrade(type) {{
            let xp = getXP();
            if(type === 'maden') {{
                if(xp < state.upgMadenCost) {{ showToast("XP Yetersiz!"); return; }}
                setXP(xp - state.upgMadenCost);
                state.upgMaden++;
                state.upgMadenCost = Math.floor(state.upgMadenCost * 1.8);
            }} else {{
                if(xp < state.upgEnerjiCost) {{ showToast("XP Yetersiz!"); return; }}
                setXP(xp - state.upgEnerjiCost);
                state.upgEnerji++;
                state.upgEnerjiCost = Math.floor(state.upgEnerjiCost * 1.8);
            }}
            showToast("✅ Yükseltme Tamamlandı!");
            saveState(); render();
        }}

        window.onload = render;
    </script>
</body>
</html>"""

# ============ 3. ARCADE OYUNU ============
arcade_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ARCADE | Cano Studio</title>
    <style>{base_css}
    .arcade-wrap {{
        min-height: 100vh; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        padding: 80px 20px; text-align: center;
    }}
    h1 {{ font-family: 'Orbitron'; color: var(--neon-orange); font-size: clamp(1.2rem, 4vw, 2rem); margin-bottom: 6px; }}
    .subtitle {{ color: #555; font-size: 0.8rem; letter-spacing: 3px; margin-bottom: 30px; }}

    #gameCanvas {{
        border: 2px solid var(--neon-orange);
        border-radius: 12px;
        box-shadow: 0 0 40px rgba(255,69,0,0.4);
        background: #0a0a0a;
        max-width: 100%;
        touch-action: none;
    }}

    .hud {{
        display: flex; gap: 30px; margin-bottom: 16px;
        font-family: 'Orbitron'; font-size: 0.85rem;
    }}
    .hud-item span {{ color: var(--neon-orange); font-size: 1.2rem; }}

    .controls {{
        display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; justify-content: center;
    }}
    .d-pad {{
        display: grid; grid-template-columns: 1fr 1fr 1fr;
        gap: 6px; margin-top: 16px;
    }}
    .d-btn {{
        background: rgba(255,69,0,0.2); border: 1px solid var(--neon-orange);
        color: #fff; padding: 14px 18px; border-radius: 8px;
        font-size: 1.2rem; cursor: pointer; user-select: none;
        transition: background 0.1s;
    }}
    .d-btn:active {{ background: rgba(255,69,0,0.5); }}
    .d-empty {{ background: transparent; border: none; pointer-events: none; }}

    #overlay {{
        position: absolute; inset: 0;
        background: rgba(0,0,0,0.85);
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        border-radius: 10px;
        font-family: 'Orbitron';
    }}
    #overlay h2 {{ font-size: 1.5rem; color: var(--neon-orange); margin-bottom: 10px; }}
    #overlay p {{ color: #aaa; margin-bottom: 20px; font-size: 0.85rem; }}
    .canvas-wrap {{ position: relative; display: inline-block; }}
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    <div class="xp-container"><span class="xp-val" id="xpVal">0</span><span class="xp-label">XP</span></div>
    <div class="level-badge" id="levelBadge">SEV 1</div>
    <div id="toast" class="toast"></div>

    <div class="arcade-wrap">
        <h1>NEON ARCADE</h1>
        <div class="subtitle">REFLEKS OYUNU · OKÇU</div>

        <div class="hud">
            <div class="hud-item">SKOR: <span id="scoreVal">0</span></div>
            <div class="hud-item">CAN: <span id="livesVal">❤️❤️❤️</span></div>
            <div class="hud-item">DALGA: <span id="waveVal">1</span></div>
        </div>

        <div class="canvas-wrap">
            <canvas id="gameCanvas" width="420" height="360"></canvas>
            <div id="overlay">
                <h2>NEON ARCHER</h2>
                <p>Düşmanları vur, XP kazan!</p>
                <p style="font-size:0.75rem;color:#555;">← → hareket | SPACE ateş | Mobilde: d-pad</p>
                <button class="btn" onclick="startGame()">BAŞLAT</button>
            </div>
        </div>

        <div class="d-pad">
            <div class="d-empty"></div>
            <button class="d-btn" onpointerdown="keys.up=true" onpointerup="keys.up=false">▲</button>
            <div class="d-empty"></div>
            <button class="d-btn" onpointerdown="keys.left=true" onpointerup="keys.left=false">◀</button>
            <button class="d-btn" onpointerdown="keys.fire=true" onpointerup="keys.fire=false">🔥</button>
            <button class="d-btn" onpointerdown="keys.right=true" onpointerup="keys.right=false">▶</button>
        </div>
    </div>

    <a href="/" class="back-btn">← GERİ</a>

    <script>
        {base_js}
        {particles_js}

        const canvas = document.getElementById('gameCanvas');
        const ctx2 = canvas.getContext('2d');
        let gameRunning = false, score = 0, lives = 3, wave = 1;
        let player = {{ x: 200, y: 320, w: 32, h: 32, speed: 5 }};
        let bullets = [], enemies = [], particles2 = [];
        let keys = {{}};
        let lastBulletTime = 0, lastEnemySpawn = 0;
        let frameCount = 0;

        document.addEventListener('keydown', e => {{
            keys[e.code] = true;
            if(e.code === 'Space') e.preventDefault();
        }});
        document.addEventListener('keyup', e => {{ keys[e.code] = false; }});

        function startGame() {{
            document.getElementById('overlay').style.display = 'none';
            score = 0; lives = 3; wave = 1; bullets = []; enemies = []; particles2 = [];
            player.x = 200; gameRunning = true;
            gameLoop();
        }}

        function spawnEnemy() {{
            let types = ['basic','fast','tank'];
            let t = types[Math.floor(Math.random() * Math.min(wave, 3))];
            enemies.push({{
                x: Math.random() * 380 + 20,
                y: -20, w: 28, h: 28,
                hp: t==='tank'?3:1,
                speed: t==='fast'?3.5:(1.2 + wave*0.15),
                type: t, color: t==='tank'?'#ff0066':t==='fast'?'#00ff88':'#00d4ff'
            }});
        }}

        function gameLoop() {{
            if(!gameRunning) return;
            frameCount++;

            // Hareket
            if((keys['ArrowLeft']||keys['left']) && player.x > 16) player.x -= player.speed;
            if((keys['ArrowRight']||keys['right']) && player.x < canvas.width-16) player.x += player.speed;

            // Ateş
            let now = Date.now();
            if((keys['Space']||keys['fire']) && now - lastBulletTime > 220) {{
                bullets.push({{ x: player.x, y: player.y - 16, speed: 9, w: 4, h: 12 }});
                lastBulletTime = now;
            }}

            // Düşman spawn
            let spawnInterval = Math.max(600, 1400 - wave * 100);
            if(now - lastEnemySpawn > spawnInterval) {{
                spawnEnemy(); lastEnemySpawn = now;
                if(Math.random() < 0.3) spawnEnemy(); // çift spawn şansı
            }}

            // Güncelle
            bullets = bullets.filter(b => {{ b.y -= b.speed; return b.y > -20; }});

            enemies.forEach(e => {{ e.y += e.speed; }});

            // Çarpışma — kurşun × düşman
            bullets = bullets.filter(b => {{
                let hit = false;
                enemies = enemies.map(e => {{
                    if(!hit && b.x > e.x-14 && b.x < e.x+14 && b.y > e.y-14 && b.y < e.y+14) {{
                        e.hp--; hit = true;
                        if(e.hp <= 0) {{
                            e.dead = true;
                            score += e.type==='tank'?30:e.type==='fast'?15:10;
                            addXP(e.type==='tank'?30:e.type==='fast'?15:10, "Düşman");
                            for(let i=0;i<8;i++) particles2.push({{
                                x:e.x,y:e.y,vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*4,
                                life:25,color:e.color
                            }});
                        }}
                    }}
                    return e;
                }}).filter(e=>!e.dead);
                return !hit;
            }});

            // Düşman ekrana ulaşırsa can azalt
            enemies = enemies.filter(e => {{
                if(e.y > canvas.height + 10) {{
                    lives--;
                    if(lives <= 0) {{ gameOver(); }}
                    return false;
                }}
                return true;
            }});

            // Dalga ilerlemesi
            if(score > wave * 150) {{ wave++; showToast("🌊 DALGA " + wave + "!"); }}

            // Parçacıklar
            particles2 = particles2.filter(p => {{ p.x+=p.vx; p.y+=p.vy; p.life--; return p.life>0; }});

            // HUD güncelle
            document.getElementById('scoreVal').innerText = score;
            document.getElementById('livesVal').innerText = '❤️'.repeat(Math.max(0,lives));
            document.getElementById('waveVal').innerText = wave;

            // Çiz
            ctx2.clearRect(0, 0, canvas.width, canvas.height);

            // Grid arka plan
            ctx2.strokeStyle = 'rgba(255,69,0,0.05)';
            ctx2.lineWidth = 1;
            for(let i=0;i<canvas.width;i+=40) {{ ctx2.beginPath(); ctx2.moveTo(i,0); ctx2.lineTo(i,canvas.height); ctx2.stroke(); }}
            for(let i=0;i<canvas.height;i+=40) {{ ctx2.beginPath(); ctx2.moveTo(0,i); ctx2.lineTo(canvas.width,i); ctx2.stroke(); }}

            // Oyuncu
            ctx2.save();
            ctx2.translate(player.x, player.y);
            ctx2.fillStyle = '#ff4500';
            ctx2.shadowColor = '#ff4500'; ctx2.shadowBlur = 15;
            ctx2.beginPath(); ctx2.moveTo(0,-16); ctx2.lineTo(12,12); ctx2.lineTo(0,6); ctx2.lineTo(-12,12); ctx2.closePath(); ctx2.fill();
            ctx2.restore();

            // Kurşunlar
            bullets.forEach(b => {{
                ctx2.fillStyle = '#ffdd00';
                ctx2.shadowColor = '#ffdd00'; ctx2.shadowBlur = 8;
                ctx2.fillRect(b.x-2, b.y, b.w, b.h);
            }});

            // Düşmanlar
            enemies.forEach(e => {{
                ctx2.save();
                ctx2.translate(e.x, e.y);
                ctx2.fillStyle = e.color;
                ctx2.shadowColor = e.color; ctx2.shadowBlur = 12;
                if(e.type==='tank') {{
                    ctx2.fillRect(-14,-14,28,28);
                }} else if(e.type==='fast') {{
                    ctx2.beginPath(); ctx2.moveTo(0,14); ctx2.lineTo(12,-14); ctx2.lineTo(-12,-14); ctx2.closePath(); ctx2.fill();
                }} else {{
                    ctx2.beginPath(); ctx2.arc(0,0,14,0,Math.PI*2); ctx2.fill();
                }}
                // HP bar (tank için)
                if(e.type==='tank' && e.hp>0) {{
                    ctx2.fillStyle = '#333'; ctx2.fillRect(-14,16,28,4);
                    ctx2.fillStyle = '#ff0066'; ctx2.fillRect(-14,16,28*(e.hp/3),4);
                }}
                ctx2.restore();
            }});

            // Parçacıklar
            particles2.forEach(p => {{
                ctx2.globalAlpha = p.life/25;
                ctx2.fillStyle = p.color;
                ctx2.beginPath(); ctx2.arc(p.x,p.y,3,0,Math.PI*2); ctx2.fill();
            }});
            ctx2.globalAlpha = 1;

            requestAnimationFrame(gameLoop);
        }}

        function gameOver() {{
            gameRunning = false;
            let ov = document.getElementById('overlay');
            ov.style.display = 'flex';
            ov.innerHTML = '<h2>GAME OVER</h2><p>Skor: '+score+' · Dalga: '+wave+'</p><button class="btn" onclick="startGame()">TEKRAR OYNA</button>';
        }}

        window.onload = updateXPDisplay;
    </script>
</body>
</html>"""

# ============ 4. HORROR ============
horror_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>HORROR | Cano Studio</title>
    <style>{base_css}
    body {{ background: #000; }}
    .horror-wrap {{
        min-height: 100vh; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        padding: 80px 20px; text-align: center;
    }}
    h1 {{ font-family: 'Orbitron'; color: #cc0000; font-size: clamp(1.2rem, 4vw, 2rem);
          margin-bottom: 6px; text-shadow: 0 0 20px #cc0000; }}
    .subtitle {{ color: #400; font-size: 0.8rem; letter-spacing: 3px; margin-bottom: 30px; }}

    .story-box {{
        background: rgba(100,0,0,0.12);
        border: 1px solid rgba(200,0,0,0.3);
        border-radius: 16px; padding: 30px;
        width: 100%; max-width: 560px;
        margin-bottom: 24px; text-align: left;
        min-height: 200px;
        position: relative; overflow: hidden;
    }}
    .story-box::before {{
        content: ''; position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #cc0000, transparent);
        animation: scanline 3s linear infinite;
    }}
    @keyframes scanline {{ from {{ top: 0; }} to {{ top: 100%; }} }}

    .story-text {{
        color: #ccc; font-size: 1rem; line-height: 1.8;
        font-family: 'Rajdhani'; min-height: 80px;
    }}

    .choices {{ display: flex; flex-direction: column; gap: 12px; width: 100%; max-width: 560px; }}
    .choice-btn {{
        background: rgba(100,0,0,0.2);
        border: 1px solid rgba(200,0,0,0.3);
        color: #ccc; padding: 14px 20px;
        border-radius: 8px; cursor: pointer;
        font-family: 'Rajdhani'; font-size: 0.95rem;
        text-align: left; transition: all 0.2s;
    }}
    .choice-btn:hover {{ background: rgba(200,0,0,0.2); border-color: #cc0000; color: #fff; }}

    .stats-row {{
        display: flex; gap: 20px; margin-bottom: 20px;
        font-family: 'Orbitron'; font-size: 0.75rem;
    }}
    .h-stat {{ background: rgba(100,0,0,0.2); border: 1px solid rgba(200,0,0,0.3); padding: 8px 16px; border-radius: 8px; }}
    .h-stat span {{ color: #cc0000; }}

    .end-screen {{
        display: none; padding: 30px; text-align: center;
    }}
    .end-screen h2 {{ font-family: 'Orbitron'; color: #cc0000; font-size: 1.5rem; margin-bottom: 10px; }}
    .end-screen p {{ color: #888; margin-bottom: 20px; }}

    #scareFlash {{
        position: fixed; inset: 0; background: red;
        opacity: 0; pointer-events: none; z-index: 9999;
        transition: opacity 0.05s;
    }}
    </style>
</head>
<body>
    <div id="scareFlash"></div>
    <canvas id="particles"></canvas>
    <div class="xp-container"><span class="xp-val" id="xpVal">0</span><span class="xp-label">XP</span></div>
    <div class="level-badge" id="levelBadge">SEV 1</div>
    <div id="toast" class="toast"></div>

    <div class="horror-wrap">
        <h1>👻 KARANLIK EV</h1>
        <div class="subtitle">İNTERAKTİF KORKU HİKAYESİ</div>

        <div class="stats-row">
            <div class="h-stat">CAN: <span id="hpVal">❤️❤️❤️</span></div>
            <div class="h-stat">KOR KOR: <span id="fearVal">0</span>/100</div>
            <div class="h-stat">BÖLÜM: <span id="chapVal">1</span>/5</div>
        </div>

        <div class="story-box">
            <div class="story-text" id="storyText">Yükleniyor...</div>
        </div>

        <div class="choices" id="choicesBox"></div>

        <div class="end-screen" id="endScreen">
            <h2 id="endTitle"></h2>
            <p id="endDesc"></p>
            <button class="btn btn-purple" onclick="restartGame()">TEKRAR OYNA</button>
        </div>
    </div>

    <a href="/" class="back-btn">← GERİ</a>

    <script>
        {base_js}
        {particles_js}

        let hp = 3, fear = 0, chapter = 1;

        const story = [
            {{
                text: "Gece yarısı eski bir eve giriyorsun. Kapı ağır bir sesle kapanıyor arkandan. Uzakta bir bebek ağlaması duyuyorsun... Elinde kırık bir fener var. Ne yaparsın?",
                choices: [
                    {{ text: "🔦 Sesi takip et", next: 1, xp: 10, fearUp: 15 }},
                    {{ text: "🚪 Kapıyı açmayı dene", next: 2, xp: 5, fearUp: 5 }},
                    {{ text: "📱 Telefona bak", next: 3, xp: 8, fearUp: 8, damage: 0 }},
                ]
            }},
            {{
                text: "Sesi takip ediyorsun. Merdivenden çıkıyorsun, her adımda tahta gıcırdıyor. En üst odanın kapısı hafifçe açık... İçeriden soğuk bir rüzgar geliyor. Bebek sesi durdu.",
                choices: [
                    {{ text: "😱 Kapıyı itiyor — içeri giriyorsun", next: 4, xp: 20, fearUp: 20 }},
                    {{ text: "👂 Kulak kabartıyorsun", next: 5, xp: 10, fearUp: 10 }},
                    {{ text: "🏃 Kaçıyorsun aşağı", next: 6, xp: 5, fearUp: 5, damage: 0 }},
                ]
            }},
            {{
                text: "Kapıyı it— ve efsane bir BOOM! sesiyle yüzüne kapanıyor. Görünmez bir güç itmiş seni. Düşüyorsun. Korku seviyeni artıyor...",
                choices: [
                    {{ text: "💪 Tekrar kalkıyorsun", next: 1, xp: 15, fearUp: 15, damage: 1 }},
                    {{ text: "😰 Yerde bekliyorsun", next: 7, xp: 5, fearUp: 25, damage: 0 }},
                ]
            }},
            {{
                text: "Telefonuna bakıyorsun — şarj %2. Ekranda garip bir mesaj var: 'EVİ TERK ET'. Mesajı kim gönderdi?! Göndereni ararsın, 'hatlar dışında' uyarısı geliyor...",
                choices: [
                    {{ text: "📞 Tekrar arıyorsun", next: 8, xp: 10, fearUp: 10 }},
                    {{ text: "🔦 Feneri yakıyorsun", next: 1, xp: 8, fearUp: 5 }},
                ]
            }},
            {{
                text: "Odaya giriyorsun. Ortada küçük bir karyola var. Yavaşça yaklaşıyorsun... Karyola BOŞ. Ama sıcak! Birisi az önce buradaydı. Perdenin arkası hareket etti...",
                choices: [
                    {{ text: "🔪 Perdeyi çekiyorsun", next: 9, xp: 25, fearUp: 30 }},
                    {{ text: "💨 Dışarı fırlıyorsun", next: 6, xp: 10, fearUp: 10, damage: 0 }},
                ]
            }},
            {{
                text: "Kulak kabarttın. Bir hışırtı duyuyorsun. Ardından derin bir nefes. Ve bir fısıltı: 'Neden geldin...' Donup kalıyorsun. Sesin kaynağı tam arkanda!",
                choices: [
                    {{ text: "😱 Dönüyorsun yavaşça", next: 10, xp: 30, fearUp: 35 }},
                    {{ text: "🏃 Sprint atıyorsun", next: 6, xp: 10, fearUp: 15, damage: 1 }},
                ]
            }},
            {{
                text: "Koşarak aşağı iniyorsun, kapıya ulaşıyorsun ama... kapı kilitli! Anahtarı yok. Bir pencere var sol tarafta. Dışarısı kasvetli, soğuk bir gece. Ay ışığı içeri vuruyor.",
                choices: [
                    {{ text: "🪟 Pencereden çıkıyorsun", next: 11, xp: 20, fearUp: 5, damage: 0 }},
                    {{ text: "🔑 Anahtar arıyorsun", next: 1, xp: 15, fearUp: 20 }},
                ]
            }},
            {{
                text: "Yerde bekliyorsun. Sessizlik var. Sonra... bir şey senin yanına oturdu. Onu göremiyorsun. Ama ağırlığını hissediyorsun. Soğuk bir el koluna dokunuyor...",
                choices: [
                    {{ text: "😱 Bağırıyorsun", next: 12, xp: 5, fearUp: 40, damage: 1 }},
                    {{ text: "🧊 Hareketsiz kalıyorsun", next: 13, xp: 20, fearUp: 15 }},
                ]
            }},
            {{
                text: "Hat bağlandı! Ses geliyor ama insan sesi değil... Gürültü, parazit, ve uzaktan bir çığlık. Telefon kapanıyor ve ekran tamamen karardı. Artık karanlıkta yalnızsın.",
                choices: [
                    {{ text: "🔦 Feneri yakıyorsun", next: 1, xp: 10, fearUp: 10 }},
                    {{ text: "🚶 Sese doğru yürüyorsun", next: 4, xp: 20, fearUp: 20 }},
                ]
            }},
            {{
                text: "Perdeyi çekiyorsun ve — HİÇ BİR ŞEY YOK. Sadece soğuk bir duvar. Nefes alıyorsun. Sonra tam arkandan duyuyorsun: karyola gıcırdadı. Yavaşça dönüyorsun...",
                choices: [
                    {{ text: "💀 Yüzleşiyorsun", next: 14, xp: 40, fearUp: 40 }},
                    {{ text: "😰 Gözlerini kapıyorsun", next: 7, xp: 5, fearUp: 20 }},
                ]
            }},
            {{
                text: "Dönüyorsun... Beyaz geceliği olan küçük bir kız duruyor. Sana bakıyor. Gözleri yok. Sadece karanlık. Ağzını açıyor ve konuşuyor: 'Neden bizi terk ettin?'",
                choices: [
                    {{ text: "🗣️ Cevap veriyorsun", next: 15, xp: 35, fearUp: 50 }},
                    {{ text: "🏃 Kaçıyorsun", next: 6, xp: 10, fearUp: 30, damage: 1 }},
                ]
            }},
            {{
                text: "Pencereden atlıyorsun! Dışarısı özgürlük! Soğuk hava yüzüne çarpıyor. Arkana bakıyorsun — evin üst penceresinde biri seni izliyor. Koşmaya devam ediyorsun ve hayatta kalıyorsun!",
                choices: [], win: true
            }},
            {{
                text: "Bağırdın ve ses duvarları sarıyor. O soğuk el sıkıştı. Korku zirvede...",
                choices: [
                    {{ text: "😤 Direniniyorsun", next: 13, xp: 10, fearUp: 5, damage: 0 }},
                    {{ text: "💀 Vazgeçiyorsun", next: -1, xp: 0, fearUp: 0, damage: 2 }},
                ]
            }},
            {{
                text: "Sakin kalıyorsun. El yavaşça çekiliyor. Sessizlik geri dönüyor. Bir fısıltı: 'Güçlüsün...' ve kaybolup gidiyor. Etraf aydınlanıyor, kapı açılıyor. Çıkış yolunu buldun!",
                choices: [], win: true
            }},
            {{
                text: "Kız ve sen karşı karşıya geliyorsunuz. Yüzleşmek ona iyi geldi... 'Teşekkürler.' diyor ve kaybolup gidiyor. Ev aydınlanıyor. Huzur buluyor, sen de çıkış yolunu buluyorsun!",
                choices: [], win: true, xpBonus: 100
            }},
            {{
                text: "'Ben... bilmiyorum' diyorsun. Kız sana uzun uzun bakıyor. Sonra gülümsüyor — gözleri beliriyor. 'Artık biliyorsun.' diyor. Bir ışık parlıyor ve ev yıkılıyor. Sağ çıkıyorsun!",
                choices: [], win: true, xpBonus: 150
            }},
        ];

        function loadChapter(idx) {{
            if(idx === -1 || hp <= 0 || fear >= 100) {{ gameEnd(false); return; }}
            let s = story[idx];
            if(!s) {{ gameEnd(false); return; }}

            chapter++;
            document.getElementById('chapVal').innerText = Math.min(chapter, 5);

            // Korku efekti
            if(s.fearUp && s.fearUp > 20) scareFlash();

            document.getElementById('storyText').innerText = s.text;
            document.getElementById('hpVal').innerText = '❤️'.repeat(Math.max(0,hp));
            document.getElementById('fearVal').innerText = fear;

            let box = document.getElementById('choicesBox');
            box.innerHTML = '';

            if(s.win) {{ gameEnd(true, s.xpBonus || 0); return; }}

            s.choices.forEach(c => {{
                let btn = document.createElement('button');
                btn.className = 'choice-btn';
                btn.innerText = c.text;
                btn.onclick = () => {{
                    if(c.damage) {{ hp -= c.damage; }}
                    if(c.fearUp) {{ fear = Math.min(100, fear + c.fearUp); }}
                    if(c.xp) {{ addXP(c.xp, "Korku"); }}
                    loadChapter(c.next);
                }};
                box.appendChild(btn);
            }});
        }}

        function scareFlash() {{
            let el = document.getElementById('scareFlash');
            el.style.opacity = '0.4';
            setTimeout(() => el.style.opacity = '0', 150);
        }}

        function gameEnd(win, bonusXP=0) {{
            document.getElementById('storyText').innerText = '';
            document.getElementById('choicesBox').innerHTML = '';
            let es = document.getElementById('endScreen');
            es.style.display = 'block';
            if(win) {{
                document.getElementById('endTitle').innerText = '🏆 HAYATTA KALDIN!';
                document.getElementById('endDesc').innerText = 'Tebrikler! Evi geçtin. Korku puanın: ' + fear;
                if(bonusXP) addXP(bonusXP, "Ev Bitti!");
                addXP(50, "Hayatta Kaldın");
            }} else {{
                document.getElementById('endTitle').innerText = '💀 KARANLIĞA YUTULDUN';
                document.getElementById('endDesc').innerText = fear >= 100 ? 'Korku seni yendi!' : 'Canın bitti!';
            }}
        }}

        function restartGame() {{
            hp = 3; fear = 0; chapter = 1;
            document.getElementById('endScreen').style.display = 'none';
            loadChapter(0);
        }}

        window.onload = function() {{
            updateXPDisplay();
            loadChapter(0);
        }};
    </script>
</body>
</html>"""

# ============ 5. MARKET ============
store_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MARKET | Cano Studio</title>
    <style>{base_css}
    .store-wrap {{
        min-height: 100vh; padding: 100px 20px 80px;
        max-width: 1000px; margin: 0 auto;
    }}
    h1 {{ font-family: 'Orbitron'; text-align: center; font-size: clamp(1.2rem, 4vw, 2rem);
          background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          margin-bottom: 6px; }}
    .subtitle {{ color: #555; text-align: center; font-size: 0.8rem; letter-spacing: 3px; margin-bottom: 30px; }}
    .balance-box {{
        background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.3);
        border-radius: 12px; padding: 16px 24px; text-align: center; margin-bottom: 30px;
        font-family: 'Orbitron';
    }}
    .balance-box .big {{ font-size: 2rem; color: var(--neon-blue); }}
    .balance-box .lbl {{ color: #555; font-size: 0.75rem; letter-spacing: 2px; }}

    .category-tabs {{ display: flex; gap: 10px; justify-content: center; margin-bottom: 24px; flex-wrap: wrap; }}
    .tab {{
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        color: #666; padding: 8px 20px; border-radius: 50px; cursor: pointer;
        font-family: 'Orbitron'; font-size: 0.75rem; transition: all 0.2s;
    }}
    .tab.active {{ border-color: var(--neon-blue); color: var(--neon-blue); background: rgba(0,212,255,0.08); }}

    .store-grid {{
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
    }}
    .item {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 24px 16px; border-radius: 14px; text-align: center;
        transition: all 0.3s; position: relative; overflow: hidden;
    }}
    .item:hover {{ transform: translateY(-4px); border-color: var(--neon-blue); }}
    .item.owned {{ border-color: var(--neon-green); opacity: 0.7; }}
    .item-icon {{ font-size: 2.5rem; display: block; margin-bottom: 10px; }}
    .item-name {{ font-family: 'Orbitron'; font-size: 0.85rem; margin-bottom: 6px; }}
    .item-desc {{ color: #666; font-size: 0.75rem; margin-bottom: 14px; }}
    .item-price {{ color: var(--neon-orange); font-family: 'Orbitron'; font-size: 0.9rem; margin-bottom: 12px; }}
    .owned-badge {{
        position: absolute; top: 10px; right: 10px;
        background: var(--neon-green); color: #000;
        font-size: 0.6rem; font-family: 'Orbitron';
        padding: 3px 8px; border-radius: 50px;
    }}
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    <div class="xp-container"><span class="xp-val" id="xpVal">0</span><span class="xp-label">XP</span></div>
    <div class="level-badge" id="levelBadge">SEV 1</div>
    <div id="toast" class="toast"></div>

    <div class="store-wrap">
        <h1>MARKET</h1>
        <div class="subtitle">XP İLE EŞYA SATIN AL</div>

        <div class="balance-box">
            <div class="big" id="balanceVal">0</div>
            <div class="lbl">MEVCUT XP BAKİYESİ</div>
        </div>

        <div class="category-tabs">
            <div class="tab active" onclick="filterItems('all', this)">TÜMÜ</div>
            <div class="tab" onclick="filterItems('skin', this)">SKİNLER</div>
            <div class="tab" onclick="filterItems('boost', this)">BOOST</div>
            <div class="tab" onclick="filterItems('special', this)">ÖZEL</div>
        </div>

        <div class="store-grid" id="storeGrid"></div>
    </div>

    <a href="/" class="back-btn">← GERİ</a>

    <script>
        {base_js}

        const ITEMS = [
            {{ id: 'gold_skin', name: 'Altın Skin', icon: '✨', cat: 'skin', price: 500, desc: 'Oyuncuna altın parlaklığı katar' }},
            {{ id: 'neon_skin', name: 'Neon Skin', icon: '💡', cat: 'skin', price: 750, desc: 'Neon renk paleti' }},
            {{ id: 'dark_skin', name: 'Karanlık Skin', icon: '🌑', cat: 'skin', price: 1000, desc: 'Gecenin derinliklerinden' }},
            {{ id: 'speed_boost', name: 'Hız Botu', icon: '⚡', cat: 'boost', price: 1000, desc: 'Arcade\'de +%20 hız' }},
            {{ id: 'xp_boost', name: 'XP x2', icon: '🔥', cat: 'boost', price: 800, desc: '24 saat boyunca çift XP' }},
            {{ id: 'mine_boost', name: 'Maden Boost', icon: '⛏️', cat: 'boost', price: 600, desc: 'Strateji\'de +5 maden/tıklama' }},
            {{ id: 'ghost_badge', name: 'Hayalet Rozeti', icon: '👻', cat: 'special', price: 1500, desc: 'Horror tamamlayanların rozeti' }},
            {{ id: 'crown', name: 'Kral Tacı', icon: '👑', cat: 'special', price: 3000, desc: 'En prestijli ödül' }},
            {{ id: 'crystal_key', name: 'Kristal Anahtar', icon: '💎', cat: 'special', price: 2000, desc: 'Gizli alanları açar' }},
        ];

        let currentFilter = 'all';

        function filterItems(cat, tab) {{
            currentFilter = cat;
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            renderStore();
        }}

        function renderStore() {{
            let xp = getXP();
            let owned = getItems();
            document.getElementById('balanceVal').innerText = xp.toLocaleString();
            let grid = document.getElementById('storeGrid');
            grid.innerHTML = '';
            ITEMS.filter(i => currentFilter === 'all' || i.cat === currentFilter).forEach(item => {{
                let isOwned = owned.includes(item.id);
                let canBuy = xp >= item.price && !isOwned;
                let div = document.createElement('div');
                div.className = 'item' + (isOwned ? ' owned' : '');
                div.innerHTML = `
                    ${{isOwned ? '<div class="owned-badge">SAHİBİSİN</div>' : ''}}
                    <span class="item-icon">${{item.icon}}</span>
                    <div class="item-name">${{item.name}}</div>
                    <div class="item-desc">${{item.desc}}</div>
                    <div class="item-price">${{item.price.toLocaleString()}} XP</div>
                    <button class="btn btn-blue" ${{!canBuy ? 'disabled' : ''}} onclick="buyItem('${{item.id}}', ${{item.price}})">
                        ${{isOwned ? '✓ SATIN ALINDI' : 'SATIN AL'}}
                    </button>
                `;
                grid.appendChild(div);
            }});
        }}

        function buyItem(id, price) {{
            let xp = getXP();
            let owned = getItems();
            if(xp < price || owned.includes(id)) {{ showToast("XP Yetersiz veya Zaten Sahipsin!"); return; }}
            setXP(xp - price);
            owned.push(id);
            localStorage.setItem('cano_items', JSON.stringify(owned));
            showToast("✅ Satın Alındı!");
            renderStore();
        }}

        window.onload = function() {{ updateXPDisplay(); renderStore(); }};
    </script>
</body>
</html>"""

# ============ FLASK ROTALAR ============
@app.route('/')
def home(): return ana_sayfa_html

@app.route('/strateji')
def strateji(): return strateji_html

@app.route('/neon-arcade')
def arcade(): return arcade_html

@app.route('/horror')
def horror(): return horror_html

@app.route('/store')
def store(): return store_html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
