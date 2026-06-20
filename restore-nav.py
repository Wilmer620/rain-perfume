# Restore nav, tabs, craft, founders, music to index.html
with open('C:/Users/Ara/rain-website/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. top-nav CSS + series-tabs CSS
topnav_css = '''
.top-nav{display:flex;gap:2.5rem;list-style:none;position:fixed;top:1.6rem;right:3.5rem;z-index:100}
.top-nav a{color:var(--ink3);text-decoration:none;font-family:Inter,sans-serif;font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;transition:all .4s;position:relative}
.top-nav a:hover{color:var(--gold)}.top-nav a::after{content:"";position:absolute;bottom:-4px;left:50%;width:3px;height:3px;border-radius:50%;background:var(--gold);transform:translateX(-50%) scale(0);transition:transform .35s}
.top-nav a.active{color:var(--ink)}.top-nav a.active::after{transform:translateX(-50%) scale(1)}
.series-tabs{display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap;margin:2rem 0 1rem;padding:0 1rem}
.series-tab{font-family:Cormorant Garamond,serif;font-size:.95rem;font-weight:400;letter-spacing:.1em;color:var(--ink3);background:none;border:none;padding:.6rem 1.2rem;cursor:none;position:relative;transition:color .4s}
.series-tab::after{content:"";position:absolute;bottom:0;left:0;right:0;height:1px;background:var(--gold);transform:scaleX(0);transition:transform .4s}
.series-tab.active{color:var(--ink)}.series-tab.active::after{transform:scaleX(1)}.series-tab:hover{color:var(--ink2)}
.sec-label{text-align:center;padding:2rem 2rem 0}.sec-label-k{font-family:Inter,sans-serif;font-size:.54rem;letter-spacing:.5em;color:var(--gold-d);text-transform:uppercase;margin-bottom:.8rem}
.sec-label-t{font-family:Cormorant Garamond,serif;font-size:clamp(1.8rem,3.5vw,2.5rem);font-weight:400;letter-spacing:.1em;color:var(--ink)}
@media (max-width:1080px){.top-nav{display:none}.series-tabs{gap:.8rem}.series-tab{font-size:.8rem}}
'''
c = c.replace('@keyframes breathe{', topnav_css + '@keyframes breathe{')

# 2. Add top-nav HTML + RAIN logo + series hub + tabs
c = c.replace('<section class="phil" id="phil">',
    '<div class="sec-label reveal"><p class="sec-label-k">01</p><h2 class="sec-label-t">品牌哲学</h2></div>\n<section class="phil" id="phil">')

# Insert RAIN logo + top-nav before <nav class="nav"
c = c.replace('<nav class="nav" id="nav">',
    '<div style="position:fixed;top:1.6rem;left:3.5rem;z-index:100;font-family:Cormorant Garamond,serif;font-size:1.35rem;font-weight:500;letter-spacing:.35em;color:var(--ink);text-transform:uppercase">RAIN</div><ul class="top-nav" id="topNav"><li><a href="#phil">品牌哲学</a></li><li><a href="#series">产品介绍</a></li><li><a href="#craft">制香之道</a></li><li><a href="#founders">主理人手记</a></li><li><a href="#quiz">寻雨之路</a></li><li><a href="#newsletter">降雨预报</a></li></ul>\n<nav class="nav" id="nav">')

# Find phil end and insert series hub between phil and collection
phil_end = c.find('</section>', c.find('id="phil"'))
divider_pos = c.find('<section class="section-divider', phil_end)

series_hub = '''</section>
<section class="section-divider reveal"><div class="section-divider-inner"><span class="section-divider-dot"></span></div></section>
<div class="sec-label reveal"><p class="sec-label-k">02</p><h2 class="sec-label-t">雨的衍生</h2></div>
<section class="series-hub reveal" id="series"><p style="font-family:Inter,sans-serif;font-size:.54rem;letter-spacing:.5em;color:var(--gold-d);text-transform:uppercase;margin-bottom:1.5rem">The Rain Derivatives</p><h2 style="font-family:Cormorant Garamond,serif;font-size:clamp(1.8rem,3.5vw,2.5rem);font-weight:400;letter-spacing:.1em;color:var(--ink);margin-bottom:.5rem">Product Lines</h2><p style="font-family:Inter,sans-serif;font-size:.54rem;letter-spacing:.5em;color:var(--gold-d);text-transform:uppercase;margin-top:.5rem">产品主题介绍</p><p style="font-family:Noto Serif SC,serif;font-size:.82rem;font-weight:300;color:var(--ink3);letter-spacing:.06em;line-height:2.2;max-width:520px;margin:1rem auto 0">每一场雨都有自己的性格，不同种进入自己的方式。</p></section>
<div class="series-tabs reveal"><button class="series-tab active" data-panel="sojourn">驻足苦旅</button><button class="series-tab" data-panel="world">世界之色</button><button class="series-tab" data-panel="feast">灵感盛宴</button><button class="series-tab" data-panel="seasons">四季所生</button><button class="series-tab" data-panel="after">雨后</button></div>
'''
c = c[:divider_pos] + series_hub + c[divider_pos:]

# 3. Add craft + founders before quiz
quiz_pos = c.find('<section class="quiz"')
craft_html = '''<section class="section-divider reveal"><div class="section-divider-inner"><span class="section-divider-dot"></span></div></section>
<div class="sec-label reveal"><p class="sec-label-k">03</p><h2 class="sec-label-t">制香之道</h2></div>
<section class="craft reveal" id="craft"><div class="craft-grid"><div class="craft-card"><span class="craft-card-num">01</span><h4>冷萃 · 锁住第一缕气息</h4><p>在低温下将植物原料浸入有机甘蔗酒精中，持续 72 小时。冷萃不是为了快——是为了抓住最脆弱的前调分子。</p></div><div class="craft-card"><span class="craft-card-num">02</span><h4>静置 · 让时间完成配方</h4><p>混合后的液体在恒温暗室中静置 4–8 周。每一天，分子都在重新组合。这不是等待——是让时间成为调香师。</p></div><div class="craft-card"><span class="craft-card-num">03</span><h4>微滤 · 只留下光的重量</h4><p>经过多层微米级过滤，去除残留的植物蜡质，却不带走任何香气分子。最终的液体透明如雨。</p></div></div></section>
<section class="section-divider reveal"><div class="section-divider-inner"><span class="section-divider-dot"></span></div></section>
<div class="sec-label reveal"><p class="sec-label-k">04</p><h2 class="sec-label-t">主理人手记</h2></div>
<section class="founders-note reveal" id="founders"><div class="founders-inner glass-panel"><p class="founders-kicker">A Letter from the Founder</p><p class="founders-text"><em>我一直在找一种气味。</em><br>不是那种走进房间就能被认出来的——<br>而是你在雨天窗边发呆时，<br>自己都不确定自己闻到了什么的那种。<br><br>2025 年冬天，我们做了 RAIN。<br>不是想做一个香水品牌。我们只是想：<br>如果有人能把<em>雨停之后那一分钟的安静</em>收集起来，<br>世界上会不会多一种温柔。<br><br>我们没有答案。但我们会一直做下去。</p><p class="founders-sign">— RAIN 主理人</p></div></section>
'''
c = c[:quiz_pos] + craft_html + c[quiz_pos:]

# 4. Add music button before back-top
c = c.replace('<button class="back-top"',
    '<button class="music-btn" id="musicBtn"><svg viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg></button>\n<button class="back-top"')

# 5. Add JS: top-nav active + series tab switching + narrative toggle + music
js_patch = '''
var topNavLinks=document.querySelectorAll(".top-nav a"),allSections=document.querySelectorAll("section[id]");function updateNav(){var y=window.scrollY+window.innerHeight/3,cur="";allSections.forEach(function(s){if(y>=s.offsetTop)cur=s.getAttribute("id")});topNavLinks.forEach(function(a){a.classList.toggle("active",a.getAttribute("href")==="#"+cur)})}window.addEventListener("scroll",updateNav,{passive:true});updateNav();
var seriesTabs=document.querySelectorAll(".series-tab"),seriesPanels=document.querySelectorAll(".series-panel");seriesTabs.forEach(function(tab){tab.addEventListener("click",function(){seriesTabs.forEach(function(t){t.classList.remove("active")});tab.classList.add("active");seriesPanels.forEach(function(p){p.classList.remove("active")});var target=document.querySelector('.series-panel[data-panel="'+tab.dataset.panel+'"]');if(target)target.classList.add("active")})});
document.querySelectorAll(".narrative-toggle").forEach(function(btn){var body=document.getElementById(btn.dataset.target),open=false;if(!body)return;body.style.maxHeight="0";body.classList.add("collapsed");btn.addEventListener("click",function(){if(open){body.style.maxHeight="0";body.classList.add("collapsed");btn.textContent="展开叙事";open=false}else{body.style.maxHeight=body.scrollHeight+"px";body.classList.remove("collapsed");btn.textContent="收起叙事";open=true}})});
(function(){var btn=document.getElementById("musicBtn"),playing=false,ctx=null,gain=null;if(!btn)return;function noiseNode(){var buf=ctx.createBuffer(1,ctx.sampleRate*3,ctx.sampleRate),d=buf.getChannelData(0);for(var i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*0.5;var s=ctx.createBufferSource();s.buffer=buf;s.loop=true;return s}btn.addEventListener("click",function(){if(!ctx){ctx=new(window.AudioContext||window.webkitAudioContext)();gain=ctx.createGain();gain.gain.value=0;gain.connect(ctx.destination)}if(playing){gain.gain.linearRampToValueAtTime(0,ctx.currentTime+0.3);btn.style.borderColor="";btn.style.boxShadow="";playing=false}else{var n1=noiseNode(),f1=ctx.createBiquadFilter();f1.type="lowpass";f1.frequency.value=350;var n2=noiseNode(),f2=ctx.createBiquadFilter();f2.type="lowpass";f2.frequency.value=600;var n3=noiseNode(),f3=ctx.createBiquadFilter();f3.type="bandpass";f3.frequency.value=2000;f3.Q.value=0.5;n1.connect(f1);f1.connect(gain);n2.connect(f2);f2.connect(gain);n3.connect(f3);f3.connect(gain);n1.start();n2.start();n3.start();gain.gain.linearRampToValueAtTime(0.22,ctx.currentTime+0.3);btn.style.borderColor="var(--gold)";btn.style.boxShadow="0 0 16px rgba(184,148,62,.25)";playing=true}})})();
'''

# Insert after entrance JS
js_marker = 'entranceEl.addEventListener("click",function(){entranceEl.classList.add("out")})'
c = c.replace(js_marker, js_marker + js_patch)

# Add interactive elements to cursor list
c = c.replace('.nl-toggle-btn', '.nl-toggle-btn,.music-btn,.top-nav a,.series-tab')

open('C:/Users/Ara/rain-website/index.html', 'w', encoding='utf-8').write(c)
print('Restore complete')
print('Size:', len(c))
print('top-nav:', c.count('top-nav'))
print('series-tab:', c.count('series-tab'))
print('craft:', c.count('class="craft"'))
print('founders:', c.count('founders-note'))
print('music:', c.count('musicBtn'))
print('sec-label:', c.count('sec-label'))
