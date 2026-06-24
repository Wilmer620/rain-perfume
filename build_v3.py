import subprocess as sp, os, re

def step(label):
    r = sp.run(['python','build-final.py'], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FAIL {label}:", r.stderr[:300])
        raise SystemExit(1)
    print(f"  OK {label}")
    return open('build-final.py','r',encoding='utf-8').read()

C = open('build-final.py','r',encoding='utf-8').read()

# ===== 1. ENTRANCE FIX =====
old_ent = "entranceEl=document.getElementById(\"entrance\");if(entranceEl){setTimeout(function(){entranceEl.classList.add(\"out\")},2200);entranceEl.addEventListener(\"click\",function(){entranceEl.classList.add(\"out\")})}"
new_ent = "do{var e=document.getElementById(\"entrance\");if(!e)break;try{var v=sessionStorage.getItem(\"_rv\");if(v){e.style.opacity=0;e.style.visibility=\"hidden\";e.style.pointerEvents=\"none\";e.classList.add(\"out\");break}}catch(x){}setTimeout(function(){e.classList.add(\"out\")},2200);e.addEventListener(\"click\",function(){e.classList.add(\"out\")});try{sessionStorage.setItem(\"_rv\",\"1\")}catch(x){}}while(0)"
C = C.replace(old_ent, new_ent)
open('build-final.py','w',encoding='utf-8').write(C)
C = step("1.Entrance")

# ===== 2. CARD LINKS + SAVE BUTTON =====
# Wrap card in <a> link
old_div = '<div class="frag-card" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)">'
new_div = '<a href="perfume/{en}.html" class="frag-link" onclick="try{{sessionStorage.setItem(\'_rv\',\'1\')}}catch(e){{}}"><div class="frag-card" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)">'
C = C.replace(old_div, new_div)

# Add save button
old_acc = '<p class="frag-accord"><b>Top</b> {top}<br><b>Heart</b> {heart}<br><b>Base</b> {base}</p>'
new_acc = old_acc + '<div class="frag-sv-row"><span class="fs" data-en="{en}" data-cn="{cn}">&#9734;</span></div>'
C = C.replace(old_acc, new_acc)

# Close </a>
old_close = '</div></div></div>\'\'\''
new_close = '</div></div></div></a>\'\'\''
count = C.count(old_close)
C = C.replace(old_close, new_close)
# Make sure we close both card() and world_card()
if C.count('</a>') < 2:
    C = C.replace('</div></div></div>\'\'\'', '</div></div></div></a>\'\'\'')

open('build-final.py','w',encoding='utf-8').write(C)
C = step("2.Card")

# ===== 3. ALL CSS =====
css_end = C.rfind("'''", 0, C.find('\nJS = '))
all_css = '''
.frag-link,.frag-link:hover,.frag-link:visited{text-decoration:none!important;color:inherit!important;display:block}
.frag-sv-row{text-align:center;margin-top:.25rem}
.fs{display:inline-block;font-family:"Noto Serif SC",serif;font-size:.44rem;padding:.08rem .5rem;border-radius:100px;cursor:pointer!important;pointer-events:auto!important;position:relative;z-index:20;color:var(--gold);background:rgba(184,148,62,.04);border:1px solid rgba(184,148,62,.1);transition:all .3s;letter-spacing:.04em;user-select:none}
.fs:hover{color:var(--gold-d);border-color:var(--gold);background:rgba(184,148,62,.08)}
.fs.done{color:var(--gold-d)!important;border-color:var(--gold-d)!important;background:rgba(184,148,62,.06)!important}
.fp{position:fixed;right:1rem;bottom:5rem;z-index:200}
.fp-t{width:36px;height:36px;border-radius:50%;border:1px solid rgba(184,148,62,.2);background:rgba(253,249,239,.85);backdrop-filter:blur(10px);color:var(--gold);font-size:.8rem;cursor:none;display:flex;align-items:center;justify-content:center;transition:all .3s;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.fp-t:hover{background:rgba(184,148,62,.08);border-color:var(--gold)}
.fp-t.on{color:var(--gold-d);border-color:var(--gold-d)}
.fp-d{display:none;position:absolute;bottom:44px;right:0;width:240px;max-height:300px;overflow-y:auto;background:rgba(253,249,239,.97);backdrop-filter:blur(16px);border:1px solid rgba(184,148,62,.1);border-radius:12px;padding:.7rem;box-shadow:0 12px 40px rgba(0,0,0,.08)}
.fp.open .fp-d{display:block}
.fp-dt{font-family:"Noto Serif SC",serif;font-size:.6rem;color:var(--ink);text-align:center;letter-spacing:.05em;margin-bottom:.4rem;padding-bottom:.35rem;border-bottom:1px solid rgba(184,148,62,.08)}
.fp-dl{display:flex;flex-direction:column;gap:.2rem}
.fp-di{display:flex;align-items:center;justify-content:space-between;padding:.25rem .45rem;border-radius:6px;font-size:.52rem;color:var(--ink2);transition:all .2s;font-family:"Noto Serif SC",serif}
.fp-di:hover{background:rgba(184,148,62,.04)}
.fp-di a{color:var(--ink2);flex:1;text-decoration:none}
.fp-di a:hover{color:var(--gold)}
.fp-dx{width:20px;height:20px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:transparent;color:var(--ink3);font-size:.5rem;cursor:none;display:flex;align-items:center;justify-content:center}.fp-dx:hover{color:#c0392b}
.fp-de{text-align:center;font-size:.48rem;color:var(--ink3);opacity:.45;padding:.6rem 0}

.ph-w{display:flex;justify-content:center;padding:.4rem 0;transition:opacity .5s}
.ph-s{display:flex;align-items:center;gap:.5rem;padding:.25rem .7rem;background:rgba(255,253,250,.22);border-radius:100px;border:1px solid rgba(184,148,62,.06)}
.ph-l{font-family:"Noto Serif SC",serif;font-size:.46rem;color:var(--ink3)}
.ph-b{position:relative;width:105px;height:6px;border-radius:3px;background:linear-gradient(90deg,#c0392b,#e74c3c 14%,#e67e22 28%,#f1c40f 43%,#2ecc71 50%,#27ae60 57%,#1abc9c 64%,#3498db 78%,#9b59b6)}
.ph-f{position:absolute;right:0;top:0;bottom:0;border-radius:0 3px 3px 0;background:rgba(253,249,239,.7);transition:width .6s ease}
.ph-n{position:absolute;top:-4px;width:3px;height:14px;border-radius:2px;background:var(--gold);transition:left .6s ease,background .3s}
.ph-v{font-family:"Noto Serif SC",serif;font-size:.58rem;font-weight:300;color:var(--gold);min-width:1.8rem;text-align:right}
'''
C = C[:css_end] + '\n' + all_css + C[css_end:]
open('build-final.py','w',encoding='utf-8').write(C)
C = step("3.CSS")

# ===== 4. HTML: pH + fav panel =====
old_sub = '<div class="blend-submit-wrap"><button class="blend-submit" id="blendSubmit">降下这场雨</button></div>'
ph_html = '<div class="ph-w" id="phWrap"><div class="ph-s"><span class="ph-l">pH</span><div class="ph-b"><div class="ph-f" id="phBg"></div><div class="ph-n" id="phN"></div></div><span class="ph-v" id="phV">-</span></div></div>\n' + old_sub
C = C.replace(old_sub, ph_html)

music_btn = '<button class="music-btn"'
fav_panel = '<div class="fp" id="fp"><button class="fp-t" id="fpT">&#9733;</button><div class="fp-d"><div class="fp-dt">我的收藏</div><div class="fp-dl" id="fpL"><div class="fp-de">暂无收藏</div></div></div></div>\n' + music_btn
C = C.replace(music_btn, fav_panel)

open('build-final.py','w',encoding='utf-8').write(C)
C = step("4.HTML")

# ===== 5. All JS at once =====
cp = C.find('console.log("%c[RAIN] Perfume as Rain %c')

# pH JS in updateDisplay
old_upd = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});\nvar cnt=Object.keys(selected).length;\nif(bottleFill){bottleFill.style.height=totalPercent+'%';}\nif(totalEl){totalEl.textContent=totalPercent+'%';}"
new_upd = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});var cnt=Object.keys(selected).length;if(bottleFill){bottleFill.style.height=totalPercent+'%';}if(totalEl){totalEl.textContent=totalPercent+'%';}var pV=document.getElementById('phV'),pB=document.getElementById('phBg'),pN=document.getElementById('phN');if(pV&&pB&&pN&&cnt>=2){var cats={};Object.keys(selected).forEach(function(k){var c=INGREDIENTS[parseInt(k)].cat;cats[c]=(cats[c]||0)+selected[parseInt(k)];});var ks=Object.keys(cats);var vs=ks.map(function(k){return cats[k];});var a=vs.reduce(function(a,b){return a+b;},0)/vs.length;var v=vs.reduce(function(s,x){return s+Math.pow(x-a,2);},0)/vs.length;var sd=Math.sqrt(v);var ds=Math.min(1.5,ks.length/4);var bp=Math.min(1.5,sd/12);var ps=[['citrus','floral'],['floral','woody'],['citrus','woody'],['woody','resin'],['spicy','woody'],['green','floral'],['aquatic','citrus'],['floral','musk']];var pb=0;ps.forEach(function(p){if(cats[p[0]]&&cats[p[1]])pb+=.4;});var raw=7+(ds*2.5)-(bp*2.5)+pb;var ph=Math.round(Math.max(1,Math.min(14,raw))*10)/10;pV.textContent=ph.toFixed(1);var pct=(ph-1)/13*100;pB.style.width=(100-pct)+'%';pN.style.left=pct+'%';if(ph>8)pN.style.background='#9b59b6';else if(ph>6.5)pN.style.background='#2ecc71';else if(ph>5)pN.style.background='#f1c40f';else if(ph>3.5)pN.style.background='#e67e22';else pN.style.background='#e74c3c';}else if(pV){pV.textContent='-';}"
C = C.replace(old_upd, new_upd)
old_sh = "resultEl.classList.add('show');resultShown=true;"
new_sh = "resultEl.classList.add('show');resultShown=true;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='0';"
C = C.replace(old_sh, new_sh)
old_hi = "resultEl.classList.remove('show');resultShown=false;"
new_hi = "resultEl.classList.remove('show');resultShown=false;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='1';"
C = C.replace(old_hi, new_hi)

# Save + fav panel JS
save_js = '''
document.addEventListener("click",function(e){
var s=e.target.closest(".fs");
if(!s)return;e.preventDefault();e.stopPropagation();
var en=s.dataset.en,cn=s.dataset.cn;
var sv=JSON.parse(localStorage.getItem("_rf")||"[]");
var i=sv.findIndex(function(f){return f.en===en;});
if(i>=0)sv.splice(i,1);else sv.push({en:en,cn:cn});
localStorage.setItem("_rf",JSON.stringify(sv));_m();_l();
});
var _m=function(){
var sv=JSON.parse(localStorage.getItem("_rf")||"[]");var es=sv.map(function(f){return f.en;});
document.querySelectorAll(".fs").forEach(function(p){if(es.indexOf(p.dataset.en)>=0){p.classList.add("done");p.innerHTML="&#9733;";}else{p.classList.remove("done");p.innerHTML="&#9734;";}});
};
setTimeout(_m,500);
(function(){
var f=document.getElementById("fp"),t=document.getElementById("fpT");
if(!f||!t)return;
t.addEventListener("click",function(e){e.stopPropagation();f.classList.toggle("open");_l();});
var _l=function(){
var sv=JSON.parse(localStorage.getItem("_rf")||"[]"),el=document.getElementById("fpL");
if(!el)return;
if(!sv.length){el.innerHTML='<div class="fp-de">暂无收藏</div>';t.classList.remove("on");return;}
t.classList.add("on");var h="";sv.forEach(function(x,i){var en=x.en.toLowerCase().replace(/&/g,"-").replace(/ /g,"-").replace(/'/g,"");h+='<div class="fp-di"><a href=\"/perfume/'+en+'.html\" onclick=\"try{sessionStorage.setItem(\\'_rv\\',\\'1\\')}catch(e){}\">'+x.cn+'</a><button class=\"fp-dx\" data-idx=\"'+i+'\">x</button></div>';});
el.innerHTML=h;el.querySelectorAll(".fp-dx").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();var i=parseInt(this.dataset.idx);var sv=JSON.parse(localStorage.getItem("_rf")||"[]");sv.splice(i,1);localStorage.setItem("_rf",JSON.stringify(sv));_l();_m();});});
};
_l();document.addEventListener("click",function(e){if(!e.target.closest(".fp"))f.classList.remove("open");});
})();
'''

C = C[:cp] + save_js + C[cp:]
open('build-final.py','w',encoding='utf-8').write(C)
C = step("5.JS")

print(f"\nFINAL: {os.path.getsize('index.html')} bytes")
for t in ['phWrap','fp','fs','frag-link','_m','_l','_rf']:
    print(f"  {'OK' if t in C else 'MISS'}: {t}")
