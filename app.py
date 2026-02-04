# ==============================================================================
# CANO STUDIO - FINAL ULTRA EDITION v15.5
# ==============================================================================
# Bu dosya tüm cihazlarla (PC & Mobil) uyumlu, 650+ satırlık bir oyun platformudur.
# Google Analytics Kimliği: G-GQS70MDDPQ
# Tasarım: Cyberpunk / Glitch / Studio Estetiği
# ==============================================================================

from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# --- SİSTEM VERİ MERKEZİ ---
# Sunucu tarafında tutulan geçici skor ve tecrübe puanı verileri.
game_database = {
    "neon_arcade": {"scores": [0]},
    "void_command": {"levels": [1]},
    "lost_forest": {"levels": [1]},
    "global_xp": 0,
    "platform_status": "OPERATIONAL"
}

# Google Analytics Kimliği (NameError'ı önlemek için burada tanımlandı)
GTAG_ID = "G-GQS70MDDPQ"

# --- PROFESYONEL TASARIM MOTORU (CSS) ---
# SyntaxError almamak için tüm süslü parantezler çiftlenmiştir {{ }}.
def get_studio_styles():
    return """
    <style>
        :root {{
            --neon-cyan: #00bcd4;
            --cyber-pink: #ff0055;
            --deep-void: #020202;
            --studio-gray: #0a0a0a;
            --xp-gold: #f1c40f;
            --white-text: #ffffff;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            touch-action: manipulation;
        }}

        body {{
            background-color: var(--deep-void);
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* --- GLITCH LOGO ANIMASYONU --- */
        .glitch-logo {{
            font-size: clamp(2.5rem, 10vw, 4.5rem);
            letter-spacing: 15px;
            color: var(--white-text);
            text-transform: uppercase;
            text-align: center;
            padding: 60px 20px;
            position: relative;
            animation: glitch-vfx 4s infinite alternate;
        }}

        @keyframes glitch-vfx {{
            0% {{ text-shadow: 3px 0 var(--cyber-pink); transform: skew(0deg); }}
            20% {{ text-shadow: -3px 0 var(--neon-cyan); transform: skew(0.5deg); }}
            40% {{ text-shadow: 2px 2px var(--xp-gold); }}
            100% {{ text-shadow: -3px -2px var(--cyber-pink); transform: skew(-0.5deg); }}
        }}

        /* --- OYUN KÜTÜPHANESİ DÜZENİ --- */
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            padding: 40px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }}

        .game-card {{
            background: var(--studio-gray);
            border: 1px solid #151515;
            padding: 50px 30px;
            border-radius: 20px;
            cursor: pointer;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        }}

        .game-card:hover {{
            border-color: var(--neon-cyan);
            background: #0f0f0f;
            transform: translateY(-10px);
            box-shadow: 0 20px 50px rgba(0, 188, 212, 0.2);
        }}

        .badge {{
            font-size: 10px;
            letter-spacing: 2px;
            border: 1px solid;
            display: inline-block;
            padding: 4px 12px;
            margin-bottom: 20px;
            border-radius: 4px;
            text-transform: uppercase;
        }}

        /* --- BUTON TASARIMLARI --- */
        .btn-action {{
            background: rgba(0, 188, 212, 0.05);
            border: 1px solid var(--neon-cyan);
            color: var(--neon-cyan);
            padding: 14px 28px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            display: inline-block;
        }}

        .btn-action:hover {{
            background-color: var(--neon-cyan);
            color: #000;
            box-shadow: 0 0 30px var(--neon-cyan);
        }}

        /* --- DESTEK MENÜSÜ --- */
        #supportModal {{
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.99);
            z-index: 9999;
            align-items: center; justify-content: center;
            backdrop-filter: blur(20px);
        }}

        .modal-inner {{
            background: #050505;
            padding: 60px 40px;
            border-radius: 30px;
            border: 1px solid var(--neon-cyan);
            max-width: 550px;
            width: 90%;
            text-align: center;
        }}

        /* --- İSTATİSTİK TABLOSU --- */
        .stats-section {{
            max-width: 900px;
            margin: 50px auto;
            background: #030303;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #111;
        }}

        .stats-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .stats-table td {{
            padding: 18px;
            border-bottom: 1px solid #080808;
            color: #555;
        }}

        .stats-table .val-cell {{
            text-align: right;
            color: #fff;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            font-size: 1.2rem;
        }}

        @media (min-width: 1025px) {{
            #mobile-joy-ui {{ display: none !important; }}
        }}

        footer {{
            margin-top: auto;
            padding: 50px;
            text-align: center;
            border-top: 1px solid #080808;
            background: #010101;
            color: #1a1a1a;
            letter-spacing: 5px;
            font-size: 0.7rem;
        }}
    </style>
    """

# --- ANALYTICS TAKİP ---
def get_analytics_code():
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GTAG_ID}');
    </script>
    """

# --- SAYFA BAŞLIK YAPILANDIRICISI ---
def get_head_content():
    return f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Cano Studio | Official Elite</title>
        {get_analytics_code()}
        {get_studio_styles()}
    </head>
    """

# --- ORTAK DESTEK BİLEŞENİ ---
support_component = """
<a href="#" onclick="openSupport(true)" class="btn-action" style="position:fixed; top:25px; right:25px; z-index:9000;">💎 DESTEK OL</a>
<div id="supportModal">
    <div class="modal-inner" id="modalTarget">
        <h2 style="color:var(--neon-cyan); letter-spacing:8px; margin-bottom:20px;">CANO STUDIO</h2>
        <p style="color:#666; margin-bottom:40px; font-size:0.9rem;">Projelerime destek olarak stüdyonun büyümesine katkıda bulunabilirsin.</p>
        
        <div style="display:flex; gap:15px; margin-bottom:40px;">
            <button class="btn-action" style="flex:1" onclick="processCopy('ininal')">ININAL</button>
            <button class="btn-action" style="flex:1" onclick="processCopy('banka')">BANKA / EFT</button>
        </div>

        <button onclick="openSupport(false)" style="background:none; border:none; color:#222; cursor:pointer; text-decoration:underline;">[ PENCEREYİ KAPAT ]</button>
    </div>
</div>

<script>
    function openSupport(show) { document.getElementById('supportModal').style.display = show ? 'flex' : 'none'; }
    function processCopy(mode) {
        const value = mode === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
        navigator.clipboard.writeText(value).then(() => {
            document.getElementById('modalTarget').innerHTML = `
                <h1 style="color:var(--neon-cyan); font-size:3rem; margin-bottom:20px;">ADAMSIN! ❤️</h1>
                <p style="color:#fff; font-size:1.1rem; line-height:1.6;">Veriler kopyalandı. Desteğin için teşekkürler!</p>
                <div style="margin-top:40px;">
                    <button onclick="location.reload()" class="btn-action">MENÜYE DÖN</button>
                </div>
            `;
        });
    }
</script>
"""

# --- ANA SAYFA ---
@app.route('/')
def home_index():
    xp = game_database["global_xp"]
    rank = "LEGEND" if xp > 2000 else "EXPERT" if xp > 1000 else "STUDENT"
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {get_head_content()}
    <body>
        {support_component}
        <header>
            <h1 class="glitch-logo" data-text="CANO STUDIO">CANO STUDIO</h1>
            <div style="text-align:center; margin-top:-30px; letter-spacing:5px; color:var(--xp-gold); font-weight:bold;">
                {rank} | EXPERIENCE: {xp} XP
            </div>
        </header>

        <main class="grid-container">
            <div class="game-card" onclick="location.href='/neon-arcade'">
                <div class="badge" style="color:var(--neon-cyan); border-color:var(--neon-cyan);">ARCADE / SPEED</div>
                <h2>NEON ARCADE</h2>
                <p>Yüksek hızlı tünelde engelleri aş. PC: SPACE | MOBIL: DOKUN</p>
                <div style="margin-top:30px; border-top:1px solid #111; padding-top:15px; font-size:0.7rem; color:#222;">MAX_SCORE: {max(game_database["neon_arcade"]["scores"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/lost-forest'">
                <div class="badge" style="color:var(--cyber-pink); border-color:var(--cyber-pink);">FPS / 3D</div>
                <h2>LOST FOREST</h2>
                <p>Raycasting motoru ile 3D labirent keşfi. PC: WASD | MOBIL: JOYSTICK</p>
                <div style="margin-top:30px; border-top:1px solid #111; padding-top:15px; font-size:0.7rem; color:#222;">SURVIVAL: {max(game_database["lost_forest"]["levels"])}</div>
            </div>

            <div class="game-card" onclick="location.href='/void-command'">
                <div class="badge" style="color:#00ff88; border-color:#00ff88;">STRATEGY / TACTICS</div>
                <h2>VOID COMMAND</h2>
                <p>Gezegenler arası fetih stratejisi. Rakip sistemleri asimile et.</p>
                <div style="margin-top:30px; border-top:1px solid #111; padding-top:15px; font-size:0.7rem; color:#222;">CONQUEST: {max(game_database["void_command"]["levels"])}</div>
            </div>
        </main>

        <section class="stats-section">
            <h3 style="text-align:center; color:#222; letter-spacing:5px; margin-bottom:30px;">KÜRESEL İSTATİSTİK MERKEZİ</h3>
            <table class="stats-table">
                <tr><td>Neon Accuracy Index</td><td class="val-cell">{max(game_database["neon_arcade"]["scores"])} PTS</td></tr>
                <tr><td>Deep Forest Progression</td><td class="val-cell">Lvl {max(game_database["lost_forest"]["levels"])}</td></tr>
                <tr><td>Total Studio Experience</td><td class="val-cell" style="color:var(--xp-gold);">{xp} XP</td></tr>
            </table>
        </section>

        <footer>
            <p style="margin-bottom:10px;">ANALYTICS: {GTAG_ID}</p>
            © 2026 CANO STUDIO DIGITAL ENTERTAINMENT.
        </footer>
    </body>
    </html>
    """

# --- NEON ARCADE ---
@app.route('/neon-arcade')
def arcade_module():
    return f"""
    <!DOCTYPE html><html>{get_head_content()}
    <body style="overflow:hidden; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh;">
        {support_component}
        <a href="/" class="btn-action" style="position:fixed; top:25px; left:25px; z-index:9000;">← ÇIKIŞ YAP</a>
        <div style="position:fixed; top:80px; color:var(--neon-cyan); font-family:monospace; font-size:1.4rem; letter-spacing:4px;">BUFFER_SCORE: <span id="sDisplay">0</span></div>
        <canvas id="canvasA" width="450" height="650" style="background:#000; border:1px solid #111;"></canvas>
        <script>
            const c=document.getElementById("canvasA"), ctx=c.getContext("2d");
            let player, pipes, frames, score, active;
            function start() {{ player={{y:300,v:0,g:0.35,j:-7.2,w:32,h:32}}; pipes=[]; frames=0; score=0; active=true; }}
            function end() {{ active=false; if(score>0) fetch('/api/xp/'+score+'/neon_arcade'); }}
            function render() {{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,450,650);
                if(!active) {{ ctx.fillStyle="rgba(0,0,0,0.8)"; ctx.fillRect(0,0,450,650); ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText("OYUN BİTTİ - TIKLA", 225, 325); return requestAnimationFrame(render); }}
                player.v+=player.g; player.y+=player.v; ctx.fillStyle="#00bcd4"; ctx.fillRect(50,player.y,player.w,player.h);
                if(frames%100===0) pipes.push({{x:450,h:Math.random()*300+100,p:false}});
                pipes.forEach((p,i)=>{{ p.x-=4.2; ctx.fillStyle="#080808"; ctx.fillRect(p.x,0,65,p.h); ctx.fillRect(p.x,p.h+170,65,650);
                if(50+player.w>p.x && 50<p.x+65 && (player.y<p.h || player.y+player.h>p.h+170)) end();
                if(p.x<50 && !p.p){{ score++; p.p=true; document.getElementById('sDisplay').innerText=score; }}
                if(p.x<-70) pipes.splice(i,1); }});
                if(player.y>650 || player.y<0) end(); frames++; requestAnimationFrame(render);
            }}
            window.addEventListener("keydown",(e)=>{{ if(e.code==="Space") {{ e.preventDefault(); if(active) player.v=player.j; else start(); }} }});
            window.addEventListener("pointerdown",()=>{{ if(active) player.v=player.j; else start(); }});
            start(); render();
        </script>
    </body></html>
    """

# --- LOST FOREST ---
@app.route('/lost-forest')
def horror_module():
    return f"""
    <!DOCTYPE html><html>{get_head_content()}
    <body style="overflow:hidden; margin:0; background:#000; touch-action:none;">
        {support_component}
        <a href="/" class="btn-action" style="position:fixed; top:25px; left:25px; z-index:9000;">← ÇIKIŞ YAP</a>
        <div id="mobile-joy-ui" style="position:fixed; bottom:60px; left:60px; width:130px; height:130px; background:rgba(255,255,255,0.03); border:1px solid #111; border-radius:50%; z-index:100;">
            <div id="innerStick" style="position:absolute; top:45px; left:45px; width:40px; height:40px; background:var(--neon-cyan); opacity:0.2; border-radius:50%;"></div>
        </div>
        <div style="position:fixed; top:80px; width:100%; text-align:center; color:#fff; font-family:monospace; opacity:0.4; letter-spacing:4px;">SECTOR: <span id="lvlDisp">1</span></div>
        <canvas id="canvasV"></canvas>
        <script>
            const c=document.getElementById("canvasV"), ctx=c.getContext("2d");
            let level=1, map=[], p={{x:1.5,y:1.5,dir:0,speed:0.045,fov:Math.PI/3}}, keys={{}}, joy={{active:false,x:0,y:0}};
            function genMap(s){{ let m=Array.from({{length:s}},()=>Array(s).fill(1)); for(let y=1;y<s-1;y++)for(let x=1;x<s-1;x++)if(Math.random()>0.4)m[y][x]=0; m[1][1]=0; m[s-2][s-2]=2; return m; }}
            function reset(){{ c.width=window.innerWidth; c.height=window.innerHeight; map=genMap(10+level*2); p.x=1.5; p.y=1.5; document.getElementById('lvlDisp').innerText=level; }}
            window.addEventListener("keydown",(e)=>keys[e.code]=true); window.addEventListener("keyup",(e)=>keys[e.code]=false);
            const jB=document.getElementById("mobile-joy-ui"), jS=document.getElementById("innerStick");
            jB.addEventListener("touchmove",(e)=>{{ e.preventDefault(); let t=e.touches[0], r=jB.getBoundingClientRect(); let dx=t.clientX-(r.left+65), dy=t.clientY-(r.top+65); let d=Math.min(Math.hypot(dx,dy),55), a=Math.atan2(dy,dx); joy.x=Math.cos(a)*(d/55); joy.y=Math.sin(a)*(d/55); jS.style.transform=`translate(${{joy.x*40}}px,${{joy.y*40}}px)`; joy.active=true; }}, {{passive:false}});
            jB.addEventListener("touchend",()=>{{ joy.active=false; jS.style.transform="translate(0,0)"; }});
            function update(){{
                let oX=p.x, oY=p.y, mY=0, tN=0;
                if(keys['KeyW']||keys['ArrowUp']) mY=1; if(keys['KeyS']||keys['ArrowDown']) mY=-1; if(keys['KeyA']||keys['ArrowLeft']) tN=-1; if(keys['KeyD']||keys['ArrowRight']) tN=1;
                if(joy.active){{ if(Math.abs(joy.y)>0.2) mY=-joy.y*1.5; if(Math.abs(joy.x)>0.2) tN=joy.x; }}
                p.dir+=tN*0.06; p.x+=Math.cos(p.dir)*mY*p.speed; p.y+=Math.sin(p.dir)*mY*p.speed;
                if(map[Math.floor(p.y)][Math.floor(p.x)]===1){{p.x=oX; p.y=oY;}}
                if(map[Math.floor(p.y)][Math.floor(p.x)]===2){{ level++; fetch('/api/xp/'+level+'/lost_forest'); reset(); }}
            }}
            function draw(){{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,c.width,c.height);
                for(let i=0;i<120;i++){{
                    let a=(p.dir-p.fov/2)+(i/120)*p.fov, d=0;
                    while(d<14){{ d+=0.08; let tx=Math.floor(p.x+Math.cos(a)*d), ty=Math.floor(p.y+Math.sin(a)*d); if(map[ty]&&map[ty][tx]>0)break; }}
                    let h=c.height/(d*Math.cos(a-p.dir)); ctx.fillStyle=`rgb(0,${{Math.max(0,160-d*12)}},0)`; ctx.fillRect(i*(c.width/120),(c.height-h)/2,c.width/120+1,h);
                }}
            }}
            function frame(){{ update(); draw(); requestAnimationFrame(frame); }}
            window.addEventListener("resize",reset); reset(); frame();
        </script>
    </body></html>
    """

# --- VOID COMMAND ---
@app.route('/void-command')
def strategy_module():
    return f"""
    <!DOCTYPE html><html>{get_head_content()}
    <body style="background:#000; overflow:hidden;">
        {support_component}
        <a href="/" class="btn-action" style="position:fixed; top:25px; left:25px; z-index:9000;">← ÇIKIŞ YAP</a>
        <canvas id="canvasG" style="width:100vw; height:100vh; background:#000; display:block;"></canvas>
        <script>
            const c=document.getElementById("canvasG"), ctx=c.getContext("2d");
            let level=1, planets=[], selected=null;
            class P {{ constructor(x,y,r,o){{this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:25;}} draw(){{ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#222'); ctx.lineWidth=selected===this?4:1; ctx.stroke(); ctx.fillStyle=ctx.strokeStyle; ctx.textAlign="center"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);}} }}
            function init(){{ c.width=window.innerWidth; c.height=window.innerHeight; planets=[new P(100,c.height/2,45,'player'), new P(c.width-100,c.height/2,45,'enemy')]; for(let i=0;i<7;i++) planets.push(new P(Math.random()*(c.width-200)+100, Math.random()*(c.height-200)+100, 30, 'neutral')); }}
            window.addEventListener("pointerdown",(e)=>{{ let p=planets.find(p=>Math.hypot(p.x-e.clientX,p.y-e.clientY)<p.r); if(p){{if(p.o==='player')selected=p; else if(selected){{let f=selected.e/2; selected.e-=f; p.e-=f; if(p.e<0){{p.o='player';p.e=Math.abs(p.e);}} selected=null;}} }}else selected=null; }});
            function loop(){{ ctx.fillStyle="rgba(0,0,0,0.15)"; ctx.fillRect(0,0,c.width,c.height); planets.forEach(p=>{{if(p.o!=='neutral')p.e+=0.02; p.draw();}}); if(!planets.some(p=>p.o==='enemy')){{level++; fetch('/api/xp/'+level+'/void_command'); init();}} requestAnimationFrame(loop); }}
            window.addEventListener("resize",init); init(); loop();
        </script>
    </body></html>
    """

# --- API SERVICES ---
@app.route('/api/xp/<int:val>/<game_id>')
def api_xp_handler(val, game_id):
    if game_id in game_database:
        target = "scores" if "scores" in game_database[game_id] else "levels"
        game_database[game_id][target].append(val)
        game_database["global_xp"] += (val * 15)
        return jsonify({"status": "success", "xp": game_database["global_xp"]})
    return jsonify({"status": "error"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
