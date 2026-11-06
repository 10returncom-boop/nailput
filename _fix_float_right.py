# -*- coding: utf-8 -*-
"""把主站子站 nailput-gallery 的浮動導覽 left:16px 改為 right:16px（放右邊）。
僅改子站 html，保留系統檔與其他頁面。UTF-8 讀寫。
"""
import glob, os

sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))
changed = 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    ns = s.replace(
        ".float-nav{position:fixed;left:16px;bottom:16px;",
        ".float-nav{position:fixed;right:16px;bottom:16px;"
    )
    if ns != s:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(ns)
        changed += 1
print(f"處理完成：{changed}/{len(htmls)} 個 html 已改為 right:16px")
