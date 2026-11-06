# -*- coding: utf-8 -*-
"""檢查主站 nailput.com 主體（排除 nailput-gallery 子站）的斷鏈/破圖。"""
import sys, glob, os
sys.path.insert(0, r"D:\_WWW_325_pub\美甲圖庫")
import check_links as c

root = r"D:\_WWW_325_public\nailput.com"
# 手動掃描主體，略過子站
htmls = [f for f in glob.glob(os.path.join(root, "**", "*.html"), recursive=True)
         if "\\nailput-gallery\\" not in f]
print(f"掃描主體 HTML 數: {len(htmls)}")
link_miss, img_miss, img_noalt = [], [], []
for f in htmls:
    rel = os.path.relpath(f, root)
    with open(f, encoding="utf-8") as fp: content = fp.read()
    pa = c.P(); pa.feed(content)
    for href in pa.links:
        ap, st = c.resolve(root, rel, href)
        if st == "missing": link_miss.append((rel, href))
    for src, alt in pa.imgs:
        if not src: img_miss.append((rel, "(無src)")); continue
        if src.startswith(c.EXTERNAL): continue
        ap, st = c.resolve(root, rel, src)
        if st == "missing": img_miss.append((rel, src))
        if not (alt or "").strip(): img_noalt.append((rel, src))
print(f"斷鏈(404): {len(link_miss)}")
for r, h in link_miss[:30]: print(f"  [{r}] -> {h}")
print(f"圖片404/破圖: {len(img_miss)}")
for r, s in img_miss[:20]: print(f"  [{r}] -> {s}")
print(f"圖片缺alt: {len(img_noalt)}")
for r, s in img_noalt[:20]: print(f"  [{r}] -> {s}")
print("結果:", "PASS" if not (link_miss or img_miss) else "FAIL")
