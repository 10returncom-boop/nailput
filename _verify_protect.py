# -*- coding: utf-8 -*-
"""驗證子站：標題換行、保護 CSS/JS、無結構破壞。"""
import glob, os
sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))
broken, br_title, css_protect, js_protect = 0, 0, 0, 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    if "<!DOCTYPE" not in s and "<html" not in s:
        broken += 1
    if "NailPut 美甲圖庫<br>300 款最流行最酷風格" in s:
        br_title += 1
    if "user-select:none" in s and "-webkit-user-drag:none" in s:
        css_protect += 1
    if "document.addEventListener('contextmenu'" in s:
        js_protect += 1
print(f"總數{len(htmls)} 被破壞{broken} 標題換行{br_title} CSS保護{css_protect} JS保護{js_protect}")
