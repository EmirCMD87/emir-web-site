# ==============================================================================
# CANO STUDIO - NEBULA EDITION v16.0
# ==============================================================================
# Geliştirici: Cano Studio
# Tema: Cyberpunk Neon / Deep Space
# Sistem: PC & Mobil Universal Controller
# Analytics: G-GQS70MDDPQ
# ==============================================================================

from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# --- STUDIO DATA ENGINE ---
# XP ve Skor verileri burada işlenir.
studio_data = {
    "neon_arcade": {"scores": [0]},
    "void_command": {"levels": [1]},
    "lost_forest": {"levels": [1]},
    "total_xp": 0,
    "current_rank": "ROOKIE"
}

GTAG_ID = "G-GQS70MDDPQ" #

# --- DESIGN SYSTEM (ADVANCED CSS) ---
# Tasarımı tamamen yenileyen devasa CSS bloğu.
def get_nebula_styles():
    return """
    <style>
        :root {{
            --accent: #00f2ff;
            --pink: #ff007f;
            --bg: #030305;
            --card-bg: rgba(15, 15, 25, 0.7);
            --gold: #ffcc00;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            touch-action: manipulation;
        }}

        body {{
            background: var(--bg);
            background-image: radial-gradient(circle at 50% 50%, #0a0a1a 0%, #030305 100%);
            color: #ffffff;
            font-family: 'Inter', -apple-system, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        /* --- GLITCH HEADER --- */
        .studio-header {{
            padding: 80px 20px;
            text-align: center;
            perspective: 1000px;
        }}

        .studio-title {{
            font-size: clamp(3rem, 12vw, 5rem);
            letter-spacing: 20px;
            text-transform: uppercase;
            font-weight: 900;
            color: #fff;
            text-shadow: 0 0 20px var(--accent);
            animation: nebula-float 6s ease-in-out infinite;
        }}

        @keyframes nebula-float {{
            0%, 100% {{ transform: translateY(0) rotateX(0); }}
            50% {{ transform: translateY(-10px) rotateX(5deg); }}
        }}

        /* --- MODERN GAMING CARDS --- */
        .library-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 40px;
            padding: 40px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }}

        .game-card {{
            position: relative;
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            padding: 60px 40px;
            overflow: hidden;
            cursor: pointer;
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .game-card::before {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
            transition: 0.5s;
        }}

        .game-card:hover {{
            transform: scale(1.05) translateY(-15px);
            border-color: var(--accent);
            box-shadow: 0 20px 60px rgba(0, 242, 255, 0.15);
        }}

        .game-card:hover::before {{ left: 100%; }}

        .game-icon {{
            font-size: 3rem;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 10px currentColor);
        }}

        .game-card h2 {{
            font-size: 1.8rem;
            letter-spacing: 4px;
            margin-bottom: 15px;
            font-weight: 800;
        }}

        .game-card p {{
            color: #888;
            font-size: 0.95rem;
            line-height: 1.6;
            text-align: center;
        }}

        /* --- XP & RANK UI --- */
        .rank-badge {{
            background: linear-gradient(45deg, var(--gold), #ff6600);
            padding: 5px 20px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: bold;
            color: #000;
            letter-spacing: 2px;
            margin-top: 10px;
            display: inline-block;
        }}

        /* --- STATS SECTION --- */
        .stats-panel {{
            max-width: 1000px;
            margin: 60px auto;
            padding: 40px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .stats-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .stats-table td {{
            padding: 25px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            font-size: 1.1rem;
            color: #666;
        }}

        .stats-table .val {{
            text-align: right;
            color: #fff;
            font-weight: bold;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* --- BUTTONS --- */
        .btn-nebula {{
            background: transparent;
            border: 2px solid var(--accent);
            color: var(--accent);
            padding: 15px 35px;
            border-radius: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 3px;
            cursor: pointer;
            text-decoration: none;
        }}

        .btn-nebula:hover {{
            background: var(--accent);
            color: #000;
            box-shadow: 0 0 30px var(--accent);
        }}

        @media (min-width: 1025px) {{
            #mobile-ui {{ display: none !important; }}
        }}

        footer {{
            margin-top: auto;
            padding: 60px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.7rem;
            color: #222;
            letter-spacing: 5px;
        }}
    </style>
    """

def get_gtag():
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GTAG_ID}');
    </script>
    """

def build_head():
    return f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Cano Studio | Nebula Platform</title>
        {get_gtag()}
        {get_nebula_styles()}
    </head>
    """

# --- OVERLAY COMPONENTS ---
support_ui = """
<a href="#" onclick="showM(true)" class="btn-nebula" style="position:fixed; top:30px; right:30px; z-index:9999;">💎 SUPPORT</a>
<div id="mOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.98); z-index:10000; align-items:center; justify-content:center;">
    <div class="stats-panel" id="mContent" style="max-width:550px; text-align:center;">
        <h2 style="color:var(--accent); letter-spacing:8px; margin-bottom:20px;">STUDIO SUPPORT</h2>
        <p style="color:#555; margin-bottom:30px;">Geliştirmeye devam etmemiz için bize destek olabilirsin.</p>
        <div style="display:flex; gap:15px; margin-bottom:40px;">
            <button class="btn-nebula" style="flex:1" onclick="copyAction('ininal')">ININAL</button>
            <button class="btn-nebula" style="flex:1" onclick="copyAction('banka')">BANKA</button>
        </div>
        <button onclick="showM(false)" style="background:none; border:none; color:#333; cursor:pointer; text-decoration:underline;">[ CLOSE ]</button>
    </div>
</div>
<script>
    function showM(s) { document.getElementById('mOverlay').style.display = s ? 'flex' : 'none'; }
    function copyAction(t) {
        const v = t === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
        navigator.clipboard.writeText(v).then(() => {
            document.getElementById('mContent').innerHTML = `
                <h1 style="color:var(--accent); font-size:3rem; margin-bottom:20px;">THANK YOU! ❤️</h1>
                <p style="color:#fff;">Veriler kopyalandı. Desteğin için teşekkürler!</p>
                <button onclick="location.reload()" class="btn-nebula" style="margin-top:30px;">DASHBOARD</button>
            `;
        });
    }
</script>
"""

# --- PAGE ROUTES ---
@app.route('/')
def home():
    xp = studio_data["total_xp"]
    rank = "ULTRA" if xp > 2000 else "EXPERIENCE" if xp > 800 else "ROOKIE"
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {build_head()}
    <body>
        {support_ui}
        <header class="studio-header">
            <h1 class="studio-title">CANO STUDIO</h1>
            <div class="rank-badge">{rank} | TOTAL EXP: {xp}</div>
        </header>

        <main class="library-grid">
            <div class="game-card" onclick="location.href='/neon-arcade'">
                <div class="game-icon" style="color:var(--accent);">⚡</div>
                <h2>NEON ARCADE</h2>
                <p>Yüksek hızda veri tünellerinden geç ve engelleri aş. PC: SPACE | MOBIL: TOUCH</p>
                <div style="margin-top:30px; font-weight:bold; color:var(--accent);">BEST: {max(studio_data["neon_arcade"]["scores"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/lost-forest'">
                <div class="game-icon" style="color:var(--pink);">👁️</div>
                <h2>LOST FOREST</h2>
                <p>3D Raycasting motoru ile karanlık labirent keşfi. PC: WASD | MOBIL: JOYSTICK</p>
                <div style="margin-top:30px; font-weight:bold; color:var(--pink);">SECTOR: {max(studio_data["lost_forest"]["levels"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/void-command'">
                <div class="game-icon" style="color:#00ff88;">🛡️</div>
                <h2>VOID COMMAND</h2>
                <p>Gezegenler arası stratejik fetih motoru. Rakip sistemleri ele geçir.</p>
                <div style="margin-top:30px; font-weight:bold; color:#00ff88;">CONQUEST: {max(studio_data["void_command"]["levels"])}</div>
            </div>
        </main>

        <section class="stats-panel">
            <table class="stats-table">
                <tr><td>Neon Accuracy Index</td><td class="val">{max(studio_data["neon_arcade"]["scores"])} PTS</td></tr>
                <tr><td>Deep Forest Survival</td><td class="val">Lvl {max(studio_data["lost_forest"]["levels"])}</td></tr>
                <tr><td>Global System Experience</td><td class="val" style="color:var(--gold);">{xp} XP</td></tr>
            </table>
        </section>

        <footer>
            ANALYTICS_ID: {GTAG_ID} | CONNECTION: ENCRYPTED
        </footer>
    </body>
    </html>
    """

# --- GAME: NEON ARCADE ---
@app.route('/neon-arcade')
def arcade():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh;">
        {support_ui}
        <a href="/" class="btn-nebula" style="position:fixed; top:30px; left:30px; z-index:9999;">← BACK</a>
        <canvas id="cA" width="450" height="650" style="background:#000; border-radius:20px; box-shadow:0 0 50px rgba(0,0,0,1);"></canvas>
        <script>
            const c=document.getElementById("cA"), ctx=c.getContext("2d");
            let p, pipes, frames, score, active;
            function start() {{ p={{y:300,v:0,g:0.38,j:-7.2,s:32}}; pipes=[]; frames=0; score=0; active=true; }}
            function end() {{ active=false; if(score>0) fetch('/api/xp/'+score+'/neon_arcade'); }}
            function draw() {{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,450,650);
                if(!active) {{ ctx.fillStyle="rgba(0,0,0,0.8)"; ctx.fillRect(0,0,450,650); ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText("SYSTEM FAILURE - TIKLA", 225, 325); return requestAnimationFrame(draw); }}
                p.v+=p.g; p.y+=p.v; ctx.fillStyle="#00f2ff"; ctx.fillRect(50,p.y,p.s,p.s);
                if(frames%100===0) pipes.push({{x:450,h:Math.random()*300+100,p:false}});
                pipes.forEach((pipe,i)=>{{ pipe.x-=4; ctx.fillStyle="#111"; ctx.fillRect(pipe.x,0,60,pipe.h); ctx.fillRect(pipe.x,pipe.h+170,60,650);
                if(50+p.s>pipe.x && 50<pipe.x+60 && (p.y<pipe.h || p.y+p.s>pipe.h+170)) end();
                if(pipe.x<50 && !pipe.p){{ score++; pipe.p=true; }}
                if(pipe.x<-70) pipes.splice(i,1); }});
                if(p.y>650 || p.y<0) end(); frames++; requestAnimationFrame(draw);
            }}
            window.addEventListener("keydown",(e)=>{{ if(e.code==="Space") {{ e.preventDefault(); if(active) p.v=p.j; else start(); }} }});
            window.addEventListener("pointerdown",()=>{{ if(active) p.v=p.j; else start(); }});
            start(); draw();
        </script>
    </body></html>
    """

# --- GAME: LOST FOREST ---
@app.route('/lost-forest')
def horror():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="overflow:hidden; margin:0; background:#000; touch-action:none;">
        {support_ui}
        <a href="/" class="btn-nebula" style="position:fixed; top:30px; left:30px; z-index:9999;">← BACK</a>
        <div id="mobile-ui" style="position:fixed; bottom:60px; left:60px; width:130px; height:130px; background:rgba(255,255,255,0.03); border:1px solid #111; border-radius:50%; z-index:100;">
            <div id="jStick" style="position:absolute; top:45px; left:45px; width:40px; height:40px; background:var(--accent); opacity:0.2; border-radius:50%;"></div>
        </div>
        <canvas id="cV"></canvas>
        <script>
            const canvas=document.getElementById("cV"), ctx=canvas.getContext("2d");
            let level=1, map=[], player={{x:1.5,y:1.5,dir:0,speed:0.045,fov:Math.PI/3}}, keys={{}}, joy={{active:false,x:0,y:0}};
            function gen(s){{ let m=Array.from({{length:s}},()=>Array(s).fill(1)); for(let y=1;y<s-1;y++)for(let x=1;x<s-1;x++)if(Math.random()>0.4)m[y][x]=0; m[1][1]=0; m[s-2][s-2]=2; return m; }}
            function reset(){{ canvas.width=window.innerWidth; canvas.height=window.innerHeight; map=gen(10+level*2); player.x=1.5; player.y=1.5; }}
            window.addEventListener("keydown",(e)=>keys[e.code]=true); window.addEventListener("keyup",(e)=>keys[e.code]=false);
            const jB=document.getElementById("mobile-ui"), jS=document.getElementById("jStick");
            jB.addEventListener("touchmove",(e)=>{{ e.preventDefault(); let t=e.touches[0], r=jB.getBoundingClientRect(); let dx=t.clientX-(r.left+65), dy=t.clientY-(r.top+65); let d=Math.min(Math.hypot(dx,dy),55), a=Math.atan2(dy,dx); joy.x=Math.cos(a)*(d/55); joy.y=Math.sin(a)*(d/55); jS.style.transform=`translate(${{joy.x*40}}px,${{joy.y*40}}px)`; joy.active=true; }}, {{passive:false}});
            jB.addEventListener("touchend",()=>{{ joy.active=false; jS.style.transform="translate(0,0)"; }});
            function update(){{
                let oX=player.x, oY=player.y, mY=0, tN=0;
                if(keys['KeyW']) mY=1; if(keys['KeyS']) mY=-1; if(keys['KeyA']) tN=-1; if(keys['KeyD']) tN=1;
                if(joy.active){{ if(Math.abs(joy.y)>0.2) mY=-joy.y*1.5; if(Math.abs(joy.x)>0.2) tN=joy.x; }}
                player.dir+=tN*0.06; player.x+=Math.cos(player.dir)*mY*player.speed; player.y+=Math.sin(player.dir)*mY*player.speed;
                if(map[Math.floor(player.y)][Math.floor(player.x)]===1){{player.x=oX; player.y=oY;}}
                if(map[Math.floor(player.y)][Math.floor(player.x)]===2){{ level++; fetch('/api/xp/'+level+'/lost_forest'); reset(); }}
            }}
            function draw(){{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,canvas.width,canvas.height);
                for(let i=0;i<120;i++){{
                    let a=(player.dir-player.fov/2)+(i/120)*player.fov, d=0;
                    while(d<14){{ d+=0.08; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d); if(map[ty]&&map[ty][tx]>0)break; }}
                    let h=canvas.height/(d*Math.cos(a-player.dir)); ctx.fillStyle=`rgb(0,${{Math.max(0,160-d*12)}},0)`; ctx.fillRect(i*(canvas.width/120),(canvas.height-h)/2,canvas.width/120+1,h);
                }}
            }}
            function frame(){{ update(); draw(); requestAnimationFrame(frame); }}
            window.addEventListener("resize",reset); reset(); frame();
        </script>
    </body></html>
    """

# --- API SERVICES ---
@app.route('/api/xp/<int:val>/<game_id>')
def api_xp(val, game_id):
    if game_id in studio_data:
        target = "scores" if "scores" in studio_data[game_id] else "levels"
        studio_data[game_id][target].append(val)
        studio_data["total_xp"] += (val * 20)
        return jsonify({"status": "success", "xp": studio_data["total_xp"]})
    return jsonify({"status": "error"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
