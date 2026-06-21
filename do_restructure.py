"""One-shot: reorder sections + add 雨时 carousel + update nav"""
import re

with open('build-final.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Evaluate COMING_SOON_SVG
cs_start = c.find("COMING_SOON_SVG = ")
cs_end = c.find("\n", cs_start)
cs_line = c[cs_start:cs_end]
local_vars = {}
exec(cs_line, {}, local_vars)
COMING_SOON_SVG = local_vars['COMING_SOON_SVG']

# === STEP 1: Extract all section blocks ===
# Find the HTML template boundaries
html_start = c.find("html = f'''")
html_tq_start = c.find("'''", html_start + 10) + 3
html_end = c.rfind("'''")  # before <script>
before_html = c[:html_tq_start]
after_html = c[html_end:]

template = c[html_tq_start:html_end]

# Section markers in current position
markers_orig = [
    "<!-- 01 · 雨之思 -->",
    "<!-- 02 · 雨的衍生 -->",
    "<!-- 03 · 臻品雨酿 -->",
    "<!-- 04 · 雨的贮存指南 -->",
    "<!-- 05 · 雨的观察日记 -->",
    "<!-- 06 · 寻雨之路 -->",
    "<!-- 07 · 降雨预报 -->",
]

# Find their positions
positions = []
for m in markers_orig:
    idx = c.find(m, html_tq_start)
    if idx >= 0:
        positions.append(idx - html_tq_start)

# Extract blocks
blocks = {}
names = ['phil', 'series', 'collection', 'craft', 'diary', 'quiz', 'newsletter']
for i, name in enumerate(names):
    start = positions[i]
    end = positions[i+1] if i+1 < len(names) else len(template)
    blocks[name] = template[start:end]

# New section order: 雨时 → 衍生 → 臻品 → 寻雨 → 雨之思 → 贮存 → 日记 → 降雨
new_order_names = ['series', 'collection', 'quiz', 'phil', 'craft', 'diary', 'newsletter']

# Build new template
new_template = template[:positions[0]]  # everything before first section

# Add 雨时
rain_time_html = '''
<!-- 01 · 雨时 -->
<div class="sec-label reveal"><p class="num">01</p><h2 class="title">雨时</h2><p class="sec-en">Moments of Rain</p></div>
<section class="rain-time reveal" id="rainTime">
<div class="rain-time-inner glass-panel" style="padding:2rem 2.5rem">
<div class="rt-img-wrap"><img class="rt-img" id="rtImg" src="" alt=""></div>
<div class="rt-info"><span class="rt-tag" id="rtTag"></span><h3 class="rt-name" id="rtName"></h3><p class="rt-cn" id="rtCn"></p></div>
<div class="rt-tabs" id="rtTabs">
<button class="rt-tab active" data-si="0">驻足苦旅</button>
<button class="rt-tab" data-si="1">世界之色</button>
<button class="rt-tab" data-si="2">灵感盛宴</button>
<button class="rt-tab" data-si="3">宙宇寰星</button>
<button class="rt-tab" data-si="4">四季所生</button>
<button class="rt-tab" data-si="5">雨后</button>
</div>
</div>
</section>

<section class="section-divider reveal"><div class="section-divider-inner"></div></section>

'''

num = 2
renumbered_blocks = []
for name in new_order_names:
    block = blocks[name]
    # Replace section comment with new number
    old_comment = re.search(r'<!-- \d+ · ([^-]+) -->', block)
    if old_comment:
        block = block.replace(old_comment.group(0), f'<!-- {num:02d} · {old_comment.group(1).strip()} -->')
    # Replace sec-label num
    block = re.sub(r'<p class="num">\d+</p>', f'<p class="num">{num:02d}</p>', block, count=1)
    renumbered_blocks.append(block)
    num += 1

# Insert after rain_time_html
for block in renumbered_blocks:
    rain_time_html += block

new_template += rain_time_html

# === Update nav links ===
# Desktop
old_desktop = '''<li><a href="#phil">雨之思</a></li>
<li><a href="#series">雨的衍生</a></li>
<li><a href="#collection">臻品雨酿</a></li>
<li><a href="#craft">雨的贮存指南</a></li>
<li><a href="#founders">雨的观察日记</a></li>
<li><a href="#quiz">寻雨之路</a></li>
<li><a href="#newsletter">降雨预报</a></li>'''

new_desktop = '''<li><a href="#rainTime">雨时</a></li>
<li><a href="#series">雨的衍生</a></li>
<li><a href="#collection">臻品雨酿</a></li>
<li><a href="#quiz">寻雨之路</a></li>
<li><a href="#phil">雨之思</a></li>
<li><a href="#craft">雨的贮存指南</a></li>
<li><a href="#founders">雨的观察日记</a></li>
<li><a href="#newsletter">降雨预报</a></li>'''
new_template = new_template.replace(old_desktop, new_desktop)

# Mobile
old_mobile = '''<a href="#phil">雨之思</a>
<a href="#series">雨的衍生</a>
<a href="#collection">臻品雨酿</a>
<a href="#craft">雨的贮存指南</a>
<a href="#founders">雨的观察日记</a>
<a href="#quiz">寻雨之路</a>
<a href="#newsletter">降雨预报</a>'''

new_mobile = '''<a href="#rainTime">雨时</a>
<a href="#series">雨的衍生</a>
<a href="#collection">臻品雨酿</a>
<a href="#quiz">寻雨之路</a>
<a href="#phil">雨之思</a>
<a href="#craft">雨的贮存指南</a>
<a href="#founders">雨的观察日记</a>
<a href="#newsletter">降雨预报</a>'''
new_template = new_template.replace(old_mobile, new_mobile)

# Rebuild
result = before_html + new_template + after_html

# === Add CSS for rain-time ===
old_css = "/* ══ Philosophy ══ */"
new_css = """/* ══ Rain Time ══ */
.rain-time{position:relative;z-index:2;text-align:center;padding:2.5rem 2rem 3rem;overflow:hidden}
.rain-time-inner{max-width:700px;margin:0 auto}
.rt-img-wrap{position:relative;width:100%;aspect-ratio:3/2;margin:0 auto 1.2rem;overflow:hidden;border-radius:4px;background:rgba(184,148,62,.02);display:flex;align-items:center;justify-content:center}
.rt-img{width:100%;height:100%;object-fit:contain;transition:opacity .4s ease,transform .4s ease}
.rt-img.fade{opacity:0;transform:scale(1.03)}
.rt-info{min-height:3em}
.rt-info .rt-name{font-family:'Cormorant Garamond',serif;font-size:1.1rem;font-weight:400;letter-spacing:.12em;color:var(--ink);margin-bottom:.15rem}
.rt-info .rt-cn{font-family:'Noto Serif SC',serif;font-size:.75rem;font-weight:300;color:var(--ink3);letter-spacing:.1em}
.rt-info .rt-tag{display:inline-block;font-family:'Inter',sans-serif;font-size:.42rem;letter-spacing:.25em;color:var(--gold-d);background:rgba(184,148,62,.05);border:1px solid rgba(184,148,62,.08);border-radius:100px;padding:.12rem .6rem;margin-bottom:.4rem;text-transform:uppercase}
.rt-tabs{display:flex;justify-content:center;gap:.4rem;flex-wrap:wrap;margin-top:1rem}
.rt-tab{font-family:'Noto Serif SC',serif;font-size:.62rem;font-weight:300;letter-spacing:.06em;color:var(--ink3);background:rgba(255,253,250,.15);border:1px solid rgba(184,148,62,.04);border-radius:100px;padding:.25rem .75rem;cursor:none;transition:all .3s}
.rt-tab:hover{color:var(--ink2);border-color:rgba(184,148,62,.1)}
.rt-tab.active{color:var(--gold-d);border-color:var(--gold);background:rgba(184,148,62,.05)}
@media (max-width:768px){.rain-time{padding:2rem 1rem 2.5rem}.rt-tab{font-size:.55rem;padding:.2rem .6rem}}

/* ══ Philosophy ══ */"""
result = result.replace(old_css, new_css, 1)

# === Add carousel JS ===
cs_escaped = COMING_SOON_SVG.replace('\\', '\\\\').replace("'", "\\'")
carousel_js = f"""/* Rain Time Carousel */
(function(){{
var cs='{cs_escaped}';
var seriesImgs=[
  [{{n:'Blur',c:'花非花·雾非雾',t:'驻足苦旅',i:cs}},{{n:'Knot',c:'结',t:'驻足苦旅',i:cs}},{{n:'Flirt',c:'风骚',t:'驻足苦旅',i:cs}},{{n:'Peak',c:'摩登巅',t:'驻足苦旅',i:cs}},{{n:'Wall',c:'围城',t:'驻足苦旅',i:cs}},{{n:'Leave',c:'再别',t:'驻足苦旅',i:cs}},{{n:'Iris',c:'瞳孔',t:'驻足苦旅',i:cs}},{{n:'Sun&Moon',c:'日月煎',t:'驻足苦旅',i:cs}}],
  [{{n:'Pulse',c:'脉搏',t:'世界之色',i:cs}},{{n:'Our Melody',c:'共鸣',t:'世界之色',i:'images/03-our-melody.webp'}},{{n:'Last Word',c:'明日',t:'世界之色',i:'images/02-last-word.webp'}},{{n:'Respiration',c:'光合',t:'世界之色',i:'images/01-respiraton.webp'}},{{n:'Rising Sunset',c:'潮汐',t:'世界之色',i:'images/04-rising-sunset.webp'}},{{n:'Past Dream',c:'旧心事',t:'世界之色',i:'images/05-past-dream.webp'}},{{n:'Prejudice',c:'我独我',t:'世界之色',i:'images/06-prejudice.webp'}}],
  [{{n:'Face',c:'皮囊',t:'灵感盛宴',i:cs}},{{n:'Gone',c:'隐身衣',t:'灵感盛宴',i:cs}},{{n:'Wait',c:'等待',t:'灵感盛宴',i:cs}},{{n:'Bliss',c:'欢愉',t:'灵感盛宴',i:cs}},{{n:'Stay',c:'侍者',t:'灵感盛宴',i:cs}},{{n:'Decree',c:'号令',t:'灵感盛宴',i:cs}}],
  [{{n:'Flash',c:'瞬息',t:'宙宇寰星',i:cs}},{{n:'Present',c:'此刻',t:'宙宇寰星',i:cs}},{{n:'Bygone',c:'彼时',t:'宙宇寰星',i:cs}},{{n:'Lightyear',c:'光年',t:'宙宇寰星',i:cs}},{{n:'Origin',c:'起源',t:'宙宇寰星',i:cs}}],
  [{{n:'Spring',c:'破土·呼吸',t:'四季所生',i:cs}},{{n:'Summer',c:'疯长·蔓延',t:'四季所生',i:cs}},{{n:'Autumn',c:'沉淀·入静',t:'四季所生',i:cs}},{{n:'Winter',c:'封存·等待',t:'四季所生',i:cs}}],
  [{{n:'Fall',c:'自天穹',t:'雨后',i:cs}},{{n:'Drift',c:'穿云间',t:'雨后',i:cs}},{{n:'Shatter',c:'碎地霜',t:'雨后',i:cs}}]
];
var img=document.getElementById('rtImg'),name=document.getElementById('rtName'),cn=document.getElementById('rtCn'),tag=document.getElementById('rtTag'),tabs=document.querySelectorAll('.rt-tab');
var si=Math.floor(Math.random()*6),pi=0,timer=null;
function show(){{
  var s=seriesImgs[si],p=s[pi];
  img.src=p.i;img.classList.add('fade');img.alt=p.n;
  setTimeout(function(){{img.classList.remove('fade')}},50);
  name.textContent=p.n;cn.textContent=p.c;tag.textContent=p.t;
  tabs.forEach(function(t){{t.classList.toggle('active',parseInt(t.dataset.si)===si)}});
}}
function next(){{
  var s=seriesImgs[si];
  if(pi<s.length-1){{pi++}}else{{si=(si+1)%6;pi=0}}
  show();
}}
function startTimer(){{clearInterval(timer);timer=setInterval(next,2000)}}
tabs.forEach(function(t){{
  t.addEventListener('click',function(){{si=parseInt(this.dataset.si);pi=0;show();startTimer()}})
}});
show();startTimer();
}})();

/* Hero Typewriter */"""
result = result.replace('/* Hero Typewriter */', carousel_js, 1)

# === Add 8th child delay for mobile nav ===
old_mob_css = '.mob-nav a:nth-child(7){transition-delay:.42s}'
new_mob_css = '.mob-nav a:nth-child(7){transition-delay:.42s}\n.mob-nav a:nth-child(8){transition-delay:.48s}'
result = result.replace(old_mob_css, new_mob_css, 1)

with open('build-final.py', 'w', encoding='utf-8') as f:
    f.write(result)

print("All done!")
print(f"COMING_SOON_SVG length: {len(COMING_SOON_SVG)}")
