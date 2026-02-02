from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- SKOR VE İLERLEME VERİTABANI ---
scores = {
    "neon_arcade": [0],
    "void_command": [1],
    "lost_forest": [1]
}

# --- GENEL BİLEŞENLER ---
footer_html = """
<footer style="background: #080808; padding: 30px; border-top: 1px solid #1a1a1a; text-align: center; margin-top: auto;">
    <p style="color: #444; font-size: 0.8rem; letter-spacing: 2px;">© 2026 CANO STUDIO - CREATIVE LABS</p>
</footer>
"""

back_button_html = """
<a href="/" style="position: fixed; top: 20px; left: 20px; color: #666; text-decoration: none; font-family: sans-serif; font-size: 0.8rem; border: 1px solid #333; padding: 5px 15px; border-radius: 4px; z-index: 1000; transition: 0.3s;" onmouseover="this.style.color='#fff';this.style.borderColor='#fff'" onmouseout="this.style.color='#666';this.style.borderColor='#333'">
    ← KÜTÜPHANEYE DÖN
</a>
"""

# --- 1. ANA SAYFA ---
@app.route('/')
def home():
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
        .container { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; padding: 40px; max-width: 1200px; margin: 0 auto; width:100%; }
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
            <tr><th>MODÜL</th><th style="text-align:right">DURUM</th></tr>
            <tr><td>Neon High Score</td><td class="val">VAR_ARCADE</td></tr>
            <tr><td>Strategy Level</td><td class="val">Lvl VAR_VOID</td></tr>
            <tr><td>Horror Progress</td><td class="val">Lvl VAR_FOREST</td></tr>
        </table>
    </div>
    VAR_FOOTER
</body>
</html>
"""
    return html.replace("VAR_ARCADE", str(max_arcade)).replace("VAR_VOID", str(max_void)).replace("VAR_FOREST", str(forest_lvl)).replace("VAR_FOOTER", footer_html)

# --- 2. NEON ARCADE ---
@app.route('/neon-arcade')
def arcade():
    html = """
<!DOCTYPE html>
<html>
<head><title>Neon Arcade</title><style>body{background:#000;margin:0;overflow:hidden;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;}canvas{border:2px solid #00d4ff;}</style></head>
<body>
    VAR_BACK
    <canvas id="c" width="400" height="500"></canvas>
    <script>
        const canvas=document.getElementById("c"), ctx=canvas.getContext("2d");
        let bird, pipes, frames, score, gameActive;
        function reset() { bird={y:250,v:0,g:0.5,j:-8}; pipes=[]; frames=0; score=0; gameActive=true; }
        function gameOver() {
            gameActive=false;
            if(score > 0) fetch('/submit_score/neon_arcade/'+score);
            ctx.fillStyle="rgba(0,0,0,0.8)"; ctx.fillRect(0,0,400,500);
            ctx.fillStyle="#ff4500"; ctx.font="bold 30px Arial"; ctx.textAlign="center";
            ctx.fillText("GAME OVER", 200, 220);
            ctx.fillStyle="#fff"; ctx.font="20px Arial"; ctx.fillText("Skor: "+score, 200, 260);
            ctx.fillStyle="#00d4ff"; ctx.font="14px Arial"; ctx.fillText("Tekrar oynamak için tıkla", 200, 310);
        }
        function draw() {
            if(!gameActive) return;
            ctx.fillStyle="#000"; ctx.fillRect(0,0,400,500);
            bird.v+=bird.g; bird.y+=bird.v;
            ctx.fillStyle="#00d4ff"; ctx.fillRect(50,bird.y,30,30);
            if(frames%100===0) pipes.push({x:400,h:Math.random()*250+50,s:false});
            for(let i=pipes.length-1; i>=0; i--) {
                let p=pipes[i]; p.x-=4;
                ctx.fillStyle="#111"; ctx.fillRect(p.x,0,50,p.h); ctx.fillRect(p.x,p.h+150,50,500);
                if(50+30>p.x && 50<p.x+50 && (bird.y<p.h || bird.y+30>p.h+150)) { gameOver(); return; }
                if(p.x<50 && !p.s){ score++; p.s=true; }
                if(p.x<-50) pipes.splice(i,1);
            }
            if(bird.y>500 || bird.y<0) { gameOver(); return; }
            ctx.fillStyle="#fff"; ctx.font="20px Arial"; ctx.fillText(score, 20, 40);
            frames++; requestAnimationFrame(draw);
        }
        window.onclick=()=>{ if(gameActive) bird.v=bird.j; else { reset(); draw(); } };
        reset(); draw();
    </script>
</body>
</html>
"""
    return html.replace("VAR_BACK", back_button_html)

# --- 3. THE LOST FOREST (FPS) ---
@app.route('/lost-forest')
def horror():
    html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lost Forest FPS</title>
    <style>
        body{background:#000; margin:0; overflow:hidden; color:white; font-family:monospace;}
        #ui{position:fixed; top:20px; width:100%; text-align:center; z-index:10; pointer-events:none;}
        #stats{position:fixed; bottom:20px; right:20px; text-align:right; color:#ff4500; font-size:1.2rem;}
    </style>
</head>
<body>
    VAR_BACK
    <div id="ui">LEVEL <span id="lvlDisplay">1</span> - KAPIDAN KAÇ!</div>
    <div id="stats">SÜRE: <span id="timer">300</span>s</div>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let level = 1, timeLeft = 300, player = { x: 1.5, y: 1.5, dir: 0, speed: 0.06 }, map = [], keys = {};

        function generateMap(size) {
            let newMap = Array.from({length: size}, () => Array(size).fill(1));
            for(let y=1; y<size-1; y++) for(let x=1; x<size-1; x++) if(Math.random() > 0.3) newMap[y][x] = 0;
            newMap[1][1] = 0; newMap[size-2][size-2] = 2; return newMap;
        }

        function resetLevel() {
            let size = 8 + (level * 2); map = generateMap(size);
            player.x = 1.5; player.y = 1.5; player.dir = 0; timeLeft = 300;
            document.getElementById("lvlDisplay").innerText = level;
        }

        window.onkeydown=(e)=>keys[e.code]=true;
        window.onkeyup=(e)=>keys[e.code]=false;

        setInterval(() => { if(timeLeft > 0) timeLeft--; else { alert("SÜRE BİTTİ!"); level=1; resetLevel(); }
            document.getElementById("timer").innerText = timeLeft;
        }, 1000);

        function update() {
            let ox=player.x, oy=player.y;
            if(keys['KeyW']) { player.x+=Math.cos(player.dir)*player.speed; player.y+=Math.sin(player.dir)*player.speed; }
            if(keys['KeyS']) { player.x-=Math.cos(player.dir)*player.speed; player.y-=Math.sin(player.dir)*player.speed; }
            if(keys['KeyA']) player.dir-=0.06; if(keys['KeyD']) player.dir+=0.06;
            if(map[Math.floor(player.y)][Math.floor(player.x)] === 1) { player.x=ox; player.y=oy; }
            if(map[Math.floor(player.y)][Math.floor(player.x)] === 2) { 
                fetch('/submit_score/lost_forest/'+level); alert("LEVEL TAMAMLANDI!"); level++; resetLevel(); 
            }
        }

        function draw() {
            ctx.fillStyle="#050805"; ctx.fillRect(0,0,canvas.width,canvas.height/2);
            ctx.fillStyle="#020402"; ctx.fillRect(0,canvas.height/2,canvas.width,canvas.height);
            const rays=100, fov=Math.PI/3;
            for(let i=0; i<rays; i++){
                let a=(player.dir-fov/2)+(i/rays)*fov, d=0, hit=0;
                while(d<15){ d+=0.06; let tx=Math.floor(player.x+Math.cos(a)*d), ty=Math.floor(player.y+Math.sin(a)*d);
                    if(ty<0||ty>=map.length||tx<0||tx>=map[0].length) break; if(map[ty][tx]>0){ hit=map[ty][tx]; break; }
                }
                let h=canvas.height/(d*Math.cos(a-player.dir));
                ctx.fillStyle=hit===2?"#fff":`rgb(0,${Math.max(0,180-d*12)},0)`;
                ctx.fillRect(i*(canvas.width/rays), (canvas.height-h)/2, canvas.width/rays+1, h);
            }
            let g=ctx.createRadialGradient(canvas.width/2,canvas.height/2,50,canvas.width/2,canvas.height/2,400);
            g.addColorStop(0,"transparent"); g.addColorStop(1,"rgba(0,0,0,0.98)");
            ctx.fillStyle=g; ctx.fillRect(0,0,canvas.width,canvas.height);
        }
        function loop(){ update(); draw(); requestAnimationFrame(loop); }
        resetLevel(); loop();
    </script>
</body>
</html>
"""
    return html.replace("VAR_BACK", back_button_html)

# --- 4. VOID COMMAND ---
@app.route('/void-command')
def strategy():
    html = """
<!DOCTYPE html>
<html>
<head><title>Void Command</title><style>body{background:#000;color:#00ff88;margin:0;overflow:hidden;font-family:monospace;} #l{margin-top:50px; padding:20px; font-size:1.2rem;}</style></head>
<body>
    VAR_BACK
    <div id="l">LEVEL: 1</div>
    <canvas id="g"></canvas>
    <script>
        const c=document.getElementById("g"), ctx=c.getContext("2d");
        c.width=window.innerWidth; c.height=window.innerHeight;
        let lvl=1, planets=[], sel=null;
        class P { constructor(x,y,r,o){this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:20;}
            draw(){ ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
                ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#333');
                ctx.lineWidth=sel===this?5:2; ctx.stroke();
                ctx.fillStyle=ctx.strokeStyle; ctx.textAlign="center"; ctx.font="bold 14px Arial"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);
            }
        }
        function init(){
            planets=[new P(150,c.height/2,45,'player')];
            for(let i=0;i<lvl;i++) planets.push(new P(c.width-150,(c.height/(lvl+1))*(i+1),40,'enemy'));
            for(let i=0;i<6;i++) planets.push(new P(Math.random()*(c.width-400)+200, Math.random()*(c.height-200)+100, 30, 'neutral'));
        }
        c.addEventListener('mousedown', (e) => {
            const rect = c.getBoundingClientRect(); const mx = e.clientX - rect.left; const my = e.clientY - rect.top;
            let clicked = planets.find(p => Math.hypot(p.x - mx, p.y - my) < p.r);
            if(clicked) { if(clicked.o === 'player') { sel = clicked; }
                else if(sel) { let force = sel.e / 2; sel.e -= force; clicked.e -= force;
                    if(clicked.e < 0) { clicked.o = 'player'; clicked.e = Math.abs(clicked.e); } sel = null;
                }
            } else { sel = null; }
        });
        function loop(){
            ctx.fillStyle="black"; ctx.fillRect(0,0,c.width,c.height);
            planets.forEach(p=>{ if(p.o !== 'neutral') p.e += 0.012 * lvl; p.draw(); });
            if(!planets.some(p => p.o === 'enemy')){ lvl++; fetch('/submit_score/void_command/'+lvl); document.getElementById("l").innerText="LEVEL: "+lvl; init(); }
            requestAnimationFrame(loop);
        }
        init(); loop();
    </script>
</body>
</html>
"""
    return html.replace("VAR_BACK", back_button_html)

# --- 5. THE GLITCH IN ME (GÖRSEL DESTEKLİ HİKAYE) ---
@app.route('/glitch-in-me')
def story_game():
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>The Glitch in Me | Cano Studio</title>
    <style>
        body { background: #050505; color: #e0e0e0; font-family: 'Segoe UI', serif; margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        #story-container { max-width: 700px; width: 90%; padding: 40px; background: #0a0a0a; border: 1px solid #1a1a1a; position: relative; }
        #story-image { width: 100%; height: 350px; object-fit: cover; margin-bottom: 25px; border-radius: 4px; border: 1px solid #9b59b633; }
        .text { font-size: 1.1rem; line-height: 1.8; margin-bottom: 30px; min-height: 150px; color: #bbb; }
        .choices { display: flex; flex-direction: column; gap: 12px; }
        button { background: transparent; border: 1px solid #222; color: #666; padding: 15px; cursor: pointer; text-align: left; transition: 0.3s; font-size: 0.9rem; }
        button:hover { border-color: #9b59b6; color: #fff; background: rgba(155, 89, 182, 0.05); }
        .glitch-text { color: #9b59b6; font-weight: bold; }
    </style>
</head>
<body>
    VAR_BACK
    <div id="story-container">
        <img id="story-image" src="" style="display:none;">
        <div id="ta" class="text">Yükleniyor...</div>
        <div id="ca" class="choices"></div>
    </div>

    <script>
        const s = {
            start: {
                img: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000',
                text: "Saat 04:12. Odan zifiri karanlık, tek ışık kaynağın monitörün. Kodlar arasında bir <span class='glitch-text'>gölgenin</span> geçtiğini görüyorsun. Ne yaparsın?",
                choices: [{ t: "Arkanı dönüp bak.", n: "look_back" }, { t: "Ekrana odaklan.", n: "focus" }]
            },
            look_back: {
                img: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=1000',
                text: "Arkanı dönüyorsun. Kimse yok. Ama çalışma koltuğunun üzerindeki hırkanın şekli, sanki birisi orada oturuyormuş gibi duruyor.",
                choices: [{ t: "Kapıyı kapatmaya git.", n: "door" }, { t: "Işıkları aç.", n: "lights" }]
            },
            focus: {
                img: 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&q=80&w=1000',
                text: "Ekrana odaklanıyorsun ama terminalde şu beliriyor: <span class='glitch-text'>'SENİ SİLİYORUM.'</span> Parmakların yavaşça şeffaflaşıyor.",
                choices: [{ t: "Fişi çek.", n: "start" }, { t: "Sisteme yalvar.", n: "start" }]
            },
            door: { text: "Kapıya yürürken aynada yansımanın sana değil, arkandaki karanlığa baktığını görüyorsun. (Kabus Sonu)", choices: [{ t: "Başa Dön", n: "start" }] },
            lights: { text: "Düğmeye basıyorsun ama ışıklar yanmıyor. Bilgisayar fanı çığlık atar gibi dönmeye başlıyor. (Hata Sonu)", choices: [{ t: "Başa Dön", n: "start" }] }
        };

        function r(id) {
            if(id === "exit") { window.location.href = "/"; return; }
            const node = s[id];
            const img = document.getElementById("story-image");
            if (node.img) { img.src = node.img; img.style.display = 'block'; } else { img.style.display = 'none'; }
            document.getElementById("ta").innerHTML = node.text;
            const ca = document.getElementById("ca"); ca.innerHTML = "";
            node.choices.forEach(c => {
                const b = document.createElement("button"); b.innerHTML = c.t;
                b.onclick = () => r(c.n); ca.appendChild(b);
            });
        }
        r("start");
    </script>
</body>
</html>
"""
    return html.replace("VAR_BACK", back_button_html)

# --- API ---
@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    if game in scores: scores[game].append(score)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
