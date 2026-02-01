from flask import Flask
import os

app = Flask(__name__)

# --- ANA SAYFA (MOBİL & PC UYUMLU PANEL) ---
def get_portal():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cano Game Studio</title>
        <style>
            body { background: #080808; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; align-items: center; justify-content: center; }
            .menu { width: 90%; max-width: 400px; display: flex; flex-direction: column; gap: 15px; }
            .btn { background: #111; border: 2px solid #222; padding: 25px; border-radius: 15px; cursor: pointer; text-align: center; transition: 0.3s; text-decoration: none; color: white; }
            .btn:hover { border-color: #e74c3c; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(231,76,60,0.2); }
            h1 { font-size: 2.5rem; letter-spacing: 5px; color: #eee; margin-bottom: 30px; text-shadow: 0 0 10px rgba(255,255,255,0.1); }
            .tag { font-size: 0.8rem; color: #666; margin-top: 10px; display: block; }
        </style>
    </head>
    <body>
        <h1>CANO STUDIO</h1>
        <div class="menu">
            <a href="/horror" class="btn">
                <strong style="color:#e74c3c; font-size: 1.5rem;">HORROR</strong><br>
                <span class="tag">PC: WASD + MOUSE | MOBİL: JOYSTICK</span>
            </a>
            <a href="/neon-arcade" class="btn">
                <strong style="color:#00d4ff; font-size: 1.5rem;">ARCADE</strong><br>
                <span class="tag">KLASİK UÇAN KARE</span>
            </a>
        </div>
    </body>
    </html>
    """

# --- HİBRİT HORROR OYUNU ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Zihnin Karanlığı | Cross-Platform</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; touch-action: none; font-family: monospace; }
        #crosshair { position: fixed; top: 50%; left: 50%; width: 4px; height: 4px; background: white; border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; opacity: 0.5; }
        
        /* MOBİL JOYSTICK - VARSAYILAN OLARAK GİZLİ */
        #joy-bound { position: fixed; bottom: 40px; left: 40px; width: 100px; height: 100px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 50%; display: none; z-index: 100; }
        #joy-stick { position: absolute; top: 30px; left: 30px; width: 40px; height: 40px; background: #e74c3c; border-radius: 50%; opacity: 0.6; }
        
        #ui { position: fixed; top: 20px; width: 100%; text-align: center; color: rgba(255,255,255,0.4); pointer-events: none; }
        #dist { position: fixed; bottom: 20px; right: 20px; color: #444; }
    </style>
</head>
<body>
<div id="crosshair"></div>
<div id="joy-bound"><div id="joy-stick"></div></div>
<div id="ui">Ağaçların arasından o binayı bul...</div>
<div id="dist"><span id="dv">---</span>m</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    let scene, camera, renderer, flashLight;
    let mv = { f: 0, b: 0, l: 0, r: 0 }; // PC Kontrol
    let joyMove = { x: 0, z: 0 }; // Mobil Kontrol
    let isMobile = ('ontouchstart' in window);
    let hosp = new THREE.Vector3(0, 0, -300);

    if(isMobile) document.getElementById('joy-bound').style.display = 'block';

    init(); animate();

    function init() {
        scene = new THREE.Scene(); scene.background = new THREE.Color(0x010101);
        scene.fog = new THREE.FogExp2(0x010101, 0.06);
        camera = new THREE.PerspectiveCamera(70, window.innerWidth/window.innerHeight, 0.1, 1000);
        camera.rotation.order = 'YXZ';

        const amb = new THREE.AmbientLight(0xffffff, 0.02); scene.add(amb);
        flashLight = new THREE.SpotLight(0xffffff, 3);
        flashLight.distance = 70; flashLight.angle = Math.PI/7; flashLight.castShadow = true;
        camera.add(flashLight); flashLight.position.set(0,0,0.1);
        let t = new THREE.Object3D(); t.position.set(0,0,-1); camera.add(t); flashLight.target = t;
        scene.add(camera);

        const floor = new THREE.Mesh(new THREE.PlaneGeometry(1000,1000), new THREE.MeshStandardMaterial({color:0x050505}));
        floor.rotation.x = -Math.PI/2; scene.add(floor);

        // Orman ve Hastane
        for(let i=0; i<450; i++) {
            let tr = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.4, 10, 6), new THREE.MeshStandardMaterial({color:0x111111}));
            tr.position.set(Math.random()*500-250, 5, Math.random()*500-250);
            if(tr.position.distanceTo(hosp) > 35) scene.add(tr);
        }
        const b = new THREE.Mesh(new THREE.BoxGeometry(50,40,70), new THREE.MeshStandardMaterial({color:0x1a1a1a}));
        b.position.copy(hosp); b.position.y = 20; scene.add(b);

        renderer = new THREE.WebGLRenderer({antialias:true});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true; document.body.appendChild(renderer.domElement);

        // PC KONTROLLER
        if(!isMobile) {
            window.addEventListener('mousedown', () => document.body.requestPointerLock());
            window.addEventListener('mousemove', (e) => {
                if(document.pointerLockElement === document.body) {
                    camera.rotation.y -= e.movementX * 0.002;
                    camera.rotation.x = Math.max(-1.5, Math.min(1.5, camera.rotation.x - e.movementY * 0.002));
                }
            });
            window.onkeydown = (e) => {
                let k = e.code;
                if(k==='KeyW') mv.f=1; if(k==='KeyS') mv.b=1;
                if(k==='KeyA') mv.l=1; if(k==='KeyD') mv.r=1;
            };
            window.onkeyup = (e) => {
                let k = e.code;
                if(k==='KeyW') mv.f=0; if(k==='KeyS') mv.b=0;
                if(k==='KeyA') mv.l=0; if(k==='KeyD') mv.r=0;
            };
        } else {
            // MOBİL KONTROLLER
            const bound = document.getElementById('joy-bound');
            const stick = document.getElementById('joy-stick');
            bound.addEventListener('touchmove', (e) => {
                let t = e.touches[0];
                let r = bound.getBoundingClientRect();
                let dx = t.clientX - (r.left + 50);
                let dy = t.clientY - (r.top + 50);
                let d = Math.min(Math.sqrt(dx*dx+dy*dy), 35);
                let a = Math.atan2(dy, dx);
                stick.style.transform = `translate(${Math.cos(a)*d}px, ${Math.sin(a)*d}px)`;
                joyMove.x = Math.cos(a) * (d/35); joyMove.z = Math.sin(a) * (d/35);
            });
            bound.addEventListener('touchend', () => {
                stick.style.transform = 'translate(0,0)'; joyMove.x = 0; joyMove.z = 0;
            });
            let lx = 0;
            window.addEventListener('touchstart', (e) => { if(e.touches[0].clientX > 150) lx = e.touches[0].clientX; });
            window.addEventListener('touchmove', (e) => {
                if(e.touches[0].clientX > 150) {
                    let dx = e.touches[0].clientX - lx;
                    camera.rotation.y -= dx * 0.006;
                    lx = e.touches[0].clientX;
                }
            });
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        let s = 0.3; // Yavaş, temkinli hız
        if(!isMobile) {
            let f = (mv.f - mv.b); let r = (mv.r - mv.l);
            camera.translateZ(-f * s); camera.translateX(r * s);
        } else {
            camera.translateZ(joyMove.z * s); camera.translateX(joyMove.x * s);
        }
        document.getElementById('dv').innerText = Math.round(camera.position.distanceTo(hosp));
        renderer.render(scene, camera);
    }
</script>
</body>
</html>
"""

@app.route('/')
def home(): return get_portal()

@app.route('/horror')
def horror(): return horror_html

@app.route('/neon-arcade')
def arcade(): return "<h1>Arcade Modu Yakında Güncellenecek</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
