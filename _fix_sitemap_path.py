# -*- coding: utf-8 -*-
"""修正 nailput-gallery sitemap 系統路徑錯誤：
實際部署圖庫在 https://nailput.com/nailput-gallery/，
但 gallery-sitemap.xml / sitemap-index.xml / robots.txt 誤寫成 /美甲圖庫/。
執行：
1. gallery-sitemap.xml：300 筆 <loc> + <image:loc> 的 美甲圖庫/ -> nailput-gallery/
2. sitemap-index.xml：改為引用 /nailput-gallery/gallery-sitemap.xml（移除不存在的 main-sitemap）
3. robots.txt：宣告 /nailput-gallery/sitemap-index.xml
UTF-8 讀寫。
"""
import os, re

sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
OLD = "https://nailput.com/美甲圖庫/"
NEW = "https://nailput.com/nailput-gallery/"

# 1. gallery-sitemap.xml
gp = os.path.join(sub, "gallery-sitemap.xml")
s = open(gp, encoding="utf-8").read()
cnt_loc = s.count(OLD)
ns = s.replace(OLD, NEW)
# 確認剩餘的 image:loc 也替換（統一前綴，一次 replace 全蓋）
open(gp, "w", encoding="utf-8", newline="").write(ns)
print(f"[gallery-sitemap.xml] 替換前綴 {cnt_loc} 處 -> {ns.count(NEW)} 處為 nailput-gallery/")

# 2. sitemap-index.xml
ip = os.path.join(sub, "sitemap-index.xml")
s = open(ip, encoding="utf-8").read()
new_index = '''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- 美甲圖庫專用 sitemap（單款作品頁 + image:image 標籤） -->
  <sitemap>
    <loc>https://nailput.com/nailput-gallery/gallery-sitemap.xml</loc>
    <lastmod>2026-10-13</lastmod>
  </sitemap>
</sitemapindex>
'''
open(ip, "w", encoding="utf-8", newline="").write(new_index)
print("[sitemap-index.xml] 已改為只引用 /nailput-gallery/gallery-sitemap.xml")

# 3. robots.txt
rp = os.path.join(sub, "robots.txt")
s = open(rp, encoding="utf-8").read()
ns = s.replace("https://nailput.com/美甲圖庫/sitemap-index.xml",
               "https://nailput.com/nailput-gallery/sitemap-index.xml")
open(rp, "w", encoding="utf-8", newline="").write(ns)
print("[robots.txt] 已改宣告 /nailput-gallery/sitemap-index.xml")
print("完成。")
