# -*- coding: utf-8 -*-
"""主站子站 nailput-gallery：只留 Home 與 Line。
- Home：加 .home class → 透明背景（不影響閱讀），連到 https://nailput.com
- 刪除 Back 按鈕（兩種：單款頁無 id、首頁有 id）
- CSS 插入 .float-btn.home 透明樣式
- Line 保留綠底
UTF-8 讀寫。
注意：使用精確字串對，避免取索引誤判。
"""
import glob, os

sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))

HOME_CSS = ".float-btn.home{background:transparent;box-shadow:none;padding:0 4px;color:var(--accent)}\n  .float-btn.home:hover{background:transparent;color:#a25c67}\n  "

CSS_ANCHOR = ".float-btn svg{width:13px;height:13px}\n"

# 精確的 (舊, 新) 字串對
REPL_PAIRS = [
    # 單款頁 Home（連 index.html）
    ('<a class="float-btn" href="index.html" aria-label="回首頁">',
     '<a class="float-btn home" href="https://nailput.com" aria-label="回首頁 NailPut">'),
    # 首頁 Home（連 #top）
    ('<a class="float-btn" href="#top" aria-label="回首頁">',
     '<a class="float-btn home" href="https://nailput.com" aria-label="回首頁 NailPut">'),
    # 刪 Back（單款頁無 id）
    ('  <button class="float-btn" aria-label="回上頁" onclick="history.back()">‹ Back</button>\n', ''),
    # 刪 Back（首頁有 id）
    ('  <button class="float-btn" id="backPrev" aria-label="回上頁" onclick="history.back()">‹ Back</button>\n', ''),
]

changed = 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    ns = s
    if ".float-btn.home{" not in ns and CSS_ANCHOR in ns:
        ns = ns.replace(CSS_ANCHOR, CSS_ANCHOR + HOME_CSS, 1)
    for old, new in REPL_PAIRS:
        ns = ns.replace(old, new)
    if ns != s:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(ns)
        changed += 1

print(f"處理完成：{changed}/{len(htmls)} 個 html（只留 Home+Line、Home 透明連 nailput.com）")
