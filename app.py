# ==============================================================================
# CANO STUDIO - UNIVERSAL GAMING PLATFORM v14.0 "COLOSSUS"
# ==============================================================================
# Bu dosya Cano Studio'nun en kapsamlı sürümüdür. 
# İçerik: Backend (Flask), Frontend (HTML5/CSS3), Oyun Motorları (JavaScript ES6)
# Platform: %100 PC (Klavye/Mouse) ve Mobil (Touch/Joystick) uyumlu.
# Google Analytics ID: G-GQS70MDDPQ
# ==============================================================================

from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# ------------------------------------------------------------------------------
# 1. VERİ SAKLAMA VE İSTATİSTİK SİSTEMİ
# ------------------------------------------------------------------------------
# Sunucu tarafında oyuncu verilerini (skorlar ve deneyim puanları) tutan yapı.
# Not: Sunucu her yeniden başladığında bu veriler sıfırlanır.
# ------------------------------------------------------------------------------
user_data = {
    "neon_arcade": {
        "scores": [0],
        "description": "Hız ve refleks tabanlı arcade tünel oyunu."
    },
    "void_command": {
        "levels": [1],
        "description": "Gezegenler arası strateji ve fetih motoru."
    },
    "lost_forest": {
        "levels": [1],
        "description": "Raycasting teknolojisi ile üretilmiş 3D FPS korku oyunu."
    },
    "platform_stats": {
        "total_xp": 0,
        "rank": "ROOKIE DEVELOPER",
        "api_calls": 0
    }
}

# ------------------------------------------------------------------------------
# 2. GLOBAL TASARIM VE STİL MOTORU (CSS)
# ------------------------------------------------------------------------------
# Sitenin Cyberpunk temasını, glitch efektlerini ve duyarlı (responsive) 
# yapısını oluşturan devasa CSS bloğu.
# ------------------------------------------------------------------------------
def generate_global_css():
    """
    Sitenin görsel kimliğini oluşturan CSS kodlarını döner. 
    F-string hatalarını önlemek için güvenli format kullanılmıştır.
    """
    css_content = """
    <style>
        /* Tasarım Değişkenleri */
        :root {
            --neon-blue: #00bcd4;
            --cyber-pink: #ff0055;
            --void-black: #020202;
            --deep-gray: #0a0a0a;
            --gold-xp: #f1c40f;
            --text-main: #e0e0e0;
        }

        /* Temel Sayfa Yapısı */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--void-black);
            color: var(--text-main);
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Gelişmiş Glitch Animasyonu */
        .header-title {
            font-size: clamp(2rem, 8vw, 4rem);
            letter-spacing: clamp(10px, 2vw, 20px);
            color: #ffffff;
            text-align: center;
            text-transform: uppercase;
            position: relative;
            animation: glitch-vfx 4s infinite alternate;
            padding: 40px 10px;
        }

        @keyframes glitch-vfx {
            0% { text-shadow: 3px 0 var(--cyber-pink); transform: skew(0deg); }
            10% { text-shadow: -3px 0 var(--neon-blue); }
            20% { transform: skew(1deg); }
            50% { text-shadow: 2px 2px var(--gold-xp); }
            100% { text-shadow: -3px -2px var(--cyber-pink); transform: skew(-1deg); }
        }

        /* Oyun Seçim Alanı */
        .game-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            padding: 40px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        .game-card {
            background: var(--deep-gray);
            border: 1px solid #151515;
            padding: 50px 30px;
            border-radius: 20px;
            cursor: pointer;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .game-card:hover {
            border-color: var(--neon-blue);
            background: #0f0f0f;
            transform: translateY(-10px);
            box-shadow: 0 20px 50px rgba(0, 188, 212, 0.15);
        }

        .game-card h2 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            letter-spacing: 3px;
            color: #fff;
        }

        .game-card p {
            color: #666;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        /* Profesyonel Butonlar */
        .btn-action {
            background: rgba(0, 188, 212, 0.05);
            border: 1px solid var(--neon-blue);
            color: var(--neon-blue);
            padding: 14px 28px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .btn-action:hover {
            background-color: var(--neon-blue);
            color: #000;
            box-shadow: 0 0 30px var(--neon-blue);
        }

        /* Destek Menüsü (Modal) */
        #modalSupport {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.98);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(15px);
        }

        .modal-content-box {
            background: #050505;
            padding: 60px 40px;
            border-radius: 25px;
            border: 1px solid var(--neon-blue);
            max-width: 600px;
            width: 90%;
            text-align: center;
            box-shadow: 0 0 100px rgba(0,188,212,0.1);
        }

        /* Tablo ve Skorlar */
        .stats-container {
            max-width: 900px;
            margin: 40px auto;
            background: #030303;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #111;
        }

        .stats-table {
            width: 100%;
            border-collapse: collapse;
        }

        .stats-table td {
            padding: 20px;
            border-bottom: 1px solid #080808;
            color: #555;
        }

        .stats-table .score-val {
            text-align: right;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            font-size: 1.2rem;
        }

        /* Cihaz Bazlı Gizleme (Responsive) */
        @media (min-width: 1025px) {
            #mobile-joystick-ui { display: none !important; }
        }

        footer {
            margin-top: auto;
            padding: 60px 20px;
            text-align: center;
            border-top: 1px solid #080808;
            background: #010101;
        }
    </style>
    """
    return css_content

# ------------------------------------------------------------------------------
# 3. ANALYTICS VE TAKİP SİSTEMİ
# ------------------------------------------------------------------------------
# Google Analytics 4 (GA4) entegrasyonu. 
# Ziyaretçi trafiğini izlemek için Measurement ID: G-GQS70MDDPQ
# ------------------------------------------------------------------------------
def generate_analytics_js():
    """
    Google Analytics scriptlerini döner. 
    Parantez çakışmasını önlemek için süslü parantezler çiftlenmiştir.
    """
    ga_id = "G-GQS70MDDPQ"
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}');
    </script>
    """

# ------------------------------------------------------------------------------
# 4. HTML ŞABLON MOTORU
# ------------------------------------------------------------------------------
# Tüm sayfalar için ortak kafa (head) ve navigasyon bileşenleri.
# ------------------------------------------------------------------------------
def get_universal_head():
    return f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Cano Studio | Professional Gaming Platform</title>
        {generate_analytics_js()}
        {generate_global_css()}
    </head>
    """

support_overlay_html = """
<a href="#" onclick="toggleSupport(true)" class="btn-action" style="position:fixed; top:25px; right:25px; z-index:9000;">💎 DESTEK OL</a>
<div id="modalSupport">
    <div class="modal-content-box" id="modalContainer">
        <h2 style="color:var(--neon-blue); letter-spacing:10px; margin-bottom:20px;">CANO STUDIO</h2>
        <p style="color:#666; margin-bottom:30px; font-size:0.9rem;">Projelerimi destekleyerek gelişmeme katkıda bulunabilirsin.</p>
        
        <div style="display:flex; gap:15px; margin-bottom:40px;">
            <button class="btn-action" style="flex:1" onclick="handleDonate('ininal')">ININAL</button>
            <button class="btn-action" style="flex:1" onclick="handleDonate('banka')">BANKA / EFT</button>
        </div>

        <button onclick="toggleSupport(false)" style="background:none; border:none; color:#333; cursor:pointer; text-decoration:underline;">[ KAPAT ]</button>
    </div>
</div>

<script>
    function toggleSupport(show) {
        document.getElementById('modalSupport').style.display = show ? 'flex' : 'none';
    }

    function handleDonate(type) {
        const payload = type === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
        navigator.clipboard.writeText(payload).then(() => {
            document.getElementById('modalContainer').innerHTML = `
                <h1 style="color:var(--neon-blue); font-size:3rem; margin-bottom:20px;">ADAMSIN! ❤️</h1>
                <p style="color:#fff; font-size:1.1rem; line-height:1.6;">Bilgiler panoya kopyalandı. Desteğin için sonsuz teşekkürler!</p>
                <div style="margin-top:40px;">
                    <button onclick="location.reload()" class="btn-action">ANA MENÜYE DÖN</button>
                </div>
            `;
        });
    }
</script>
"""

# ------------------------------------------------------------------------------
# 5. ANA SAYFA (DASHBOARD)
# ------------------------------------------------------------------------------
# Kullanıcının oyunları seçtiği ve skorlarını gördüğü merkez üssü.
# ------------------------------------------------------------------------------
@app.route('/')
def route_home():
    # XP ve Rütbe Hesaplama
    total_xp = user_data["platform_stats"]["total_xp"]
    if total_xp > 2000: rank = "PLATINUM LEGEND"
    elif total_xp > 1000: rank = "GOLD MASTER"
    elif total_xp > 500: rank = "SILVER EXPERT"
    else: rank = "BRONZE ROOKIE"

    html_output = f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_universal_head()}
    <body>
        {support_overlay_html}
        
        <header>
            <h1 class="header-title" data-text="CANO STUDIO">CANO STUDIO</h1>
            <div style="text-align:center; margin-top:-20px;">
                <span style="color:var(--gold-xp); font-weight:bold; letter-spacing:4px;">{rank}</span>
                <span style="color:#222; margin:0 20px;">|</span>
                <span style="color:var(--neon-blue); font-family:monospace; font-size:1.1rem;">EXP_{total_xp}</span>
            </div>
        </header>

        <main class="game-grid">
            <div class="game-card" onclick="location.href='/neon-arcade'">
                <div style="color:var(--neon-blue); font-size:0.7rem; border:1px solid; display:inline-block; padding:3px 10px; border-radius:4px; margin-bottom:20px;">ARCADE / PC & MOBIL</div>
                <h2>NEON ARCADE</h2>
                <p>Veri tünellerinde ışık hızında ilerle. Engellere takılmadan en yüksek verimlilik skoruna ulaş.</p>
                <div style="margin-top:30px; border-top:1px solid #111; padding-top:15px; font-size:0.7rem; color:#333;">MAX_SCORE: {max(user_data["neon_arcade"]["scores"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/lost-forest'">
                <div style="color:var(--cyber-pink); font-size:0.7rem; border:1px solid; display:inline-block; padding:3px 10px; border-radius:4px; margin-bottom:20px;">FPS / RAYCASTING</div>
                <h2>LOST FOREST</h2>
                <p>Karanlık bir labirentte sinyalleri takip ederek çıkışı bulmaya çalış. Hayatta kalma testi.</p>
                <div style="margin-top:30px; border-top:1px solid #111; padding-top:15px; font-size:0.7rem; color:#333;">SECTOR_REACHED: {max(user_data["lost_forest"]["levels"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/void-command'">
                <div style="color:#00ff88; font-size:0.7rem; border:1px solid; display:inline-block; padding:3px 10px; border-radius:4px; margin-bottom:20px;">STRATEGY / TACTICS</div>
                <h2>VOID COMMAND</h2>
                <p>Gezegenler arası enerji dengesini sağla ve rakip sistemleri kendi ağına dahil et.</p>
                <div style="margin-top:30px; border-top:1px solid #111; padding-top:15px; font-size:0.7rem; color:#333;">SYSTEM_CONQUEST: {max(user_data["void_command"]["levels"])}</div>
            </div>
        </main>

        <section class="stats-container">
            <h3 style="text-align:center; color:#222; letter-spacing:6px; margin-bottom:40px; text-transform:uppercase;">Global Veri Merkezi</h3>
            <table class="stats-table">
                <tbody>
                    <tr>
                        <td>Neon Arcade Verimliliği</td>
                        <td class="score-val">{max(user_data["neon_arcade"]["scores"])} PTS</td>
                    </tr>
                    <tr>
                        <td>Derin Orman Keşfi</td>
                        <td class="score-val">Lvl {max(user_data["lost_forest"]["levels"])}</td>
                    </tr>
                    <tr>
                        <td>Boşluk Komut Yetkisi</td>
                        <td class="score-val">Lvl {max(user_data["void_command"]["levels"])}</td>
                    </tr>
                    <tr style="border:none;">
                        <td style="color:var(--gold-xp); font-weight:bold;">Toplam Platform Tecrübesi</td>
                        <td class="score-val" style="color:var(--gold-xp);">{total_xp} XP</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <footer>
            <p style="color:#222; font-size:0.7rem; letter-spacing:4px; margin-bottom:10px;">ANALYTICS_ID: {GTAG_ID} | CONNECTION: SECURE</p>
            <p style="color:#111; font-size:0.6rem;">© 2026 CANO STUDIO DIGITAL ENTERTAINMENT. ALL RIGHTS RESERVED.</p>
        </footer>
    </body>
    </html>
    """
    return html_output

# ------------------------------------------------------------------------------
# 6. NEON ARCADE (UNIVERSAL ENGINE)
# ------------------------------------------------------------------------------
# Hem klavye hem dokunmatik girişleri destekleyen fizik tabanlı oyun motoru.
# ------------------------------------------------------------------------------
@app.route('/neon-arcade')
def route_arcade():
    html_page = f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_universal_head()}
    <body style="overflow:hidden; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh;">
        {support_overlay_html}
        <a href="/" class="btn-action" style="position:fixed; top:25px; left:25px; z-index:9000;">← ÇIKIŞ YAP</a>
        
        <div style="position:fixed; top:80px; color:var(--neon-blue); font-family:monospace; font-size:1.4rem; letter-spacing:3px;">
            BUFFER: <span id="score-live">0</span>
        </div>

        <canvas id="canvasArcade" width="450" height="650" style="background:#000; border:1px solid #111; box-shadow:0 0 40px rgba(0,0,0,1);"></canvas>

        <script>
            /**
             * NEON ARCADE CORE ENGINE v2.0
             * Klavye: Space Bar
             * Mobil: Ekranın herhangi bir yerine dokunma
             */
            const canvas = document.getElementById("canvasArcade");
            const ctx = canvas.getContext("2d");
            const liveScore = document.getElementById("score-live");

            let player, obstacles, frames, currentScore, isPlaying;

            function startup() {{
                player = {{ y: 325, vel: 0, gravity: 0.35, jump: -7.2, w: 34, h: 34 }};
                obstacles = [];
                frames = 0;
                currentScore = 0;
                isPlaying = true;
                liveScore.innerText = "0";
            }}

            function endGame() {{
                isPlaying = false;
                if(currentScore > 0) {{
                    fetch('/api/submit/' + currentScore + '/neon_arcade');
                }}
            }}

            function render() {{
                // Background
                ctx.fillStyle = "#000";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                if(!isPlaying) {{
                    ctx.fillStyle = "rgba(0,0,0,0.85)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#fff";
                    ctx.font = "bold 20px Courier New";
                    ctx.textAlign = "center";
                    ctx.fillText("SISTEM HATASI: CARPISMA", canvas.width/2, canvas.height/2 - 20);
                    ctx.fillStyle = var("--neon-blue");
                    ctx.fillText("YENIDEN BASLAT (TIKLA)", canvas.width/2, canvas.height/2 + 30);
                    return requestAnimationFrame(render);
                }}

                // Player Physics
                player.vel += player.gravity;
                player.y += player.vel;

                // Player Visual
                ctx.shadowBlur = 20; ctx.shadowColor = var("--neon-blue");
                ctx.fillStyle = var("--neon-blue");
                ctx.fillRect(50, player.y, player.w, player.h);
                ctx.shadowBlur = 0;

                // obstacle Logic
                if(frames % 100 === 0) {{
                    let gap = 175;
                    let h = Math.random() * (canvas.height - gap - 200) + 100;
                    obstacles.push({{ x: canvas.width, h: h, g: gap, s: false }});
                }}

                for(let i = obstacles.length - 1; i >= 0; i--) {{
                    let o = obstacles[i];
                    o.x -= 4.5;

                    ctx.fillStyle = "#080808";
                    ctx.fillRect(o.x, 0, 70, o.h);
                    ctx.fillRect(o.x, o.h + o.g, 70, canvas.height);

                    // Collision Detection
                    if(50 + player.w > o.x && 50 < o.x + 70) {{
                        if(player.y < o.h || player.y + player.h > o.h + o.g) endGame();
                    }}

                    if(o.x < 50 && !o.s) {{
                        currentScore++; o.s = true;
                        liveScore.innerText = currentScore;
                    }}

                    if(o.x < -100) obstacles.splice(i, 1);
                }}

                if(player.y > canvas.height || player.y < 0) endGame();

                frames++;
                requestAnimationFrame(render);
            }}

            // Universal Controls
            window.addEventListener("keydown", (e) => {{
                if(e.code === "Space") {{
                    e.preventDefault();
                    if(isPlaying) player.vel = player.jump; else startup();
                }}
            }});

            window.addEventListener("pointerdown", (e) => {{
                if(isPlaying) player.vel = player.jump; else startup();
            }});

            startup();
            render();
        </script>
    </body>
    </html>
    """
    return html_page

# ------------------------------------------------------------------------------
# 7. LOST FOREST (RAYCASTING ENGINE)
# ------------------------------------------------------------------------------
# 3D derinlik algısı yaratan raycasting motoru.
# ------------------------------------------------------------------------------
@app.route('/lost-forest')
def route_horror():
    html_page = f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_universal_head()}
    <body style="overflow:hidden; margin:0; background:#000; touch-action:none;">
        {support_overlay_html}
        <a href="/" class="btn-action" style="position:fixed; top:25px; left:25px; z-index:9000;">← ÇIKIŞ YAP</a>

        <div id="mobile-joystick-ui" style="position:fixed; bottom:50px; left:50px; width:130px; height:130px; background:rgba(255,255,255,0.03); border:1px solid #111; border-radius:50%; z-index:100;">
            <div id="inner-stick" style="position:absolute; top:45px; left:45px; width:40px; height:40px; background:var(--neon-blue); opacity:0.2; border-radius:50%;"></div>
        </div>

        <div style="position:fixed; top:80px; width:100%; text-align:center; color:#fff; font-family:monospace; z-index:10; letter-spacing:4px; opacity:0.4;">
            LOCATION: SECTOR_<span id="lvl-num">1</span> | RADAR_SIGN: <span id="radar">STABLE</span>
        </div>

        <canvas id="horrorCanvas"></canvas>

        <script>
            /**
             * LOST FOREST 3D ENGINE
             * PC: WASD / Ok Tuşları
             * Mobil: Sol Joystick
             */
            const canvas = document.getElementById("horrorCanvas");
            const ctx = canvas.getContext("2d");
            const lvlLabel = document.getElementById("lvl-num");

            let level = 1;
            let maze = [];
            let p = {{ x: 1.5, y: 1.5, dir: 0, speed: 0.045, fov: Math.PI / 3 }};
            let keys = {{}};
            let joystick = {{ active: false, x: 0, y: 0 }};

            function createMaze(s) {{
                let m = Array.from({{ length: s }}, () => Array(s).fill(1));
                for(let y=1; y<s-1; y++) {{
                    for(let x=1; x<s-1; x++) {{
                        if(Math.random() > 0.4) m[y][x] = 0;
                    }}
                }}
                m[1][1] = 0;
                m[s-2][s-2] = 2; // Çıkış noktası
                return m;
            }}

            function initWorld() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                maze = createMaze(10 + (level * 2));
                p.x = 1.5; p.y = 1.5;
                lvlLabel.innerText = level;
            }}

            // PC Controls
            window.addEventListener("keydown", (e) => keys[e.code] = true);
            window.addEventListener("keyup", (e) => keys[e.code] = false);

            // Mobil Controls
            const jBox = document.getElementById("mobile-joystick-ui");
            const jStick = document.getElementById("inner-stick");

            jBox.addEventListener("touchstart", () => joystick.active = true);
            jBox.addEventListener("touchmove", (e) => {{
                e.preventDefault();
                let touch = e.touches[0];
                let rect = jBox.getBoundingClientRect();
                let dx = touch.clientX - (rect.left + 65);
                let dy = touch.clientY - (rect.top + 65);
                let dist = Math.min(Math.hypot(dx, dy), 55);
                let angle = Math.atan2(dy, dx);
                
                joystick.x = Math.cos(angle) * (dist / 55);
                joystick.y = Math.sin(angle) * (dist / 55);
                jStick.style.transform = `translate(${{joystick.x * 40}}px, ${{joystick.y * 40}}px)`;
            }});
            jBox.addEventListener("touchend", () => {{
                joystick.active = false;
                jStick.style.transform = "translate(0,0)";
            }});

            function update() {{
                let oldX = p.x, oldY = p.y;
                
                // Klavye ve Joystick Hareket Birleştirme
                let moveX = 0, moveY = 0, turn = 0;

                if(keys['KeyW'] || keys['ArrowUp']) moveY = 1;
                if(keys['KeyS'] || keys['ArrowDown']) moveY = -1;
                if(keys['KeyA'] || keys['ArrowLeft']) turn = -1;
                if(keys['KeyD'] || keys['ArrowRight']) turn = 1;

                if(joystick.active) {{
                    if(Math.abs(joystick.y) > 0.2) moveY = -joystick.y * 1.5;
                    if(Math.abs(joystick.x) > 0.2) turn = joystick.x;
                }}

                p.dir += turn * 0.055;
                p.x += Math.cos(p.dir) * moveY * p.speed;
                p.y += Math.sin(p.dir) * moveY * p.speed;

                // Collision
                if(maze[Math.floor(p.y)][Math.floor(p.x)] === 1) {{
                    p.x = oldX; p.y = oldY;
                }}

                // Exit Logic
                if(maze[Math.floor(p.y)][Math.floor(p.x)] === 2) {{
                    level++;
                    fetch('/api/submit/' + level + '/lost_forest');
                    initWorld();
                }}
            }}

            function draw() {{
                ctx.fillStyle = "#000"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                const numRays = 120;
                for(let i=0; i<numRays; i++) {{
                    let angle = (p.dir - p.fov/2) + (i / numRays) * p.fov;
                    let d = 0;
                    while(d < 14) {{
                        d += 0.08;
                        let tx = Math.floor(p.x + Math.cos(angle) * d);
                        let ty = Math.floor(p.y + Math.sin(angle) * d);
                        if(maze[ty] && maze[ty][tx] > 0) break;
                    }}
                    d *= Math.cos(angle - p.dir);
                    let h = canvas.height / d;
                    let c = Math.max(0, 160 - (d * 12));
                    ctx.fillStyle = `rgb(0, ${{c}}, 0)`;
                    ctx.fillRect(i * (canvas.width/numRays), (canvas.height - h)/2, (canvas.width/numRays)+1, h);
                }}

                // Vignette Effect
                let grad = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 100, canvas.width/2, canvas.height/2, canvas.width);
                grad.addColorStop(0, "transparent"); grad.addColorStop(1, "rgba(0,0,0,0.9)");
                ctx.fillStyle = grad; ctx.fillRect(0, 0, canvas.width, canvas.height);
            }}

            function frame() {{ update(); draw(); requestAnimationFrame(frame); }}
            window.addEventListener("resize", initWorld);
            initWorld();
            frame();
        </script>
    </body>
    </html>
    """
    return html_page

# ------------------------------------------------------------------------------
# 8. API KATMANI (BACKEND)
# ------------------------------------------------------------------------------
# Oyunlardan gelen skorları veritabanına işleyen API uç noktaları.
# ------------------------------------------------------------------------------
@app.route('/api/submit/<int:val>/<game_id>')
def api_submit(val, game_id):
    """
    Skorları işler ve XP puanına dönüştürür.
    """
    if game_id == "neon_arcade":
        user_data["neon_arcade"]["scores"].append(val)
        user_data["platform_stats"]["total_xp"] += (val * 15)
    elif game_id == "lost_forest":
        user_data["lost_forest"]["levels"].append(val)
        user_data["platform_stats"]["total_xp"] += (val * 100)
    elif game_id == "void_command":
        user_data["void_command"]["levels"].append(val)
        user_data["platform_stats"]["total_xp"] += (val * 80)
        
    return jsonify({
        "status": "success",
        "xp_updated": user_data["platform_stats"]["total_xp"]
    })

# ------------------------------------------------------------------------------
# 9. SUNUCU BAŞLATMA
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Render ortamı için dinamik port ataması
    server_port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=server_port)

# ==============================================================================
# CANO STUDIO KOD SONU. PROJE OMEGA SEVIYESINDEDIR.
# ==============================================================================
