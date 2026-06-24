"""Comprehensive fix: add all features to clean git build-final.py."""
import subprocess as sp, os

C = open('build-final.py', 'r', encoding='utf-8').read()
changes = []

# === 1. ENTRANCE FIX ===
old_ent = 'var entranceEl=document.getElementById("entrance");if(entranceEl){setTimeout(function(){entranceEl.classList.add("out")},2200);entranceEl.addEventListener("click",function(){entranceEl.classList.add("out")})}'
new_ent = 'var _e=document.getElementById("entrance");if(_e){(function(){try{var _v=sessionStorage.getItem("_rv");if(_v){_e.classList.add("out");_e.style.display="none";return}}catch(_x){}setTimeout(function(){_e.classList.add("out")},2200);_e.addEventListener("click",function(){_e.classList.add("out")});try{sessionStorage.setItem("_rv","1")}catch(_x){}})()}'
assert old_ent in C, "ENTRANCE NOT FOUND"
C = C.replace(old_ent, new_ent)
changes.append("1.Entrance fix")

# === 2. INSERT HELPER FUNCTIONS before card() ===
card_pos = C.find('def card(num, en, cn, top, heart, base, has_img=False):')
assert card_pos > 0, "card() not found"

helpers = '''def _slug(en):
  s=en.replace('&','and').replace(' ','-').replace("'",'')
  return s.lower()

def rain_tag_for(en):
  import re as _re
  n=_NF.get(en,"")
  m=_re.search(r'rain-fall">([^<]+)</em>',n or"")
  return m.group(1)if m else""

def series_for(en):
  for sn,sd in[("驻足苦旅","sojourn"),("世界之色","world"),("灵感盛宴","feast"),("宙宇寰星","cosmos"),("四季所生","seasons"),("雨后","after")]:
    for item in NARRATIVES.get(sd,{}).get("items",[]):
      if item[0]==en:return sn
  coll={'Figment':'臻品雨酿','Adorn':'臻品雨酿','Tonight':'臻品雨酿','Entropy':'臻品雨酿','Migration':'臻品雨酿','Renew':'臻品雨酿'}
  return coll.get(en,"")

def collection_data(en):
  d={'Figment':('当归\\u00b7没药\\u00b7粉红胡椒','鸢尾\\u00b7紫罗兰\\u00b7纸莎草','檀木\\u00b7香草\\u00b7安息香'),
     'Adorn':('苦橙叶\\u00b7白松香\\u00b7粉红胡椒','土耳其玫瑰\\u00b7沉香\\u00b7番红花','皮革\\u00b7琥珀\\u00b7苏合香'),
     'Tonight':('香槟调\\u00b7杜松\\u00b7柑橘皮','鸢尾\\u00b7烟草\\u00b7黑巧克力','愈创木\\u00b7皮革\\u00b7麝香'),
     'Entropy':('醛香\\u00b7臭氧\\u00b7薄荷','鸢尾\\u00b7没药\\u00b7焚香','白麝香\\u00b7琥珀\\u00b7矿物调'),
     'Migration':('竹叶\\u00b7薄荷\\u00b7柑橘','桂花\\u00b7白茶\\u00b7紫藤','白麝香\\u00b7檀木\\u00b7米浆'),
     'Renew':('绿叶\\u00b7佛手柑\\u00b7薄荷','铃兰\\u00b7白茶\\u00b7蕨类','白麝香\\u00b7雪松\\u00b7琥珀')}
  return d.get(en,('','',''))

def collection_cn(en):
  m={'Figment':'我故臆想','Adorn':'着我之境','Tonight':'今夜唯我','Entropy':'熵增时','Migration':'新时代迁流','Renew':'致新生'}
  return m.get(en,en)

def collection_poster_tag(en):
  m={'Figment':'典藏臻酿 \\u00b7 忆中虚构','Adorn':'典藏臻酿 \\u00b7 身体美术馆','Tonight':'典藏臻酿 \\u00b7 午夜款待','Entropy':'典藏臻酿 \\u00b7 秩序散落','Migration':'典藏臻酿 \\u00b7 岁时坐标','Renew':'典藏臻酿 \\u00b7 未来首句'}
  return m.get(en,'')

def collection_series(en):
  m={'Figment':('SOJOURN','驻足苦旅'),'Adorn':('WORLD','世界之色'),'Tonight':('FEAST','灵感盛宴'),'Entropy':('COSMOS','宙宇寰星'),'Migration':('SEASONS','四季所生'),'Renew':('AFTER','雨后')}
  return m.get(en,('',''))

'''

C = C[:card_pos] + helpers + C[card_pos:]
changes.append("2.Helper functions")

# === 3. NARRATIVES FLAT (_NF) ===
# Find the end of NARRATIVES dict
ns = C.find('NARRATIVES = {')
d = 0; st = False
for i in range(ns, len(C)):
    if C[i] == '{': d += 1; st = True
    elif C[i] == '}': d -= 1
    if st and d == 0:
        ne = i + 1
        break
flat = '''
_NF={}
for _s in NARRATIVES.values():
  if isinstance(_s,dict)and"items"in _s:
    for _i in _s["items"]:
      _NF[_i[0]]=_i[2]
_NF['Figment']=_NF.get('我故臆想','')
_NF['Adorn']=_NF.get('着我之境','')
_NF['Tonight']=_NF.get('今夜唯我','')
_NF['Entropy']=_NF.get('熵增时','')
_NF['Migration']=_NF.get('新时代迁流','')
_NF['Renew']=_NF.get('致新生','')
'''
C = C[:ne] + flat + C[ne:]
changes.append("3._NF flat")

# === 4. REPLACE card() function ===
old_card_start = 'def card(num, en, cn, top, heart, base, has_img=False):'
old_card_marker = C.find(old_card_start)
# Find the end of the OLD card function (closing ''')
old_card_end = C.find("'''\n\ndef world_card(filename", old_card_marker)
assert old_card_end > 0, "card end not found"
# Include the closing ''' and newlines
old_card_end = old_card_end + 3  # length of '''
# Find next def
next_def = C.find('\ndef ', old_card_end)
old_card_full = C[old_card_marker:next_def]

new_card = '''def card(num, en, cn, top, heart, base, has_img=False):
  sn = series_for(en); rt = rain_tag_for(en)
  first_note = top.split('\\u00b7')[0].strip() if top else ''
  p = []
  p.append('<a href="perfume/'+_slug(en)+'.html" class="frag-link" onclick="try{sessionStorage.setItem(\\'_rv\\',\\'1\\')}catch(e){}"><div class="frag-card" data-en="'+en+'">')
  p.append('<div class="frag-cn">'+cn+'</div>')
  p.append('<div class="frag-en">'+en+'</div>')
  if rt: p.append('<div class="frag-rain">'+rt+'</div>')
  p.append('<div class="frag-note-type"><span class="frag-note-dot top-dot"></span>'+first_note+'调</div>')
  p.append('<div class="frag-sv"><span class="fs2" data-en="'+en+'" data-cn="'+cn+'">\\u2606</span></div>')
  p.append('</div></a>')
  return '\\n'.join(p)

'''

C = C.replace(old_card_full, new_card)
changes.append("4.card() replaced")

# === 5. REPLACE world_card() function ===
old_wc_marker = 'def world_card(filename, alt, num, en, cn, top, heart, base):\n  # These have real images with different filenames'
old_wc_start = C.find(old_wc_marker)
assert old_wc_start > 0, "world_card start not found"
old_wc_end = C.find("\ndef panel(", old_wc_start)
old_wc_full = C[old_wc_start:old_wc_end]

new_world_card = '''def world_card(filename, alt, num, en, cn, top, heart, base):
  return card(num, en, cn, top, heart, base, has_img=True)

'''

C = C.replace(old_wc_full, new_world_card)
changes.append("5.world_card() replaced")

# === 6. ADD collection_card() function ===
panel_pos = C.find('def panel(pid, cards_html, default_active=False, narrative=\'\'):')
assert panel_pos > 0, "panel() not found"

collection_func = '''def collection_card(en):
  cn = collection_cn(en); top,heart,base = collection_data(en)
  sen,scn = collection_series(en); tag = collection_poster_tag(en)
  first_note = top.split('\\u00b7')[0].strip() if top else ''
  p = []
  p.append('<a href="perfume/'+_slug(en)+'.html" class="frag-link" onclick="try{sessionStorage.setItem(\\'_rv\\',\\'1\\')}catch(e){}"><div class="frag-card collection-card-v2" data-en="'+en+'">')
  p.append('<div class="frag-cn">'+cn+'</div>')
  p.append('<div class="frag-en">'+en+'</div>')
  p.append('<div class="frag-note-type"><span class="frag-note-dot top-dot"></span>'+first_note+'调</div>')
  p.append('<div class="frag-sv"><span class="fs2" data-en="'+en+'" data-cn="'+cn+'">\\u2606</span></div>')
  p.append('</div></a>')
  return '\\n'.join(p)

'''

C = C[:panel_pos] + collection_func + C[panel_pos:]
changes.append("6.collection_card() added")

# === 7. REPLACE HARDCODED COLLECTION CARDS ===
grid_start = C.find('<div class="frag-grid reveal">\n<div class="frag-card collection-card"')
narr_btn_marker = "{narrative_btn('collection', 'Narr')}"
narr_btn_pos = C.find(narr_btn_marker, grid_start)
assert grid_start > 0, "collection grid start not found"
assert narr_btn_pos > 0, "narrative_btn not found"

close_div = C.rfind('</div>', grid_start, narr_btn_pos)
# Build new grid
new_grid_lines = ['<div class="frag-grid reveal">']
for en in ['Figment','Adorn','Tonight','Entropy','Migration','Renew']:
    new_grid_lines.append('{collection_card("' + en + '")}')
new_grid_lines.append('</div>')
new_grid = '\n'.join(new_grid_lines)

old_grid = C[grid_start:close_div]
C = C.replace(old_grid, new_grid)
changes.append("7.Collection cards replaced")

# === 8. FAV MODAL HTML ===
old_music = '<button class="music-btn"'
assert old_music in C, "music-btn not found"
fav_html = '<div class="fvp" id="fvp"><button class="fvt" id="fvt">&#9733;</button></div>\n<div class="fvm" id="fvm"><div class="fvmc"><button class="fvmx" id="fvmx">&#10799;</button><div class="fvms"><div class="fvmt">我的收藏</div><p class="fvmsub">你曾在雨中驻足的那些片刻，<br>都悄悄地留在了这里。</p><div class="fvml" id="fvml"><div class="fvme">雨中来信，静待珍藏。<br>点击卡片中的 &#9734; 即可收藏。</div></div></div></div></div>\n' + old_music
C = C.replace(old_music, fav_html)
changes.append("8.Fav modal HTML")

# === 9. pH HTML ===
old_submit = '<div class="blend-submit-wrap"><button class="blend-submit" id="blendSubmit">降下这场雨</button></div>'
assert old_submit in C, "blend-submit not found"
ph_html = '<div class="phw" id="phWrap"><div class="phs"><span class="phl">pH</span><div class="phb"><div class="phf" id="phBg"></div><div class="phn" id="phN"></div></div><span class="phv" id="phV">-</span></div></div>\n' + old_submit
C = C.replace(old_submit, ph_html)
changes.append("9.pH HTML")

# === 10. APPEND CSS (at end of existing CSS section) ===
css_end = C.rfind("'''", 0, C.find('\nJS = '))
new_css = '''
.frag-link,.frag-link:hover,.frag-link:visited{text-decoration:none!important;color:inherit!important;display:block}
.frag-card{padding:.8rem .9rem;margin-bottom:.6rem;text-align:center;background:rgba(255,253,250,.28);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(184,148,62,.05);border-radius:9px;transition:all .3s;display:flex;flex-direction:column;gap:.15rem;position:relative;overflow:hidden}
.frag-card:hover{border-color:rgba(184,148,62,.14);background:rgba(255,253,250,.44);transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.02)}
.frag-cn{font-family:"Noto Serif SC",serif;font-size:.9rem;color:var(--ink);font-weight:500;letter-spacing:.04em;line-height:1.2}
.frag-en{font-family:Inter,sans-serif;font-size:.55rem;color:var(--ink3);opacity:.38;letter-spacing:.03em}
.frag-rain{font-family:"Noto Serif SC",serif;font-size:.52rem;color:var(--gold);opacity:.42;font-style:italic;letter-spacing:.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.frag-note-type{font-family:"Noto Serif SC",serif;font-size:.5rem;color:var(--ink3);display:flex;align-items:center;justify-content:center;gap:.2rem;opacity:.48}
.frag-note-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}.top-dot{background:#d4b660}
.frag-sv{display:flex;justify-content:center}
.fs2{display:inline-block;font-family:"Noto Serif SC",serif;font-size:.44rem;padding:.04rem .4rem;border-radius:100px;cursor:pointer!important;pointer-events:auto!important;position:relative;z-index:20;color:var(--gold);background:rgba(184,148,62,.04);border:1px solid rgba(184,148,62,.08);transition:all .3s;letter-spacing:.04em;user-select:none}
.fs2:hover{color:var(--gold-d);border-color:var(--gold);background:rgba(184,148,62,.08)}
.fs2.sv2{color:var(--gold-d)!important;border-color:var(--gold-d)!important;background:rgba(184,148,62,.06)!important}
.collection-card-v2{border-color:rgba(184,148,62,.08)!important;background:rgba(255,253,250,.36)!important}
.collection-card-v2 .frag-cn{font-size:1.15rem!important}
.frag-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.8rem}
/* Hide old card elements */
.frag-card .corner,.frag-img-wrap,.frag-img,.frag-num,.frag-name-en,.frag-name-cn,.frag-accord,.poster-badge,.frag-card-inner,.frag-info,.frag-card-header,.frag-card-names,.frag-card-rain-tag,.frag-card-series,.frag-card-notes,.frag-card-collapse-btn,.frag-card-tags,.frag-card-actions,.frag-card-narrative,.frag-card .save-action,.frag-card-action,.frag-collapse,.frag-narrative,.frag-notes,.frag-meta,.frag-pill,.fsr{display:none!important}
.narr-hub,.narr-hub-title,.narr-hub-sub,.narr-hub-desc,.narr-tabs,.narr-tab,.narr-body{display:none!important}
/* Fav modal */
.fvp{position:fixed;right:2.5rem;bottom:9.5rem;z-index:200}.fvt{width:44px;height:44px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:rgba(253,249,240,.4);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);color:var(--gold);font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .4s}.fvt:hover{background:rgba(253,249,240,.55);border-color:rgba(184,148,62,.14)}.fvt.on{color:var(--gold-d);border-color:var(--gold-d)}.fvm{display:none;position:fixed;inset:0;z-index:800;align-items:center;justify-content:center;background:rgba(253,249,239,.96);backdrop-filter:blur(20px)}.fvm.open{display:flex}.fvmc{position:relative;width:92%;max-width:560px;max-height:80vh;overflow:hidden;border:1px solid rgba(184,148,62,.08);border-radius:20px;background:rgba(255,253,250,.45);backdrop-filter:blur(16px);box-shadow:0 24px 80px rgba(0,0,0,.08);animation:fvIn .4s cubic-bezier(.4,0,.2,1)}@keyframes fvIn{from{opacity:0;transform:translateY(20px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}.fvmx{position:absolute;top:.8rem;right:.8rem;z-index:3;width:32px;height:32px;border-radius:50%;border:1px solid rgba(184,148,62,.15);background:rgba(255,253,250,.7);color:var(--ink3);font-size:.9rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .3s}.fvmx:hover{background:rgba(184,148,62,.08);border-color:var(--gold);color:var(--ink);transform:rotate(90deg)}.fvms{overflow-y:auto;max-height:80vh;padding:2rem 1.8rem 2.2rem}.fvmt{font-family:"Noto Serif SC",serif;font-size:1.05rem;color:var(--ink);text-align:center;letter-spacing:.06em;font-weight:500;margin-bottom:.2rem}.fvmsub{text-align:center;font-family:"Noto Serif SC",serif;font-size:.52rem;color:var(--ink3);opacity:.45;line-height:1.8;letter-spacing:.03em;margin-bottom:1rem}.fvml{display:flex;flex-direction:column;gap:.25rem}.fvmi{display:flex;align-items:center;justify-content:space-between;padding:.35rem .55rem;border-radius:8px;font-size:.55rem;color:var(--ink2);font-family:"Noto Serif SC",serif;transition:.2s;background:rgba(255,253,250,.3);border:1px solid rgba(184,148,62,.04)}.fvmi:hover{background:rgba(184,148,62,.04);border-color:rgba(184,148,62,.1)}.fvmi a{color:var(--ink2);flex:1;text-decoration:none!important}.fvmi a:hover{color:var(--gold)}.fvm2{width:22px;height:22px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:transparent;color:var(--ink3);font-size:.5rem;cursor:pointer;display:flex;align-items:center;justify-content:center}.fvm2:hover{color:#c0392b}.fvme{text-align:center;font-size:.52rem;color:var(--ink3);opacity:.4;padding:1.2rem 0}
/* pH */
.phw{display:flex;justify-content:center;padding:.4rem 0;transition:opacity .5s}.phs{display:flex;align-items:center;gap:.5rem;padding:.25rem .7rem;background:rgba(255,253,250,.22);border-radius:100px;border:1px solid rgba(184,148,62,.06)}.phl{font-family:"Noto Serif SC",serif;font-size:.46rem;color:var(--ink3)}.phb{position:relative;width:105px;height:6px;border-radius:3px;background:linear-gradient(90deg,#c0392b,#e74c3c 14%,#e67e22 28%,#f1c40f 43%,#2ecc71 50%,#27ae60 57%,#1abc9c 64%,#3498db 78%,#9b59b6)}.phf{position:absolute;right:0;top:0;bottom:0;border-radius:0 3px 3px 0;background:rgba(253,249,239,.7);transition:width .6s ease}.phn{position:absolute;top:-4px;width:3px;height:14px;border-radius:2px;background:var(--gold);transition:left .6s ease,background .3s}.phv{font-family:"Noto Serif SC",serif;font-size:.58rem;font-weight:300;color:var(--gold);min-width:1.8rem;text-align:right}
'''
C = C[:css_end] + '\n' + new_css + C[css_end:]
changes.append("10.CSS appended")

# === 11. REMOVE NARR-HUB ===
narr_hub = C.find('<div class="narr-hub reveal">')
if narr_hub > 0:
    # Find the closing </section> after narr-hub
    next_section = C.find('<section class="section-divider', narr_hub + 50)
    if next_section > 0:
        C = C[:narr_hub] + C[next_section:]
        changes.append("11.Narr-hub removed")
    else:
        changes.append("11.Narr-hub SKIP (no next section)")
else:
    changes.append("11.Narr-hub SKIP (not found)")

# === 12. JS: save + fav + pH ===
cp = C.find('console.log("%c[RAIN] Perfume as Rain %c')
assert cp > 0, "console.log not found"

# pH in updateDisplay
old_ud = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});\nvar cnt=Object.keys(selected).length;\nif(bottleFill){bottleFill.style.height=totalPercent+'%';}\nif(totalEl){totalEl.textContent=totalPercent+'%';}"
new_ud = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});var cnt=Object.keys(selected).length;if(bottleFill){bottleFill.style.height=totalPercent+'%';}if(totalEl){totalEl.textContent=totalPercent+'%';}var pV=document.getElementById('phV'),pB=document.getElementById('phBg'),pN=document.getElementById('phN');if(pV&&pB&&pN&&cnt>=2){var cats={};Object.keys(selected).forEach(function(k){var c=INGREDIENTS[parseInt(k)].cat;cats[c]=(cats[c]||0)+selected[parseInt(k)];});var ks=Object.keys(cats);var vs=ks.map(function(k){return cats[k];});var a=vs.reduce(function(a,b){return a+b;},0)/vs.length;var v=vs.reduce(function(s,x){return s+Math.pow(x-a,2);},0)/vs.length;var sd=Math.sqrt(v);var ds=Math.min(1.5,ks.length/4);var bp=Math.min(1.5,sd/12);var ps=[['citrus','floral'],['floral','woody'],['citrus','woody'],['woody','resin'],['spicy','woody'],['green','floral'],['aquatic','citrus'],['floral','musk']];var pb=0;ps.forEach(function(p){if(cats[p[0]]&&cats[p[1]])pb+=.4;});var raw=7+(ds*2.5)-(bp*2.5)+pb;var ph=Math.round(Math.max(1,Math.min(14,raw))*10)/10;pV.textContent=ph.toFixed(1);var pct=(ph-1)/13*100;pB.style.width=(100-pct)+'%';pN.style.left=pct+'%';if(ph>8)pN.style.background='#9b59b6';else if(ph>6.5)pN.style.background='#2ecc71';else if(ph>5)pN.style.background='#f1c40f';else if(ph>3.5)pN.style.background='#e67e22';else pN.style.background='#e74c3c';}else if(pV){pV.textContent='-';}"
assert old_ud in C, "updateDisplay not found"
C = C.replace(old_ud, new_ud)
C = C.replace("resultEl.classList.add('show');resultShown=true;", "resultEl.classList.add('show');resultShown=true;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='0';")
C = C.replace("resultEl.classList.remove('show');resultShown=false;", "resultEl.classList.remove('show');resultShown=false;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='1';")
changes.append("12a.pH JS")

# Save + Fav JS
all_js = 'document.addEventListener("click",function(e){var s=e.target.closest(".fs2");if(!s)return;e.preventDefault();e.stopPropagation();var en=s.dataset.en,cn=s.dataset.cn;var sv=JSON.parse(localStorage.getItem("_rf")||"[]");var i=sv.findIndex(function(f){return f.en===en;});if(i>=0)sv.splice(i,1);else sv.push({en:en,cn:cn});localStorage.setItem("_rf",JSON.stringify(sv));_rfA()});var _rfA=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]");var es=sv.map(function(f){return f.en;});document.querySelectorAll(".fs2").forEach(function(p){if(es.indexOf(p.dataset.en)>=0){p.classList.add("sv2");p.innerHTML="\\u2605";}else{p.classList.remove("sv2");p.innerHTML="\\u2606";}});};setTimeout(_rfA,500);\nvar _fvL=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]"),el=document.getElementById("fvml");if(!el)return;var bt=document.getElementById("fvt");if(!bt)return;if(!sv.length){el.innerHTML=\'<div class="fvme">雨中来信，静待珍藏。<br>点击卡片中的 ☆ 即可收藏。</div>\';bt.classList.remove("on");return;}bt.classList.add("on");var h="";sv.forEach(function(x,i){var slug=x.en.replace(/&/g,"and").replace(/ /g,"-").replace(/\'/g,"").toLowerCase();h+=\'<div class="fvmi"><a href="/perfume/\'+slug+\'.html">\'+x.cn+\'</a><button class="fvm2" data-idx="\'+i+\'">×</button></div>\';});el.innerHTML=h;el.querySelectorAll(".fvm2").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();var i=parseInt(this.dataset.idx);var sv=JSON.parse(localStorage.getItem("_rf")||"[]");sv.splice(i,1);localStorage.setItem("_rf",JSON.stringify(sv));_fvL();_rfA();});});};var fvTg=document.getElementById("fvt");if(fvTg)fvTg.addEventListener("click",function(e){e.stopPropagation();document.getElementById("fvm").classList.add("open");_fvL();});var fvX=document.getElementById("fvmx");if(fvX)fvX.addEventListener("click",function(){document.getElementById("fvm").classList.remove("open");});var fvBg=document.getElementById("fvm");if(fvBg)fvBg.addEventListener("click",function(e){if(e.target===this)this.classList.remove("open");});_fvL();\n'
C = C[:cp] + all_js + C[cp:]
changes.append("12b.Save+Fav JS")

# Write back and build
open('build-final.py', 'w', encoding='utf-8').write(C)
print("Changes applied:")
for c in changes:
    print("  " + c)

print("\nBuilding...")
r = sp.run(['python', 'build-final.py'], capture_output=True, text=True)
if r.returncode != 0:
    print('FAIL:')
    for line in r.stderr.split('\n')[:15]:
        print(line)
    raise SystemExit(1)

I = open('index.html', 'rb').read()
js = I[I.find(b'<script>') + 8:I.find(b'</script>')]
o = js.count(b'{')
c2 = js.count(b'}')
dec = I.decode('utf-8', 'replace')

print("Braces: " + str(o) + " vs " + str(c2) + (" OK" if o == c2 else " MISMATCH!"))

for t in ['_rfA','_fvL','fvp','fvm','phWrap','frag-link','fs2',
          'figment.html','adorn.html','tonight.html','entropy.html','migration.html','renew.html',
          'collection-card-v2','frag-cn','frag-rain','frag-note-type']:
    count = dec.count(t)
    print("  " + ("OK" if count > 0 else "MISS") + ": " + t + " (" + str(count) + ")")

# Check detail pages
for slug in ['figment','adorn','tonight','entropy','migration','renew']:
    path = os.path.join('perfume', slug + '.html')
    if os.path.exists(path):
        print("  Detail: " + slug + ".html EXISTS (" + str(os.path.getsize(path)) + " bytes)")
    else:
        print("  Detail: " + slug + ".html MISSING!")

print("\nSize: " + str(os.path.getsize('index.html')) + " bytes")
print("DONE!")
