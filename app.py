from flask import Flask
import os

app = Flask(__name__)

# --- ANA PORTAL ---
def get_portal():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cano Game Studio</title>
        <style>
            body { background: #080808; color: white; font-family: sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh; }
            .menu { display: flex; flex-direction: column; gap: 20px; width: 300px; }
            .btn { background: #111; border: 2px solid #222; padding: 20px; border-radius: 10px; cursor: pointer; text-align: center; text-decoration: none; color: white; font-weight: bold; transition: 0.3s; }
            .btn:hover { border-color: #5d6d7e; background: #1a1a1a; box-shadow: 0 0 15px rgba(255,255,255,0.1); }
        </style>
    </head>
    <body>
        <div class="menu">
            <h1 style="text-align:center; letter-spacing:3px;">CANO STUDIO</h1>
            <a href="/horror" class="btn" style="color:#aeb6bf">MOONLIGHT HORROR</a>
            <a href="/neon-arcade" class="btn" style="color:#00d4ff">ARCADE</a>
        </div>
    </body>
    </html>
    """

# --- MOONLIGHT HORROR ---
horror_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Zihnin Karanlığı | Ay Işığı</title>
    <style>
        body { margin: 0; overflow: hidden; background: #05070a; touch-action: none; }
        #crosshair { position: fixed; top: 50%; left: 50%; width: 4px; height: 4px; background: white; border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; opacity: 0.3; }
        #joy-bound { position: fixed; bottom: 40px; left: 40px; width: 100px; height: 100px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 50%; display: none; z-index: 100; }
        #joy-stick { position: absolute; top: 30px; left: 30px; width: 40px; height: 40px; background: rgba(255,255,255,0.3); border-radius: 50%; }
        #dist { position: fixed; bottom: 20px; right: 20px; color: #5d6d7e; font-family: monospace; font-weight: bold; }
    </style>
</head>
<body>
<div id="crosshair"></div>
<div id="joy-bound"><div id="joy-stick"></div></div>
<div id="dist">Binaya Mesafe: <span id="dv">---</span>m</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    let scene, camera, renderer, moonLight, flashLight;
    let keys = { w: false, s: false, a: false, d: false };
    let joyMove = { x: 0, z: 0 };
    let isMobile = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
    let hospPos = new THREE.Vector3(0, 0, -300);

    if(isMobile) document.getElementById('joy-bound').style.display = 'block';

    init(); animate();

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x05070a); // Gece mavisi gökyüzü
        scene.fog = new THREE.FogExp2(0x05070a, 0.02); // Sis azaltıldı, görüş açıldı

        camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1500);
        camera.rotation.order = 'YXZ';

        // --- AY IŞIĞI (DIRECTIONAL LIGHT) ---
        // TLOU tarzı mavi-beyaz soğuk ışık
        moonLight = new THREE.DirectionalLight(0x4a5a7a, 1.2); 
        moonLight.position.set(50, 100, 50);
        moonLight.castShadow = true;
        scene.add(moonLight);

        // Ortam ışığı (Tam karanlığı engellemek için)
        const amb = new THREE.AmbientLight(0x1a2a3a, 0.4); 
        scene.add(amb);

        // Fener (Hala var ama artık zorunlu değil)
        flashLight = new THREE.SpotLight(0xffffff, 1.5);
        flashLight.distance = 60; flashLight.angle = Math.PI/8;
        camera.add(flashLight); flashLight.position.set(0,0,0.1);
        let t = new THREE.Object3D(); t.position.set(0,0,-1); camera.add(t); flashLight.target = t;
        scene.add(camera);

        // Zemin
        const floor = new THREE.Mesh(
            new THREE.PlaneGeometry(2000,2000), 
            new THREE.MeshStandardMaterial({color: 0x0a1a0a, roughness: 0.8})
        );
        floor.rotation.x = -Math.PI/2;
        floor.receiveShadow = true;
        scene.add(floor);

        // Orman
        const treeGeo = new THREE.CylinderGeometry(0.3, 0.6, 12, 6);
        const treeMat = new THREE.MeshStandardMaterial({color: 0x0a0a0a});
        for(let i=0; i<500; i++) {
            let tr = new THREE.Mesh(treeGeo, treeMat);
            tr.position.set(Math.random()*800-400, 6, Math.random()*800-400);
            tr.castShadow = true;
            tr.receiveShadow = true;
            if(tr.position.distanceTo(hospPos) > 40) scene.add(tr);
        }

        // Hastane (Ay ışığında parlayan gri kütle)
        const hospital = new THREE.Mesh(
            new THREE.BoxGeometry(60,50,100), 
            new THREE.MeshStandardMaterial({color: 0x1a2a3a})
        );
        hospital.position.set(0, 25, -300);
        hospital.castShadow = true;
        hospital.receiveShadow = true;
        scene.add(hospital);

        renderer = new THREE.WebGLRenderer({antialias:true});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.body.appendChild(renderer.domElement);

        // Kontrolcü Kayıtları
        window.addEventListener('keydown', (e) => {
            const key = e.key.toLowerCase();
            if(key === 'w') keys.w = true; if(key === 's') keys.s = true;
            if(key === 'a') keys.a = true; if(key === 'd') keys.d = true;
        });
        window.addEventListener('keyup', (e) => {
            const key = e.key.toLowerCase();
            if(key === 'w') keys.w = false; if(key === 's') keys.s = false;
            if(key === 'a') keys.a = false; if(key === 'd') keys.d = false;
        });

        document.addEventListener('mousedown', () => { if(!isMobile) document.body.requestPointerLock(); });
        document.addEventListener('mousemove', (e) => {
            if(document.pointerLockElement === document.body) {
                camera.rotation.y -= e.movementX * 0.002;
                camera.rotation.x = Math.max(-1.5, Math.min(1.5, camera.rotation.x - e.movementY * 0.002));
            }
        });

        if(isMobile) {
            const bound = document.getElementById('joy-bound');
            const stick = document.getElementById('joy-stick');
            bound.addEventListener('touchmove', (e) => {
                let t = e.touches[0]; let r = bound.getBoundingClientRect();
                let dx = t.clientX - (r.left + 50); let dy = t.clientY - (r.top + 50);
                let d = Math.min(Math.sqrt(dx*dx+dy*dy), 35); let a = Math.atan2(dy, dx);
                stick.style.transform = `translate(${Math.cos(a)*d}px, ${Math.sin(a)*d}px)`;
                joyMove.x = Math.cos(a) * (d/35); joyMove.z = Math.sin(a) * (d/35);
            });
            bound.addEventListener('touchend', () => {
                stick.style.transform = 'translate(0,0)'; joyMove.x = 0; joyMove.z = 0;
            });
            let lx = 0;
            window.addEventListener('touchmove', (e) => {
                if(e.touches[0].clientX > 150) {
                    let dx = e.touches[0].clientX - lx;
                    camera.rotation.y -= dx * 0.006;
                    lx = e.touches[0].clientX;
                }
            }, {passive: false});
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        let speed = 0.45;
        if(keys.w) camera.translateZ(-speed); if(keys.s) camera.translateZ(speed);
        if(keys.a) camera.translateX(-speed); if(keys.d) camera.translateX(speed);
        if(isMobile) { camera.translateZ(joyMove.z * speed); camera.translateX(joyMove.x * speed); }
        document.getElementById('dv').innerText = Math.round(camera.position.distanceTo(hospPos));
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
def arcade(): return "<h1>Arcade Yakında...</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
