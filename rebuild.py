import subprocess as sp, os, re

C = open('build-final.py', 'r', encoding='utf-8').read()

# === ENTRANCE ===
C = C.replace(
    'var entranceEl=document.getElementById("entrance");if(entranceEl){setTimeout(function(){entranceEl.classList.add("out")},2200);entranceEl.addEventListener("click",function(){entranceEl.classList.add("out")})}',
    'var _e=document.getElementById("entrance");if(_e){(function(){try{var _v=sessionStorage.getItem("_rv");if(_v){_e.classList.add("out");_e.style.display="none";return}}catch(_x){}setTimeout(function(){_e.classList.add("out")},2200);_e.addEventListener("click",function(){_e.classList.add("out")});try{sessionStorage.setItem("_rv","1")}catch(_x){}})()}'
)

# === SLUG ===
card_pos = C.find('def card(num, en, cn, top, heart, base, has_img=False):')
C = C[:card_pos] + "def _slug(en):\n  s=en.replace('&','and').replace(' ','-').replace(\"'\",'')\n  return s.lower()\n\n" + C[card_pos:]

# === NARRATIVES FLAT ===
ns = C.find('NARRATIVES = {')
d=0;st=False
for i in range(ns, len(C)):
    if C[i]=='{': d+=1; st=True
    elif C[i]=='}': d-=1
    if st and d==0: ne=i+1; break
flat = '\n_NF={}\nfor _s in NARRATIVES.values():\n  if isinstance(_s,dict)and"items"in _s:\n    for _i in _s["items"]:\n      _NF[_i[0]]=_i[2]\n'
# Also add English-name entries for collection
for en,cn in [('Figment','我故臆想'),('Adorn','着我之境'),('Tonight','今夜唯我'),('Entropy','熵增时'),('Migration','新时代迁流'),('Renew','致新生')]:
    flat += f"\n_NF['{en}']=_NF.get('{cn}','')\n"
C = C[:ne] + flat + C[ne:]

# === HELPERS ===
helpers = '''def rain_tag_for(en):
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
  d={'Figment':('当归·没药·粉红胡椒','鸢尾·紫罗兰·纸莎草','檀木·香草·安息香'),
     'Adorn':('苦橙叶·白松香·粉红胡椒','土耳其玫瑰·沉香·番红花','皮革·琥珀·苏合香'),
     'Tonight':('香槟调·杜松·柑橘皮','鸢尾·烟草·黑巧克力','愈创木·皮革·麝香'),
     'Entropy':('醛香·臭氧·薄荷','鸢尾·没药·焚香','白麝香·琥珀·矿物调'),
     'Migration':('竹叶·薄荷·柑橘','桂花·白茶·紫藤','白麝香·檀木·米浆'),
     'Renew':('绿叶·佛手柑·薄荷','铃兰·白茶·蕨类','白麝香·雪松·琥珀')}
  return d.get(en,('','',''))

def collection_cn(en):
  m={'Figment':'我故臆想','Adorn':'着我之境','Tonight':'今夜唯我','Entropy':'熵增时','Migration':'新时代迁流','Renew':'致新生'}
  return m.get(en,en)
'''

# Find card function position
card_pos = C.find('def card(num, en, cn, top, heart, base, has_img=False):')
C = C[:card_pos] + helpers + C[card_pos:]

# === CARD FUNCTION ===
old_card = C.find('def card(num, en, cn, top, heart, base, has_img=False):')
old_card_end = C.find('\ndef world_card(filename', old_card)
new_card = '''def card(num, en, cn, top, heart, base, has_img=False):
  sn = series_for(en); rt = rain_tag_for(en)
  first_note = top.split('\\xb7')[0].strip() if top else ''
  p = []
  p.append('<a href=\"perfume/'+_slug(en)+'.html\" class=\"frag-link\"><div class=\"frag-card\" data-en=\"'+en+'\">')
  p.append('<div class=\"frag-cn\">'+cn+'</div>')
  p.append('<div class=\"frag-en\">'+en+'</div>')
  if rt: p.append('<div class=\"frag-rain\">'+rt+'</div>')
  p.append('<div class=\"frag-note-type\"><span class=\"frag-note-dot top-dot\"></span>'+first_note+'调</div>')
  p.append('<div class=\"frag-sv\"><span class=\"fs2\" data-en=\"'+en+'\" data-cn=\"'+cn+'\">☆</span></div>')
  p.append('</div></a>')
  return '\\n'.join(p)

def world_card(filename, alt, num, en, cn, top, heart, base):
  return card(num, en, cn, top, heart, base, has_img=True)

def collection_card(en):
  cn = collection_cn(en); top,heart,base = collection_data(en)
  sn = '臻品雨酿'; first_note = top.split('·')[0].strip() if top else ''
  p = []
  p.append('<a href=\"perfume/'+_slug(en)+'.html\" class=\"frag-link\"><div class=\"frag-card collection-card-v2\" data-en=\"'+en+'\">')
  p.append('<div class=\"frag-cn\">'+cn+'</div>')
  p.append('<div class=\"frag-en\">'+en+'</div>')
  p.append('<div class=\"frag-note-type\"><span class=\"frag-note-dot top-dot\"></span>'+first_note+'调</div>')
  p.append('<div class=\"frag-sv\"><span class=\"fs2\" data-en=\"'+en+'\" data-cn=\"'+cn+'\">☆</span></div>')
  p.append('</div></a>')
  return '\\n'.join(p)
'''
C = C[:old_card] + new_card + C[old_card_end:]
print("Card functions replaced")

# === REPLACE COLLECTION CARDS ===
# Find the hardcoded cards (old format with inline divs)
coll_start = C.find('<div class="frag-grid reveal">')
coll_narr = C.find('{narrative_btn(\'collection\'', coll_start)
if coll_narr > 0:
    coll_end = coll_narr + len("{narrative_btn('collection', 'Narr')}")
    new_coll = '<div class="frag-grid reveal">\n'
    for en in ['Figment','Adorn','Tonight','Entropy','Migration','Renew']:
        new_coll += '{collection_card("'+en+'")}\n'
    new_coll += '</div>\n'
    C = C[:coll_start] + new_coll + C[coll_end:]
    print("Collection cards replaced")
else:
    print("WARNING: Collection narr not found")

# === REMOVE NARR HUB ===
narr = C.find('<div class="narr-hub reveal">')
if narr > 0:
    nxt = C.find('<section class="section-divider', narr+50)
    if nxt > 0: C = C[:narr] + C[nxt:]

# === CSS: ALL AT ONCE ===
css_end = C.rfind("'''", 0, C.find('\nJS = '))

# Remove old card CSS (frag-card rules) and replace
old_css_start = C.find('.frag-card{')
old_css_end = C.find('.collection-section{margin:2rem 0}', old_css_start)
if old_css_end < 0:
    old_css_end = C.find('.frag-grid{', old_css_start)
if old_css_end > 0:
    old_css_end += len('.collection-section{margin:2rem 0}') if 'collection' in C[old_css_end-30:old_css_end+30] else C.find('}\n', old_css_end)+1

new_all_css = '''
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
.frag-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.8rem}
.frag-card .corner,.frag-img-wrap,.frag-img,.frag-num,.frag-name-en,.frag-name-cn,.frag-accord,.poster-badge,.frag-card-inner,.frag-info,.frag-card-header,.frag-card-names,.frag-card-rain-tag,.frag-card-series,.frag-card-notes,.frag-card-collapse-btn,.frag-card-tags,.frag-card-actions,.frag-card-narrative,.frag-card .save-action,.frag-card-action,.frag-collapse,.frag-narrative,.frag-notes,.frag-meta,.frag-pill,.fsr{display:none!important}
.narr-hub,.narr-hub-title,.narr-hub-sub,.narr-hub-desc,.narr-tabs,.narr-tab,.narr-body,.narr-btn,.qr-narr-btn{display:none!important}
.fvp{position:fixed;right:2.5rem;bottom:9.5rem;z-index:200}.fvt{width:44px;height:44px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:rgba(253,249,240,.4);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);color:var(--gold);font-size:1rem;cursor:none;display:flex;align-items:center;justify-content:center;transition:all .4s}.fvt:hover{background:rgba(253,249,240,.55);border-color:rgba(184,148,62,.14)}.fvt.on{color:var(--gold-d);border-color:var(--gold-d)}.fvm{display:none;position:fixed;inset:0;z-index:800;align-items:center;justify-content:center;background:rgba(253,249,239,.96);backdrop-filter:blur(20px)}.fvm.open{display:flex}.fvmc{position:relative;width:92%;max-width:560px;max-height:80vh;overflow:hidden;border:1px solid rgba(184,148,62,.08);border-radius:20px;background:rgba(255,253,250,.45);backdrop-filter:blur(16px);box-shadow:0 24px 80px rgba(0,0,0,.08);animation:fvIn .4s cubic-bezier(.4,0,.2,1)}@keyframes fvIn{from{opacity:0;transform:translateY(20px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}.fvmx{position:absolute;top:.8rem;right:.8rem;z-index:3;width:32px;height:32px;border-radius:50%;border:1px solid rgba(184,148,62,.15);background:rgba(255,253,250,.7);color:var(--ink3);font-size:.9rem;cursor:none;display:flex;align-items:center;justify-content:center;transition:all .3s}.fvmx:hover{background:rgba(184,148,62,.08);border-color:var(--gold);color:var(--ink);transform:rotate(90deg)}.fvms{overflow-y:auto;max-height:80vh;padding:2rem 1.8rem 2.2rem}.fvmt{font-family:"Noto Serif SC",serif;font-size:1.05rem;color:var(--ink);text-align:center;letter-spacing:.06em;font-weight:500;margin-bottom:.2rem}.fvmsub{text-align:center;font-family:"Noto Serif SC",serif;font-size:.52rem;color:var(--ink3);opacity:.45;line-height:1.8;letter-spacing:.03em;margin-bottom:1rem}.fvml{display:flex;flex-direction:column;gap:.25rem}.fvmi{display:flex;align-items:center;justify-content:space-between;padding:.35rem .55rem;border-radius:8px;font-size:.55rem;color:var(--ink2);font-family:"Noto Serif SC",serif;transition:.2s;background:rgba(255,253,250,.3);border:1px solid rgba(184,148,62,.04)}.fvmi:hover{background:rgba(184,148,62,.04);border-color:rgba(184,148,62,.1)}.fvmi a{color:var(--ink2);flex:1;text-decoration:none!important}.fvmi a:hover{color:var(--gold)}.fvm2{width:22px;height:22px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:transparent;color:var(--ink3);font-size:.5rem;cursor:none;display:flex;align-items:center;justify-content:center}.fvm2:hover{color:#c0392b}.fvme{text-align:center;font-size:.52rem;color:var(--ink3);opacity:.4;padding:1.2rem 0}
.phw{display:flex;justify-content:center;padding:.4rem 0;transition:opacity .5s}.phs{display:flex;align-items:center;gap:.5rem;padding:.25rem .7rem;background:rgba(255,253,250,.22);border-radius:100px;border:1px solid rgba(184,148,62,.06)}.phl{font-family:"Noto Serif SC",serif;font-size:.46rem;color:var(--ink3)}.phb{position:relative;width:105px;height:6px;border-radius:3px;background:linear-gradient(90deg,#c0392b,#e74c3c 14%,#e67e22 28%,#f1c40f 43%,#2ecc71 50%,#27ae60 57%,#1abc9c 64%,#3498db 78%,#9b59b6)}.phf{position:absolute;right:0;top:0;bottom:0;border-radius:0 3px 3px 0;background:rgba(253,249,239,.7);transition:width .6s ease}.phn{position:absolute;top:-4px;width:3px;height:14px;border-radius:2px;background:var(--gold);transition:left .6s ease,background .3s}.phv{font-family:"Noto Serif SC",serif;font-size:.58rem;font-weight:300;color:var(--gold);min-width:1.8rem;text-align:right}
'''
C = C[:old_css_start] + new_all_css + C[old_css_end:]
print("CSS replaced")

# === HTML: fav modal + pH ===
C = C.replace('<button class="music-btn"','<div class="fvp" id="fvp"><button class="fvt" id="fvt">★</button></div>\n<div class="fvm" id="fvm"><div class="fvmc"><button class="fvmx" id="fvmx">x</button><div class="fvms"><div class="fvmt">我的收藏</div><p class="fvmsub">你曾在雨中驻足的那些片刻，<br>都悄悄地留在了这里。</p><div class="fvml" id="fvml"><div class="fvme">雨中来信，静待珍藏。<br>点击卡片中的 ☆ 即可收藏。</div></div></div></div></div>\n<button class="music-btn"')
C = C.replace('<div class="blend-submit-wrap"><button class="blend-submit" id="blendSubmit">降下这场雨</button></div>','<div class="phw" id="phWrap"><div class="phs"><span class="phl">pH</span><div class="phb"><div class="phf" id="phBg"></div><div class="phn" id="phN"></div></div><span class="phv" id="phV">-</span></div></div>\n<div class="blend-submit-wrap"><button class="blend-submit" id="blendSubmit">降下这场雨</button></div>')

# === JS: save + fav + pH ===
cp = C.find('console.log("%c[RAIN] Perfume as Rain %c')

old_ud = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});\nvar cnt=Object.keys(selected).length;\nif(bottleFill){bottleFill.style.height=totalPercent+'%';}\nif(totalEl){totalEl.textContent=totalPercent+'%';}"
ph_ud = "totalPercent=0;Object.values(selected).forEach(function(v){totalPercent+=v;});var cnt=Object.keys(selected).length;if(bottleFill){bottleFill.style.height=totalPercent+'%';}if(totalEl){totalEl.textContent=totalPercent+'%';}var pV=document.getElementById('phV'),pB=document.getElementById('phBg'),pN=document.getElementById('phN');if(pV&&pB&&pN&&cnt>=2){var cats={};Object.keys(selected).forEach(function(k){var c=INGREDIENTS[parseInt(k)].cat;cats[c]=(cats[c]||0)+selected[parseInt(k)];});var ks=Object.keys(cats);var vs=ks.map(function(k){return cats[k];});var a=vs.reduce(function(a,b){return a+b;},0)/vs.length;var v=vs.reduce(function(s,x){return s+Math.pow(x-a,2);},0)/vs.length;var sd=Math.sqrt(v);var ds=Math.min(1.5,ks.length/4);var bp=Math.min(1.5,sd/12);var ps=[['citrus','floral'],['floral','woody'],['citrus','woody'],['woody','resin'],['spicy','woody'],['green','floral'],['aquatic','citrus'],['floral','musk']];var pb=0;ps.forEach(function(p){if(cats[p[0]]&&cats[p[1]])pb+=.4;});var raw=7+(ds*2.5)-(bp*2.5)+pb;var ph=Math.round(Math.max(1,Math.min(14,raw))*10)/10;pV.textContent=ph.toFixed(1);var pct=(ph-1)/13*100;pB.style.width=(100-pct)+'%';pN.style.left=pct+'%';if(ph>8)pN.style.background='#9b59b6';else if(ph>6.5)pN.style.background='#2ecc71';else if(ph>5)pN.style.background='#f1c40f';else if(ph>3.5)pN.style.background='#e67e22';else pN.style.background='#e74c3c';}else if(pV){pV.textContent='-';}"
C = C.replace(old_ud, ph_ud)
C = C.replace("resultEl.classList.add('show');resultShown=true;", "resultEl.classList.add('show');resultShown=true;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='0';")
C = C.replace("resultEl.classList.remove('show');resultShown=false;", "resultEl.classList.remove('show');resultShown=false;var pw=document.getElementById('phWrap');if(pw)pw.style.opacity='1';")

all_js = 'document.addEventListener("click",function(e){var s=e.target.closest(".fs2");if(!s)return;e.preventDefault();e.stopPropagation();var en=s.dataset.en,cn=s.dataset.cn;var sv=JSON.parse(localStorage.getItem("_rf")||"[]");var i=sv.findIndex(function(f){return f.en===en;});if(i>=0)sv.splice(i,1);else sv.push({en:en,cn:cn});localStorage.setItem("_rf",JSON.stringify(sv));_rfA()});var _rfA=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]");var es=sv.map(function(f){return f.en;});document.querySelectorAll(".fs2").forEach(function(p){if(es.indexOf(p.dataset.en)>=0){p.classList.add("sv2");p.innerHTML="★";}else{p.classList.remove("sv2");p.innerHTML="☆";}});};setTimeout(_rfA,500);\nvar _fvL=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]"),el=document.getElementById("fvml");if(!el)return;var bt=document.getElementById("fvt");if(!bt)return;if(!sv.length){el.innerHTML="<div class=fvme>雨中来信，静待珍藏。<br>点击卡片中的 ☆ 即可收藏。</div>";bt.classList.remove("on");return;}bt.classList.add("on");var h="";sv.forEach(function(x,i){var en=x.en.replace(/&/g,"and").replace(/ /g,"-").replace(/\'/g,"").toLowerCase();h+="<div class=fvmi><a href=/perfume/"+en+".html>"+x.cn+"</a><button class=fvm2 data-idx="+i+">x</button></div>";});el.innerHTML=h;el.querySelectorAll(".fvm2").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();var i=parseInt(this.dataset.idx);var sv=JSON.parse(localStorage.getItem("_rf")||"[]");sv.splice(i,1);localStorage.setItem("_rf",JSON.stringify(sv));_fvL();_rfA();});});};var fvTg=document.getElementById("fvt");if(fvTg)fvTg.addEventListener("click",function(e){e.stopPropagation();document.getElementById("fvm").classList.add("open");_fvL();});var fvX=document.getElementById("fvmx");if(fvX)fvX.addEventListener("click",function(){document.getElementById("fvm").classList.remove("open");});var fvBg=document.getElementById("fvm");if(fvBg)fvBg.addEventListener("click",function(e){if(e.target===this)this.classList.remove("open");});_fvL();\n'
C = C[:cp] + all_js + C[cp:]

open('build-final.py', 'w', encoding='utf-8').write(C)
r = sp.run(['python', 'build-final.py'], capture_output=True, text=True)
if r.returncode != 0:
    for line in r.stderr.split('\n')[:10]:
        print(line)
else:
    I = open('index.html', 'r', encoding='utf-8').read()
    js = I[I.find('<script>')+8:I.find('</script>')]
    print(f"BUILD OK braces {js.count('{')} vs {js.count('}')} size={os.path.getsize('index.html')}")
    for en in ['Figment','Adorn','Tonight','Entropy','Migration','Renew','Blur','Pause','Flirt','Babel']:
        c = I.count(en)
        print(f"  {en}: {c}x")
    links = re.findall(r'href="perfume/([^"]+)"', I)
    bad = [l for l in links if '&' in l or ' ' in l]
    print(f"Links: {len(links)} {'clean' if not bad else 'BAD:'+str(bad)}")
