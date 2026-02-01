from flask import Flask
import os

app = Flask(__name__)

# --- ANA SAYFA ---
def get_ana_sayfa():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cano Game Studio</title>
        <style>
            body { background: #0a0a0a; color: white; font-family: sans-serif; margin: 0; text-align: center; }
            .container { display: flex; flex-direction: column; gap: 20px; padding: 20px; align-items: center; justify-content: center; height: 100vh; }
            .card { border: 2px solid #222; padding: 30px; border-radius: 15px; cursor: pointer; width: 80%; max-width: 300px; transition: 0.3s; }
            .card:hover { border-color: #00d4ff; }
            h1 { color: #00d4ff; letter-spacing: 2px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CANO STUDIO</h1>
            <div class="card" onclick="window.location.href='/horror'">
                <h2 style="color:#e74c3c">HORROR</h2>
                <p>3D Orman Gezisi</p>
            </div>
            <div class="card" onclick="window.location.href='/neon-arcade'">
                <h2 style="color:#00d4ff">ARCADE</h2>
                <p>Uçan Kare</p>
            </div>
        </div>
    </body>
    </html>
    """

# --- 3D HORROR (MOBİL JOYSTICK EKLENDİ) ---
horror_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Zihnin Karanlığı | Mobil</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; touch-action: none; }
        #ui-voice { position: fixed; top: 10%; width: 100%; text-align: center; color: rgba(255,255,255,0.5); font-family: monospace; font-size: 18px; pointer-events: none; z-index: 10; }
        
        /* MOBİL JOYSTICK STİLLERİ */
        #joystick-container { position: fixed; bottom: 50px; left: 50px; width: 120px; height: 120px; background: rgba(255,255,255,0.1); border-radius: 50%; z-index: 100; border: 1px solid rgba(255,255,255,0.2); }
        #joystick-knob { position: absolute; top: 35px; left: 35px; width: 50px; height: 50px; background: rgba(231, 76, 60, 0.5); border-radius: 50%; }
        
        #dist { position: fixed; bottom: 20px; right: 20px; color: #444; font-family: monospace; font-size: 14px; }
    </style>
</head>
<body>
<div id="ui-voice"></div>
<div id="joystick-container"><div id="joystick-knob"></div></div>
<div id="dist">Mesafe: <span id="dv">---</span>m</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    let scene, camera, renderer, flashLight;
    let moveDir = { x: 0, z: 0 };
    let hosp = new THREE.Vector3(0, 0, -300);

    init(); animate();

    function init() {
        scene = new THREE.Scene(); scene.background = new THREE.Color(0x010101);
        scene.fog = new THREE.FogExp2(0x010101, 0.05);
        camera = new THREE.PerspectiveCamera(70, window.innerWidth/window.innerHeight, 0.1, 1000);
        
        const amb = new THREE.AmbientLight(0x404040, 0.1); scene.add(amb);
        flashLight = new THREE.SpotLight(0xffffff, 3);
        flashLight.distance = 80; flashLight.angle = Math.PI/6;
        camera.add(flashLight); flashLight.position.set(0,0,0.1);
        let target = new THREE.Object3D(); target.position.set(0,0,-1);
        camera.add(target); flashLight.target = target; scene.add(camera);

        const floor = new THREE.Mesh(new THREE.PlaneGeometry(2000,2000), new THREE.MeshStandardMaterial({color:0x050505}));
        floor.rotation.x = -Math.PI/2; scene.add(floor);

        for(let i=0; i<400; i++) {
            let t = new THREE.Mesh(new THREE.CylinderGeometry(0.3,0.5,10,6), new THREE.MeshStandardMaterial({color:0x111111}));
            t.position.set(Math.random()*600-300, 5, Math.random()*600-300);
            if(t.position.distanceTo(hosp) > 40) scene.add(t);
        }

        const hBody = new THREE.Mesh(new THREE.BoxGeometry(60,40,80), new THREE.MeshStandardMaterial({color:0x222222}));
        hBody.position.set(0, 20, -300); scene.add(hBody);

        renderer = new THREE.WebGLRenderer({antialias:true});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // MOBİL KONTROLLER (DOKUNMATİK)
        const knob = document.getElementById('joystick-knob');
        const container = document.getElementById('joystick-container');
        
        container.addEventListener('touchmove', (e) => {
            const touch = e.touches[0];
            const rect = container.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            let dx = touch.clientX - centerX;
            let dy = touch.clientY - centerY;
            const dist = Math.min(Math.sqrt(dx*dx + dy*dy), 40);
            const angle = Math.atan2(dy, dx);
            
            knob.style.transform = `translate(${Math.cos(angle)*dist}px, ${Math.sin(angle)*dist}px)`;
            
            moveDir.x = Math.cos(angle) * (dist / 40);
            moveDir.z = Math.sin(angle) * (dist / 40);
        });

        container.addEventListener('touchend', () => {
            knob.style.transform = `translate(0, 0)`;
            moveDir.x = 0; moveDir.z = 0;
        });

        // Ekranda parmak kaydırarak bakış açısı değiştirme
        let lastTouchX = 0;
        document.addEventListener('touchstart', (e) => { if(e.touches[0].clientX > 150) lastTouchX = e.touches[0].clientX; });
        document.addEventListener('touchmove', (e) => {
            if(e.touches[0].clientX > 150) {
                let dx = e.touches[0].clientX - lastTouchX;
                camera.rotation.y -= dx * 0.005;
                lastTouchX = e.touches[0].clientX;
            }
        });
    }

    function animate() {
        requestAnimationFrame(animate);
        // Hareket uygula
        camera.translateX(moveDir.x * 0.5);
        camera.translateZ(moveDir.z * 0.5);
        
        document.getElementById('dv').innerText = Math.round(camera.position.distanceTo(hosp));
        renderer.render(scene, camera);
    }
</script>
</body>
</html>
"""

@app.route('/')
def home(): return get_ana_sayfa()

@app.route('/horror')
def horror(): return horror_sayfa_html

@app.route('/neon-arcade')
def arcade(): return "<h1>Arcade Yakında Telefondan Oynanacak!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
