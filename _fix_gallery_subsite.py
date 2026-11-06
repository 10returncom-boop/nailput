# -*- coding: utf-8 -*-
"""修復主站 nailput-gallery 子站斷鏈：
1. 300 個單款頁回首頁連結 美甲圖庫.html -> index.html
2. 移除 index.html 未接線的 lightbox 破圖（img src=""）
純連結修正，不動任何網址本體；UTF-8 讀寫。
"""
import os, glob, re

sub = r"D:\_WWW_325_public\nailput.com\nailput-gallery"

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def write(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

# 1) 300 單款頁：美甲圖庫.html -> index.html
single = [p for p in glob.glob(os.path.join(sub, "*.html"))
          if os.path.basename(p) not in ("index.html",)]
changed = 0
for p in single:
    s = read(p)
    if "美甲圖庫.html" in s:
        ns = s.replace("美甲圖庫.html", "index.html")
        if ns != s:
            write(p, ns); changed += 1
print(f"單款頁替換完成：{changed}/{len(single)}")

# 2) index.html：移除 lightbox（精確字串替換，比照圖庫原站修法）
idx = os.path.join(sub, "index.html")
s = read(idx)

# CSS 7 行
css_block = """  .lightbox{position:fixed;inset:0;background:rgba(30,20,18,.82);display:none;align-items:center;justify-content:center;z-index:60;padding:24px}
  .lightbox.open{display:flex}
  .lightbox figure{max-width:min(92vw,440px);width:100%;background:var(--surface);border-radius:14px;overflow:hidden}
  .lightbox img{width:100%;display:block}
  .lightbox figcaption{padding:14px 18px;font-size:14px;color:var(--muted)}
  .lightbox figcaption b{color:var(--ink);font-size:16px;display:block;margin-bottom:4px}
  .lightbox .close{position:absolute;top:16px;right:20px;background:none;border:none;color:#fff;font-size:34px;cursor:pointer;line-height:1;font-family:inherit}
"""
# HTML 燈箱
html_block = """<div class="lightbox" id="lightbox" role="dialog" aria-modal="true">
  <button class="close" id="lightboxClose" aria-label="關閉">&times;</button>
  <figure>
    <img id="lightboxImg" src="" alt="">
    <figcaption><b id="lightboxName"></b><span id="lightboxMeta"></span></figcaption>
  </figure>
</div>

"""
# JS 關閉邏輯
js_block = """  // Lightbox 關閉
  var lb=document.getElementById('lightbox');
  document.getElementById('lightboxClose').addEventListener('click',function(){lb.classList.remove('open');});
  lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('open');});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('open'))lb.classList.remove('open');});

"""

c1 = css_block in s
c2 = html_block in s
c3 = js_block in s
print(f"CSS含={c1} HTML含={c2} JS含={c3}")
s = s.replace(css_block, "\n").replace(html_block, "\n").replace(js_block, "\n")
write(idx, s)
print("index.html 已處理，lightboxImg 殘留:", "lightboxImg" in read(idx))
