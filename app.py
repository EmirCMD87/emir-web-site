from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- VERİTABANI (Sayaçlar ve Skorlar) ---
stats = {
    "total_visits": 0
}

scores = {
    "neon_arcade": [0],
    "void_command": [1],
    "lost_forest": [1]
}

# --- GENEL BİLEŞENLER ---
def get_footer():
    return f"""
<footer style="background: #080808; padding: 30px; border-top: 1px solid #1a1a1a; text-align: center; margin-top: auto;">
    <p style="color: #444; font-size: 0.8rem; letter-spacing: 2px;">© 2026 CANO STUDIO - CREATIVE LABS</p>
    <p style="color: #00bcd4; font-size: 0.7rem; margin-top: 10px; font-family: monospace;">TOPLAM ZİYARETÇİ: {stats['total_visits']}</p>
</footer>
"""

back_button_html = """
<a href="/" style="position: fixed; top: 20px; left: 20px; color: #666; text-decoration: none; font-family: sans-serif; font-size: 0.8rem; border: 1px solid #333; padding: 5px 15px; border-radius: 4px; z-index: 1000; transition: 0.3s;" onmouseover="this.style.color='#fff';this.style.borderColor='#fff'" onmouseout="this.style.color='#666';this.style.borderColor='#333'">
    ← KÜTÜPHANEYE DÖN
</a>
"""

# DESTEK VE TEŞEKKÜR SİSTEMİ
support_button_html = """
<a href="#" onclick="showSupport()" style="position: fixed; top: 20px; right: 20px; color: #00bcd4; text-decoration: none; font-family: sans-serif; font-size: 0.8rem; border: 1px solid #00bcd4; padding: 5px 15px; border-radius: 4px; z-index: 1000; transition: 0.3s; background: rgba(0, 188, 212, 0.05); font-weight: bold;" onmouseover="this.style.background='#00bcd4';this.style.color='#fff'" onmouseout="this.style.background='rgba(0, 188, 212, 0.05)';this.style.color='#00bcd4'">
    💳 DESTEK OL
</a>

<div id="supportModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.98); z-index:2000; align-items:center; justify-content:center; flex-direction:column; font-family:sans-serif; text-align:center; padding:20px;">
    <div id="supportBox" style="background:#0a0a0a; padding:30px; border-radius:15px; border:1px solid #00bcd4; max-width:480px; width:100%; box-shadow: 0 0 50px rgba(0, 188, 212, 0.15);">
        <div id="supportContent">
            <h2 style="color:#00bcd4; margin-bottom:5px;">Cano Studio'yu Destekle</h2>
            <div style="display:flex; gap:10px; margin-bottom:20px; margin-top:20px;">
                <button onclick="switchTab('ininal')" id="tab-ininal" style="flex:1; padding:10px; border:1px solid #00bcd4; background:#00bcd4; color:#000; cursor:pointer; font-weight:bold; border-radius:4px;">ininal</button>
                <button onclick="switchTab('banka')" id="tab-banka" style="flex:1; padding:10px; border:1px solid #333; background:transparent; color:#666; cursor:pointer; font-weight:bold; border-radius:4px;">Banka / EFT</button>
            </div>

            <div id="panel-ininal">
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin-bottom:20px;">
                    <button class="amt-btn" onclick="copyAction('ininal', 10)">10 TL</button>
                    <button class="amt-btn" onclick="copyAction('ininal', 50)">50 TL</button>
                    <button class="amt-btn" onclick="copyAction('ininal', 100)">100 TL</button>
                </div>
                <div style="background:#000; padding:10px; border:1px dashed #333; border-radius:8px; color:#fff; font-weight:bold; letter-spacing:2px;">4000 0000 0000 0</div>
            </div>

            <div id="panel-banka" style="display:none;">
                <div style="text-align:left; background:#000; padding:15px; border-radius:8px; border:1px solid #222; color:#fff; font-size:0.8rem;">
                    <b>ALICI:</b> [İSMİNİZ]<br>
                    <b>IBAN:</b> TR00 0000 0000 0000 0000 0000 00<br>
                    <span style="color:#ff4500; font-size:0.7rem;">* Açıklamaya barkod numaranızı yazmayı unutmayın!</span>
                </div>
                <button class="amt-btn" style="width:100%; margin-top:15px;" onclick="copyAction('IBAN', 'Tümü')">IBAN KOPYALA</button>
            </div>

            <button onclick="hideSupport()" style="background:transparent; color:#444; border:none; cursor:pointer; font-size:0.8rem; text-decoration:underline; margin-top:20px;">Kapat</button>
        </div>
    </div>
</div>

<style>
.amt-btn { background: #111; border: 1px solid #222; color: #fff; padding: 10px; border-radius: 4px; cursor: pointer; transition: 0.2s; font-size: 0.8rem; }
.amt-btn:hover { border-color: #00bcd4; color:#00bcd4; }
</style>

<script>
function showSupport() { document.getElementById('supportModal').style.display='flex'; }
function hideSupport() { document.getElementById('supportModal').style.display='none'; location.reload(); }
function switchTab(t) {
    document.getElementById('panel-ininal').style.display = t==='ininal'?'block':'none';
    document.getElementById('panel-banka').style.display = t==='banka'?'block':'none';
    document.getElementById('tab-ininal').style.background = t==='ininal'?'#00bcd4':'transparent';
    document.getElementById('tab-banka').style.background = t==='banka'?'#00bcd4':'transparent';
}
function copyAction(method, amt) {
    const val = method === 'ininal' ? "4000000000000" : "TR000000000000000000000000";
    navigator.clipboard.writeText(val);
    document.getElementById('supportBox').innerHTML = `
        <h2 style="color:#00bcd4;">Adamsın! ❤️</h2>
        <p style="color:#fff;">${amt} desteğin için teşekkürler! Bilgiler kopyalandı.</p>
        <button onclick="location.reload()" style="background:#00bcd4; color:#000; border:none; padding:10px 30px; border-radius:4px; cursor:pointer; font-weight:bold; margin-top:20px;">OYUNA DÖN</button>
    `;
}
</script>
"""

# --- 1. ANA SAYFA ---
@app.route('/')
def home():
    stats["total_visits"] += 1
    max_arcade = max(scores["neon_arcade"])
    max_void = max(scores["void_command"])
    forest_lvl = max(scores["lost_forest"])
    
    html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Studio | Dashboard</title>
    <style>
        * { box-sizing: border-box; transition: 0.3s ease; }
        body { background: #020202; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header { padding: 40px 20px; text-align: center; }
        h1 { font-size: 2.5rem; letter-spacing: 12px; margin: 0; color: #fff; font-weight: 200; }
        .container { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; padding: 40px; max-width: 1400px; margin: 0 auto; width:100%; }
        .game-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 30px; border-radius: 8px; cursor: pointer; }
        .game-card:hover { border-color: #fff; background: #111; transform: translateY(-5px); }
        .status { font-size: 9px; letter-spacing: 2px; border: 1px solid; display: inline-block; padding: 2px 8px; margin-bottom: 15px; border-radius: 4px; }
        .leaderboard { background: #050505; border: 1px solid #1a1a1a; padding: 30px; margin: 0 40px 40px 40px; border-radius: 8px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #111; }
        th { color: #555; text-transform: uppercase; font-size: 0.7rem; }
        .val { color: #fff; font-weight: bold; text-align: right; }
    </style>
</head>
<body>
    VAR_SUPPORT
    <div class="header"><h1>CANO STUDIO</h1></div>
    <div class="container">
        <div class="game-card" onclick="window.location.href='/neon-arcade'">
            <div class="status" style="color:#00d4ff;">ARCADE</div>
            <h2>NEON ARCADE</h2>
        </div>
        <div class="game-card" onclick="window.location.href='/void-command'">
            <div class="status" style="color:#00ff88;">STRATEGY</div>
            <h2>VOID COMMAND</h2>
        </div>
        <div class="game-card" onclick="window.location.href='/lost-forest'">
            <div class="status" style="color:#ff4500;">FPS HORROR</div>
            <h2>LOST FOREST</h2>
        </div>
        <div class="game-card" onclick="window.location.href='/glitch-in-me'" style="border-color: #9b59b6;">
            <div class="status" style="color:#9b59b6;">NARRATIVE</div>
            <h2 style="color:#9b59b6">THE GLITCH IN ME</h2>
        </div>
    </div>
    <div class="leaderboard">
        <table>
            <tr><th>MODÜL</th><th style="text-align:right">BAŞARI</th></tr>
            <tr><td>Neon Score</td><td class="val">VAR_ARCADE</td></tr>
            <tr><td>Strategy Lvl</td><td class="val">VAR_VOID</td></tr>
            <tr><td>Horror Lvl</td><td class="val">VAR_FOREST</td></tr>
        </table>
    </div>
    VAR_FOOTER
</body>
</html>
"""
    return html.replace("VAR_ARCADE", str(max_arcade)).replace("VAR_VOID", str(max_void)).replace("VAR_FOREST", str(forest_lvl)).replace("VAR_FOOTER", get_footer()).replace("VAR_SUPPORT", support_button_html)

# --- OYUN ROUTE'LARI ---
@app.route('/neon-arcade')
def arcade():
    html = """<!DOCTYPE html><html><head><title>Arcade</title><style>body{background:#000;margin:0;overflow:hidden;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;}canvas{border:2px solid #00d4ff;}</style></head>
    <body>VAR_BACK VAR_SUPPORT<canvas id="c" width="400" height="500"></canvas>
    <script>const canvas=document.getElementById("c"), ctx=canvas.getContext("2d"); let bird, pipes, frames, score, gameActive;
    function reset() { bird={y:250,v:0,g:0.5,j:-8}; pipes=[]; frames=0; score=0; gameActive=true; }
    function gameOver() { gameActive=false; if(score > 0) fetch('/submit_score/neon_arcade/'+score); ctx.fillStyle="rgba(0,0,0,0.8)"; ctx.fillRect(0,0,400,500); ctx.fillStyle="#ff4500"; ctx.font="bold 30px Arial"; ctx.textAlign="center"; ctx.fillText("GAME OVER", 200, 220); ctx.fillStyle="#fff"; ctx.font="20px Arial"; ctx.fillText("Skor: "+score, 200, 260); ctx.fillStyle="#00d4ff"; ctx.font="14px Arial"; ctx.fillText("Tekrar oynamak için tıkla", 200, 310); }
    function draw() { if(!gameActive) return; ctx.fillStyle="#000"; ctx.fillRect(0,0,400,500); bird.v+=bird.g; bird.y+=bird.v; ctx.fillStyle="#00d4ff"; ctx.fillRect(50,bird.y,30,30); if(frames%100===0) pipes.push({x:400,h:Math.random()*250+50,s:false});
    for(let i=pipes.length-1; i>=0; i--) { let p=pipes[i]; p.x-=4; ctx.fillStyle="#111"; ctx.fillRect(p.x,0,50,p.h); ctx.fillRect(p.x,p.h+150,50,500); if(50+30>p.x && 50<p.x+50 && (bird.y<p.h || bird.y+30>p.h+150)) { gameOver(); return; } if(p.x<50 && !p.s){ score++; p.s=true; } if(p.x<-50) pipes.splice(i,1); }
    if(bird.y>500 || bird.y<0) { gameOver(); return; } ctx.fillStyle="#fff"; ctx.font="20px Arial"; ctx.fillText(score, 20, 40); frames++; requestAnimationFrame(draw); }
    window.onclick=()=>{ if(gameActive) bird.v=bird.j; else { reset(); draw(); } }; reset(); draw();</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

@app.route('/lost-forest')
def horror():
    html = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Lost Forest</title><style>body{background:#000;margin:0;overflow:hidden;color:white;font-family:monospace;} #ui{position:fixed;top:20px;width:100%;text-align:center;} #stats{position:fixed;bottom:20px;right:20px;color:#ff4500;} #joystick{position:fixed;bottom:40px;left:40px;width:100px;height:100px;background:rgba(255,255,255,0.1);border-radius:50%;display:none;touch-action:none;} #stick{position:absolute;top:30px;left:30px;width:40px;height:40px;background:rgba(255,255,255,0.2);border-radius:50%;} @media (max-width:768px){#joystick{display:block;}}</style></head>
    <body>VAR_BACK VAR_SUPPORT <div id="ui">LEVEL <span id="lvlDisplay">1</span></div><div id="stats">SÜRE: <span id="timer">300</span></div><div id="joystick"><div id="stick"></div></div><canvas id="canvas"></canvas>
    <script>const canvas=document.getElementById('canvas'), ctx=canvas.getContext('2d'); canvas.width=window.innerWidth; canvas.height=window.innerHeight; let level=1, timeLeft=300, player={x:1.5,y:1.5,dir:0,speed:0.06}, map=[], keys={}; let joy={active:false,x:0,y:0};
    function generateMap(size) { let newMap=Array.from({length:size},()=>Array(size).fill(1)); for(let y=1;y<size-1;y++) for(let x=1;x<size-1;x++) if(Math.random()>0.3) newMap[y][x]=0; newMap[1][1]=0; newMap[size-2][size-2]=2; return newMap; }
    function resetLevel() { let size=8+(level*2); map=generateMap(size); player.x=1.5; player.y=1.5; timeLeft=300; document.getElementById("lvlDisplay").innerText=level; }
    window.onkeydown=(e)=>keys[e.code]=true; window.onkeyup=(e)=>keys[e.code]=false;
    const jZone=document.getElementById("joystick"), jStick=document.getElementById("stick");
    jZone.ontouchmove=(e)=>{ joy.active=true; let t=e.touches[0], r=jZone.getBoundingClientRect(); let dx=t.clientX-(r.left+50), dy=t.clientY-(r.top+50); let d=Math.min(Math.hypot(dx,dy),40), a=Math.atan2(dy,dx); joy.x=Math.cos(a)*(d/40); joy.y=Math.sin(a)*(d/40); jStick.style.transform=`translate(${joy.x*30}px,${joy.y*30}px)`; };
    jZone.ontouchend=()=>{ joy.active=false; joy.x=0; joy.y=0; jStick.style.transform="translate(0,0)"; };
    setInterval(()=>{ if(timeLeft>0) timeLeft--; else { alert("SÜRE BİTTİ!"); level=1; resetLevel(); } document.getElementById("timer").innerText=timeLeft; },1000);
    function update() { let ox=player.x, oy=player.y; if(keys['KeyW']||joy.y<-0.2){player.x+=Math.cos(player.dir)*player.speed; player.y+=Math.sin(player.dir)*player.speed;} if(keys['KeyS']||joy.y>0.2){player.x-=Math.cos(player.dir)*player.speed; player.y-=Math.sin(player.dir)*player.speed;} if(keys['KeyA']||joy.x<-0.2) player.dir-=0.06; if(keys['KeyD']||joy.x>0.2) player.dir+=0.06;
    if(map[Math.floor(player.y)][Math.floor(player.x)]===1){player.x=ox; player.y=oy;} if(map[Math.floor(player.y)][Math.floor(player.x)]===2){fetch('/submit_score/lost_forest/'+level); alert("KAZANDIN!"); level++; resetLevel();}}
    function draw() { ctx.fillStyle="#050805"; ctx.fillRect(0,0,canvas.width,canvas.height/2); ctx.fillStyle="#020402"; ctx.fillRect(0,canvas.height/2,canvas.width,canvas.height); const rays=100, fov=Math.PI/3; for(let i=0;i<rays;i++){ let a=(player.dir-fov/2)+(i/rays)*fov, d=0, hit=0; while(d<15){d+=0.06; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d); if(ty<0||ty>=map.length||tx<0||tx>=map[0].length) break; if(map[ty][tx]>0){hit=map[ty][tx]; break;}} let h=canvas.height/(d*Math.cos(a-player.dir)); ctx.fillStyle=hit===2?"#fff":`rgb(0,${Math.max(0,180-d*12)},0)`; ctx.fillRect(i*(canvas.width/rays),(canvas.height-h)/2,canvas.width/rays+1,h);}
    let g=ctx.createRadialGradient(canvas.width/2,canvas.height/2,50,canvas.width/2,canvas.height/2,400); g.addColorStop(0,"transparent"); g.addColorStop(1,"rgba(0,0,0,0.98)"); ctx.fillStyle=g; ctx.fillRect(0,0,canvas.width,canvas.height); }
    function loop(){ update(); draw(); requestAnimationFrame(loop); } resetLevel(); loop();</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

@app.route('/void-command')
def strategy():
    html = """<!DOCTYPE html><html><head><title>Strategy</title><style>body{background:#000;color:#00ff88;margin:0;overflow:hidden;font-family:monospace;} #l{margin-top:50px;padding:20px;}</style></head>
    <body>VAR_BACK VAR_SUPPORT <div id="l">LEVEL: 1</div><canvas id="g"></canvas>
    <script>const c=document.getElementById("g"), ctx=c.getContext("2d"); c.width=window.innerWidth; c.height=window.innerHeight; let lvl=1, planets=[], sel=null;
    class P { constructor(x,y,r,o){this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:20;} draw(){ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#333'); ctx.lineWidth=sel===this?5:2; ctx.stroke(); ctx.fillStyle=ctx.strokeStyle; ctx.textAlign="center"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);}}
    function init(){ planets=[new P(150,c.height/2,45,'player')]; for(let i=0;i<lvl;i++) planets.push(new P(c.width-150,(c.height/(lvl+1))*(i+1),40,'enemy')); for(let i=0;i<6;i++) planets.push(new P(Math.random()*c.width, Math.random()*c.height, 30, 'neutral')); }
    c.onmousedown=(e)=>{ const r=c.getBoundingClientRect(); let mx=e.clientX-r.left, my=e.clientY-r.top; let p=planets.find(p=>Math.hypot(p.x-mx,p.y-my)<p.r); if(p){if(p.o==='player')sel=p; else if(sel){let f=sel.e/2; sel.e-=f; p.e-=f; if(p.e<0){p.o='player';p.e=Math.abs(p.e);} sel=null;}}else sel=null;};
    function loop(){ ctx.fillStyle="black"; ctx.fillRect(0,0,c.width,c.height); planets.forEach(p=>{if(p.o!=='neutral')p.e+=0.012*lvl; p.draw();}); if(!planets.some(p=>p.o==='enemy')){lvl++; fetch('/submit_score/void_command/'+lvl); document.getElementById("l").innerText="LEVEL: "+lvl; init();} requestAnimationFrame(loop); } init(); loop();</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

@app.route('/glitch-in-me')
def story_game():
    html = """<!DOCTYPE html><html><head><title>Glitch</title><style>body{background:#050505;color:#e0e0e0;font-family:sans-serif;margin:0;display:flex;align-items:center;justify-content:center;height:100vh;overflow:hidden;} #sc{max-width:650px;width:90%;padding:40px;background:#0a0a0a;border:1px solid #1a1a1a;} .img-s{width:100%;height:300px;object-fit:cover;margin-bottom:20px;filter:brightness(0.6);} .chs{display:flex;flex-direction:column;gap:12px;} button{background:transparent;border:1px solid #222;color:#888;padding:15px;cursor:pointer;text-align:left;}</style></head>
    <body>VAR_BACK VAR_SUPPORT <div id="sc"><img id="si" class="img-s" src="" style="display:none;"><div id="ta" style="margin-bottom:30px;line-height:1.8;"></div><div id="ca" class="chs"></div></div>
    <script>const s={start:{i:'https://images.unsplash.com/photo-1550751827-4bd374c3f58b',t:"Saat 04:12. Kodlarda bir gölge gördün.",c:[{t:"Bak",n:"look"},{t:"Odaklan",n:"focus"}]},look:{i:'https://images.unsplash.com/photo-1518770660439-4636190af475',t:"Kimse yok ama kapı aralandı...",c:[{t:"Kaç",n:"exit"}]},focus:{t:"'SENİ SİLİYORUM' yazıyor.",c:[{t:"Yalvar",n:"exit"}]},exit:{t:"Oyun Bitti.",c:[{t:"Kütüphane",n:"lib"}]}};
    function r(id){if(id==="lib"){location.href="/";return;} const n=s[id]; const img=document.getElementById("si"); if(n.i){img.src=n.i;img.style.display='block';}else img.style.display='none'; document.getElementById("ta").innerText=n.t; const ca=document.getElementById("ca"); ca.innerHTML=""; n.c.forEach(ch=>{const b=document.createElement("button"); b.innerText=ch.t; b.onclick=()=>r(ch.n); ca.appendChild(b);});} r("start");</script></body></html>"""
    return html.replace("VAR_BACK", back_button_html).replace("VAR_SUPPORT", support_button_html)

# --- API ---
@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    if game in scores: scores[game].append(score)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
