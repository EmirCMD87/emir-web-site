from flask import Flask, request, jsonify
import os, random

app = Flask(__name__)

# --- VERİTABANI (XP VE SKORLAR) ---
scores = {
    "neon_arcade": [0],
    "void_command": [1],
    "lost_forest": [1],
    "xp": 0
}

# --- GOOGLE ANALYTICS & GLOBAL STYLE ---
GTAG_ID = "G-GQS70MDDPQ"

global_head = f"""
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GTAG_ID}');
    </script>
    <style>
        :root {{ --neon: #00bcd4; --dark: #020202; --glitch: #ff0055; --gold: #f1c40f; }}
        * {{ box-sizing: border-box; transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); touch-action: manipulation; }}
        body {{ 
            background: var(--dark); color: #e0e0e0; font-family: 'Segoe UI', sans-serif; 
            margin: 0; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden;
        }}
        .glitch-header {{ font-size: 3rem; letter-spacing: 15px; color: #fff; position: relative; animation: glitch 3s infinite; }}
        @keyframes glitch {{
            0% {{ text-shadow: 2px 2px var(--glitch); }}
            25% {{ text-shadow: -2px -2px var(--neon); }}
            50% {{ text-shadow: 2px -2px var(--glitch); }}
            100% {{ text-shadow: -2px 2px var(--neon); }}
        }}
        .game-card {{ 
            background: #080808; border: 1px solid #151515; padding: 40px; border-radius: 12px; 
            cursor: pointer; position: relative; overflow: hidden; text-align: center;
        }}
        .game-card:hover {{ border-color: var(--neon); background: #0c0c0c; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,188,212,0.1); }}
        .game-card::before {{
            content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(0,188,212,0.05) 0%, transparent 70%);
        }}
        .btn-ui {{ 
            background: rgba(0, 188, 212, 0.05); border: 1px solid var(--neon); color: var(--neon);
            padding: 10px 20px; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 0.8rem; font-weight: bold;
        }}
        .btn-ui:hover {{ background: var(--neon); color: #000; box-shadow: 0 0 20px var(--neon); }}
        
        /* Gelişmiş Destek Sistemi */
        #supportModal {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.97); z-index:2000; align-items:center; justify-content:center; }}
        .modal-box {{ background:#0a0a0a; padding:40px; border-radius:15px; border:1px solid var(--neon); max-width:500px; width:90%; }}
        .tab-btn {{ flex:1; padding:12px; border:1px solid #222; background:transparent; color:#666; cursor:pointer; font-weight:bold; }}
        .tab-btn.active {{ border-color:var(--neon); color:var(--neon); background:rgba(0,188,212,0.1); }}
    </style>
</head>
"""

back_btn = '<a href="/" class="btn-ui" style="position:fixed; top:20px; left:20px; z-index:1000;">← MENÜ</a>'

support_html = """
<a href="#" onclick="showSupport()" class="btn-ui" style="position:fixed; top:20px; right:20px; z-index:1000;">💎 DESTEK</a>
<div id="supportModal">
    <div class="modal-box" id="supportBox">
        <h2 style="color:var(--neon); margin-top:0;">CANO STUDIO DESTEK</h2>
        <p style="color:#555; font-size:0.8rem;">Geliştirdiğim oyunları sevdiysen bir kahve ısmarlayabilirsin!</p>
        <div style="display:flex; gap:5px; margin:25px 0;">
            <button class="tab-btn active" id="bIninal" onclick="tab('ininal')">ininal</button>
            <button class="tab-btn" id="bBanka" onclick="tab('banka')">Banka/EFT</button>
        </div>
        <div id="pIninal">
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin-bottom:20px;">
                <button class="btn-ui" onclick="donate('ininal', 10)">10 TL</button>
                <button class="btn-ui" onclick="donate('ininal', 50)">50 TL</button>
                <button class="btn-ui" onclick="donate('ininal', 100)">100 TL</button>
            </div>
            <div style="background:#000; padding:15px; border:1px dashed #333; font-weight:bold;">BARKOD: 4000 0000 0000 0</div>
        </div>
        <div id="pBanka" style="display:none">
            <div style="background:#000; padding:20px; text-align:left; font-size:0.8rem; border-radius:8px; border:1px solid #222;">
                <b>ALICI:</b> CANO STUDIO / [İSMİNİZ]<br>
                <b>IBAN:</b> TR00 0000 0000 0000 0000 0000 00<br>
                <p style="color:red; font-size:0.7rem; margin-top:10px;">* Açıklamaya ininal barkodunuzu yazmayı unutmayın!</p>
            </div>
            <button class="btn-ui" style="width:100%; margin-top:15px;" onclick="donate('banka', 'IBAN')">IBAN KOPYALA</button>
        </div>
        <br><button onclick="hideSupport()" style="color:#333; background:none; border:none; cursor:pointer; text-decoration:underline;">[ Kapat ]</button>
    </div>
</div>
<script>
function showSupport() { document.getElementById('supportModal').style.display='flex'; }
function hideSupport() { document.getElementById('supportModal').style.display='none'; }
function tab(t) {
    document.getElementById('pIninal').style.display = t==='ininal'?'block':'none';
    document.getElementById('pBanka').style.display = t==='banka'?'block':'none';
    document.getElementById('bIninal').className = t==='ininal'?'tab-btn active':'tab-btn';
    document.getElementById('bBanka').className = t==='banka'?'tab-btn active':'tab-btn';
}
function donate(m, a) {
    const val = m==='ininal' ? "4000000000000" : "TR000000000000000000000000";
    navigator.clipboard.writeText(val);
    document.getElementById('supportBox').innerHTML = `<h2 style="color:var(--neon)">ADAMSIN! ❤️</h2><p>${a} desteğin için teşekkürler. Bilgiler kopyalandı!</p><button onclick="location.reload()" class="btn-ui">MENÜYE DÖN</button>`;
}
</script>
"""

# --- 1. ANA SAYFA ---
@app.route('/')
def home():
    xp = scores["xp"]
    rank = "Çaylak" if xp < 100 else "Gelişmiş" if xp < 500 else "Efsane"
    
    html = f"""
<!DOCTYPE html>
<html>
{global_head}
<body>
    {support_html}
    <div style="padding:80px 20px; text-align:center;">
        <h1 class="glitch-header">CANO STUDIO</h1>
        <p style="color:var(--neon); letter-spacing:5px; font-size:0.8rem; margin-top:-20px;">RANK: {rank} | TOTAL_XP: {xp}</p>
    </div>

    <div class="container">
        <div class="game-card" onclick="location.href='/neon-arcade'">
            <div style="color:var(--neon); font-size:0.6rem; border:1px solid; display:inline-block; padding:2px 8px; margin-bottom:10px;">SYSTEM_SPEED</div>
            <h2>NEON ARCADE</h2>
            <p style="color:#555; font-size:0.8rem;">Reflekslerini dijital boyuta taşı.</p>
        </div>
        <div class="game-card" onclick="location.href='/lost-forest'">
            <div style="color:#ff4500; font-size:0.6rem; border:1px solid; display:inline-block; padding:2px 8px; margin-bottom:10px;">RAYCAST_FPS</div>
            <h2>LOST FOREST</h2>
            <p style="color:#555; font-size:0.8rem;">Karanlık labirentten sağ çık.</p>
        </div>
        <div class="game-card" onclick="location.href='/void-command'">
            <div style="color:#00ff88; font-size:0.6rem; border:1px solid; display:inline-block; padding:2px 8px; margin-bottom:10px;">VOID_TACTICS</div>
            <h2>VOID COMMAND</h2>
            <p style="color:#555; font-size:0.8rem;">Yıldız sistemlerini ele geçir.</p>
        </div>
    </div>

    <div style="max-width:800px; margin:50px auto; padding:30px; background:#050505; border-radius:12px; border:1px solid #111;">
        <h4 style="text-align:center; color:#333; letter-spacing:3px;">LİDERLİK_VERİSİ</h4>
        <table style="width:100%; border-collapse:collapse; margin-top:20px; font-size:0.9rem;">
            <tr style="color:#444; border-bottom:1px solid #111;"><th>MODÜL</th><th style="text-align:right">SCORE</th></tr>
            <tr><td style="padding:10px 0;">Neon Arcade High</td><td style="text-align:right; color:var(--neon); font-weight:bold;">{max(scores["neon_arcade"])}</td></tr>
            <tr><td style="padding:10px 0;">Strategy Conquest</td><td style="text-align:right; color:#00ff88; font-weight:bold;">Lvl {max(scores["void_command"])}</td></tr>
            <tr><td style="padding:10px 0;">Horror Survival</td><td style="text-align:right; color:#ff4500; font-weight:bold;">Lvl {max(scores["lost_forest"])}</td></tr>
        </table>
    </div>

    <footer style="margin-top:auto; padding:40px; text-align:center; border-top:1px solid #080808;">
        <p style="color:#222; font-size:0.6rem; letter-spacing:3px;">GOOGLE ANALYTICS ACTIVE: {GTAG_ID}</p>
    </footer>
</body>
</html>
"""
    return html

# --- 2. NEON ARCADE (DEV MOD) ---
@app.route('/neon-arcade')
def arcade():
    html = f"""
<!DOCTYPE html>
<html>
{global_head}
<body style="overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh;">
    {back_btn} {support_html}
    <canvas id="c" width="400" height="600" style="border:5px solid #0a0a0a; box-shadow:0 0 50px rgba(0,188,212,0.1);"></canvas>
    <script>
        const canvas=document.getElementById("c"), ctx=canvas.getContext("2d");
        let bird, pipes, frames, score, active;
        function reset(){{ bird={{y:300,v:0,g:0.4,j:-7,s:30}}; pipes=[]; frames=0; score=0; active=true; }}
        function gameOver(){{ active=false; fetch('/submit_score/neon_arcade/'+score); }}
        function draw(){{
            ctx.fillStyle="#000"; ctx.fillRect(0,0,400,600);
            if(!active){{
                ctx.fillStyle="rgba(0,0,0,0.8)"; ctx.fillRect(0,0,400,600);
                ctx.fillStyle=var("--neon"); ctx.font="bold 25px Arial"; ctx.textAlign="center";
                ctx.fillText("CORE FAILURE", 200, 280); ctx.font="14px Arial";
                ctx.fillText("REBOOT (TIKLA)", 200, 320); return;
            }}
            bird.v+=bird.g; bird.y+=bird.v;
            ctx.fillStyle=var("--neon"); ctx.shadowBlur=15; ctx.shadowColor=var("--neon");
            ctx.fillRect(50,bird.y,bird.s,bird.s); ctx.shadowBlur=0;
            if(frames%85===0) pipes.push({{x:400,h:Math.random()*300+100,p:false}});
            pipes.forEach((p,i)=>{{
                p.x-=4.2; ctx.fillStyle="#080808"; ctx.fillRect(p.x,0,60,p.h); ctx.fillRect(p.x,p.h+165,60,600);
                if(50+bird.s>p.x && 50<p.x+60 && (bird.y<p.h || bird.y+bird.s>p.h+165)) gameOver();
                if(p.x<50 && !p.p){{ score++; p.p=true; }}
                if(p.x<-60) pipes.splice(i,1);
            }});
            if(bird.y>600 || bird.y<0) gameOver();
            ctx.fillStyle="#fff"; ctx.font="16px monospace"; ctx.fillText("STABILITY: "+score, 20, 40);
            frames++; requestAnimationFrame(draw);
        }
        window.onpointerdown=(e)=>{{ e.preventDefault(); if(active) bird.v=bird.j; else {{ reset(); draw(); }} }};
        reset(); draw();
    </script>
</body>
</html>
"""
    return html

# --- 3. LOST FOREST (RAYCASTING v2 PRO) ---
@app.route('/lost-forest')
def horror():
    html = f"""
<!DOCTYPE html>
<html>
{global_head}
<body style="overflow:hidden; margin:0; touch-action:none; background:#000;">
    {back_btn} {support_html}
    <div id="ui" style="position:fixed; top:70px; width:100%; text-align:center; color:white; font-family:monospace; z-index:10; letter-spacing:2px;">
        SECTOR: <span id="l">1</span> | SIGNAL: <span id="r">OK</span>
    </div>
    <div id="joystick" style="position:fixed; bottom:50px; left:50px; width:120px; height:120px; background:rgba(255,255,255,0.03); border:1px solid #222; border-radius:50%; z-index:100;">
        <div id="stick" style="position:absolute; top:40px; left:40px; width:40px; height:40px; background:var(--neon); opacity:0.2; border-radius:50%;"></div>
    </div>
    <canvas id="v"></canvas>
    <script>
        const canvas=document.getElementById('v'), ctx=canvas.getContext('2d');
        let level=1, map=[], player={{x:1.5,y:1.5,dir:0,speed:0.042}}, joy={{x:0,y:0,active:false}};
        function gen(s){{ 
            let m=Array.from({{length:s}},()=>Array(s).fill(1)); 
            for(let y=1;y<s-1;y++)for(let x=1;x<s-1;x++)if(Math.random()>0.38)m[y][x]=0; 
            m[1][1]=0; m[s-2][s-2]=2; return m; 
        }}
        function reset(){{
            canvas.width=window.innerWidth; canvas.height=window.innerHeight;
            map=gen(10+level*2); player.x=1.5; player.y=1.5; document.getElementById('l').innerText=level;
        }}
        window.addEventListener('resize', reset);
        const jz=document.getElementById('joystick'), js=document.getElementById('stick');
        jz.addEventListener('touchmove',(e)=>{{
            e.preventDefault(); let t=e.touches[0], r=jz.getBoundingClientRect();
            let dx=t.clientX-(r.left+60), dy=t.clientY-(r.top+60);
            let d=Math.min(Math.hypot(dx,dy),50), a=Math.atan2(dy,dx);
            joy.x=Math.cos(a)*(d/50); joy.y=Math.sin(a)*(d/50);
            js.style.transform=`translate(${{joy.x*40}}px,${{joy.y*40}}px)`; joy.active=true;
        }});
        jz.addEventListener('touchend',()=>{{ joy.active=false; js.style.transform='translate(0,0)'; }});
        
        function update(){{
            if(!joy.active) return;
            let ox=player.x, oy=player.y;
            if(Math.abs(joy.y)>0.2){{ player.x+=Math.cos(player.dir)*player.speed*(-joy.y*1.4); player.y+=Math.sin(player.dir)*player.speed*(-joy.y*1.4); }}
            if(Math.abs(joy.x)>0.2) player.dir+=joy.x*0.06;
            if(map[Math.floor(player.y)][Math.floor(player.x)]===1){{player.x=ox; player.y=oy;}}
            if(map[Math.floor(player.y)][Math.floor(player.x)]===2){{ level++; fetch('/submit_score/lost_forest/'+level); reset(); }}
        }}
        
        function draw(){{
            ctx.fillStyle="#000"; ctx.fillRect(0,0,canvas.width,canvas.height);
            const rays=100, fov=Math.PI/3;
            for(let i=0;i<rays;i++){{
                let a=(player.dir-fov/2)+(i/rays)*fov, d=0, hit=0;
                while(d<14){{
                    d+=0.1; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d);
                    if(map[ty]&&map[ty][tx]>0){{hit=map[ty][tx]; break;}}
                }}
                let h=canvas.height/(d*Math.cos(a-player.dir));
                ctx.fillStyle=hit===2?`#fff`:`rgb(0,${{Math.max(0,160-d*11)}},0)`;
                ctx.fillRect(i*(canvas.width/rays), (canvas.height-h)/2, canvas.width/rays+1, h);
            }}
            let g=ctx.createRadialGradient(canvas.width/2,canvas.height/2,100,canvas.width/2,canvas.height/2,canvas.width);
            g.addColorStop(0,"transparent"); g.addColorStop(1,"rgba(0,0,0,0.95)");
            ctx.fillStyle=g; ctx.fillRect(0,0,canvas.width,canvas.height);
        }}
        function loop(){ update(); draw(); requestAnimationFrame(loop); }
        reset(); loop();
    </script>
</body>
</html>
"""
    return html

# --- 4. VOID COMMAND (PRO TACTICS) ---
@app.route('/void-command')
def strategy():
    html = f"""
<!DOCTYPE html>
<html>
{global_head}
<body style="background:#000; overflow:hidden;">
    {back_btn} {support_html}
    <div id="l" style="position:fixed; top:70px; width:100%; text-align:center; color:#00ff88; font-family:monospace; letter-spacing:3px;">CONQUEST_LVL: 1</div>
    <canvas id="g"></canvas>
    <script>
        const c=document.getElementById("g"), ctx=c.getContext("2d");
        let lvl=1, planets=[], sel=null;
        class P {{
            constructor(x,y,r,o){{this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:25;this.max=r*2.5;}}
            draw(){{
                ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
                ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#222');
                ctx.lineWidth=sel===this?4:1; ctx.stroke();
                ctx.fillStyle=ctx.strokeStyle; ctx.fillRect(this.x-this.r,this.y+this.r+12, (this.e/this.max)*this.r*2, 3);
                ctx.font="10px monospace"; ctx.textAlign="center"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);
            }}
        }}
        function init(){{
            c.width=window.innerWidth; c.height=window.innerHeight;
            planets=[new P(100,c.height/2,45,'player'), new P(c.width-100,c.height/2,45,'enemy')];
            for(let i=0;i<lvl+5;i++) planets.push(new P(Math.random()*(c.width-200)+100, Math.random()*(c.height-200)+100, 28, 'neutral'));
        }}
        window.addEventListener('resize', init);
        c.onpointerdown=(e)=>{{
            let p=planets.find(p=>Math.hypot(p.x-e.clientX,p.y-e.clientY)<p.r);
            if(p){{
                if(p.o==='player')sel=p;
                else if(sel){{
                    let f=sel.e/2; sel.e-=f; p.e-=f;
                    if(p.e<0){{p.o='player';p.e=Math.abs(p.e);}}
                    sel=null;
                }}
            }}else sel=null;
        }};
        function loop(){{
            ctx.fillStyle="rgba(0,0,0,0.15)"; ctx.fillRect(0,0,c.width,c.height);
            planets.forEach(p=>{{ if(p.o!=='neutral') p.e = Math.min(p.max, p.e+0.025); p.draw(); }});
            if(!planets.some(p=>p.o==='enemy')){{ lvl++; fetch('/submit_score/void_command/'+lvl); init(); document.getElementById('l').innerText="CONQUEST_LVL: "+lvl; }}
            requestAnimationFrame(loop);
        }}
        init(); loop();
    </script>
</body>
</html>
"""
    return html

# --- API ---
@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    if game in scores:
        scores[game].append(score)
        scores["xp"] += (score * 15)
    return jsonify({"status": "success", "xp": scores["xp"]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
