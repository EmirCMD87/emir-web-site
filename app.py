# ==============================================================================
# CANO STUDIO - TITAN CROSS v25.5 (UNIVERSAL SYNC)
# ==============================================================================
# Geliştirici: Cano Studio | Analytics: G-GQS70MDDPQ
# Platform: PC (WASD/Space/Mouse) & MOBİL (Joystick/Touch)
# Durum: %100 Stabil - Render Uyumlu
# ==============================================================================

from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# --- CENTRAL DATA CORE ---
studio_core = {
    "xp": 0,
    "analytics_id": "G-GQS70MDDPQ"
}

# --- STYLE SYSTEM (NEURAL-GLOW UI) ---
def get_studio_styles():
    return """
    <style>
        :root {{
            --void-bg: #000000;
            --horror-glow: rgba(255, 0, 0, 0.4);
            --arcade-glow: rgba(0, 242, 255, 0.4);
            --strat-glow: rgba(0, 255, 136, 0.4);
            --white: #ffffff;
            --font-main: 'Inter', -apple-system, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            touch-action: manipulation;
        }}

        body {{
            background-color: var(--void-bg);
            color: var(--white);
            font-family: var(--font-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        .studio-header {{ padding: 80px 20px 40px; text-align: center; }}
        .logo {{ font-size: clamp(3rem, 12vw, 5rem); letter-spacing: 15px; text-transform: uppercase; font-weight: 900; animation: float 6s ease-in-out infinite; }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}

        .library-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; padding: 40px; max-width: 1400px; margin: 0 auto; width: 100%; }}
        .lib-card {{ position: relative; background: #080808; border-radius: 24px; padding: 60px 30px; text-align: center; cursor: pointer; border: 1px solid #111; }}

        .lib-card.horror:hover {{ background: #1a0000; border-color: #ff0000; box-shadow: 0 20px 60px var(--horror-glow); transform: scale(1.05) translateY(-10px); }}
        .lib-card.arcade:hover {{ background: #001a1a; border-color: #00f2ff; box-shadow: 0 20px 60px var(--arcade-glow); transform: scale(1.05) translateY(-10px); }}
        .lib-card.strat:hover {{ background: #001a0a; border-color: #00ff88; box-shadow: 0 20px 60px var(--strat-glow); transform: scale(1.05) translateY(-10px); }}

        .btn-ui {{ background: rgba(255, 255, 255, 0.05); border: 1px solid #333; color: #fff; padding: 12px 24px; border-radius: 8px; font-weight: bold; text-transform: uppercase; cursor: pointer; text-decoration: none; }}
        .btn-ui:hover {{ background: #fff; color: #000; }}

        #modalOverlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.98); z-index: 9999; align-items: center; justify-content: center; }}
        .modal-box {{ background: #0a0a0a; padding: 50px; border-radius: 20px; border: 1px solid #222; max-width: 500px; width: 90%; text-align: center; }}

        /* Joystick Style - Only on Mobile */
        #mobile-joy {{ position: fixed; bottom: 50px; left: 50px; width: 120px; height: 120px; background: rgba(255,255,255,0.05); border-radius: 50%; z-index: 100; display: none; border: 1px solid #222; }}
        #joy-stick {{ position: absolute; top: 35px; left: 35px; width: 50px; height: 50px; background: #fff; opacity: 0.2; border-radius: 50%; }}

        @media (max-width: 1024px) {{ #mobile-joy {{ display: block; }} }}

        footer {{ margin-top: auto; padding: 40px; background: #020202; text-align: center; border-top: 1px solid #080808; }}
    </style>
    """

def get_analytics():
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={studio_core['analytics_id']}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{studio_core['analytics_id']}');
    </script>
    """

def build_head():
    return f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>CANO STUDIO | UNIVERSAL</title>
        {get_analytics()}
        {get_studio_styles()}
    </head>
    """

support_modal = """
<a href="#" onclick="toggleM(true)" class="btn-ui" style="position:fixed; top:25px; right:25px; z-index:9000;">💰 DESTEK</a>
<div id="modalOverlay">
    <div class="modal-box" id="mC">
        <h2 style="color:#00f2ff; letter-spacing:8px; margin-bottom:20px;">STUDIO PATREON</h2>
        <div style="display:flex; gap:10px; margin-bottom:30px;">
            <button class="btn-ui" style="flex:1" onclick="copyD('ininal')">ININAL</button>
            <button class="btn-ui" style="flex:1" onclick="copyD('banka')">BANKA</button>
        </div>
        <button onclick="toggleM(false)" style="background:none; border:none; color:#333; cursor:pointer;">[ KAPAT ]</button>
    </div>
</div>
<script>
    function toggleM(s) { document.getElementById('modalOverlay').style.display = s ? 'flex' : 'none'; }
    function copyD(t) {
        const v = t === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
        navigator.clipboard.writeText(v).then(() => {{
            document.getElementById('mC').innerHTML = `<h1 style="color:#00f2ff">ADAMSIN! ❤️</h1><p>Bilgiler kopyalandı. Teşekkürler!</p><button onclick="location.reload()" class="btn-ui">DÖN</button>`;
        }});
    }
</script>
"""

# --- ROUTES ---
@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    {build_head()}
    <body>
        {support_modal}
        <header class="studio-header"><h1 class="logo">CANO STUDIO</h1></header>
        <main class="library-grid">
            <div class="lib-card horror" onclick="location.href='/horror'"><h2>HORROR</h2><p>Ormandan Kaçış. PC: WASD | MOBİL: JOYSTICK</p></div>
            <div class="lib-card arcade" onclick="location.href='/arcade-hub'"><h2>NEON ARCADE</h2><p>Drift & Bird. PC: Klavye | MOBİL: Dokunmatik</p></div>
            <div class="lib-card strat" onclick="location.href='/strategy'"><h2>STRATEGY</h2><p>Sistem Fethi. PC & MOBİL: Mouse/Dokun</p></div>
        </main>
        <footer>
            <a href="mailto:destek@canostudio.com" class="btn-ui" style="font-size:0.7rem;">İLETİŞİM</a>
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
        <div id="mind-text" style="position:fixed; top:40%; width:100%; text-align:center; color:rgba(255,255,255,0.15); font-size:1.5rem; pointer-events:none; z-index:5;"></div>
        <canvas id="cV"></canvas>
        <script>
            const c=document.getElementById("cV"), ctx=c.getContext("2d");
            const thoughts = ["Sesleri duydun mu?", "ASLA ÇIKAMAYACAKSIN", "Onlar arkanda.", "Işığa güvenme."];
            let map=[], player={{x:1.5,y:1.5,dir:0,speed:0.045}}, joy={{active:false, x:0, y:0}};
            function gen(s){{ let m=Array.from({{length:s}},()=>Array(s).fill(1)); for(let y=1;y<s-1;y++)for(let x=1;x<s-1;x++)if(Math.random()>0.4)m[y][x]=0; m[1][1]=0; m[s-2][s-2]=2; return m; }}
            function reset(){{ c.width=window.innerWidth; c.height=window.innerHeight; map=gen(12); player.x=1.5; player.y=1.5; }}
            
            // PC CONTROLS
            window.onkeydown=(e)=>{{ 
                if(e.key==='w') {{ player.x+=Math.cos(player.dir)*0.1; player.y+=Math.sin(player.dir)*0.1; }}
                if(e.key==='a') player.dir-=0.1; if(e.key==='d') player.dir+=0.1;
                if(Math.random()>0.95) {{ document.getElementById('mind-text').innerText=thoughts[Math.floor(Math.random()*thoughts.length)]; setTimeout(()=>document.getElementById('mind-text').innerText="", 2000); }}
            }};

            // MOBILE CONTROLS (Joystick)
            const jB=document.getElementById('mobile-joy'), jS=document.getElementById('joy-stick');
            jB.addEventListener('touchmove',(e)=>{{
                e.preventDefault(); let t=e.touches[0], r=jB.getBoundingClientRect();
                let dx=t.clientX-(r.left+60), dy=t.clientY-(r.top+60);
                let d=Math.min(Math.hypot(dx,dy),50), a=Math.atan2(dy,dx);
                joy.x=Math.cos(a)*(d/50); joy.y=Math.sin(a)*(d/50);
                jS.style.transform=`translate(${{joy.x*40}}px,${{joy.y*40}}px)`;
                player.dir+=joy.x*0.05; player.x+=Math.cos(player.dir)*(-joy.y*0.1); player.y+=Math.sin(player.dir)*(-joy.y*0.1);
            }}, {{passive:false}});
            jB.addEventListener('touchend',()=>{{ jS.style.transform='translate(0,0)'; }});

            function draw(){{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,c.width,c.height);
                for(let i=0;i<120;i++){{
                    let a=(player.dir-0.5)+(i/120), d=0;
                    while(d<14){{ d+=0.1; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d); if(map[ty]&&map[ty][tx]>0) break; }}
                    let h=c.height/d; ctx.fillStyle=`rgb(0,${{Math.max(0,180-d*12)}},0)`; ctx.fillRect(i*(c.width/120),(c.height-h)/2,c.width/120+1,h);
                }}
                if(map[Math.floor(player.y)][Math.floor(player.x)]===2) {{ alert("ORMANIN DERİNLİKLERİNE İNDİN..."); reset(); }}
                requestAnimationFrame(draw);
            }}
            window.addEventListener("resize", reset); reset(); draw();
        </script>
    </body></html>
    """

# --- NEON BIRD (Universal) ---
@app.route('/neon-bird')
def bird_game():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh; background:#000;">
        <a href="/arcade-hub" class="btn-ui" style="position:fixed; top:25px; left:25px;">← GERİ</a>
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
                pipes.forEach((pipe,i)=>{{ pipe.x-=3.5; ctx.fillStyle="#111"; ctx.fillRect(pipe.x,0,50,pipe.h); ctx.fillRect(pipe.x,pipe.h+160,50,600);
                if(50+30>pipe.x && 50<pipe.x+50 && (p.y<pipe.h || p.y+30>pipe.h+160)) active=false;
                if(pipe.x<50 && !pipe.p){{ score++; pipe.p=true; }}
                if(pipe.x<-50) pipes.splice(i,1); }});
                if(p.y>600 || p.y<0) active=false; frames++; requestAnimationFrame(loop);
            }}
            window.addEventListener('keydown',(e)=>{{ if(e.code==='Space') p.v=p.j; }});
            window.onpointerdown=()=>{{ if(active) p.v=p.j; else init(); }}; init(); loop();
        </script>
    </body></html>
    """

# --- NEON DRIFT (Universal) ---
@app.route('/neon-drift')
def drift_game():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body style="overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh; background:#000;">
        <a href="/arcade-hub" class="btn-ui" style="position:fixed; top:25px; left:25px;">← GERİ</a>
        <canvas id="cD" width="400" height="600" style="border:2px solid #ff007f;"></canvas>
        <script>
            const c=document.getElementById("cD"), ctx=c.getContext("2d");
            let x=180, obs=[], frames=0, active=true;
            function loop(){{
                ctx.fillStyle="#000"; ctx.fillRect(0,0,400,600);
                if(!active) {{ ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText("YENİLDİN - TIKLA", 200, 300); return requestAnimationFrame(loop); }}
                ctx.fillStyle="#ff007f"; ctx.fillRect(x, 500, 40, 60);
                if(frames%60===0) obs.push({{x:Math.random()*360, y:-50}});
                obs.forEach((o,i)=>{{ o.y+=5.5; ctx.fillStyle="#222"; ctx.fillRect(o.x, o.y, 40, 40);
                if(x<o.x+40 && x+40>o.x && 500<o.y+40 && 560>o.y) active=false;
                if(o.y>600) obs.splice(i,1); }});
                frames++; requestAnimationFrame(loop);
            }}
            window.onkeydown=(e)=>{{ if(e.key==='a'&&x>0)x-=25; if(e.key==='d'&&x<360)x+=25; }};
            window.onpointerdown=(e)=>{{ 
                if(!active) {{ active=true; obs=[]; x=180; return; }}
                if(e.clientX < window.innerWidth/2 && x>0) x-=25;
                if(e.clientX > window.innerWidth/2 && x<360) x+=25;
            }}; loop();
        </script>
    </body></html>
    """

# --- STRATEGY ENGINE (Universal) ---
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
            class P {{ constructor(x,y,r,o){{this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:20;}} draw(){{ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#333'); ctx.lineWidth=sel===this?4:1; ctx.stroke(); ctx.fillStyle=ctx.strokeStyle; ctx.textAlign="center"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);}} }}
            function init(){{ c.width=window.innerWidth; c.height=window.innerHeight; planets=[new P(100,c.height/2,45,'player'), new P(c.width-100,c.height/2,45,'enemy')]; for(let i=0;i<6;i++) planets.push(new P(Math.random()*(c.width-200)+100, Math.random()*(c.height-200)+100, 30, 'neutral')); }}
            window.addEventListener("pointerdown",(e)=>{{ 
                let p=planets.find(p=>Math.hypot(p.x-e.clientX,p.y-e.clientY)<p.r); 
                if(p){{if(p.o==='player')sel=p; else if(sel){{let f=sel.e/2; sel.e-=f; p.e-=f; if(p.e<0){{p.o='player';p.e=Math.abs(p.e);}} sel=null;}} }}else sel=null; 
            }});
            function loop(){{ ctx.fillStyle="rgba(0,0,0,0.15)"; ctx.fillRect(0,0,c.width,c.height); planets.forEach(p=>{{if(p.o!=='neutral')p.e+=0.02; p.draw();}}); requestAnimationFrame(loop); }}
            init(); loop();
        </script>
    </body></html>
    """

# --- ARCADE HUB ---
@app.route('/arcade-hub')
def arcade_hub():
    return f"""
    <!DOCTYPE html><html>{build_head()}
    <body>{support_modal}
    <div style="padding:100px 20px; text-align:center;">
        <h1 class="logo" style="color:#00f2ff; font-size:2rem;">ARCADE HUB</h1>
        <div class="library-grid">
            <div class="lib-card arcade" onclick="location.href='/neon-bird'"><h2>NEON BIRD</h2><p>Flappy refleks.</p></div>
            <div class="lib-card arcade" onclick="location.href='/neon-drift'"><h2>NEON DRIFT</h2><p>Tünel yarışı.</p></div>
        </div>
        <a href="/" class="btn-ui">GERİ</a>
    </div></body></html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
