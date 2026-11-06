# -*- coding: utf-8 -*-
"""為 300 張美甲 WebP 產生單款作品頁 {base}.html（含 Schema、麵包屑、標籤、同系列推薦）"""
import os

BASE = r"D:\_WWW_325_pub\美甲圖庫"
ASSETS = os.path.join(BASE, "assets")
DOMAIN = "https://nailput.com"
GALLERY = "美甲圖庫"

COLORS = {
    "celadon":"青瓷綠","champagne":"香檳金","cocoa":"可可棕","coral":"珊瑚橘","gray":"灰調",
    "lavender":"薰衣草","lemon":"檸檬黃","midnight":"午夜藍","milk":"奶白","mint":"薄荷綠",
    "misty":"霧藍","moonlight":"月光銀","morandi":"莫蘭迪","navy":"墨藍","nude":"裸粉",
    "obsidian":"黑曜","peach":"蜜桃","pure":"純白","rose":"玫瑰粉","wine":"酒紅",
}
STYLES = {
    "animal":"動物紋","cateye":"貓眼","colorblock":"撞色","french":"法式","geometric":"幾何",
    "glitter":"亮片","gradient":"漸層","handpainted":"手繪","jelly":"果凍","marble":"大理石",
    "matte":"霧面","metallic":"金屬","minimal":"極簡","mirror":"鏡面","mosaic":"馬賽克",
    "ombre":"暈染","pearl":"珍珠","plaid":"格紋","polka":"點點","rainbow":"彩虹",
    "retro":"復古","starry":"星空","woodgrain":"木紋",
}

# 收集全部 webp
files = sorted(f for f in os.listdir(ASSETS) if f.lower().endswith(".webp"))
items = []
for f in files:
    b = os.path.splitext(f)[0]
    parts = b.split("-")
    c = parts[0]; s = parts[-1]
    items.append({"base": b, "file": f, "color": c, "style": s,
                  "color_zh": COLORS.get(c, c), "style_zh": STYLES.get(s, s)})

def rel_links(cur):
    """同色系 + 同款式 推薦（最多各 4 張，排除自己）"""
    same_color = [i for i in items if i["color"]==cur["color"] and i["base"]!=cur["base"]]
    same_style = [i for i in items if i["style"]==cur["style"] and i["base"]!=cur["base"]]
    picks = (same_color + same_style)
    # 去重
    seen, out = set(), []
    for i in picks:
        if i["base"] not in seen:
            seen.add(i["base"]); out.append(i)
    return out[:8]

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def make_page(it):
    name = f'{it["color_zh"]}{it["style_zh"]}'
    title = f'{name}美甲｜{it["color_zh"]}色系{it["style_zh"]}款式'
    desc = f'{name}美甲，{it["color_zh"]}色系{it["style_zh"]}設計，美甲款式參考，適合{it["color_zh"]}調系愛好者。'
    page_url = f'{DOMAIN}/{GALLERY}/{it["base"]}.html'
    img_url = f'{DOMAIN}/{GALLERY}/assets/{it["file"]}'

    rels = rel_links(it)
    rel_cards = ""
    for r in rels:
        rn = f'{r["color_zh"]}{r["style_zh"]}'
        rel_cards += (f'<a class="rel-card" href="{r["base"]}.html"><img src="assets/{r["file"]}" alt="{rn}美甲" loading="lazy"><span>{rn}</span></a>')
    if not rel_cards:
        rel_cards = '<p style="color:var(--muted)">暫無同系列款式。</p>'

    # 款式說明區的 2 張同系列迷你卡片
    rel_mini = ""
    for r in rels[:2]:
        rn = f'{r["color_zh"]}{r["style_zh"]}'
        rel_mini += f'<a class="mini-card" href="{r["base"]}.html"><img src="assets/{r["file"]}" alt="{rn}美甲" loading="lazy"><span>{rn}</span></a>'
    if not rel_mini:
        rel_mini = '<p style="color:var(--muted)">暫無同系列款式。</p>'

    # JSON-LD（BreadcrumbList + ImageObject + ItemList 分開 script）
    jsonld_bread = f'''{{
  "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"首頁","item":"{DOMAIN}/"}},
    {{"@type":"ListItem","position":2,"name":"美甲圖庫","item":"{DOMAIN}/{GALLERY}/"}},
    {{"@type":"ListItem","position":3,"name":"{esc(name)}美甲","item":"{page_url}"}}]}}'''
    jsonld_img = f'''{{
  "@context":"https://schema.org","@type":"ImageObject","name":"{esc(name)}美甲",
  "description":"{esc(desc)}","contentUrl":"{img_url}","representativeOfPage":true}}'''

    itemlist = [f'{{"@type":"ListItem","position":{i+1},"name":"{esc(r["color_zh"]+r["style_zh"])}美甲","image":"{DOMAIN}/{GALLERY}/assets/{r["file"]}"}}' for i,r in enumerate(rels)]
    jsonld_itemlist = f'{{"@context":"https://schema.org","@type":"ItemList","name":"相關{esc(name)}美甲","itemListElement":[{",".join(itemlist)}]}}' if itemlist else ""

    html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{img_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1600">
<meta property="og:locale" content="zh_TW">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23b76e79' d='M12 2a5 5 0 0 1 5 5v6a5 5 0 0 1-4 4.9V22h-2v-4.1A5 5 0 0 1 7 13V7a5 5 0 0 1 5-5Z'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://miaoda.feishu.cn">
<link rel="stylesheet" href="https://miaoda.feishu.cn/fonts/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<script type="application/ld+json">{jsonld_bread}</script>
<script type="application/ld+json">{jsonld_img}</script>
{('<script type="application/ld+json">'+jsonld_itemlist+'</script>') if jsonld_itemlist else ''}
<style>
  :root{{--bg:#faf5f0;--surface:#fff;--ink:#3b3330;--muted:#9c8c85;--line:#ece2da;--accent:#b76e79;--accent-soft:#f3e6e2}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:var(--bg);color:var(--ink)}}
  body{{font-family:'Noto Sans TC','Microsoft JhengHei','PingFang TC',sans-serif;line-height:1.6}}
  .wrap{{max-width:980px;margin:0 auto;padding:0 20px 60px}}
  .top{{position:sticky;top:0;z-index:30;background:#fff;border-bottom:1px solid var(--line)}}
  .top-in{{max-width:980px;margin:0 auto;padding:0 20px;display:flex;align-items:center;height:56px;gap:16px}}
  .brand{{font-weight:900;font-size:18px;color:var(--accent);text-decoration:none;display:flex;align-items:center;gap:8px}}
  .brand svg{{width:20px;height:20px}}
  .top-in a.back{{margin-left:auto;color:var(--accent);text-decoration:none;font-size:14px;font-weight:700}}
  .crumb{{padding:14px 0 2px;font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px}}
  .crumb a{{color:var(--muted);text-decoration:none}}
  .crumb a:hover{{color:var(--accent)}}
  h1{{font-size:clamp(22px,4vw,32px);font-weight:900;margin:12px 0 4px}}
  .tagline{{color:var(--muted);font-size:14px}}
  .detail{{display:grid;grid-template-columns:1fr;gap:24px;margin-top:20px}}
  @media (min-width:720px){{.detail{{grid-template-columns:minmax(0,420px) 1fr}}}}
  .detail .main-img{{width:100%;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(150,110,95,.12)}}
  .detail .main-img img{{width:100%;display:block}}
  .tags{{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px}}
  .tag{{border:1px solid var(--accent);color:var(--accent);background:#fff;border-radius:999px;padding:4px 12px;font-size:13px;font-weight:700}}
  .info p{{margin-top:12px;color:var(--ink);font-size:15px}}
  .mini-cards{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:14px}}
  .mini-card{{background:var(--surface);border-radius:12px;overflow:hidden;text-decoration:none;color:var(--ink);box-shadow:0 4px 14px rgba(150,110,95,.08);transition:transform .18s ease}}
  .mini-card:hover{{transform:translateY(-3px)}}
  .mini-card img{{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}}
  .mini-card span{{display:block;padding:7px 10px;font-size:12px;font-weight:700;text-align:center}}
  .related{{margin-top:34px}}
  .related h2{{font-size:18px;font-weight:900;margin-bottom:12px}}
  .rel-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}
  @media (min-width:640px){{.rel-grid{{grid-template-columns:repeat(4,1fr)}}}}
  .rel-card{{background:var(--surface);border-radius:12px;overflow:hidden;text-decoration:none;color:var(--ink);box-shadow:0 4px 14px rgba(150,110,95,.08);transition:transform .18s ease}}
  .rel-card:hover{{transform:translateY(-3px)}}
  .rel-card img{{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}}
  .rel-card span{{display:block;padding:8px 10px;font-size:13px;font-weight:700}}
  .float-nav{{position:fixed;left:16px;bottom:16px;display:flex;flex-direction:column;gap:8px;z-index:35}}
  .float-btn{{height:42px;min-width:42px;padding:0 13px;border-radius:999px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;font-size:14px;font-weight:700;box-shadow:0 6px 14px rgba(150,110,95,.3);font-family:inherit;text-decoration:none}}
  .float-btn:hover{{background:#a25c67}}
  .float-btn svg{{width:16px;height:16px}}
  .float-btn.line{{background:#06C755}}
  .float-btn.line:hover{{background:#05ad4a}}
  footer{{margin-top:38px;text-align:center;font-size:13px;color:var(--muted)}}
</style>
</head>
<body>
<div class="top">
  <div class="top-in">
    <a class="brand" href="美甲圖庫.html"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a5 5 0 0 1 5 5v6a5 5 0 0 1-4 4.9V22h-2v-4.1A5 5 0 0 1 7 13V7a5 5 0 0 1 5-5Z"/></svg>NailPut 美甲圖庫</a>
    <a class="back" href="美甲圖庫.html">← 返回圖庫</a>
  </div>
</div>

<div class="wrap">
  <nav class="crumb" aria-label="麵包屑">
    <a href="美甲圖庫.html">首頁</a><span>›</span><a href="美甲圖庫.html">美甲圖庫</a><span>›</span><span>{esc(name)}美甲</span>
  </nav>

  <h1>{esc(name)}美甲</h1>
  <p class="tagline">{esc(it["color_zh"])}色系 · {esc(it["style_zh"])}款式 · 美甲款式參考</p>

  <div class="detail">
    <div>
      <div class="main-img"><img src="assets/{it["file"]}" alt="{esc(name)}美甲，{esc(it["color_zh"])}色系{esc(it["style_zh"])}款式"></div>
      <div class="tags">
        <span class="tag">{esc(it["color_zh"])}</span><span class="tag">{esc(it["style_zh"])}</span>
      </div>
    </div>
    <div class="info">
      <h2 style="font-size:18px;font-weight:900">款式說明</h2>
      <div class="mini-cards">{rel_mini}</div>
      <p>{esc(name)}美甲，以{esc(it["color_zh"])}色系為底，搭配{esc(it["style_zh"])}手法設計，呈現出{esc(it["color_zh"])}{esc(it["style_zh"])}的視覺效果，適合作為美甲款式參考與靈感。</p>
    </div>
  </div>

  <section class="related">
    <h2>相關款式</h2>
    <div class="rel-grid">{rel_cards}</div>
  </section>

  <footer>美甲圖庫 · 三三藝 gallery 作品庫</footer>
</div>

<div class="float-nav">
  <a class="float-btn" href="美甲圖庫.html" aria-label="回首頁"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 10.5 12 3l9 7.5M5 9.5V21h5v-6h4v6h5V9.5"/></svg>Home</a>
  <button class="float-btn" aria-label="回上頁" onclick="history.back()">‹ Back</button>
  <a class="float-btn line" href="https://line.me/ti/p/g-FTLSqJAR" target="_blank" rel="noopener" aria-label="Line 社群"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.6 2 2.5 5.6 2.5 10c0 2.5 1.3 4.7 3.4 6.2L5 20.2l3.9-2.1c1 .3 2 .4 3.1.4 5.4 0 9.5-3.6 9.5-8S17.4 2 12 2Z"/></svg>Line</a>
</div>
</body>
</html>
'''
    return html

# 產生全部頁面
count = 0
for it in items:
    out = os.path.join(BASE, it["base"] + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(make_page(it))
    count += 1
print(f"已產生 {count} 個單款作品頁")
