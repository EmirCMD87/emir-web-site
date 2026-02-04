# ==========================================
# CANO STUDIO - ULTIMATE GAMING PLATFORM v12
# ==========================================
# Geliştirici: Cano Studio
# Sürüm: 12.0 "Omega"
# Özellikler: 4 Oyun, XP Sistemi, G-Analytics
# ==========================================

from flask import Flask, request, jsonify
import os, random

app = Flask(__name__)

# --- GLOBAL VERİ SİSTEMİ ---
# Bu bölüm kullanıcıların skorlarını ve XP durumlarını geçici bellekte tutar.
scores = {
    "neon_arcade": [0],
    "void_command": [1],
    "lost_forest": [1],
    "glitch_in_me": [0],
    "xp": 0
}

# --- GOOGLE ANALYTICS KİMLİĞİ ---
# Bu ID ile cano-studio.onrender.com üzerindeki tüm trafiği izleyebilirsin.
GTAG_ID = "G-GQS70MDDPQ"

# --- GELİŞMİŞ CSS TASARIM SİSTEMİ ---
# Sayfaların görsel kimliğini belirleyen, parazit (glitch) efektli Cyberpunk tasarımı.
def get_global_styles():
    return """
    <style>
        :root { 
            --neon: #00bcd4; 
            --dark: #020202; 
            --glitch: #ff0055; 
            --gold: #f1c40f; 
            --bg-deep: #050505;
        }
        
        * { 
            box-sizing: border-box; 
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
            touch-action: manipulation; 
        }

        body { 
            background: var(--dark); 
            color: #e0e0e0; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            display: flex; 
            flex-direction: column; 
            min-height: 100vh; 
            overflow-x: hidden; 
        }

        /* Glitch Başlık Animasyonu */
        .glitch-header { 
            font-size: 3.5rem; 
            letter-spacing: 18px; 
            color: #fff; 
            position: relative; 
            animation: glitch-anim 3.5s infinite;
            text-transform: uppercase;
        }

        @keyframes glitch-anim {
            0% { text-shadow: 3px 3px var(--glitch); transform: skew(0deg); }
            20% { text-shadow: -3px -3px var(--neon); transform: skew(1deg); }
            40% { text-shadow: 3px -3px var(--glitch); transform: skew(-1deg); }
            60% { text-shadow: -3px 3px var(--neon); transform: skew(0deg); }
            80% { text-shadow: 2px 2px var(--glitch); transform: scale(1.02); }
            100% { text-shadow: -2px 2px var(--neon); transform: scale(1); }
        }

        /* Oyun Kartları Tasarımı */
        .container { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
            gap: 25px; 
            padding: 40px; 
            max-width: 1400px; 
            margin: 0 auto; 
            width:100%; 
        }

        .game-card { 
            background: #080808; 
            border: 1px solid #1a1a1a; 
            padding: 45px; 
            border-radius: 15px; 
            cursor: pointer; 
            position: relative; 
            overflow: hidden; 
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }

        .game-card:hover { 
            border-color: var(--neon); 
            background: #0d0d0d; 
            transform: translateY(-8px) scale(1.02); 
            box-shadow: 0 15px 40px rgba(0,188,212,0.15); 
        }

        .game-card h2 { margin: 15px 0; letter-spacing: 3px; font-weight: 300; }
        .game-card p { color: #555; font-size: 0.85rem; line-height: 1.5; }

        .status-badge { 
            font-size: 10px; 
            letter-spacing: 2px; 
            border: 1px solid; 
            display: inline-block; 
            padding: 4px 12px; 
            margin-bottom: 20px; 
            border-radius: 4px; 
            text-transform: uppercase;
        }

        /* Kullanıcı Arayüzü Butonları */
        .btn-ui { 
            background: rgba(0, 188, 212, 0.05); 
            border: 1px solid var(--neon); 
            color: var(--neon); 
            padding: 12px 24px; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            font-size: 0.85rem; 
            font-weight: bold; 
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .btn-ui:hover { 
            background: var(--neon); 
            color: #000; 
            box-shadow: 0 0 25px var(--neon); 
        }

        /* Destek ve Modal Sistemi */
        #supportModal { 
            display:none; 
            position:fixed; 
            top:0; 
            left:0; 
            width:100%; 
            height:100%; 
            background:rgba(0,0,0,0.98); 
            z-index:2000; 
            align-items:center; 
            justify-content:center; 
            backdrop-filter: blur(10px);
        }

        .modal-box { 
            background:#0a0a0a; 
            padding:50px; 
            border-radius:20px; 
            border:1px solid var(--neon); 
            max-width:550px; 
            width:90%; 
            text-align:center;
            box-shadow: 0 0 60px rgba(0,188,212,0.1);
        }

        .tab-nav { display:flex; gap:10px; margin:30px 0; }
        .tab-btn { 
            flex:1; 
            padding:15px; 
            border:1px solid #222; 
            background:transparent; 
            color:#444; 
            cursor:pointer; 
            font-weight:bold;
        }
        .tab-btn.active { border-color:var(--neon); color:var(--neon); background:rgba(0,188,212,0.05); }

        .amt-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-bottom:25px; }

        /* Liderlik Tablosu */
        .leaderboard-section {
            max-width: 900px;
            margin: 60px auto;
            padding: 40px;
            background: #050505;
            border-radius: 15px;
            border: 1px solid #111;
        }

        table { width: 100%; border-collapse: collapse; }
        th { color: #333; font-size: 0.75rem; text-align: left; padding: 15px; text-transform: uppercase; letter-spacing: 2px; }
        td { padding: 18px 15px; border-bottom: 1px solid #0d0d0d; color: #888; }
        .val-text { color: #fff; font-weight: bold; text-align: right; font-family: monospace; font-size: 1.1rem; }

        footer { 
            margin-top: auto; 
            padding: 50px; 
            border-top: 1px solid #080808; 
            text-align: center; 
            background: #030303;
        }
    </style>
    """

# --- GOOGLE ANALYTICS SCRIPT ---
def get_gtag_script():
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GTAG_ID}');
    </script>
    """

# --- GENEL HEADER ---
def get_head():
    return f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Cano Studio | Ultimate Platform</title>
        {get_gtag_script()}
        {get_global_styles()}
    </head>
    """

# --- NAVİGASYON VE DESTEK ---
support_ui = """
<a href="#" onclick="showSupport()" class="btn-ui" style="position:fixed; top:25px; right:25px; z-index:1000;">💳 STUDIO DESTEK</a>
<div id="supportModal">
    <div class="modal-box" id="supportBox">
        <h2 style="color:var(--neon); margin-top:0; letter-spacing:5px;">CANO STUDIO</h2>
        <p style="color:#666; font-size:0.9rem;">Projelerime destek olarak daha fazla oyun geliştirmemi sağlayabilirsin.</p>
        
        <div class="tab-nav">
            <button class="tab-btn active" id="btn-ininal" onclick="switchTab('ininal')">ININAL</button>
            <button class="tab-btn" id="btn-banka" onclick="switchTab('banka')">BANKA / EFT</button>
        </div>

        <div id="panel-ininal">
            <div class="amt-grid">
                <button class="btn-ui" onclick="donate('ininal', 10)">10 TL</button>
                <button class="btn-ui" onclick="donate('ininal', 50)">50 TL</button>
                <button class="btn-ui" onclick="donate('ininal', 100)">100 TL</button>
            </div>
            <div style="background:#000; padding:20px; border:1px dashed #333; color:#fff; font-family:monospace; letter-spacing:2px;">
                BARKOD: 4000 0000 0000 0
            </div>
        </div>

        <div id="panel-banka" style="display:none">
            <div style="background:#000; padding:25px; text-align:left; font-size:0.85rem; border-radius:10px; border:1px solid #222; line-height:1.8;">
                <b style="color:var(--neon)">ALICI:</b> CANO STUDIO<br>
                <b style="color:var(--neon)">IBAN:</b> TR00 0000 0000 0000 0000 0000 00<br>
                <p style="color:#ff4500; font-size:0.75rem; margin-top:15px; border-top:1px solid #111; pt:10px;">
                    * Transfer açıklama kısmına ininal barkod numaranızı eklemeyi unutmayın!
                </p>
            </div>
            <button class="btn-ui" style="width:100%; margin-top:20px;" onclick="donate('banka', 'IBAN')">IBAN KOPYALA</button>
        </div>

        <br>
        <button onclick="hideSupport()" style="color:#333; background:none; border:none; cursor:pointer; font-size:0.8rem; margin-top:25px; text-decoration:underline;">[ PENCEREYİ KAPAT ]</button>
    </div>
</div>

<script>
    function showSupport() { document.getElementById('supportModal').style.display='flex'; }
    function hideSupport() { document.getElementById('supportModal').style.display='none'; }
    
    function switchTab(t) {
        const pininal = document.getElementById('panel-ininal');
        const pbanka = document.getElementById('panel-banka');
        const bininal = document.getElementById('btn-ininal');
        const bbanka = document.getElementById('btn-banka');
        
        if(t === 'ininal') {
            pininal.style.display = 'block'; pbanka.style.display = 'none';
            bininal.className = 'tab-btn active'; bbanka.className = 'tab-btn';
        } else {
            pininal.style.display = 'none'; pbanka.style.display = 'block';
            bininal.className = 'tab-btn'; bbanka.className = 'tab-btn active';
        }
    }

    function donate(method, amount) {
        const data = method === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
        navigator.clipboard.writeText(data).then(() => {
            document.getElementById('supportBox').innerHTML = `
                <h1 style="color:var(--neon); font-size:3rem;">ADAMSIN! ❤️</h1>
                <p style="color:#fff; font-size:1.2rem; margin:20px 0;">${amount} TL değerindeki desteğin için teşekkürler.</p>
                <p style="color:#555;">Kopyalanan bilgileri uygulamanıza yapıştırarak işlemi tamamlayabilirsiniz.</p>
                <button onclick="location.reload()" class="btn-ui" style="margin-top:30px;">ANA MENÜYE DÖN</button>
            `;
        });
    }
</script>
"""

# --- 1. ANA SAYFA ROUTE ---
@app.route('/')
def home():
    xp_total = scores["xp"]
    # Rütbe Hesaplama Mantığı
    if xp_total < 150: rank = "BRONZE DEVELOPER"
    elif xp_total < 600: rank = "SILVER CODER"
    elif xp_total < 1500: rank = "GOLDEN CREATOR"
    else: rank = "PLATINUM LEGEND"

    html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_head()}
    <body>
        {support_ui}
        
        <div style="padding:100px 20px 60px 20px; text-align:center;">
            <h1 class="glitch-header" data-text="CANO STUDIO">CANO STUDIO</h1>
            <div style="margin-top:-15px;">
                <span style="color:var(--gold); font-weight:bold; letter-spacing:3px; font-size:0.9rem;">{rank}</span>
                <span style="color:#333; margin:0 15px;">|</span>
                <span style="color:var(--neon); font-family:monospace; font-size:1rem;">XP_{xp_total}</span>
            </div>
        </div>

        <div class="container">
            <div class="game-card" onclick="location.href='/neon-arcade'">
                <div class="status-badge" style="color:var(--neon); border-color:var(--neon);">Arcade / Action</div>
                <h2>NEON ARCADE</h2>
                <p>Yüksek hızda veri tünellerinden geç ve en yüksek skoru elde et. Reflekslerini test etme zamanı.</p>
                <div style="margin-top:20px; font-size:0.7rem; color:#333;">TOP_SCORE: {max(scores["neon_arcade"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/lost-forest'">
                <div class="status-badge" style="color:#ff4500; border-color:#ff4500;">FPS / Horror</div>
                <h2>LOST FOREST</h2>
                <p>Karanlık bir labirentte sıkıştın. Çıkışı bulmak için sinyalleri takip et. Raycasting teknolojisiyle hazırlandı.</p>
                <div style="margin-top:20px; font-size:0.7rem; color:#333;">SURVIVAL_LVL: {max(scores["lost_forest"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/void-command'">
                <div class="status-badge" style="color:#00ff88; border-color:#00ff88;">Strategy / Tactics</div>
                <h2>VOID COMMAND</h2>
                <p>Galaksiler arası enerji transferi yönetimi. Düşman gezegenleri fethet ve sistemini genişlet.</p>
                <div style="margin-top:20px; font-size:0.7rem; color:#333;">SECTOR_CONQUEST: {max(scores["void_command"])}</div>
            </div>
        </div>

        <div class="leaderboard-section">
            <h3 style="text-align:center; color:#222; letter-spacing:5px; margin-bottom:30px;">KÜRESEL_İSTATİSTİKLER</h3>
            <table>
                <thead>
                    <tr><th>GÖREV ADI</th><th style="text-align:right;">DURUM VERİSİ</th></tr>
                </thead>
                <tbody>
                    <tr><td>Neon Tunnel Accuracy</td><td class="val-text">{max(scores["neon_arcade"])} pts</td></tr>
                    <tr><td>Deep Forest Survival</td><td class="val-text">Lvl {max(scores["lost_forest"])}</td></tr>
                    <tr><td>Void System Dominance</td><td class="val-text">Lvl {max(scores["void_command"])}</td></tr>
                    <tr style="border:none;"><td>Platform Experience</td><td class="val-text" style="color:var(--gold);">{xp_total} XP</td></tr>
                </tbody>
            </table>
        </div>

        <footer>
            <p style="color:#111; font-size:0.65rem; letter-spacing:4px;">CONNECTION_SECURE: ANALYTICS_STREAMING_{GTAG_ID}</p>
            <p style="color:#222; font-size:0.6rem; margin-top:10px;">© 2026 CANO STUDIO DIGITAL LABS. ALL RIGHTS RESERVED.</p>
        </footer>
    </body>
    </html>
    """
    return html

# --- 2. NEON ARCADE OYUN MOTORU ---
@app.route('/neon-arcade')
def arcade():
    # Bu bölüm oyunun fizik motorunu ve görsel render sistemini içerir.
    html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_head()}
    <body style="overflow:hidden; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh;">
        {support_ui}
        <a href="/" class="btn-ui" style="position:fixed; top:25px; left:25px; z-index:1000;">← ÇIKIŞ</a>
        
        <div id="game-ui" style="position:fixed; top:80px; color:var(--neon); font-family:monospace; font-size:1.2rem; letter-spacing:2px;">
            SCORE_BUFFER: <span id="score-val">0</span>
        </div>

        <canvas id="arcadeCanvas" width="450" height="650" style="border:1px solid #111; background:#000; box-shadow: 0 0 50px rgba(0,188,212,0.05); cursor:crosshair;"></canvas>

        <script>
            const canvas = document.getElementById("arcadeCanvas");
            const ctx = canvas.getContext("2d");
            const scoreEl = document.getElementById("score-val");

            let bird, pipes, frames, score, gameActive, particles;

            // Motoru Başlat
            function init() {{
                bird = {{ y: 300, velocity: 0, gravity: 0.38, jump: -7.5, size: 32 }};
                pipes = [];
                particles = [];
                frames = 0;
                score = 0;
                gameActive = true;
                scoreEl.innerText = "0";
            }}

            function createExplosion(x, y, color) {{
                for(let i=0; i<15; i++) {{
                    particles.push({{
                        x: x, y: y,
                        vx: (Math.random()-0.5) * 8,
                        vy: (Math.random()-0.5) * 8,
                        life: 1.0,
                        color: color
                    }});
                }}
            }}

            function updateParticles() {{
                for(let i=particles.length-1; i>=0; i--) {{
                    let p = particles[i];
                    p.x += p.vx; p.y += p.vy;
                    p.life -= 0.02;
                    if(p.life <= 0) particles.splice(i, 1);
                }}
            }}

            function drawParticles() {{
                particles.forEach(p => {{
                    ctx.globalAlpha = p.life;
                    ctx.fillStyle = p.color;
                    ctx.fillRect(p.x, p.y, 3, 3);
                }});
                ctx.globalAlpha = 1.0;
            }}

            function triggerGameOver() {{
                gameActive = false;
                createExplosion(50 + bird.size/2, bird.y + bird.size/2, "#ff0055");
                if(score > 0) fetch('/submit_score/neon_arcade/' + score);
            }}

            function mainLoop() {{
                // Ekranı Temizle
                ctx.fillStyle = "#000";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                if(!gameActive) {{
                    ctx.fillStyle = "rgba(0,0,0,0.8)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#fff";
                    ctx.font = "20px monospace";
                    ctx.textAlign = "center";
                    ctx.fillText("CRITICAL FAILURE", canvas.width/2, canvas.height/2 - 20);
                    ctx.fillStyle = var("--neon");
                    ctx.fillText("REBOOT (TIKLA)", canvas.width/2, canvas.height/2 + 20);
                    drawParticles();
                    updateParticles();
                    requestAnimationFrame(mainLoop);
                    return;
                }}

                // Kuş Fiziği
                bird.velocity += bird.gravity;
                bird.y += bird.velocity;

                // Kuş Render
                ctx.shadowBlur = 15; ctx.shadowColor = var("--neon");
                ctx.fillStyle = var("--neon");
                ctx.fillRect(50, bird.y, bird.size, bird.size);
                ctx.shadowBlur = 0;

                // Boru Üretimi
                if(frames % 90 === 0) {{
                    let gap = 170;
                    let h = Math.random() * (canvas.height - gap - 200) + 100;
                    pipes.push({{ x: canvas.width, h: h, gap: gap, passed: false }});
                }}

                // Boru Render ve Çarpışma
                for(let i = pipes.length - 1; i >= 0; i--) {{
                    let p = pipes[i];
                    p.x -= 4.2;

                    ctx.fillStyle = "#080808";
                    ctx.strokeStyle = "#151515";
                    // Üst Boru
                    ctx.fillRect(p.x, 0, 65, p.h);
                    ctx.strokeRect(p.x, 0, 65, p.h);
                    // Alt Boru
                    ctx.fillRect(p.x, p.h + p.gap, 65, canvas.height);
                    ctx.strokeRect(p.x, p.h + p.gap, 65, canvas.height);

                    // Çarpışma Kontrolü
                    if(50 + bird.size > p.x && 50 < p.x + 65) {{
                        if(bird.y < p.h || bird.y + bird.size > p.h + p.gap) {{
                            triggerGameOver();
                        }}
                    }}

                    // Skor Artışı
                    if(p.x < 50 && !p.passed) {{
                        score++;
                        p.passed = true;
                        scoreEl.innerText = score;
                    }}

                    if(p.x < -70) pipes.splice(i, 1);
                }}

                if(bird.y > canvas.height || bird.y < 0) triggerGameOver();

                frames++;
                requestAnimationFrame(mainLoop);
            }}

            window.addEventListener("pointerdown", (e) => {{
                e.preventDefault();
                if(gameActive) bird.velocity = bird.jump;
                else init();
            }});

            // Başlat
            init();
            mainLoop();
        </script>
    </body>
    </html>
    """
    return html

# --- 3. LOST FOREST (FPS MOTORU) ---
@app.route('/lost-forest')
def horror():
    # Bu bölüm Raycasting teknolojisiyle yazılmış 3D görünümlü bir FPS motorudur.
    html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_head()}
    <body style="overflow:hidden; background:#000; margin:0; touch-action:none;">
        {support_ui}
        <a href="/" class="btn-ui" style="position:fixed; top:25px; left:25px; z-index:1000;">← ÇIKIŞ</a>
        
        <div style="position:fixed; top:80px; width:100%; text-align:center; color:#fff; font-family:monospace; z-index:10; letter-spacing:4px; opacity:0.6;">
            DEPTH_LEVEL: <span id="lvl-display">1</span> | SIGNAL_STATUS: <span id="sig">STABLE</span>
        </div>

        <div id="joy-container" style="position:fixed; bottom:60px; left:60px; width:140px; height:140px; background:rgba(255,255,255,0.02); border:1px solid #222; border-radius:50%; z-index:100;">
            <div id="joy-stick" style="position:absolute; top:45px; left:45px; width:50px; height:50px; background:var(--neon); opacity:0.15; border-radius:50%; transition:0.1s;"></div>
        </div>

        <canvas id="rayCanvas"></canvas>

        <script>
            const canvas = document.getElementById("rayCanvas");
            const ctx = canvas.getContext("2d");
            const lvlDisp = document.getElementById("lvl-display");

            let level = 1;
            let map = [];
            let player = {{ x: 1.5, y: 1.5, dir: 0, speed: 0.045, fov: Math.PI / 3 }};
            let joy = {{ active: false, x: 0, y: 0 }};

            // Harita Oluşturucu
            function generateMap(size) {{
                let m = Array.from({{ length: size }}, () => Array(size).fill(1));
                for(let y=1; y<size-1; y++) {{
                    for(let x=1; x<size-1; x++) {{
                        if(Math.random() > 0.38) m[y][x] = 0;
                    }}
                }}
                m[1][1] = 0; // Başlangıç
                m[size-2][size-2] = 2; // Çıkış Kapısı
                return m;
            }}

            function resize() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }}

            const jCont = document.getElementById("joy-container");
            const jStick = document.getElementById("joy-stick");

            jCont.addEventListener("touchstart", (e) => {{ joy.active = true; }}, {{passive: false}});
            jCont.addEventListener("touchmove", (e) => {{
                e.preventDefault();
                let t = e.touches[0];
                let rect = jCont.getBoundingClientRect();
                let dx = t.clientX - (rect.left + 70);
                let dy = t.clientY - (rect.top + 70);
                let dist = Math.min(Math.hypot(dx, dy), 60);
                let angle = Math.atan2(dy, dx);
                
                joy.x = Math.cos(angle) * (dist / 60);
                joy.y = Math.sin(angle) * (dist / 60);
                jStick.style.transform = `translate(${{joy.x * 45}}px, ${{joy.y * 45}}px)`;
            }}, {{passive: false}});

            jCont.addEventListener("touchend", () => {{
                joy.active = false;
                joy.x = 0; joy.y = 0;
                jStick.style.transform = "translate(0,0)";
            }});

            function initLevel() {{
                let size = 10 + (level * 2);
                map = generateMap(size);
                player.x = 1.5; player.y = 1.5;
                lvlDisp.innerText = level;
            }}

            function update() {{
                if(!joy.active) return;
                
                let oldX = player.x, oldY = player.y;
                
                // Hareket (İleri-Geri)
                if(Math.abs(joy.y) > 0.2) {{
                    let moveStep = -joy.y * player.speed * 1.5;
                    player.x += Math.cos(player.dir) * moveStep;
                    player.y += Math.sin(player.dir) * moveStep;
                }}
                
                // Dönüş (Sağ-Sol)
                if(Math.abs(joy.x) > 0.2) {{
                    player.dir += joy.x * 0.07;
                }}

                // Duvar Çarpışması
                if(map[Math.floor(player.y)][Math.floor(player.x)] === 1) {{
                    player.x = oldX; player.y = oldY;
                }}

                // Seviye Atlama
                if(map[Math.floor(player.y)][Math.floor(player.x)] === 2) {{
                    level++;
                    fetch('/submit_score/lost_forest/' + level);
                    initLevel();
                }}
            }}

            function draw() {{
                // Zemin ve Tavan
                ctx.fillStyle = "#050805";
                ctx.fillRect(0, 0, canvas.width, canvas.height/2);
                ctx.fillStyle = "#020402";
                ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height);

                const numRays = 120;
                for(let i=0; i<numRays; i++) {{
                    let rayAngle = (player.dir - player.fov/2) + (i / numRays) * player.fov;
                    let dist = 0;
                    let hit = 0;
                    
                    while(dist < 15) {{
                        dist += 0.08;
                        let tx = Math.floor(player.x + Math.cos(rayAngle) * dist);
                        let ty = Math.floor(player.y + Math.sin(rayAngle) * dist);
                        
                        if(map[ty] && map[ty][tx] > 0) {{
                            hit = map[ty][tx];
                            break;
                        }}
                    }}

                    // Balıkgözü Etkisi Düzeltme
                    dist *= Math.cos(rayAngle - player.dir);
                    let wallH = canvas.height / (dist + 0.001);
                    
                    // Gölgelendirme
                    let colorVal = Math.max(0, 160 - (dist * 12));
                    ctx.fillStyle = hit === 2 ? "#fff" : `rgb(0, ${{colorVal}}, 0)`;
                    ctx.fillRect(i * (canvas.width/numRays), (canvas.height - wallH)/2, (canvas.width/numRays)+1, wallH);
                }}

                // Karanlık Atmosfer Overlay
                let grad = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 50, canvas.width/2, canvas.height/2, canvas.width*0.8);
                grad.addColorStop(0, "transparent");
                grad.addColorStop(1, "rgba(0,0,0,0.95)");
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }}

            function renderLoop() {{
                update();
                draw();
                requestAnimationFrame(renderLoop);
            }}

            window.addEventListener("resize", resize);
            resize();
            initLevel();
            renderLoop();
        </script>
    </body>
    </html>
    """
    return html

# --- 4. VOID COMMAND (STRATEJİ MOTORU) ---
@app.route('/void-command')
def strategy():
    # Bu bölüm gezegenler arası enerji yönetimi üzerine kurulu taktiksel bir oyundur.
    html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_head()}
    <body style="background:#000; overflow:hidden;">
        {support_ui}
        <a href="/" class="btn-ui" style="position:fixed; top:25px; left:25px; z-index:1000;">← ÇIKIŞ</a>
        
        <div id="strat-ui" style="position:fixed; top:85px; width:100%; text-align:center; color:#00ff88; font-family:monospace; letter-spacing:5px;">
            SYSTEM_CONQUEST: <span id="lvl-val">1</span>
        </div>

        <canvas id="stratCanvas"></canvas>

        <script>
            const canvas = document.getElementById("stratCanvas");
            const ctx = canvas.getContext("2d");
            const lvlVal = document.getElementById("lvl-val");

            let level = 1;
            let planets = [];
            let selected = null;
            let particles = [];

            class Planet {{
                constructor(x, y, radius, owner) {{
                    this.x = x; this.y = y; this.radius = radius;
                    this.owner = owner; // 'player', 'enemy', 'neutral'
                    this.energy = owner === 'neutral' ? 5 : 25;
                    this.maxEnergy = radius * 2.5;
                    this.pulse = 0;
                }}

                update() {{
                    if(this.owner !== 'neutral') {{
                        this.energy = Math.min(this.maxEnergy, this.energy + 0.035);
                    }}
                    this.pulse += 0.05;
                }}

                draw() {{
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.radius + Math.sin(this.pulse)*2, 0, Math.PI*2);
                    
                    if(this.owner === 'player') ctx.strokeStyle = "#00ff88";
                    else if(this.owner === 'enemy') ctx.strokeStyle = "#ff4400";
                    else ctx.strokeStyle = "#222";
                    
                    ctx.lineWidth = selected === this ? 5 : 2;
                    ctx.stroke();

                    // Enerji Göstergesi
                    ctx.fillStyle = ctx.strokeStyle;
                    ctx.font = "12px monospace";
                    ctx.textAlign = "center";
                    ctx.fillText(Math.floor(this.energy), this.x, this.y + 5);

                    // Enerji Barı Altlık
                    ctx.fillStyle = "rgba(255,255,255,0.05)";
                    ctx.fillRect(this.x - 20, this.y + this.radius + 15, 40, 4);
                    // Enerji Barı Doluluk
                    ctx.fillStyle = ctx.strokeStyle;
                    ctx.fillRect(this.x - 20, this.y + this.radius + 15, (this.energy / this.maxEnergy) * 40, 4);
                }}
            }}

            function initGame() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                planets = [];
                selected = null;
                lvlVal.innerText = level;

                // Oyuncu Gezegeni
                planets.push(new Planet(120, canvas.height/2, 50, 'player'));
                // Düşman Gezegeni
                planets.push(new Planet(canvas.width - 120, canvas.height/2, 50, 'enemy'));

                // Tarafsız Gezegenler
                for(let i=0; i < level + 5; i++) {{
                    let rx = Math.random() * (canvas.width - 300) + 150;
                    let ry = Math.random() * (canvas.height - 200) + 100;
                    planets.push(new Planet(rx, ry, 30, 'neutral'));
                }}
            }}

            canvas.addEventListener("pointerdown", (e) => {{
                let p = planets.find(p => Math.hypot(p.x - e.clientX, p.y - e.clientY) < p.radius + 10);
                
                if(p) {{
                    if(p.owner === 'player') {{
                        selected = p;
                    }} else if(selected) {{
                        // Saldırı veya Takviye
                        let force = selected.energy / 2;
                        selected.energy -= force;
                        p.energy -= force;
                        
                        if(p.energy < 0) {{
                            p.owner = 'player';
                            p.energy = Math.abs(p.energy);
                        }}
                        selected = null;
                    }}
                }} else {{
                    selected = null;
                }}
            }});

            function loop() {{
                ctx.fillStyle = "rgba(0,0,0,0.2)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                planets.forEach(p => {{
                    p.update();
                    p.draw();
                }});

                // Bölüm Sonu Kontrolü
                if(!planets.some(p => p.owner === 'enemy')) {{
                    level++;
                    fetch('/submit_score/void_command/' + level);
                    initGame();
                }}

                requestAnimationFrame(loop);
            }}

            window.addEventListener("resize", initGame);
            initGame();
            loop();
        </script>
    </body>
    </html>
    """
    return html

# --- API SERVİSLERİ ---
@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    # Bu API, oyunlardan gelen skorları toplar ve XP hesaplaması yapar.
    if game in scores:
        scores[game].append(score)
        # XP Katsayısı: Skor x 15
        scores["xp"] += (score * 15)
        return jsonify({"status": "success", "new_xp": scores["xp"]})
    return jsonify({"status": "error"}), 400

# --- UYGULAMA BAŞLATICI ---
if __name__ == "__main__":
    # Render üzerinde PORT değişkeni otomatik atanır.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# KOD SONU - CANO STUDIO OMEGA SÜRÜMÜ
# ==========================================
