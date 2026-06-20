#!/usr/bin/env python
"""Full rebuild: take clean original, add ALL features, produce final index.html"""
import re, sys

with open('C:/Users/Ara/rain-website/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"Input: {len(c)} chars, JS scripts: {c.count('<script>')}")

# ============================================================
# STEP 1: Fix body cursor (always on)
# ============================================================
# Already has body{cursor:none} — good

# ============================================================
# STEP 2: Add entrance animation CSS (before Hero CSS)
# ============================================================
entrance_css = '''
.entrance{position:fixed;inset:0;z-index:10000;background:var(--bg);display:flex;align-items:center;justify-content:center;pointer-events:all;transition:opacity .8s ease,visibility .8s ease}
.entrance.out{opacity:0;visibility:hidden;pointer-events:none}
.entrance-ripple{position:absolute;top:50%;left:50%;width:0;height:0;border-radius:50%;border:1px solid rgba(184,148,62,.25);transform:translate(-50%,-50%);animation:rippleOut 1.8s .2s ease-out forwards}
.entrance-ripple:nth-child(2){animation-delay:.4s;border-color:rgba(184,148,62,.15)}
.entrance-ripple:nth-child(3){animation-delay:.6s;border-color:rgba(184,148,62,.1)}
.entrance-brand{position:relative;z-index:1;text-align:center;opacity:0;animation:brandReveal .7s .9s cubic-bezier(.25,.1,.25,1) forwards}
.entrance-brand h2{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,4.5rem);font-weight:400;letter-spacing:.3em;color:var(--ink);margin-bottom:.3rem}
.entrance-brand p{font-family:'Noto Serif SC',serif;font-size:.7rem;font-weight:300;letter-spacing:.5em;color:var(--ink3)}
.entrance-skip-wrap{position:absolute;bottom:3rem;left:50%;transform:translateX(-50%)}
.entrance-skip{font-family:'Inter',sans-serif;font-size:.55rem;letter-spacing:.35em;color:var(--ink3);text-transform:uppercase;opacity:0;animation:brandReveal .5s 1.2s ease-out forwards;cursor:none}
.entrance-drop{position:absolute;top:-40px;left:50%;width:2px;height:20px;background:linear-gradient(to bottom,transparent,var(--gold),var(--gold-d));border-radius:0 0 2px 2px;transform:translateX(-50%);animation:dropFall .7s .05s cubic-bezier(.33,0,.66,1) forwards}
@keyframes rippleOut{0%{width:0;height:0;opacity:.6}100%{width:360px;height:360px;opacity:0}}
@keyframes brandReveal{0%{opacity:0;transform:translateY(16px) scale(.96);filter:blur(8px)}60%{opacity:.7;filter:blur(2px)}100%{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
@keyframes dropFall{0%{top:-40px;opacity:0}15%{opacity:1}85%{top:calc(50% - 6px);opacity:1}100%{top:calc(50% - 2px);opacity:0}}
'''

# Add after hero scroll line CSS, before the first media query
target = '@media (max-width:1080px)'
c = c.replace(target, entrance_css + '\n' + target)

# ============================================================
# STEP 3: Add music button + top nav + side deco + scroll-bg CSS
# ============================================================
extra_css = '''
.music-btn{position:fixed;bottom:5.5rem;right:2.5rem;z-index:101;width:44px;height:44px;display:flex;align-items:center;justify-content:center;background:rgba(254,252,245,.4);backdrop-filter:blur(22px);border:1px solid rgba(184,148,62,.08);border-radius:50%;cursor:none;transition:all .4s;box-shadow:0 4px 20px rgba(139,105,30,.02)}
.music-btn:hover{background:rgba(254,252,245,.55);border-color:rgba(184,148,62,.14);box-shadow:0 8px 32px rgba(139,105,30,.06)}
.music-btn svg{width:16px;height:16px;fill:none;stroke:var(--gold-d);stroke-width:1.5;transition:stroke .4s}.music-btn:hover svg{stroke:var(--gold)}
.top-nav{display:flex;gap:2.5rem;list-style:none;position:fixed;top:1.6rem;right:3.5rem;z-index:100}
.top-nav a{color:var(--ink3);text-decoration:none;font-family:'Inter',sans-serif;font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;transition:all .4s;position:relative}
.top-nav a:hover{color:var(--gold)}.top-nav a::after{content:'';position:absolute;bottom:-4px;left:50%;width:3px;height:3px;border-radius:50%;background:var(--gold);transform:translateX(-50%) scale(0);transition:transform .35s}
.top-nav a.active{color:var(--ink)}.top-nav a.active::after{transform:translateX(-50%) scale(1)}
.side-deco{position:fixed;top:0;bottom:0;z-index:0;pointer-events:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5rem}
.side-deco-l{left:2.5rem}.side-deco-r{right:2.5rem}
.side-deco .s-diamond{width:22px;height:22px;border:1.5px solid var(--gold-d);transform:rotate(45deg);opacity:.22}
.side-deco .s-dot{width:6px;height:6px;border-radius:50%;background:var(--gold-d);opacity:.28}
.side-deco .s-line{width:1px;height:80px;background:var(--gold-d);opacity:.2}
.side-deco .s-circle{width:26px;height:26px;border-radius:50%;border:1.5px solid var(--gold-d);opacity:.18}
.showcase-toggle-wrap{text-align:center;margin-top:1.5rem}
.showcase-toggle{font-family:'Inter',sans-serif;font-size:.58rem;letter-spacing:.3em;color:var(--ink3);background:rgba(255,254,253,.2);backdrop-filter:blur(8px);border:1px solid rgba(184,148,62,.08);border-radius:100px;padding:.5rem 1.5rem;cursor:none;text-transform:uppercase;display:inline-block;transition:all .4s}
.showcase-toggle:hover{border-color:var(--gold);color:var(--gold-d);background:rgba(255,254,253,.35)}
.showcase-body{transition:max-height .6s ease,opacity .4s ease;overflow:hidden}
.showcase-body.collapsed{max-height:0!important;opacity:0}
.series-tabs{display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap;margin:2rem 0 1rem;padding:0 1rem}
.series-tab{font-family:'Cormorant Garamond',serif;font-size:.95rem;font-weight:400;letter-spacing:.1em;color:var(--ink3);background:none;border:none;padding:.6rem 1.2rem;cursor:none;position:relative;transition:color .4s}
.series-tab::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:var(--gold);transform:scaleX(0);transition:transform .4s}
.series-tab.active{color:var(--ink)}.series-tab.active::after{transform:scaleX(1)}.series-tab:hover{color:var(--ink2)}
.series-panel{display:none}.series-panel.active{display:block;animation:fUp .5s ease-out}
.sec-label{text-align:center;padding:2rem 2rem 0}.sec-label-k{font-family:'Inter',sans-serif;font-size:.54rem;letter-spacing:.5em;color:var(--gold-d);text-transform:uppercase;margin-bottom:.8rem}
.sec-label-t{font-family:'Cormorant Garamond',serif;font-size:clamp(1.8rem,3.5vw,2.5rem);font-weight:400;letter-spacing:.1em;color:var(--ink)}
.craft{position:relative;z-index:2;padding:1rem 3rem 3rem;max-width:1100px;margin:0 auto}
.craft-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.craft-card{padding:2.5rem 2rem;text-align:center;background:rgba(255,254,253,.1);backdrop-filter:blur(20px);border:1px solid rgba(184,148,62,.04);border-radius:var(--radius);box-shadow:0 4px 28px rgba(139,105,30,.02);transition:all .4s}
.craft-card:hover{background:rgba(255,254,253,.18);border-color:rgba(184,148,62,.1);box-shadow:0 8px 36px rgba(139,105,30,.04);transform:translateY(-3px)}
.craft-card-num{font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:300;color:var(--gold-d);opacity:.3;margin-bottom:1rem}
.craft-card h4{font-family:'Noto Serif SC',serif;font-size:.88rem;font-weight:500;color:var(--ink);margin-bottom:.6rem;letter-spacing:.06em}
.craft-card p{font-family:'Noto Serif SC',serif;font-size:.76rem;font-weight:300;line-height:2;color:var(--ink3)}
.founders-note{position:relative;z-index:2;padding:1rem 3rem 3rem;max-width:800px;margin:0 auto;text-align:center}
.founders-inner{padding:4rem 3.5rem}
.founders-kicker{font-family:'Inter',sans-serif;font-size:.54rem;letter-spacing:.5em;color:var(--gold-d);text-transform:uppercase;margin-bottom:2rem}
.founders-text{font-family:'Noto Serif SC',serif;font-size:.95rem;font-weight:300;line-height:2.8;color:var(--ink2);letter-spacing:.05em}
.founders-text em{font-style:normal;color:var(--gold);font-weight:500}
.founders-sign{font-family:'Cormorant Garamond',serif;font-size:1.1rem;letter-spacing:.3em;color:var(--gold-d);margin-top:2.5rem}
@media (max-width:1080px){.top-nav{display:none}.side-deco{display:none}.series-tabs{gap:.8rem}.series-tab{font-size:.8rem}.craft-grid{grid-template-columns:1fr;gap:14px}}
@media (max-width:768px){.music-btn{bottom:4.5rem;right:1.2rem;width:40px;height:40px}.craft-card{padding:2rem 1.5rem}.founders-inner{padding:2.5rem 1.5rem}}
'''

c = c.replace('@media (max-width:1080px){', extra_css + '\n@media (max-width:1080px){')

# ============================================================
# STEP 4: Update hero animation timing (entry → hero blend)
# ============================================================
c = c.replace(
    '.hero-scroll-line{width:1px;height:32px;background:linear-gradient(to bottom,var(--ink3),transparent);animation:breathe 3s ease-in-out infinite}',
    '.hero-scroll-line{width:1px;height:32px;background:linear-gradient(to bottom,var(--ink3),transparent);animation:breathe 3s ease-in-out infinite}\n.hero-tag,.hero-title,.hero-sub,.hero-vd,.hero-line{animation-delay:1.8s!important}\n.hero-scroll-inner{animation-delay:2s!important}'
)

# ============================================================
# STEP 5: Add entrance HTML
# ============================================================
c = c.replace(
    '<div class="cursor-dot"',
    '<div class="entrance" id="entrance"><div class="entrance-drop"></div><div class="entrance-ripple"></div><div class="entrance-ripple"></div><div class="entrance-ripple"></div><div class="entrance-brand"><h2>RAIN</h2><p>Perfume as Rain</p></div><div class="entrance-skip-wrap"><span class="entrance-skip">每一滴雨都是重生</span></div></div>\n<div class="cursor-dot"'
)

# ============================================================
# STEP 6: Add top nav + RAIN logo + side deco + music button
# ============================================================
c = c.replace(
    '<nav class="nav" id="nav">',
    '<div style="position:fixed;top:1.6rem;left:3.5rem;z-index:100;font-family:Cormorant Garamond,serif;font-size:1.35rem;font-weight:500;letter-spacing:.35em;color:var(--ink);text-transform:uppercase">RAIN</div>\n<ul class="top-nav" id="topNav"><li><a href="#phil">品牌哲学</a></li><li><a href="#series">产品介绍</a></li><li><a href="#craft">制香之道</a></li><li><a href="#founders">主理人手记</a></li><li><a href="#quiz">寻雨之路</a></li><li><a href="#newsletter">降雨预报</a></li></ul>\n<!-- SIDE DECO -->\n<div class="side-deco side-deco-l"><span class="s-diamond"></span><span class="s-circle"></span><span class="s-dot"></span><span class="s-line"></span><span class="s-dot"></span><span class="s-circle"></span><span class="s-diamond"></span></div>\n<div class="side-deco side-deco-r"><span class="s-diamond"></span><span class="s-circle"></span><span class="s-dot"></span><span class="s-line"></span><span class="s-dot"></span><span class="s-circle"></span><span class="s-diamond"></span></div>\n<nav class="nav" id="nav">'
)

# ============================================================
# STEP 7: Replace the COLLECTION section with SERIES HUB
# Find everything from collection section start to ethos-strip
# ============================================================
col_start = c.find('<section id="collection"')
ethos_start = c.find('<section class="ethos-strip"')

series_html = '''
<div class="sec-label reveal"><p class="sec-label-k">01</p><h2 class="sec-label-t">品牌哲学</h2></div>
'''
# Keep phil section where it is — just move it before collection
# Actually the original has phil BEFORE collection. Let me just add labels.

# Replace "The Six Rains" text with new hub
col_header_old = '<p class="col-kicker">The Six Rains</p>'
col_header_new = '''<p class="col-kicker">The Six Rains</p><h2 class="col-title" style="margin-bottom:.5rem">世界之色</h2><p class="col-sub">WORLD OF COLORS</p>'''

# Actually let me just fix the collection to be world-only and add series hub after phil
# The simplest approach: keep original structure but insert key elements

# Insert section labels before each major section
# phil is at the start, add label before it
c = c.replace('<section class="phil" id="phil">', '<div class="sec-label reveal"><p class="sec-label-k">01</p><h2 class="sec-label-t">品牌哲学</h2></div>\n<section class="phil" id="phil">')

# After philosophy, before collection: add 雨的衍生 label + series hub
phil_end = c.find('</section>', c.find('id="phil"'))
section_divider = c.find('<section class="section-divider"', phil_end)
if section_divider > 0:
    prefix = c[:section_divider]
    suffix = c[section_divider:]

    series_markup = '''
<div class="sec-label reveal"><p class="sec-label-k">02</p><h2 class="sec-label-t">雨的衍生</h2></div>
<section class="series-hub reveal" id="series">
  <p style="font-family:Inter,sans-serif;font-size:.54rem;letter-spacing:.5em;color:var(--gold-d);text-transform:uppercase;margin-bottom:1.5rem">The Rain Derivatives</p>
  <h2 style="font-family:Cormorant Garamond,serif;font-size:clamp(1.8rem,3.5vw,2.5rem);font-weight:400;letter-spacing:.1em;color:var(--ink);margin-bottom:.5rem">Product Lines</h2>
  <p style="font-family:Inter,sans-serif;font-size:.54rem;letter-spacing:.5em;color:var(--gold-d);text-transform:uppercase;margin-top:.5rem">产品主题介绍</p>
  <p style="font-family:Noto Serif SC,serif;font-size:.82rem;font-weight:300;color:var(--ink3);letter-spacing:.06em;line-height:2.2;max-width:520px;margin:1rem auto 0">每一场雨都有自己的性格，不同种进入自己的方式。</p>
</section>
<div class="series-tabs reveal">
  <button class="series-tab active" data-panel="sojourn">驻足苦旅</button>
  <button class="series-tab" data-panel="world">世界之色</button>
  <button class="series-tab" data-panel="feast">灵感盛宴</button>
  <button class="series-tab" data-panel="seasons">四季所生</button>
  <button class="series-tab" data-panel="after">雨后</button>
</div>
'''
    c = prefix + series_markup + suffix

print(f"Phil end: {phil_end}, Divider at: {section_divider}")
print(f"Size after edits: {len(c)}")

# ============================================================
# STEP 8: Add narrative toggles + craft/founders/seasons sections before quiz
# ============================================================
# Find the quiz section
quiz_pos = c.find('<section class="quiz"')

# Insert craft + founders before quiz
craft_html = '''
<section class="section-divider reveal"><div class="section-divider-inner"><span class="section-divider-dot"></span></div></section>
<div class="sec-label reveal"><p class="sec-label-k">03</p><h2 class="sec-label-t">制香之道</h2></div>
<section class="craft reveal" id="craft"><div class="craft-grid">
  <div class="craft-card"><span class="craft-card-num">01</span><h4>冷萃 · 锁住第一缕气息</h4><p>在低温下将植物原料浸入有机甘蔗酒精中，持续 72 小时。冷萃不是为了快——是为了抓住最脆弱的前调分子。</p></div>
  <div class="craft-card"><span class="craft-card-num">02</span><h4>静置 · 让时间完成配方</h4><p>混合后的液体在恒温暗室中静置 4–8 周。每一天，分子都在重新组合。这不是等待——是让时间成为调香师。</p></div>
  <div class="craft-card"><span class="craft-card-num">03</span><h4>微滤 · 只留下光的重量</h4><p>经过多层微米级过滤，去除残留的植物蜡质，却不带走任何香气分子。最终的液体透明如雨。</p></div>
</div></section>
<section class="section-divider reveal"><div class="section-divider-inner"><span class="section-divider-dot"></span></div></section>
<div class="sec-label reveal"><p class="sec-label-k">04</p><h2 class="sec-label-t">主理人手记</h2></div>
<section class="founders-note reveal" id="founders"><div class="founders-inner glass-panel">
  <p class="founders-kicker">A Letter from the Founder</p>
  <p class="founders-text"><em>我一直在找一种气味。</em><br>不是那种走进房间就能被认出来的——<br>而是你在雨天窗边发呆时，<br>自己都不确定自己闻到了什么的那种。<br><br>2025 年冬天，我们做了 RAIN。<br>不是想做一个香水品牌。我们只是想：<br>如果有人能把<em>雨停之后那一分钟的安静</em>收集起来，<br>世界上会不会多一种温柔。<br><br>我们没有答案。但我们会一直做下去。</p>
  <p class="founders-sign">— RAIN 主理人</p>
</div></section>
'''

c = c[:quiz_pos] + craft_html + c[quiz_pos:]

# ============================================================
# STEP 9: Add music button + JS additions
# ============================================================
# Find back-top button
backtop = c.find('<button class="back-top"')
if backtop > 0:
    c = c[:backtop] + '<button class="music-btn" id="musicBtn"><svg viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg></button>\n' + c[backtop:]

# ============================================================
# STEP 10: Add entrance + scroll-bg + music + nav + narrative-toggle JS
# ============================================================
js_add = '''
var entranceEl=document.getElementById("entrance");if(entranceEl){setTimeout(function(){entranceEl.classList.add("out")},2200);entranceEl.addEventListener("click",function(){entranceEl.classList.add("out")})}
(function(){var stops=[{p:0,r:253,g:251,b:245},{p:.18,r:253,g:247,b:232},{p:.36,r:251,g:249,b:242},{p:.54,r:250,g:250,b:244},{p:.72,r:253,g:246,b:228},{p:1,r:253,g:251,b:245}];function lerp(a,b,t){return a+(b-a)*t}function updateBg(){var h=document.documentElement.scrollHeight-window.innerHeight;if(h<=0)return;var t=Math.min(1,Math.max(0,window.scrollY/h));for(var i=0;i<stops.length-1;i++){if(t>=stops[i].p&&t<=stops[i+1].p){var lt=(t-stops[i].p)/(stops[i+1].p-stops[i].p);var r=Math.round(lerp(stops[i].r,stops[i+1].r,lt));var g=Math.round(lerp(stops[i].g,stops[i+1].g,lt));var b=Math.round(lerp(stops[i].b,stops[i+1].b,lt));document.body.style.backgroundColor="rgb("+r+","+g+","+b+")";return}}}window.addEventListener("scroll",updateBg,{passive:true});updateBg()})();
var topNavLinks=document.querySelectorAll(".top-nav a"),allSections=document.querySelectorAll("section[id]");function updateNav(){var y=window.scrollY+window.innerHeight/3,cur="";allSections.forEach(function(s){if(y>=s.offsetTop)cur=s.getAttribute("id")});topNavLinks.forEach(function(a){a.classList.toggle("active",a.getAttribute("href")==="#"+cur)})}window.addEventListener("scroll",updateNav,{passive:true});updateNav();
var seriesTabs=document.querySelectorAll(".series-tab"),seriesPanels=document.querySelectorAll(".series-panel");seriesTabs.forEach(function(tab){tab.addEventListener("click",function(){seriesTabs.forEach(function(t){t.classList.remove("active")});tab.classList.add("active");seriesPanels.forEach(function(p){p.classList.remove("active")});document.querySelector('.series-panel[data-panel="'+tab.dataset.panel+'"]').classList.add("active")})});
document.querySelectorAll(".narrative-toggle").forEach(function(btn){var body=document.getElementById(btn.dataset.target),open=false;if(!body)return;body.style.maxHeight="0";body.classList.add("collapsed");btn.addEventListener("click",function(){if(open){body.style.maxHeight="0";body.classList.add("collapsed");btn.textContent="展开叙事";open=false}else{body.style.maxHeight=body.scrollHeight+"px";body.classList.remove("collapsed");btn.textContent="收起叙事";open=true}})});
(function(){var btn=document.getElementById("musicBtn"),playing=false,ctx=null,gain=null;if(!btn)return;function noiseNode(){var buf=ctx.createBuffer(1,ctx.sampleRate*3,ctx.sampleRate),d=buf.getChannelData(0);for(var i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*0.5;var s=ctx.createBufferSource();s.buffer=buf;s.loop=true;return s}btn.addEventListener("click",function(){if(!ctx){ctx=new(window.AudioContext||window.webkitAudioContext)();gain=ctx.createGain();gain.gain.value=0;gain.connect(ctx.destination)}if(playing){gain.gain.linearRampToValueAtTime(0,ctx.currentTime+0.3);btn.style.borderColor="";btn.style.boxShadow="";playing=false}else{var n1=noiseNode(),f1=ctx.createBiquadFilter();f1.type="lowpass";f1.frequency.value=350;var n2=noiseNode(),f2=ctx.createBiquadFilter();f2.type="lowpass";f2.frequency.value=600;var n3=noiseNode(),f3=ctx.createBiquadFilter();f3.type="bandpass";f3.frequency.value=2000;f3.Q.value=0.5;n1.connect(f1);f1.connect(gain);n2.connect(f2);f2.connect(gain);n3.connect(f3);f3.connect(gain);n1.start();n2.start();n3.start();gain.gain.linearRampToValueAtTime(0.22,ctx.currentTime+0.3);btn.style.borderColor="var(--gold)";btn.style.boxShadow="0 0 16px rgba(184,148,62,.25)";playing=true}})})();
'''

# Add music-btn to cursor interactive list
c = c.replace('.nl-toggle-btn', '.nl-toggle-btn,.music-btn,.top-nav a,.series-tab')

# Insert JS additions after the scroll reveal code
c = c.replace('/* ── Nav + Back to top', js_add + '\n/* ── Nav + Back to top')

# ============================================================
# STEP 11: Add placeholder panels for sojourn, feast, seasons, after
# Insert after the world collection section, before ethos
# ============================================================
# Find the closing of the world frag-grid
frag_end = c.find('<!-- ====== ETHOS STRIP ====== -->')
if frag_end > 0:
    # Find the section closing before it
    sec_close = c.rfind('</section>', 0, frag_end)

    panels_html = '''
<div class="series-panel active" data-panel="sojourn"><div class="frag-grid">'''
# 7 placeholder cards for 驻足苦旅
sojourn_data = [('01','Blur','花非花·雾非雾','White Peony · Pear · Mist','Jasmine · Osmanthus · Silk','White Musk · Ambroxan'),('02','Knot','结','Cardamom · Black Pepper','Cedar · Clove · Labdanum','Oud · Leather · Birch Tar'),('03','Flirt','风骚','Pink Pepper · Bergamot','Rose de Mai · Peony','Musk · Sandalwood'),('04','Peak','摩登巅','Juniper · Lemon','Cedar · Orris · Violet','Musk · Amber'),('05','Wall','围城','Incense · Elemi','Rose · Myrrh · Patchouli','Frankincense · Sandalwood'),('06','Leave','再别','Bergamot · Black Tea','Orris · Papyrus · Violet','Cedar · Vanilla'),('07','Iris','瞳孔','Carrot Seed · Aldehydes','Orris · Mimosa','Musk · Sandalwood')]
for s in sojourn_data:
    panels_html += '<div class="frag-card reveal reveal-d1" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)"><span class="corner c-tl"></span><span class="corner c-br"></span><div class="frag-card-inner"><div class="frag-img-wrap"></div><div class="frag-info"><p class="frag-num">NO. '+s[0]+'</p><h3 class="frag-name-en">'+s[1]+'</h3><p class="frag-name-cn">'+s[2]+'</p><p class="frag-accord"><b>Top</b> '+s[3]+'<br><b>Heart</b> '+s[4]+'<br><b>Base</b> '+s[5]+'</p></div></div></div>\n'

panels_html += '</div><div class="showcase-toggle-wrap"><button class="showcase-toggle narrative-toggle" data-target="narrative-sojourn">展开叙事</button></div><div class="showcase-body collapsed" id="narrative-sojourn" style="max-width:900px;margin:0 auto;padding:2rem;text-align:center"><div style="padding:3rem 2rem;background:rgba(255,254,253,.1);backdrop-filter:blur(20px);border:1px solid rgba(184,148,62,.04);border-radius:6px;font-family:Noto Serif SC,serif;font-size:.9rem;font-weight:300;color:var(--ink3);line-height:2.5">驻足苦旅 的深度叙事即将呈现。<br>每一场雨都有自己的故事。</div></div></div>\n'

# World panel (keep existing collection content)
panels_html += '<div class="series-panel" data-panel="world">\n'
# Copy frag-grid content from original collection section

# Feast panel
feast_data = [('01','Face','皮囊','Juniper · Lemon Peel','Orris · Violet · Powder','White Musk · Cool Amber'),('02','Gone','隐身衣','Black Pepper · Clove','Smoke · Incense · Ash','Vetiver · Leather'),('03','Wait','等待','Bergamot · Cardamom','Amber · Labdanum · Honey','Oud · Sandalwood'),('04','Rush','欢愉','Pink Pepper · Mandarin','Rose · Jasmine · Peach','Musk · Sandalwood'),('05','Stay','侍者','Green Tea · Bamboo','Lotus · Moss · Water Lily','White Musk · Cedar')]
panels_html += '<div class="series-panel" data-panel="feast"><div class="frag-grid">'
for f in feast_data:
    panels_html += '<div class="frag-card reveal reveal-d1" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)"><span class="corner c-tl"></span><span class="corner c-br"></span><div class="frag-card-inner"><div class="frag-img-wrap"></div><div class="frag-info"><p class="frag-num">NO. '+f[0]+'</p><h3 class="frag-name-en">'+f[1]+'</h3><p class="frag-name-cn">'+f[2]+'</p><p class="frag-accord"><b>Top</b> '+f[3]+'<br><b>Heart</b> '+f[4]+'<br><b>Base</b> '+f[5]+'</p></div></div></div>\n'
panels_html += '</div><div class="showcase-toggle-wrap"><button class="showcase-toggle narrative-toggle" data-target="narrative-feast">展开叙事</button></div><div class="showcase-body collapsed" id="narrative-feast" style="max-width:900px;margin:0 auto;padding:2rem;text-align:center"><div style="padding:3rem 2rem;background:rgba(255,254,253,.1);backdrop-filter:blur(20px);border:1px solid rgba(184,148,62,.04);border-radius:6px;font-family:Noto Serif SC,serif;font-size:.9rem;font-weight:300;color:var(--ink3);line-height:2.5">灵感盛宴 的深度叙事即将呈现。<br>每一场雨都有自己的故事。</div></div></div>\n'

# Seasons
seasons_data = [('春','生','破土·呼吸'),('夏','长','疯长·蔓延'),('秋','收','沉淀·入静'),('冬','藏','封存·等待')]
panels_html += '<div class="series-panel" data-panel="seasons"><div class="frag-grid">'
for s in seasons_data:
    panels_html += '<div class="frag-card reveal reveal-d1"><div class="frag-card-inner"><div class="frag-img-wrap"></div><div class="frag-info"><p class="frag-num">'+s[0]+'</p><h3 class="frag-name-en">'+s[1]+'</h3><p class="frag-name-cn">'+s[2]+'</p><p class="frag-accord">'+s[0]+'日限定系列 · 即将呈现</p></div></div></div>\n'
panels_html += '</div><div class="showcase-toggle-wrap"><button class="showcase-toggle narrative-toggle" data-target="narrative-seasons">展开叙事</button></div><div class="showcase-body collapsed" id="narrative-seasons" style="max-width:900px;margin:0 auto;padding:2rem;text-align:center"><div style="padding:3rem 2rem;background:rgba(255,254,253,.1);backdrop-filter:blur(20px);border:1px solid rgba(184,148,62,.04);border-radius:6px;font-family:Noto Serif SC,serif;font-size:.9rem;font-weight:300;color:var(--ink3);line-height:2.5">四季所生 的深度叙事即将呈现。<br>每一场雨都有自己的故事。</div></div></div>\n'

# After
after_data = [('01','Fall','自天穹','Ozone · Bergamot','Rain Accord · Iris','White Musk · Cedar'),('02','Drift','穿云间','Aldehydes · Bergamot','Cotton Flower · Magnolia','Musk · Sandalwood'),('03','Shatter','碎地霜','Cassia · Black Tea','Osmanthus · Patchouli','Vetiver · Oakmoss')]
panels_html += '<div class="series-panel" data-panel="after"><div class="frag-grid">'
for a in after_data:
    panels_html += '<div class="frag-card reveal reveal-d1" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)"><span class="corner c-tl"></span><span class="corner c-br"></span><div class="frag-card-inner"><div class="frag-img-wrap"></div><div class="frag-info"><p class="frag-num">NO. '+a[0]+'</p><h3 class="frag-name-en">'+a[1]+'</h3><p class="frag-name-cn">'+a[2]+'</p><p class="frag-accord"><b>Top</b> '+a[3]+'<br><b>Heart</b> '+a[4]+'<br><b>Base</b> '+a[5]+'</p></div></div></div>\n'
panels_html += '</div><div class="showcase-toggle-wrap"><button class="showcase-toggle narrative-toggle" data-target="narrative-after">展开叙事</button></div><div class="showcase-body collapsed" id="narrative-after" style="max-width:900px;margin:0 auto;padding:2rem;text-align:center"><div style="padding:3rem 2rem;background:rgba(255,254,253,.1);backdrop-filter:blur(20px);border:1px solid rgba(184,148,62,.04);border-radius:6px;font-family:Noto Serif SC,serif;font-size:.9rem;font-weight:300;color:var(--ink3);line-height:2.5">雨后 的深度叙事即将呈现。<br>每一场雨都有自己的故事。</div></div></div>\n'

c = c[:sec_close] + panels_html + c[sec_close:]

# ============================================================
# STEP 12: Update nav links in original nav
# ============================================================
# Actually the original had nav-links - let me update them to point to new sections
# Already have top-nav added. The original nav-links are in a <nav> element.
# We can leave them or simplify them. The top-nav is the main navigation now.

# ============================================================
# WRITE
# ============================================================
open('C:/Users/Ara/rain-website/index.html', 'w', encoding='utf-8').write(c)
print(f"FINAL SIZE: {len(c)} chars")
print(f"Script tags: {c.count('<script>')} / {c.count('</script>')}")
print(f"Sections: {c.count('<section')}")
print(f"Toggles: {c.count('narrative-toggle')}")
print(f"Bodies: {c.count('showcase-body')}")
