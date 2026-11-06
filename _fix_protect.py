# -*- coding: utf-8 -*-
"""主站子站 nailput-gallery：標題換行 + 全站保護（防選取/拖拽/右鍵/複製）。"""
import glob, os
sub = r"D:\_WWW_325_public\+nailput.com\nailput-gallery"
htmls = sorted(glob.glob(os.path.join(sub, "*.html")))

PROTECT_CSS = """  /* 全站保護：防選取、防拖拽存圖、防右鍵 */
  body{user-select:none;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none}
  img, svg{-webkit-user-drag:none;user-select:none}
"""

PROTECT_JS = """<script>
/* 全站保護：防右鍵、防拖拽、防複製、防另存快捷鍵 */
document.addEventListener('contextmenu',function(e){e.preventDefault();return false;});
document.addEventListener('dragstart',function(e){e.preventDefault();return false;});
document.addEventListener('selectstart',function(e){e.preventDefault();});
document.addEventListener('copy',function(e){e.preventDefault();});
document.addEventListener('keydown',function(e){if(e.key==='F12'||e.ctrlKey&&(e.key==='s'||e.key==='S'||e.key==='u'||e.key==='U')){e.preventDefault();return false;}});
</script>
</body>
"""

# CSS 插入錨點：footer .dot 行之後接 </style>；或 footer 樣式後
CSS_ANCHORS = [
    "  footer .dot{margin:0 6px;color:var(--accent)}\n</style>",
    "  footer{margin-top:38px;text-align:center;font-size:13px;color:var(--muted)}\n</style>",
]

changed = 0
for p in htmls:
    with open(p, encoding="utf-8") as f:
        s = f.read()
    ns = s
    # 1. 標題換行
    ns = ns.replace(
        "<h1>NailPut 美甲圖庫 · 300 款最流行最酷風格</h1>",
        "<h1>NailPut 美甲圖庫<br>300 款最流行最酷風格</h1>")
    # 2. 保護 CSS
    if "user-select:none" not in ns:
        for a in CSS_ANCHORS:
            if a in ns:
                ns = ns.replace(a, a.replace("</style>", PROTECT_CSS + "</style>"), 1)
                break
    # 3. 保護 JS（在 </body> 前）
    if "document.addEventListener('contextmenu'" not in ns and ns.rstrip().endswith("</html>"):
        ns = ns.replace("</body>", PROTECT_JS, 1)
    if ns != s:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(ns)
        changed += 1

print(f"處理完成：{changed}/{len(htmls)}（標題換行 + 全站保護）")
