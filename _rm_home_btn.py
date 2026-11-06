# -*- coding: utf-8 -*-
"""批次刪除 nailput-gallery 全部 html 的 Home 浮動按鈕，只保留 Line。"""
import os, glob

HOME_A = '''  <a class="float-btn home" href="https://nailput.com" aria-label="回首頁 NailPut"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 10.5 12 3l9 7.5M5 9.5V21h5v-6h4v6h5V9.5"/></svg>Home</a>
'''

sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
files = glob.glob(os.path.join(sub, "*.html"))
changed = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    if HOME_A in s:
        ns = s.replace(HOME_A, "")
        open(f, "w", encoding="utf-8", newline="").write(ns)
        changed += 1
print(f"處理 {len(files)} 個 html，刪除 Home 按鈕 {changed} 個。")
