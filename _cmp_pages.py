# -*- coding: utf-8 -*-
"""比對圖庫原站單款頁 與 repo子站單款頁（舊版完好），確認除浮動區塊外是否一致，
以判斷能否用原站直接覆蓋子站。"""
import re

src = r"D:\_WWW_325_pub\美甲圖庫\celadon-animal.html"
repo = r"D:\_WWW_325\_____nailput.com\美甲圖庫知識網\nailput-gallery\celadon-animal.html"

def strip_float(s):
    # 移除 .float-nav ... </div> 區塊與相關 CSS
    s = re.sub(r'<div class="float-nav">.*?</div>', '[FLOAT-NAV]', s, flags=re.S)
    s = re.sub(r'\.float-nav\{.*?\n', '[CSS]', s)
    s = re.sub(r'\.float-btn[^\n]*\n', '[CSS]', s)
    return s

a = open(src, encoding="utf-8").read()
b = open(repo, encoding="utf-8").read()

sa, sb = strip_float(a), strip_float(b)
print("原站 len:", len(a), "repo len:", len(b))
print("去浮動後相同:", sa == sb)
if sa != sb:
    # 找差異行
    import difflib
    la, lb = sa.splitlines(), sb.splitlines()
    print("行數: 原站", len(la), "repo", len(lb))
    d = list(difflib.unified_diff(la, lb, lineterm="", n=1))
    print("差異行數:", len(d))
    for line in d[:40]:
        print(line)
