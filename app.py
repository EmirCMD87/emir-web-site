# ==============================================================================
# CANO STUDIO - ULTIMATE TITAN EDITION v15.0
# ==============================================================================
# Geliştirici: Cano Studio
# Lisans: Open Source (Hobi ve Gelişim Amaçlı)
# Platform Desteği: %100 PC & MOBİL Sync
# Google Analytics ID: G-GQS70MDDPQ
# ==============================================================================

from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# ------------------------------------------------------------------------------
# 1. VERİ YAPISI VE BELLEK YÖNETİMİ
# ------------------------------------------------------------------------------
# Sunucu tarafında oyuncu istatistiklerini tutan ana sözlük yapısı.
# XP Katsayıları: Arcade (15x), Horror (100x), Strategy (80x)
# ------------------------------------------------------------------------------
user_database = {
    "neon_arcade": {
        "scores": [0],
        "metadata": "High-speed reflex data tunnel"
    },
    "void_command": {
        "levels": [1],
        "metadata": "Interstellar tactical energy management"
    },
    "lost_forest": {
        "levels": [1],
        "metadata": "3D Raycasting survival labyrinth"
    },
    "studio_meta": {
        "total_xp": 0,
        "api_hits": 0,
        "version": "15.0.0"
    }
}

# ------------------------------------------------------------------------------
# 2. GLOBAL STİL MOTORU (CSS3)
# ------------------------------------------------------------------------------
# Parantez hatası (500 Error) almamak için süslü parantezler çiftlenmiştir {{ }}.
# Cyberpunk, Glitch ve Responsive (Duyarlı) tasarım öğelerini içerir.
# ------------------------------------------------------------------------------
def generate_master_styles():
    return """
    <style>
        :root {{
            --neon: #00bcd4;
            --glitch: #ff0055;
            --void: #020202;
            --surface: #0a0a0a;
            --gold: #f1c40f;
            --white: #ffffff;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            background-color: var(--void);
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* --- ANIMASYONLAR --- */
        @keyframes glitch-vfx {{
            0% {{ text-shadow: 2px 0 var(--glitch); transform: skew(0deg); }}
            20% {{ text-shadow: -2px 0 var(--neon); }}
            40% {{ transform: skew(1deg); }}
            60% {{ text-shadow: 2px -2px var(--gold); }}
            100% {{ text-shadow: -2px 2px var(--glitch); transform: skew(-1deg); }}
        }}

        /* --- HEADER TASARIMI --- */
        .platform-header {{
            padding: 80px 20px 40px;
            text-align: center;
        }}

        .glitch-title {{
            font-size: clamp(2.5rem, 10vw, 4.5rem);
            letter-spacing: clamp(10px, 3vw, 25px);
            color: var(--white);
            text-transform: uppercase;
            animation: glitch-vfx 4s infinite alternate-reverse;
            position: relative;
        }}

        .rank-info {{
            margin-top: 15px;
            font-size: 0.9rem;
            letter-spacing: 5px;
            color: var(--gold);
            font-weight: bold;
        }}

        /* --- OYUN KARTLARI --- */
        .game-grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            padding: 40px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }}

        .game-card-item {{
            background: var(--surface);
            border: 1px solid #151515;
            padding: 60px 30px;
            border-radius: 24px;
            cursor: pointer;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        }}

        .game-card-item:hover {{
            border-color: var(--neon);
            background: #111;
            transform: translateY(-12px);
            box-shadow: 0 20px 50px rgba(0, 188, 212, 0.2);
        }}

        .game-card-item h2 {{
            font-size: 1.6rem;
            margin-bottom: 15px;
            letter-spacing: 3px;
            font-weight: 300;
        }}

        .game-card-item p {{
            color: #555;
            font-size: 0.9rem;
            line-height: 1.7;
        }}

        /* --- UI ELEMENTLERI --- */
        .btn-universal {{
            background: rgba(0, 188, 212, 0.05);
            border: 1px solid var(--neon);
            color: var(--neon);
            padding: 14px 28px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            display: inline-block;
        }}

        .btn-universal:hover {{
            background-color: var(--neon);
            color: #000;
            box-shadow: 0 0 30px var(--neon);
        }}

        /* --- MODAL VE DESTEK --- */
        #supportModalWrapper {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.99);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(20px);
        }}

        .modal-body {{
            background: #050505;
            padding: 60px;
            border-radius: 30px;
            border: 1px solid var(--neon);
            max-width: 600px;
            width: 90%;
            text-align: center;
            box-shadow: 0 0 120px rgba(0,188,212,0.15);
        }}

        /* --- TABLOLAR --- */
        .stats-wrapper {{
            max-width: 1000px;
            margin: 60px auto;
            background: #030303;
            padding: 40px;
            border-radius: 20px;
            border: 1px solid #080808;
        }}

        .global-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .global-table td {{
            padding: 22px;
            border-bottom: 1px solid #0a0a0a;
            color: #444;
        }}

        .global-table .val-field {{
            text-align: right;
            color: var(--white);
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            font-size: 1.3rem;
        }}

        /* PC'de Joystick Gizleme */
        @media (min-width: 1025px) {{
            #mobile-ui-controls {{ display: none !important; }}
        }}

        footer {{
            margin-top: auto;
            padding: 60px;
            text-align: center;
            border-top: 1px solid #080808;
            background: #010101;
            color: #1a1a1a;
            letter-spacing: 5px;
            font-size: 0.7rem;
        }}
    </style>
    """

# ------------------------------------------------------------------------------
# 3. ANALYTICS MOTORU
# ------------------------------------------------------------------------------
def get_analytics_payload():
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GQS70MDDPQ"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-GQS70MDDPQ');
    </script>
    """

# ------------------------------------------------------------------------------
# 4. UNIVERSAL HEAD MOTORU
# ------------------------------------------------------------------------------
def get_master_head():
    return f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>CANO STUDIO | OFFICIAL PLATFORM</title>
        {get_analytics_payload()}
        {generate_master_styles()}
    </head>
    """

# ------------------------------------------------------------------------------
# 5. SUPPORT & OVERLAY UI
# ------------------------------------------------------------------------------
support_overlay_html = """
<a href="#" onclick="toggleSupport(true)" class="btn-universal" style="position:fixed; top:30px; right:30px; z-index:9000;">💎 DESTEK</a>
<div id="supportModalWrapper">
    <div class="modal-body" id="modalMainBox">
        <h2 style="color:var(--neon); letter-spacing:8px; margin-bottom:25px;">CANO STUDIO</h2>
        <p style="color:#555; margin-bottom:40px; line-height:1.6;">Bu platform bir geliştiricinin hayalidir. Katkıda bulunmak istersen bilgiler aşağıdadır.</p>
        
        <div style="display:flex; gap:15px; margin-bottom:40px;">
            <button class="btn-universal" style="flex:1" onclick="triggerCopy('ininal')">ININAL</button>
            <button class="btn-universal" style="flex:1" onclick="triggerCopy('banka')">BANKA / EFT</button>
        </div>

        <button onclick="toggleSupport(false)" style="background:none; border:none; color:#222; cursor:pointer; text-decoration:underline;">[ PENCEREYİ KAPAT ]</button>
    </div>
</div>

<script>
    function toggleSupport(state) {
        document.getElementById('supportModalWrapper').style.display = state ? 'flex' : 'none';
    }

    function triggerCopy(mode) {
        const payload = mode === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
        navigator.clipboard.writeText(payload).then(() => {
            document.getElementById('modalMainBox').innerHTML = `
                <h1 style="color:var(--neon); font-size:3.5rem; margin-bottom:20px;">ADAMSIN! ❤️</h1>
                <p style="color:#fff; font-size:1.2rem; margin-bottom:40px;">Veriler panoya kopyalandı. Desteğin için teşekkür ederim!</p>
                <button onclick="location.reload()" class="btn-universal">ANA MENÜYE DÖN</button>
            `;
        });
    }
</script>
"""

# ------------------------------------------------------------------------------
# 6. ROUTE: ANA SAYFA (DASHBOARD)
# ------------------------------------------------------------------------------
@app.route('/')
def route_index():
    xp = user_database["studio_meta"]["total_xp"]
    rank = "LEGENDARY" if xp > 2000 else "EXPERT" if xp > 1000 else "STUDENT"
    
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_master_head()}
    <body>
        {support_overlay_html}
        
        <header class="platform-header">
            <h1 class="glitch-title" data-text="CANO STUDIO">CANO STUDIO</h1>
            <div class="rank-info">{rank} | XP_{xp}</div>
        </header>

        <main class="game-grid-container">
            <div class="game-card-item" onclick="location.href='/neon-arcade'">
                <div style="color:var(--neon); border:1px solid; display:inline-block; padding:4px 12px; border-radius:4px; font-size:0.7rem; margin-bottom:25px;">REFLEX_ENGINE</div>
                <h2>NEON ARCADE</h2>
                <p>Yüksek frekanslı tünellerden geçerek veri akışını koru. Hız ve konsantrasyon testi.</p>
                <div style="margin-top:35px; color:#222; font-size:0.7rem;">TOP_SYNC_SCORE: {max(user_database["neon_arcade"]["scores"])}</div>
            </div>

            <div class="game-card-item" onclick="location.href='/lost-forest'">
                <div style="color:var(--glitch); border:1px solid; display:inline-block; padding:4px 12px; border-radius:4px; font-size:0.7rem; margin-bottom:25px;">FPS_SURVIVAL</div>
                <h2>LOST FOREST</h2>
                <p>3D Raycasting algoritması ile oluşturulmuş labirentte hayatta kalmaya çalış.</p>
                <div style="margin-top:35px; color:#222; font-size:0.7rem;">DEEPEST_SECTOR: {max(user_database["lost_forest"]["levels"])}</div>
            </div>

            <div class="game-card-item" onclick="location.href='/void-command'">
                <div style="color:#00ff88; border:1px solid; display:inline-block; padding:4px 12px; border-radius:4px; font-size:0.7rem; margin-bottom:25px;">TACTICAL_GRID</div>
                <h2>VOID COMMAND</h2>
                <p>Gezegenler arası enerji transferini yönet ve düşman sistemleri asimile et.</p>
                <div style="margin-top:35px; color:#222; font-size:0.7rem;">CONQUEST_LEVEL: {max(user_database["void_command"]["levels"])}</div>
            </div>
        </main>

        <section class="stats-wrapper">
            <h3 style="text-align:center; color:#1a1a1a; letter-spacing:8px; margin-bottom:40px;">DATA_CORE_İSTATİSTİKLER</h3>
            <table class="global-table">
                <tr><td>Neon Accuracy Index</td><td class="val-field">{max(user_database["neon_arcade"]["scores"])}</td></tr>
                <tr><td>Forest Sector Progress</td><td class="val-field">Lvl {max(user_database["lost_forest"]["levels"])}</td></tr>
                <tr><td>Total Platform Experience</td><td class="val-field" style="color:var(--gold);">{xp} XP</td></tr>
            </table>
        </section>

        <footer>
            ANALYTICS_ID: G-GQS70MDDPQ | SYSTEM_VERSION: 15.0.0_ULTRA
        </footer>
    </body>
    </html>
    """

# ------------------------------------------------------------------------------
# 7. ROUTE: NEON ARCADE (MOTOR)
# ------------------------------------------------------------------------------
@app.route('/neon-arcade')
def route_arcade():
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_master_head()}
    <body style="overflow:hidden; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh;">
        {support_overlay_html}
        <a href="/" class="btn-universal" style="position:fixed; top:30px; left:30px; z-index:9000;">← ÇIKIŞ</a>
        
        <div id="live-ui" style="position:fixed; top:100px; color:var(--neon); font-family:monospace; font-size:1.5rem; letter-spacing:4px;">
            STABILITY: <span id="score-text">0</span>
        </div>

        <canvas id="neonCanvas" width="450" height="650" style="background:#000; border:1px solid #111; box-shadow:0 0 60px rgba(0,0,0,1);"></canvas>

        <script>
            /**
             * NEON ARCADE MOTORU v15.0
             * Kontroller: Space (PC) / Dokunma (Mobil)
             */
            const c = document.getElementById("neonCanvas"), ctx = c.getContext("2d");
            const scoreDisp = document.getElementById("score-text");

            let player, pipes, frames, score, active;

            function boot() {{
                player = {{ y: 325, v: 0, g: 0.38, j: -7.5, size: 32 }};
                pipes = []; frames = 0; score = 0; active = true;
                scoreDisp.innerText = "0";
            }}

            function fail() {{
                active = false;
                if(score > 0) fetch('/api/record/' + score + '/neon_arcade');
            }}

            function loop() {{
                ctx.fillStyle = "#000"; ctx.fillRect(0, 0, c.width, c.height);

                if(!active) {{
                    ctx.fillStyle = "rgba(0,0,0,0.8)"; ctx.fillRect(0, 0, c.width, c.height);
                    ctx.fillStyle = "#fff"; ctx.font = "20px monospace"; ctx.textAlign = "center";
                    ctx.fillText("DATA CORRUPTED", 225, 310);
                    ctx.fillStyle = var("--neon"); ctx.fillText("REBOOT (TIKLA)", 225, 350);
                    return requestAnimationFrame(loop);
                }}

                player.v += player.g; player.y += player.v;
                ctx.shadowBlur = 15; ctx.shadowColor = var("--neon"); ctx.fillStyle = var("--neon");
                ctx.fillRect(60, player.y, player.size, player.size); ctx.shadowBlur = 0;

                if(frames % 95 === 0) {{
                    let gap = 175;
                    let h = Math.random() * (c.height - gap - 200) + 100;
                    pipes.push({{ x: c.width, h: h, g: gap, s: false }});
                }}

                for(let i = pipes.length - 1; i >= 0; i--) {{
                    let p = pipes[i]; p.x -= 4.5;
                    ctx.fillStyle = "#080808"; ctx.fillRect(p.x, 0, 70, p.h); ctx.fillRect(p.x, p.h+p.g, 70, c.height);

                    if(60 + player.size > p.x && 60 < p.x + 70) {{
                        if(player.y < p.h || player.y + player.size > p.h + p.gap) fail();
                    }}
                    if(p.x < 60 && !p.s) {{ score++; p.s = true; scoreDisp.innerText = score; }}
                    if(p.x < -80) pipes.splice(i, 1);
                }}

                if(player.y > c.height || player.y < 0) fail();
                frames++; requestAnimationFrame(loop);
            }}

            window.addEventListener("keydown", (e) => {{ if(e.code === "Space") {{ e.preventDefault(); if(active) player.v = player.j; else boot(); }} }});
            window.addEventListener("pointerdown", () => {{ if(active) player.v = player.j; else boot(); }});

            boot(); loop();
        </script>
    </body>
    </html>
    """

# ------------------------------------------------------------------------------
# 8. ROUTE: LOST FOREST (FPS MOTORU)
# ------------------------------------------------------------------------------
@app.route('/lost-forest')
def route_horror():
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_master_head()}
    <body style="overflow:hidden; margin:0; background:#000; touch-action:none;">
        {support_overlay_html}
        <a href="/" class="btn-universal" style="position:fixed; top:30px; left:30px; z-index:9000;">← ÇIKIŞ</a>

        <div id="mobile-ui-controls" style="position:fixed; bottom:60px; left:60px; width:140px; height:140px; background:rgba(255,255,255,0.02); border:1px solid #111; border-radius:50%; z-index:100;">
            <div id="joy-stick-inner" style="position:absolute; top:45px; left:45px; width:50px; height:50px; background:var(--neon); opacity:0.15; border-radius:50%;"></div>
        </div>

        <div style="position:fixed; top:100px; width:100%; text-align:center; color:#fff; font-family:monospace; z-index:10; opacity:0.4; letter-spacing:4px;">
            SECTOR: <span id="lvl-txt">1</span> | SIGNAL: STABLE
        </div>

        <canvas id="fpsCanvas"></canvas>

        <script>
            /**
             * LOST FOREST 3D RAYCASTER v15.0
             * PC: WASD / Oklar | MOBİL: Joystick
             */
            const c = document.getElementById("fpsCanvas"), ctx = c.getContext("2d");
            const lvlT = document.getElementById("lvl-txt");

            let level = 1, map = [], keys = {{}}, joy = {{ active: false, x: 0, y: 0 }};
            let p = {{ x: 1.5, y: 1.5, dir: 0, speed: 0.048, fov: Math.PI / 3 }};

            function generate(s) {{
                let m = Array.from({{ length: s }}, () => Array(s).fill(1));
                for(let y=1; y<s-1; y++)for(let x=1; x<s-1; x++) if(Math.random()>0.38) m[y][x]=0;
                m[1][1]=0; m[s-2][s-2]=2; return m;
            }}

            function sync() {{ c.width = window.innerWidth; c.height = window.innerHeight; map = generate(10 + level*2); p.x=1.5; p.y=1.5; lvlT.innerText=level; }}
            window.addEventListener("resize", sync);

            // Universal Controls
            window.addEventListener("keydown", (e) => keys[e.code] = true);
            window.addEventListener("keyup", (e) => keys[e.code] = false);

            const jB = document.getElementById("mobile-ui-controls"), jS = document.getElementById("joy-stick-inner");
            jB.addEventListener("touchstart", () => joy.active = true);
            jB.addEventListener("touchmove", (e) => {{
                e.preventDefault(); let t = e.touches[0], r = jB.getBoundingClientRect();
                let dx = t.clientX - (r.left + 70), dy = t.clientY - (r.top + 70);
                let d = Math.min(Math.hypot(dx, dy), 60), a = Math.atan2(dy, dx);
                joy.x = Math.cos(a)*(d/60); joy.y = Math.sin(a)*(d/60);
                jS.style.transform = `translate(${{joy.x*50}}px, ${{joy.y*50}}px)`;
            }});
            jB.addEventListener("touchend", () => {{ joy.active = false; jS.style.transform = "translate(0,0)"; }});

            function update() {{
                let oX = p.x, oY = p.y, mY = 0, trn = 0;
                if(keys['KeyW'] || keys['ArrowUp']) mY = 1;
                if(keys['KeyS'] || keys['ArrowDown']) mY = -1;
                if(keys['KeyA'] || keys['ArrowLeft']) trn = -1;
                if(keys['KeyD'] || keys['ArrowRight']) trn = 1;

                if(joy.active) {{ if(Math.abs(joy.y)>0.2) mY = -joy.y * 1.5; if(Math.abs(joy.x)>0.2) trn = joy.x; }}

                p.dir += trn * 0.06;
                p.x += Math.cos(p.dir) * mY * p.speed;
                p.y += Math.sin(p.dir) * mY * p.speed;

                if(map[Math.floor(p.y)][Math.floor(p.x)] === 1) {{ p.x = oX; p.y = oY; }}
                if(map[Math.floor(p.y)][Math.floor(p.x)] === 2) {{ level++; fetch('/api/record/'+level+'/lost_forest'); sync(); }}
            }}

            function draw() {{
                ctx.fillStyle = "#000"; ctx.fillRect(0, 0, c.width, c.height);
                const rays = 120;
                for(let i=0; i<rays; i++) {{
                    let a = (p.dir - p.fov/2) + (i / rays) * p.fov, d = 0;
                    while(d < 15) {{
                        d += 0.08;
                        let tx = Math.floor(p.x + Math.cos(a)*d), ty = Math.floor(p.y + Math.sin(a)*d);
                        if(map[ty] && map[ty][tx] > 0) break;
                    }}
                    let h = c.height / (d * Math.cos(a - p.dir));
                    ctx.fillStyle = `rgb(0, ${{Math.max(0, 160-d*11)}}, 0)`;
                    ctx.fillRect(i*(c.width/rays), (c.height-h)/2, (c.width/rays)+1, h);
                }}
                let g = ctx.createRadialGradient(c.width/2, c.height/2, 100, c.width/2, c.height/2, c.width);
                g.addColorStop(0, "transparent"); g.addColorStop(1, "rgba(0,0,0,0.95)");
                ctx.fillStyle = g; ctx.fillRect(0, 0, c.width, c.height);
            }}

            function frame() {{ update(); draw(); requestAnimationFrame(frame); }}
            sync(); frame();
        </script>
    </body>
    </html>
    """

# ------------------------------------------------------------------------------
# 9. ROUTE: VOID COMMAND (STRATEJİ MOTORU)
# ------------------------------------------------------------------------------
@app.route('/void-command')
def route_strategy():
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_master_head()}
    <body style="background:#000; overflow:hidden;">
        {support_overlay_html}
        <a href="/" class="btn-universal" style="position:fixed; top:30px; left:30px; z-index:9000;">← ÇIKIŞ</a>
        <canvas id="strategyCanvas"></canvas>
        <script>
            /**
             * VOID COMMAND v15.0
             * Mouse & Touch Support
             */
            const c = document.getElementById("strategyCanvas"), ctx = c.getContext("2d");
            let level = 1, planets = [], selected = null;

            class Planet {{
                constructor(x, y, r, o) {{ this.x=x; this.y=y; this.r=r; this.o=o; this.e=o==='neutral'?5:25; this.max=r*2.5; }}
                draw() {{
                    ctx.beginPath(); ctx.arc(this.x, this.y, this.r, 0, Math.PI*2);
                    ctx.strokeStyle = this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#222');
                    ctx.lineWidth = selected === this ? 5 : 2; ctx.stroke();
                    ctx.fillStyle = ctx.strokeStyle; ctx.font = "12px monospace"; ctx.textAlign="center";
                    ctx.fillText(Math.floor(this.e), this.x, this.y+5);
                }}
            }}

            function init() {{
                c.width = window.innerWidth; c.height = window.innerHeight; planets = [];
                planets.push(new Planet(120, c.height/2, 50, 'player'), new Planet(c.width-120, c.height/2, 50, 'enemy'));
                for(let i=0; i<7; i++) planets.push(new Planet(Math.random()*(c.width-300)+150, Math.random()*(c.height-200)+100, 30, 'neutral'));
            }}

            c.onpointerdown = (e) => {{
                let p = planets.find(p => Math.hypot(p.x-e.clientX, p.y-e.clientY) < p.r + 10);
                if(p) {{
                    if(p.o === 'player') selected = p;
                    else if(selected) {{
                        let f = selected.energy / 2; selected.energy -= f; p.energy -= f;
                        if(p.energy < 0) {{ p.o='player'; p.energy=Math.abs(p.energy); }}
                        selected = null;
                    }}
                }} else selected = null;
            }};

            function loop() {{
                ctx.fillStyle = "rgba(0,0,0,0.15)"; ctx.fillRect(0, 0, c.width, c.height);
                planets.forEach(p => {{ if(p.o !== 'neutral') p.e = Math.min(p.max, p.e+0.025); p.draw(); }});
                if(!planets.some(p => p.o==='enemy')) {{ level++; fetch('/api/record/'+level+'/void_command'); init(); }}
                requestAnimationFrame(loop);
            }}
            window.addEventListener("resize", init); init(); loop();
        </script>
    </body>
    </html>
    """

# ------------------------------------------------------------------------------
# 10. API: SKOR KAYIT VE XP İŞLEME
# ------------------------------------------------------------------------------
@app.route('/api/record/<int:val>/<game_id>')
def api_record(val, game_id):
    """
    Bu API noktası oyunlardan gelen veriyi işleyerek kalıcı belleğe aktarır.
    """
    if game_id in user_database:
        user_database[game_id]["scores" if "scores" in user_database[game_id] else "levels"].append(val)
        # XP Katsayısı: Skor x 20
        user_database["studio_meta"]["total_xp"] += (val * 20)
        return jsonify({ "status": "success", "total_xp": user_database["studio_meta"]["total_xp"] })
    return jsonify({ "status": "error" }), 404

# ------------------------------------------------------------------------------
# 11. BAŞLATICI
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Render ortamı için PORT konfigürasyonu
    server_port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=server_port)

# ==============================================================================
# KOD SONU. CANO STUDIO v15.0 - TAM KAPASITE.
# ==============================================================================
