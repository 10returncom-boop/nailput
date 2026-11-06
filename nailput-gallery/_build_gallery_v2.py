# -*- coding: utf-8 -*-
"""產生美甲圖庫 HTML：以 CSV 清單為權威資料源，靜態寫入全部圖片 + MegaMenu + 篩選 + 分頁 + SEO"""
import csv, io

CSV_PATH = r"D:\_WWW_325_pub\美甲圖庫\美甲圖庫清單.csv"
OUT_PATH = r"D:\_WWW_325_pub\美甲圖庫\美甲圖庫.html"
PER_PAGE = 40
SITE = "https://nailput.com"

with open(CSV_PATH, "rb") as f:
    text = f.read().decode("utf-8-sig")

rows = list(csv.DictReader(io.StringIO(text)))
for r in rows:
    r["色系"] = r["色系"].strip()
    r["款式"] = r["款式"].strip()

colors = sorted(set(r["色系"] for r in rows))
styles = sorted(set(r["款式"] for r in rows))
total_pages = (len(rows) + PER_PAGE - 1) // PER_PAGE

# ---- 卡片 HTML（靜態 img src） ----
cards = []
for i, r in enumerate(rows, 1):
    name = f"{r['色系']}·{r['款式']}"
    desc = (r["風格簡述"] or "").strip()
    alt = (r["alt-text"] or f"女性手部特寫，展示{name}美甲").strip()
    cards.append(
        f'''    <figure class="card" data-color="{r['色系']}" data-style="{r['款式']}" data-name="{name}" data-desc="{desc}" data-page="{(i - 1) // PER_PAGE + 1}">
      <div class="thumb"><span class="tag-badge">{r['款式']}</span><img src="assets/{r['filename']}" alt="{alt}" loading="lazy"></div>
      <figcaption class="info"><div class="name">{name}</div><div class="meta"><span class="num">#{i:03d}</span><span class="dot">·</span>{r['色系']}</div><div class="desc">{desc}</div></figcaption>
    </figure>'''
    )

color_links = "\n".join(f'<a href="#grid" data-color="{c}">{c}</a>' for c in colors)
style_links = "\n".join(f'<a href="#grid" data-style="{s}">{s}</a>' for s in styles)
color_chips = "\n".join(f'<button class="chip" data-color="{c}">{c}</button>' for c in colors)
style_chips = "\n".join(f'<button class="chip" data-style="{s}">{s}</button>' for s in styles)

def jle(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

item_list = ",".join(
    f'{{"@type":"ListItem","position":{i},"name":"{jle(r["色系"] + r["款式"])}","image":"{SITE}/美甲圖庫/assets/{r["filename"]}"}}'
    for i, r in enumerate(rows, 1)
)

CSS = """  :root{
    --bg:#faf5f0;--surface:#ffffff;--ink:#3b3330;--muted:#9c8c85;
    --line:#ece2da;--accent:#b76e79;--accent-soft:#f3e6e2;--chip:#f1e9e3;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:var(--bg);color:var(--ink)}
  body{font-family:'Noto Sans TC','Microsoft JhengHei','PingFang TC',sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
  a{color:inherit;text-decoration:none}
  .wrap{max-width:1240px;margin:0 auto;padding:20px 20px 96px}

  /* ===== 頂部 MegaMenu ===== */
  .topbar{background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:40}
  .topbar-inner{max-width:1240px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:16px;height:60px}
  .brand{font-weight:900;font-size:19px;letter-spacing:.02em;display:flex;align-items:center;gap:8px;white-space:nowrap;color:var(--accent)}
  .brand svg{width:22px;height:22px;flex:0 0 auto}
  .mega{display:flex;align-items:center;gap:2px;flex:1;min-width:0}
  .mega > a,.m-item{display:block;padding:8px 12px;border-radius:8px;font-size:15px;font-weight:700;color:var(--ink);cursor:pointer;position:relative;white-space:nowrap}
  .mega > a:hover,.m-item:hover{background:var(--accent-soft);color:var(--accent)}
  .m-item .caret{font-size:11px;margin-left:4px;color:var(--muted)}
  .dropdown{display:none;position:absolute;top:100%;left:0;background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:0 12px 30px rgba(150,110,95,.14);padding:12px;min-width:560px;z-index:50;grid-template-columns:repeat(4,1fr);gap:2px}
  .m-item.open .dropdown{display:grid}
  .dropdown a{display:block;padding:7px 10px;border-radius:7px;font-size:14px;color:var(--ink);white-space:nowrap}
  .dropdown a:hover{background:var(--accent-soft);color:var(--accent)}
  .search-box{position:relative;margin-left:auto;flex:0 0 220px}
  .search-box input{width:100%;padding:8px 12px 8px 34px;border:1px solid var(--line);border-radius:999px;font-size:14px;font-family:inherit;background:#fff;outline:none;color:var(--ink)}
  .search-box input:focus{border-color:var(--accent)}
  .search-box svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);width:16px;height:16px;color:var(--muted);pointer-events:none}
  .suggest{position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 26px rgba(0,0,0,.08);display:none;max-height:260px;overflow:auto;z-index:55}
  .suggest.open{display:block}
  .suggest a{display:block;padding:8px 14px;font-size:14px;color:var(--ink)}
  .suggest a:hover{background:var(--accent-soft);color:var(--accent)}
  .burger{display:none;margin-left:auto;background:none;border:none;font-size:24px;cursor:pointer;color:var(--ink);font-family:inherit}

  /* ===== 麵包屑 ===== */
  .crumb{padding:16px 0 2px;font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;align-items:center}
  .crumb a{color:var(--muted)}
  .crumb a:hover{color:var(--accent)}
  .crumb .sep{color:var(--line)}

  /* ===== 頁首 ===== */
  .hero{padding:22px 0 18px;text-align:center}
  .eyebrow{display:inline-flex;align-items:center;gap:8px;color:var(--accent);font-size:13px;font-weight:700;letter-spacing:.14em;margin-bottom:12px}
  .eyebrow svg{width:18px;height:18px}
  h1{font-size:clamp(26px,4.5vw,42px);font-weight:900;letter-spacing:.02em}
  .sub{margin-top:8px;color:var(--muted);font-size:15px;max-width:700px;margin-left:auto;margin-right:auto}

  /* ===== 篩選 ===== */
  .filters{margin-top:18px;display:flex;flex-direction:column;gap:10px}
  .filter-row{display:flex;align-items:center;flex-wrap:wrap;gap:6px}
  .filter-label{font-size:13px;font-weight:700;color:var(--muted);width:44px;flex:0 0 44px}
  .chip{border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:5px 12px;border-radius:999px;font-size:13px;cursor:pointer;transition:all .18s ease;font-family:inherit}
  .chip:hover{border-color:var(--accent);color:var(--accent)}
  .chip.active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
  .result-line{margin-top:12px;font-size:13px;color:var(--muted)}
  .result-line b{color:var(--ink);font-weight:700}
  .tool-btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:4px 12px;font-size:12px;cursor:pointer;font-family:inherit;margin-left:8px}
  .tool-btn:hover,.tool-btn.on{border-color:var(--accent);color:var(--accent)}

  /* ===== 圖庫網格 ===== */
  .grid{margin-top:18px;display:grid;gap:16px;grid-template-columns:repeat(2,1fr)}
  @media (min-width:600px){.grid{grid-template-columns:repeat(3,1fr)}}
  @media (min-width:900px){.grid{grid-template-columns:repeat(4,1fr)}}
  .card{background:var(--surface);border-radius:14px;overflow:hidden;box-shadow:0 6px 22px rgba(150,110,95,.10);cursor:pointer;transition:transform .18s ease,box-shadow .18s ease;display:flex;flex-direction:column}
  .card:hover{transform:translateY(-4px);box-shadow:0 14px 30px rgba(150,110,95,.16)}
  .thumb{position:relative;aspect-ratio:3/4;overflow:hidden;background:#eee2da}
  .thumb img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s ease}
  .card:hover .thumb img{transform:scale(1.04)}
  .tag-badge{position:absolute;top:10px;left:10px;background:rgba(255,255,255,.92);color:var(--accent);font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px}
  .fav{position:absolute;top:8px;right:8px;width:32px;height:32px;border-radius:50%;border:none;background:rgba(255,255,255,.92);cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--muted);transition:all .15s ease;z-index:2}
  .fav svg{width:16px;height:16px}
  .fav.on{color:#fff;background:var(--accent)}
  .info{padding:12px 14px 14px}
  .name{font-size:15px;font-weight:900}
  .meta{margin-top:4px;font-size:12px;color:var(--muted)}
  .meta .dot{color:var(--accent);margin:0 5px}
  .desc{margin-top:6px;font-size:12.5px;color:#6b5f5a;line-height:1.55;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}

  /* ===== 分頁 ===== */
  .pagination{display:flex;align-items:center;justify-content:center;gap:6px;margin-top:26px;flex-wrap:wrap}
  .page-btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);min-width:38px;height:38px;border-radius:10px;font-size:14px;cursor:pointer;font-family:inherit;transition:all .15s ease}
  .page-btn:hover{border-color:var(--accent);color:var(--accent)}
  .page-btn.active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
  .page-btn:disabled{opacity:.4;cursor:not-allowed}

  /* ===== 右下角浮動導航 ===== */
  .float-nav{position:fixed;right:18px;bottom:18px;z-index:45;display:flex;flex-direction:column;gap:8px}
  .float-btn{width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--accent);font-size:18px;cursor:pointer;box-shadow:0 6px 18px rgba(150,110,95,.18);font-family:inherit;display:flex;align-items:center;justify-content:center}
  .float-btn:hover{background:var(--accent);color:#fff}

  /* ===== Lightbox ===== */
  .lightbox{position:fixed;inset:0;background:rgba(30,20,18,.82);display:none;align-items:center;justify-content:center;z-index:60;padding:24px}
  .lightbox.open{display:flex}
  .lightbox figure{max-width:min(92vw,480px);width:100%;background:var(--surface);border-radius:16px;overflow:hidden}
  .lightbox img{width:100%;display:block}
  .lightbox figcaption{padding:16px 20px;font-size:14px;color:var(--muted)}
  .lightbox figcaption b{color:var(--ink);font-size:17px;display:block;margin-bottom:4px}
  .lightbox .close{position:absolute;top:18px;right:22px;background:none;border:none;color:#fff;font-size:34px;cursor:pointer;line-height:1;font-family:inherit}
  .empty{display:none;margin-top:30px;text-align:center;color:var(--muted);padding:40px 0;font-size:15px}

  footer{margin-top:40px;text-align:center;font-size:13px;color:var(--muted)}
  footer .dot{margin:0 6px;color:var(--accent)}

  @media (max-width:760px){
    .topbar-inner{flex-wrap:wrap;height:auto;padding:10px 16px;gap:8px}
    .burger{display:block}
    .mega{display:none;flex-direction:column;width:100%;align-items:stretch;order:4}
    .mega.open{display:flex}
    .dropdown{position:static;min-width:0;grid-template-columns:repeat(3,1fr);box-shadow:none;border:none;padding:6px 0 6px 10px}
    .search-box{flex:1 1 100%;margin-left:0}
    .grid{grid-template-columns:repeat(2,1fr)}
  }
  @media (max-width:420px){.grid{grid-template-columns:repeat(1,1fr)}}
"""

JS = """  (function(){
    var grid=document.getElementById('grid');
    var cards=Array.prototype.slice.call(grid.querySelectorAll('.card'));
    var perPage=%PER_PAGE%;
    var state={color:'all',style:'all',q:'',favOnly:false,page:1};
    var resultText=document.getElementById('resultText');
    var emptyEl=document.getElementById('empty');
    var pager=document.getElementById('pager');

    function match(card){
      if(state.favOnly && !card.classList.contains('is-fav')) return false;
      if(state.color!=='all' && card.dataset.color!==state.color) return false;
      if(state.style!=='all' && card.dataset.style!==state.style) return false;
      if(state.q){
        var hay=(card.dataset.name+' '+card.dataset.desc+' '+card.dataset.color+' '+card.dataset.style).toLowerCase();
        if(hay.indexOf(state.q)<0) return false;
      }
      return true;
    }
    function visibleList(){ return cards.filter(match); }
    function pages(){ return Math.max(1,Math.ceil(visibleList().length/perPage)); }

    function apply(){
      var visible=visibleList();
      emptyEl.style.display=visible.length===0?'block':'none';
      resultText.innerHTML='符合篩選 <b>'+visible.length+'</b> / '+cards.length+' 款美甲設計';
      if(state.page>pages())state.page=pages();
      renderPage();
    }
    function renderPage(){
      var visible=visibleList(),pgs=pages();
      if(state.page>pgs)state.page=pgs;
      cards.forEach(function(c){c.style.display='none';});
      var start=(state.page-1)*perPage;
      for(var i=start;i<Math.min(start+perPage,visible.length);i++){visible[i].style.display='';}
      var h='<button class="page-btn" data-p="prev" '+(state.page<=1?'disabled':'')+'>‹</button>';
      var from=Math.max(1,state.page-3),to=Math.min(pgs,state.page+3);
      if(from>1)h+='<button class="page-btn" data-p="1">1</button><span style="color:var(--muted)">…</span>';
      for(var p=from;p<=to;p++)h+='<button class="page-btn'+(p===state.page?' active':'')+'" data-p="'+p+'">'+p+'</button>';
      if(to<pgs)h+='<span style="color:var(--muted)">…</span><button class="page-btn" data-p="'+pgs+'">'+pgs+'</button>';
      h+='<button class="page-btn" data-p="next" '+(state.page>=pgs?'disabled':'')+'>›</button>';
      pager.innerHTML=h;
    }
    function refreshChips(rowId,val,attr){
      document.getElementById(rowId).querySelectorAll('.chip').forEach(function(ch){
        ch.classList.toggle('active',ch.dataset[attr]===val);
      });
    }
    function setColor(c){state.color=c;state.page=1;refreshChips('colorFilters',c,'color');}
    function setStyle(s){state.style=s;state.page=1;refreshChips('styleFilters',s,'style');}
    function clearChips(){
      document.querySelectorAll('#colorFilters .chip,#styleFilters .chip').forEach(function(c){
        c.classList.toggle('active',c.dataset.color==='all'||c.dataset.style==='all');
      });
    }

    document.getElementById('colorFilters').addEventListener('click',function(e){
      var b=e.target.closest('.chip');if(!b)return;setColor(b.dataset.color);apply();
    });
    document.getElementById('styleFilters').addEventListener('click',function(e){
      var b=e.target.closest('.chip');if(!b)return;setStyle(b.dataset.style);apply();
    });
    document.getElementById('resetBtn').addEventListener('click',function(){
      state={color:'all',style:'all',q:'',favOnly:false,page:1};
      document.getElementById('searchInput').value='';
      document.getElementById('suggestBox').classList.remove('open');
      clearChips();apply();
    });
    document.getElementById('showFav').addEventListener('click',function(){
      state.favOnly=!state.favOnly;state.page=1;
      this.classList.toggle('on',state.favOnly);apply();
    });

    var searchTimer;
    document.getElementById('searchInput').addEventListener('input',function(e){
      clearTimeout(searchTimer);
      var v=e.target.value.trim().toLowerCase();
      var sBox=document.getElementById('suggestBox');
      var names=[];
      cards.forEach(function(c){var n=c.dataset.name;if(names.indexOf(n)<0)names.push(n);});
      var hits=names.filter(function(n){return n.toLowerCase().indexOf(v)>=0;}).slice(0,8);
      sBox.innerHTML=hits.map(function(n){return '<a href="#" data-n="'+n+'">'+n+'</a>';}).join('');
      sBox.classList.toggle('open',v.length>0);
      searchTimer=setTimeout(function(){state.q=v;state.page=1;apply();},200);
    });
    document.getElementById('suggestBox').addEventListener('click',function(e){
      var a=e.target.closest('a');if(!a)return;
      e.preventDefault();
      document.getElementById('searchInput').value=a.dataset.n;
      state.q=a.dataset.n.toLowerCase();state.page=1;
      document.getElementById('suggestBox').classList.remove('open');apply();
    });
    document.addEventListener('click',function(e){
      if(!e.target.closest('.search-box'))document.getElementById('suggestBox').classList.remove('open');
    });

    pager.addEventListener('click',function(e){
      var b=e.target.closest('.page-btn');if(!b||b.disabled)return;
      var p=b.dataset.p;
      if(p==='prev')state.page=Math.max(1,state.page-1);
      else if(p==='next')state.page+=1;
      else state.page=parseInt(p,10);
      renderPage();
      grid.scrollIntoView({behavior:'smooth',block:'start'});
    });

    // ===== MegaMenu =====
    document.querySelectorAll('.m-item').forEach(function(item){
      item.addEventListener('click',function(e){
        if(e.target.closest('a'))return;
        var open=item.classList.contains('open');
        document.querySelectorAll('.m-item').forEach(function(i){i.classList.remove('open');});
        if(!open)item.classList.add('open');
      });
    });
    document.addEventListener('click',function(e){
      if(!e.target.closest('.m-item')&&!e.target.closest('.mega'))
        document.querySelectorAll('.m-item').forEach(function(i){i.classList.remove('open');});
    });
    document.querySelectorAll('.dropdown a').forEach(function(a){
      a.addEventListener('click',function(e){
        e.preventDefault();
        var color=a.dataset.color,style=a.dataset.style;
        if(color){state={color:color,style:'all',q:'',favOnly:false,page:1};clearChips();refreshChips('colorFilters',color,'color');}
        if(style){state={color:'all',style:style,q:'',favOnly:false,page:1};clearChips();refreshChips('styleFilters',style,'style');}
        document.querySelectorAll('.m-item').forEach(function(i){i.classList.remove('open');});
        document.getElementById('megaMenu').classList.remove('open');
        apply();
        document.querySelector('.filters').scrollIntoView({behavior:'smooth',block:'start'});
      });
    });
    document.getElementById('burger').addEventListener('click',function(){
      document.getElementById('megaMenu').classList.toggle('open');
    });

    // ===== 收藏（localStorage）=====
    var favStore='nailFavs';
    var favs=JSON.parse(localStorage.getItem(favStore)||'[]');
    function renderFavs(){
      cards.forEach(function(cd){
        var k=cd.querySelector('img').getAttribute('src');
        var on=favs.indexOf(k)>=0;
        cd.classList.toggle('is-fav',on);
        var b=cd.querySelector('.fav');if(b)b.classList.toggle('on',on);
      });
    }
    grid.addEventListener('click',function(e){
      var fb=e.target.closest('.fav');
      var card=e.target.closest('.card');
      if(fb){
        e.stopPropagation();
        var k=card.querySelector('img').getAttribute('src');
        var i=favs.indexOf(k);
        if(i>=0){favs.splice(i,1);}else{favs.push(k);}
        localStorage.setItem(favStore,JSON.stringify(favs));
        renderFavs();return;
      }
      if(card){
        var img=card.querySelector('img');
        document.getElementById('lightboxImg').src=img.src;
        document.getElementById('lightboxName').textContent=card.querySelector('.name').textContent;
        document.getElementById('lightboxMeta').textContent=(card.querySelector('.desc')?card.querySelector('.desc').textContent+' ｜ ':'')+card.querySelector('.meta').textContent;
        document.getElementById('lightbox').classList.add('open');
      }
    });
    renderFavs();

    // ===== 浮動導航 =====
    document.getElementById('backTop').addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
    document.getElementById('backPrev').addEventListener('click',function(){history.back();});
    document.getElementById('floatPrev').addEventListener('click',function(){state.page=Math.max(1,state.page-1);renderPage();window.scrollTo({top:0,behavior:'smooth'});});
    document.getElementById('floatNext').addEventListener('click',function(){
      if(state.page<pages()){state.page+=1;renderPage();}
      window.scrollTo({top:0,behavior:'smooth'});
    });

    // ===== Lightbox 關閉 =====
    var lb=document.getElementById('lightbox');
    document.getElementById('lightboxClose').addEventListener('click',function(){lb.classList.remove('open');});
    lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('open');});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('open'))lb.classList.remove('open');});

    apply();
  })();
"""

html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>美甲圖庫｜{len(rows)} 款美甲設計大全 Nail Art Gallery</title>
<meta name="description" content="美甲圖庫收錄 {len(rows)} 款不同美甲設計，涵蓋 {len(styles)} 種款式（法式、貓眼、暈染、漸層、霧面、亮片水鑽、彩繪等）與 {len(colors)} 種色系，可依色系款式篩選、搜尋與收藏，美甲款式參考首選。">
<link rel="canonical" href="{SITE}/美甲圖庫/">
<meta property="og:type" content="website">
<meta property="og:title" content="美甲圖庫｜{len(rows)} 款美甲款式大全">
<meta property="og:description" content="{len(rows)} 款美甲設計圖庫，{len(styles)} 種款式 × {len(colors)} 種色系，快速篩選瀏覽。">
<meta property="og:url" content="{SITE}/美甲圖庫/">
<meta property="og:image" content="{SITE}/美甲圖庫/assets/{rows[0]['filename']}">
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
{{"@type":"ListItem","position":1,"name":"首頁","item":"{SITE}/"}},
{{"@type":"ListItem","position":2,"name":"美甲圖庫","item":"{SITE}/美甲圖庫/"}}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ItemList","name":"美甲圖庫 {len(rows)} 款","numberOfItems":{len(rows)},"itemListElement":[{item_list}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebSite","name":"美甲圖庫","url":"{SITE}/美甲圖庫/","potentialAction":{{"@type":"SearchAction","target":"{SITE}/美甲圖庫/?q={{search_term_string}}","query-input":"required name=search_term_string"}}}}
</script>
<style>
{CSS}
</style>
</head>
<body>

<!-- ===== 頂部 MegaMenu ===== -->
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="#hero">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2a5 5 0 0 1 5 5v6a5 5 0 0 1-4 4.9V22h-2v-4.1A5 5 0 0 1 7 13V7a5 5 0 0 1 5-5Z"/></svg>
      美甲圖庫
    </a>
    <button class="burger" id="burger" aria-label="開啟選單">☰</button>
    <nav class="mega" id="megaMenu" aria-label="主導覽">
      <a href="#hero">首頁</a>
      <div class="m-item">色系瀏覽<span class="caret">▾</span>
        <div class="dropdown">
{color_links}
        </div>
      </div>
      <div class="m-item">款式瀏覽<span class="caret">▾</span>
        <div class="dropdown">
{style_links}
        </div>
      </div>
      <a href="#grid">全部款式</a>
    </nav>
    <div class="search-box">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="searchInput" type="search" placeholder="搜尋款式…" aria-label="搜尋款式" autocomplete="off">
      <div class="suggest" id="suggestBox"></div>
    </div>
  </div>
</header>

<div class="wrap">
  <!-- ===== 麵包屑 ===== -->
  <nav class="crumb" aria-label="麵包屑">
    <a href="#">首頁</a><span class="sep">›</span><span>美甲圖庫</span>
  </nav>

  <!-- ===== 頁首 ===== -->
  <header class="hero" id="hero">
    <div class="eyebrow">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2a5 5 0 0 1 5 5v6a5 5 0 0 1-4 4.9V22h-2v-4.1A5 5 0 0 1 7 13V7a5 5 0 0 1 5-5Z"/></svg>
      Nail Art Gallery
    </div>
    <h1>美甲圖庫 · {len(rows)} 款款式大全</h1>
    <p class="sub">收錄 {len(rows)} 款美甲設計：{len(colors)} 種色系 × {len(styles)} 種款式。點擊圖片放大、❤ 收藏、支援色系／款式篩選、關鍵字搜尋與分頁瀏覽。</p>
  </header>

  <!-- ===== 篩選列 ===== -->
  <section class="filters" aria-label="篩選">
    <div class="filter-row" id="colorFilters">
      <span class="filter-label">色系</span>
      <button class="chip active" data-color="all">全部</button>
{color_chips}
    </div>
    <div class="filter-row" id="styleFilters">
      <span class="filter-label">款式</span>
      <button class="chip active" data-style="all">全部</button>
{style_chips}
    </div>
    <p class="result-line"><span id="resultText">載入中…</span>
      <button class="tool-btn" id="showFav">❤ 我的收藏</button>
      <button class="tool-btn" id="resetBtn">清除篩選</button>
    </p>
  </section>

  <!-- ===== 圖庫網格 ===== -->
  <main class="grid" id="grid" aria-live="polite">
{chr(10).join(cards)}
  </main>

  <div class="empty" id="empty">沒有符合篩選條件的美甲款式，請調整篩選條件。</div>

  <!-- ===== 分頁 ===== -->
  <nav class="pagination" id="pager" aria-label="分頁"></nav>

  <!-- ===== 頁尾 ===== -->
  <footer>美甲圖庫 · 共 {len(rows)} 款<span class="dot">·</span>Nail Art Gallery<span class="dot">·</span>{len(colors)} 色系 / {len(styles)} 款式</footer>
</div>

<!-- ===== 右下角浮動導航 ===== -->
<div class="float-nav">
  <button class="float-btn" id="backTop" aria-label="回頂部" title="回頂部">⌃</button>
  <button class="float-btn" id="backPrev" aria-label="回上頁" title="回上頁">‹</button>
  <button class="float-btn" id="floatPrev" aria-label="上一頁" title="上一頁">◀</button>
  <button class="float-btn" id="floatNext" aria-label="下一頁" title="下一頁">▶</button>
</div>

<!-- ===== Lightbox ===== -->
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true">
  <button class="close" id="lightboxClose" aria-label="關閉">&times;</button>
  <figure>
    <img id="lightboxImg" src="" alt="">
    <figcaption><b id="lightboxName"></b><span id="lightboxMeta"></span></figcaption>
  </figure>
</div>

<script>
{JS.replace("%TOTAL_PAGES%", str(total_pages)).replace("%PER_PAGE%", str(PER_PAGE))}
</script>
</body>
</html>
"""

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("已產生:", OUT_PATH)
print("卡片數:", len(cards), "| 分頁數:", total_pages, "| 色系:", len(colors), "| 款式:", len(styles))
