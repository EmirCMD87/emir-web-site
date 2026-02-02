from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- SKOR VERİTABANI ---
# Uygulama çalıştığı sürece skorları burada tutar.
scores = {
    "neon_arcade": [0],
    "void_command": [0],
    "lost_forest": [0]
}

# --- ORTAK FOOTER ---
footer_html = """
<footer style="background: #080808; padding: 30px; border-top: 1px solid #1a1a1a; text-align: center; margin-top: auto;">
    <p style="color: #444; font-size: 0.8rem; letter-spacing: 2px;">© 2026 CANO STUDIO - GLOBAL SYSTEMS</p>
</footer>
"""

# --- 1. ANA SAYFA (Dinamik Skor Tablosu ile) ---
@app.route('/')
def home():
    max_arcade = max(scores["neon_arcade"])
    max_void = max(scores["void_command"])
    forest_wins = len([x for x in scores["lost_forest"] if x > 0])
    
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
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; padding: 40px; max-width: 1200px; margin: 0 auto; width:100%; }}
        .game-card {{ background: #0a0a0a; border: 1px solid #1a1a1a; padding: 30px; border-radius: 8px; cursor: pointer; }}
        .game-card:hover {{ border-color: #fff; background: #111; transform: translateY(-5px); }}
        .status {{ font-size: 9px; letter-spacing: 2px; border: 1px solid; display: inline-block; padding: 2px 8px; margin-bottom: 15px; border-radius: 4px; }}
        .leaderboard {{ background: #050505; border: 1px solid #1a1a1a; padding: 30px; margin: 0 40px 40px 40px; border-radius: 8px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #111; }}
        th {{ color: #555; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 2px; }}
        .val {{ color: #fff; font-weight: bold; text-align: right; }}
    </style>
</head>
<body>
    <div class="header"><h1>CANO STUDIO</h1></div>
    <div class="container">
        <div class="game-card" onclick="window.location.href='/neon-arcade'">
            <div class="status" style="color:#00d4ff; border-color:#00d4ff;">ARCADE</div>
            <h2>NEON ARCADE</h2>
            <p style="color:#555">Hızlı refleks testi. Game Over ekranı ve skor kaydı aktif.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/void-command'">
            <div class="status" style="color:#00ff88; border-color:#00ff88;">STRATEGY</div>
            <h2>VOID COMMAND</h2>
            <p style="color:#555">Level tabanlı uzay stratejisi. Seviye atladıkça zorlaşır.</p>
        </div>
        <div class="game-card" onclick="window.location.href='/lost-forest'">
            <div class="status" style="color:#ff4500; border-color:#ff4500;">FPS HORROR</div>
            <h2 style="color:#ff4500">THE LOST FOREST</h2>
            <p style="color:#555">FPS kamerası ve el feneri ile ormanda hayatta kal.</p>
        </div>
    </div>
    
    <div class="leaderboard">
        <h3 style="letter-spacing: 5px; color:#444; margin-top:0;">GLOBAL LEADERBOARD</h3>
        <table>
            <tr><th>OYUN MODÜLÜ</th><th style="text-align:right">EN YÜKSEK SKOR / BAŞARI</th></tr>
            <tr><td>Neon Arcade</td><td class="val">{max_arcade} Puan</td></tr>
            <tr><td>Void Command</td><td class="val">Level {max_void}</td></tr>
            <tr><td>Lost Forest</td><td class="val">{forest_wins} Kaçış</td></tr>
        </table>
    </div>
    {footer_html}
</body>
</html>
"""

# --- 2. NEON ARCADE (Game Over & Skor Kaydı) ---
@app.route('/neon-arcade')
def arcade():
    return """
<!DOCTYPE html>
<html>
<head><title>Neon Arcade | Cano Studio</title><style>body{background:#000;margin:0;overflow:hidden;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;}canvas{border:2px solid #00d4ff;}</style></head>
<body>
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
            ctx.fillStyle="#00d4ff"; ctx.font="14px Arial"; ctx.fillText("Devam etmek için tıkla", 200, 310);
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

# --- 3. THE LOST FOREST (FPS + Fener + WASD + Mobil) ---
@app.route('/lost-forest')
def horror():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lost Forest FPS | Cano Studio</title>
    <style>
        body{background:#000; margin:0; overflow:hidden; color:white; font-family:monospace;}
        #ui{position:fixed; top:20px; width:100%; text-align:center; z-index:10; pointer-events:none; letter-spacing:2px;}
        #joystick{position:fixed; bottom:40px; left:40px; width:100px; height:100px; background:rgba(255,255,255,0.1); border-radius:50%; display:none; touch-action:none;}
        #stick{position:absolute; top:30px; left:30px; width:40px; height:40px; background:rgba(255,255,255,0.2); border-radius:50%;}
        @media (max-width:768px){ #joystick{display:block;} }
    </style>
</head>
<body>
    <div id="ui">ORMANIN DERİNLİĞİNDEKİ BEYAZ IŞIĞA ULAŞ...</div>
    <div id="joystick"><div id="stick"></div></div>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;

        let player = { x: 2, y: 2, dir: 0, speed: 0.05 };
        let map = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
            [1,1,1,0,1,1,1,1,0,1,1,0,1,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,2,1], // 2 = Kapı (Bitiş)
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ];

        let keys = {};
        window.onkeydown=(e)=>keys[e.code]=true;
        window.onkeyup=(e)=>keys[e.code]=false;

        // Mobil Kontrol
        let joy = {active: false, x:0, y:0};
        const jZone = document.getElementById("joystick");
        const jStick = document.getElementById("stick");
        jZone.ontouchmove=(e)=>{
            joy.active=true; let t=e.touches[0], r=jZone.getBoundingClientRect();
            let dx=t.clientX-(r.left+50), dy=t.clientY-(r.top+50);
            let d=Math.min(Math.hypot(dx,dy),40), a=Math.atan2(dy,dx);
            joy.x=Math.cos(a)*(d/40); joy.y=Math.sin(a)*(d/40);
            jStick.style.transform=`translate(${joy.x*30}px,${joy.y*30}px)`;
        };
        jZone.ontouchend=()=>{ joy.active=false; joy.x=0; joy.y=0; jStick.style.transform="translate(0,0)"; };

        function update() {
            let oldX=player.x, oldY=player.y;
            let moveX = 0, moveY = 0;
            if(keys['KeyW'] || joy.y < -0.2) { moveX += Math.cos(player.dir)*player.speed; moveY += Math.sin(player.dir)*player.speed; }
            if(keys['KeyS'] || joy.y > 0.2) { moveX -= Math.cos(player.dir)*player.speed; moveY -= Math.sin(player.dir)*player.speed; }
            if(keys['KeyA'] || joy.x < -0.2) player.dir -= 0.04;
            if(keys['KeyD'] || joy.x > 0.2) player.dir += 0.04;

            player.x += moveX; player.y += moveY;
            if(map[Math.floor(player.y)][Math.floor(player.x)] === 1) { player.x=oldX; player.y=oldY; }
            if(map[Math.floor(player.y)][Math.floor(player.x)] === 2) { 
                fetch('/submit_score/lost_forest/1');
                alert("KURTULDUN!"); location.href="/"; 
            }
        }

        function draw() {
            // Tavan ve Yer (Lo-Fi Korku Havası)
            ctx.fillStyle="#050805"; ctx.fillRect(0,0,canvas.width,canvas.height/2);
            ctx.fillStyle="#020402"; ctx.fillRect(0,canvas.height/2,canvas.width,canvas.height);

            const rays=100, fov=Math.PI/3;
            for(let i=0; i<rays; i++){
                let angle = (player.dir-fov/2)+(i/rays)*fov;
                let dist=0, hit=0;
                while(dist<15){
                    dist+=0.05;
                    let tx=Math.floor(player.x+Math.cos(angle)*dist), ty=Math.floor(player.y+Math.sin(angle)*dist);
                    if(map[ty][tx]>0){ hit=map[ty][tx]; break; }
                }
                let h = canvas.height/(dist*Math.cos(angle-player.dir));
                let b = Math.max(0, 200-(dist*15));
                ctx.fillStyle = hit===2 ? `rgb(255,255,255)` : `rgb(0,${b/3},0)`;
                ctx.fillRect(i*(canvas.width/rays), (canvas.height-h)/2, canvas.width/rays+1, h);
            }
            // Fener Efekti
            let g=ctx.createRadialGradient(canvas.width/2,canvas.height/2,50,canvas.width/2,canvas.height/2,350);
            g.addColorStop(0,"transparent"); g.addColorStop(1,"rgba(0,0,0,0.95)");
            ctx.fillStyle=g; ctx.fillRect(0,0,canvas.width,canvas.height);
        }
        function loop(){ update(); draw(); requestAnimationFrame(loop); }
        loop();
    </script>
</body>
</html>
"""

# --- 4. VOID COMMAND (Strateji & Level Sistemi) ---
@app.route('/void-command')
def strategy():
    return """
<!DOCTYPE html>
<html>
<head><title>Void Command | Cano Studio</title><style>body{background:#000;color:#00ff88;margin:0;overflow:hidden;font-family:monospace;}</style></head>
<body>
    <div id="l" style="padding:20px; font-size:1.2rem;">LEVEL: 1</div>
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
            for(let i=0;i<5;i++) planets.push(new P(Math.random()*c.width, Math.random()*c.height, 25, 'neutral'));
        }
        c.onclick=(e)=>{
            let p=planets.find(p=>Math.hypot(p.x-e.clientX,p.y-e.clientY)<p.r);
            if(p){ 
                if(p.o==='player') sel=p;
                else if(sel){ let f=sel.e/2; sel.e-=f; p.e-=f; if(p.e<0){p.o='player';p.e=Math.abs(p.e);} sel=null;}
            }
            if(!planets.some(p=>p.o==='enemy')){lvl++; fetch('/submit_score/void_command/'+lvl); document.getElementById("l").innerText="LEVEL: "+lvl; init();}
        };
        function loop(){ ctx.fillStyle="black"; ctx.fillRect(0,0,c.width,c.height); planets.forEach(p=>{if(p.o!=='neutral')p.e+=0.01*lvl; p.draw();}); requestAnimationFrame(loop); }
        init(); loop();
    </script>
</body>
</html>
"""

# --- API: SKOR KAYIT ---
@app.route('/submit_score/<game>/<int:score>')
def submit_score(game, score):
    if game in scores:
        scores[game].append(score)
        print(f"Skor Alındı: {game} -> {score}")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
