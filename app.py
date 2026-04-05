from flask import Flask, request
import os
import json
import threading
from datetime import datetime, date, timedelta

app = Flask(__name__)

ADMIN_PASSWORD = "emir2011"
_lock = threading.Lock()

# ===== BELLEK TABANLI VERİ =====
_db = {
    "total": 0, "daily": {}, "monthly": {}, "pages": {},
    "yorumlar": [], "xp_scores": [],
    "anons": {"text": "", "active": False, "maintenance": False}
}

def get_db():
    return _db

def save_db(d):
    pass  # Bellekte tutuluyor

def track(page_name):
    with _lock:
        today = str(date.today()); month = today[:7]
        _db["total"] += 1
        _db["daily"][today] = _db["daily"].get(today, 0) + 1
        _db["monthly"][month] = _db["monthly"].get(month, 0) + 1
        _db["pages"][page_name] = _db["pages"].get(page_name, 0) + 1

def load_stats():
    return {"total": _db["total"], "daily": _db["daily"], "monthly": _db["monthly"], "pages": _db["pages"]}

def load_yorumlar():
    return _db["yorumlar"]

def save_yorumlar(y):
    _db["yorumlar"] = y

def load_anons():
    return _db["anons"]

def save_anons(a):
    _db["anons"] = a

def load_xp():
    return _db["xp_scores"]

def save_xp(x):
    _db["xp_scores"] = x

def update_xp(name, xp):
    with _lock:
        scores = _db["xp_scores"]
        found = False
        for s in scores:
            if s["name"] == name:
                if xp > s["xp"]: s["xp"] = xp
                found = True; break
        if not found:
            scores.append({"name": name, "xp": xp})
        scores.sort(key=lambda x: -x["xp"])
        _db["xp_scores"] = scores[:50]

# ============ YARDIMCI FONKSİYON ============
def page(title, extra_css, body_html, extra_js, color="var(--neon-orange)"):
    """Tüm sayfalar bu fonksiyonla üretiliyor — tek CSS/JS kaynağı"""
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title} | Cano Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
<style>
:root {{
  --neon-orange:#ff4500; --neon-blue:#00d4ff;
  --neon-purple:#bf00ff; --neon-green:#00ff88;
  --dark-bg:#050505;
}}
*{{margin:0;padding:0;box-sizing:border-box;touch-action:manipulation;-webkit-tap-highlight-color:transparent;}}
body{{background:var(--dark-bg);color:#fff;font-family:'Rajdhani',sans-serif;overflow-x:hidden;min-height:100vh;}}
#particles{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:-1;}}
.xp-container{{position:fixed;top:20px;right:20px;background:rgba(255,69,0,0.15);border:1px solid var(--neon-orange);padding:10px 20px;border-radius:50px;z-index:1000;backdrop-filter:blur(10px);display:flex;align-items:center;gap:8px;}}
.xp-val{{color:var(--neon-orange);font-weight:900;font-size:1.1rem;font-family:'Orbitron';}}
.xp-label{{color:#aaa;font-size:0.8rem;}}
.level-badge{{position:fixed;top:20px;left:20px;background:rgba(0,212,255,0.15);border:1px solid var(--neon-blue);padding:10px 20px;border-radius:50px;z-index:1000;backdrop-filter:blur(10px);font-family:'Orbitron';font-size:0.85rem;color:var(--neon-blue);}}
.btn{{background:linear-gradient(135deg,var(--neon-orange),#ff6b35);color:#fff;border:none;padding:12px 28px;font-family:'Orbitron';font-size:0.85rem;cursor:pointer;border-radius:8px;transition:all 0.3s;letter-spacing:1px;}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 8px 25px rgba(255,69,0,0.5);}}
.btn:active{{transform:scale(0.97);}}
.btn:disabled{{opacity:0.4;cursor:not-allowed;transform:none;}}
.btn-blue{{background:linear-gradient(135deg,var(--neon-blue),#0099cc);}}
.btn-blue:hover{{box-shadow:0 8px 25px rgba(0,212,255,0.5);}}
.btn-purple{{background:linear-gradient(135deg,var(--neon-purple),#8800cc);}}
.back-btn{{position:fixed;bottom:30px;left:30px;color:#666;text-decoration:none;font-family:'Orbitron';font-size:0.8rem;z-index:100;transition:color 0.3s;padding:10px 20px;border:1px solid #333;border-radius:50px;}}
.back-btn:hover{{color:var(--neon-orange);border-color:var(--neon-orange);}}
.toast{{position:fixed;bottom:80px;right:20px;background:rgba(0,255,136,0.15);border:1px solid var(--neon-green);color:var(--neon-green);padding:12px 20px;border-radius:10px;font-family:'Orbitron';font-size:0.75rem;z-index:9999;opacity:0;transition:opacity 0.3s;pointer-events:none;}}
.toast.show{{opacity:1;}}
@keyframes xpPop{{0%{{transform:scale(1);}}50%{{transform:scale(1.3);}}100%{{transform:scale(1);}}}}
.xp-anim{{animation:xpPop 0.4s ease;}}
/* Muzik Player */
#mp{{position:fixed;bottom:20px;right:20px;background:rgba(5,5,5,0.95);border:1px solid var(--neon-purple);border-radius:16px;padding:12px;z-index:2000;backdrop-filter:blur(20px);width:260px;box-shadow:0 0 30px rgba(191,0,255,0.3);transition:all 0.3s;}}
#mp.mini{{width:46px;height:46px;padding:0;border-radius:50%;overflow:hidden;cursor:pointer;}}
#mp.mini #mpContent{{display:none;}}
#mp.mini #mpToggle{{width:46px;height:46px;border-radius:50%;}}
#mpToggle{{width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,var(--neon-purple),#5500aa);border:none;color:#fff;font-size:1.1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;}}
#mpContent{{margin-top:8px;}}
.mp-title{{font-family:'Orbitron';font-size:0.62rem;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.mp-artist{{font-size:0.58rem;color:#555;margin-bottom:8px;}}
.mp-ctrl{{display:flex;align-items:center;gap:6px;margin-bottom:8px;}}
.mp-btn{{background:none;border:1px solid rgba(255,255,255,0.1);color:#fff;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:0.75rem;display:flex;align-items:center;justify-content:center;transition:all 0.2s;}}
.mp-btn:hover{{border-color:var(--neon-purple);background:rgba(191,0,255,0.2);}}
.mp-play{{width:34px;height:34px;background:linear-gradient(135deg,var(--neon-purple),#5500aa);border:none;}}
.mp-prog{{height:4px;background:#222;border-radius:50px;cursor:pointer;margin-bottom:6px;}}
.mp-fill{{height:100%;border-radius:50px;background:linear-gradient(90deg,var(--neon-purple),var(--neon-blue));pointer-events:none;}}
.mp-vol{{display:flex;align-items:center;gap:4px;}}
.mp-vol input{{flex:1;height:3px;accent-color:var(--neon-purple);cursor:pointer;}}
.mp-vol span{{font-size:0.6rem;color:#444;}}
.mp-pl-btn{{background:none;border:none;color:#444;font-size:0.58rem;font-family:'Orbitron';cursor:pointer;margin-top:6px;width:100%;text-align:center;}}
.mp-pl-btn:hover{{color:var(--neon-purple);}}
.mp-pl{{display:none;margin-top:6px;border-top:1px solid rgba(255,255,255,0.05);padding-top:6px;max-height:130px;overflow-y:auto;}}
.mp-pl.open{{display:block;}}
.mp-item{{padding:5px 6px;border-radius:6px;cursor:pointer;font-size:0.62rem;color:#666;display:flex;justify-content:space-between;align-items:center;}}
.mp-item:hover{{background:rgba(191,0,255,0.1);color:#fff;}}
.mp-item.active{{color:var(--neon-purple);}}
.mp-tag{{font-size:0.52rem;background:rgba(191,0,255,0.2);padding:2px 5px;border-radius:50px;color:var(--neon-purple);}}
{extra_css}
</style>
</head>
<body>
<canvas id="particles"></canvas>
<div class="xp-container"><span class="xp-val" id="xpVal">0</span><span class="xp-label">XP</span></div>
<div class="level-badge" id="levelBadge">SEV 1</div>
<div id="toast" class="toast"></div>

{body_html}

<!-- MUZIK PLAYER -->
<div id="mp" class="mini">
  <button id="mpToggle" onclick="mpToggle()">&#127925;</button>
  <div id="mpContent">
    <div class="mp-title" id="mpTitle">Yukleniyor...</div>
    <div class="mp-artist" id="mpArtist">-</div>
    <div class="mp-ctrl">
      <button class="mp-btn" onclick="mpPrev()">&#9198;</button>
      <button class="mp-btn mp-play" onclick="mpPlay()" id="mpPlayBtn">&#9654;</button>
      <button class="mp-btn" onclick="mpNext()">&#9197;</button>
    </div>
    <div class="mp-prog" id="mpProg" onclick="mpSeek(event)">
      <div class="mp-fill" id="mpFill" style="width:0%"></div>
    </div>
    <div class="mp-vol">
      <span>&#128264;</span>
      <input type="range" min="0" max="100" value="50" oninput="mpVol(this.value)">
      <span>&#128266;</span>
    </div>
    <button class="mp-pl-btn" onclick="mpTogglePl()">&#9660; PLAYLİST</button>
    <div class="mp-pl" id="mpPl"></div>
  </div>
</div>

<script>
// ===== ORTAK JS =====
function getXP(){{return parseInt(localStorage.getItem('cano_xp'))||0;}}
function setXP(v){{localStorage.setItem('cano_xp',v);updateXPDisplay();}}
function addXP(amt,lbl){{
  var x=getXP()+amt; setXP(x);
  showToast('+'+amt+' XP'+(lbl?' - '+lbl:''));
  var el=document.getElementById('xpVal');
  if(el){{el.classList.remove('xp-anim');void el.offsetWidth;el.classList.add('xp-anim');}}
}}
function updateXPDisplay(){{
  var x=getXP();
  var el=document.getElementById('xpVal');
  if(el) el.innerText=x.toLocaleString();
  var lv=document.getElementById('levelBadge');
  if(lv) lv.innerText='SEV '+Math.floor(x/500+1);
}}
function showToast(msg){{
  var t=document.getElementById('toast');
  if(!t) return;
  t.innerText=msg; t.classList.add('show');
  setTimeout(function(){{t.classList.remove('show');}},2500);
}}
function getItems(){{return JSON.parse(localStorage.getItem('cano_items'))||[];}}

// ===== PARÇACIKLAR =====
(function(){{
  var pc=document.getElementById('particles');
  if(!pc) return;
  var cx=pc.getContext('2d');
  pc.width=window.innerWidth; pc.height=window.innerHeight;
  window.addEventListener('resize',function(){{pc.width=window.innerWidth;pc.height=window.innerHeight;}});
  var pts=[];
  for(var i=0;i<60;i++) pts.push({{
    x:Math.random()*pc.width,y:Math.random()*pc.height,
    vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.5,
    r:Math.random()*2+0.5,
    c:['#ff4500','#00d4ff','#bf00ff'][Math.floor(Math.random()*3)]
  }});
  function draw(){{
    cx.clearRect(0,0,pc.width,pc.height);
    pts.forEach(function(p){{
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>pc.width) p.vx*=-1;
      if(p.y<0||p.y>pc.height) p.vy*=-1;
      cx.beginPath(); cx.arc(p.x,p.y,p.r,0,Math.PI*2);
      cx.fillStyle=p.c; cx.fill();
    }});
    requestAnimationFrame(draw);
  }}
  draw();
}})();

// ===== MÜZİK PLAYER =====
var TRACKS=[
  {{t:'Neon Drive',     a:'Synthwave Free', g:'Synthwave', s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'}},
  {{t:'Cyber City',     a:'Cyberpunk Beats',g:'Cyberpunk',  s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'}},
  {{t:'Epic Quest',     a:'Orchestral Free',g:'Epic',       s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'}},
  {{t:'Midnight Lofi',  a:'Lofi Chill',     g:'Lofi',       s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'}},
  {{t:'Steel Storm',    a:'Metal Zone',     g:'Metal',      s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'}},
  {{t:'Digital Horizon',a:'Synthwave Free', g:'Synthwave',  s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3'}},
  {{t:'Battle Theme',   a:'Orchestral Free',g:'Epic',       s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3'}},
  {{t:'Rainy Night',    a:'Lofi Chill',     g:'Lofi',       s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3'}},
  {{t:'Iron Fist',      a:'Metal Zone',     g:'Metal',      s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3'}},
  {{t:'Ghost Protocol', a:'Cyberpunk Beats',g:'Cyberpunk',  s:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3'}},
];
var mpAud=new Audio(), mpIdx=0, mpIsPlaying=false, mpPlOpen=false;
function mpLoad(i){{
  mpIdx=i; var tr=TRACKS[i];
  mpAud.src=tr.s;
  var ti=document.getElementById('mpTitle');
  var ar=document.getElementById('mpArtist');
  if(ti) ti.innerText=tr.t;
  if(ar) ar.innerText=tr.a+' · '+tr.g;
  if(mpIsPlaying) mpAud.play();
  mpRenderPl();
}}
function mpPlay(){{
  if(mpIsPlaying){{mpAud.pause();mpIsPlaying=false;document.getElementById('mpPlayBtn').innerHTML='&#9654;';}}
  else{{mpAud.play();mpIsPlaying=true;document.getElementById('mpPlayBtn').innerHTML='&#9646;&#9646;';}}
}}
function mpPrev(){{mpLoad((mpIdx-1+TRACKS.length)%TRACKS.length);}}
function mpNext(){{mpLoad((mpIdx+1)%TRACKS.length);}}
function mpSeek(e){{
  var b=document.getElementById('mpProg');
  var r=b.getBoundingClientRect();
  mpAud.currentTime=((e.clientX-r.left)/r.width)*mpAud.duration;
}}
function mpVol(v){{mpAud.volume=v/100;}}
function mpToggle(){{
  var p=document.getElementById('mp');
  if(p) p.classList.toggle('mini');
}}
function mpTogglePl(){{
  mpPlOpen=!mpPlOpen;
  var d=document.getElementById('mpPl');
  if(d) d.className='mp-pl'+(mpPlOpen?' open':'');
}}
function mpRenderPl(){{
  var d=document.getElementById('mpPl'); if(!d) return;
  d.innerHTML='';
  TRACKS.forEach(function(tr,i){{
    var div=document.createElement('div');
    div.className='mp-item'+(i===mpIdx?' active':'');
    div.innerHTML=(i===mpIdx?'&#9834; ':'')+tr.t+'<span class="mp-tag">'+tr.g+'</span>';
    div.onclick=function(){{mpLoad(i);mpIsPlaying=true;mpAud.play();document.getElementById('mpPlayBtn').innerHTML='&#9646;&#9646;';}};
    d.appendChild(div);
  }});
}}
mpAud.addEventListener('timeupdate',function(){{
  if(!mpAud.duration) return;
  var f=document.getElementById('mpFill');
  if(f) f.style.width=(mpAud.currentTime/mpAud.duration*100)+'%';
}});
mpAud.addEventListener('ended',mpNext);

{extra_js}

window.onload=function(){{updateXPDisplay();mpLoad(0);mpRenderPl();}};
</script>
</body>
</html>"""


# ===== ANA SAYFA =====
def ana_sayfa():
    css = """
.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:80px 20px;}
.logo{font-family:'Orbitron';font-size:clamp(2rem,6vw,4rem);font-weight:900;letter-spacing:4px;background:linear-gradient(90deg,var(--neon-orange),var(--neon-blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;}
.tagline{color:#555;font-size:0.85rem;letter-spacing:3px;margin-bottom:40px;}
.stats-bar{display:flex;gap:24px;margin-bottom:40px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);padding:14px 28px;border-radius:12px;}
.stat-b{text-align:center;}
.stat-b .v{font-family:'Orbitron';font-size:1.2rem;color:var(--neon-orange);}
.stat-b .l{font-size:0.68rem;color:#555;letter-spacing:2px;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;width:90%;max-width:1000px;}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);padding:28px 18px;border-radius:16px;text-decoration:none;color:#fff;transition:all 0.3s;cursor:pointer;position:relative;overflow:hidden;}
.card:hover{border-color:var(--neon-orange);transform:translateY(-6px);background:rgba(255,69,0,0.08);}
.card-icon{font-size:2.2rem;margin-bottom:10px;display:block;}
.card h2{font-family:'Orbitron';font-size:0.9rem;margin-bottom:4px;letter-spacing:2px;}
.card p{color:#777;font-size:0.8rem;}
.card.blue:hover{border-color:var(--neon-blue);background:rgba(0,212,255,0.08);}
.card.green:hover{border-color:var(--neon-green);background:rgba(0,255,136,0.08);}
"""
    body = """
<section class="hero">
  <div class="logo">CANO STUDIO</div>
  <div class="tagline">OYUN &middot; STRATEJİ &middot; KORKU &middot; MARKET</div>
  <div class="stats-bar">
    <div class="stat-b"><div class="v" id="stXP">0</div><div class="l">TOPLAM XP</div></div>
    <div class="stat-b"><div class="v" id="stLv">1</div><div class="l">SEVİYE</div></div>
    <div class="stat-b"><div class="v" id="stIt">0</div><div class="l">EŞYA</div></div>
  </div>
  <div class="grid">
    <a href="/neon-arcade" class="card"><span class="card-icon">&#127918;</span><h2>ARCADE</h2><p>Hız ve Refleks</p></a>
    <a href="/strateji" class="card"><span class="card-icon">&#127758;</span><h2>STRATEJİ</h2><p>Gezegen Yönetimi</p></a>
    <a href="/horror" class="card"><span class="card-icon">&#128123;</span><h2>HORROR</h2><p>Korku Hikayesi</p></a>
    <a href="/store" class="card blue"><span class="card-icon">&#128722;</span><h2>MARKET</h2><p>XP Harca</p></a>
    <a href="/profil" class="card green"><span class="card-icon">&#128100;</span><h2>PROFİL</h2><p>İsim &amp; İstatistik</p></a>
    <a href="/gorevler" class="card green"><span class="card-icon">&#128203;</span><h2>GÖREVLER</h2><p>Günlük XP Kazan</p></a>
    <a href="/yorumlar" class="card" style="border-color:rgba(191,0,255,0.3)"><span class="card-icon">&#128172;</span><h2>YORUMLAR</h2><p>Görüşünü Yaz</p></a>
    <a href="/neon-rush" class="card" style="border-color:rgba(191,0,255,0.3)"><span class="card-icon">&#9889;</span><h2>NEON RUSH</h2><p>Uzay Uçuşu</p></a>
    <a href="/isinlanma" class="card" style="border-color:rgba(100,0,180,0.4)"><span class="card-icon">&#128300;</span><h2>IŞINLANMA</h2><p>Bilim Kurgu Korku</p></a>
  </div>
</section>
"""
    js = """
  document.getElementById('stXP').innerText=getXP().toLocaleString();
  document.getElementById('stLv').innerText=Math.floor(getXP()/500+1);
  document.getElementById('stIt').innerText=getItems().length;
"""
    return page("CANO STUDIO", css, body, js)


# ===== STRATEJİ =====
def strateji_page():
    css = """
.gw{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:80px 20px;}
h1{font-family:'Orbitron';font-size:clamp(1.2rem,4vw,2rem);margin-bottom:6px;color:var(--neon-blue);}
.sub{color:#555;font-size:0.8rem;letter-spacing:2px;margin-bottom:24px;}
.planet-wrap{position:relative;width:160px;height:160px;margin:0 auto 24px;}
.planet{width:160px;height:160px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#00eeff,#003a6e);box-shadow:0 0 60px rgba(0,212,255,0.6);animation:spin 12s linear infinite;cursor:pointer;transition:transform 0.2s;}
.planet:hover{transform:scale(1.06);}
.planet:active{transform:scale(0.95);}
@keyframes spin{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
.ring{position:absolute;top:50%;left:50%;width:220px;height:55px;border:2px solid rgba(0,212,255,0.3);border-radius:50%;transform:translate(-50%,-50%) rotateX(75deg);pointer-events:none;}
.res-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;width:100%;max-width:460px;margin-bottom:24px;}
.res-c{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);padding:14px 10px;border-radius:12px;}
.res-c .ri{font-size:1.4rem;}
.res-c .rn{font-size:0.65rem;color:#555;letter-spacing:1px;margin-top:3px;}
.res-c .rv{font-family:'Orbitron';font-size:1.1rem;color:#fff;margin-top:3px;}
.acts{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:18px;}
.prog-bg{width:100%;max-width:400px;background:#111;border-radius:50px;height:7px;margin-bottom:8px;overflow:hidden;}
.prog-f{height:100%;border-radius:50px;background:linear-gradient(90deg,var(--neon-blue),var(--neon-purple));transition:width 0.5s;}
.upg-box{background:rgba(191,0,255,0.07);border:1px solid rgba(191,0,255,0.25);border-radius:12px;padding:18px;width:100%;max-width:460px;margin-bottom:16px;}
.upg-box h3{font-family:'Orbitron';color:var(--neon-purple);font-size:0.8rem;margin-bottom:10px;}
.upg-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.upg-i{background:rgba(0,0,0,0.3);padding:10px;border-radius:8px;text-align:left;}
.upg-i .un{font-size:0.75rem;color:#aaa;}
.upg-i .uc{font-size:0.7rem;color:var(--neon-purple);}
"""
    body = """
<a href="/" class="back-btn">&larr; GERİ</a>
<div class="gw">
  <h1>GALAKTİK YÖNETİM</h1>
  <div class="sub">GEZEGENİNİ YÖNET &middot; KAYNAK TOPLA</div>
  <div class="planet-wrap">
    <div class="planet" id="planet" onclick="mine()" title="Tıkla - Maden"></div>
    <div class="ring"></div>
  </div>
  <div class="prog-bg"><div class="prog-f" id="progBar"></div></div>
  <div style="color:#555;font-size:0.75rem;margin-bottom:20px;" id="lvlInfo">Gezegen Seviyesi: 1</div>
  <div class="res-grid">
    <div class="res-c"><div class="ri">&#9935;</div><div class="rn">MADEN</div><div class="rv" id="rM">0</div></div>
    <div class="res-c"><div class="ri">&#9889;</div><div class="rn">ENERJİ</div><div class="rv" id="rE">0</div></div>
    <div class="res-c"><div class="ri">&#128142;</div><div class="rn">KRİSTAL</div><div class="rv" id="rK">0</div></div>
  </div>
  <div class="acts">
    <button class="btn" onclick="mine()">&#9935; MADEN (+10 XP)</button>
    <button class="btn btn-blue" onclick="genEnergy()">&#9889; ENERJİ (+5 XP)</button>
    <button class="btn btn-purple" id="crystalBtn" onclick="mkCrystal()" disabled>&#128142; KRİSTAL (50 Maden)</button>
  </div>
  <div class="upg-box">
    <h3>&#128300; GELİŞTİRMELER</h3>
    <div class="upg-grid">
      <div class="upg-i"><div class="un">Kazma x<span id="upM">1</span></div><div class="uc">Maliyet: <span id="upMC">100</span> XP</div><button class="btn" style="margin-top:6px;padding:5px 10px;font-size:0.68rem;" onclick="upg('m')">YÜKSELT</button></div>
      <div class="upg-i"><div class="un">Jeneratör x<span id="upE">1</span></div><div class="uc">Maliyet: <span id="upEC">150</span> XP</div><button class="btn btn-blue" style="margin-top:6px;padding:5px 10px;font-size:0.68rem;" onclick="upg('e')">YÜKSELT</button></div>
    </div>
  </div>
</div>
"""
    js = """
  var ST=JSON.parse(localStorage.getItem('cano_st'))||{m:0,e:0,k:0,gl:1,gx:0,um:1,ue:1,umc:100,uec:150};
  function saveST(){localStorage.setItem('cano_st',JSON.stringify(ST));}
  function renderST(){
    document.getElementById('rM').innerText=ST.m;
    document.getElementById('rE').innerText=ST.e;
    document.getElementById('rK').innerText=ST.k;
    document.getElementById('crystalBtn').disabled=ST.m<50;
    document.getElementById('upM').innerText=ST.um;
    document.getElementById('upE').innerText=ST.ue;
    document.getElementById('upMC').innerText=ST.umc;
    document.getElementById('upEC').innerText=ST.uec;
    var need=ST.gl*100;
    document.getElementById('progBar').style.width=Math.min(100,(ST.gx/need)*100)+'%';
    document.getElementById('lvlInfo').innerText='Gezegen Seviyesi: '+ST.gl+' · Sonraki: '+(need-ST.gx)+' maden';
    updateXPDisplay();
  }
  function mine(){
    var g=10*ST.um; ST.m+=ST.um; ST.gx+=ST.um;
    var mn=parseInt(localStorage.getItem('cano_maden')||0)+ST.um;
    localStorage.setItem('cano_maden',mn);
    var need=ST.gl*100;
    if(ST.gx>=need){ST.gx=0;ST.gl++;showToast('GEZEGEN SEVİYE '+ST.gl+'!');}
    addXP(g,'Maden'); saveST(); renderST();
  }
  function genEnergy(){
    var g=5*ST.ue; ST.e+=ST.ue;
    addXP(g,'Enerji'); saveST(); renderST();
  }
  function mkCrystal(){
    if(ST.m<50) return;
    ST.m-=50; ST.k++;
    addXP(30,'Kristal'); saveST(); renderST();
  }
  function upg(t){
    var xp=getXP();
    if(t==='m'){
      if(xp<ST.umc){showToast('XP Yetersiz!');return;}
      setXP(xp-ST.umc); ST.um++; ST.umc=Math.floor(ST.umc*1.8);
    } else {
      if(xp<ST.uec){showToast('XP Yetersiz!');return;}
      setXP(xp-ST.uec); ST.ue++; ST.uec=Math.floor(ST.uec*1.8);
    }
    showToast('Yukseltme tamam!'); saveST(); renderST();
  }
  renderST();
"""
    return page("STRATEJİ", css, body, js)


# ===== ARCADE =====
def arcade_page():
    css = """
.aw{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;text-align:center;}
h1{font-family:'Orbitron';color:var(--neon-orange);font-size:clamp(1.2rem,4vw,2rem);margin-bottom:4px;}
.sub{color:#555;font-size:0.78rem;letter-spacing:3px;margin-bottom:20px;}
.hud{display:flex;gap:20px;margin-bottom:12px;font-family:'Orbitron';font-size:0.8rem;}
.hud span{color:var(--neon-orange);font-size:1.1rem;}
#gameCanvas{border:2px solid var(--neon-orange);border-radius:12px;box-shadow:0 0 40px rgba(255,69,0,0.4);background:#0a0a0a;max-width:100%;touch-action:none;}
.cw{position:relative;display:inline-block;}
#ov{position:absolute;inset:0;background:rgba(0,0,0,0.85);display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:10px;font-family:'Orbitron';}
#ov h2{font-size:1.4rem;color:var(--neon-orange);margin-bottom:8px;}
#ov p{color:#aaa;margin-bottom:16px;font-size:0.8rem;}
.dpad{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:14px;}
.db{background:rgba(255,69,0,0.2);border:1px solid var(--neon-orange);color:#fff;padding:13px 16px;border-radius:8px;font-size:1.1rem;cursor:pointer;user-select:none;transition:background 0.1s;}
.db:active{background:rgba(255,69,0,0.5);}
.de{background:transparent;border:none;pointer-events:none;}
.shop{margin-top:18px;width:100%;max-width:420px;}
.shop-title{font-family:'Orbitron';font-size:0.72rem;color:#444;letter-spacing:2px;margin-bottom:8px;text-align:center;}
.shop-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;}
.shop-c{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:10px;text-align:center;}
.shop-ic{font-size:1.3rem;}
.shop-nm{font-family:'Orbitron';font-size:0.6rem;margin:4px 0;}
.shop-lv{font-size:0.65rem;color:#555;}
.shop-co{font-size:0.65rem;color:var(--neon-blue);margin:3px 0;}
"""
    body = """
<a href="/" class="back-btn">&larr; GERİ</a>
<div class="aw">
  <h1>NEON ARCADE</h1>
  <div class="sub">REFLEKS OYUNU &middot; OKÇU</div>
  <div class="hud">
    <div>SKOR: <span id="scoreVal">0</span></div>
    <div>CAN: <span id="livesVal">&#10084;&#10084;&#10084;</span></div>
    <div>DALGA: <span id="waveVal">1</span></div>
    <div style="color:var(--neon-blue)">&#128176; <span id="coinVal">0</span></div>
  </div>
  <div class="cw">
    <canvas id="gameCanvas" width="420" height="360"></canvas>
    <div id="ov">
      <h2>NEON ARCHER</h2>
      <p>Dusmanları vur, XP &amp; coin kazan!</p>
      <p style="font-size:0.72rem;color:#444;">&larr; &rarr; hareket | SPACE ates | Mobil: dpad</p>
      <button class="btn" onclick="startGame()">BASLAT</button>
    </div>
  </div>
  <div class="dpad">
    <div class="de"></div>
    <button class="db" onpointerdown="keys.up=true" onpointerup="keys.up=false">&#9650;</button>
    <div class="de"></div>
    <button class="db" onpointerdown="keys.left=true" onpointerup="keys.left=false">&#9664;</button>
    <button class="db" onpointerdown="keys.fire=true" onpointerup="keys.fire=false">&#128293;</button>
    <button class="db" onpointerdown="keys.right=true" onpointerup="keys.right=false">&#9654;</button>
  </div>
  <div class="shop">
    <div class="shop-title">SİLAH MAGAZA</div>
    <div class="shop-grid">
      <div class="shop-c"><div class="shop-ic">&#9889;</div><div class="shop-nm">ATES HIZI</div><div class="shop-lv" id="spLv">Sev 1</div><div class="shop-co" id="spCo">20 &#128176;</div><button class="btn btn-blue" style="padding:5px 8px;font-size:0.58rem;margin-top:4px;" onclick="buyU('sp')">AL</button></div>
      <div class="shop-c"><div class="shop-ic">&#128165;</div><div class="shop-nm">HASAR</div><div class="shop-lv" id="dmLv">Sev 1</div><div class="shop-co" id="dmCo">30 &#128176;</div><button class="btn btn-blue" style="padding:5px 8px;font-size:0.58rem;margin-top:4px;" onclick="buyU('dm')">AL</button></div>
      <div class="shop-c"><div class="shop-ic">&#10084;</div><div class="shop-nm">CAN AL</div><div class="shop-lv" id="hpLv">3 Can</div><div class="shop-co" id="hpCo">50 &#128176;</div><button class="btn btn-blue" style="padding:5px 8px;font-size:0.58rem;margin-top:4px;" onclick="buyU('hp')">AL</button></div>
    </div>
  </div>
  <a href="/neon-rush" style="display:inline-block;margin-top:16px;font-family:'Orbitron';font-size:0.72rem;color:var(--neon-purple);border:1px solid rgba(191,0,255,0.4);padding:8px 20px;border-radius:50px;text-decoration:none;">&#9889; NEON RUSH OYNA &rarr;</a>
</div>
"""
    js = r"""
  var gc=document.getElementById('gameCanvas');
  var cx2=gc.getContext('2d');
  var running=false,score=0,lives=3,wave=1;
  var player={x:200,y:320,spd:5};
  var bullets=[],enemies=[],parts=[],drops=[];
  var keys={};
  var lastBullet=0,lastSpawn=0;
  var UPG=JSON.parse(localStorage.getItem('cano_au'))||{coins:0,sp:1,dm:1,hp:3,spc:20,dmc:30,hpc:50};
  function saveU(){localStorage.setItem('cano_au',JSON.stringify(UPG));}
  function renderShop(){
    document.getElementById('coinVal').innerText=UPG.coins;
    document.getElementById('spLv').innerText='Sev '+UPG.sp;
    document.getElementById('spCo').innerText=UPG.spc+' \uD83D\uDCB0';
    document.getElementById('dmLv').innerText='Sev '+UPG.dm;
    document.getElementById('dmCo').innerText=UPG.dmc+' \uD83D\uDCB0';
    document.getElementById('hpLv').innerText=UPG.hp+' Can';
    document.getElementById('hpCo').innerText=UPG.hpc+' \uD83D\uDCB0';
  }
  function buyU(t){
    if(t==='sp'){if(UPG.coins<UPG.spc){showToast('Coin yetersiz!');return;}UPG.coins-=UPG.spc;UPG.sp++;UPG.spc=Math.floor(UPG.spc*1.6);showToast('Ates hizi yukseltildi!');}
    else if(t==='dm'){if(UPG.coins<UPG.dmc){showToast('Coin yetersiz!');return;}UPG.coins-=UPG.dmc;UPG.dm++;UPG.dmc=Math.floor(UPG.dmc*1.6);showToast('Hasar yukseltildi!');}
    else if(t==='hp'){if(UPG.coins<UPG.hpc){showToast('Coin yetersiz!');return;}UPG.coins-=UPG.hpc;UPG.hp++;lives++;UPG.hpc=Math.floor(UPG.hpc*1.8);showToast('Can eklendi!');}
    saveU();renderShop();
  }
  document.addEventListener('keydown',function(e){keys[e.code]=true;if(e.code==='Space')e.preventDefault();});
  document.addEventListener('keyup',function(e){keys[e.code]=false;});
  function startGame(){
    document.getElementById('ov').style.display='none';
    score=0;lives=UPG.hp;wave=1;
    bullets=[];enemies=[];parts=[];drops=[];
    player.x=200;running=true;
    renderShop();loop();
  }
  function spawnE(){
    var types=['basic','fast','tank'];
    var t=types[Math.floor(Math.random()*Math.min(wave,3))];
    enemies.push({x:Math.random()*380+20,y:-20,hp:t==='tank'?3:1,spd:t==='fast'?3.5:(1.2+wave*0.15),type:t,color:t==='tank'?'#ff0066':t==='fast'?'#00ff88':'#00d4ff'});
  }
  function loop(){
    if(!running) return;
    if(keys['ArrowLeft']||keys['left']) player.x=Math.max(16,player.x-player.spd);
    if(keys['ArrowRight']||keys['right']) player.x=Math.min(gc.width-16,player.x+player.spd);
    var now=Date.now();
    var fr=Math.max(80,220-(UPG.sp-1)*30);
    if((keys['Space']||keys['fire'])&&now-lastBullet>fr){
      bullets.push({x:player.x,y:player.y-16,spd:9,w:4,h:12});
      if(UPG.sp>=3){bullets.push({x:player.x-10,y:player.y-10,spd:9,w:4,h:12});bullets.push({x:player.x+10,y:player.y-10,spd:9,w:4,h:12});}
      lastBullet=now;
    }
    var si=Math.max(600,1400-wave*100);
    if(now-lastSpawn>si){spawnE();lastSpawn=now;if(Math.random()<0.3)spawnE();}
    bullets=bullets.filter(function(b){b.y-=b.spd;return b.y>-20;});
    enemies.forEach(function(e){e.y+=e.spd;});
    bullets=bullets.filter(function(b){
      var hit=false;
      enemies=enemies.map(function(e){
        if(!hit&&b.x>e.x-14&&b.x<e.x+14&&b.y>e.y-14&&b.y<e.y+14){
          e.hp-=UPG.dm;hit=true;
          if(e.hp<=0){
            e.dead=true;
            var pts=e.type==='tank'?30:e.type==='fast'?15:10;
            var cd=e.type==='tank'?5:e.type==='fast'?3:1;
            score+=pts;addXP(pts,'Dusман');
            drops.push({x:e.x,y:e.y,vy:1.5,c:cd,life:80});
            var kl=parseInt(localStorage.getItem('cano_kill')||0)+1;
            localStorage.setItem('cano_kill',kl);
            for(var i=0;i<8;i++) parts.push({x:e.x,y:e.y,vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*4,life:25,col:e.color});
          }
        }
        return e;
      }).filter(function(e){return !e.dead;});
      return !hit;
    });
    enemies=enemies.filter(function(e){
      if(e.y>gc.height+10){lives--;if(lives<=0)gameOver();return false;}
      return true;
    });
    if(score>wave*150){wave++;showToast('DALGA '+wave+'!');}
    drops=drops.filter(function(d){
      d.y+=d.vy;d.life--;
      if(Math.abs(d.x-player.x)<20&&Math.abs(d.y-player.y)<20){
        UPG.coins+=d.c;saveU();renderShop();showToast('+'+d.c+' coin');return false;
      }
      return d.life>0&&d.y<gc.height+20;
    });
    parts=parts.filter(function(p){p.x+=p.vx;p.y+=p.vy;p.life--;return p.life>0;});
    document.getElementById('scoreVal').innerText=score;
    document.getElementById('livesVal').innerText='\u2764\uFE0F'.repeat(Math.max(0,lives));
    document.getElementById('waveVal').innerText=wave;
    cx2.clearRect(0,0,gc.width,gc.height);
    cx2.strokeStyle='rgba(255,69,0,0.05)';cx2.lineWidth=1;
    for(var i=0;i<gc.width;i+=40){cx2.beginPath();cx2.moveTo(i,0);cx2.lineTo(i,gc.height);cx2.stroke();}
    for(var i=0;i<gc.height;i+=40){cx2.beginPath();cx2.moveTo(0,i);cx2.lineTo(gc.width,i);cx2.stroke();}
    cx2.save();cx2.translate(player.x,player.y);
    cx2.fillStyle='#ff4500';cx2.shadowColor='#ff4500';cx2.shadowBlur=15;
    cx2.beginPath();cx2.moveTo(0,-16);cx2.lineTo(12,12);cx2.lineTo(0,6);cx2.lineTo(-12,12);cx2.closePath();cx2.fill();
    cx2.restore();
    bullets.forEach(function(b){cx2.fillStyle='#ffdd00';cx2.shadowColor='#ffdd00';cx2.shadowBlur=8;cx2.fillRect(b.x-2,b.y,b.w,b.h);});
    enemies.forEach(function(e){
      cx2.save();cx2.translate(e.x,e.y);cx2.fillStyle=e.color;cx2.shadowColor=e.color;cx2.shadowBlur=12;
      if(e.type==='tank'){cx2.fillRect(-14,-14,28,28);}
      else if(e.type==='fast'){cx2.beginPath();cx2.moveTo(0,14);cx2.lineTo(12,-14);cx2.lineTo(-12,-14);cx2.closePath();cx2.fill();}
      else{cx2.beginPath();cx2.arc(0,0,14,0,Math.PI*2);cx2.fill();}
      if(e.type==='tank'&&e.hp>0){cx2.fillStyle='#333';cx2.fillRect(-14,16,28,4);cx2.fillStyle='#ff0066';cx2.fillRect(-14,16,28*(e.hp/3),4);}
      cx2.restore();
    });
    drops.forEach(function(d){
      cx2.globalAlpha=d.life/80;cx2.fillStyle='#ffd700';cx2.shadowColor='#ffd700';cx2.shadowBlur=8;
      cx2.beginPath();cx2.arc(d.x,d.y,6,0,Math.PI*2);cx2.fill();
      cx2.fillStyle='#000';cx2.shadowBlur=0;cx2.font='bold 7px Arial';cx2.textAlign='center';cx2.fillText(d.c,d.x,d.y+3);
    });
    parts.forEach(function(p){cx2.globalAlpha=p.life/25;cx2.fillStyle=p.col;cx2.beginPath();cx2.arc(p.x,p.y,3,0,Math.PI*2);cx2.fill();});
    cx2.globalAlpha=1;
    requestAnimationFrame(loop);
  }
  function gameOver(){
    running=false;
    var ov=document.getElementById('ov');ov.style.display='flex';
    ov.innerHTML='<h2>GAME OVER</h2><p>Skor: '+score+' Dalga: '+wave+'</p><button class="btn" onclick="startGame()">TEKRAR</button>';
  }
  renderShop();
"""
    return page("ARCADE", css, body, js)

# ===== NEON RUSH (Flappy Bird tarzı) =====
def neonrush_page():
    css = """
.nrw{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;text-align:center;}
h1{font-family:'Orbitron';color:var(--neon-purple);font-size:clamp(1.2rem,4vw,2rem);margin-bottom:4px;}
.sub{color:#555;font-size:0.78rem;letter-spacing:3px;margin-bottom:20px;}
.hud2{display:flex;gap:20px;margin-bottom:12px;font-family:'Orbitron';font-size:0.8rem;}
.hud2 span{color:var(--neon-purple);font-size:1.1rem;}
#nrCanvas{border:2px solid var(--neon-purple);border-radius:12px;box-shadow:0 0 40px rgba(191,0,255,0.5);background:#0a0a0a;max-width:100%;touch-action:none;cursor:pointer;}
.nrcw{position:relative;display:inline-block;}
#nrov{position:absolute;inset:0;background:rgba(0,0,0,0.88);display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:10px;font-family:'Orbitron';}
#nrov h2{font-size:1.4rem;color:var(--neon-purple);margin-bottom:8px;}
#nrov p{color:#aaa;margin-bottom:6px;font-size:0.8rem;}
#nrov .best{color:var(--neon-orange);font-size:0.75rem;margin-bottom:16px;}
.tap-hint{margin-top:16px;color:#444;font-family:'Orbitron';font-size:0.7rem;letter-spacing:2px;}
"""
    body = """
<a href="/neon-arcade" class="back-btn">&larr; ARCADE</a>
<div class="nrw">
  <h1>&#9889; NEON RUSH</h1>
  <div class="sub">ENGELLERDEN KAC &middot; XP KAZAN</div>
  <div class="hud2">
    <div>SKOR: <span id="nrScore">0</span></div>
    <div>EN İYİ: <span id="nrBest">0</span></div>
    <div style="color:var(--neon-orange)">XP: <span id="nrXP">0</span></div>
  </div>
  <div class="nrcw">
    <canvas id="nrCanvas" width="400" height="500"></canvas>
    <div id="nrov">
      <h2>NEON RUSH</h2>
      <p>Engellerden kac, XP kazan!</p>
      <p class="best" id="nrBestOv">En iyi: 0</p>
      <button class="btn btn-purple" onclick="nrStart()">BASLAT</button>
      <div class="tap-hint">SPACE / TIKLA / DOKUN</div>
    </div>
  </div>
  <div class="tap-hint" style="margin-top:12px;">Her 5 skorda +10 XP</div>
</div>
"""
    js = r"""
  var nrc = document.getElementById('nrCanvas');
  var nrcx = nrc.getContext('2d');
  var NRW = nrc.width, NRH = nrc.height;
  var nrRunning = false, nrScore = 0, nrXP = 0;
  var nrBest = parseInt(localStorage.getItem('cano_nr_best')) || 0;
  document.getElementById('nrBest').innerText = nrBest;
  document.getElementById('nrBestOv').innerText = 'En iyi: ' + nrBest;

  // Oyun değişkenleri
  var ship, pipes, stars, particles3, nrFrame, nrSpeed, nrLastPipe, nrGravity;

  function nrReset() {
    ship = {
      x: 80, y: NRH / 2, vy: 0,
      w: 28, h: 18,
      trail: []
    };
    pipes = [];
    particles3 = [];
    stars = [];
    for (var i = 0; i < 80; i++) {
      stars.push({
        x: Math.random() * NRW,
        y: Math.random() * NRH,
        r: Math.random() * 1.5 + 0.3,
        s: Math.random() * 0.5 + 0.2
      });
    }
    nrScore = 0; nrXP = 0; nrFrame = 0;
    nrSpeed = 3; nrLastPipe = 0;
    nrGravity = 0.32;
    document.getElementById('nrScore').innerText = 0;
    document.getElementById('nrXP').innerText = 0;
  }

  function nrStart() {
    document.getElementById('nrov').style.display = 'none';
    nrReset();
    nrRunning = true;
    nrLoop();
  }

  function nrFlap() {
    if (!nrRunning) return;
    ship.vy = -7.5;
  }

  // Kontroller
  document.addEventListener('keydown', function(e) {
    if (e.code === 'Space') { e.preventDefault(); nrFlap(); }
  });
  nrc.addEventListener('click', nrFlap);
  nrc.addEventListener('touchstart', function(e) { e.preventDefault(); nrFlap(); }, {passive: false});

  function spawnPipe() {
    var gap = Math.max(120, 180 - Math.floor(nrScore / 10) * 5);
    var minTop = 60, maxTop = NRH - gap - 60;
    var topH = Math.random() * (maxTop - minTop) + minTop;
    var hue1 = (nrFrame * 0.5) % 360;
    pipes.push({
      x: NRW + 10, topH: topH, botY: topH + gap,
      w: 52, scored: false,
      color: 'hsl(' + hue1 + ',100%,60%)'
    });
  }

  function nrLoop() {
    if (!nrRunning) return;
    nrFrame++;

    // Fizik
    ship.vy += nrGravity;
    ship.y += ship.vy;
    ship.trail.push({x: ship.x, y: ship.y});
    if (ship.trail.length > 18) ship.trail.shift();

    // Hız artışı
    nrSpeed = 3 + nrScore * 0.12;

    // Boru spawn
    if (nrFrame - nrLastPipe > Math.max(60, 95 - nrScore * 2)) {
      spawnPipe();
      nrLastPipe = nrFrame;
    }

    // Borular güncelle
    pipes = pipes.filter(function(p) {
      p.x -= nrSpeed;
      if (!p.scored && p.x + p.w < ship.x) {
        p.scored = true;
        nrScore++;
        document.getElementById('nrScore').innerText = nrScore;
        // XP
        if (nrScore % 5 === 0) {
          nrXP += 10;
          addXP(10, 'Neon Rush');
          document.getElementById('nrXP').innerText = nrXP;
          showToast('+10 XP');
        }
        // Parçacık patlaması
        for (var k = 0; k < 12; k++) {
          particles3.push({
            x: ship.x + 20, y: ship.y,
            vx: (Math.random() - 0.5) * 5,
            vy: (Math.random() - 0.5) * 5,
            life: 30, color: p.color
          });
        }
      }
      return p.x > -p.w;
    });

    // Parçacıklar
    particles3 = particles3.filter(function(p) {
      p.x += p.vx; p.y += p.vy; p.life--;
      return p.life > 0;
    });

    // Yıldızlar
    stars.forEach(function(st) { st.x -= st.s; if (st.x < 0) st.x = NRW; });

    // Çarpışma — zemin/tavan
    if (ship.y + ship.h / 2 > NRH || ship.y - ship.h / 2 < 0) {
      nrGameOver(); return;
    }

    // Çarpışma — borular
    for (var i = 0; i < pipes.length; i++) {
      var p = pipes[i];
      var sx = ship.x, sy = ship.y, sw = ship.w * 0.7, sh = ship.h * 0.7;
      if (sx + sw / 2 > p.x && sx - sw / 2 < p.x + p.w) {
        if (sy - sh / 2 < p.topH || sy + sh / 2 > p.botY) {
          nrGameOver(); return;
        }
      }
    }

    // Çiz
    nrcx.clearRect(0, 0, NRW, NRH);

    // Yıldızlar
    stars.forEach(function(st) {
      nrcx.beginPath();
      nrcx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
      nrcx.fillStyle = 'rgba(255,255,255,0.6)';
      nrcx.fill();
    });

    // Grid
    nrcx.strokeStyle = 'rgba(191,0,255,0.04)';
    nrcx.lineWidth = 1;
    for (var i = 0; i < NRW; i += 40) { nrcx.beginPath(); nrcx.moveTo(i, 0); nrcx.lineTo(i, NRH); nrcx.stroke(); }
    for (var i = 0; i < NRH; i += 40) { nrcx.beginPath(); nrcx.moveTo(0, i); nrcx.lineTo(NRW, i); nrcx.stroke(); }

    // Borular
    pipes.forEach(function(p) {
      var grad = nrcx.createLinearGradient(p.x, 0, p.x + p.w, 0);
      grad.addColorStop(0, p.color);
      grad.addColorStop(1, 'rgba(0,0,0,0.3)');
      nrcx.fillStyle = grad;
      nrcx.shadowColor = p.color; nrcx.shadowBlur = 18;
      // Üst boru
      nrcx.fillRect(p.x, 0, p.w, p.topH);
      nrcx.fillRect(p.x - 4, p.topH - 16, p.w + 8, 16);
      // Alt boru
      nrcx.fillRect(p.x, p.botY, p.w, NRH - p.botY);
      nrcx.fillRect(p.x - 4, p.botY, p.w + 8, 16);
      nrcx.shadowBlur = 0;
    });

    // Trail
    ship.trail.forEach(function(t, i) {
      var alpha = i / ship.trail.length * 0.5;
      nrcx.beginPath();
      nrcx.arc(t.x, t.y, 4 * (i / ship.trail.length), 0, Math.PI * 2);
      nrcx.fillStyle = 'rgba(191,0,255,' + alpha + ')';
      nrcx.fill();
    });

    // Gemi
    nrcx.save();
    nrcx.translate(ship.x, ship.y);
    var tilt = Math.max(-0.5, Math.min(0.5, ship.vy * 0.06));
    nrcx.rotate(tilt);
    // Gövde
    nrcx.fillStyle = '#bf00ff';
    nrcx.shadowColor = '#bf00ff'; nrcx.shadowBlur = 20;
    nrcx.beginPath();
    nrcx.moveTo(14, 0); nrcx.lineTo(-14, -9); nrcx.lineTo(-10, 0); nrcx.lineTo(-14, 9);
    nrcx.closePath(); nrcx.fill();
    // Cam
    nrcx.fillStyle = '#00d4ff';
    nrcx.shadowColor = '#00d4ff'; nrcx.shadowBlur = 10;
    nrcx.beginPath();
    nrcx.arc(2, 0, 5, 0, Math.PI * 2); nrcx.fill();
    // Motor alevi
    nrcx.fillStyle = '#ff4500';
    nrcx.shadowColor = '#ff4500'; nrcx.shadowBlur = 12;
    nrcx.beginPath();
    nrcx.moveTo(-10, 0);
    var flicker = (Math.random() * 6 + 8);
    nrcx.lineTo(-10 - flicker, -4); nrcx.lineTo(-10 - flicker * 0.6, 0);
    nrcx.lineTo(-10 - flicker, 4); nrcx.closePath(); nrcx.fill();
    nrcx.restore();

    // Parçacıklar
    particles3.forEach(function(p) {
      nrcx.globalAlpha = p.life / 30;
      nrcx.fillStyle = p.color;
      nrcx.beginPath(); nrcx.arc(p.x, p.y, 3, 0, Math.PI * 2); nrcx.fill();
    });
    nrcx.globalAlpha = 1;

    // Skor HUD (canvas üzerinde)
    nrcx.fillStyle = 'rgba(191,0,255,0.8)';
    nrcx.font = 'bold 22px Orbitron,monospace';
    nrcx.textAlign = 'center';
    nrcx.shadowColor = '#bf00ff'; nrcx.shadowBlur = 10;
    nrcx.fillText(nrScore, NRW / 2, 40);
    nrcx.shadowBlur = 0;

    requestAnimationFrame(nrLoop);
  }

  function nrGameOver() {
    nrRunning = false;
    if (nrScore > nrBest) {
      nrBest = nrScore;
      localStorage.setItem('cano_nr_best', nrBest);
      addXP(nrScore * 2, 'Neon Rush Rekoru');
    }
    document.getElementById('nrBest').innerText = nrBest;
    var ov = document.getElementById('nrov');
    ov.style.display = 'flex';
    ov.innerHTML = (
      '<h2>GAME OVER</h2>' +
      '<p>Skor: ' + nrScore + '</p>' +
      '<p class="best">En iyi: ' + nrBest + ' &nbsp;|&nbsp; Toplam XP: ' + nrXP + '</p>' +
      '<button class="btn btn-purple" onclick="nrStart()">TEKRAR</button>' +
      '<div class="tap-hint" style="margin-top:12px;">SPACE / TIKLA</div>'
    );
  }
"""
    return page("NEON RUSH", css, body, js)

# ===== IŞINLANMA - HİKAYE OYUNU =====
def isinlanma_page():
    css = """
body{background:#000!important;}
.iw{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 20px;text-align:center;background:#000;}
.scene-box{width:100%;max-width:600px;min-height:320px;position:relative;border-radius:16px;overflow:hidden;margin-bottom:24px;background:#0a0005;}
.scene-img{width:100%;height:280px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;}
.scene-title{font-family:'Orbitron';font-size:0.7rem;color:#444;letter-spacing:3px;margin-bottom:8px;}
.story-text{color:#ccc;font-size:1rem;line-height:1.8;font-family:'Rajdhani';width:100%;max-width:580px;margin-bottom:20px;min-height:80px;text-align:left;white-space:pre-wrap;word-break:break-word;}
.choices{display:flex;flex-direction:column;gap:10px;width:100%;max-width:580px;}
.choice-btn{background:rgba(80,0,120,0.2);border:1px solid rgba(160,0,255,0.3);color:#ccc;padding:14px 20px;border-radius:8px;cursor:pointer;font-family:'Rajdhani';font-size:0.95rem;text-align:left;transition:all 0.2s;}
.choice-btn:hover{background:rgba(160,0,255,0.2);border-color:#a000ff;color:#fff;}
.end-screen{display:none;width:100%;max-width:580px;text-align:center;padding:30px;}
.end-screen h2{font-family:'Orbitron';font-size:1.4rem;margin-bottom:10px;}
.end-screen p{color:#888;margin-bottom:20px;}
.progress-bar{width:100%;max-width:580px;height:3px;background:#111;border-radius:50px;margin-bottom:24px;overflow:hidden;}
.progress-fill{height:100%;border-radius:50px;background:linear-gradient(90deg,#a000ff,#00d4ff);transition:width 0.6s;}
#glitch{position:fixed;inset:0;pointer-events:none;z-index:9998;opacity:0;}
.typing{border-right:2px solid #a000ff;animation:blink 0.7s infinite;}
@keyframes blink{0%,100%{border-color:#a000ff;}50%{border-color:transparent;}}
"""

    body = """
<div id="glitch"></div>
<a href="/" class="back-btn">&larr; ANA SAYFA</a>
<div class="iw">
  <div class="progress-bar"><div class="progress-fill" id="progFill" style="width:0%"></div></div>
  <div class="scene-title" id="sceneTitle">BÖLÜM 1</div>
  <div class="scene-box">
    <div class="scene-img" id="sceneImg"></div>
  </div>
  <div class="story-text" id="storyText"></div>
  <div class="choices" id="choicesBox"></div>
  <div class="end-screen" id="endScreen">
    <h2 id="endTitle"></h2>
    <p id="endDesc"></p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
      <button class="btn btn-purple" onclick="restart()">TEKRAR OYNA</button>
      <a href="/" class="btn" style="text-decoration:none;">ANA SAYFA</a>
    </div>
  </div>
</div>
"""

    js = r"""
  var chapter = 0;
  var choices_made = [];

  var SCENES = [
    {
      title: "SABAH — LAB",
      color: "#0a0510",
      draw: function(c,w,h) {
        c.fillStyle = "#0a0510"; c.fillRect(0,0,w,h);
        // Laboratuar arka plan
        for(var i=0;i<w;i+=40){c.strokeStyle="rgba(100,0,150,0.15)";c.beginPath();c.moveTo(i,0);c.lineTo(i,h);c.stroke();}
        for(var i=0;i<h;i+=40){c.beginPath();c.moveTo(0,i);c.lineTo(w,i);c.stroke();}
        // Masa
        c.fillStyle="#1a0a2a"; c.fillRect(w*0.1,h*0.55,w*0.8,h*0.35);
        c.strokeStyle="#a000ff"; c.lineWidth=1; c.strokeRect(w*0.1,h*0.55,w*0.8,h*0.35);
        // Makine
        c.fillStyle="#200030"; c.fillRect(w*0.35,h*0.2,w*0.3,h*0.35);
        c.strokeStyle="#00d4ff"; c.lineWidth=2; c.strokeRect(w*0.35,h*0.2,w*0.3,h*0.35);
        // Makine ışıkları
        for(var i=0;i<5;i++){
          c.fillStyle="rgba(0,212,255,"+(0.3+Math.random()*0.4)+")";
          c.beginPath(); c.arc(w*0.38+i*w*0.05, h*0.25, 4, 0, Math.PI*2); c.fill();
        }
        // Adam (basit siluet)
        c.fillStyle="#2a0a3a";
        c.beginPath(); c.arc(w*0.25,h*0.4,18,0,Math.PI*2); c.fill();
        c.fillRect(w*0.18,h*0.47,30,50);
        // Saat pencere
        c.fillStyle="rgba(0,0,0,0.7)"; c.fillRect(w*0.65,h*0.1,w*0.2,h*0.15);
        c.strokeStyle="#333"; c.strokeRect(w*0.65,h*0.1,w*0.2,h*0.15);
        c.fillStyle="#ffcc00"; c.font="11px Orbitron,monospace";
        c.textAlign="center"; c.fillText("06:47",w*0.75,h*0.19);
      },
      text: "Sabahın 6:47'si. Dr. Emir gözlerini açtığında masasının üzerinde yüzlerce kablo ve devre döküntüsü vardı. Uyumamıştı. Bir gecede... bitmişti. Işınlanma makinesi. Titreyen eliyle ON düğmesine uzandı.",
      choices: [
        {t:"Düğmeye bas", n:1, xp:10},
        {t:"Önce test et — hayvanla dene", n:2, xp:10}
      ]
    },
    {
      title: "AKTİVASYON",
      color: "#000520",
      draw: function(c,w,h) {
        c.fillStyle="#000520"; c.fillRect(0,0,w,h);
        // Portal efekti
        var cx=w/2, cy=h/2;
        for(var r=80;r>0;r-=10){
          var alpha = (80-r)/80*0.8;
          c.strokeStyle="rgba(160,0,255,"+alpha+")";
          c.lineWidth=2; c.beginPath(); c.arc(cx,cy,r,0,Math.PI*2); c.stroke();
        }
        c.fillStyle="rgba(160,0,255,0.15)"; c.beginPath(); c.arc(cx,cy,80,0,Math.PI*2); c.fill();
        // Işık huzmeleri
        for(var i=0;i<8;i++){
          var angle = i * Math.PI/4;
          c.strokeStyle="rgba(0,212,255,0.3)"; c.lineWidth=1;
          c.beginPath(); c.moveTo(cx,cy);
          c.lineTo(cx+Math.cos(angle)*w*0.6, cy+Math.sin(angle)*h*0.6); c.stroke();
        }
        // Titreşim efekti — yatay çizgiler
        for(var i=0;i<h;i+=4){
          if(Math.random()>0.85){
            c.fillStyle="rgba(160,0,255,0.05)"; c.fillRect(0,i,w,2);
          }
        }
        c.fillStyle="#a000ff"; c.font="bold 18px Orbitron,monospace";
        c.textAlign="center"; c.fillText("IŞINLANMA AKTİF",w/2,h*0.85);
      },
      text: "Makine uğuldamaya başladı. Mavi-mor bir ışık tüm laboratuarı kapladı. Emir'in gözleri kamaştı. Ve sonra... ses. Dışarıdan değil. İÇERİDEN. Duvarların içinden gelen fısıltılar. Adını söylüyorlardı.",
      choices: [
        {t:"Makineyi kapat", n:3, xp:10},
        {t:"Fısıltıları dinle", n:4, xp:15}
      ]
    },
    {
      title: "HAYVAN DENEYİ",
      color: "#050a00",
      draw: function(c,w,h) {
        c.fillStyle="#050a00"; c.fillRect(0,0,w,h);
        // Kafes
        for(var i=0;i<8;i++){
          c.strokeStyle="rgba(0,255,100,0.2)"; c.lineWidth=1;
          c.beginPath(); c.moveTo(w*0.3+i*w*0.05,h*0.2); c.lineTo(w*0.3+i*w*0.05,h*0.7); c.stroke();
        }
        c.strokeStyle="rgba(0,255,100,0.3)"; c.strokeRect(w*0.3,h*0.2,w*0.4,h*0.5);
        // Hayvan silueti (tavşan)
        c.fillStyle="#0a1a0a";
        c.beginPath(); c.arc(w*0.5,h*0.48,20,0,Math.PI*2); c.fill();
        c.beginPath(); c.arc(w*0.46,h*0.32,8,0,Math.PI*2); c.fill();
        c.beginPath(); c.arc(w*0.54,h*0.32,8,0,Math.PI*2); c.fill();
        c.fillStyle="#00ff44"; c.font="12px Orbitron,monospace";
        c.textAlign="center"; c.fillText("DENEY #001",w/2,h*0.85);
      },
      text: "Emir kafesten beyaz tavşanı çıkardı ve ışınlanma platformuna koydu. Makineyi çalıştırdı. Bir flaş. Tavşan gözden kayboldu. Sonra... beş saniye sessizlik. Ve platform yeniden parladı. Tavşan geri döndü. Ama farklıydı.",
      choices: [
        {t:"Tavşana dokun", n:5, xp:10},
        {t:"Gözlemle — dokunma", n:6, xp:15}
      ]
    },
    {
      title: "KAPATIYOR",
      color: "#0a0000",
      draw: function(c,w,h) {
        c.fillStyle="#0a0000"; c.fillRect(0,0,w,h);
        // Kırmızı alarm
        c.fillStyle="rgba(255,0,0,0.05)"; c.fillRect(0,0,w,h);
        for(var i=0;i<3;i++){
          c.strokeStyle="rgba(255,0,0,"+(0.1+i*0.1)+")";
          c.lineWidth=3; c.strokeRect(10+i*8,10+i*8,w-20-i*16,h-20-i*16);
        }
        // Makine kapanıyor
        c.fillStyle="#1a0000"; c.fillRect(w*0.35,h*0.2,w*0.3,h*0.4);
        c.strokeStyle="rgba(255,50,0,0.5)"; c.lineWidth=2; c.strokeRect(w*0.35,h*0.2,w*0.3,h*0.4);
        // Yanıp sönen ışık
        c.fillStyle="rgba(255,100,0,0.6)"; c.beginPath(); c.arc(w*0.5,h*0.4,12,0,Math.PI*2); c.fill();
        c.fillStyle="#ff3300"; c.font="14px Orbitron,monospace";
        c.textAlign="center"; c.fillText("KAPANIYOR...",w/2,h*0.75);
        c.fillText("ERİŞİLEMEZ",w/2,h*0.85);
      },
      text: "Emir güç düğmesine bastı. Makine durdu. Ama sesler... durmadı. Duvarlar hâlâ fısıldıyordu. Artık dışarıdan da sesler geliyordu. Sokaktan. Sanki herkes aynı anda konuşmaya başlamıştı. Cebinden telefonu çıkardı.",
      choices: [
        {t:"Arkadaşını ara — Mert'i", n:7, xp:10},
        {t:"Evi terk et — kaç", n:8, xp:10}
      ]
    },
    {
      title: "FIŞILTILAR",
      color: "#050510",
      draw: function(c,w,h) {
        c.fillStyle="#050510"; c.fillRect(0,0,w,h);
        // Dalga efekti
        for(var y=0;y<h;y+=3){
          var offset = Math.sin(y*0.05)*20;
          c.strokeStyle="rgba(100,0,200,"+(0.05+Math.sin(y*0.1)*0.05)+")";
          c.lineWidth=1; c.beginPath(); c.moveTo(0+offset,y); c.lineTo(w+offset,y); c.stroke();
        }
        // Yüz silueti (bulanık)
        c.fillStyle="rgba(80,0,150,0.2)";
        c.beginPath(); c.arc(w/2,h*0.4,60,0,Math.PI*2); c.fill();
        c.fillStyle="rgba(160,0,255,0.1)";
        c.beginPath(); c.arc(w/2,h*0.4,40,0,Math.PI*2); c.fill();
        // Gözler
        c.fillStyle="rgba(255,255,255,0.8)";
        c.beginPath(); c.arc(w*0.44,h*0.38,6,0,Math.PI*2); c.fill();
        c.beginPath(); c.arc(w*0.56,h*0.38,6,0,Math.PI*2); c.fill();
        c.fillStyle="#a000ff"; c.font="13px Orbitron,monospace";
        c.textAlign="center"; c.fillText("SEN DE BİZDENSİN",w/2,h*0.82);
      },
      text: "Fısıltılar şekillendi. Bir ses, sonra on, sonra yüzlerce. 'Emir. Emir. Emir.' Onu çağırıyorlardı. Makinenin açtığı kapıdan bir şeyler gelmişti. Ve onlar Emir'i tanıyordu. Hep tanımışlardı.",
      choices: [
        {t:"Onlara cevap ver", n:9, xp:20},
        {t:"Arkadaşını ara — hemen", n:7, xp:10}
      ]
    },
    {
      title: "TAVŞAN",
      color: "#000a00",
      draw: function(c,w,h) {
        c.fillStyle="#000a00"; c.fillRect(0,0,w,h);
        // Tavşan yakın plan — anormal
        c.fillStyle="#0a1500";
        c.beginPath(); c.arc(w/2,h*0.45,45,0,Math.PI*2); c.fill();
        // Gözler — kırmızı
        c.fillStyle="#ff0000"; c.shadowColor="#ff0000"; c.shadowBlur=15;
        c.beginPath(); c.arc(w*0.43,h*0.4,8,0,Math.PI*2); c.fill();
        c.beginPath(); c.arc(w*0.57,h*0.4,8,0,Math.PI*2); c.fill();
        c.shadowBlur=0;
        // Ağız
        c.strokeStyle="rgba(200,0,0,0.7)"; c.lineWidth=2;
        c.beginPath(); c.arc(w*0.5,h*0.5,15,0.1,Math.PI-0.1); c.stroke();
        c.fillStyle="#ff3333"; c.font="12px Orbitron,monospace";
        c.textAlign="center"; c.fillText("O ARTIK O DEĞİL",w/2,h*0.82);
      },
      text: "Emir elini uzattı. Tavşan kımıldamadı. Sonra döndü. Gözleri... kırmızıydı. Hem de kan kırmızısı. Sesi yoktu artık. Ama Emir bir şey hissetti — tavşanın içinde bir şey vardı. Makine onu götürmüş, başka bir şey göndermişti.",
      choices: [
        {t:"Tavşanı kafese geri koy", n:10, xp:10},
        {t:"Makineyi hemen kapat", n:3, xp:10}
      ]
    },
    {
      title: "GÖZLEMCİ",
      color: "#050a00",
      draw: function(c,w,h) {
        c.fillStyle="#050a00"; c.fillRect(0,0,w,h);
        // Mikroskop görüntüsü
        c.strokeStyle="rgba(0,200,0,0.2)"; c.lineWidth=1;
        for(var i=0;i<5;i++){c.beginPath();c.arc(w/2,h/2,30+i*20,0,Math.PI*2);c.stroke();}
        // Hücre benzeri şekiller
        for(var i=0;i<6;i++){
          var angle=i*Math.PI/3;
          c.fillStyle="rgba(0,"+Math.floor(100+Math.random()*100)+",0,0.3)";
          c.beginPath(); c.arc(w/2+Math.cos(angle)*40,h/2+Math.sin(angle)*40,10,0,Math.PI*2); c.fill();
        }
        c.fillStyle="#00ff44"; c.font="11px Orbitron,monospace";
        c.textAlign="center"; c.fillText("DNA ANOMALY +%847",w/2,h*0.85);
      },
      text: "Emir not defterini açtı ve gözlemlemeye başladı. Tavşan saatlerce aynı köşede oturdu. Nefes almıyordu. Ama canlıydı. Sonra defterine baktı — kendi eliyle yazmıştı, ama yazmadığı bir cümle vardı: 'SEN SONRASIN'",
      choices: [
        {t:"Arkadaşını ara — Mert'i", n:7, xp:15},
        {t:"Daha fazla araştır", n:11, xp:20}
      ]
    },
    {
      title: "MERT GELİYOR",
      color: "#0a0005",
      draw: function(c,w,h) {
        c.fillStyle="#0a0005"; c.fillRect(0,0,w,h);
        // Telefon ekranı
        c.fillStyle="#111"; c.fillRect(w*0.35,h*0.15,w*0.3,h*0.55);
        c.strokeStyle="#a000ff"; c.lineWidth=1; c.strokeRect(w*0.35,h*0.15,w*0.3,h*0.55);
        // Profil
        c.fillStyle="#2a0a3a"; c.beginPath(); c.arc(w*0.5,h*0.32,20,0,Math.PI*2); c.fill();
        c.fillStyle="#ccc"; c.font="10px monospace"; c.textAlign="center";
        c.fillText("MERT",w*0.5,h*0.5);
        c.fillStyle="#00ff44"; c.font="9px monospace";
        c.fillText("ARANIYOR...",w*0.5,h*0.58);
        // Kapı
        c.fillStyle="#0d0010"; c.fillRect(w*0.1,h*0.3,w*0.18,h*0.55);
        c.strokeStyle="#333"; c.strokeRect(w*0.1,h*0.3,w*0.18,h*0.55);
        c.fillStyle="#888"; c.beginPath(); c.arc(w*0.25,h*0.57,4,0,Math.PI*2); c.fill();
      },
      text: "Telefon üç kez çaldı. Mert cevap verdi. 'Sesim garipleşti, değil mi?' diye sordu Emir. Uzun bir sessizlik. 'Geliyorum' dedi Mert. Kırk dakika sonra kapı çalındı. Emir kapıyı açtı. Orada Mert vardı... ama gözleri farklıydı.",
      choices: [
        {t:"İçeri al", n:12, xp:10},
        {t:"Kapıyı kapatmaya çalış", n:13, xp:15}
      ]
    },
    {
      title: "KAÇIŞ",
      color: "#050000",
      draw: function(c,w,h) {
        c.fillStyle="#050000"; c.fillRect(0,0,w,h);
        // Gece sokağı
        for(var i=0;i<w;i+=60){
          c.fillStyle="#0d0d0d"; c.fillRect(i,h*0.4,50,h*0.6);
          c.strokeStyle="#1a0a00"; c.strokeRect(i,h*0.4,50,h*0.6);
          // Pencere ışıkları
          for(var j=0;j<3;j++){
            c.fillStyle=Math.random()>0.5?"rgba(255,180,0,0.3)":"rgba(0,0,0,0.5)";
            c.fillRect(i+8,h*0.45+j*h*0.12,15,10);
          }
        }
        // Yol
        c.fillStyle="#0a0a0a"; c.fillRect(0,h*0.7,w,h*0.3);
        // Adam koşuyor
        c.fillStyle="#1a0a2a";
        c.beginPath(); c.arc(w*0.2,h*0.63,12,0,Math.PI*2); c.fill();
        c.fillRect(w*0.16,h*0.67,18,28);
        c.fillStyle="#ff3300"; c.font="11px Orbitron,monospace";
        c.textAlign="center"; c.fillText("KAÇIYOR",w/2,h*0.88);
      },
      text: "Emir cebini kapıp dışarı fırladı. Gece sokaklarında koşmaya başladı. Ama sokak... değişmişti. Her köşede aynı adam duruyordu. Kendisi. Kendisine benzeyenler. Makine bir kapı açmıştı — ve o kapıdan çok şey geçmişti.",
      choices: [
        {t:"Durumunu kabul et", n:14, xp:20},
        {t:"Geri dön — makineyi yok et", n:15, xp:25}
      ]
    },
    {
      title: "ONLARLA KONUŞ",
      color: "#050510",
      draw: function(c,w,h) {
        c.fillStyle="#050510"; c.fillRect(0,0,w,h);
        // Boyutlar arası geçiş
        var cx=w/2, cy=h/2;
        for(var i=0;i<20;i++){
          var r=i*8; var alpha=(20-i)/20*0.3;
          c.strokeStyle="rgba(160,0,255,"+alpha+")"; c.lineWidth=0.5;
          c.beginPath(); c.arc(cx,cy,r,0,Math.PI*2); c.stroke();
        }
        // Siluetler
        for(var i=0;i<5;i++){
          var x=w*0.1+i*w*0.2;
          c.fillStyle="rgba(80,0,150,0.2)";
          c.beginPath(); c.arc(x,h*0.5,20,0,Math.PI*2); c.fill();
          c.fillRect(x-10,h*0.55,20,30);
        }
        c.fillStyle="#a000ff"; c.font="11px Orbitron,monospace";
        c.textAlign="center"; c.fillText("BOYUTLAR ARASI",w/2,h*0.88);
      },
      text: "Emir cevap verdi: 'Kimsiniz?' Fısıltılar birleşti, tek bir ses oldu. 'Biz senin olasılıklarınız. Makine onları serbest bıraktı. Her karar bir boyut yaratır — ve şimdi hepsi burada.' Emir anladı. Makine sadece nesne değil — olasılık kapısıydı.",
      choices: [
        {t:"Kapıyı kapat — hepsini gönder geri", n:16, xp:30},
        {t:"Onları kabul et — yeni dünya", n:17, xp:25}
      ]
    },
    {
      title: "TEMAS",
      color: "#050000",
      draw: function(c,w,h) {
        c.fillStyle="#050000"; c.fillRect(0,0,w,h);
        // El uzanıyor
        c.fillStyle="#0a0000";
        c.beginPath();
        c.moveTo(w*0.3,h*0.8); c.lineTo(w*0.45,h*0.5); c.lineTo(w*0.55,h*0.5); c.lineTo(w*0.7,h*0.8);
        c.closePath(); c.fill();
        // Parmaklar
        for(var i=0;i<5;i++){
          c.fillRect(w*0.35+i*w*0.07,h*0.3,10,h*0.22);
        }
        c.fillStyle="rgba(255,0,0,0.15)"; c.fillRect(0,0,w,h);
        c.fillStyle="#ff3300"; c.font="12px Orbitron,monospace";
        c.textAlign="center"; c.fillText("DOKUNMA...",w/2,h*0.18);
      },
      text: "Tavşanı kafese koydu ve elleri titreyerek geri çekildi. Ama geç kalmıştı. Parmak ucunda siyah bir leke belirmişti. Küçücük. Ama genişliyordu. Ve Emir bir şey hissetti — içinde bir sesin sustuğunu. Kendi sesinin.",
      choices: [
        {t:"Arkadaşını ara", n:7, xp:10},
        {t:"Makineyi yeniden çalıştır — tersine", n:18, xp:25}
      ]
    },
    {
      title: "ARAŞTIRMA",
      color: "#000510",
      draw: function(c,w,h) {
        c.fillStyle="#000510"; c.fillRect(0,0,w,h);
        // Notlar, formüller
        c.fillStyle="rgba(0,100,200,0.1)"; c.fillRect(0,0,w,h);
        for(var i=0;i<8;i++){
          c.fillStyle="rgba(100,150,255,0.15)"; c.fillRect(w*0.1,h*0.1+i*h*0.1,w*0.8,2);
          c.fillStyle="rgba(100,150,255,0.2)"; c.font="9px monospace"; c.textAlign="left";
          var formulas=["E=mc²","ΔX·ΔP≥ħ/2","∇²ψ=0","P(A|B)=P(B|A)·P(A)/P(B)","∮E·dA=Q/ε₀"];
          c.fillText(formulas[i%formulas.length], w*0.12, h*0.15+i*h*0.1);
        }
        c.fillStyle="#00d4ff"; c.font="11px Orbitron,monospace";
        c.textAlign="center"; c.fillText("BOYUT KAPISI TESPİT EDİLDİ",w/2,h*0.88);
      },
      text: "Saatler geçti. Emir notlarını inceledi ve tüyler ürpertici bir şey fark etti — makinenin formülleri, kendi el yazısıyla yazılmıştı. Ama bazı sayfalar sanki başka biri yazmış gibiydi. Aynı el ama... farklı bir zihin. Sonra telefon çaldı. Arayan: KENDİSİ.",
      choices: [
        {t:"Telefonu aç", n:19, xp:25},
        {t:"Kapat — aramaya devam et", n:7, xp:15}
      ]
    },
    {
      title: "MERT — KAPIDA",
      color: "#0a0010",
      draw: function(c,w,h) {
        c.fillStyle="#0a0010"; c.fillRect(0,0,w,h);
        // Kapıda duran figür
        c.fillStyle="#050010"; c.fillRect(w*0.35,h*0.05,w*0.3,h*0.85);
        c.strokeStyle="#200030"; c.lineWidth=2; c.strokeRect(w*0.35,h*0.05,w*0.3,h*0.85);
        // Figür silueti
        c.fillStyle="#0d0020";
        c.beginPath(); c.arc(w*0.5,h*0.28,22,0,Math.PI*2); c.fill();
        c.fillRect(w*0.44,h*0.36,24,45);
        // Gözler — parlıyor
        c.fillStyle="rgba(160,0,255,0.9)"; c.shadowColor="#a000ff"; c.shadowBlur=10;
        c.beginPath(); c.arc(w*0.47,h*0.26,5,0,Math.PI*2); c.fill();
        c.beginPath(); c.arc(w*0.53,h*0.26,5,0,Math.PI*2); c.fill();
        c.shadowBlur=0;
        c.fillStyle="#a000ff"; c.font="11px Orbitron,monospace";
        c.textAlign="center"; c.fillText("HER ŞEY BİTTİ",w/2,h*0.92);
      },
      text: "Mert içeri girdi ve kapıyı kapattı. Oturdu. Uzun süre sessiz kaldı. Sonra Emir'e döndü ve dedi ki: 'Her şey bitti.' Sesi farklıydı. Derin. Çok katmanlı. Sanki aynı anda birden fazla kişi konuşuyordu. 'Makine seçti seni, Emir.'",
      choices: [
        {t:"'Ne için seçti?' diye sor", n:20, xp:20},
        {t:"Kaç — pencereden atla", n:21, xp:15}
      ]
    },
    {
      title: "DİRENİŞ",
      color: "#0a0000",
      draw: function(c,w,h) {
        c.fillStyle="#0a0000"; c.fillRect(0,0,w,h);
        // Kapı kapanıyor
        c.fillStyle="#0d0005"; c.fillRect(w*0.35,h*0.05,w*0.3,h*0.85);
        c.strokeStyle="rgba(255,0,0,0.5)"; c.lineWidth=3; c.strokeRect(w*0.35,h*0.05,w*0.3,h*0.85);
        // Çizikler kapıda
        for(var i=0;i<5;i++){
          c.strokeStyle="rgba(255,0,0,0.2)"; c.lineWidth=2;
          c.beginPath(); c.moveTo(w*0.4+i*5,h*0.1); c.lineTo(w*0.37+i*5,h*0.5); c.stroke();
        }
        // Kilit
        c.fillStyle="#1a0000"; c.fillRect(w*0.46,h*0.5,0.08*w,0.1*h);
        c.fillStyle="#ff3300"; c.font="11px Orbitron,monospace";
        c.textAlign="center"; c.fillText("TUZAK",w/2,h*0.88);
      },
      text: "Emir kapıyı kapatmaya çalıştı — ama Mert çoktan içeri girmişti. Hız... insanüstüydü. Emir geri çekildi. 'Neden kaçıyorsun?' dedi Mert. Sesi sakin, soğuktu. 'Makineyi çalıştırdın. Bu bir kapıydı. Ve sen kapıyı açtın.'",
      choices: [
        {t:"'Ne geçti kapıdan?' diye sor", n:20, xp:20},
        {t:"Makineyi kır", n:22, xp:30}
      ]
    },
    {
      title: "KABUL",
      color: "#000510",
      draw: function(c,w,h) {
        c.fillStyle="#000510"; c.fillRect(0,0,w,h);
        // Paralel çizgiler — çok boyut
        for(var i=0;i<12;i++){
          var y = i*h/12;
          var col = "hsl("+(270+i*10)+",80%,30%)";
          c.strokeStyle=col; c.lineWidth=0.5; c.globalAlpha=0.3;
          c.beginPath(); c.moveTo(0,y); c.lineTo(w,y+20); c.stroke();
        }
        c.globalAlpha=1;
        c.fillStyle="#6600aa"; c.font="13px Orbitron,monospace";
        c.textAlign="center"; c.fillText("YENİ GERÇEK",w/2,h*0.88);
      },
      text: "Emir durdu. Baktı. Kendine bakan onlarca kendisi. Ve anladı — kaçış yoktu. Makine onu seçmemişti. O makineyi yapmıştı. Ve derin içinden bir ses dedi: 'Hep böyleydi. Sen sadece hatırladın.'",
      choices: [
        {t:"Onlara katıl", n:17, xp:30},
        {t:"Hepsini reddet — kendi kal", n:23, xp:35}
      ]
    },
    {
      title: "YOK ET",
      color: "#0a0000",
      draw: function(c,w,h) {
        c.fillStyle="#0a0000"; c.fillRect(0,0,w,h);
        // Kırık makine
        for(var i=0;i<20;i++){
          var x=Math.random()*w, y=Math.random()*h;
          var size=Math.random()*20+5;
          c.fillStyle="rgba(255,"+(Math.floor(Math.random()*50))+",0,"+(0.1+Math.random()*0.3)+")";
          c.fillRect(x,y,size,size);
        }
        c.fillStyle="#ff4400"; c.font="14px Orbitron,monospace";
        c.textAlign="center"; c.fillText("SİSTEM ÇÖKÜYOR",w/2,h*0.5);
        c.fillStyle="#ff6600"; c.font="11px Orbitron,monospace";
        c.fillText("BOYUTLAR KAPANIYOR",w/2,h*0.6);
      },
      text: "Emir geri döndü, laboratuara girdi ve makineye bir kez baktı. Sonra balyozu kaldırdı. İlk darbe — bir çığlık. Makinenin çığlığı mıydı, yoksa başka bir şeyin mi? İkinci darbe. Üçüncü. Fısıltılar azaldı. Azaldı. Ve...",
      choices: [
        {t:"Son darbeyi vur", n:24, xp:40},
        {t:"Dur — dinle", n:25, xp:20}
      ]
    },

    // SONLAR
    {
      title: "SON: KAPININ BEKÇİSİ",
      color: "#050010",
      draw: function(c,w,h) {
        c.fillStyle="#050010"; c.fillRect(0,0,w,h);
        var cx=w/2,cy=h/2;
        for(var r=120;r>0;r-=8){c.strokeStyle="rgba(160,0,255,"+(120-r)/120*0.5+")";c.lineWidth=1;c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.stroke();}
        c.fillStyle="#a000ff"; c.font="16px Orbitron,monospace"; c.textAlign="center";
        c.fillText("∞",cx,cy+6);
        c.fillStyle="#ccc"; c.font="11px Orbitron,monospace"; c.fillText("SEN ARTIK BEKÇİSİN",cx,h*0.85);
      },
      text: "Emir kapıyı kapattı — tüm olasılıkları geri gönderdi. Ama bedelini ödedi. Artık o da tam bu dünyada değildi. Kapının bekçisi olmuştu. Görünmez, ama her yerde. Makineyi bir daha kimse çalıştıramadı. Çünkü artık Emir vardı — aralarında.",
      choices: [], end: "bekci", xpBonus: 80
    },
    {
      title: "SON: YENİ DÜNYA",
      color: "#000520",
      draw: function(c,w,h) {
        c.fillStyle="#000520"; c.fillRect(0,0,w,h);
        for(var i=0;i<50;i++){
          c.fillStyle="rgba("+Math.floor(Math.random()*100)+","+Math.floor(Math.random()*100)+",255,0.4)";
          c.beginPath(); c.arc(Math.random()*w,Math.random()*h,Math.random()*3,0,Math.PI*2); c.fill();
        }
        c.fillStyle="#00d4ff"; c.font="14px Orbitron,monospace"; c.textAlign="center";
        c.fillText("YENİ DÜZEN",w/2,h*0.85);
      },
      text: "Emir kabul etti. Tüm olasılıklar, tüm boyutlar birleşti. Dünya değişmedi — ama Emir değişti. Artık her şeyi görüyordu. Her kararın yarattığı dalgalanmaları. Ve bir gün, başka biri de bir makine yapacaktı. Emir orada olacaktı.",
      choices: [], end: "yenidunya", xpBonus: 60
    },
    {
      title: "SON: SEÇİLMİŞ",
      color: "#0a0505",
      draw: function(c,w,h) {
        c.fillStyle="#0a0505"; c.fillRect(0,0,w,h);
        c.fillStyle="#ff4400"; c.font="18px Orbitron,monospace"; c.textAlign="center";
        c.fillText("SEÇİLMİŞ",w/2,h*0.45);
        c.fillStyle="#ccc"; c.font="11px Orbitron,monospace";
        c.fillText("SON YOK, SADECE BAŞLANGIÇ",w/2,h*0.62);
      },
      text: "Mert Emir'e döndü ve gülümsedi. 'Makine için değil. İnsanlık için seçildin. Her 10.000 yılda bir, birisi kapıyı açar. Sen açtın. Şimdi ne yapacağın senin elinde.' Emir pencereye baktı. Güneş doğuyordu — ama mavi.",
      choices: [], end: "secilmis", xpBonus: 100
    },
    {
      title: "SON: KAÇIŞ",
      color: "#050000",
      draw: function(c,w,h) {
        c.fillStyle="#050000"; c.fillRect(0,0,w,h);
        c.fillStyle="#333"; c.fillRect(0,h*0.7,w,h*0.3);
        c.strokeStyle="#1a0000"; c.strokeRect(0,h*0.7,w,h*0.3);
        for(var i=0;i<w;i+=20){c.strokeStyle="rgba(50,0,0,0.3)";c.beginPath();c.moveTo(i,h*0.7);c.lineTo(i,h);c.stroke();}
        c.fillStyle="#ff6600"; c.font="13px Orbitron,monospace"; c.textAlign="center";
        c.fillText("ÖZGÜR MÜ?",w/2,h*0.88);
      },
      text: "Pencereden atladı — ikinci kat. Düştü, kalktı. Koştu. Şehir dışına çıktı. Yıllarca saklandı. Ama her baktığı aynada kendisini gördü — ama hep biraz farklı. Makine onu bulamamıştı. Ya da bulmak istememişti.",
      choices: [], end: "kacis", xpBonus: 40
    },
    {
      title: "SON: KIRILMA",
      color: "#0a0000",
      draw: function(c,w,h) {
        c.fillStyle="#0a0000"; c.fillRect(0,0,w,h);
        for(var i=0;i<30;i++){
          var x=Math.random()*w,y=Math.random()*h;
          c.strokeStyle="rgba(255,50,0,0.2)"; c.lineWidth=1;
          c.beginPath(); c.moveTo(x,y); c.lineTo(x+(Math.random()-0.5)*80,y+(Math.random()-0.5)*80); c.stroke();
        }
        c.fillStyle="#ff3300"; c.font="13px Orbitron,monospace"; c.textAlign="center";
        c.fillText("HER ŞEY BİTTİ",w/2,h*0.88);
      },
      text: "Son darbe. Makine patladı. Bir flaş. Ve sessizlik. Emir yerde oturuyordu. Fısıltılar kesilmişti. Mert... kaybolmuştu. Dışarıya çıktı. Normal bir sabah. Kuşlar, trafik. Ama Emir biliyordu — bir şeyi kırmıştı. Ve o şey geri gelmezdi.",
      choices: [], end: "kirilma", xpBonus: 70
    },
    {
      title: "SON: SON KAPIYA DOĞRU",
      color: "#050510",
      draw: function(c,w,h) {
        c.fillStyle="#050510"; c.fillRect(0,0,w,h);
        var cx=w/2,cy=h/2;
        c.fillStyle="rgba(100,0,200,0.15)"; c.fillRect(0,0,w,h);
        c.strokeStyle="rgba(100,0,200,0.5)"; c.lineWidth=2;
        c.strokeRect(w*0.3,h*0.2,w*0.4,h*0.6);
        c.fillStyle="#a000ff"; c.font="13px Orbitron,monospace"; c.textAlign="center";
        c.fillText("OTÖTEKİ KAPIYA",cx,h*0.88);
      },
      text: "Durdu. Dinledi. Fısıltılar değişmişti — artık çığlık değil, bir şarkıydı. Ve Emir anladı. Makine kırılmamıştı. Değişmişti. Bir sonraki boyuta kapı açmıştı. Emir eşiğe adım attı. Ve adım attığı anda, arkasında laboratuar —  kayboldu.",
      choices: [], end: "oteki", xpBonus: 90
    }
  ];

  var canvas = document.createElement('canvas');
  canvas.width = 560; canvas.height = 280;
  document.getElementById('sceneImg').appendChild(canvas);
  var ctx = canvas.getContext('2d');

  function drawScene(sc) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    sc.draw(ctx, canvas.width, canvas.height);
  }

  function typeText(text, callback) {
    var el = document.getElementById('storyText');
    el.textContent = '';
    el.classList.add('typing');
    var i = 0;
    var speed = 22;
    var timer = setInterval(function() {
      el.textContent += text.charAt(i);
      i++;
      if(i >= text.length) {
        clearInterval(timer);
        el.classList.remove('typing');
        if(callback) callback();
      }
    }, speed);
  }

  function glitchEffect() {
    var el = document.getElementById('glitch');
    el.style.background = 'rgba(160,0,255,0.08)';
    el.style.opacity = '1';
    setTimeout(function() { el.style.opacity='0'; }, 80);
    setTimeout(function() { el.style.opacity='1'; el.style.background='rgba(255,0,0,0.05)'; }, 120);
    setTimeout(function() { el.style.opacity='0'; }, 200);
  }

  function loadScene(idx) {
    var sc = SCENES[idx];
    chapter = idx;

    var prog = Math.min(100, (idx / (SCENES.length-1)) * 100);
    document.getElementById('progFill').style.width = prog + '%';
    document.getElementById('sceneTitle').innerText = sc.title;

    glitchEffect();
    drawScene(sc);

    if(sc.end) {
      document.getElementById('choicesBox').innerHTML = '';
      typeText(sc.text, function() {
        var bonus = sc.xpBonus || 50;
        addXP(bonus, sc.end + ' sonu');
        setTimeout(function() {
          document.getElementById('endScreen').style.display = 'block';
          var titles = {
            bekci: 'KAPININ BEKÇİSİ', yenidunya: 'YENİ DÜNYA',
            secilmis: 'SEÇİLMİŞ', kacis: 'KAÇIŞ',
            kirilma: 'KIRILMA', oteki: 'ÖTEKİ KAPI'
          };
          var descs = {
            bekci: 'Sen kapıyı kapattın — ama içinde kaldın.',
            yenidunya: 'Yeni bir düzen. Sen merkezindesin.',
            secilmis: 'Her şeyin başlangıcısın. Mavi güneş doğuyor.',
            kacis: 'Özgür müsün? Yoksa sadece başka bir kafeste mi?',
            kirilma: 'Kırdın. Ama ne kırdın tam olarak?',
            oteki: 'Öte kapıya adım attın. Dönüş yok.'
          };
          document.getElementById('endTitle').innerText = titles[sc.end] || 'SON';
          document.getElementById('endDesc').innerText = descs[sc.end] || '';
          document.getElementById('endScreen').style.display = 'block';
        }, 500);
      });
      return;
    }

    typeText(sc.text, function() {
      var box = document.getElementById('choicesBox');
      box.innerHTML = '';
      sc.choices.forEach(function(ch) {
        var btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.innerText = ch.t;
        btn.onclick = function() {
          if(ch.xp) addXP(ch.xp, 'Işınlanma');
          choices_made.push(idx);
          document.getElementById('choicesBox').innerHTML = '';
          document.getElementById('storyText').innerText = '';
          setTimeout(function() { loadScene(ch.n); }, 300);
        };
        box.appendChild(btn);
      });
    });
  }

  function restart() {
    document.getElementById('endScreen').style.display = 'none';
    choices_made = [];
    loadScene(0);
  }

  loadScene(0);
"""
    return page("IŞINLANMA", css, body, js)



# ===== HORROR =====
def horror_page():
    css = """
body{background:#000;}
.hw{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;text-align:center;}
h1{font-family:'Orbitron';color:#cc0000;font-size:clamp(1.2rem,4vw,2rem);margin-bottom:6px;text-shadow:0 0 20px #cc0000;}
.sub{color:#400;font-size:0.78rem;letter-spacing:3px;margin-bottom:20px;}
.hrow{display:flex;gap:16px;margin-bottom:18px;font-family:'Orbitron';font-size:0.72rem;}
.hst{background:rgba(100,0,0,0.2);border:1px solid rgba(200,0,0,0.3);padding:7px 14px;border-radius:8px;}
.hst span{color:#cc0000;}
.sb{background:rgba(100,0,0,0.12);border:1px solid rgba(200,0,0,0.3);border-radius:16px;padding:28px;width:100%;max-width:540px;margin-bottom:20px;text-align:left;min-height:180px;position:relative;overflow:hidden;}
.sb::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#cc0000,transparent);animation:sc 3s linear infinite;}
@keyframes sc{from{top:0;}to{top:100%;}}
.st{color:#ccc;font-size:0.95rem;line-height:1.8;font-family:'Rajdhani';}
.ch{display:flex;flex-direction:column;gap:10px;width:100%;max-width:540px;}
.cb{background:rgba(100,0,0,0.2);border:1px solid rgba(200,0,0,0.3);color:#ccc;padding:13px 18px;border-radius:8px;cursor:pointer;font-family:'Rajdhani';font-size:0.92rem;text-align:left;transition:all 0.2s;}
.cb:hover{background:rgba(200,0,0,0.2);border-color:#cc0000;color:#fff;}
.es{display:none;padding:28px;text-align:center;}
.es h2{font-family:'Orbitron';color:#cc0000;font-size:1.4rem;margin-bottom:8px;}
.es p{color:#777;margin-bottom:18px;}
#sf{position:fixed;inset:0;background:red;opacity:0;pointer-events:none;z-index:9999;transition:opacity 0.05s;}
"""
    body = """
<div id="sf"></div>
<a href="/" class="back-btn">&larr; GERİ</a>
<div class="hw">
  <h1>&#128123; KARANLIK EV</h1>
  <div class="sub">İNTERAKTİF KORKU HİKAYESİ</div>
  <div class="hrow">
    <div class="hst">CAN: <span id="hpV">&#10084;&#10084;&#10084;</span></div>
    <div class="hst">KORKU: <span id="frV">0</span>/100</div>
    <div class="hst">BOLUM: <span id="chV">1</span>/5</div>
  </div>
  <div class="sb"><div class="st" id="stT">Yukleniyor...</div></div>
  <div class="ch" id="chB"></div>
  <div class="es" id="endS">
    <h2 id="endTit"></h2>
    <p id="endDsc"></p>
    <button class="btn btn-purple" onclick="restart()">TEKRAR OYNA</button>
  </div>
</div>
"""
    js = """
  var hp=3,fear=0,chapter=1;
  var STORY=[
    {text:"Gece yarisi eski bir eve giriyorsun. Kapi agir bir sesle kapaniyor. Uzakta bebek aglamasi duyuyorsun... Ne yaparsın?",
     choices:[{t:"Sesi takip et",n:1,xp:10,f:15},{t:"Kapiyi acmayi dene",n:2,xp:5,f:5},{t:"Telefona bak",n:3,xp:8,f:8}]},
    {text:"Merdivenden cikiyorsun. En ust odanin kapisi hafifce acik. Iceriden soguk bir ruzgar geliyor. Bebek sesi durdu.",
     choices:[{t:"Iceri giriyorsun",n:4,xp:20,f:20},{t:"Kulak kabartiyor",n:5,xp:10,f:10},{t:"Kaciyorsun",n:6,xp:5,f:5,d:0}]},
    {text:"Kapiya kosu... BOOM! Gorünmez bir guc seni geri itti. Dusuyor, korkuyorsun.",
     choices:[{t:"Tekrar kalkiyorsun",n:1,xp:15,f:15,d:1},{t:"Yerde bekliyorsun",n:7,xp:5,f:25}]},
    {text:"Telefon sarji %2. Ekranda garip mesaj: 'EVİ TERK ET'. Kim gonderdi?",
     choices:[{t:"Tekrar ariyorsun",n:8,xp:10,f:10},{t:"Feneri yakiyorsun",n:1,xp:8,f:5}]},
    {text:"Odaya giriyorsun. Karyola bos ama SICAK. Perde hareket etti...",
     choices:[{t:"Perdeyi cekiyorsun",n:9,xp:25,f:30},{t:"Disari firliyorsun",n:6,xp:10,f:10}]},
    {text:"Kulak kabartin. Fisiltı: 'Neden geldin...' Ses tam arkanda!",
     choices:[{t:"Yavascа donuyorsun",n:10,xp:30,f:35},{t:"Sprint atiyorsun",n:6,xp:10,f:15,d:1}]},
    {text:"Asagi kostun ama kapi KILITLI! Pencere var sol tarafta.",
     choices:[{t:"Pencereden cikiyorsun",n:11,xp:20,f:5},{t:"Anahtar ariyorsun",n:1,xp:15,f:20}]},
    {text:"Yerde bekliyorsun. Birsey yanina oturdu. Soguk el koluna dokunuyor...",
     choices:[{t:"Bagiriyorsun",n:12,xp:5,f:40,d:1},{t:"Hareketsiz kaliyorsun",n:13,xp:20,f:15}]},
    {text:"Hat baglandi - insan sesi degil. Gurultu, parazit, uzaktan ciglik. Telefon kapandi.",
     choices:[{t:"Feneri yakiyorsun",n:1,xp:10,f:10},{t:"Sese dogru yuruyorsun",n:4,xp:20,f:20}]},
    {text:"Perdeyi cekiyorsun - HIC BIR SEY YOK. Sonra arkadan: karyola girirladı...",
     choices:[{t:"Yuzlesiyorsun",n:14,xp:40,f:40},{t:"Gozlerini kapiyorsun",n:7,xp:5,f:20}]},
    {text:"Donuyorsun... Gozleri olmayan kiz: 'Neden bizi terk ettin?'",
     choices:[{t:"Cevap veriyorsun",n:15,xp:35,f:50},{t:"Kaciyorsun",n:6,xp:10,f:30,d:1}]},
    {text:"Pencereden atladın! Arkana bakiyorsun — bir silüet pencereden izliyor. KURTULDUN!",choices:[],win:true},
    {text:"Bagirdin ve o soguk el sıkıstı. Korku zırvede...",
     choices:[{t:"Direniyorsun",n:13,xp:10,f:5},{t:"Vazgeciyorsun",n:-1,xp:0,f:0,d:2}]},
    {text:"Sakin kaliyorsun. El cekiliyor. 'Guclusun...' fısıltisi. Kapi acıliyor!",choices:[],win:true},
    {text:"Karsi karşıya. Yuzlesme ona iyi geldi. 'Tesekkurler' deyip kayboluyor. Cikis!",choices:[],win:true,xpB:100},
    {text:"'Bilmiyorum' diyorsun. Kiz gülumsuyor — gozleri beliriyor. 'Artık biliyorsun.' KURTULDUN!",choices:[],win:true,xpB:150},
  ];
  function loadCh(idx){
    if(idx===-1||hp<=0||fear>=100){gameEnd(false);return;}
    var s=STORY[idx]; if(!s){gameEnd(false);return;}
    chapter++;
    document.getElementById('chV').innerText=Math.min(chapter,5);
    if(s.f&&s.f>20){var sf=document.getElementById('sf');sf.style.opacity='0.4';setTimeout(function(){sf.style.opacity='0';},150);}
    document.getElementById('stT').innerText=s.text;
    document.getElementById('hpV').innerText='\u2764\uFE0F'.repeat(Math.max(0,hp));
    document.getElementById('frV').innerText=fear;
    var box=document.getElementById('chB'); box.innerHTML='';
    if(s.win){gameEnd(true,s.xpB||0);return;}
    s.choices.forEach(function(c){
      var btn=document.createElement('button'); btn.className='cb'; btn.innerText=c.t;
      btn.onclick=function(){
        if(c.d) hp-=c.d;
        if(c.f) fear=Math.min(100,fear+c.f);
        if(c.xp) addXP(c.xp,'Korku');
        var hc=parseInt(localStorage.getItem('cano_horror_choice')||0)+1;
        localStorage.setItem('cano_horror_choice',hc);
        loadCh(c.n);
      };
      box.appendChild(btn);
    });
  }
  function gameEnd(win,bonus){
    document.getElementById('stT').innerText='';
    document.getElementById('chB').innerHTML='';
    var es=document.getElementById('endS'); es.style.display='block';
    if(win){
      document.getElementById('endTit').innerText='HAYATTA KALDIN!';
      document.getElementById('endDsc').innerText='Tebrikler! Korku: '+fear;
      if(bonus) addXP(bonus,'Ev Bitti');
      addXP(50,'Hayatta Kaldi');
    } else {
      document.getElementById('endTit').innerText='KARANLIGA YUTULDUN';
      document.getElementById('endDsc').innerText=fear>=100?'Korku seni yendi!':'Canın bitti!';
    }
  }
  function restart(){hp=3;fear=0;chapter=1;document.getElementById('endS').style.display='none';loadCh(0);}
  loadCh(0);
"""
    return page("HORROR", css, body, js)


# ===== MARKET =====
def store_page():
    css = """
.sw{min-height:100vh;padding:90px 20px 80px;max-width:1000px;margin:0 auto;}
h1{font-family:'Orbitron';text-align:center;font-size:clamp(1.2rem,4vw,2rem);background:linear-gradient(90deg,var(--neon-blue),var(--neon-purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px;}
.sub{color:#555;text-align:center;font-size:0.78rem;letter-spacing:3px;margin-bottom:24px;}
.bal{background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.3);border-radius:12px;padding:14px 22px;text-align:center;margin-bottom:24px;font-family:'Orbitron';}
.bal .big{font-size:1.9rem;color:var(--neon-blue);}
.bal .lbl{color:#444;font-size:0.7rem;letter-spacing:2px;}
.tabs{display:flex;gap:8px;justify-content:center;margin-bottom:20px;flex-wrap:wrap;}
.tab{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);color:#555;padding:7px 18px;border-radius:50px;cursor:pointer;font-family:'Orbitron';font-size:0.72rem;transition:all 0.2s;}
.tab.active{border-color:var(--neon-blue);color:var(--neon-blue);background:rgba(0,212,255,0.08);}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;}
.si{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);padding:22px 14px;border-radius:14px;text-align:center;transition:all 0.3s;position:relative;}
.si:hover{transform:translateY(-4px);border-color:var(--neon-blue);}
.si.owned{border-color:var(--neon-green);opacity:0.7;}
.si-ic{font-size:2.3rem;display:block;margin-bottom:8px;}
.si-nm{font-family:'Orbitron';font-size:0.82rem;margin-bottom:4px;}
.si-ds{color:#555;font-size:0.72rem;margin-bottom:12px;}
.si-pr{color:var(--neon-orange);font-family:'Orbitron';font-size:0.88rem;margin-bottom:10px;}
.ob{position:absolute;top:8px;right:8px;background:var(--neon-green);color:#000;font-size:0.58rem;font-family:'Orbitron';padding:2px 7px;border-radius:50px;}
"""
    body = """
<a href="/" class="back-btn">&larr; GERİ</a>
<div class="sw">
  <h1>MARKET</h1>
  <div class="sub">XP İLE ESYA SATIN AL</div>
  <div class="bal"><div class="big" id="balV">0</div><div class="lbl">MEVCUT XP</div></div>
  <div class="tabs">
    <div class="tab active" onclick="filt('all',this)">TUMU</div>
    <div class="tab" onclick="filt('skin',this)">SKİNLER</div>
    <div class="tab" onclick="filt('boost',this)">BOOST</div>
    <div class="tab" onclick="filt('special',this)">OZEL</div>
  </div>
  <div class="sg" id="sg"></div>
</div>
"""
    js = """
  var ITEMS=[
    {id:'gold_skin',  nm:'Altin Skin',    ic:'&#10024;',cat:'skin',   pr:500, ds:'Altin parlaklik'},
    {id:'neon_skin',  nm:'Neon Skin',     ic:'&#128161;',cat:'skin',   pr:750, ds:'Neon renk paleti'},
    {id:'dark_skin',  nm:'Karanlik Skin', ic:'&#127761;',cat:'skin',   pr:1000,ds:'Gece derinligi'},
    {id:'speed_boost',nm:'Hiz Botu',      ic:'&#9889;',  cat:'boost',  pr:1000,ds:'Arcade +20% hiz'},
    {id:'xp_boost',   nm:'XP x2',        ic:'&#128293;',cat:'boost',  pr:800, ds:'24 saat cift XP'},
    {id:'mine_boost', nm:'Maden Boost',   ic:'&#9935;',  cat:'boost',  pr:600, ds:'Stratejide +5 maden'},
    {id:'ghost_badge',nm:'Hayalet Rozeti',ic:'&#128123;',cat:'special',pr:1500,ds:'Horror bitirenlerin rozeti'},
    {id:'crown',      nm:'Kral Taci',     ic:'&#128081;',cat:'special',pr:3000,ds:'En prestijli odul'},
    {id:'crystal_key',nm:'Kristal Anahtar',ic:'&#128142;',cat:'special',pr:2000,ds:'Gizli alanlari acar'},
  ];
  var cur='all';
  function filt(c,tab){
    cur=c;
    document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active');});
    tab.classList.add('active');
    render();
  }
  function render(){
    var xp=getXP(); var owned=getItems();
    document.getElementById('balV').innerText=xp.toLocaleString();
    var g=document.getElementById('sg'); g.innerHTML='';
    ITEMS.filter(function(i){return cur==='all'||i.cat===cur;}).forEach(function(item){
      var io=owned.includes(item.id);
      var cb=xp>=item.pr&&!io;
      var d=document.createElement('div');
      d.className='si'+(io?' owned':'');
      var h='';
      if(io) h+='<div class="ob">SAHİBİSİN</div>';
      h+='<span class="si-ic">'+item.ic+'</span>';
      h+='<div class="si-nm">'+item.nm+'</div>';
      h+='<div class="si-ds">'+item.ds+'</div>';
      h+='<div class="si-pr">'+item.pr.toLocaleString()+' XP</div>';
      h+='<button class="btn btn-blue" '+(cb?'':'disabled')+' onclick="buy(\''+item.id+'\','+item.pr+')">'+(io?'ALINDI':'SATIN AL')+'</button>';
      d.innerHTML=h; g.appendChild(d);
    });
  }
  function buy(id,pr){
    var xp=getXP(); var owned=getItems();
    if(xp<pr||owned.includes(id)){showToast('XP Yetersiz!');return;}
    setXP(xp-pr); owned.push(id);
    localStorage.setItem('cano_items',JSON.stringify(owned));
    var b=parseInt(localStorage.getItem('cano_bought')||0)+1;
    localStorage.setItem('cano_bought',b);
    showToast('Satin Alindi!'); render();
  }
  render();
"""
    return page("MARKET", css, body, js)


# ===== PROFİL =====
def profil_page():
    css = """
.pw{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;}
.av{width:90px;height:90px;border-radius:50%;background:linear-gradient(135deg,var(--neon-orange),var(--neon-purple));display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin-bottom:14px;box-shadow:0 0 40px rgba(255,69,0,0.4);cursor:pointer;}
.uname{font-family:'Orbitron';font-size:1.4rem;color:#fff;margin-bottom:3px;}
.utitle{color:#444;font-size:0.75rem;letter-spacing:3px;margin-bottom:26px;}
.pg{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;width:100%;max-width:560px;margin-bottom:22px;}
.pc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);padding:18px 10px;border-radius:14px;text-align:center;}
.pc .v{font-family:'Orbitron';font-size:1.3rem;color:var(--neon-orange);}
.pc .l{font-size:0.65rem;color:#444;letter-spacing:2px;margin-top:3px;}
.xpbw{width:100%;max-width:560px;margin-bottom:22px;}
.xpbl{display:flex;justify-content:space-between;font-size:0.7rem;color:#444;margin-bottom:5px;font-family:'Orbitron';}
.xpbb{background:#111;border-radius:50px;height:8px;overflow:hidden;}
.xpbf{height:100%;border-radius:50px;background:linear-gradient(90deg,var(--neon-orange),var(--neon-purple));transition:width 0.6s;}
.its{width:100%;max-width:560px;}
.its h3{font-family:'Orbitron';font-size:0.78rem;color:#444;letter-spacing:2px;margin-bottom:10px;}
.irow{display:flex;gap:8px;flex-wrap:wrap;}
.it{background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);padding:6px 14px;border-radius:8px;font-size:0.75rem;color:var(--neon-blue);}
.nm-modal{position:fixed;inset:0;background:rgba(0,0,0,0.92);display:flex;align-items:center;justify-content:center;z-index:9999;}
.nm-box{background:#111;border:1px solid var(--neon-orange);border-radius:16px;padding:36px;text-align:center;max-width:380px;width:90%;}
.nm-box h2{font-family:'Orbitron';color:var(--neon-orange);margin-bottom:18px;}
.nm-inp{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);color:#fff;padding:11px 18px;border-radius:8px;font-family:'Orbitron';font-size:0.95rem;width:100%;margin-bottom:14px;outline:none;text-align:center;}
.nm-inp:focus{border-color:var(--neon-orange);}
"""
    body = """
<a href="/" class="back-btn">&larr; GERİ</a>
<div id="nmModal" class="nm-modal" style="display:none">
  <div class="nm-box">
    <h2>KULLANICI ADINI GİR</h2>
    <input id="nmInp" class="nm-inp" maxlength="16" placeholder="ADINIZ...">
    <button class="btn" onclick="saveName()">KAYDET</button>
  </div>
</div>
<div class="pw">
  <div class="av" onclick="changeName()">&#128100;</div>
  <div class="uname" id="pName">İSİMSİZ</div>
  <div class="utitle" id="pTitle">ACEMİ</div>
  <div class="pg">
    <div class="pc"><div class="v" id="pXP">0</div><div class="l">TOPLAM XP</div></div>
    <div class="pc"><div class="v" id="pLv">1</div><div class="l">SEVİYE</div></div>
    <div class="pc"><div class="v" id="pIt">0</div><div class="l">EŞYA</div></div>
  </div>
  <div class="xpbw">
    <div class="xpbl"><span id="xpBL">0 / 500 XP</span><span id="xpBN">SEV 2</span></div>
    <div class="xpbb"><div class="xpbf" id="xpBF" style="width:0%"></div></div>
  </div>
  <div class="its">
    <h3>SAHİP OLUNAN EŞYALAR</h3>
    <div class="irow" id="iRow"></div>
  </div>
</div>
"""
    js = """
  var INAMES={
    'gold_skin':'Altin Skin &#10024;','neon_skin':'Neon Skin &#128161;',
    'dark_skin':'Karanlik Skin &#127761;','speed_boost':'Hiz Botu &#9889;',
    'xp_boost':'XP x2 &#128293;','mine_boost':'Maden Boost &#9935;',
    'ghost_badge':'Hayalet Rozeti &#128123;','crown':'Kral Taci &#128081;',
    'crystal_key':'Kristal Anahtar &#128142;'
  };
  var TITLES=[[0,'ACEMİ'],[500,'GEZGİN'],[1000,'SAVAŞÇI'],[2500,'EFSANE'],[5000,'TANRI']];
  function getTitle(xp){var t=TITLES[0][1];for(var i=0;i<TITLES.length;i++){if(xp>=TITLES[i][0])t=TITLES[i][1];}return t;}
  function renderP(){
    var xp=getXP(); var items=getItems(); var lv=Math.floor(xp/500+1);
    var nm=localStorage.getItem('cano_name')||'';
    document.getElementById('pName').innerText=nm||'İSİMSİZ';
    document.getElementById('pTitle').innerText=getTitle(xp);
    document.getElementById('pXP').innerText=xp.toLocaleString();
    document.getElementById('pLv').innerText=lv;
    document.getElementById('pIt').innerText=items.length;
    document.getElementById('xpBF').style.width=Math.min(100,(xp%500)/500*100)+'%';
    document.getElementById('xpBL').innerText=(xp%500)+' / 500 XP';
    document.getElementById('xpBN').innerText='SEV '+(lv+1);
    var ir=document.getElementById('iRow'); ir.innerHTML='';
    if(!items.length){ir.innerHTML='<span style="color:#333;font-size:0.78rem;">Henuz esya yok</span>';}
    else{items.forEach(function(id){var s=document.createElement('span');s.className='it';s.innerHTML=INAMES[id]||id;ir.appendChild(s);});}
    updateXPDisplay();
  }
  function saveName(){
    var v=document.getElementById('nmInp').value.trim();
    if(!v) return;
    localStorage.setItem('cano_name',v.toUpperCase());
    document.getElementById('nmModal').style.display='none';
    renderP();
  }
  function changeName(){document.getElementById('nmInp').value=localStorage.getItem('cano_name')||'';document.getElementById('nmModal').style.display='flex';}
  if(!localStorage.getItem('cano_name')) document.getElementById('nmModal').style.display='flex';
  renderP();
  // XP'yi sunucuya kaydet (leaderboard için)
  var nm = localStorage.getItem("cano_name");
  var xpVal = getXP();
  if(nm && xpVal > 0) {
    fetch("/xp-kaydet", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({name: nm, xp: xpVal})
    });
  }
"""
    return page("PROFİL", css, body, js)

# ===== GÜNLÜK GÖREVLER =====
def gorevler_page():
    css = """
.gw{min-height:100vh;padding:90px 20px 80px;max-width:680px;margin:0 auto;}
h1{font-family:'Orbitron';text-align:center;font-size:clamp(1.2rem,4vw,2rem);color:var(--neon-green);margin-bottom:4px;}
.sub{color:#444;text-align:center;font-size:0.78rem;letter-spacing:3px;margin-bottom:12px;}
.timer{text-align:center;font-family:'Orbitron';font-size:0.72rem;color:#333;margin-bottom:22px;}
.timer span{color:var(--neon-green);}
.gl{display:flex;flex-direction:column;gap:12px;}
.gc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:18px;display:flex;align-items:center;gap:14px;transition:all 0.3s;}
.gc.done{border-color:var(--neon-green);opacity:0.6;}
.gi{font-size:1.8rem;min-width:40px;text-align:center;}
.ginfo{flex:1;}
.gn{font-family:'Orbitron';font-size:0.82rem;margin-bottom:3px;}
.gd{font-size:0.75rem;color:#555;margin-bottom:7px;}
.gpb{background:#111;border-radius:50px;height:5px;overflow:hidden;}
.gpf{height:100%;border-radius:50px;background:linear-gradient(90deg,var(--neon-green),var(--neon-blue));transition:width 0.4s;}
.gpc{font-size:0.65rem;color:#333;margin-top:3px;}
.gr{font-family:'Orbitron';font-size:0.78rem;color:var(--neon-orange);min-width:65px;text-align:right;}
.gc.done .gr{color:var(--neon-green);}
"""
    body = """
<a href="/" class="back-btn">&larr; GERİ</a>
<div class="gw">
  <h1>GÜNLÜK GÖREVLER</h1>
  <div class="sub">HER GÜN YENİLENİR</div>
  <div class="timer">Yenileme: <span id="timer">--:--:--</span></div>
  <div class="gl" id="gl"></div>
</div>
"""
    js = """
  var GOREVLER=[
    {id:'mine10',  ic:'&#9935;',  nm:'MADENCİ',     ds:'Stratejide 10 maden cikart', h:10, xp:50,  k:'cano_maden'},
    {id:'kill20',  ic:'&#128165;',nm:'AVCI',         ds:'Arcadede 20 dusман vur',     h:20, xp:75,  k:'cano_kill'},
    {id:'story3',  ic:'&#128123;',nm:'KORKUSUZ',     ds:'Horrorda 3 karar ver',        h:3,  xp:60,  k:'cano_horror_choice'},
    {id:'buy1',    ic:'&#128722;',nm:'ALISVERİŞÇİ',  ds:'Marketten 1 esya al',         h:1,  xp:40,  k:'cano_bought'},
    {id:'xp500',   ic:'&#11088;', nm:'XP AVCISI',   ds:'Toplam 500 XP kazan',         h:500,xp:100, k:'cano_xp'},
  ];
  function getDayKey(){var d=new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();}
  function getDone(){return JSON.parse(localStorage.getItem('cano_done_'+getDayKey()))||[];}
  function markDone(id){var k='cano_done_'+getDayKey();var d=getDone();if(!d.includes(id)){d.push(id);localStorage.setItem(k,JSON.stringify(d));}}
  function renderG(){
    var done=getDone();
    var gl=document.getElementById('gl'); gl.innerHTML='';
    GOREVLER.forEach(function(g){
      var isDone=done.includes(g.id);
      var cur=parseInt(localStorage.getItem(g.k))||0;
      var prog=Math.min(g.h,cur);
      var pct=Math.min(100,(prog/g.h)*100);
      if(!isDone&&prog>=g.h){markDone(g.id);setXP(getXP()+g.xp);showToast('+'+g.xp+' XP — '+g.nm+' tamam!');isDone=true;}
      var c=document.createElement('div'); c.className='gc'+(isDone?' done':'');
      c.innerHTML='<div class="gi">'+g.ic+'</div><div class="ginfo"><div class="gn">'+g.nm+'</div><div class="gd">'+g.ds+'</div><div class="gpb"><div class="gpf" style="width:'+pct+'%"></div></div><div class="gpc">'+prog+' / '+g.h+'</div></div><div class="gr">'+(isDone?'&#10003; TAMAM':'+'+g.xp+' XP')+'</div>';
      gl.appendChild(c);
    });
    var now=new Date(); var mn=new Date(now); mn.setHours(24,0,0,0);
    var diff=Math.floor((mn-now)/1000);
    var h=Math.floor(diff/3600),m=Math.floor((diff%3600)/60),s=diff%60;
    var ti=document.getElementById('timer');
    if(ti) ti.innerText=h+'s '+m+'d '+s+'sn';
  }
  renderG();
  setInterval(renderG,1000);
"""
    return page("GÖREVLER", css, body, js)

# ===== FLASK ROTALAR =====
@app.route("/")
def home():
    a = load_anons()
    if a.get("maintenance"):
        return "<html><body style='background:#050505;color:#fff;font-family:Orbitron,monospace;display:flex;align-items:center;justify-content:center;height:100vh;flex-direction:column;gap:12px;'><div style='font-size:2rem;color:#ff4500;'>BAKIM MODU</div><div style='color:#444;font-size:0.85rem;letter-spacing:3px;'>Site gecici olarak kapali. Yakinda donuyoruz!</div></body></html>"
    track("anasayfa")
    return ana_sayfa()

@app.route("/strateji")
def strateji(): track("strateji"); return strateji_page()

@app.route("/neon-arcade")
def arcade(): track("arcade"); return arcade_page()

@app.route("/neon-rush")
def neonrush(): track("neonrush"); return neonrush_page()

@app.route("/isinlanma")
def isinlanma(): track("isinlanma"); return isinlanma_page()

@app.route("/horror")
def horror(): track("horror"); return horror_page()

@app.route("/store")
def store(): track("market"); return store_page()

@app.route("/profil")
def profil(): track("profil"); return profil_page()

@app.route("/gorevler")
def gorevler(): track("gorevler"); return gorevler_page()

@app.route("/yorumlar")
def yorumlar():
    track("yorumlar")
    yorumlar_list = load_yorumlar()
    anons = load_anons()
    anons_html = ""
    if anons.get("active") and anons.get("text"):
        anons_html = f"<div style=\"position:fixed;top:70px;left:50%;transform:translateX(-50%);background:rgba(255,69,0,0.15);border:1px solid var(--neon-orange);padding:10px 24px;border-radius:50px;z-index:999;font-family:Orbitron,sans-serif;font-size:0.75rem;color:#ff4500;\">&#128226; {anons['text']}</div>"

    card_parts = []
    for y in reversed(yorumlar_list):
        stars = "&#11088;" * y.get("puan", 5)
        card_parts.append(
            "<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);"
            "border-radius:14px;padding:20px;margin-bottom:14px;'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:8px;'>"
            "<span style='font-family:Orbitron,sans-serif;font-size:0.82rem;color:#fff;'>" + y["isim"] + "</span>"
            "<span style='font-size:0.8rem;'>" + stars + "</span></div>"
            "<div style='color:#aaa;font-size:0.9rem;line-height:1.6;'>" + y["metin"] + "</div>"
            "<div style='color:#333;font-size:0.65rem;margin-top:8px;font-family:Orbitron,sans-serif;'>" + y["tarih"] + "</div>"
            "</div>"
        )
    cards = "".join(card_parts)
    if not cards:
        cards = "<div style='color:#333;text-align:center;font-family:Orbitron,sans-serif;font-size:0.8rem;padding:40px;'>Henuz yorum yok. İlk sen yaz!</div>"

    css = (
        ".yw{min-height:100vh;padding:90px 20px 80px;max-width:680px;margin:0 auto;}"
        "h1{font-family:Orbitron,sans-serif;text-align:center;font-size:clamp(1.2rem,4vw,2rem);"
        "color:var(--neon-purple);margin-bottom:6px;}"
        ".sub{color:#444;text-align:center;font-size:0.78rem;letter-spacing:3px;margin-bottom:24px;}"
        ".form-box{background:rgba(191,0,255,0.07);border:1px solid rgba(191,0,255,0.25);"
        "border-radius:14px;padding:22px;margin-bottom:28px;}"
        ".form-box h3{font-family:Orbitron,sans-serif;font-size:0.8rem;color:var(--neon-purple);margin-bottom:14px;}"
        ".inp{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);"
        "color:#fff;padding:10px 16px;border-radius:8px;font-family:Rajdhani,sans-serif;"
        "font-size:0.95rem;width:100%;margin-bottom:10px;outline:none;}"
        ".inp:focus{border-color:var(--neon-purple);}"
        "textarea.inp{min-height:90px;resize:vertical;}"
        ".stars{display:flex;gap:8px;margin-bottom:12px;}"
        ".star{font-size:1.4rem;cursor:pointer;opacity:0.3;transition:opacity 0.2s;}"
        ".star.on{opacity:1;}"
        "#charCount{font-size:0.65rem;color:#444;text-align:right;margin-top:-6px;margin-bottom:10px;}"
    )

    body = f"""
{anons_html}
<a href="/" class="back-btn">&larr; GERİ</a>
<div class="yw">
  <h1>&#128172; ZİYARETÇİ YORUMLARI</h1>
  <div class="sub">DENEYİMİNİ PAYLAŞ</div>
  <div class="form-box">
    <h3>YENİ YORUM YAZ</h3>
    <input id="yIsim" class="inp" maxlength="20" placeholder="İsmin...">
    <div class="stars" id="stars">
      <span class="star on" data-v="1">&#11088;</span>
      <span class="star on" data-v="2">&#11088;</span>
      <span class="star on" data-v="3">&#11088;</span>
      <span class="star on" data-v="4">&#11088;</span>
      <span class="star on" data-v="5">&#11088;</span>
    </div>
    <textarea id="yMetin" class="inp" maxlength="300" placeholder="Yorumun..." oninput="document.getElementById('charCount').innerText=this.value.length+'/300'"></textarea>
    <div id="charCount">0/300</div>
    <button class="btn btn-purple" onclick="submitYorum()">YORUM GÖNDER</button>
  </div>
  <div id="yorumCards">{cards}</div>
</div>
"""
    js = """
  var puan = 5;
  document.querySelectorAll(".star").forEach(function(s) {
    s.onclick = function() {
      puan = parseInt(this.getAttribute("data-v"));
      document.querySelectorAll(".star").forEach(function(st, i) {
        st.className = "star" + (i < puan ? " on" : "");
      });
    };
  });
  function submitYorum() {
    var isim = document.getElementById("yIsim").value.trim();
    var metin = document.getElementById("yMetin").value.trim();
    if(!isim || !metin) { showToast("Isim ve yorum gerekli!"); return; }
    fetch("/yorum-gonder", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({isim: isim, metin: metin, puan: puan})
    }).then(function(r) { return r.json(); })
      .then(function(d) {
        if(d.ok) { showToast("Yorum gonderildi!"); setTimeout(function(){location.reload();}, 1000); }
        else showToast("Hata: " + d.error);
      });
  }
"""
    return page("YORUMLAR", css, body, js)

@app.route("/yorum-gonder", methods=["POST"])
def yorum_gonder():
    from flask import jsonify
    data = request.get_json()
    isim = (data.get("isim") or "").strip()[:20]
    metin = (data.get("metin") or "").strip()[:300]
    puan = max(1, min(5, int(data.get("puan", 5))))
    if not isim or not metin:
        return jsonify({"ok": False, "error": "Bos alan"})
    ok = save_yorum(isim, metin, puan)
    return jsonify({"ok": ok})

@app.route("/xp-kaydet", methods=["POST"])
def xp_kaydet():
    from flask import jsonify
    data = request.get_json()
    name = (data.get("name") or "").strip()[:16]
    xp = int(data.get("xp", 0))
    if name and xp > 0:
        update_xp(name, xp)
    return jsonify({"ok": True})

@app.route("/admin", methods=["GET", "POST"])
def admin():
    from flask import jsonify
    pw = request.args.get("pw", "")
    if pw != ADMIN_PASSWORD:
        return (
            "<html><body style='background:#050505;color:#fff;font-family:monospace;"
            "display:flex;align-items:center;justify-content:center;height:100vh;"
            "flex-direction:column;gap:16px;'>"
            "<div style='font-size:1.3rem;color:#ff4500;font-family:Orbitron,monospace;'>CANO STUDIO ADMIN</div>"
            "<form method='get'>"
            "<input name='pw' type='password' placeholder='Sifre...' "
            "style='background:#111;border:1px solid #333;color:#fff;padding:10px 16px;"
            "border-radius:8px;font-size:1rem;outline:none;'>"
            "<button type='submit' style='background:#ff4500;border:none;color:#fff;"
            "padding:10px 18px;border-radius:8px;cursor:pointer;margin-left:8px;'>GİRİŞ</button>"
            "</form></body></html>"
        )

    # POST işlemleri
    if request.method == "POST":
        action = request.form.get("action")
        if action == "anons":
            a = load_anons()
            a["text"] = request.form.get("text", "")
            a["active"] = request.form.get("active") == "1"
            save_anons(a)
        elif action == "maintenance":
            a = load_anons()
            a["maintenance"] = not a.get("maintenance", False)
            save_anons(a)
        elif action == "del_yorum":
            yid = request.form.get("yid", -1)
            del_yorum(yid)

    s = load_stats()
    anons = load_anons()
    yorumlar = load_yorumlar()
    xp_scores = load_xp()
    today = str(date.today())
    month = today[:7]


    days7 = []
    for i in range(6, -1, -1):
        
        d = str(date.today() - timedelta(days=i))
        days7.append({"d": d[5:], "v": s["daily"].get(d, 0)})
    max7 = max([d["v"] for d in days7] + [1])

    months6 = []
    
    for i in range(5, -1, -1):
        m_date = date.today().replace(day=1)
        for _ in range(i):
            m_date = (m_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        mk = str(m_date)[:7]
        months6.append({"m": mk[5:], "v": s["monthly"].get(mk, 0)})
    max6 = max([m["v"] for m in months6] + [1])

    bars7 = "".join(
        "<div style='display:flex;flex-direction:column;align-items:center;gap:3px;flex:1;'>"
        f"<div style='font-size:0.62rem;color:#ff4500;'>{d['v']}</div>"
        f"<div style='width:100%;background:#ff4500;border-radius:3px 3px 0 0;height:{max(3,int(d['v']/max7*80))}px;'></div>"
        f"<div style='font-size:0.58rem;color:#333;'>{d['d']}</div></div>"
        for d in days7
    )
    bars6 = "".join(
        "<div style='display:flex;flex-direction:column;align-items:center;gap:3px;flex:1;'>"
        f"<div style='font-size:0.62rem;color:#00d4ff;'>{m['v']}</div>"
        f"<div style='width:100%;background:#00d4ff;border-radius:3px 3px 0 0;height:{max(3,int(m['v']/max6*80))}px;'></div>"
        f"<div style='font-size:0.58rem;color:#333;'>{m['m']}</div></div>"
        for m in months6
    )

    pages_html = "".join(
        f"<div style='display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #111;'>"
        f"<span style='color:#888;'>{pg}</span>"
        f"<span style='color:#ff4500;font-family:Orbitron,monospace;'>{cnt}</span></div>"
        for pg, cnt in sorted(s["pages"].items(), key=lambda x: -x[1])
    )

    xp_html = "".join(
        f"<div style='display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #111;'>"
        f"<div style='display:flex;align-items:center;gap:10px;'>"
        f"<span style='font-family:Orbitron,monospace;font-size:0.7rem;color:#444;'>#{i+1}</span>"
        f"<span style='color:#fff;'>{sc['name']}</span></div>"
        f"<span style='color:#ff4500;font-family:Orbitron,monospace;'>{sc['xp']:,} XP</span></div>"
        for i, sc in enumerate(xp_scores[:20])
    ) or "<div style='color:#333;font-size:0.78rem;padding:12px 0;'>Henuz kayit yok.</div>"

    yorum_parts = []
    for i, y in enumerate(reversed(yorumlar)):
        stars = "&#11088;" * y.get("puan", 5)
        yorum_parts.append(
            "<div style='background:#0d0d0d;border:1px solid #1a1a1a;border-radius:10px;padding:14px;margin-bottom:10px;'>"
            "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;'>"
            "<span style='font-family:Orbitron,monospace;font-size:0.78rem;color:#fff;'>" + y["isim"] + "</span>"
            "<div style='display:flex;align-items:center;gap:8px;'>"
            "<span style='font-size:0.75rem;color:#555;'>" + y["tarih"] + "</span>"
            "<form method='post' action='/admin?pw=" + pw + "' style='display:inline;'>"
            "<input type='hidden' name='action' value='del_yorum'>"
            "<input type='hidden' name='idx' value='" + str(i) + "'>"
            "<button type='submit' style='background:#cc0000;border:none;color:#fff;padding:3px 10px;border-radius:6px;cursor:pointer;font-size:0.65rem;'>SIL</button>"
            "</form></div></div>"
            "<div style='color:#aaa;font-size:0.88rem;'>" + y["metin"] + "</div>"
            "<div style='color:#444;font-size:0.65rem;margin-top:4px;'>" + stars + "</div>"
            "</div>"
        )
    yorum_html = "".join(yorum_parts) if yorum_parts else "<div style='color:#333;font-size:0.78rem;padding:12px 0;'>Henuz yorum yok.</div>"

    maint_color = "#cc0000" if anons.get("maintenance") else "#1a1a1a"
    maint_text = "BAKIMI KAPAT" if anons.get("maintenance") else "BAKIMA AL"
    anons_checked = "checked" if anons.get("active") else ""

    css = (
        "*{margin:0;padding:0;box-sizing:border-box;}"
        "body{background:#050505;color:#fff;font-family:Rajdhani,sans-serif;padding:24px 16px;max-width:900px;margin:0 auto;}"
        ".logo{font-family:Orbitron,monospace;font-size:1.3rem;color:#ff4500;margin-bottom:4px;}"
        ".sub{color:#333;font-size:0.72rem;letter-spacing:2px;margin-bottom:24px;}"
        ".cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:20px;}"
        ".card{background:#0a0a0a;border:1px solid #1a1a1a;border-radius:12px;padding:16px;text-align:center;}"
        ".v{font-family:Orbitron,monospace;font-size:1.6rem;color:#ff4500;}"
        ".vb{color:#00d4ff;}.vg{color:#00ff88;}.vp{color:#bf00ff;}"
        ".l{font-size:0.62rem;color:#333;letter-spacing:2px;margin-top:3px;}"
        ".sec{background:#0a0a0a;border:1px solid #1a1a1a;border-radius:12px;padding:16px;margin-bottom:14px;}"
        ".sec h3{font-family:Orbitron,monospace;font-size:0.75rem;color:#444;letter-spacing:2px;margin-bottom:12px;}"
        ".bars{display:flex;align-items:flex-end;gap:5px;height:88px;}"
        ".inp{background:#111;border:1px solid #222;color:#fff;padding:9px 14px;border-radius:8px;font-family:Rajdhani,sans-serif;font-size:0.92rem;width:100%;margin-bottom:10px;outline:none;}"
        ".inp:focus{border-color:#ff4500;}"
        ".btn-a{background:#ff4500;border:none;color:#fff;padding:9px 20px;border-radius:8px;cursor:pointer;font-family:Orbitron,monospace;font-size:0.72rem;margin-right:8px;}"
        ".btn-m{border:none;color:#fff;padding:9px 20px;border-radius:8px;cursor:pointer;font-family:Orbitron,monospace;font-size:0.72rem;}"
        ".tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;}"
        ".tab{background:#111;border:1px solid #1a1a1a;color:#555;padding:6px 16px;border-radius:50px;cursor:pointer;font-family:Orbitron,monospace;font-size:0.68rem;transition:all 0.2s;}"
        ".tab.active{border-color:#ff4500;color:#ff4500;}"
        ".panel{display:none;}.panel.active{display:block;}"
        ".back{display:inline-block;margin-top:16px;color:#333;text-decoration:none;font-family:Orbitron,monospace;font-size:0.68rem;border:1px solid #1a1a1a;padding:7px 16px;border-radius:50px;}"
    )

    html = (
        "<!DOCTYPE html><html><head>"
        "<meta charset=\'UTF-8\'>"
        "<meta name=\'viewport\' content=\'width=device-width,initial-scale=1.0\'>"
        "<title>Admin | Cano Studio</title>"
        "<style>" + css + "</style></head><body>"
        "<div class=\'logo\'>CANO STUDIO ADMIN</div>"
        "<div class=\'sub\'>YONETİM PANELİ</div>"
        "<div class=\'cards\'>"
        "<div class=\'card\'><div class=\'v\'>" + str(s["total"]) + "</div><div class=\'l\'>TOPLAM ZİYARET</div></div>"
        "<div class=\'card\'><div class=\'v vb\'>" + str(s["daily"].get(today,0)) + "</div><div class=\'l\'>BUGÜN</div></div>"
        "<div class=\'card\'><div class=\'v vg\'>" + str(s["monthly"].get(month,0)) + "</div><div class=\'l\'>BU AY</div></div>"
        "<div class=\'card\'><div class=\'v vp\'>" + str(len(yorumlar)) + "</div><div class=\'l\'>YORUM</div></div>"
        "</div>"
        "<div class=\'tabs\'>"
        "<div class=\'tab active\' onclick=\'showTab(&#34;istatistik&#34;,this)\'>İSTATİSTİK</div>"
        "<div class=\'tab\' onclick=\'showTab(&#34;anons&#34;,this)\'>ANONS</div>"
        "<div class=\'tab\' onclick=\'showTab(&#34;yorumlar&#34;,this)\'>YORUMLAR</div>"
        "<div class=\'tab\' onclick=\'showTab(&#34;xp&#34;,this)\'>XP SIRALAMA</div>"
        "</div>"
        "<div id=\'istatistik\' class=\'panel active\'>"
        "<div class=\'sec\'><h3>SON 7 GÜN</h3><div class=\'bars\'>" + bars7 + "</div></div>"
        "<div class=\'sec\'><h3>SON 6 AY</h3><div class=\'bars\'>" + bars6 + "</div></div>"
        "<div class=\'sec\'><h3>SAYFA ZİYARETLERİ</h3>" + pages_html + "</div>"
        "</div>"
        "<div id=\'anons\' class=\'panel\'>"
        "<div class=\'sec\'><h3>DUYURU YAYINLA</h3>"
        "<form method=\'post\' action=\'/admin?pw=" + pw + "\'>"
        "<input type=\'hidden\' name=\'action\' value=\'anons\'>"
        "<input name=\'text\' class=\'inp\' placeholder=\'Duyuru metni...\' value=\'" + anons.get("text","") + "\'>"
        "<label style=\'display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:0.85rem;color:#888;\'>"
        "<input type=\'checkbox\' name=\'active\' value=\'1\' " + anons_checked + "> Duyuruyu aktif et</label>"
        "<button type=\'submit\' class=\'btn-a\'>KAYDET</button></form></div>"
        "<div class=\'sec\'><h3>BAKIM MODU</h3>"
        "<div style=\'color:#888;font-size:0.85rem;margin-bottom:12px;\'>Aktifken ana sayfa bakim mesaji gosterir.</div>"
        "<form method=\'post\' action=\'/admin?pw=" + pw + "\'>"
        "<input type=\'hidden\' name=\'action\' value=\'maintenance\'>"
        "<button type=\'submit\' class=\'btn-m\' style=\'background:" + maint_color + ";\'>"+maint_text+"</button>"
        "</form></div></div>"
        "<div id=\'yorumlar\' class=\'panel\'>"
        "<div class=\'sec\'><h3>ZİYARETÇİ YORUMLARI (" + str(len(yorumlar)) + ")</h3>"
        "<form method=\'post\' action=\'/admin?pw=" + pw + "\'>" + yorum_html + "</form></div></div>"
        "<div id=\'xp\' class=\'panel\'>"
        "<div class=\'sec\'><h3>XP SIRALAMASI (İLK 20)</h3>" + xp_html + "</div></div>"
        "<a href=\'/\' class=\'back\'>&larr; ANASAYFA</a>"
        "<script>"
        "function showTab(id,el){"
        "var ps=document.querySelectorAll(\'.panel\');"
        "for(var i=0;i<ps.length;i++)ps[i].classList.remove(\'active\');"
        "var ts=document.querySelectorAll(\'.tab\');"
        "for(var i=0;i<ts.length;i++)ts[i].classList.remove(\'active\');"
        "document.getElementById(id).classList.add(\'active\');"
        "el.classList.add(\'active\');}"
        "</script></body></html>"
    )
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
