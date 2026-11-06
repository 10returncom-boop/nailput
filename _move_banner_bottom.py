# -*- coding: utf-8 -*-
"""把首頁美甲圖庫滿版橫幅移到頁面最底部（最新文章 section 之後、wrap 結束前）。"""
p = r"D:\_WWW_325_public\+nailput.com\index.html"
s = open(p, encoding="utf-8").read()

BANNER_OPEN = '<section style="margin:0 -20px 26px">'
i_b = s.find(BANNER_OPEN)
print("找到橫幅開頭:", i_b >= 0, i_b)
if i_b < 0:
    raise SystemExit("橫幅未找到")

i_b_end = s.find('</section>', i_b) + len('</section>')
banner = s[i_b:i_b_end]
print("橫幅長度:", len(banner))

# 移除原橫幅
s2 = s[:i_b] + s[i_b_end:]

# 定位 wrap 結尾（最新文章 section 結束後的最後一個 </section></div>）
marker = '</section></div>'
i_m = s2.rfind(marker)
print("wrap 結尾 marker 位置:", i_m >= 0, i_m)
if i_m < 0:
    raise SystemExit("wrap 結尾未找到")
# 確認這是檔內最後一個 section 結尾
print("marker 後 30 字:", s2[i_m:i_m+30].replace('\n',' '))

# 插入點：在 </section> 之後、</div> 之前
i_insert = i_m + len('</section>')
s3 = s2[:i_insert] + banner + s2[i_insert:]

open(p, "w", encoding="utf-8", newline="").write(s3)
print("已把橫幅移到頁面最底部。")
print("長度:", len(s), "->", len(s3))
