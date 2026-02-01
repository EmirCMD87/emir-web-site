from flask import Flask
import os

app = Flask(__name__)

horror_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Zihnin Karanlığı | High-Gen Horror</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        #ui-overlay { position: fixed; bottom: 20px; left: 20px; color: white; font-family: sans-serif; z-index: 100; pointer-events: none; }
        #crosshair { position: fixed; top: 50%; left: 50%; width: 4px; height: 4px; background: white; border-radius: 50%; transform: translate(-50%, -50%); z-index: 100; opacity: 0.5; }
        #inventory { 
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            width: 300px; background: rgba(0,0,0,0.9); border: 1px solid #e74c3c; 
            padding: 20px; display: none; color: white; z-index: 200;
        }
    </style>
</head>
<body>

<div id="ui-overlay">
    <div>WASD: Hareket | E: Envanter | Mouse: Etrafa Bak</div>
    <div id="status">Durum: Ormanda Kayboldu...</div>
</div>
<div id="crosshair"></div>
<div id="inventory">
    <h3 style="color:#e74c3c">ENVANTER</h3>
    <p>🔦 Fener (Açık)</p>
    <p>🔪 Çakı</p>
    <p>📱 Telefon (Şarj %4)</p>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
    let scene, camera, renderer, flashLight, inventoryOpen = false;
    let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
    let velocity = new THREE.Vector3();
    let direction = new THREE.Vector3();

    init();
    animate();

    function init() {
        // 1. Sahne ve Kamera (Outlast Tarzı FPS)
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020202);
        scene.fog = new THREE.FogExp2(0x020202, 0.15); // Sisli orman havası

        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        
        // 2. Işıklandırma (Fener Efekti)
        const ambientLight = new THREE.AmbientLight(0x404040, 0.2); // Çok hafif ortam ışığı
        scene.add(ambientLight);

        flashLight = new THREE.SpotLight(0xffffff, 2);
        flashLight.distance = 40;
        flashLight.angle = Math.PI / 6;
        flashLight.penumbra = 0.5;
        flashLight.decay = 2;
        flashLight.castShadow = true;
        
        camera.add(flashLight);
        flashLight.position.set(0, 0, 1);
        flashLight.target = camera; // Fener kameranın baktığı yere baksın
        scene.add(camera);

        // 3. Yer ve Orman (Zemin)
        const floorGeo = new THREE.PlaneGeometry(1000, 1000);
        const floorMat = new THREE.MeshStandardMaterial({ color: 0x050505 });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);

        // 4. Rastgele Ağaçlar (Performanslı Model)
        for(let i = 0; i < 200; i++) {
            const treeHeight = Math.random() * 5 + 5;
            const treeGeo = new THREE.CylinderGeometry(0.2, 0.5, treeHeight, 8);
            const treeMat = new THREE.MeshStandardMaterial({ color: 0x1a0f00 });
            const tree = new THREE.Mesh(treeGeo, treeMat);
            
            tree.position.x = Math.random() * 200 - 100;
            tree.position.z = Math.random() * 200 - 100;
            tree.position.y = treeHeight / 2;
            tree.castShadow = true;
            scene.add(tree);
        }

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);

        // Mouse Kilitleme (FPS Kontrolü için)
        document.body.addEventListener('click', () => {
            if(!inventoryOpen) document.body.requestPointerLock();
        });

        document.addEventListener('mousemove', (e) => {
            if (document.pointerLockElement === document.body) {
                camera.rotation.y -= e.movementX * 0.002;
                camera.rotation.x -= e.movementY * 0.002;
            }
        });

        // Klavye Kontrolleri
        const onKeyDown = (e) => {
            switch (e.code) {
                case 'KeyW': moveForward = true; break;
                case 'KeyS': moveBackward = true; break;
                case 'KeyA': moveLeft = true; break;
                case 'KeyD': moveRight = true; break;
                case 'KeyE': toggleInventory(); break;
            }
        };
        const onKeyUp = (e) => {
            switch (e.code) {
                case 'KeyW': moveForward = false; break;
                case 'KeyS': moveBackward = false; break;
                case 'KeyA': moveLeft = false; break;
                case 'KeyD': moveRight = false; break;
            }
        };
        document.addEventListener('keydown', onKeyDown);
        document.addEventListener('keyup', onKeyUp);
    }

    function toggleInventory() {
        inventoryOpen = !inventoryOpen;
        document.getElementById('inventory').style.display = inventoryOpen ? 'block' : 'none';
        if(inventoryOpen) document.exitPointerLock();
    }

    function animate() {
        requestAnimationFrame(animate);
        
        if (!inventoryOpen && document.pointerLockElement === document.body) {
            const delta = 0.1;
            direction.z = Number(moveForward) - Number(moveBackward);
            direction.x = Number(moveRight) - Number(moveLeft);
            direction.normalize();

            if (moveForward || moveBackward) velocity.z -= direction.z * 4.0 * delta;
            if (moveLeft || moveRight) velocity.x -= direction.x * 4.0 * delta;

            camera.translateX(-velocity.x * delta);
            camera.translateZ(velocity.z * delta);
            
            velocity.x *= 0.9;
            velocity.z *= 0.9;
        }

        renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
</script>
</body>
</html>
"""

@app.route('/')
def home(): return horror_sayfa_html # Test için direkt korku açılıyor

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
