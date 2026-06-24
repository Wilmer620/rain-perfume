import subprocess as sp, os

C = open('build-final.py', 'r', encoding='utf-8').read()

# === 1. Replace CSS ===
old_css = '.fvd{display:none;position:absolute;bottom:44px;right:0;width:240px;max-height:300px;overflow-y:auto;background:rgba(253,249,239,.97);backdrop-filter:blur(16px);border:1px solid rgba(184,148,62,.1);border-radius:12px;padding:.7rem;box-shadow:0 12px 40px rgba(0,0,0,.08)}.fvp.open .fvd{display:block}.fvdt{font-family:"Noto Serif SC",serif;font-size:.6rem;color:var(--ink);text-align:center;letter-spacing:.05em;margin-bottom:.4rem;padding-bottom:.35rem;border-bottom:1px solid rgba(184,148,62,.08)}.fvdl{display:flex;flex-direction:column;gap:.2rem}.fvdi{display:flex;align-items:center;justify-content:space-between;padding:.25rem .45rem;border-radius:6px;font-size:.52rem;color:var(--ink2);font-family:"Noto Serif SC",serif;transition:.2s}.fvdi:hover{background:rgba(184,148,62,.04)}.fvdi a{color:var(--ink2);flex:1;text-decoration:none!important}.fvdi a:hover{color:var(--gold)}.fvd2{width:20px;height:20px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:transparent;color:var(--ink3);font-size:.5rem;cursor:none;display:flex;align-items:center;justify-content:center}.fvd2:hover{color:#c0392b}.fvde{text-align:center;font-size:.48rem;color:var(--ink3);opacity:.45;padding:.6rem 0}'

new_css = '.fvm{display:none;position:fixed;inset:0;z-index:800;align-items:center;justify-content:center;background:rgba(253,249,239,.96);backdrop-filter:blur(20px)}.fvm.open{display:flex}.fvmc{position:relative;width:92%;max-width:560px;max-height:80vh;overflow:hidden;background:rgba(255,253,250,.5);border:1px solid rgba(184,148,62,.08);border-radius:20px;box-shadow:0 24px 80px rgba(0,0,0,.08);animation:fvIn .4s cubic-bezier(.4,0,.2,1)}@keyframes fvIn{from{opacity:0;transform:translateY(20px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}.fvmx{position:absolute;top:.8rem;right:.8rem;z-index:3;width:34px;height:34px;border-radius:50%;border:1px solid rgba(184,148,62,.15);background:rgba(255,253,250,.7);color:var(--ink3);font-size:1rem;cursor:none;display:flex;align-items:center;justify-content:center;transition:all .3s}.fvmx:hover{background:rgba(184,148,62,.08);border-color:var(--gold);color:var(--ink);transform:rotate(90deg)}.fvms{overflow-y:auto;max-height:80vh;padding:2.2rem 2rem 2.5rem}.fvmt{font-family:"Noto Serif SC",serif;font-size:1.1rem;color:var(--ink);text-align:center;letter-spacing:.06em;font-weight:500;margin-bottom:.3rem}.fvmsub{text-align:center;font-family:"Noto Serif SC",serif;font-size:.55rem;color:var(--ink3);opacity:.5;line-height:1.8;letter-spacing:.03em;margin-bottom:1.2rem}.fvml{display:flex;flex-direction:column;gap:.3rem}.fvmi{display:flex;align-items:center;justify-content:space-between;padding:.4rem .6rem;border-radius:8px;font-size:.58rem;color:var(--ink2);font-family:"Noto Serif SC",serif;transition:.2s;background:rgba(255,253,250,.3);border:1px solid rgba(184,148,62,.04)}.fvmi:hover{background:rgba(184,148,62,.04);border-color:rgba(184,148,62,.1)}.fvmi a{color:var(--ink2);flex:1;text-decoration:none!important}.fvmi a:hover{color:var(--gold)}.fvm2{width:24px;height:24px;border-radius:50%;border:1px solid rgba(184,148,62,.08);background:transparent;color:var(--ink3);font-size:.55rem;cursor:none;display:flex;align-items:center;justify-content:center}.fvm2:hover{color:#c0392b}.fvme{text-align:center;font-size:.55rem;color:var(--ink3);opacity:.45;padding:1.5rem 0}'

C = C.replace(old_css, new_css)
print("CSS replaced")

# === 2. Replace HTML ===
old_html = '<div class="fvp" id="fvp"><button class="fvt" id="fvt">&#9733;</button><div class="fvd"><div class="fvdt">收藏</div><div class="fvdl" id="fvdl"><div class="fvde">暂无</div></div></div></div>'
new_html = '<div class="fvp" id="fvp"><button class="fvt" id="fvt">&#9733;</button></div><div class="fvm" id="fvm"><div class="fvmc"><button class="fvmx" id="fvmx">x</button><div class="fvms"><div class="fvmt">我的收藏</div><p class="fvmsub">你曾在雨中驻足的那些片刻，<br>都悄悄地留在了这里。</p><div class="fvml" id="fvml"><div class="fvme">雨中来信，静待珍藏。<br>点击香水卡片中的 ☆ 即可收藏。</div></div></div></div></div>'
C = C.replace(old_html, new_html)
print("HTML replaced")

# === 3. Replace JS ===
old_js = 'var _fvL=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]"),el=document.getElementById("fvdl");if(!el)return;var bt=document.getElementById("fvt");if(!bt)return;if(!sv.length){el.innerHTML=\'<div class="fvde">暂无收藏</div>\';bt.classList.remove("on");return;}bt.classList.add("on");var h="";sv.forEach(function(x,i){var en=x.en.toLowerCase().replace(/&/g,"-").replace(/ /g,"-').replace(/\'/g,"");h+=\'<div class="fvdi"><a href="/perfume/\'+en+\'.html">\'+x.cn+\'</a><button class="fvd2" data-idx="\'+i+\'">x</button></div>\';});el.innerHTML=h;el.querySelectorAll(".fvd2").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();var i=parseInt(this.dataset.idx);var sv=JSON.parse(localStorage.getItem("_rf")||"[]");sv.splice(i,1);localStorage.setItem("_rf",JSON.stringify(sv));_fvL();_rfA();});});};var fvTg=document.getElementById("fvt");if(fvTg)fvTg.addEventListener("click",function(e){e.stopPropagation();document.getElementById("fvp").classList.toggle("open");_fvL();});document.addEventListener("click",function(e){if(!e.target.closest(".fvp")){var el=document.getElementById("fvp");if(el)el.classList.remove("open");}});_fvL();'

new_js = 'var _fvL=function(){var sv=JSON.parse(localStorage.getItem("_rf")||"[]"),el=document.getElementById("fvml");if(!el)return;var bt=document.getElementById("fvt");if(!bt)return;if(!sv.length){el.innerHTML=\'<div class="fvme">雨中来信，静待珍藏。<br>点击香水卡片中的 ☆ 即可收藏。</div>\';bt.classList.remove("on");return;}bt.classList.add("on");var h="";sv.forEach(function(x,i){var en=x.en.toLowerCase().replace(/&/g,"-").replace(/ /g,"-').replace(/\'/g,"");h+=\'<div class="fvmi"><a href="/perfume/\'+en+\'.html">\'+x.cn+\'</a><button class="fvm2" data-idx="\'+i+\'">x</button></div>\';});el.innerHTML=h;el.querySelectorAll(".fvm2").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();var i=parseInt(this.dataset.idx);var sv=JSON.parse(localStorage.getItem("_rf")||"[]");sv.splice(i,1);localStorage.setItem("_rf",JSON.stringify(sv));_fvL();_rfA();});});};var fvTg=document.getElementById("fvt");if(fvTg)fvTg.addEventListener("click",function(e){e.stopPropagation();document.getElementById("fvm").classList.add("open");_fvL();});var fvX=document.getElementById("fvmx");if(fvX)fvX.addEventListener("click",function(){document.getElementById("fvm").classList.remove("open");});var fvBg=document.getElementById("fvm");if(fvBg)fvBg.addEventListener("click",function(e){if(e.target===this)this.classList.remove("open");});_fvL();'

C = C.replace(old_js, new_js)
print("JS replaced")

open('build-final.py', 'w', encoding='utf-8').write(C)
r = sp.run(['python', 'build-final.py'], capture_output=True, text=True)
if r.returncode != 0:
    print('FAIL:', r.stderr[:500])
else:
    I = open('index.html', 'rb').read()
    js = I[I.find(b'<script>') + 8:I.find(b'</script>')]
    o = js.count(b'{')
    c = js.count(b'}')
    print(f"OK braces {o} vs {c} size={len(I)}")
