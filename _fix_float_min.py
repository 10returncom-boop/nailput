# -*- coding: utf-8 -*-
"""把主站子站 nailput-gallery 的浮動導覽按鈕縮到最小，與圖庫原站一致。
首頁與單款頁兩種樣式都改。UTF-8 讀寫。
"""
import glob, os

sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))

# 兩種舊樣式 → 統一最小版
REPL = {
    # 首頁 44px 版
    ".float-btn{height:44px;min-width:44px;padding:0 14px;border-radius:999px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 6px 16px rgba(150,110,95,.3);font-family:inherit;font-size:14px;font-weight:700;text-decoration:none}":
        ".float-btn{height:32px;min-width:32px;padding:0 8px;border-radius:999px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:4px;box-shadow:0 4px 10px rgba(150,110,95,.25);font-family:inherit;font-size:10px;font-weight:700;text-decoration:none}",
    # 單款頁 42px 版
    ".float-btn{height:42px;min-width:42px;padding:0 13px;border-radius:999px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;font-size:14px;font-weight:700;box-shadow:0 6px 14px rgba(150,110,95,.3);font-family:inherit;text-decoration:none}":
        ".float-btn{height:32px;min-width:32px;padding:0 8px;border-radius:999px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:4px;font-size:10px;font-weight:700;box-shadow:0 4px 10px rgba(150,110,95,.25);font-family:inherit;text-decoration:none}",
    # svg 縮小（首頁17 / 單款16 → 13）
    ".float-btn svg{width:17px;height:17px}":
        ".float-btn svg{width:13px;height:13px}",
    ".float-btn svg{width:16px;height:16px}":
        ".float-btn svg{width:13px;height:13px}",
    # gap 6 → 4
    "display:flex;align-items:center;justify-content:center;gap:6px;":
        "display:flex;align-items:center;justify-content:center;gap:4px;",
}

changed = 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    ns = s
    for old, new in REPL.items():
        ns = ns.replace(old, new)
    if ns != s:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(ns)
        changed += 1

print(f"處理完成：{changed}/{len(htmls)} 個 html 已縮到最小")
