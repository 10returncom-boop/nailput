# -*- coding: utf-8 -*-
"""確認 repo 子站 301 檔完好（無 < 變 a 破壞），並檢查其浮動導覽版本。"""
import glob, os

repo_sub = r"D:\_WWW_325\_____nailput.com\美甲圖庫知識網\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(repo_sub, "*.html")))
print("repo 子站 html 數:", len(htmls))
broken = 0
left = 0
right = 0
has_back = 0
sample = None
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    if "<!DOCTYPE" not in s and "<html" not in s:
        broken += 1
    if "left:16px" in s:
        left += 1
    if "right:16px" in s:
        right += 1
    if "backPrev" in s or ">‹ Back<" in s or ">Back</button" in s:
        has_back += 1
print(f"被破壞: {broken}, 用 left: {left}, 用 right: {right}, 含 Back: {has_back}")
