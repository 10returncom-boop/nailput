# -*- coding: utf-8 -*-
"""統一主站子站 CSS 細節與圖庫原站一致：gap、.line padding。"""
import glob, os
sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))
changed = 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    ns = s
    ns = ns.replace(".float-nav{position:fixed;right:16px;bottom:16px;display:flex;flex-direction:column;gap:8px;",
                    ".float-nav{position:fixed;right:16px;bottom:16px;display:flex;flex-direction:column;gap:6px;")
    ns = ns.replace(".float-btn.line{background:#06C755}",
                    ".float-btn.line{background:#06C755;padding:0 6px}")
    if ns != s:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(ns)
        changed += 1
print(f"已統一 CSS：{changed}/{len(htmls)}")
