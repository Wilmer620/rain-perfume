"""Generate 6 collection detail pages + update build-final.py with collection_card()."""
import subprocess as sp, os

# ═══════════════════════════════════════════
# DATA for 6 collection products
# ═══════════════════════════════════════════
COLLECTION = [
    dict(slug='figment', cn='我故臆想', en_short='Figment', en_full='The Fable I Tell Myself',
         series_en='SOJOURN', series_cn='驻足苦旅', poster_tag='典藏臻酿 · 忆中虚构',
         rain_tag='雨，落在记忆重写的虚构之夜。', note_type='木质东方调',
         top='当归 · 没药 · 粉红胡椒', heart='鸢尾 · 紫罗兰 · 纸莎草', base='檀木 · 香草 · 安息香',
         narrative='记忆从不负责记录——它负责<em>重新安排</em>。不是你回到了某个过去的时刻，是你带着现在全部的重量，把那个时刻<em>重写了一遍</em>。我故臆想取的正是这种精致的再造：一件从未发生的事、一句从未说出口的话、一个从未存在过的夜晚——但在你的叙述里，它们比真实还要<em>不可动摇</em>。它是关于「讲述」的香气——你如何讲述自己，你便如何成为自己。',
         chips=[('当归','根部最深的泥土气息——苦中带着回甘，像一段走了很远才理解的路。'),('没药','比乳香更深、更古老——古埃及人用它保存永恒，带着药感与神圣的暗色。'),('纸莎草','干燥的书写材料——每个字都见过光，每个字都在等一个人来读。'),('安息香','琥珀色的树脂——温暖到让人闭上眼睛，是所有故事最温柔的句号。')]),
    dict(slug='adorn', cn='着我之境', en_short='Adorn', en_full='The World Through Me',
         series_en='WORLD', series_cn='世界之色', poster_tag='典藏臻酿 · 身体美术馆',
         rain_tag='雨，落在身体美术馆的每一幅画框上。', note_type='花香皮革调',
         top='苦橙叶 · 白松香 · 粉红胡椒', heart='土耳其玫瑰 · 沉香 · 番红花', base='皮革 · 琥珀 · 苏合香',
         narrative='你不是一块接收光线的幕布——你是<em>改变光线</em>的介质。同一片天空穿过不同的人，折射成完全不同的颜色。着我之境捕捉的正是这种穿透与偏折——你不必去冒险去远方，你已经是一座<em>行走的美术馆</em>：大海在你皮肤上留下盐的刻度，古老街道在你衣领里藏了灰。你不是看过世界——你<em>就是</em>世界被看的方式。',
         chips=[('苦橙叶','橙花树下被碾碎的叶——青绿、微苦、清醒，像第一次独自出远门时吸入的第一口空气。'),('土耳其玫瑰','必须在天亮前手工采摘——玫瑰中的玫瑰，浓而不艳，近而不逼。'),('苏合香','来自东方的树脂——甜中带辛，像一段跨越大洲的记忆，熟悉又陌生。'),('皮革','鞣制过的皮面气息——粗粝、干燥、带着体温，是所有远方统一的底色。')]),
    dict(slug='tonight', cn='今夜唯我', en_short='Tonight', en_full='Tonight, Only I Remain',
         series_en='FEAST', series_cn='灵感盛宴', poster_tag='典藏臻酿 · 午夜款待',
         rain_tag='雨，落在所有人离去之后的寂静里。', note_type='美食木香调',
         top='香槟调 · 杜松 · 柑橘皮', heart='鸢尾 · 烟草 · 黑巧克力', base='愈创木 · 皮革 · 麝香',
         narrative='派对的高潮不在杯盏之间——在<em>所有的人都走了以后</em>。你解开领口的第一颗扣子，空气忽然多了三分米的体积。没有什么需要庆祝了——<em>安静本身</em>就是庆祝。今夜唯我捕捉的正是这最终的一刻——不挽留热闹，不与任何人为伍，房间空了之后你第一次听见自己的呼吸。这不是孤独——这是所有社交结束之后，你<em>还给自己的款待</em>。',
         chips=[('香槟调','气泡破裂时释放的微醺——欢庆的开场但不喧哗，是克制后的自由。'),('烟草','烟叶在指尖揉碎时的气息——干燥、微甜、带着成年人的安静与克制。'),('黑巧克力','可可含量80%以上的苦甜——复杂的愉悦，不是每个人都懂，但懂的人会笑。'),('愈创木','南美洲密度最大的硬木——沉于水，是所有轻浮的反面，是最安静的坚定。')]),
    dict(slug='entropy', cn='熵增时', en_short='Entropy', en_full='The Hour of Entropy',
         series_en='COSMOS', series_cn='宙宇寰星', poster_tag='典藏臻酿 · 秩序散落',
         rain_tag='雨，落在秩序散落后的自由粒子间。', note_type='醛香木调',
         top='醛香 · 臭氧 · 薄荷', heart='鸢尾 · 没药 · 焚香', base='白麝香 · 琥珀 · 矿物调',
         narrative='一切秩序的尽头不是<em>毁灭</em>——是<em>散落</em>。当所有结构被温和地松开，当每一个曾经聚拢的瞬间回到它们各自的轨道——这不是终结，是<em>归还</em>。熵增时捕捉的是宙宇寰星五支各自抵达<em>热力学终点</em>之后的形态：瞬息不再是一个空拍，而是<em>永恒中的第一个毫秒</em>；此刻不再抓紧现在，而是允许一切的<em>流逝</em>；彼时将记忆交还给时间；光年把目光收回闭上；起源回到未命名的混沌。所有的事物回归它们<em>未被整理</em>的样子——不是混乱，是<em>自由</em>。',
         chips=[('醛香','人工合成的第一缕明亮——像刚熨过的白衬衫，干净到发出声响。'),('鸢尾','根茎需陈化数年才能提取——气味如粉状紫罗兰，却更深邃，像一段被时间打磨过的记忆。'),('白麝香','干净的棉布贴在皮肤上——是所有香气最终回归的地方，不争不抢。'),('琥珀','松脂历经千万年而成——把时间封存在金色的透明里，是大地最古老的记忆。')]),
    dict(slug='migration', cn='新时代迁流', en_short='Migration', en_full='The River of Seasons',
         series_en='SEASONS', series_cn='四季所生', poster_tag='典藏臻酿 · 岁时坐标',
         rain_tag='雨，落在四季流过的河面上。', note_type='绿意花香调',
         top='竹叶 · 薄荷 · 柑橘', heart='桂花 · 白茶 · 紫藤', base='白麝香 · 檀木 · 米浆',
         narrative='你不随时间流逝——时间<em>从你身上流过</em>。春雨在你的左手虎口发芽，夏阳从你的右肩倾斜而下，秋风在你的脚踝处打着旋，冬雪从你头顶落下，却从未真正触碰你。你站在河中央。<em>不增不减。</em>新时代迁流不是一支关于时间的香——它是一个<em>在时间之外的坐标</em>：此刻，此身，此在。四季从你身边经过，你不动——你<em>就是</em>四季经过的方式。',
         chips=[('竹叶','清晨竹叶上的露水被风吹散——清、冷、一直向上，不争不抢却从不停止。'),('紫藤','春夏之交悬挂的花穗——淡紫到几乎透明，香气却让你走过时一定回头。'),('米浆','石磨碾过米粒时溢出的白色液体——最朴素的安全感，每个人都认得。'),('檀木','寺庙里多年的香火记忆——是时间最温柔的证明，让人想把呼吸放慢。')]),
    dict(slug='renew', cn='致新生', en_short='Renew', en_full='To What Comes Next',
         series_en='AFTER', series_cn='雨后', poster_tag='典藏臻酿 · 未来首句',
         rain_tag='雨，落在推开窗户后的第一口空气里。', note_type='清新绿调',
         top='绿叶 · 佛手柑 · 薄荷', heart='铃兰 · 白茶 · 蕨类', base='白麝香 · 雪松 · 琥珀',
         narrative='最重要的时刻不是结束——是<em>结束之后的第一个瞬间</em>。雨停了。你不确定接下来会发生什么——但你已经在<em>准备吸气</em>了。致新生守在一个模棱两可的临界点上：旧的一页尚未完全翻过，新的一行还没写下。它不是写给过去的悼词——它是写给空气里<em>即将到来的事物</em>的第一句问候。你不需要知道那是什么。你只需要<em>推开窗户</em>。',
         chips=[('铃兰','山谷里最早开的花——细小、洁白，香气却可以穿透整片森林，清而不淡。'),('蕨类','森林底层的古老植物——比花更安静，比树更久远，是所有新生的底床。'),('白麝香','干净的棉布贴在皮肤上——是所有香气最终回归的地方，不争不抢。'),('琥珀','松脂历经千万年而成——把时间封存在金色的透明里，是大地最古老的记忆。')]),
]

# ═══════════════════════════════════════════
# CSS + shared HTML for detail pages
# ═══════════════════════════════════════════
DETAIL_CSS = '''<style>:root{--bg:#fdf9ef;--ink:#2b2722;--ink2:#5c5750;--ink3:#8a857b;--gold:#b8943e;--gold-d:#8b691e}*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}html{font-size:16px;scroll-behavior:smooth}body{font-family:Inter,"Noto Serif SC",sans-serif;background:var(--bg);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}a{text-decoration:none!important}.nav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:.65rem 1.5rem;background:rgba(253,249,239,.94);backdrop-filter:blur(16px);border-bottom:1px solid rgba(184,148,62,.06)}.nav-links{display:flex;gap:.7rem;flex-wrap:wrap}.nav-links a{font-family:"Noto Serif SC",serif;font-size:.62rem;color:var(--ink3);letter-spacing:.04em}.nav-links a:hover{color:var(--gold)}.bc{padding:4.2rem 1.5rem .2rem;max-width:960px;margin:0 auto}.bc a,.bc span{font-size:.6rem;color:var(--ink3);opacity:.45}.bc a:hover{opacity:1;color:var(--gold)}.bc span{margin:0 .25rem;opacity:.25}.hero{max-width:960px;margin:.8rem auto 1.8rem;padding:0 1.5rem}.hero-bg{padding:2.2rem 1.8rem;border-radius:14px;position:relative;overflow:hidden}.hero-cn{font-family:"Noto Serif SC",serif;font-size:1.7rem;color:var(--ink);letter-spacing:.07em;font-weight:600;position:relative;z-index:1}.hero-en{font-family:Georgia,serif;font-size:.65rem;color:var(--ink3);opacity:.3;letter-spacing:.1em;margin-top:.15rem;position:relative;z-index:1}.hero-rain{font-family:"Noto Serif SC",serif;font-size:.65rem;color:var(--gold);opacity:.6;font-style:italic;letter-spacing:.04em;margin-top:.35rem;position:relative;z-index:1}.hero-tags{display:flex;gap:.3rem;flex-wrap:wrap;margin-top:.5rem;position:relative;z-index:1}.hero-tag{font-size:.48rem;padding:.1rem .45rem;border-radius:100px;letter-spacing:.04em;border:1px solid rgba(184,148,62,.1);color:var(--ink3)}.notes{max-width:960px;margin:0 auto 1.8rem;padding:0 1.5rem}.notes-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.7rem}.nb{padding:.9rem .7rem;border-radius:10px;text-align:center}.nb .nbl{display:block;font-family:Inter,sans-serif;font-size:.4rem;text-transform:uppercase;letter-spacing:.08em;opacity:.3;margin-bottom:.25rem}.nb .nbt{font-family:"Noto Serif SC",serif;font-size:.58rem;color:var(--ink);font-weight:500;margin-bottom:.15rem}.top-bg{background:linear-gradient(135deg,rgba(212,182,96,.05),rgba(230,210,140,.01));border:1px solid rgba(212,182,96,.08)}.mid-bg{background:linear-gradient(135deg,rgba(184,148,62,.05),rgba(200,160,80,.01));border:1px solid rgba(184,148,62,.08)}.base-bg{background:linear-gradient(135deg,rgba(139,105,30,.03),rgba(160,120,50,.01));border:1px solid rgba(139,105,30,.06)}.narr{max-width:680px;margin:0 auto 2.2rem;padding:0 1.5rem}.narr-title{font-family:"Noto Serif SC",serif;font-size:.65rem;color:var(--gold);opacity:.4;text-align:center;letter-spacing:.08em;margin-bottom:1rem}.narr-text{font-family:"Noto Serif SC",serif;font-size:.62rem;color:var(--ink2);line-height:2.1;letter-spacing:.03em}.narr-text em{font-style:normal;color:var(--gold);font-weight:500}.narr-text p{margin-bottom:.9rem}.chips{max-width:880px;margin:0 auto 2.2rem;padding:0 1.5rem}.chips-title{font-family:"Noto Serif SC",serif;font-size:.62rem;color:var(--ink);text-align:center;letter-spacing:.05em;margin-bottom:.7rem}.chips-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:.45rem}.chip{padding:.55rem .7rem;background:rgba(255,253,250,.35);border:1px solid rgba(184,148,62,.05);border-radius:8px}.chip-name{font-family:"Noto Serif SC",serif;font-size:.52rem;color:var(--ink);font-weight:500;margin-bottom:.12rem}.chip-desc{font-family:"Noto Serif SC",serif;font-size:.46rem;color:var(--ink2);line-height:1.7;opacity:.7}.snav{max-width:960px;margin:2.2rem auto 1.8rem;padding:0 1.5rem}.snav-title{font-family:"Noto Serif SC",serif;font-size:.62rem;color:var(--ink2);text-align:center;letter-spacing:.06em;margin-bottom:.7rem}.snav-cards{display:flex;gap:.35rem;overflow-x:auto;padding-bottom:.2rem;justify-content:center;flex-wrap:wrap}.snav-card{padding:.28rem .65rem;background:rgba(255,253,250,.3);border:1px solid rgba(184,148,62,.05);border-radius:100px;font-size:.52rem;color:var(--ink2);white-space:nowrap;font-family:"Noto Serif SC",serif}.snav-card:hover,.snav-card.cur{border-color:var(--gold);color:var(--gold);background:rgba(184,148,62,.04)}.snav-pn{display:flex;justify-content:center;gap:.7rem;margin-top:.6rem}.snav-pn a{font-family:"Noto Serif SC",serif;font-size:.58rem;color:var(--gold);padding:.28rem .9rem;border:1px solid rgba(184,148,62,.1);border-radius:100px}.snav-pn a:hover{background:rgba(184,148,62,.05);border-color:var(--gold)}.ret{text-align:center;margin:2.2rem 0 3rem}.ret a{font-family:"Noto Serif SC",serif;font-size:.62rem;color:var(--gold);padding:.4rem 1.6rem;border:1px solid rgba(184,148,62,.1);border-radius:100px}.ret a:hover{background:rgba(184,148,62,.05);border-color:var(--gold)}.rain-c{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.12}.ft{padding:2rem 1.5rem;text-align:center;border-top:1px solid rgba(184,148,62,.04)}.ft-text{font-size:.48rem;color:var(--ink3);opacity:.25;letter-spacing:.05em}@media(max-width:768px){.notes-grid{grid-template-columns:1fr}.chips-grid{grid-template-columns:1fr}.snav-cards{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start}}</style>'''

RAIN_JS = '''<script>(function(){var c=document.getElementById("rc"),x=c.getContext("2d"),w,h,d=[];function rs(){w=c.width=window.innerWidth;h=c.height=window.innerHeight;}rs();window.addEventListener("resize",rs);for(var i=0;i<20;i++)d.push({x:Math.random()*w,y:Math.random()*h,s:.5+Math.random()*2,l:5+Math.random()*15,o:.02+Math.random()*.04,w:(Math.random()-.5)*.15});function dr(){x.clearRect(0,0,w,h);d.forEach(function(r){x.beginPath();x.strokeStyle="rgba(184,148,62,"+r.o+")";x.moveTo(r.x,r.y);x.lineTo(r.x+r.w,r.y+r.l);x.lineWidth=.3;x.stroke();r.y+=r.s;if(r.y>h+r.l){r.y=-r.l;r.x=Math.random()*w;}});requestAnimationFrame(dr);}dr();})();</script>'''

NAV_HTML = '''<nav class="nav"><a href="/" class="nav-logo"><svg viewBox="0 0 260 64" width="110"><line x1="122" y1="4" x2="122" y2="18" stroke="#2b2722" stroke-width=".7" stroke-linecap="round"/><line x1="130" y1="2" x2="130" y2="20" stroke="#2b2722" stroke-width=".9" stroke-linecap="round"/><line x1="138" y1="6" x2="138" y2="16" stroke="#2b2722" stroke-width=".5" stroke-linecap="round"/><circle cx="130" cy="1" r=".8" fill="#b8943e"/><text x="130" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="22" letter-spacing="8" fill="#2b2722">RAIN</text></svg></a><div class="nav-links"><a href="/">首页</a><a href="/#series">雨的衍生</a><a href="/#collection">臻品雨釀</a><a href="/#quiz">寻雨之路</a><a href="/#simRain">模拟降雨</a></div></nav>'''

def gen_detail_page(d):
    """Generate a single collection detail page HTML."""
    # Build series nav chips (all 6 collection products)
    nav_chips = []
    for other in COLLECTION:
        cur_class = ' cur' if other['slug'] == d['slug'] else ''
        nav_chips.append('<a href="' + other['slug'] + '.html" class="snav-card' + cur_class + '">' + other['cn'] + '</a>')
    nav_chips_html = ''.join(nav_chips)

    # Build prev/next
    idx = COLLECTION.index(d)
    prev_html = next_html = ''
    if idx > 0:
        p = COLLECTION[idx - 1]
        prev_html = '<a href="' + p['slug'] + '.html">← ' + p['cn'] + '</a>'
    if idx < len(COLLECTION) - 1:
        n = COLLECTION[idx + 1]
        next_html = '<a href="' + n['slug'] + '.html">' + n['cn'] + ' →</a>'

    # Build chips
    chips_html = ''
    for name, desc in d['chips']:
        chips_html += '<div class="chip"><div class="chip-name">' + name + '</div><div class="chip-desc">' + desc + '</div></div>'

    # Build narrative
    narr = d['narrative']
    if not narr.startswith('<p'):
        narr = '<p>' + narr + '</p>'

    bg = 'background:linear-gradient(135deg,rgba(184,148,62,.06),rgba(253,249,239,.95))'

    html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">\n<title>' + d['cn'] + ' · ' + d['en_short'] + ' — RAIN | 臻品雨釀</title>\n' + DETAIL_CSS + '</head>\n<body>\n<canvas class="rain-c" id="rc"></canvas>\n' + NAV_HTML + '\n<div class="bc"><a href="/">首页</a><span>/</span><a href="/#collection">臻品雨釀</a><span>/</span><span>' + d['cn'] + '</span></div>\n<div class="hero"><div class="hero-bg" style="' + bg + '"><h1 class="hero-cn">' + d['cn'] + '</h1><p class="hero-en">' + d['en_short'] + '</p><p class="hero-rain">' + d['rain_tag'] + '</p><div class="hero-tags"><span class="hero-tag">' + d['note_type'] + '</span><span class="hero-tag">典藏臻釀</span><span class="hero-tag">' + d['series_cn'] + '</span></div></div></div>\n<div class="notes"><div class="notes-grid"><div class="nb top-bg"><span class="nbl">Top · 前调</span><span class="nbt">' + d['top'] + '</span></div><div class="nb mid-bg"><span class="nbl">Heart · 中调</span><span class="nbt">' + d['heart'] + '</span></div><div class="nb base-bg"><span class="nbl">Base · 尾调</span><span class="nbt">' + d['base'] + '</span></div></div></div>\n<div class="narr"><div class="narr-title">叙事</div><div class="narr-text">' + narr + '</div></div>\n<div class="chips"><div class="chips-title">香料解析</div><div class="chips-grid">' + chips_html + '</div></div>\n<div class="snav"><div class="snav-title">臻品雨釀 · 六支典藏</div><div class="snav-cards">' + nav_chips_html + '</div>\n<div class="snav-pn">' + prev_html + next_html + '</div></div>\n<div class="ret"><a href="/#collection">← 返回臻品雨釀</a></div>\n<div class="ft"><p class="ft-text">RAIN · Perfume as Rain</p></div>\n' + RAIN_JS + '\n</body></html>'
    return html

# ═══════════════════════════════════════════
# STEP 1: Generate detail pages
# ═══════════════════════════════════════════
print("=" * 60)
print("STEP 1: Generating 6 collection detail pages...")
for d in COLLECTION:
    path = os.path.join('perfume', d['slug'] + '.html')
    html = gen_detail_page(d)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("  OK " + d['slug'] + ".html (" + str(len(html)) + " bytes)")

# ═══════════════════════════════════════════
# STEP 2: Update build-final.py
# ═══════════════════════════════════════════
print("\nSTEP 2: Updating build-final.py...")
C = open('build-final.py', 'r', encoding='utf-8').read()

# 2a. Add collection_card() function before panel()
marker = "def panel(pid, cards_html, default_active=False, narrative=''):"
collection_card_func = """def collection_card(en, cn, series_en, series_cn, tag, top, heart, base):
  slug = en.lower().replace('&','and').replace(' ','-').replace("'","")
  img = POSTER_MAP.get(cn, COMING_SOON_SVG)
  return ('<a href="perfume/' + slug + '.html" class="frag-link" onclick="try{sessionStorage.setItem(\\'_rv\\',\\'1\\')}catch(e){}">'
    '<div class="frag-card collection-card" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)">'
    '<span class="corner c-tl"></span><span class="corner c-br"></span>'
    '<div class="frag-card-inner">'
    '<div class="frag-img-wrap"><span class="poster-badge">' + tag + '</span> <img class="frag-img frag-img-cs" src="' + img + '" alt="' + cn + '"></div>'
    '<div class="frag-info">'
    '<p class="frag-num">' + series_en + ' \\u00b7 ' + series_cn + '</p>'
    '<h3 class="frag-name-en" style="font-size:1.75rem">' + cn + '</h3>'
    '<p class="frag-name-cn">' + en + '</p>'
    '<p class="frag-accord"><b>Top</b> ' + top + '<br><b>Heart</b> ' + heart + '<br><b>Base</b> ' + base + '</p>'
    '<div class="fsr"><span class="fs2" data-en="' + en + '" data-cn="' + cn + '">&#9734;</span></div>'
    '</div></div></div></a>')

"""
C = C.replace(marker, collection_card_func + marker)
print("  Added collection_card() function")

# 2b. Replace hardcoded collection cards
# Find start: line with '<div class="frag-grid reveal">' followed by collection-card
grid_start_marker = '<div class="frag-grid reveal">\n<div class="frag-card collection-card"'
grid_start = C.find(grid_start_marker)
if grid_start == -1:
    print("  ERROR: Could not find collection grid start!")
    raise SystemExit(1)

# Find end: the closing </div> of the grid, followed by narrative_btn
# Pattern: </div>\n\n{narrative_btn('collection', 'Narr')}
grid_end_marker = "{narrative_btn('collection', 'Narr')}"
grid_end = C.find(grid_end_marker, grid_start)
if grid_end == -1:
    print("  ERROR: Could not find narrative_btn after grid!")
    raise SystemExit(1)

# Find the </div> just before narrative_btn
close_div = C.rfind('</div>', grid_start, grid_end)
if close_div == -1:
    print("  ERROR: Could not find closing </div>!")
    raise SystemExit(1)

# Build new grid
new_lines = ['<div class="frag-grid reveal">']
for d in COLLECTION:
    call = "{collection_card('" + d['en_short'] + "', '" + d['cn'] + "', '" + d['series_en'] + "', '" + d['series_cn'] + "', '" + d['poster_tag'] + "', '" + d['top'] + "', '" + d['heart'] + "', '" + d['base'] + "')}"
    new_lines.append(call)
new_lines.append('</div>')
new_grid = '\n'.join(new_lines)

old_grid = C[grid_start:close_div]
C = C.replace(old_grid, new_grid)
print("  Replaced collection cards (old: " + str(len(old_grid)) + " chars, new: " + str(len(new_grid)) + " chars)")

# Write back
open('build-final.py', 'w', encoding='utf-8').write(C)

# ═══════════════════════════════════════════
# STEP 3: Build
# ═══════════════════════════════════════════
print("\nSTEP 3: Building index.html...")
r = sp.run(['python', 'build-final.py'], capture_output=True, text=True)
if r.returncode != 0:
    print('FAIL:', r.stderr[:800])
    raise SystemExit(1)

I = open('index.html', 'rb').read()
js = I[I.find(b'<script>') + 8:I.find(b'</script>')]
o = js.count(b'{')
c2 = js.count(b'}')
dec = I.decode('utf-8', 'replace')

print("  Braces: " + str(o) + " vs " + str(c2) + (" OK" if o == c2 else " MISMATCH!"))

# Verify key markers
for t in ['collection_card', 'figment', 'adorn', 'tonight', 'entropy', 'migration', 'renew', 'frag-link']:
    count = dec.count(t)
    print("  " + ("OK" if count > 0 else "MISS") + ": " + t + " (" + str(count) + ")")

# Check detail pages exist
for d in COLLECTION:
    path = os.path.join('perfume', d['slug'] + '.html')
    exists = os.path.exists(path)
    print("  Detail page: " + d['slug'] + ".html " + ("EXISTS" if exists else "MISSING!"))

print("\n  Size: " + str(os.path.getsize('index.html')) + " bytes")
print("\nDONE!")
