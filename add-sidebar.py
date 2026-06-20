c = open('C:/Users/Ara/rain-website/index.html', 'r', encoding='utf-8').read()

sidebar_css = '\n.sidebar{position:fixed;right:1.8rem;top:50%;transform:translateY(-50%);z-index:150;display:flex;flex-direction:column;gap:1.5rem}\n'
sidebar_css += '.sidebar a{display:flex;align-items:center;gap:.5rem;color:var(--ink3);text-decoration:none;font-family:Inter,sans-serif;font-size:.52rem;letter-spacing:.2em;text-transform:uppercase;transition:all .4s;white-space:nowrap}\n'
sidebar_css += '.sidebar a::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--gold-d);opacity:.25;flex-shrink:0;transition:all .4s}\n'
sidebar_css += '.sidebar a:hover{color:var(--gold)}\n'
sidebar_css += '.sidebar a.active{color:var(--ink)}\n'
sidebar_css += '.sidebar a.active::before{opacity:.9;width:7px;height:7px;box-shadow:0 0 8px rgba(184,148,62,.3)}\n'
sidebar_css += '@media (max-width:1080px){.sidebar{display:none}}\n'

c = c.replace('@media (max-width:1080px){.frag-grid{grid-template-columns:1fr 1fr', sidebar_css + '@media (max-width:1080px){.frag-grid{grid-template-columns:1fr 1fr')

sidebar_html = '<nav class="sidebar" id="sidebar"><a href="#phil">品牌哲学</a><a href="#series">产品介绍</a><a href="#craft">制香之道</a><a href="#founders">主理人手记</a><a href="#quiz">寻雨之路</a><a href="#newsletter">降雨预报</a></nav>\n'
c = c.replace('</nav>\n', '</nav>\n' + sidebar_html, 1)

sidebar_js = '\nvar sidebarLinks=document.querySelectorAll(".sidebar a");function updateSidebar(){var y=window.scrollY+window.innerHeight/3,cur="";allSecs.forEach(function(s){if(y>=s.offsetTop)cur=s.getAttribute("id")});sidebarLinks.forEach(function(a){a.classList.toggle("active",a.getAttribute("href")==="#" + cur)})}window.addEventListener("scroll",updateSidebar,{passive:true});updateSidebar();\n'
c = c.replace('/* Reveal */', sidebar_js + '/* Reveal */')

open('C:/Users/Ara/rain-website/index.html', 'w', encoding='utf-8').write(c)
print('Sidebar added. Size:', len(c))
