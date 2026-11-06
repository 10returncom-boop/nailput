# -*- coding: utf-8 -*-
"""檢查工作目錄子站是否已恢復完好。"""
import glob, os
sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))
broken, left, right, back = 0, 0, 0, 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    if "<!DOCTYPE" not in s and "<html" not in s:
        broken += 1
    if "left:16px" in s: left += 1
    if "right:16px" in s: right += 1
    if "backPrev" in s or ">Back</button" in s or "‹ Back" in s: back += 1
print(f"工作子站 總數{len(htmls)} 被破壞{broken} left{left} right{right} 含Back{back}")
