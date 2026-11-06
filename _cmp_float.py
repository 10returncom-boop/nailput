# -*- coding: utf-8 -*-
"""比對圖庫原站 vs 主站子站 的浮動導覽（CSS+HTML）是否一致。"""
import re

pairs = [
    (r"D:\_WWW_325_pub\美甲圖庫\celadon-animal.html",
     r"D:\_WWW_325_public\+nailput.com\nailput-gallery\celadon-animal.html"),
]
def float_block(s):
    m = re.search(r'\.float-nav\{.*?</div>', s, flags=re.S)
    return m.group(0) if m else None
for a, b in pairs:
    sa = float_block(open(a, encoding="utf-8").read())
    sb = float_block(open(b, encoding="utf-8").read())
    print("原站 vs 子站 浮動區塊相同:", sa == sb)
    if sa != sb:
        print("--- 原站 ---"); print(sa)
        print("--- 子站 ---"); print(sb)
