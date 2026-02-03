from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- VERİTABANI (Sayaçlar ve Skorlar) ---
stats = {"total_visits": 0}
scores = {"neon_arcade": [0], "void_command": [1], "lost_forest": [1]}

# --- GENEL BİLEŞENLER ---
def get_footer():
    return f"""
<footer style="background: #080808; padding: 30px; border-top: 1px solid #1a1a1a; text-align: center; margin-top: auto;">
    <p style="color: #444; font-size: 0.8rem; letter-spacing: 2px;">© 2026 CANO STUDIO - CREATIVE LABS</p>
    <p style="color: #00bcd4; font-size: 0.7rem; margin-top: 10px; font-family: monospace;">ZİYARETÇİ SAYISI: {stats['total_visits']}</p>
</footer>"""

back_button_html = """<a href="/" style="position: fixed; top: 20px; left: 20px; color: #666; text-decoration: none; font-family: sans-serif; font-size: 0.8rem; border: 1px solid #333; padding: 5px 15px; border-radius: 4px; z-index: 1000; background: rgba(0,0,0,0.5);">← GERİ</a>"""

support_button_html = """
<a href="#" onclick="showSupport()" style="position: fixed; top: 20px; right: 20px; color: #00bcd4; text-decoration: none; font-family: sans-serif; font-size: 0.8rem; border: 1px solid #00bcd4; padding: 5px 15px; border-radius: 4px; z-index: 1000; font-weight: bold; background: rgba(0,0,0,0.5);">💳 DESTEK</a>
<div id="supportModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.98); z-index:2000; align-items:center; justify-content:center; flex-direction:column; font-family:sans-serif; text-align:center; padding:20px;">
    <div id="supportBox" style="background:#0a0a0a; padding:30px; border-radius:15px; border:1px solid #00bcd4; max-width:480px; width:100%;">
        <div id="supportContent">
            <h2 style="color:#00bcd4;">Cano Studio'yu Destekle</h2>
            <div style="display:flex; gap:10px; margin:20px 0;">
                <button onclick="switchTab('ininal')" id="tab-ininal" style="flex:1; padding:10px; border:1px solid #00bcd4; background:#00bcd4; color:#000; cursor:pointer; font-weight:bold;">ininal</button>
                <button onclick="switchTab('banka')" id="tab-banka" style="flex:1; padding:10px; border:1px solid #333; background:transparent; color:#666; cursor:pointer; font-weight:bold;">Banka / EFT</button>
            </div>
            <div id="panel-ininal">
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin-bottom:20px;">
                    <button class="amt-btn" onclick="copyAction('ininal', 10)">10 TL</button>
                    <button class="amt-btn" onclick="copyAction('ininal', 50)">50 TL</button>
                    <button class="amt-btn" onclick="copyAction('ininal', 100)">100 TL</button>
                </div>
                <div style="background:#000; padding:10px; border:1px dashed #333; color:#fff;">4000 0000 0000 0</div>
            </div>
            <div id="panel-banka" style="display:none; text-align:left; background:#000; padding:15px; border:1px solid #222; color:#fff; font-size:0.8rem;">
                <b>ALICI:</b> [İSMİNİZ]<br><b>IBAN:</b> TR00 0000 0000 0000 0000 0000 00
            </div>
            <button onclick="hideSupport()" style="background:transparent; color:#444; border:none; cursor:pointer; margin-top:20px;">[Kapat]</button>
        </div>
    </div>
</div>
<script>
function showSupport() { document.getElementById('supportModal').style.display='flex'; }
function hideSupport() { document.getElementById('supportModal').style.display='none'; }
function switchTab(t) {
    document.getElementById('panel-ininal').style.display = t==='ininal'?'block':'none';
    document.getElementById('panel-banka').style.display = t==='banka'?'block':'none';
    document.getElementById('tab-ininal').style.background = t==='ininal'?'#00bcd4':'transparent';
    document.getElementById('tab-banka').style.background = t==='banka'?'#00bcd4':'transparent';
}
function copyAction(m, a) {
    const val = m === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
    navigator.clipboard.writeText(val);
    document.getElementById('supportBox').innerHTML = `<h2 style="color:#00bcd4;">Adamsın! ❤️</h2><p style="color:#fff;">Desteğin için teşekkürler. Bilgiler kopyalandı.</p><button onclick="location.reload()" style="background:#00bcd4; border:none; padding:10px 20px; cursor:pointer; font-weight:bold;">OYUNA DÖN</button>`;
}
</script>"""

# --- 1. ANA SAYFA ---
@app.route('/')
def home():
    stats["total_visits"] += 1
    html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>Cano Studio</title><style>
* { box-sizing: border-box; transition: 0.3s; touch-action: manipulation; }
body { background: #020202; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden; }
.header { padding: 40px 20px; text-align: center; } h1 { font-size: 2rem; letter-spacing: 10px; color: #fff; font-weight: 200; }
.container { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; padding: 20px; max-width: 1200px; margin: 0 auto; width:100%; }
.game-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 25px; border-radius: 8px; cursor: pointer; text-align: center; }
.game-card:hover { border-color: #00bcd4; transform: translateY(-3px); }
.status { font-size: 10px; border: 1px solid; padding: 2px 8px; border-radius: 4px; margin-bottom: 10px; display: inline-block; }
.leaderboard { background: #050505; border: 1px solid #1a1a1a; padding: 20px; margin: 0 20px 40px 20px; border-radius: 8px; }
table { width: 100%; border-collapse: collapse; } td { padding: 10px; border-bottom: 1px solid #111; } .val { color: #fff; font-weight: bold; text-align: right; }
.amt-btn { background: #111; border: 1px solid #222; color: #fff; padding: 10px; border-radius: 4px; cursor: pointer; }
</style></head>
<body>VAR_SUPPORT <div class="header"><h1>CANO STUDIO</h1></div>
<div class="container">
    <div class="game-card" onclick="location.href='/neon-arcade'"><div class="status" style="color:#00d4ff;">ARCADE</div><h2>NEON ARCADE</h2></div>
    <div class="game-card" onclick="location.href='/void-command'"><div class="status" style="color:#00ff88;">STRATEGY</div><h2>VOID COMMAND</h2></div>
    <div class="game-card" onclick="location.href='/lost-forest'"><div class="status" style="color:#ff4500;">FPS HORROR</div><h2>LOST FOREST</h2></div>
    <div class="game-card" onclick="location.href='/glitch-in-me'"><div class="status" style="color:#9b59b6;">NARRATIVE</div><h2>GLITCH IN ME</h2></div>
</div>
<div class="leaderboard"><table>
<tr><td>Neon Max Score</td><td class="val">VAR_ARCADE</td></tr>
<tr><td>Strategy Lvl</td><td class="val">Lvl VAR_VOID</td></tr>
<tr><td>Horror Lvl</td><td class="val">Lvl VAR_FOREST</td></tr>
</table></div>VAR_FOOTER</body></html>"""
    return html.replace("VAR_ARCADE", str(max(scores["neon_arcade"]))).replace("VAR_VOID", str(max(scores["void_command"]))).replace("VAR_FOREST", str(max(scores["lost_forest"]))).replace("VAR_FOOTER", get_footer()).replace("VAR_SUPPORT", support_button_html)

# --- 2. NEON ARCADE ---
@app.route('/neon-arcade')
def arcade():
    html = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><style>
    body{background:#000;margin:0;overflow:hidden;display:flex;justify-content:center;align-items:center;height:100vh;touch-action:none;}
    canvas{border:2px solid #00d4ff; touch-action:manipulation; max-width:95vw; max-height:80vh;}</style></head><body>VAR_BACK VAR_SUPPORT<canvas id="c" width="400" height="500"></canvas>
    <script>const canvas=document.getElementById("c"), ctx=canvas.getContext("2d"); let bird, pipes, frames, score, gameActive;
    function reset() { bird={y:250,v:0,g:0.4,j:-7}; pipes=[]; frames=0; score=0; gameActive=true; }
    function gameOver() { gameActive=false; if(score > 0) fetch('/submit_score/neon_arcade/'+score); }
    function draw() { if(!gameActive) { ctx.fillStyle="rgba(0,0,0,0.7)"; ctx.fillRect(0,0,400,500); ctx.fillStyle="#fff"; ctx.textAlign="center"; ctx.fillText("OYUN BİTTİ - TIKLA", 200, 250); return; }
    ctx.fillStyle="#000"; ctx.fillRect(0,0,400,500); bird.v+=bird.g; bird.y+=bird.v; ctx.fillStyle="#00d4ff"; ctx.fillRect(50,bird.y,30,30);
    if(frames%100===0) pipes.push({x:400,h:Math.random()*200+50,s:false});
    for(let i=pipes.length-1; i>=0; i--) { let p=pipes[i]; p.x-=3.5; ctx.fillStyle="#111"; ctx.fillRect(p.x,0,50,p.h); ctx.fillRect(p.x,p.h+160,50,500); if(50+30>p.x && 50<p.x+50 && (bird.y<p.h || bird.y+30>p.h+160)) gameOver(); if(p.x<50 && !p.s){ score++; p.s=true; } if(p.x<-50) pipes.splice(i,1); }
    if(bird.y>500 || bird.y<0) gameOver(); ctx.fillStyle="#fff"; ctx.font="20px Arial"; ctx.fillText(score, 20, 40); frames++; requestAnimationFrame(draw); }
    window.onpointerdown=(e)=>{ e.preventDefault(); if(gameActive) bird.v=bird.j; else { reset(); draw(); } }; reset(); draw();</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

# --- 3. LOST FOREST ---
@app.route('/lost-forest')
def horror():
    html = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><style>
    body{background:#000;margin:0;overflow:hidden;color:white;font-family:monospace;touch-action:none;} #joystick{position:fixed;bottom:40px;left:40px;width:100px;height:100px;background:rgba(255,255,255,0.1);border-radius:50%;z-index:100;} #stick{position:absolute;top:30px;left:30px;width:40px;height:40px;background:rgba(0,188,212,0.4);border-radius:50%;}
    canvas{display:block; width:100vw; height:100vh;}</style></head><body>VAR_BACK VAR_SUPPORT <div style="position:fixed;top:60px;width:100%;text-align:center;z-index:10;">LVL <span id="l">1</span></div><div id="joystick"><div id="stick"></div></div><canvas id="v"></canvas>
    <script>const canvas=document.getElementById('v'), ctx=canvas.getContext('2d'); let level=1, map=[], player={x:1.5,y:1.5,dir:0,speed:0.04}; let joy={x:0,y:0,active:false};
    function gen(s){ let m=Array.from({length:s},()=>Array(s).fill(1)); for(let y=1;y<s-1;y++)for(let x=1;x<s-1;x++)if(Math.random()>0.3)m[y][x]=0; m[1][1]=0; m[s-2][s-2]=2; return m; }
    function reset(){ canvas.width=window.innerWidth; canvas.height=window.innerHeight; map=gen(8+level*2); player.x=1.5; player.y=1.5; document.getElementById('l').innerText=level; }
    window.addEventListener('resize', reset); const jz=document.getElementById('joystick'), js=document.getElementById('stick');
    jz.addEventListener('touchmove',(e)=>{ e.preventDefault(); let t=e.touches[0], r=jz.getBoundingClientRect(); let dx=t.clientX-(r.left+50), dy=t.clientY-(r.top+50); let d=Math.min(Math.hypot(dx,dy),40), a=Math.atan2(dy,dx); joy.x=Math.cos(a)*(d/40); joy.y=Math.sin(a)*(d/40); js.style.transform=`translate(${joy.x*30}px,${joy.y*30}px)`; joy.active=true; });
    jz.addEventListener('touchend',()=>{ joy.x=0; joy.y=0; joy.active=false; js.style.transform='translate(0,0)'; });
    function update(){ let ox=player.x, oy=player.y; if(joy.active){ if(Math.abs(joy.y)>0.2){ player.x+=Math.cos(player.dir)*player.speed*(-joy.y*1.5); player.y+=Math.sin(player.dir)*player.speed*(-joy.y*1.5); } if(Math.abs(joy.x)>0.2) player.dir+=joy.x*0.05; }
    if(map[Math.floor(player.y)][Math.floor(player.x)]===1){player.x=ox; player.y=oy;} if(map[Math.floor(player.y)][Math.floor(player.x)]===2){level++; fetch('/submit_score/lost_forest/'+level); reset();}}
    function draw(){ ctx.fillStyle="#050805"; ctx.fillRect(0,0,canvas.width,canvas.height/2); ctx.fillStyle="#020402"; ctx.fillRect(0,canvas.height/2,canvas.width,canvas.height); const rays=80, fov=Math.PI/3; for(let i=0;i<rays;i++){ let a=(player.dir-fov/2)+(i/rays)*fov, d=0; while(d<12){ d+=0.1; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d); if(map[ty]&&map[ty][tx]>0){break;} } let h=canvas.height/(d*Math.cos(a-player.dir)); ctx.fillStyle=`rgb(0,${150-d*10},0)`; ctx.fillRect(i*(canvas.width/rays),(canvas.height-h)/2,canvas.width/rays+1,h);} }
    function loop(){ update(); draw(); requestAnimationFrame(loop); } reset(); loop();</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

# --- 4. VOID COMMAND ---
@app.route('/void-command')
def strategy():
    html = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><style>body{background:#000;color:#00ff88;margin:0;overflow:hidden;font-family:monospace;touch-action:none;} #l{position:fixed;top:60px;width:100%;text-align:center;}</style></head>
    <body>VAR_BACK VAR_SUPPORT <div id="l">LEVEL: 1</div><canvas id="g"></canvas>
    <script>const c=document.getElementById("g"), ctx=c.getContext("2d"); let lvl=1, planets=[], sel=null;
    class P { constructor(x,y,r,o){this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:20;} draw(){ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#333'); ctx.lineWidth=sel===this?5:2; ctx.stroke(); ctx.fillStyle=ctx.strokeStyle; ctx.textAlign="center"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);}}
    function init(){ c.width=window.innerWidth; c.height=window.innerHeight; planets=[new P(100,c.height/2,40,'player'), new P(c.width-100,c.height/2,40,'enemy')]; for(let i=0;i<5;i++) planets.push(new P(Math.random()*(c.width-200)+100, Math.random()*(c.height-200)+100, 25, 'neutral')); }
    window.addEventListener('resize', init);
    c.onpointerdown=(e)=>{ let mx=e.clientX, my=e.clientY; let p=planets.find(p=>Math.hypot(p.x-mx,p.y-my)<p.r); if(p){if(p.o==='player')sel=p; else if(sel){let f=sel.e/2; sel.e-=f; p.e-=f; if(p.e<0){p.o='player';p.e=Math.abs(p.e);} sel=null;}}else sel=null;};
    function loop(){ ctx.fillStyle="black"; ctx.fillRect(0,0,c.width,c.height); planets.forEach(p=>{if(p.o!=='neutral')p.e+=0.012; p.draw();}); if(!planets.some(p=>p.o==='enemy')){lvl++; document.getElementById("l").innerText="LEVEL: "+lvl; init();} requestAnimationFrame(loop); } init(); loop();</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

# --- 5. GLITCH IN ME ---
@app.route('/glitch-in-me')
def story_game():
    html = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{background:#050505;color:#e0e0e0;font-family:sans-serif;margin:0;display:flex;align-items:center;justify-content:center;height:100vh;overflow:hidden;} #sc{max-width:600px;width:90%;padding:30px;background:#0a0a0a;border:1px solid #1a1a1a;} .chs{display:flex;flex-direction:column;gap:12px;} button{background:transparent;border:1px solid #222;color:#888;padding:15px;cursor:pointer;text-align:left;}</style></head>
    <body>VAR_BACK VAR_SUPPORT <div id="sc"><img id="si" src="" style="width:100%;height:200px;object-fit:cover;margin-bottom:20px;display:none;filter:brightness(0.6);"><div id="ta" style="margin-bottom:30px;line-height:1.6;"></div><div id="ca" class="chs"></div></div>
    <script>const s={start:{i:'https://images.unsplash.com/photo-1550751827-4bd374c3f58b',t:"Kodlarda bir gölge gördün.",c:[{t:"Arkanı dön",n:"look"},{t:"Odaklan",n:"focus"}]},look:{t:"Kimse yok ama ekran parazitleniyor...",c:[{t:"Başa Dön",n:"start"}]},focus:{t:"'SENİ SİLİYORUM' yazıyor. Sistem çöküyor.",c:[{t:"Kaç",n:"start"}]}};
    function r(id){const n=s[id]; const img=document.getElementById("si"); if(n.i){img.src=n.i;img.style.display='block';}else img.style.display='none'; document.getElementById("ta").innerText=n.t; const ca=document.getElementById("ca"); ca.innerHTML=""; n.c.forEach(ch=>{const b=document.createElement("button"); b.innerText=ch.t; b.onclick=()=>r(ch.n); ca.appendChild(b);});} r("start");</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    if game in scores: scores[game].append(score)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
