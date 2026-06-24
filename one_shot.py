"""One-shot: read clean, modify in memory, write once, build once."""
import subprocess as sp, os

C = open('build-final.py','r',encoding='utf-8').read()

# ===== 1. ENTRANCE =====
old_ent = 'var entranceEl=document.getElementById("entrance");if(entranceEl){setTimeout(function(){entranceEl.classList.add("out")},2200);entranceEl.addEventListener("click",function(){entranceEl.classList.add("out")})}'
new_ent = 'var _e=document.getElementById("entrance");if(_e){(function(){try{var _v=sessionStorage.getItem("_rv");if(_v){_e.classList.add("out");_e.style.display="none";return}}catch(_x){}setTimeout(function(){_e.classList.add("out")},2200);_e.addEventListener("click",function(){_e.classList.add("out")});try{sessionStorage.setItem("_rv","1")}catch(_x){}})()}'
assert old_ent in C, "OLD ENTRANCE NOT FOUND"
C = C.replace(old_ent, new_ent)

# ===== 2. CARD LINKS =====
old_div = '<div class="frag-card" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)">'
new_div = '<a href="perfume/{en}.html" class="frag-link"><div class="frag-card" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)">'
C = C.replace(old_div, new_div)
C = C.replace("</div></div></div>'''", "</div></div></div></a>'''")

# ===== 3. SAVE BUTTON IN CARD =====
old_acc = '<p class="frag-accord"><b>Top</b> {top}<br><b>Heart</b> {heart}<br><b>Base</b> {base}</p>'
new_acc = old_acc + '<div class="fsr"><span class="fs2" data-en="{en}" data-cn="{cn}">&#9734;</span></div>'
C = C.replace(old_acc, new_acc)

# ===== 4. FAV PANEL HTML =====
old_music = '<button class="music-btn"'
new_music = '<div class="fvp" id="fvp"><button class="fvt" id="fvt">&#9733;</button><div class="fvd"><div class="fvdt">收藏</div><div class="fvdl" id="fvdl"><div class="fvde">暂无</div></div></div></div>\n' + old_music
C = C.replace(old_music, new_music)

# ===== 5. pH HTML =====
old_submit_wrap = '<div class="blend-submit-wrap"><button class="blend-submit" id="blendSubmit">降下这场雨</button></div>'
new_submit_wrap = '<div class="phw" id="phWrap"><div class="phs"><span class="phl">pH</span><div class="phb"><div class="phf" id="phBg"></div><div class="phn" id="phN"></div></div><span class="phv" id="phV">-</span></div></div>\n' + old_submit_wrap
C = C.replace(old_submit_wrap, new_submit_wrap)

# ===== 6. ALL CSS =====
css_end = C.rfind("'''", 0, C.find('\nJS = '))
all_css = '''
.frag-link,.frag-link:hover,.frag-link:visited{text-decoration:none!important;color:inherit!important;display:block}
.fsr{text-align:center;margin-top:.2rem}
.fs2{display:inline-block;font-family:"Noto Serif SC",serif;font-size:.44rem;padding:.08rem .5rem;border-radius:100px;cursor:pointer!important;pointer-events:auto!important;position:relative;z-index:20;color:var(--gold);background:rgba(184,148,62,.04);border:1px solid rgba(184,148,62,.1);transition:all .3s;letter-spacing:.04em;user-select:none}
.fs2:hover{color:var(--gold-d);border-color:var(--gold);background:rgba(184,148,62,.08)}
.fs2.sv2{color:var(--gold-d)!important;border-color:var(--gold-d)!important;background:rgba(184,148,62,.06)!important}
.fvp{position:fixed;right:1rem;bottom:5rem;z-index:200}
.fvt{width:36px;height:36px;border-radius:50%;border:1px solid rgba(184,148,62,.2);background:rgba(253,249,239,.85);backdrop-filter:blur(10px);color:var(--gold);font-size:.8rem;cursor:none;display:flex;align-items:center;justify-content:center;transition:all .3s;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.fvt:hover{background:rgba(184,148,62,.08);border-color:var(--gold)}
.fvt.on{color:var(--gold-d);border-color:var(--gold-d)}
.fvd{display:none;position:absolute;bottom:44px;right:0;width:240px;max-height:300px;overflow-y:auto;background:rgba(253,249,239,.97);backdrop-filter:blur(16px);border:1px solid rgba(184,148,62,.1);border-radius:12px;padding:.7rem;box-shadow:0 12px 40px rgba(0,0,0,.08)}
.fvp.open .fvd{display:block}
.fvdt{font-family:"Noto Serif SC",serif;font-size:.6rem;color:var(--ink);text-align:center;letter-spacing:.05em;margin-bottom:.4rem;padding-bottom:.35rem;border-bottom:1px solid rgba(184,148,62,.08)}
.fvdl{display:flex;flex-direction:column;gap:.2rem}
.fvdi{display:flex;align-items:center;justify-content:space-between;padding:.25rem .45rem;border-radius:6px;font-size:.52rem;color:var(--ink2);font-family:"Noto Serif SC",serif;transition:.2s}
.fvdi:hover{background:rgba(184,148,62,.04)}
.fvdi a{color:var(--ink2);flex:1;text-decoration:none!important}
.fvdi a:hover{color:var(--gold)}
.fvd2{width:20px;height:20px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:transparent;color:var(--ink3);font-size:.5rem;cursor:none;display:flex;align-items:center;justify-content:center}
.fvd2:hover{color:#c0392b}
.fvde{text-align:center;font-size:.48rem;color:var(--ink3);opacity:.45;padding:.6rem 0}
.phw{display:flex;justify-content:center;padding:.4rem 0;transition:opacity .5s}
.phs{display:flex;align-items:center;gap:.5rem;padding:.25rem .7rem;background:rgba(255,253,250,.22);border-radius:100px;border:1px solid rgba(184,148,62,.06)}
.phl{font-family:"Noto Serif SC",serif;font-size:.46rem;color:var(--ink3)}
.phb{position:relative;width:105px;height:6px;border-radius:3px;background:linear-gradient(90deg,#c0392b,#e74c3c 14%,#e67e22 28%,#f1c40f 43%,#2ecc71 50%,#27ae60 57%,#1abc9c 64%,#3498db 78%,#9b59b6)}
.phf{position:absolute;right:0;top:0;bottom:0;border-radius:0 3px 3px 0;background:rgba(253,249,239,.7);transition:width .6s ease}
.phn{position:absolute;top:-4px;width:3px;height:14px;border-radius:2px;background:var(--gold);transition:left .6s ease,background .3s}
.phv{font-family:"Noto Serif SC",serif;font-size:.58rem;font-weight:300;color:var(--gold);min-width:1.8rem;text-align:right}
'''
C = C[:css_end] + '\n' + all_css + C[css_end:]

# ===== 7. ALL JS =====
cp = C.find('console.log("%c[RAIN] Perfume as Rain %c')

# 7a. Save handler
save_js = 'document.addEventListener("click",function(e){var s=e.target.closest(".fs2");if(!s)return;e.preventDefault();e.stopPropagation();var en=s.dataset.en,cn=s.dataset.cn;var sv=JSON.parse(localStorage.getItem("_rf")||"[]");var i=sv.findIndex(function(f){return f.en===en;});if(i>=0)sv.splice(i,1);else sv.push({en:en,cn:cn});localStorage.setItem("_rf",JSON.stringify(sv));_rfA()});var _rfA=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]");var es=sv.map(function(f){return f.en;});document.querySelectorAll(".fs2").forEach(function(p){if(es.indexOf(p.dataset.en)>=0){p.classList.add("sv2");p.innerHTML="&#9733;";}else{p.classList.remove("sv2");p.innerHTML="&#9734;";}});};setTimeout(_rfA,500);'

# 7b. pH in updateDisplay
old_ud = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});\nvar cnt=Object.keys(selected).length;\nif(bottleFill){bottleFill.style.height=totalPercent+'%';}\nif(totalEl){totalEl.textContent=totalPercent+'%';}"
ph_ud = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});var cnt=Object.keys(selected).length;if(bottleFill){bottleFill.style.height=totalPercent+'%';}if(totalEl){totalEl.textContent=totalPercent+'%';}var pV=document.getElementById('phV'),pB=document.getElementById('phBg'),pN=document.getElementById('phN');if(pV&&pB&&pN&&cnt>=2){var cats={};Object.keys(selected).forEach(function(k){var c=INGREDIENTS[parseInt(k)].cat;cats[c]=(cats[c]||0)+selected[parseInt(k)];});var ks=Object.keys(cats);var vs=ks.map(function(k){return cats[k];});var a=vs.reduce(function(a,b){return a+b;},0)/vs.length;var v=vs.reduce(function(s,x){return s+Math.pow(x-a,2);},0)/vs.length;var sd=Math.sqrt(v);var ds=Math.min(1.5,ks.length/4);var bp=Math.min(1.5,sd/12);var ps=[['citrus','floral'],['floral','woody'],['citrus','woody'],['woody','resin'],['spicy','woody'],['green','floral'],['aquatic','citrus'],['floral','musk']];var pb=0;ps.forEach(function(p){if(cats[p[0]]&&cats[p[1]])pb+=.4;});var raw=7+(ds*2.5)-(bp*2.5)+pb;var ph=Math.round(Math.max(1,Math.min(14,raw))*10)/10;pV.textContent=ph.toFixed(1);var pct=(ph-1)/13*100;pB.style.width=(100-pct)+'%';pN.style.left=pct+'%';if(ph>8)pN.style.background='#9b59b6';else if(ph>6.5)pN.style.background='#2ecc71';else if(ph>5)pN.style.background='#f1c40f';else if(ph>3.5)pN.style.background='#e67e22';else pN.style.background='#e74c3c';}else if(pV){pV.textContent='-';}"
C = C.replace(old_ud, ph_ud)
C = C.replace("resultEl.classList.add('show');resultShown=true;", "resultEl.classList.add('show');resultShown=true;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='0';")
C = C.replace("resultEl.classList.remove('show');resultShown=false;", "resultEl.classList.remove('show');resultShown=false;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='1';")

# 7c. Fav panel
fv_js = 'var _fvL=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]"),el=document.getElementById("fvdl");if(!el)return;var bt=document.getElementById("fvt");if(!bt)return;if(!sv.length){el.innerHTML=\'<div class="fvde">暂无收藏</div>\';bt.classList.remove("on");return;}bt.classList.add("on");var h="";sv.forEach(function(x,i){var en=x.en.toLowerCase().replace(/&/g,"-").replace(/ /g,"-").replace(/\'/g,"");h+=\'<div class="fvdi"><a href="/perfume/\'+en+\'.html">\'+x.cn+\'</a><button class="fvd2" data-idx="\'+i+\'">x</button></div>\';});el.innerHTML=h;el.querySelectorAll(".fvd2").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();var i=parseInt(this.dataset.idx);var sv=JSON.parse(localStorage.getItem("_rf")||"[]");sv.splice(i,1);localStorage.setItem("_rf",JSON.stringify(sv));_fvL();_rfA();});});};var fvTg=document.getElementById("fvt");if(fvTg)fvTg.addEventListener("click",function(e){e.stopPropagation();document.getElementById("fvp").classList.toggle("open");_fvL();});document.addEventListener("click",function(e){if(!e.target.closest(".fvp")){var el=document.getElementById("fvp");if(el)el.classList.remove("open");}});_fvL();'

# Combine all JS
all_js_new = save_js + '\n' + fv_js + '\n'
C = C[:cp] + all_js_new + C[cp:]

# ===== BUILD =====
open('build-final.py', 'w', encoding='utf-8').write(C)
r = sp.run(['python', 'build-final.py'], capture_output=True, text=True)
if r.returncode != 0:
    # Print error with context
    lines = r.stderr.split('\n')
    for line in lines[:8]:
        print(line)
    raise SystemExit(1)

# Verify
I = open('index.html', 'rb').read()
js = I[I.find(b'<script>')+8:I.find(b'</script>')]
o = js.count(b'{')
c2 = js.count(b'}')
dec = I.decode('utf-8', 'replace')

print(f"Braces: {o} vs {c2}")
for t in ['entranceEl', '}while(0', '_e=document.getElementById("entrance")']:
    found = dec.count(t)
    if t == '_e=document.getElementById("entrance")':
        print(f"  Entrance OK: {found}x")
    elif found:
        print(f"  WARN: {t}={found}")
    else:
        print(f"  Clean: {t}")

for f in ['frag-link', 'fs2', 'fvp', 'phWrap', '_rfA', '_fvL']:
    print(f"  {'OK' if f.encode() in I else 'MISS'}: {f}")

print(f"\nSize: {os.path.getsize('index.html')} bytes")
print("DONE - ONE SHOT")
