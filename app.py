from flask import Flask
import os

app = Flask(__name__)

horror_sayfa_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Zihnin Karanlığı | Orman</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        #ui-overlay { position: fixed; top: 10%; width: 100%; text-align: center; color: rgba(255,255,255,0.6); font-family: 'Courier New', monospace; font-style: italic; font-size: 22px; z-index: 100; pointer-events: none; text-shadow: 0 0 10px red; transition: 1s; opacity: 0; }
        #crosshair { position: fixed; top: 50%; left: 50%; width: 2px; height: 2px; background: white; transform: translate(-50%, -50%); z-index: 100; opacity: 0.3; }
        #inventory { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; background: rgba(0,0,0,0.9); border: 1px solid #e74c3c; padding: 20px; display: none; color: white; z-index: 200; }
        #instructions { position: fixed; bottom: 20px; left: 20px; color: #444; font-family: sans-serif; font-size: 12px; }
    </style>
</head>
<body>

<div id="ui-overlay">Biri mi var orada?</div>
<div id="crosshair"></div>
<div id="inventory">
    <h3 style="color:#e74c3c">ENVANTER (E)</h3>
    <p>🔦 Fener (Açık)</p>
    <p>🔪 Çakı</p>
    <p>📱 Telefon (Şarj %4)</p>
</div>
<div id="instructions">WASD: Ağır Hareket | E: Envanter | Tıkla: Odaklan</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
    let scene, camera, renderer, flashLight, inventoryOpen = false;
    let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
    let velocity = new THREE.Vector3();
    let direction = new THREE.Vector3();
    
    const thoughts = [
        "Neden buradayım?",
        "Bu ağaçlar... sanki yer değiştiriyorlar.",
        "İlacım nerede? Onu bulmalıyım.",
        "Sesler... kesilmiyor.",
        "Doktor nerede? Bana bunu o yaptı.",
        "Sakin ol... sadece bir halüsinasyon."
    ];

    init();
    animate();

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x010101);
        scene.fog = new THREE.FogExp2(0x010101, 0.08); // Daha geniş ama puslu görüş

        camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 1000);
        
        const ambientLight = new THREE.AmbientLight(0x404040, 0.1); 
        scene.add(ambientLight);

        flashLight = new THREE.SpotLight(0xffffff, 2.5);
        flashLight.distance = 50;
        flashLight.angle = Math.PI / 5;
        flashLight.penumbra = 0.6;
        flashLight.decay = 1.5;
        flashLight.castShadow = true;
        
        camera.add(flashLight);
        flashLight.position.set(0, 0, 1);
        flashLight.target = camera; 
        scene.add(camera);

        // Zemin (Toprak/Çimen dokusu rengi)
        const floorGeo = new THREE.PlaneGeometry(2000, 2000);
        const floorMat = new THREE.MeshStandardMaterial({ color: 0x020502 });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);

        // 500 Ağaçlık Dev Orman
        const treeTrunkGeo = new THREE.CylinderGeometry(0.2, 0.4, 8, 8);
        const treeTrunkMat = new THREE.MeshStandardMaterial({ color: 0x1a1a1a });
        const treeTopGeo = new THREE.ConeGeometry(2, 5, 8);
        const treeTopMat = new THREE.MeshStandardMaterial({ color: 0x050a05 });

        for(let i = 0; i < 500; i++) {
            const group = new THREE.Group();
            
            const trunk = new THREE.Mesh(treeTrunkGeo, treeTrunkMat);
            trunk.position.y = 4;
            trunk.castShadow = true;
            group.add(trunk);

            const top = new THREE.Mesh(treeTopGeo, treeTopMat);
            top.position.y = 8;
            top.castShadow = true;
            group.add(top);

            group.position.x = Math.random() * 400 - 200;
            group.position.z = Math.random() * 400 - 200;
            scene.add(group);
        }

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);

        document.body.addEventListener('click', () => {
            if(!inventoryOpen) document.body.requestPointerLock();
        });

        document.addEventListener('mousemove', (e) => {
            if (document.pointerLockElement === document.body) {
                camera.rotation.y -= e.movementX * 0.0015;
                camera.rotation.x -= e.movementY * 0.0015;
            }
        });

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

        // Rastgele Şizofreni Düşünceleri
        setInterval(() => {
            if(!inventoryOpen) {
                const voice = document.getElementById('ui-overlay');
                voice.innerText = thoughts[Math.floor(Math.random() * thoughts.length)];
                voice.style.opacity = 1;
                setTimeout(() => { voice.style.opacity = 0; }, 3000);
            }
        }, 8000);
    }

    function toggleInventory() {
        inventoryOpen = !inventoryOpen;
        document.getElementById('inventory').style.display = inventoryOpen ? 'block' : 'none';
        if(inventoryOpen) document.exitPointerLock();
    }

    function animate() {
        requestAnimationFrame(animate);
        
        if (!inventoryOpen && document.pointerLockElement === document.body) {
            const delta = 0.05; // HAREKET YAVAŞLATILDI (Yarısı kadar yavaş)
            direction.z = Number(moveForward) - Number(moveBackward);
            direction.x = Number(moveRight) - Number(moveLeft);
            direction.normalize();

            if (moveForward || moveBackward) velocity.z -= direction.z * 1.5 * delta;
            if (moveLeft || moveRight) velocity.x -= direction.x * 1.5 * delta;

            camera.translateX(-velocity.x * delta);
            camera.translateZ(velocity.z * delta);
            
            velocity.x *= 0.85; // Sürtünme artırıldı (daha hantal duruş)
            velocity.z *= 0.85;
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
def home(): return horror_sayfa_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
