from flask import Flask
import os

app = Flask(__name__)

# --- ORTAK FOOTER ---
footer_html = """
<footer style="background: #111; padding: 25px; border-top: 2px solid #333; text-align: center; margin-top: auto;">
    <button style="background:#ff4500; color:white; padding:12px 25px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">☕ DESTEK OL</button>
    <button style="background:#444; color:white; padding:12px 25px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; margin-left:10px;" onclick="document.getElementById('c-box').style.display='block'">✉️ İLETİŞİM</button>
    <div id="c-box" style="display:none; color:#aaa; margin-top:10px;">iletisim@canostudio.com</div>
</footer>
"""

# --- ANA SAYFA ---
ana_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><title>Cano Game Studio | Portal</title>
    <style>
        body {{ background: #0a0a0a; color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
        .container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; padding: 40px; max-width: 1200px; margin: 0 auto; }}
        .card {{ border: 2px solid #222; padding: 40px; border-radius: 20px; cursor: pointer; text-align: center; transition: 0.4s; }}
        .card:hover {{ transform: scale(1.05); border-color: #00d4ff; box-shadow: 0 0 30px rgba(0,212,255,0.1); }}
        h1 {{ text-align: center; margin-top: 50px; letter-spacing: 5px; color: #00d4ff; }}
    </style>
</head>
<body>
    <h1>CANO GAME STUDIO</h1>
    <div class="container">
        <div class="card" onclick="window.location.href='/neon-arcade'">
            <h2 style="color:#00d4ff">NEON ARCADE</h2>
            <p>Uçan Kare (Klasik Refleks)</p>
        </div>
        <div class="card" onclick="window.location.href='/horror'" style="border-color:#e74c3c">
            <h2 style="color:#e74c3c">HORROR / ACTION</h2>
            <p>Zihnin Karanlığı (3D Açık Dünya)</p>
        </div>
    </div>
    {footer_html}
</body>
</html>
"""

# --- 3D HORROR OYUNU ---
horror_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><title>Zihnin Karanlığı</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        #ui-voice { position: fixed; top: 15%; width: 100%; text-align: center; color: rgba(255,255,255,0.5); font-family: monospace; font-size: 20px; z-index: 100; pointer-events: none; transition: 1s; opacity: 0; }
        #inventory { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; background: rgba(0,0,0,0.9); border: 1px solid #e74c3c; padding: 20px; display: none; color: white; z-index: 200; font-family: monospace; }
        #dist { position: fixed; bottom: 20px; right: 20px; color: #444; font-family: monospace; }
    </style>
</head>
<body>
<div id="ui-voice"></div>
<div id="inventory"><h3>ENVANTER (E)</h3><p>🔦 Fener</p><p>🔪 Çakı</p><p>📱 Telefon</p></div>
<div id="dist">Hedef: <span id="dv">---</span>m</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    let scene, camera, renderer, flashLight, inv = false;
    let mvF = false, mvB = false, mvL = false, mvR = false;
    let vel = new THREE.Vector3(), dir = new THREE.Vector3();
    let hosp = new THREE.Vector3(0, 0, -300);

    init(); animate();

    function init() {
        scene = new THREE.Scene(); scene.background = new THREE.Color(0x010101);
        scene.fog = new THREE.FogExp2(0x010101, 0.05);
        camera = new THREE.PerspectiveCamera(70, window.innerWidth/window.innerHeight, 0.1, 1500);
        camera.rotation.order = 'YXZ';
        
        const amb = new THREE.AmbientLight(0x404040, 0.1); scene.add(amb);
        flashLight = new THREE.SpotLight(0xffffff, 2.8);
        flashLight.distance = 75; flashLight.angle = Math.PI/6; flashLight.castShadow = true;
        camera.add(flashLight); flashLight.position.set(0,0,0.1);
        let target = new THREE.Object3D(); target.position.set(0,0,-1);
        camera.add(target); flashLight.target = target; scene.add(camera);

        const floor = new THREE.Mesh(new THREE.PlaneGeometry(2000,2000), new THREE.MeshStandardMaterial({color:0x050505}));
        floor.rotation.x = -Math.PI/2; floor.receiveShadow = true; scene.add(floor);

        for(let i=0; i<500; i++) {
            let t = new THREE.Mesh(new THREE.CylinderGeometry(0.3,0.5,10,6), new THREE.MeshStandardMaterial({color:0x111111}));
            t.position.set(Math.random()*600-300, 5, Math.random()*600-300);
            if(t.position.distanceTo(hosp) > 40) scene.add(t);
        }

        const hBody = new THREE.Mesh(new THREE.BoxGeometry(60,40,80), new THREE.MeshStandardMaterial({color:0x222222}));
        hBody.position.set(0, 20, -300); scene.add(hBody);

        renderer = new THREE.WebGLRenderer({antialias:true});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true; document.body.appendChild(renderer.domElement);

        document.body.addEventListener('click', () => { if(!inv) document.body.requestPointerLock(); });
        document.addEventListener('mousemove', (e) => {
            if (document.pointerLockElement === document.body) {
                camera.rotation.y -= e.movementX * 0.002;
                let nX = camera.rotation.x - e.movementY * 0.002;
                camera.rotation.x = Math.max(-Math.PI/2.5, Math.min(Math.PI/2.5, nX));
            }
        });

        window.onkeydown = (e) => { 
            if(e.code==='KeyW') mvF=true; if(e.code==='KeyS') mvB=true;
            if(e.code==='KeyA') mvL=true; if(e.code==='KeyD') mvR=true;
            if(e.code==='KeyE') { inv=!inv; document.getElementById('inventory').style.display=inv?'block':'none'; if(inv) document.exitPointerLock(); }
        };
        window.onkeyup = (e) => { 
            if(e.code==='KeyW') mvF=false; if(e.code==='KeyS') mvB=false;
            if(e.code==='KeyA') mvL=false; if(e.code==='KeyD') mvR=false;
        };
    }

    function animate() {
        requestAnimationFrame(animate);
        if(!inv && document.pointerLockElement === document.body) {
            let d = 0.04;
            dir.z = Number(mvF) - Number(mvB); dir.x = Number(mvR) - Number(mvL); dir.normalize();
            if(mvF || mvB) vel.z -= dir.z * 1.2 * d; if(mvL || mvR) vel.x -= dir.x * 1.2 * d;
            camera.translateX(-vel.x*d); camera.translateZ(vel.z*d);
            vel.x *= 0.85; vel.z *= 0.85;
            document.getElementById('dv').innerText = Math.round(camera.position.distanceTo(hosp));
        }
        renderer.render(scene, camera);
    }
</script>
</body>
</html>
"""

# --- NEON ARCADE ---
arcade_sayfa_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"><title>Uçan Kare</title></head>
<body style="background:#000; color:#00d4ff; text-align:center; font-family:sans-serif; margin:0;">
    <nav style="padding:20px; background:#111;"><a href="/" style="color:#fff; text-decoration:none;">⬅ Kütüphaneye Dön</a></nav>
    <canvas id="gc" width="400" height="400" style="border:3px solid #00d4ff; margin-top:20px;"></canvas>
    {footer_html}
    <script>
        const canvas = document.getElementById("gc"); const ctx = canvas.getContext("2d");
        let b = {{y:200, v:0}}, p = [], f = 0;
        function draw() {{
            ctx.fillStyle="#000"; ctx.fillRect(0,0,400,400);
            b.v += 0.6; b.y += b.v;
            ctx.fillStyle="#00d4ff"; ctx.fillRect(50, b.y, 25, 25);
            if(f%90===0) p.push({{x:400, h:Math.random()*200+50}});
            for(let i=p.length-1; i>=0; i--) {{
                p[i].x -= 3; ctx.fillStyle="#333";
                ctx.fillRect(p[i].x, 0, 50, p[i].h);
                ctx.fillRect(p[i].x, p[i].h+130, 50, 400);
                if(50<p[i].x+50 && 75>p[i].x && (b.y<p[i].h || b.y+25>p[i].h+130)) location.reload();
                if(p[i].x < -50) p.splice(i,1);
            }
            f++; requestAnimationFrame(draw);
        }}
        window.onclick = () => b.v = -9; draw();
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return ana_sayfa_html

@app.route('/horror')
def horror(): return horror_sayfa_html

@app.route('/neon-arcade')
def arcade(): return arcade_sayfa_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
