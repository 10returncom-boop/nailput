# -*- coding: utf-8 -*-
"""全面驗證工作目錄子站修復結果。"""
import glob, os
sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))
broken, left, back = 0, 0, 0
home_ok, home_nailput, home_class, line_ok = 0, 0, 0, 0
no_float_nav = 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    if "<!DOCTYPE" not in s and "<html" not in s:
        broken += 1
    if "left:16px" in s: left += 1
    if "backPrev" in s or ">Back</button" in s or "‹ Back" in s: back += 1
    if "float-nav" not in s: no_float_nav += 1
    if "href=\"https://nailput.com\"" in s: home_nailput += 1
    if "float-btn home" in s: home_class += 1
    if "float-btn.line" in s or "float-btn line" in s: line_ok += 1
print(f"總數{len(htmls)} 被破壞{broken} 殘留left{left} 殘留Back{back} 無float-nav{no_float_nav}")
print(f"Home連nailput.com:{home_nailput} Home含home class:{home_class} Line存在:{line_ok}")
