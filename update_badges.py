"""Update POSTER_TAGS labels, add world_card badges, fix collection badges"""
import re

with open('build-final.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Replace POSTER_TAGS
old_start = c.find('POSTER_TAGS = {')
old_end = c.find('}POSTER_MAP = {', old_start) + 1  # include the }

if old_end <= old_start:
    print("ERROR: POSTER_MAP not found after POSTER_TAGS")
    exit(1)

new_tags = '''POSTER_TAGS = {
    'Blur': '哲思凝聚 · 于此时',
    'Knot': '哲思凝聚 · 于此时',
    'Flirt': '哲思凝聚 · 于此时',
    'Peak': '哲思凝聚 · 于此时',
    'Wall': '哲思凝聚 · 于此时',
    'Leave': '哲思凝聚 · 于此时',
    'Iris': '哲思凝聚 · 于此时',
    'Sun&Moon': '哲思凝聚 · 于此时',
    'Pause': '七彩琉光 · 雨亦棱镜',
    'Our Melody': '七彩琉光 · 雨亦棱镜',
    'Last Word': '七彩琉光 · 雨亦棱镜',
    'Respiration': '七彩琉光 · 雨亦棱镜',
    'Rising Sunset': '七彩琉光 · 雨亦棱镜',
    'Past Dream': '七彩琉光 · 雨亦棱镜',
    'Prejudice': '七彩琉光 · 雨亦棱镜',
    'Face': '本我珍藏 · 面具',
    'Gone': '本我珍藏 · 面具',
    'Wait': '本我珍藏 · 面具',
    'Bliss': '本我珍藏 · 面具',
    'Stay': '本我珍藏 · 面具',
    'Decree': '本我珍藏 · 面具',
    'Flash': '太初之道 · 星云',
    'Present': '太初之道 · 星云',
    'Bygone': '太初之道 · 星云',
    'Lightyear': '太初之道 · 星云',
    'Origin': '太初之道 · 星云',
    'Spring': '季节限定 · 时节',
    'Summer': '季节限定 · 时节',
    'Autumn': '季节限定 · 时节',
    'Winter': '季节限定 · 时节',
    'Fall': '永恒佳作 · 净尘',
    'Drift': '永恒佳作 · 净尘',
    'Shatter': '永恒佳作 · 净尘',
    '我故臆想': '典藏臻酿 · 忆中虚构',
    '着我之境': '典藏臻酿 · 身体美术馆',
    '今夜唯我': '典藏臻酿 · 午夜款待',
    '熵增时': '典藏臻酿 · 秩序散落',
    '新时代迁流': '典藏臻酿 · 岁时坐标',
    '致新生': '典藏臻酿 · 未来首句',
}'''

c = c[:old_start] + new_tags + '\n' + c[old_end+1:]
print("1. POSTER_TAGS replaced")

# 2. Modify world_card to add badge
old_world = "<div class=\"frag-img-wrap\"><img class=\"frag-img\""
new_world = "<div class=\"frag-img-wrap\"><span class=\"poster-badge\">{POSTER_TAGS.get(en, '')}</span><img class=\"frag-img\""
c = c.replace(old_world, new_world)
print("2. world_card badges added")

# 3. Fix missing collection badges - find the 3 cards that need them
# Check each collection product
collection_badges = {
    '我故臆想': '典藏臻酿 · 忆中虚构',
    '着我之境': '典藏臻酿 · 身体美术馆',
    '今夜唯我': '典藏臻酿 · 午夜款待',
    '熵增时': '典藏臻酿 · 秩序散落',
    '新时代迁流': '典藏臻酿 · 岁时坐标',
    '致新生': '典藏臻酿 · 未来首句',
}

lines = c.split('\n')
fixed = 0
for i, line in enumerate(lines):
    for cn, tag in collection_badges.items():
        if cn in line and 'frag-name-en' in line and 'font-size:1.75rem' in line:
            # Walk backwards to find frag-img-wrap without poster-badge
            for j in range(i-1, max(0, i-20), -1):
                if 'frag-img-wrap' in lines[j]:
                    if 'poster-badge' not in lines[j]:
                        lines[j] = lines[j].replace(
                            '<div class="frag-img-wrap"><img',
                            f'<div class="frag-img-wrap"><span class="poster-badge">{tag}</span><img')
                        fixed += 1
                        print(f"  Fixed: {cn}")
                    break

c = '\n'.join(lines)
print(f"3. Collection badges fixed: {fixed}")

with open('build-final.py', 'w', encoding='utf-8') as f:
    f.write(c)
print("\nDone!")
