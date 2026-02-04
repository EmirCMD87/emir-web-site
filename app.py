# ==============================================================================
# CANO STUDIO - FINAL MASTER v26.0
# ==============================================================================
# Geliştirici: Cano Studio | Analytics: G-GQS70MDDPQ
# Tasarım: Siyah Arka Plan + Neon Glow + Hover Depth
# Platform: PC (WASD/Space/Mouse) & MOBİL (Joystick/Touch)
# ==============================================================================

from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# --- CENTRAL DATA ---
studio_data = {
    "xp": 0,
    "analytics_id": "G-GQS70MDDPQ"
}

# --- STYLE SYSTEM (CSS) ---
def get_master_styles():
    return """
    <style>
        :root {{
            --bg-black: #000000;
            --horror-red: #ff0000;
            --arcade-cyan: #00f2ff;
            --strat-green: #00ff88;
            --white: #ffffff;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            touch-action: manipulation;
        }}

        body {{
            background-color: var(--bg-black);
            color: var(--white);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            /* Dinamik Yıldız Arkaplanı (CSS ile) */
            background-image: radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
                              radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px);
            background-size: 550px 550px, 350px 350px;
            animation: move-stars 100s linear infinite;
        }}

        @keyframes move-stars {{
            from {{ background-position: 0 0; }}
            to {{ background-position: 1000px 1000px; }}
        }}

        /* --- HEADER --- */
        .studio-header {{ padding: 80px 20px; text-align: center; }}
        .logo {{ font-size: clamp(3rem, 12vw, 5rem); letter-spacing: 15px; font-weight: 900; text-transform: uppercase; }}

        /* --- LIBRARY GRID --- */
        .library-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 40px;
            padding: 40px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }}

        .lib-card {{
            position: relative;
            background: rgba(10, 10, 10, 0.8);
            border-radius: 30px;
            padding: 80px 40px;
            text-align: center;
            cursor: pointer;
            border: 1px solid #111;
            backdrop-filter: blur(10px);
            z-index: 1;
        }}

        /* Renkli Arkaplanlar & Hover Efektleri */
        .horror:hover {{ background: rgba(40, 0, 0, 0.9); border-color: var(--horror-red); box-shadow: 0 0 50px rgba(255,0,0,0.3); transform: scale(1.08) translateY(-15px); z-index: 10; }}
        .arcade:hover {{ background: rgba(0, 40, 40, 0.9); border-color: var(--arcade-cyan); box-shadow: 0 0 50px rgba(0,242,255,0.3); transform: scale(1.08) translateY(-15px); z-index: 10; }}
        .strat:hover {{ background: rgba(0, 40, 0, 0.9); border-color: var(--strat-green); box-shadow: 0 0 50px rgba(0,255,136,0.3); transform: scale(1.08) translateY(-15px); z-index: 10; }}

        .lib-card h2 {{ font-size: 2rem; letter-spacing: 5px; margin-bottom: 20px; font-weight: 900; }}
        .lib-card p {{ color: #777; font-size: 0.95rem; line-height: 1.6; }}

        /* --- UI ELEMENTS --- */
        .btn-ui {{ background: rgba(255, 255, 255, 0.05); border: 1px solid #333; color: #fff; padding: 14px 28px; border-radius: 10px; font-weight: bold; text-transform: uppercase; cursor: pointer; text-decoration: none; }}
        .btn-ui:hover {{ background: #fff; color: #000; box-shadow: 0 0 20px #fff; }}

        /* --- JOYSTICK (Mobile Only) --- */
        #mobile-joy {{ position: fixed; bottom: 50px; left: 50px; width: 120px; height: 120px; background: rgba(255,255,255,0.05); border-radius: 50%; z-index: 100; display: none; border: 1px solid #222; }}
        #joy-stick {{ position: absolute; top: 35px; left: 35px; width: 50px; height: 50px; background: #fff; opacity: 0.2; border-radius: 50%; }}
        @media (max-width: 1024px) {{ #mobile-joy {{ display: block; }} }}

        footer {{ margin-top: auto; padding: 50px; background: #000; text-align: center; border-top: 1px solid #111; }}
    </style>
    """

def get_analytics():
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={studio_data['analytics_id']}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{studio_data['analytics_id']}');
    </script>
    """

def build_head():
    return f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>CANO STUDIO | OFFICIAL</title>
        {get_analytics()}
        {get_master_styles()}
    </head>
    """

# --- MAIN PAGE ---
@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {build_head()}
    <body>
        <a href="#" class="btn-ui" style="position:fixed; top:25px; right:25px; z-index:9000;">💰 DESTEK</a>
        
        <header class="studio-header">
            <h1 class="logo">CANO STUDIO</h1>
        </header>

        <main class="library-grid">
            <div class="lib-card horror" onclick="location.href='/horror'">
                <h2>HORROR</h2>
                <p>Karanlık Orman Keşfi. PC: WASD | MOBİL: Joystick</p>
            </div>
            <div class="lib-card arcade" onclick="location.href='/arcade-hub'">
                <h2>NEON ARCADE</h2>
                <p>Neon Bird & Neon Drift. PC: Klavye | MOBİL: Dokunmatik</p>
            </div>
            <div class="lib-card strat" onclick="location.href='/strategy'">
                <h2>STRATEGY</h2>
                <p>Gezegen Fethi. PC & MOBİL: Mouse/Touch</p>
            </div>
        </main>

        <footer>
            <a href="mailto:destek@canostudio.com" class="btn-ui" style="font-size:0.75rem;">İLETİŞİM</a>
        </footer>
    </body>
    </html>
    """

# --- HORROR ENGINE ---
@app.route('/horror')
def horror_game():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="overflow:hidden; background:#000; margin:0; touch-action:none;">
        <a href="/" class="btn-ui" style="position:fixed; top:25px; left:25px; z-index:9000;">← ÇIKIŞ</a>
        <div id="mobile-joy"><div id="joy-stick"></div></div>
        <div id="mind-text" style="position:fixed; top:40%; width:100%; text-align:center; color:rgba(255,255,255,0.1); font-size:1.5rem; pointer-events:none; z-index:5;"></div>
        <canvas id="cV"></canvas>
        <script>
            const c=document.getElementById("cV"), ctx=c.getContext("2d");
            const thoughts = ["Biri mi var?", "Geri dönmeliyim.", "Sesleri duydun mu?", "ASLA ÇIKAMAYACAKSIN", "Onlar arkanda."];
            let map=[], player={{x:1.5,y:1.5,dir:0,speed:0.045}};
            function gen(s){{ let m=Array.from({{length:s}},()=>Array(s).fill(1)); for(let y=1;y<s-1;y++)for(let x=1;x<s-1;x++)if(Math.random()>0.4)m[y][x]=0; m[1][1]=0; m[s-2][s-2]=2; return m; }}
            function reset(){{ c.width=window.innerWidth; c.height=window.innerHeight; map=gen(14); player.x=1.5; player.y=1.5; }}
            
            window.onkeydown=(e)=>{{ 
                if(e.key==='w') {{ player.x+=Math.cos(player.dir)*0.1; player.y+=Math.sin(player.dir)*0.1; }}
                if(e.key==='a') player.dir-=0.1; if(e.key==='d') player.dir+=0.1;
                if(Math.random()>0.95) {{ document.getElementById('mind-text').innerText=thoughts[Math.floor(Math.random()*thoughts.length)]; setTimeout(()=>document.getElementById('mind-text').innerText="", 1500); }}
            }};

            function draw(){{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,c.width,c.height);
                for(let i=0;i<120;i++){{
                    let a=(player.dir-0.5)+(i/120), d=0;
                    while(d<15){{ d+=0.08; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d); if(map[ty]&&map[ty][tx]>0) break; }}
                    let h=c.height/d; ctx.fillStyle=`rgb(0,${{Math.max(0,180-d*10)}},0)`; ctx.fillRect(i*(c.width/120),(c.height-h)/2,c.width/120+1,h);
                }}
                requestAnimationFrame(draw);
            }}
            window.addEventListener("resize", reset); reset(); draw();
        </script>
    </body></html>
    """

# --- ARCADE HUB ---
@app.route('/arcade-hub')
def arcade_hub():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body>
    <div style="padding:100px 20px; text-align:center;">
        <h1 class="logo" style="color:#00f2ff; font-size:2rem;">ARCADE HUB</h1>
        <div class="library-grid">
            <div class="lib-card arcade" onclick="location.href='/neon-bird'"><h2>NEON BIRD</h2><p>PC: Space | MOBİL: Dokun</p></div>
            <div class="lib-card arcade" onclick="location.href='/neon-drift'"><h2>NEON DRIFT</h2><p>PC: A-D | MOBİL: Sağ-Sol Dokun</p></div>
        </div>
        <a href="/" class="btn-ui">GERİ</a>
    </div></body></html>
    """

@app.route('/neon-bird')
def bird_game():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh; background:#000;">
        <a href="/arcade-hub" class="btn-ui" style="position:fixed; top:25px; left:25px; z-index:9000;">← GERİ</a>
        <canvas id="cB" width="400" height="600" style="border:2px solid #00f2ff;"></canvas>
        <script>
            const c=document.getElementById("cB"), ctx=c.getContext("2d");
            let p, pipes, frames, score, active;
            function init(){{ p={{y:300,v:0,g:0.4,j:-7,s:30}}; pipes=[]; frames=0; score=0; active=true; }}
            function loop(){{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,400,600);
                if(!active) {{ ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText("SKOR: "+score+" - TIKLA", 200, 300); return requestAnimationFrame(loop); }}
                p.v+=p.g; p.y+=p.v; ctx.fillStyle="#00f2ff"; ctx.fillRect(50,p.y,30,30);
                if(frames%100===0) pipes.push({{x:400,h:Math.random()*300+100,p:false}});
                pipes.forEach((pipe,i)=>{{ pipe.x-=4; ctx.fillStyle="#111"; ctx.fillRect(pipe.x,0,60,pipe.h); ctx.fillRect(pipe.x,pipe.h+160,60,600);
                if(50+30>pipe.x && 50<pipe.x+60 && (p.y<pipe.h || p.y+30>pipe.h+160)) active=false;
                if(pipe.x<50 && !pipe.p){{ score++; pipe.p=true; }} if(pipe.x<-70) pipes.splice(i,1); }});
                if(p.y>600 || p.y<0) active=false; frames++; requestAnimationFrame(loop);
            }}
            window.onpointerdown=()=>{{ if(active) p.v=p.j; else init(); }}; init(); loop();
        </script>
    </body></html>
    """

@app.route('/neon-drift')
def drift_game():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh; background:#000;">
        <a href="/arcade-hub" class="btn-ui" style="position:fixed; top:25px; left:25px; z-index:9000;">← GERİ</a>
        <canvas id="cD" width="400" height="600" style="border:2px solid #ff007f;"></canvas>
        <script>
            const c=document.getElementById("cD"), ctx=c.getContext("2d");
            let x=180, obs=[], active=true;
            function loop(){{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,400,600);
                if(!active) {{ ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText("YENİLDİN - TIKLA", 200, 300); return requestAnimationFrame(loop); }}
                ctx.fillStyle="#ff007f"; ctx.fillRect(x, 520, 40, 60);
                if(Math.random()>0.97) obs.push({{x:Math.random()*360, y:-50}});
                obs.forEach((o,i)=>{{ o.y+=6; ctx.fillStyle="#333"; ctx.fillRect(o.x, o.y, 45, 45);
                if(x<o.x+45 && x+40>o.x && 520<o.y+45 && 580>o.y) active=false;
                if(o.y>600) obs.splice(i,1); }});
                requestAnimationFrame(loop);
            }}
            window.onkeydown=(e)=>{{ if(e.key==='a'&&x>0)x-=30; if(e.key==='d'&&x<360)x+=30; }};
            window.onpointerdown=(e)=>{{ 
                if(!active) {{ active=true; obs=[]; x=180; return; }}
                if(e.clientX < window.innerWidth/2) x-=30; else x+=30;
                if(x<0) x=0; if(x>360) x=360;
            }}; loop();
        </script>
    </body></html>
    """

# --- STRATEGY ENGINE ---
@app.route('/strategy')
def strategy_game():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="background:#000; overflow:hidden;">
        <a href="/" class="btn-ui" style="position:fixed; top:25px; left:25px; z-index:9000;">← ÇIKIŞ</a>
        <canvas id="cS" style="width:100vw; height:100vh;"></canvas>
        <script>
            const c=document.getElementById("cS"), ctx=c.getContext("2d");
            let planets=[], sel=null;
            class P {{ constructor(x,y,r,o){{this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:25;}} draw(){{ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#222'); ctx.lineWidth=sel===this?4:1; ctx.stroke(); ctx.fillStyle=ctx.strokeStyle; ctx.textAlign="center"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);}} }}
            function init(){{ c.width=window.innerWidth; c.height=window.innerHeight; planets=[new P(100,c.height/2,50,'player'), new P(c.width-100,c.height/2,50,'enemy')]; for(let i=0;i<7;i++) planets.push(new P(Math.random()*(c.width-200)+100, Math.random()*(c.height-200)+100, 30, 'neutral')); }}
            window.addEventListener("pointerdown",(e)=>{{ 
                let p=planets.find(p=>Math.hypot(p.x-e.clientX,p.y-e.clientY)<p.r); 
                if(p){{if(p.o==='player')sel=p; else if(sel){{let f=sel.e/2; sel.e-=f; p.e-=f; if(p.e<0){{p.o='player';p.e=Math.abs(p.e);}} sel=null;}} }}else sel=null; 
            }});
            function loop(){{ ctx.fillStyle="rgba(0,0,0,0.2)"; ctx.fillRect(0,0,c.width,c.height); planets.forEach(p=>{{if(p.o!=='neutral')p.e+=0.025; p.draw();}}); requestAnimationFrame(loop); }}
            init(); loop();
        </script>
    </body></html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
