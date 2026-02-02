from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Basit Skor Veritabanı (Bellek üzerinde tutulur, uygulama kapanınca sıfırlanır)
scores = {
    "neon_arcade": [],
    "void_command": [],
    "lost_forest": []
}

# --- GENEL TEMA VE FOOTER ---
footer_html = """
<footer style="background: #080808; padding: 30px; border-top: 1px solid #1a1a1a; text-align: center; margin-top: auto;">
    <p style="color: #444; font-size: 0.8rem; letter-spacing: 2px;">© 2026 CANO STUDIO - GLOBAL SYSTEMS</p>
</footer>
"""

# --- 1. ANA PORTAL SAYFASI (SKOR TABLOSU EKLENDİ) ---
@app.route('/')
def home():
    return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cano Studio | Dashboard</title>
    <style>
        * {{ box-sizing: border-box; transition: 0.3s ease; }}
        body {{ background: #020202; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .header {{ padding: 60px 20px; text-align: center; }}
        h1 {{ font-size: 3rem; letter-spacing: 12px; margin: 0; color: #fff; font-weight: 200; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 40px; max-width: 1200px; margin: 0 auto; width:100%; }}
        .game-card {{ background: #0a0a0a; border: 1px solid #1a1a1a; padding: 30px; border-radius: 8px; cursor: pointer; }}
        .game-card:hover {{ border-color: #fff; background: #111; transform: translateY(-5px); }}
        .status {{ font-size: 9px; letter-spacing: 2px; border: 1px solid; display: inline-block; padding: 2px 8px; margin-bottom: 15px; border-radius: 4px; }}
        .leaderboard {{ background: #050505; border: 1px solid #1a1a1a; padding: 20px; margin: 0 40px; border-radius: 8px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #111; }}
        th {{ color: #555; text-transform: uppercase; font-size: 0.7rem; }}
    </style>
</head>
<body>
    <div class="header"><h1>CANO STUDIO</h1></div>
    <div class="container">
        <div class="game-card" onclick="window.location.href='/neon-arcade'">
            <div class="status" style="color:#00d4ff">ARCADE</div>
            <h2>NEON ARCADE</h2>
            <p style="color:#555">Anlık refleks testi. En yüksek skoru hedefle!</p>
        </div>
        <div class="game-card" onclick="window.location.href='/void-command'">
            <div class="status" style="color:#00ff88">STRATEGY</div>
            <h2>VOID COMMAND</h2>
            <p style="color:#555">Bölüm bazlı strateji. Galaksiyi feth et.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/lost-forest'">
            <div class="status" style="color:#ff4500">HORROR (FPS)</div>
            <h2 style="color:#ff4500">THE LOST FOREST</h2>
            <p style="color:#555">FPS Kamerası ile ormanda hayatta kal. Kapıyı bul.</p>
        </div>
    </div>
    
    <div class="leaderboard">
        <h3 style="letter-spacing: 5px; color:#444">GLOBAL LEADERBOARD</h3>
        <table>
            <tr><th>Oyun</th><th>Skor</th></tr>
            <tr><td>Neon Arcade</td><td>{max(scores['neon_arcade']+[0])}</td></tr>
            <tr><td>Void Command (Lvl)</td><td>{max(scores['void_command']+[0])}</td></tr>
        </table>
    </div>
    {footer_html}
</body>
</html>
"""

# --- 2. NEON ARCADE ---
@app.route('/neon-arcade')
def arcade():
    return """
<!DOCTYPE html>
<html>
<head><title>Neon Arcade</title><style>body{background:#000;margin:0;overflow:hidden;display:flex;justify-content:center;align-items:center;height:100vh;}canvas{border:2px solid #00d4ff;}</style></head>
<body>
    <canvas id="c" width="400" height="500"></canvas>
    <script>
        const canvas=document.getElementById("c"), ctx=canvas.getContext("2d");
        let bird, pipes, frames, score;
        function reset() {
            if(score > 0) fetch('/submit_score/neon_arcade/'+score);
            bird={y:250,v:0,g:0.5,j:-8}; pipes=[]; frames=0; score=0;
        }
        function draw() {
            ctx.fillStyle="#000"; ctx.fillRect(0,0,400,500);
            bird.v+=bird.g; bird.y+=bird.v;
            ctx.fillStyle="#00d4ff"; ctx.fillRect(50,bird.y,30,30);
            if(frames%100===0) pipes.push({x:400,h:Math.random()*250+50,s:false});
            pipes.forEach((p,i)=>{
                p.x-=4; ctx.fillStyle="#111"; ctx.fillRect(p.x,0,50,p.h); ctx.fillRect(p.x,p.h+150,50,500);
                if(50+30>p.x && 50<p.x+50 && (bird.y<p.h || bird.y+30>p.h+150)) reset();
                if(p.x<50 && !p.s) { score++; p.s=true; }
            });
            if(bird.y>500 || bird.y<0) reset();
            ctx.fillStyle="#fff"; ctx.fillText("Score: "+score, 10, 20);
            frames++; requestAnimationFrame(draw);
        }
        window.onclick=()=>bird.v=bird.j;
        reset(); draw();
    </script>
</body>
</html>
"""

# --- 3. THE LOST FOREST (FPS - 1. ŞAHIS KAMERA + FENER) ---
@app.route('/lost-forest')
def horror():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lost Forest FPS</title>
    <style>
        body{background:#000; margin:0; overflow:hidden; color:white; font-family:monospace;}
        #ui{position:fixed; top:20px; width:100%; text-align:center; z-index:10; pointer-events:none;}
        #joystick{position:fixed; bottom:40px; left:40px; width:100px; height:100px; background:rgba(255,255,255,0.1); border-radius:50%; display:none;}
        @media (max-width:768px){ #joystick{display:block;} }
    </style>
</head>
<body>
    <div id="ui">ORMANIN DERİNLİĞİNDEKİ IŞIĞA GİT...</div>
    <div id="joystick"><div id="stick" style="position:absolute; top:30px; left:30px; width:40px; height:40px; background:rgba(255,255,255,0.2); border-radius:50%;"></div></div>
    <canvas id="canvas"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;

        let player = { x: 5, y: 5, dir: 0, speed: 0.05 };
        let map = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,0,0,1,0,0,1],
            [1,0,0,0,2,0,0,0,0,1], // 2 = Kapı
            [1,1,1,1,1,1,1,1,1,1]
        ];

        let keys = {};
        window.onkeydown = (e) => keys[e.code] = true;
        window.onkeyup = (e) => keys[e.code] = false;

        function playStep() {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.frequency.setValueAtTime(60, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.02, audioCtx.currentTime);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        }

        function update() {
            let oldX = player.x, oldY = player.y;
            if(keys['KeyW']) { player.x += Math.cos(player.dir)*player.speed; player.y += Math.sin(player.dir)*player.speed; }
            if(keys['KeyS']) { player.x -= Math.cos(player.dir)*player.speed; player.y -= Math.sin(player.dir)*player.speed; }
            if(keys['KeyA']) player.dir -= 0.05;
            if(keys['KeyD']) player.dir += 0.05;

            if(map[Math.floor(player.y)][Math.floor(player.x)] === 1) { player.x = oldX; player.y = oldY; }
            if(map[Math.floor(player.y)][Math.floor(player.x)] === 2) { alert("KURTULDUN!"); location.href="/"; }
            if((keys['KeyW'] || keys['KeyS']) && Math.random() < 0.1) playStep();
        }

        function drawFPS() {
            // Gökyüzü ve Yer
            ctx.fillStyle = "#050805"; ctx.fillRect(0,0,canvas.width,canvas.height/2);
            ctx.fillStyle = "#020402"; ctx.fillRect(0,canvas.height/2,canvas.width,canvas.height);

            const numRays = 120;
            const fov = Math.PI/3;
            for(let i=0; i<numRays; i++) {
                let rayAngle = (player.dir - fov/2) + (i/numRays)*fov;
                let distance = 0;
                let hitWall = false;
                let hitDoor = false;

                while(!hitWall && distance < 15) {
                    distance += 0.05;
                    let testX = Math.floor(player.x + Math.cos(rayAngle)*distance);
                    let testY = Math.floor(player.y + Math.sin(rayAngle)*distance);
                    if(map[testY][testX] === 1) hitWall = true;
                    if(map[testY][testX] === 2) { hitWall = true; hitDoor = true; }
                }

                let wallHeight = canvas.height / (distance * Math.cos(rayAngle - player.dir));
                let brightness = Math.max(0, 255 - (distance * 20));
                ctx.fillStyle = hitDoor ? `rgb(255,255,255)` : `rgb(0, ${brightness/4}, 0)`;
                ctx.fillRect(i * (canvas.width/numRays), (canvas.height-wallHeight)/2, canvas.width/numRays + 1, wallHeight);
            }

            // Fener Efekti (Overlay)
            let grad = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 50, canvas.width/2, canvas.height/2, 400);
            grad.addColorStop(0, "rgba(255,255,200,0.1)");
            grad.addColorStop(1, "rgba(0,0,0,0.9)");
            ctx.fillStyle = grad; ctx.fillRect(0,0,canvas.width,canvas.height);
        }

        function loop() { update(); drawFPS(); requestAnimationFrame(loop); }
        loop();
    </script>
</body>
</html>
"""

# --- 4. VOID COMMAND (Strateji) ---
@app.route('/void-command')
def strategy():
    return """
<!DOCTYPE html>
<html>
<head><title>Void Command</title><style>body{background:#000;color:#00ff88;margin:0;overflow:hidden;font-family:monospace;}</style></head>
<body>
    <div id="l" style="padding:20px;">LEVEL: 1</div>
    <canvas id="g"></canvas>
    <script>
        const c=document.getElementById("g"), ctx=c.getContext("2d");
        c.width=window.innerWidth; c.height=window.innerHeight;
        let lvl=1, planets=[], sel=null;
        class P {
            constructor(x,y,r,o){this.x=x;this.y=y;this.r=r;this.o=o;this.e=o==='neutral'?5:20;}
            draw(){
                ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
                ctx.strokeStyle=this.o==='player'?'#00ff88':(this.o==='enemy'?'#f40':'#333');
                ctx.lineWidth=sel===this?4:2; ctx.stroke();
                ctx.fillStyle=ctx.strokeStyle; ctx.textAlign="center"; ctx.fillText(Math.floor(this.e),this.x,this.y+5);
            }
        }
        function init(){
            planets=[new P(100,c.height/2,40,'player')];
            for(let i=0;i<lvl;i++) planets.push(new P(c.width-100,(c.height/(lvl+1))*(i+1),35,'enemy'));
        }
        c.onclick=(e)=>{
            let p=planets.find(p=>Math.hypot(p.x-e.clientX,p.y-e.clientY)<p.r);
            if(p){ 
                if(p.o==='player') sel=p;
                else if(sel){ let f=sel.e/2; sel.e-=f; p.e-=f; if(p.e<0){p.o='player';p.e=Math.abs(p.e);} sel=null;}
            }
            if(!planets.some(p=>p.o==='enemy')){lvl++; fetch('/submit_score/void_command/'+lvl); init();}
        };
        function loop(){ ctx.fillStyle="black"; ctx.fillRect(0,0,c.width,c.height); planets.forEach(p=>{if(p.o!=='neutral')p.e+=0.01*lvl; p.draw();}); requestAnimationFrame(loop); }
        init(); loop();
    </script>
</body>
</html>
"""

# --- API: SKOR KAYDETME ---
@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    if game in scores:
        scores[game].append(score)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
