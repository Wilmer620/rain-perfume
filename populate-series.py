#!/usr/bin/env python
"""Populate all series content for RAIN website"""
import re

with open('C:/Users/Ara/rain-website/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# ═══════════════════════════════════════════
# DATA: All fragrances
# ═══════════════════════════════════════════

sojourn_frags = [
    {
        'num': 'NO. 01', 'en': 'Blur',
        'cn': '花非花 · 雾非雾',
        'top': 'White Peony · Pear · Mist Accord',
        'heart': 'Jasmine · Osmanthus · Silk',
        'base': 'White Musk · Ambroxan · Blonde Woods',
        'notes': [
            ('白牡丹', '花中之王——层层叠叠的白色花瓣，香气清甜不腻，如雾中花影。'),
            ('桂花', '秋夜桂花的幽香——不是迎面扑来的，而是随风潜入的。'),
            ('白麝香', '最干净的麝香——没有动物感，像刚洗过的皮肤，温暖又纯净。'),
        ],
        'narrative': '像花还是像雾？当你靠近时，它退成一片朦胧的白——看不真切，但你知道它在那里。花非花是对<em>边界</em>的提问：在确定与不确定之间，有一种更真实的存在。'
    },
    {
        'num': 'NO. 02', 'en': 'Knot',
        'cn': '结',
        'top': 'Cardamom · Black Pepper · Bergamot',
        'heart': 'Cedar · Clove · Labdanum',
        'base': 'Oud · Leather · Birch Tar',
        'notes': [
            ('小豆蔻', '姜科植物的种子——清凉微辛，像从中东集市里飘来的绿色豆荚。'),
            ('乌木', '沉香木——数十年树龄才能在伤口处形成的黑色树脂，自然界最珍贵的香材。'),
            ('皮革', '鞣制过的皮具气息——粗粝中带着性感，像旧时光里的皮手套。'),
        ],
        'narrative': '一段解不开的东西。可能是一句话，一段记忆，一个人。结不是关于困境——是关于<em>不可解的意义</em>。有些东西之所以珍贵，恰恰在于它无法被拆开。'
    },
    {
        'num': 'NO. 03', 'en': 'Flirt',
        'cn': '风骚',
        'top': 'Pink Pepper · Bergamot · Saffron',
        'heart': 'Rose de Mai · Peony · Violet',
        'base': 'Musk · Sandalwood · Vanilla',
        'notes': [
            ('粉红胡椒', '并非真正的胡椒——它更明亮、微甜，像粉红色的泡泡在舌尖爆开。'),
            ('五月玫瑰', '每年五月只开一季的玫瑰——蜜感、荔枝甜，比普通玫瑰更饱满。'),
            ('檀木', '奶感、顺滑的木质——像被时间打磨过的温暖。'),
        ],
        'narrative': '风骚不是轻浮。是知道你有多迷人，并且<em>允许自己发光</em>。是穿过人群时，不用回头就知道有人在看你——而你本就打算被看见。'
    },
    {
        'num': 'NO. 04', 'en': 'Peak',
        'cn': '摩登巅',
        'top': 'Juniper · Lemon · Metal Accord',
        'heart': 'Cedar · Orris · Violet Leaf',
        'base': 'Musk · Amber · Concrete Accord',
        'notes': [
            ('杜松子', '金酒的核心原料——清冽、微辛、带着松针般的凉意，干净利落。'),
            ('鸢尾', '鸢尾根茎需风干三年以上才释放香气——粉质、紫罗兰般的柔光，优雅至极。'),
            ('琥珀', '化石化的松脂——温暖、圆润、像被阳光晒过的蜜蜡。'),
        ],
        'narrative': '摩登的顶点不是人多的地方。是当你站在一栋楼的顶层，透过玻璃幕墙看城市轮廓线——<em>安静、清晰、不动声色</em>。这是属于你自己的峰顶。'
    },
    {
        'num': 'NO. 05', 'en': 'Wall',
        'cn': '围城',
        'top': 'Incense · Elemi · Bergamot',
        'heart': 'Rose · Myrrh · Patchouli',
        'base': 'Frankincense · Sandalwood · Benzoin',
        'notes': [
            ('焚香', '古老寺庙里燃烧的树脂——烟熏、木质、上升的仪式感。'),
            ('没药', '圣经里三博士的礼物之一——微苦、药感、古老的疗愈气息。'),
            ('乳香', '白色树脂燃烧后的烟——从古代神庙飘到现在。'),
        ],
        'narrative': '你建了一堵墙。不是为了把人挡在外面——是为了保证<em>只有对的人能进来</em>。围城不是堡垒，是门槛。墙内是你为自己留的安静。'
    },
    {
        'num': 'NO. 06', 'en': 'Leave',
        'cn': '再别',
        'top': 'Bergamot · Black Tea · Lemon',
        'heart': 'Orris · Papyrus · Violet',
        'base': 'Cedar · Vanilla · Musk',
        'notes': [
            ('佛手柑', '柑橘家族中最优雅的一员——微苦中带甜，像指尖刚剥开的新鲜果皮。'),
            ('纸莎草', '古埃及人书写《亡灵书》用的植物——干燥、微甜、像泛黄纸张。'),
            ('雪松', '干燥的木香——像铅笔削过后的木屑气味，沉稳而不沉重。'),
        ],
        'narrative': '再见之后还有再见吗？再别不是第一次离开——是<em>学会了告别之后的告别</em>。不哭不闹，只是把行李放在门口，最后看了一眼房间。'
    },
    {
        'num': 'NO. 07', 'en': 'Iris',
        'cn': '瞳孔',
        'top': 'Carrot Seed · Aldehydes · Mandarin',
        'heart': 'Orris · Mimosa · Violet',
        'base': 'Musk · Sandalwood · Ambrette',
        'notes': [
            ('鸢尾', '鸢尾花的根茎需风干三年以上——粉质、紫罗兰般的柔光。'),
            ('含羞草', '毛茸茸的黄色小花——甜得不像花，像阳光晒过的蜜粉。'),
            ('白麝香', '最干净的麝香——没有动物感，像刚洗过的皮肤。'),
        ],
        'narrative': '当一个人离你很近很近的时候，你能在她的瞳孔里看到自己。瞳孔是关于<em>可能被看见的最小距离</em>——只适合那些愿意被你看进深处的人。'
    },
]

feast_frags = [
    {
        'num': 'NO. 01', 'en': 'Face',
        'cn': '皮囊',
        'top': 'Juniper · Lemon Peel · Aldehydes',
        'heart': 'Orris · Violet · Powder',
        'base': 'White Musk · Cool Amber · Suede',
        'notes': [
            ('杜松子', '金酒的核心原料——清冽微辛，干净利落。'),
            ('鸢尾', '根茎风干三年才释放香气——粉质柔光。'),
            ('白麂皮', '鞣制过的白色皮革——比普通皮革更柔软、更干净。'),
        ],
        'narrative': '一层半透的薄纱浮在雾中。皮囊不是伪装——是灵魂选择<em>被看见的那一面</em>。薄到光可以穿过，柔到像刚醒来的皮肤。'
    },
    {
        'num': 'NO. 02', 'en': 'Gone',
        'cn': '隐身衣',
        'top': 'Black Pepper · Clove · Aldehydes',
        'heart': 'Smoke · Incense · Ash',
        'base': 'Vetiver · Leather · Patchouli',
        'notes': [
            ('黑胡椒', '辛辣、微木香——像第一口的刺激感。'),
            ('焚香', '树脂燃烧——烟熏、木质、上升的仪式。'),
            ('岩兰草', '根茎的泥土气息——潮湿、微甜、像雨后翻开的土壤。'),
        ],
        'narrative': '靛蓝的烟裹住你，然后散开——你还在原地，但<em>世界不再盯着你看</em>。消失不是逃跑，是收回被注视的权利。'
    },
    {
        'num': 'NO. 03', 'en': 'Wait',
        'cn': '等待',
        'top': 'Bergamot · Cardamom · Saffron',
        'heart': 'Amber · Labdanum · Honey',
        'base': 'Oud · Sandalwood · Vanilla Absolute',
        'notes': [
            ('小豆蔻', '清凉微辛的绿色豆荚——中东集市的香料感。'),
            ('蜂蜜', '金黄粘稠的甜——温暖、圆润。'),
            ('乌木', '沉香木——数十年形成的黑色树脂，最珍贵的香材。'),
        ],
        'narrative': '一滴琥珀停在暗水之上——撞击前的瞬间被拉成永恒。<em>等待不是空无</em>，是所有可能同时活着的那一刻。'
    },
    {
        'num': 'NO. 04', 'en': 'Rush',
        'cn': '欢愉',
        'top': 'Pink Pepper · Mandarin · Cassis',
        'heart': 'Rose · Jasmine · Peach Skin',
        'base': 'Musk · Sandalwood · Praline',
        'notes': [
            ('粉红胡椒', '明亮微甜——像粉红色泡泡爆开。'),
            ('茉莉', '夜间开得最浓的白色花朵——像深夜花园的幽香。'),
            ('果仁糖', '焦糖化的坚果——甜而不腻的温暖。'),
        ],
        'narrative': '香槟色的光粒子在慢动作中炸开——不是爆炸，是<em>同时绽放</em>。欢愉不需要理由，只需要此刻。'
    },
    {
        'num': 'NO. 05', 'en': 'Stay',
        'cn': '侍者',
        'top': 'Green Tea · Bamboo · Cucumber',
        'heart': 'Lotus · Moss · Water Lily',
        'base': 'White Musk · Cedar · Rice',
        'notes': [
            ('绿茶', '杀青后的茶叶——清涩、微蒸。'),
            ('莲花', '水中开放的白花——凉意、空灵。'),
            ('雪松', '干燥木香——沉稳不沉重。'),
        ],
        'narrative': '灰绿的水彩洇在暖纸上——<em>陪伴不需要出声</em>。有人愿意安静地存在于另一个人的世界里，成为他们不必说出口的背景。'
    },
]

after_frags = [
    {
        'num': 'NO. 01', 'en': 'Fall',
        'cn': '自天穹',
        'top': 'Ozone · Bergamot · Silver Fir',
        'heart': 'Rain Accord · Iris · Violet Leaf',
        'base': 'White Musk · Cedar · Mineral Notes',
        'notes': [
            ('臭氧调', '雷雨前空气中那种带电的清新——干净、微刺、像天空被劈开的味道。'),
            ('雨调', '模拟雨水打在热石板上蒸腾而起的气息——水、矿物、灰尘刚被洗去的瞬间。'),
            ('银冷杉', '高山针叶——比雪松更锋利的绿意，带松脂的凉。'),
        ],
        'narrative': '雨滴从几千米的高空开始坠落——穿过云层、穿过光线、穿过空气。<em>每一滴雨都来自天穹</em>。在它触碰大地之前，它见过我们从未见过的东西。'
    },
    {
        'num': 'NO. 02', 'en': 'Drift',
        'cn': '穿云间',
        'top': 'Aldehydes · Bergamot · Mint',
        'heart': 'Cotton Flower · Magnolia · Cucumber',
        'base': 'Musk · Sandalwood · White Amber',
        'notes': [
            ('醛香', '香槟气泡般的提亮感——让一切变得更轻盈、更通透。'),
            ('棉花花', '干净的、刚洗过的织物气息——像云朵的触感。'),
            ('白玉兰', '奶白色花瓣——柔甜不腻，像记忆里的南方春天。'),
        ],
        'narrative': '不是站在雨外面看雨——是<em>穿过一层云</em>，再穿过下一层云。<em>穿云间</em>是关于进入：进入一个你从未到过的气象，让雨水成为你的皮肤。'
    },
    {
        'num': 'NO. 03', 'en': 'Shatter',
        'cn': '碎地霜',
        'top': 'Cassia · Black Tea · Rhubarb',
        'heart': 'Osmanthus · Patchouli · Leaves',
        'base': 'Vetiver · Oakmoss · Earth Accord',
        'notes': [
            ('大黄', '微酸涩、带粉质——不是甜果，是潮湿土壤上刚裂开的蔓。'),
            ('岩兰草', '根茎的泥土气息——潮湿、微甜。'),
            ('橡苔', '森林地面的腐叶和苔藓——暗绿、潮湿、原始的木质感。'),
        ],
        'narrative': '雨坠到地面的一那刻——碎裂、散开、渗入泥土。碎地霜是关于<em>抵达</em>：结束了旅程的雨滴，正在变成明天早上的雾、草叶上的露、另一个人的呼吸。'
    },
]

# ═══════════════════════════════════════════
# HELPER: Build a frag card HTML
# ═══════════════════════════════════════════
def build_card(f, is_placeholder=False):
    if is_placeholder:
        return (
            '<div class="frag-card placeholder reveal reveal-d1">'
            '<div class="frag-card-inner"><div class="frag-img-wrap"></div>'
            '<div class="frag-info"><p class="frag-num">' + f['num'] + '</p>'
            '<h3 class="frag-name-en">Coming Soon</h3>'
            '<p class="frag-name-cn">' + f['cn'] + '</p>'
            '</div></div></div>'
        )

    notes_html = ''
    for note, tip in f['notes']:
        notes_html += '<span class="note-tag" data-tip="' + tip.replace('"', '&quot;') + '">' + note + '</span>'

    return (
        '<div class="frag-card reveal reveal-d1" onmousemove="cardTilt(this,event)" onmouseleave="cardReset(this)">'
        '<span class="corner c-tl"></span><span class="corner c-br"></span>'
        '<div class="frag-card-inner">'
        '<div class="frag-img-wrap"></div>'
        '<div class="frag-info">'
        '<p class="frag-num">' + f['num'] + '</p>'
        '<h3 class="frag-name-en">' + f['en'] + '</h3>'
        '<p class="frag-name-cn">' + f['cn'] + '</p>'
        '<p class="frag-accord"><b>Top</b> ' + f['top'] + '<br>'
        '<b>Heart</b> ' + f['heart'] + '<br>'
        '<b>Base</b> ' + f['base'] + '</p>'
        '</div></div></div>'
    )

def build_narrative(panel_id, title, frags):
    stories = ''
    for i, f in enumerate(frags):
        stories += (
            '<div class="sc-item" style="display:grid;grid-template-columns:1fr 1fr;gap:5rem;align-items:center;margin-bottom:5rem">'
            '<div class="sc-visual" style="aspect-ratio:2800/1840;background:rgba(255,254,253,.1);backdrop-filter:blur(24px);border:1px solid rgba(184,148,62,.04);border-radius:6px;overflow:hidden;position:relative">'
            '<div class="sc-visual-num" style="position:absolute;top:-1.2rem;right:-.8rem;font-family:Cormorant Garamond,serif;font-size:10rem;font-weight:300;color:rgba(184,148,62,.03);line-height:1;pointer-events:none">' + str(i+1).zfill(2) + '</div>'
            '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:Cormorant Garamond,serif;font-size:3rem;font-weight:300;color:rgba(184,148,62,.06);letter-spacing:.15em;text-transform:uppercase">' + f['en'].upper() + '</div>'
            '</div>'
            '<div class="sc-text" style="padding:1.5rem 0">'
            '<p class="sc-num" style="font-family:Cormorant Garamond,serif;font-size:.65rem;letter-spacing:.42em;color:var(--gold-d);margin-bottom:1.8rem">' + f['num'] + '</p>'
            '<h3 class="sc-name" style="font-family:Cormorant Garamond,serif;font-size:2.5rem;font-weight:400;letter-spacing:.08em;color:var(--ink);margin-bottom:.12rem">' + f['en'] + '</h3>'
            '<p class="sc-name-cn" style="font-family:Noto Serif SC,serif;font-size:1.15rem;font-weight:400;letter-spacing:.3em;color:var(--ink2);margin-bottom:1.6rem">' + f['cn'] + '</p>'
            '<p class="sc-desc" style="font-family:Noto Serif SC,serif;font-size:.86rem;line-height:2.5;color:var(--ink3);letter-spacing:.04em;margin-bottom:1.8rem">' + f['narrative'] + '</p>'
            '</div></div>'
        )

    return (
        '<div class="showcase-toggle-wrap" style="margin-top:1.5rem;text-align:center"><button class="showcase-toggle narrative-toggle" data-target="narrative-' + panel_id + '">展开叙事</button></div>'
        '<div class="showcase-body collapsed" id="narrative-' + panel_id + '" style="max-width:1200px;margin:0 auto;padding:0 2rem">'
        + stories +
        '</div>'
    )

# ═══════════════════════════════════════════
# STEP 1: Remove ALL existing narrative blocks
# ═══════════════════════════════════════════
c = re.sub(r'<div class="showcase-toggle-wrap".*?narrative-toggle.*?</button></div>\s*<div class="showcase-body[^>]*id="narrative-[^\"]*".*?</div>\s*</div>\s*</div>',
           '', c, flags=re.DOTALL)

# ═══════════════════════════════════════════
# STEP 2: Find each series-panel and replace content
# ═══════════════════════════════════════════
def find_panel_range(c, panel_id):
    """Find start and end of a series-panel div"""
    pattern = 'data-panel="' + panel_id + '"'
    pos = c.find(pattern)
    if pos < 0: return None, None
    # Go back to <div class="series-panel
    start = c.rfind('<div class="series-panel', 0, pos)
    if start < 0: start = c.rfind('<div class=\"series-panel', 0, pos)

    # Find closing by depth counting
    depth = 0; i = start
    while i < len(c):
        if c[i:i+4] == '<div': depth += 1
        elif c[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return start, i + 6
        i += 1
    return start, -1

# ═══════════════════════════════════════════
# STEP 3: Replace sojourn panel
# ═══════════════════════════════════════════
cards = ''
for f in sojourn_frags:
    cards += build_card(f) + '\n'
cards += build_narrative('sojourn', '驻足苦旅', sojourn_frags)

start, end = find_panel_range(c, 'sojourn')
if start and end > 0:
    c = c[:start] + '<div class="series-panel active" data-panel="sojourn">\n<div class="frag-grid">\n' + cards + '\n</div>\n</div>\n' + c[end:]

# ═══════════════════════════════════════════
# STEP 4: Replace feast panel
# ═══════════════════════════════════════════
cards = ''
for f in feast_frags:
    cards += build_card(f) + '\n'
cards += build_narrative('feast', '灵感盛宴', feast_frags)

start, end = find_panel_range(c, 'feast')
if start and end > 0:
    c = c[:start] + '<div class="series-panel" data-panel="feast">\n<div class="frag-grid">\n' + cards + '\n</div>\n</div>\n' + c[end:]

# ═══════════════════════════════════════════
# STEP 5: Replace after panel
# ═══════════════════════════════════════════
cards = ''
for f in after_frags:
    cards += build_card(f) + '\n'
cards += build_narrative('after', '雨后', after_frags)

start, end = find_panel_range(c, 'after')
if start and end > 0:
    c = c[:start] + '<div class="series-panel" data-panel="after">\n<div class="frag-grid">\n' + cards + '\n</div>\n</div>\n' + c[end:]

# ═══════════════════════════════════════════
# STEP 6: Fix world panel — make sure it has narrative toggle
# ═══════════════════════════════════════════
world_narrative = build_narrative('world', '世界之色', [
    {'num':'NO. 01','en':'Respiration','cn':'光 合','narrative':'雨后清晨的第一口呼吸——树叶仍在滴水，光线透过水珠折射出细碎的光谱。光合是关于<em style="font-style:normal;color:var(--gold);font-weight:500">开始</em>的气息：不是花开，而是种子破土前那一秒的寂静张力。'},
    {'num':'NO. 02','en':'Last Word','cn':'明 日','narrative':'黎明的第一缕光尚未抵达，雨丝已先一步落了下来。明日是关于<em style="font-style:normal;color:var(--gold);font-weight:500">终局与开端的交界</em>——不是告别，而是一句悬在空气里、即将成为现实的承诺。'},
    {'num':'NO. 03','en':'Our Melody','cn':'共 鸣','narrative':'两个人站在同一场雨里，听见的是同一首无声的旋律。共鸣不是靠近——是在<em style="font-style:normal;color:var(--gold);font-weight:500">各自的世界里被同一缕香气同时击中</em>。'},
    {'num':'NO. 04','en':'Rising Sunset','cn':'潮 汐','narrative':'日落与海潮共同构成了这世上最古老的节拍器。潮汐不是落寞的黄昏——它是潮水上涨时的一种<em style="font-style:normal;color:var(--gold);font-weight:500">上升感</em>，是夕阳在水面融化成千万片碎金的瞬间。'},
    {'num':'NO. 05','en':'Past Dream','cn':'旧 心 事','narrative':'雨水打在旧书页上，字迹慢慢洇开。旧心事不是悲伤——它是<em style="font-style:normal;color:var(--gold);font-weight:500">被雨水冲淡后剩下的温柔</em>，是时光冲刷后残存的、微微泛黄的光。'},
    {'num':'NO. 06','en':'Prejudice','cn':'我 独 我','narrative':'对\"偏见\"的重新解读——不是被别人误解，而是你主动选择<em style="font-style:normal;color:var(--gold);font-weight:500">不被理解的权利</em>。当整个世界都在寻求共鸣的时候，有一种香气说的是：我不需要你懂我。'},
])

start, end = find_panel_range(c, 'world')
if start and end > 0:
    # Find the closing point — just before </div> of panel
    closing = c.rfind('</div>', start, end)
    if closing > 0:
        c = c[:closing] + '\n' + world_narrative + '\n' + c[closing:]

# ═══════════════════════════════════════════
# STEP 7: Fix seasons panel — need narrative too
# ═══════════════════════════════════════════
seasons_narrative = build_narrative('seasons', '四季所生', [
    {'num':'春','en':'生','cn':'破土·呼吸','narrative':'春天第一场雨后，泥土开裂，一个新芽顶了出来。生不是开始——是<em style="font-style:normal;color:var(--gold);font-weight:500">不可逆转地向前</em>。你只能成为你，别无选择。'},
    {'num':'夏','en':'长','cn':'疯长·蔓延','narrative':'暴雨过后的疯长——不等待批准，不计代价。长是关于<em style="font-style:normal;color:var(--gold);font-weight:500">力量的野蛮表达</em>，把根扎进一切能扎进去的地方。'},
    {'num':'秋','en':'收','cn':'沉淀·入静','narrative':'秋雨不急——它知道自己不需要催促任何东西。收不是结束——是<em style="font-style:normal;color:var(--gold);font-weight:500">把该留的留下</em>，该放的放走。'},
    {'num':'冬','en':'藏','cn':'封存·等待','narrative':'冻雨把一切都封了一层薄冰。藏不是消失——是<em style="font-style:normal;color:var(--gold);font-weight:500">在看不见的地方酝酿</em>。明年春天的芽已经在土里了。'},
])

start, end = find_panel_range(c, 'seasons')
if start and end > 0:
    closing = c.rfind('</div>', start, end)
    if closing > 0:
        c = c[:closing] + '\n' + seasons_narrative + '\n' + c[closing:]

# ═══════════════════════════════════════════
# STEP 8: Write
# ═══════════════════════════════════════════
open('C:/Users/Ara/rain-website/index.html', 'w', encoding='utf-8').write(c)

toggles = c.count('narrative-toggle')
bodies = c.count('showcase-body')
card_count = c.count('frag-name-en')
placeholder_count = c.count('Coming Soon')
print(f'Done: {toggles} toggles, {bodies} bodies')
print(f'Cards: {card_count}, Placeholders: {placeholder_count}')
