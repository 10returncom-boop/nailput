# -*- coding: utf-8 -*-
"""檢查子站被破壞範圍：偵測 `<` 被換成 `a` 的檔（HTML 標籤應以 < 開頭）。"""
import glob, os

sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))
broken = []
ok = []
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    # 正常 HTML 檔應有 <html 或 <!DOCTYPE
    if "<!DOCTYPE" not in s and "<html" not in s and "<head" not in s:
        # 判斷是否全被替換成 a（所有 < 都消失）
        if s.count("<") == 0 and "a" in s:
            broken.append(os.path.basename(p))
        else:
            ok.append(os.path.basename(p))
    else:
        ok.append(os.path.basename(p))
print(f"被破壞檔數: {len(broken)}")
print(f"正常檔數: {len(ok)}")
if broken:
    print("被破壞檔(前10):", broken[:10])
