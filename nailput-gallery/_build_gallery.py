# -*- coding: utf-8 -*-
"""產生 300 款美甲圖庫網頁（含 MegaMenu、分面篩選、收藏、SEO）"""
import os, re

BASE = r"D:\_WWW_325_pub\美甲圖庫"
ASSETS = os.path.join(BASE, "assets")
OUT = os.path.join(BASE, "美甲圖庫.html")

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

def cn(name):
    m = name.split("-")
    c = COLORS.get(m[0], m[0])
    s = STYLES.get(m[-1], m[-1])
    return c, s

def group_chips(groups, attr):
    """依大類分組產生篩選 chip（attr=color|style）"""
    name_map = COLORS if attr == "color" else STYLES
    out = []
    for gname, keys in groups.items():
        inner = "".join(
            f'<button class="chip" data-{attr}="{k}">{name_map[k]}</button>'
            for k in keys if k in name_map
        )
        out.append(f'<div class="grp"><div class="grp-title">{gname}</div><div class="grp-row">{inner}</div></div>')
    return "".join(out)

# 讀取 webp 清單
webp = sorted(f for f in os.listdir(ASSETS) if f.lower().endswith(".webp"))
print("偵測到 WebP 圖片：", len(webp))

# 組卡片
cards = []
for f in webp:
    base = os.path.splitext(f)[0]
    c, s = cn(base)
    cards.append({
        "file": f, "color_en": base.split("-")[0], "style_en": base.split("-")[-1],
        "color_zh": c, "style_zh": s, "name": f"{c}{s}"
    })
# 色系輪轉排序：依色系分組，每輪依序取各色系一款，讓每頁涵蓋全部色系各一代表款
by_color = {}
for c in cards:
    by_color.setdefault(c["color_en"], []).append(c)
color_order = [ce for ce in by_color]  # 依出現順序
max_n = max(len(by_color[ce]) for ce in by_color)
rotated = []
for i in range(max_n):
    for ce in color_order:
        if i < len(by_color[ce]):
            rotated.append(by_color[ce][i])
cards = rotated

# 色系選項
color_opts = []
color_seen = []
for f in webp:
    b = os.path.splitext(f)[0]
    ce = b.split("-")[0]
    if ce not in color_seen:
        color_seen.append(ce)
        color_opts.append(f'<button class="chip" data-color="{ce}">{COLORS[ce]}</button>')
color_opts_html = '<button class="chip active" data-color="all">全部</button>' + "".join(color_opts)

# 款式選項
style_opts = []
style_seen = []
for f in webp:
    b = os.path.splitext(f)[0]
    se = b.split("-")[-1]
    if se not in style_seen:
        style_seen.append(se)
        style_opts.append(f'<button class="chip" data-style="{se}">{STYLES[se]}</button>')
style_opts_html = '<button class="chip active" data-style="all">全部</button>' + "".join(style_opts)

# 大類分組（收合後選項不超過 20 種）
STYLE_GROUPS = {
    "經典質感": ["french", "minimal", "matte", "jelly", "pearl", "retro"],
    "光感系": ["glitter", "metallic", "mirror", "starry", "cateye"],
    "暈染漸層": ["gradient", "ombre", "marble", "rainbow"],
    "圖樣藝術": ["animal", "geometric", "plaid", "polka", "mosaic", "woodgrain", "handpainted", "colorblock"],
}
COLOR_GROUPS = {
    "暖色系": ["champagne", "cocoa", "coral", "lemon", "peach", "nude", "rose", "wine"],
    "冷色系": ["celadon", "lavender", "mint", "misty", "midnight", "navy"],
    "中性色系": ["gray", "milk", "moonlight", "morandi", "obsidian", "pure"],
}
style_group_html = group_chips(STYLE_GROUPS, "style")
color_group_html = group_chips(COLOR_GROUPS, "color")

# MegaMenu 款式群組
mega_groups = {
    "經典百搭": ["french","minimal","retro","jelly"],
    "光感系": ["cateye","metallic","mirror","pearl","starry","glitter"],
    "漸層質感": ["gradient","ombre","marble","rainbow"],
    "圖樣藝術": ["animal","geometric","plaid","polka","mosaic","woodgrain","handpainted","colorblock"],
}
mega_html = []
for gname, slist in mega_groups.items():
    links = "".join(f'<a class="mega-link" href="#" data-jump="style" data-val="{s}">{STYLES[s]}</a>' for s in slist)
    mega_html.append(f'<div class="mega-group"><div class="mega-title">{gname}</div>{links}</div>')
mega_style_html = "".join(mega_html)

# 色系 MegaMenu 連結
color_links = "".join(f'<a class="mega-link" href="#" data-jump="color" data-val="{ce}">{COLORS[ce]}</a>' for ce in color_seen)

# Accordion 分類連結（款式 / 色系）
acc_style_links = "".join(f'<a class="acc-link" href="#" data-jump="style" data-val="{s}">{STYLES[s]}</a>' for s in style_seen)
acc_color_links = "".join(f'<a class="acc-link" href="#" data-jump="color" data-val="{ce}">{COLORS[ce]}</a>' for ce in color_seen)

# 卡片
grid_html = []
for c in cards:
    grid_html.append(
f'''    <figure class="card" data-color="{c['color_en']}" data-style="{c['style_en']}">
      <a class="card-link" href="{c['file'][:-5]}.html" title="{c['name']}">
      <div class="thumb"><span class="tag-badge">{c['style_zh']}</span><img src="assets/{c['file']}" alt="{c['name']}，{c['color_zh']}色系{c['style_zh']}款式" loading="lazy"><button class="fav" data-fav="{c['file']}" aria-label="收藏"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21.2l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.8Z"/></svg></button></div>
      <figcaption class="info"><div class="name">{c['name']}</div><div class="meta">{c['color_zh']} · {c['style_zh']}</div></figcaption>
      </a>
    </figure>'''
)
grid_html_str = "\n".join(grid_html)

# JSON-LD 結構化資料
def jl_escape(s):
    return s.replace("\\","\\\\").replace('"','\\"')

item_list = []
for c in cards:
    item_list.append(f'{{"@type":"ListItem","position":{cards.index(c)+1},"name":"{c["name"]}","image":"https://nailput.com/美甲圖庫/assets/{c["file"]}"}}')
jsonld_items = ",".join(item_list)

html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>美甲圖庫｜300款美甲款式大全 Nail Art Gallery</title>
<meta name="description" content="收錄 300 款美甲設計圖庫，涵蓋法式、貓眼、暈染、漸層、霧面、亮片、手繪等熱門款式與 20 種色系，可依色系、款式快速篩選，美甲款式參考首選。">
<link rel="canonical" href="https://nailput.com/美甲圖庫/">
<meta property="og:type" content="website">
<meta property="og:title" content="美甲圖庫｜300款美甲款式大全">
<meta property="og:description" content="300 款美甲設計圖庫，法式、貓眼、暈染、漸層、霧面、亮片等款式 × 20 色系，快速篩選瀏覽。">
<meta property="og:url" content="https://nailput.com/美甲圖庫/">
<meta property="og:image" content="https://nailput.com/美甲圖庫/assets/nude-french.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1600">
<meta property="og:locale" content="zh_TW">
<meta property="og:site_name" content="美甲圖庫">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23b76e79' d='M12 2a5 5 0 0 1 5 5v6a5 5 0 0 1-4 4.9V22h-2v-4.1A5 5 0 0 1 7 13V7a5 5 0 0 1 5-5Z'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://miaoda.feishu.cn">
<link rel="stylesheet" href="https://miaoda.feishu.cn/fonts/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"首頁","item":"https://nailput.com/"}},
{{"@type":"ListItem","position":2,"name":"美甲圖庫","item":"https://nailput.com/美甲圖庫/"}}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ItemList","name":"美甲圖庫 300 款","numberOfItems":{len(cards)},"itemListElement":[{jsonld_items}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebSite","name":"美甲圖庫","url":"https://nailput.com/美甲圖庫/","potentialAction":{{"@type":"SearchAction","target":"https://nailput.com/美甲圖庫/?q={{search_term_string}}","query-input":"required name=search_term_string"}}}}
</script>
<style>
  :root{{--bg:#faf5f0;--surface:#fff;--ink:#3b3330;--muted:#9c8c85;--line:#ece2da;--accent:#b76e79;--accent-soft:#f3e6e2}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:var(--bg);color:var(--ink)}}
  body{{font-family:'Noto Sans TC','Microsoft JhengHei','PingFang TC',sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:1240px;margin:0 auto;padding:0 20px 80px}}

  /* Header + MegaMenu */
  .site-header{{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid var(--line)}}
  .header-inner{{max-width:1240px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:24px;height:60px}}
  .brand{{font-weight:900;font-size:19px;color:var(--accent);display:flex;align-items:center;gap:8px;text-decoration:none}}
  .brand svg{{width:22px;height:22px}}
  .nav{{display:flex;align-items:center;gap:4px;flex:1}}
  .nav-item{{position:relative}}
  .nav-btn{{background:none;border:none;font-family:inherit;font-size:15px;color:var(--ink);padding:20px 14px;cursor:pointer;font-weight:500;display:flex;align-items:center;gap:5px}}
  .nav-btn:hover{{color:var(--accent)}}
  .mega{{display:none;position:absolute;left:0;top:100%;background:#fff;border:1px solid var(--line);border-top:2px solid var(--accent);border-radius:0 0 12px 12px;box-shadow:0 18px 40px rgba(150,110,95,.14);padding:18px;min-width:520px}}
  .nav-item:hover .mega,.nav-item:focus-within .mega,.nav-item.open .mega{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}
  .mega-group .mega-title{{font-size:13px;font-weight:900;color:var(--accent);margin-bottom:8px}}
  .mega-link{{display:block;padding:5px 6px;border-radius:6px;font-size:14px;color:var(--ink);text-decoration:none}}
  .mega-link:hover{{background:var(--accent-soft);color:var(--accent)}}
  .search-box{{position:relative;margin-left:auto}}
  .search-box input{{border:1px solid var(--line);border-radius:999px;padding:8px 14px 8px 34px;font-size:16px;width:min(180px,24vw);font-family:inherit;background:#faf6f2}}
  .search-box .mag{{position:absolute;left:11px;top:50%;transform:translateY(-50%);width:16px;height:16px;color:var(--muted);pointer-events:none}}
  .suggest{{position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 26px rgba(0,0,0,.08);display:none;max-height:260px;overflow:auto;z-index:50}}
  .suggest.open{{display:block}}
  .suggest a{{display:block;padding:8px 14px;font-size:14px;color:var(--ink);text-decoration:none}}
  .suggest a:hover{{background:var(--accent-soft);color:var(--accent)}}

  @media (max-width:760px){{
    .nav{{display:none}}
    .search-box{{margin-left:auto}}
    .search-box input{{width:130px}}
  }}

  /* 麵包屑 */
  .crumb{{padding:16px 0 4px;font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
  .crumb a{{color:var(--muted);text-decoration:none}}
  .crumb a:hover{{color:var(--accent)}}
  .crumb .sep{{color:var(--line)}}

  /* Hero */
  .hero{{padding:14px 0 22px;text-align:center}}
  .eyebrow{{color:var(--accent);font-size:13px;font-weight:700;letter-spacing:.14em;margin-bottom:10px}}
  h1{{font-size:clamp(26px,4.5vw,40px);font-weight:900;letter-spacing:.02em}}
  .sub{{margin:10px auto 0;color:var(--muted);font-size:15px;max-width:680px}}

  /* 篩選 */
  .filters{{margin-top:18px;display:flex;flex-direction:column;gap:10px}}
  .filter-row{{display:flex;align-items:center;flex-wrap:wrap;gap:8px}}
  .filter-label{{font-size:13px;font-weight:700;color:var(--muted);width:44px;flex:0 0 44px}}
  .chip{{border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:5px 13px;border-radius:999px;font-size:14px;cursor:pointer;transition:all .18s ease;font-family:inherit}}
  .chip:hover{{border-color:var(--accent);color:var(--accent)}}
  .chip.active{{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}}
  .result-line{{margin-top:12px;font-size:13px;color:var(--muted)}}
  .result-line b{{color:var(--ink);font-weight:700}}
  .result-line button{{margin-left:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:4px 12px;font-size:12px;cursor:pointer;font-family:inherit}}
  .result-line button:hover{{border-color:var(--accent);color:var(--accent)}}

  /* 網格 */
  .grid{{margin-top:18px;display:grid;gap:16px;grid-template-columns:repeat(1,1fr)}}
  @media (min-width:600px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
  @media (min-width:900px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}
  @media (min-width:1140px){{.grid{{grid-template-columns:repeat(4,1fr)}}}}
  .card{{background:var(--surface);border-radius:14px;overflow:hidden;box-shadow:0 6px 20px rgba(150,110,95,.10);cursor:pointer;display:flex;flex-direction:column;transition:transform .18s ease,box-shadow .18s ease}}
  .card-link{{display:flex;flex-direction:column;height:100%;color:inherit;text-decoration:none}}
  .card:hover{{transform:translateY(-4px);box-shadow:0 12px 28px rgba(150,110,95,.16)}}
  .thumb{{position:relative;aspect-ratio:3/4;overflow:hidden;background:#eee2da}}
  .thumb img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s ease}}
  .card:hover .thumb img{{transform:scale(1.04)}}
  .tag-badge{{position:absolute;top:10px;left:10px;background:rgba(255,255,255,.92);color:var(--accent);font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px}}
  .fav{{position:absolute;top:8px;right:8px;width:34px;height:34px;border-radius:50%;border:none;background:rgba(255,255,255,.92);cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--muted);transition:all .15s ease}}
  .fav svg{{width:17px;height:17px}}
  .fav.on{{color:#fff;background:var(--accent)}}
  .info{{padding:12px 14px 14px}}
  .name{{font-size:15px;font-weight:900}}
  .meta{{margin-top:4px;font-size:13px;color:var(--muted)}}
  .loadmore{{display:none;margin:26px auto 0;border:1px solid var(--accent);color:var(--accent);background:#fff;border-radius:999px;padding:10px 26px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit}}
  .loadmore.show{{display:block}}
  .empty{{display:none;margin-top:30px;text-align:center;color:var(--muted);padding:40px 0;font-size:15px}}
  .gallery-title{{margin-top:24px;font-size:18px;font-weight:900;color:var(--ink)}}
  .layout{{display:grid;grid-template-columns:1fr;gap:24px;margin-top:8px}}
  @media (min-width:980px){{
    .layout{{grid-template-columns:250px 1fr;align-items:start}}
    .sidebar{{position:sticky;top:76px;max-height:calc(100vh - 92px);overflow:auto}}
  }}
  .sidebar{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 16px}}
  .sidebar-title{{font-size:16px;font-weight:900;color:var(--accent);margin-bottom:14px}}

  /* Accordion 折疊分類 */
  .acc{{border:1px solid var(--line);border-radius:10px;margin-bottom:10px;overflow:hidden;background:var(--surface)}}
  .acc-head{{width:100%;text-align:left;background:none;border:none;font-family:inherit;font-size:14px;font-weight:700;color:var(--ink);padding:12px 14px;cursor:pointer;display:flex;justify-content:space-between;align-items:center}}
  .acc-head:hover{{color:var(--accent)}}
  .acc-head .arr{{color:var(--accent);transition:transform .2s ease;font-size:12px}}
  .acc.open .acc-head .arr{{transform:rotate(180deg)}}
  .acc-body{{display:none;padding:4px 12px 12px}}
  .acc.open .acc-body{{display:block}}
  .acc-link{{display:block;padding:6px 8px;border-radius:6px;font-size:13px;color:var(--ink);text-decoration:none}}
  .acc-link:hover{{background:var(--accent-soft);color:var(--accent)}}
  .grp{{margin-bottom:12px}}
  .grp:last-child{{margin-bottom:2px}}
  .grp-title{{font-size:12px;font-weight:900;color:var(--accent);margin-bottom:7px;letter-spacing:.05em}}
  .grp-row{{display:flex;flex-wrap:wrap;gap:6px}}

  /* 分頁 */
  .pagination{{display:flex;align-items:center;justify-content:center;gap:6px;margin-top:26px;flex-wrap:wrap}}
  .page-btn{{border:1px solid var(--line);background:var(--surface);color:var(--ink);min-width:38px;height:38px;border-radius:10px;font-size:14px;cursor:pointer;font-family:inherit;transition:all .15s ease}}
  .page-btn:hover{{border-color:var(--accent);color:var(--accent)}}
  .page-btn.active{{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}}
  .page-btn:disabled{{opacity:.4;cursor:not-allowed}}

  /* 浮動導航（左下角） */
  .float-nav{{position:fixed;left:16px;bottom:16px;display:flex;flex-direction:column;gap:8px;z-index:45}}
  .float-btn{{height:44px;min-width:44px;padding:0 14px;border-radius:999px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 6px 16px rgba(150,110,95,.3);font-family:inherit;font-size:14px;font-weight:700;text-decoration:none}}
  .float-btn:hover{{background:#a25c67}}
  .float-btn svg{{width:17px;height:17px}}
  .float-btn.line{{background:#06C755}}
  .float-btn.line:hover{{background:#05ad4a}}

  footer{{margin-top:44px;text-align:center;font-size:13px;color:var(--muted)}}
  footer .dot{{margin:0 6px;color:var(--accent)}}
  .lightbox{{position:fixed;inset:0;background:rgba(30,20,18,.82);display:none;align-items:center;justify-content:center;z-index:60;padding:24px}}
  .lightbox.open{{display:flex}}
  .lightbox figure{{max-width:min(92vw,440px);width:100%;background:var(--surface);border-radius:14px;overflow:hidden}}
  .lightbox img{{width:100%;display:block}}
  .lightbox figcaption{{padding:14px 18px;font-size:14px;color:var(--muted)}}
  .lightbox figcaption b{{color:var(--ink);font-size:16px;display:block;margin-bottom:4px}}
  .lightbox .close{{position:absolute;top:16px;right:20px;background:none;border:none;color:#fff;font-size:34px;cursor:pointer;line-height:1;font-family:inherit}}
</style>
</head>
<body>
<div id="top"></div>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="#top">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a5 5 0 0 1 5 5v6a5 5 0 0 1-4 4.9V22h-2v-4.1A5 5 0 0 1 7 13V7a5 5 0 0 1 5-5Z"/></svg>
      NailPut 美甲圖庫
    </a>
    <nav class="nav" aria-label="主導覽">
      <div class="nav-item"><a class="nav-btn" href="#top">首頁</a></div>
      <div class="nav-item">
        <button class="nav-btn" type="button">款式 ▾</button>
        <div class="mega">
          {mega_style_html}
        </div>
      </div>
      <div class="nav-item">
        <button class="nav-btn" type="button">色系 ▾</button>
        <div class="mega" style="grid-template-columns:repeat(2,1fr);min-width:460px">{color_links}</div>
      </div>
    </nav>
    <div class="search-box">
      <svg class="mag" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3-3"/></svg>
      <input type="text" id="searchInput" placeholder="搜尋款式…" aria-label="搜尋款式" autocomplete="off">
      <div class="suggest" id="suggestBox"></div>
    </div>
  </div>
</header>

<div class="wrap">
  <nav class="crumb" aria-label="麵包屑">
    <a href="#top">首頁</a><span class="sep">›</span><span>美甲圖庫</span>
  </nav>

  <header class="hero">
    <div class="eyebrow">Nail Art Gallery</div>
    <h1>NailPut 美甲圖庫 · 300 款最流行最酷風格</h1>
    <p class="sub">收錄 300 款美甲設計，涵蓋 {len(STYLES)} 種款式 × {len(COLORS)} 種色系。點擊圖片放大、可加入收藏清單，支援色系／款式篩選與快速搜尋。</p>
  </header>

  <div class="layout">
  <aside class="sidebar">
  <h2 class="sidebar-title">篩選</h2>

  <!-- 款式 Accordion（大類分組） -->
  <div class="acc open">
    <button class="acc-head" type="button" aria-expanded="true">款式分類<span class="arr">▾</span></button>
    <div class="acc-body">
      <div class="filter-row" id="styleFilters" style="flex-direction:column;align-items:stretch;gap:12px">
        <div class="grp-row"><button class="chip active" data-style="all">全部款式</button></div>
        {style_group_html}
      </div>
    </div>
  </div>

  <!-- 色系 Accordion（大類分組） -->
  <div class="acc">
    <button class="acc-head" type="button" aria-expanded="false">色系分類<span class="arr">▾</span></button>
    <div class="acc-body">
      <div class="filter-row" id="colorFilters" style="flex-direction:column;align-items:stretch;gap:12px">
        <div class="grp-row"><button class="chip active" data-color="all">全部色系</button></div>
        {color_group_html}
      </div>
    </div>
  </div>

  <p class="result-line" id="resultLine">
    <span id="resultText">顯示 <b>20</b> / {len(cards)} 款美甲設計</span>
    <button id="showFav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;vertical-align:-2px"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21.2l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.8Z"/></svg> 我的收藏</button>
    <button id="resetBtn">清除篩選</button>
  </p>
  </aside>
  <div class="content">
  <h2 class="gallery-title">瀏覽全部款式</h2>
  <main class="grid" id="grid" aria-live="polite">
{grid_html_str}
  </main>

  <nav class="pagination" id="pager" aria-label="分頁"></nav>
  <div class="empty" id="empty">沒有符合條件的款式，請調整篩選。</div>
  </div>
  </div>

  <footer>美甲圖庫 · 共 {len(cards)} 款<span class="dot">·</span>Nail Art Gallery</footer>
</div>

<div class="float-nav">
  <a class="float-btn" href="#top" aria-label="回首頁"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 10.5 12 3l9 7.5M5 9.5V21h5v-6h4v6h5V9.5"/></svg>Home</a>
  <button class="float-btn" id="backPrev" aria-label="回上頁" onclick="history.back()">‹ Back</button>
  <a class="float-btn line" href="https://line.me/ti/p/g-FTLSqJAR" target="_blank" rel="noopener" aria-label="Line 社群"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.6 2 2.5 5.6 2.5 10c0 2.5 1.3 4.7 3.4 6.2L5 20.2l3.9-2.1c1 .3 2 .4 3.1.4 5.4 0 9.5-3.6 9.5-8S17.4 2 12 2Z"/></svg>Line</a>
</div>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true">
  <button class="close" id="lightboxClose" aria-label="關閉">&times;</button>
  <figure>
    <img id="lightboxImg" src="" alt="">
    <figcaption><b id="lightboxName"></b><span id="lightboxMeta"></span></figcaption>
  </figure>
</div>

<script>
(function(){{
  var grid=document.getElementById('grid');
  var cards=Array.prototype.slice.call(grid.querySelectorAll('.card'));
  var PER=20, state={{color:'all',style:'all',q:'',favOnly:false,shown:0,page:1}};
  var resultText=document.getElementById('resultText');
  var emptyEl=document.getElementById('empty');
  var pager=document.getElementById('pager');

  function nameOf(card){{
    return card.querySelector('.name').textContent;
  }}

  function match(card){{
    if(state.favOnly && !card.classList.contains('is-fav')) return false;
    if(state.color!=='all' && card.dataset.color!==state.color) return false;
    if(state.style!=='all' && card.dataset.style!==state.style) return false;
    if(state.q){{
      var n=nameOf(card).toLowerCase();
      if(n.indexOf(state.q)<0) return false;
    }}
    return true;
  }}

  function renderCards(){{
    var visible=cards.filter(match);
    var total=visible.length;
    var pages=Math.max(1,Math.ceil(total/PER));
    if(state.page>pages) state.page=pages;
    cards.forEach(function(cd){{cd.style.display='none';}});
    var start=(state.page-1)*PER;
    for(var i=start;i<Math.min(start+PER,total);i++){{visible[i].style.display='';}}
    resultText.innerHTML='顯示 <b>'+visible.slice(start,start+PER).length+'</b> / '+cards.length+' 款美甲設計';
    emptyEl.style.display=total===0?'block':'none';
    renderPager(total,pages);
  }}

  function renderPager(total,pages){{
    if(total<=PER){{ pager.innerHTML=''; return; }}
    var h='<button class="page-btn" data-p="prev" '+(state.page===1?'disabled':'')+' aria-label="上一頁">‹</button>';
    for(var p=1;p<=pages;p++){{
      h+='<button class="page-btn'+(p===state.page?' active':'')+'" data-p="'+p+'">'+p+'</button>';
    }}
    h+='<button class="page-btn" data-p="next" '+(state.page===pages?'disabled':'')+' aria-label="下一頁">›</button>';
    pager.innerHTML=h;
  }}

  function apply(){{ state.page=1; renderCards(); }}

  pager.addEventListener('click',function(e){{
    var btn=e.target.closest('.page-btn'); if(!btn||btn.disabled) return;
    var p=btn.dataset.p;
    if(p==='prev') state.page=Math.max(1,state.page-1);
    else if(p==='next') state.page+=1;
    else state.page=parseInt(p,10);
    renderCards();
    grid.scrollIntoView({{behavior:'smooth',block:'start'}});
  }});

  function bindRow(rid,key,attr){{
    var row=document.getElementById(rid);
    row.addEventListener('click',function(e){{
      var btn=e.target.closest('.chip'); if(!btn) return;
      state[key]=btn.dataset[attr];
      row.querySelectorAll('.chip').forEach(function(c){{c.classList.remove('active');}});
      btn.classList.add('active');
      apply();
    }});
  }}
  bindRow('colorFilters','color','color');
  bindRow('styleFilters','style','style');

  // Accordion 展開/收合
  document.querySelectorAll('.acc-head').forEach(function(h){{
    h.addEventListener('click',function(){{
      var acc=h.closest('.acc');
      var open=acc.classList.toggle('open');
      h.setAttribute('aria-expanded',open?'true':'false');
    }});
  }});

  document.getElementById('resetBtn').addEventListener('click',function(){{
    state={{color:'all',style:'all',q:'',favOnly:false,shown:0,page:1}};
    document.querySelectorAll('#colorFilters .chip,#styleFilters .chip').forEach(function(c){{
      c.classList.toggle('active',c.dataset.color==='all'||c.dataset.style==='all');
    }});
    document.getElementById('searchInput').value='';
    document.getElementById('suggestBox').classList.remove('open');
    apply();
  }});

  document.getElementById('showFav').addEventListener('click',function(){{
    state.favOnly=!state.favOnly;
    this.style.background=state.favOnly?'var(--accent)':'var(--surface)';
    this.style.color=state.favOnly?'#fff':'var(--ink)';
    apply();
  }});

  // 收藏
  var favStore='nailFavs';
  var favs=JSON.parse(localStorage.getItem(favStore)||'[]');
  function renderFavs(){{
    cards.forEach(function(cd){{
      var k=cd.dataset.fav;
      var on=favs.indexOf(k)>=0;
      cd.classList.toggle('is-fav',on);
      var b=cd.querySelector('.fav'); if(b) b.classList.toggle('on',on);
    }});
  }}
  grid.addEventListener('click',function(e){{
    var fb=e.target.closest('.fav');
    if(fb){{
      e.stopPropagation();
      e.preventDefault();
      var card=e.target.closest('.card');
      var k=card.querySelector('img').getAttribute('src');
      var i=favs.indexOf(k);
      if(i>=0){{favs.splice(i,1);}} else {{favs.push(k);}}
      localStorage.setItem(favStore,JSON.stringify(favs));
      renderFavs(); return;
    }}
    // 其餘點擊由 <a class="card-link"> 導航到單款頁
  }});
  renderFavs();

  // 搜尋 autocomplete
  var sInput=document.getElementById('searchInput');
  var sBox=document.getElementById('suggestBox');
  sInput.addEventListener('input',function(){{
    var v=sInput.value.trim().toLowerCase();
    state.q=v;
    var names=cards.map(nameOf).filter(function(n,idx,arr){{return arr.indexOf(n)===idx;}});
    var hits=names.filter(function(n){{return n.toLowerCase().indexOf(v)>=0;}}).slice(0,8);
    sBox.innerHTML=hits.map(function(n){{return '<a href="#" data-n="'+n+'">'+n+'</a>';}}).join('');
    sBox.classList.toggle('open',v.length>0);
    apply();
  }});
  sBox.addEventListener('click',function(e){{
    var a=e.target.closest('a'); if(!a) return;
    e.preventDefault();
    sInput.value=a.dataset.n; state.q=a.dataset.n.toLowerCase();
    sBox.classList.remove('open'); apply();
  }});
  document.addEventListener('click',function(e){{
    if(!e.target.closest('.search-box')) sBox.classList.remove('open');
  }});

  // MegaMenu 點擊切換（行動版也適用）
  document.querySelectorAll('.nav-item button.nav-btn').forEach(function(btn){{
    btn.addEventListener('click',function(){{
      var ni=btn.closest('.nav-item');
      document.querySelectorAll('.nav-item').forEach(function(o){{if(o!==ni)o.classList.remove('open');}});
      ni.classList.toggle('open');
    }});
  }});
  document.addEventListener('click',function(e){{
    if(!e.target.closest('.nav-item')) document.querySelectorAll('.nav-item').forEach(function(o){{o.classList.remove('open');}});
  }});

  // MegaMenu / Accordion 跳轉
  document.querySelectorAll('.mega-link,.acc-link').forEach(function(l){{
    l.addEventListener('click',function(e){{e.preventDefault();
      var k=l.dataset.jump, v=l.dataset.val;
      state={{color:'all',style:'all',q:'',favOnly:false,shown:0,page:1}};
      document.querySelectorAll('#colorFilters .chip,#styleFilters .chip').forEach(function(c){{c.classList.remove('active');}});
      if(k==='color'){{state.color=v; var cc=document.querySelector('#colorFilters [data-color="'+v+'"]'); if(cc)cc.classList.add('active');}}
      else if(k==='style'){{state.style=v; var sc=document.querySelector('#styleFilters [data-style="'+v+'"]'); if(sc)sc.classList.add('active');}}
      apply(); window.scrollTo({{top:document.querySelector('.filters').offsetTop-80,behavior:'smooth'}});
    }});
  }});

  // Lightbox 關閉
  var lb=document.getElementById('lightbox');
  document.getElementById('lightboxClose').addEventListener('click',function(){{lb.classList.remove('open');}});
  lb.addEventListener('click',function(e){{if(e.target===lb)lb.classList.remove('open');}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&lb.classList.contains('open'))lb.classList.remove('open');}});

  apply();
}})();
</script>
</body>
</html>
'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("已寫入：", OUT)
print("卡片數：", len(cards))
