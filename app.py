from flask import Flask, request, jsonify
import os, random

app = Flask(__name__)

# --- VERİTABANI (Bellek Üstünde) ---
scores = {
    "neon_arcade": [0],
    "void_command": [1],
    "lost_forest": [1],
    "xp": 0
}

# --- BİLEŞENLER VE TASARIM (CSS/HTML) ---
# Google Analytics ve Global CSS
GTAG_ID = "G-XXXXXXXXXX" # Kendi ID'ni buraya yapıştır

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
        :root {{ --neon: #00bcd4; --dark: #020202; --glitch: #ff0055; }}
        * {{ box-sizing: border-box; transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); touch-action: manipulation; }}
        body {{ 
            background: var(--dark); color: #e0e0e0; font-family: 'Segoe UI', sans-serif; 
            margin: 0; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden;
        }}
        .glitch-text {{ position: relative; display: inline-block; }}
        .glitch-text:hover::after {{
            content: attr(data-text); position: absolute; left: 2px; text-shadow: -2px 0 red;
            top: 0; background: var(--dark); overflow: hidden; clip: rect(0, 900px, 0, 0);
            animation: noise-anim 2s infinite linear alternate-reverse;
        }}
        @keyframes noise-anim {{ 0% {{ clip: rect(10px, 9999px, 20px, 0); }} 100% {{ clip: rect(80px, 9999px, 90px, 0); }} }}
        
        .btn-ui {{ 
            background: rgba(0, 188, 212, 0.1); border: 1px solid var(--neon); color: var(--neon);
            padding: 8px 16px; border-radius: 4px; cursor: pointer; text-decoration: none;
            font-size: 0.8rem; font-weight: bold; z-index: 1000;
        }}
        .btn-ui:hover {{ background: var(--neon); color: #000; box-shadow: 0 0 20px var(--neon); }}
        
        /* Modal ve Destek */
        #supportModal {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:2000; align-items:center; justify-content:center; }}
        .modal-content {{ background:#0a0a0a; padding:30px; border-radius:15px; border:1px solid var(--neon); max-width:500px; width:95%; text-align:center; }}
        .tab-btn {{ flex:1; padding:12px; border:1px solid #333; background:transparent; color:#666; cursor:pointer; }}
        .tab-btn.active {{ border-color:var(--neon); color:var(--neon); background:rgba(0,188,212,0.1); }}
        .amt-grid {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin:20px 0; }}
        .amt-btn {{ background:#111; border:1px solid #222; color:#fff; padding:12px; cursor:pointer; border-radius:4px; }}
        .amt-btn:hover {{ border-color:var(--neon); color:var(--neon); }}
    </style>
</head>
"""

back_btn = f'<a href="/" class="btn-ui" style="position:fixed; top:20px; left:20px;">← KÜTÜPHANE</a>'

support_ui = """
<a href="#" onclick="showSupport()" class="btn-ui" style="position:fixed; top:20px; right:20px;">💎 DESTEK</a>
<div id="supportModal">
    <div class="modal-content" id="supportBox">
        <h2 style="color:var(--neon)">STUDIO DESTEK</h2>
        <div style="display:flex; gap:5px; margin:20px 0;">
            <button class="tab-btn active" id="tIninal" onclick="switchT('ininal')">ininal</button>
            <button class="tab-btn" id="tBanka" onclick="switchT('banka')">Banka/IBAN</button>
        </div>
        <div id="pIninal">
            <div class="amt-grid">
                <button class="amt-btn" onclick="copyD('ininal', 10)">10 TL</button>
                <button class="amt-btn" onclick="copyD('ininal', 50)">50 TL</button>
                <button class="amt-btn" onclick="copyD('ininal', 100)">100 TL</button>
            </div>
            <p style="color:#555; font-size:0.7rem">BARKOD: 4000 0000 0000 0</p>
        </div>
        <div id="pBanka" style="display:none">
            <div style="background:#000; padding:15px; text-align:left; font-size:0.8rem; border-radius:8px;">
                <b>IBAN:</b> TR00 0000 0000 0000 0000 0000 00<br>
                <b>ALICI:</b> CANO STUDIO<br>
                <span style="color:red">Açıklamaya barkodunuzu yazın!</span>
            </div>
            <button class="amt-btn" style="width:100%; margin-top:10px;" onclick="copyD('banka', 'IBAN')">IBAN KOPYALA</button>
        </div>
        <br><button onclick="hideSupport()" style="color:#444; background:none; border:none; cursor:pointer; text-decoration:underline;">[ Kapat ]</button>
    </div>
</div>
<script>
function showSupport() { document.getElementById('supportModal').style.display='flex'; }
function hideSupport() { document.getElementById('supportModal').style.display='none'; }
function switchT(t) {
    document.getElementById('pIninal').style.display = t==='ininal'?'block':'none';
    document.getElementById('pBanka').style.display = t==='banka'?'block':'none';
    document.getElementById('tIninal').className = t==='ininal'?'tab-btn active':'tab-btn';
    document.getElementById('tBanka').className = t==='banka'?'tab-btn active':'tab-btn';
}
function copyD(m, a) {
    const val = m==='ininal' ? "4000000000000" : "TR000000000000000000000000";
    navigator.clipboard.writeText(val);
    document.getElementById('supportBox').innerHTML = `<h2 style="color:var(--neon)">ADAMSIN! ❤️</h2><p>Destek verin kopyalandı. Geliştirmeye senin sayende devam ediyorum!</p><button onclick="location.reload()" class="btn-ui">OYUNA DÖN</button>`;
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
    {support_ui}
    <div style="padding:60px 20px; text-align:center;">
        <h1 class="glitch-text" data-text="CANO STUDIO">CANO STUDIO</h1>
        <p style="color:var(--neon); letter-spacing:4px; font-size:0.8rem;">LEVEL: {rank} | XP: {xp}</p>
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; padding:0 40px; max-width:1400px; margin:0 auto;">
        <div onclick="location.href='/neon-arcade'" style="background:#0a0a0a; border:1px solid #111; padding:40px; border-radius:8px; cursor:pointer; position:relative; overflow:hidden;">
            <div style="color:var(--neon); font-size:0.7rem; border:1px solid; display:inline-block; padding:2px 8px; margin-bottom:15px;">ARCADE</div>
            <h2 style="margin:0">NEON ARCADE</h2>
            <p style="color:#444; font-size:0.8rem;">Hız ve refleks testi.</p>
        </div>
        <div onclick="location.href='/lost-forest'" style="background:#0a0a0a; border:1px solid #111; padding:40px; border-radius:8px; cursor:pointer;">
            <div style="color:#ff4500; font-size:0.7rem; border:1px solid; display:inline-block; padding:2px 8px; margin-bottom:15px;">FPS HORROR</div>
            <h2 style="margin:0">LOST FOREST</h2>
            <p style="color:#444; font-size:0.8rem;">Labirentten sağ çık.</p>
        </div>
        <div onclick="location.href='/void-command'" style="background:#0a0a0a; border:1px solid #111; padding:40px; border-radius:8px; cursor:pointer;">
            <div style="color:#00ff88; font-size:0.7rem; border:1px solid; display:inline-block; padding:2px 8px; margin-bottom:15px;">STRATEGY</div>
            <h2 style="margin:0">VOID COMMAND</h2>
            <p style="color:#444; font-size:0.8rem;">Gezegenleri fethet.</p>
        </div>
    </div>

    <div style="margin:40px auto; max-width:1000px; padding:20px; background:#050505; border-radius:8px;">
        <h3 style="color:#333; font-size:0.8rem; text-align:center;">LİDERLİK TABLOSU</h3>
        <table style="width:100%; border-collapse:collapse; margin-top:10px;">
            <tr style="color:#444; font-size:0.7rem;"><th>MODÜL</th><th style="text-align:right">BAŞARI</th></tr>
            <tr><td>Neon High Score</td><td style="text-align:right; font-weight:bold;">{max(scores["neon_arcade"])}</td></tr>
            <tr><td>Strategy Level</td><td style="text-align:right; font-weight:bold;">{max(scores["void_command"])}</td></tr>
            <tr><td>Horror Progress</td><td style="text-align:right; font-weight:bold;">{max(scores["lost_forest"])}</td></tr>
        </table>
    </div>

    <footer style="margin-top:auto; padding:40px; border-top:1px solid #111; text-align:center;">
        <p style="color:#222; font-size:0.7rem; letter-spacing:2px;">GOOGLE ANALYTICS AKTİF</p>
    </footer>
</body>
</html>
"""
    return html

# --- 2. NEON ARCADE (DEV GÜNCELLEME) ---
@app.route('/neon-arcade')
def arcade():
    html = f"""
<!DOCTYPE html>
<html>
{global_head}
<body style="overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh;">
    {back_btn} {support_ui}
    <canvas id="c" width="400" height="600" style="border:4px solid var(--neon); box-shadow:0 0 40px rgba(0,188,212,0.2);"></canvas>
    <script>
        const canvas=document.getElementById("c"), ctx=canvas.getContext("2d");
        let bird, pipes, frames, score, active, particles=[];
        function reset(){{ bird={{y:300,v:0,g:0.4,j:-7,s:30}}; pipes=[]; frames=0; score=0; active=true; }}
        function createP(x,y,c){{ for(let i=0;i<10;i++) particles.push({{x,y,vx:(Math.random()-0.5)*10,vy:(Math.random()-0.5)*10,a:1,c}}); }}
        function gameOver(){{ active=false; fetch('/submit_score/neon_arcade/'+score); }}
        function draw(){{
            ctx.fillStyle="#000"; ctx.fillRect(0,0,400,600);
            if(!active){{
                ctx.fillStyle="rgba(0,0,0,0.8)"; ctx.fillRect(0,0,400,600);
                ctx.fillStyle=var("--neon"); ctx.font="30px Arial"; ctx.textAlign="center";
                ctx.fillText("DATA CORRUPTED", 200, 280); ctx.font="15px Arial";
                ctx.fillText("TIKLA VE TEKRAR YÜKLE", 200, 320); return;
            }}
            bird.v+=bird.g; bird.y+=bird.v;
            ctx.shadowBlur=15; ctx.shadowColor=var("--neon");
            ctx.fillStyle=var("--neon"); ctx.fillRect(50,bird.y,bird.s,bird.s);
            ctx.shadowBlur=0;
            if(frames%90===0) pipes.push({{x:400,h:Math.random()*300+100,p:false}});
            pipes.forEach((p,i)=>{{
                p.x-=4; ctx.fillStyle="#0a0a0a"; ctx.strokeStyle="#1a1a1a";
                ctx.fillRect(p.x,0,60,p.h); ctx.strokeRect(p.x,0,60,p.h);
                ctx.fillRect(p.x,p.h+160,60,600); ctx.strokeRect(p.x,p.h+160,60,600);
                if(50+bird.s>p.x && 50<p.x+60 && (bird.y<p.h || bird.y+bird.s>p.h+160)) gameOver();
                if(p.x<50 && !p.p){{ score++; p.p=true; }}
                if(p.x<-60) pipes.splice(i,1);
            }});
            if(bird.y>600 || bird.y<0) gameOver();
            ctx.fillStyle="#fff"; ctx.font="20px monospace"; ctx.fillText("CORE_STABILITY: "+score, 20, 40);
            frames++; requestAnimationFrame(draw);
        }
        window.onpointerdown=(e)=>{{ e.preventDefault(); if(active) bird.v=bird.j; else {{ reset(); draw(); }} }};
        reset(); draw();
    </script>
</body>
</html>
"""
    return html

# --- 3. LOST FOREST (FPS RAYCASTING v2) ---
@app.route('/lost-forest')
def horror():
    html = f"""
<!DOCTYPE html>
<html>
{global_head}
<body style="overflow:hidden; margin:0; touch-action:none;">
    {back_btn} {support_ui}
    <div id="ui" style="position:fixed; top:70px; width:100%; text-align:center; color:white; font-family:monospace; z-index:10;">
        DEPTH: <span id="l">1</span> | RADAR_SIGNALS: <span id="r">0</span>
    </div>
    <div id="joystick" style="position:fixed; bottom:50px; left:50px; width:120px; height:120px; background:rgba(255,255,255,0.05); border:1px solid #333; border-radius:50%; z-index:100;">
        <div id="stick" style="position:absolute; top:40px; left:40px; width:40px; height:40px; background:var(--neon); opacity:0.3; border-radius:50%;"></div>
    </div>
    <canvas id="v"></canvas>
    <script>
        const canvas=document.getElementById('v'), ctx=canvas.getContext('2d');
        let level=1, map=[], player={{x:1.5,y:1.5,dir:0,speed:0.04}}, joy={{x:0,y:0,active:false}};
        function gen(s){{ 
            let m=Array.from({{length:s}},()=>Array(s).fill(1)); 
            for(let y=1;y<s-1;y++)for(let x=1;x<s-1;x++)if(Math.random()>0.35)m[y][x]=0; 
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
            if(Math.abs(joy.y)>0.2){{ player.x+=Math.cos(player.dir)*player.speed*(-joy.y*1.5); player.y+=Math.sin(player.dir)*player.speed*(-joy.y*1.5); }}
            if(Math.abs(joy.x)>0.2) player.dir+=joy.x*0.06;
            if(map[Math.floor(player.y)][Math.floor(player.x)]===1){{player.x=ox; player.y=oy;}}
            if(map[Math.floor(player.y)][Math.floor(player.x)]===2){{ level++; fetch('/submit_score/lost_forest/'+level); reset(); }}
        }}
        
        function draw(){{
            ctx.fillStyle="#000"; ctx.fillRect(0,0,canvas.width,canvas.height);
            const rays=120, fov=Math.PI/3;
            for(let i=0;i<rays;i++){{
                let a=(player.dir-fov/2)+(i/rays)*fov, d=0, hit=0;
                while(d<14){{
                    d+=0.1; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d);
                    if(map[ty]&&map[ty][tx]>0){{hit=map[ty][tx]; break;}}
                }}
                let h=canvas.height/(d*Math.cos(a-player.dir));
                let color=hit===2?255:Math.max(0,180-d*12);
                ctx.fillStyle=hit===2?`#fff`:`rgb(0,${{color}},0)`;
                ctx.fillRect(i*(canvas.width/rays), (canvas.height-h)/2, canvas.width/rays+1, h);
            }}
            // Glitch overlay
            if(Math.random()>0.98){{ ctx.fillStyle="rgba(255,0,0,0.1)"; ctx.fillRect(0,0,canvas.width,canvas.height); }}
            let g=ctx.createRadialGradient(canvas.width/2,canvas.height/2,100,canvas.width/2,canvas.height/2,canvas.width);
            g.addColorStop(0,"transparent"); g.addColorStop(1,"black");
            ctx.fillStyle=g; ctx.fillRect(0,0,canvas.width,canvas.height);
        }}
        function loop(){ update(); draw(); requestAnimationFrame(loop); }
        reset(); loop();
    </script>
</body>
</html>
"""
    return html

# --- 4. VOID COMMAND (GELİŞMİŞ STRATEJİ) ---
@app.route('/void-command')
def strategy():
    html = f"""
<!DOCTYPE html>
<html>
{global_head}
<body style="background:#000; overflow:hidden;">
    {back_btn} {support_ui}
    <div id="l" style="position:fixed; top:70px; width:100%; text-align:center; color:#00ff88; font-family:monospace;">SYSTEM_CONQUEST: LEVEL 1</div>
    <canvas id="g"></canvas>
    <script>
        const c=document.getElementById("g"), ctx=c.getContext("2d");
        let lvl=1, planets=[], sel=null, particles=[];
        class P {{
            constructor(x,y,r,o){{this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:20;this.max=r*2;}}
            draw(){{
                ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
                ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#333');
                ctx.lineWidth=sel===this?4:1; ctx.stroke();
                // Enerji Barı
                ctx.fillStyle=ctx.strokeStyle; ctx.fillRect(this.x-this.r,this.y+this.r+10, (this.e/this.max)*this.r*2, 4);
                ctx.font="10px monospace"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);
            }}
        }}
        function init(){{
            c.width=window.innerWidth; c.height=window.innerHeight;
            planets=[new P(100,c.height/2,50,'player'), new P(c.width-100,c.height/2,50,'enemy')];
            for(let i=0;i<lvl+4;i++) planets.push(new P(Math.random()*(c.width-200)+100, Math.random()*(c.height-200)+100, 30, 'neutral'));
        }}
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
            ctx.fillStyle="rgba(0,0,0,0.2)"; ctx.fillRect(0,0,c.width,c.height);
            planets.forEach(p=>{{
                if(p.o!=='neutral') p.e = Math.min(p.max, p.e+0.02);
                p.draw();
            }});
            if(!planets.some(p=>p.o==='enemy')){{ lvl++; fetch('/submit_score/void_command/'+lvl); init(); }}
            requestAnimationFrame(loop);
        }}
        init(); loop();
    </script>
</body>
</html>
"""
    return html

# --- API VE SİSTEM ---
@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    if game in scores:
        scores[game].append(score)
        scores["xp"] += score * 10
    return jsonify({"status": "success", "xp": scores["xp"]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
