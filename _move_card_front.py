# -*- coding: utf-8 -*-
"""把主站首頁的「NailPut 美甲圖庫」粉紅長卡片從 10大主題群之後移到之前。
卡片區塊：<section style="padding:20px 0 4px"><a href="nailput-gallery/index.html">...</section>
"""
import io

p = r"D:\_WWW_325_public\+nailput.com\index.html"
s = open(p, encoding="utf-8").read()

CARD = '<section style="padding:20px 0 4px">'
i_card = s.find(CARD)
print("找到卡片開頭:", i_card >= 0, i_card)
if i_card < 0:
    raise SystemExit("卡片區塊未找到")

i_card_end = s.find('</section>', i_card) + len('</section>')
card_block = s[i_card:i_card_end]
print("卡片區塊長度:", len(card_block))
print("卡片前 60 字:", s[i_card-60:i_card].replace('\n',' ')[-60:])
print("卡片後 40 字:", s[i_card_end:i_card_end+40].replace('\n',' '))

# 10大主題群 section 開始位置（i_card 之前最近一個 <section>，不含卡片自身）
i_10sec = s.rfind('<section>', 0, i_card)
print("10大主題群 section 開始:", i_10sec >= 0, i_10sec)
print("10大主題群前 50 字:", s[i_10sec-50:i_10sec].replace('\n',' ')[-50:])

# 重組：hero + 卡片 + 10大主題群 + 之後
s_new = s[:i_10sec] + card_block + s[i_10sec:i_card] + s[i_card_end:]

open(p, "w", encoding="utf-8", newline="").write(s_new)
print("已移動：卡片現在位於 10大主題群之前。")
print("總長度:", len(s), "->", len(s_new))
