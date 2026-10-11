# NailPut 美甲知識與選購指南 — README

> 美甲知識庫：從凝膠、水晶到彩繪與款式，認識原理、做法步驟、優缺點與新手雷區，一站搞懂美甲。

## 專案資訊

- **網站名稱**：NailPut 美甲知識與選購指南
- **網域**：https://nailput.com/
- **託管**：GitHub Pages（https://github.com/10returncom-boop/nailput）
- **本地路徑**：`D:\_WWW_325\_____nailput.com\美甲圖庫知識網\`
- **文章數**：128 篇
- **主題數**：10 大主題群

## 標準執行步驟

1. **探查版型**：沿用驗證過的 `build.py + data/ + CONTENT-SPEC.md` 生成器架構。
2. **資料層**：`data_master.py`（10 主題/子分類）＋ `styles_data.py`（128 篇美甲知識）。
3. **內容展開**：`seed.py` 產生 `data/site.json` 與全部 `.md`。
4. **視覺素材**：`gen_images.py` 用 PIL 產生 WebP（章節＋每篇主視覺＋辨識卡）。
5. **頁面生成**：`build.py` 產出全站 HTML。
6. **文件交付**：`gen_excel.py` 產出兩份 Excel。
7. **部署**：`git add . && git commit -m "msg" && git push` → GitHub Pages 1~2 分鐘生效。

## 明確執行項目指令

```powershell
cd D:\_WWW_325\_____nailput.com\美甲圖庫知識網
python seed.py         # 展開內容
python gen_images.py   # 產生 WebP
python build.py        # 建置全站
python gen_excel.py    # 產出 Excel
git add . && git commit -m "更新說明" && git push
```

## 10 大主題群

| # | 主題 | 英文名 | 子分類 |
|---|---|---|---|
| 1 | 入門與基礎 | Basics | 認識指甲與甲床、衛生消毒與器材、美甲師入門 |
| 2 | 凝膠美甲 | Gel Nails | 凝膠基礎、底膠與上層、光療燈與固化、可剝凝膠 |
| 3 | 水晶指甲 | Acrylic Nails | 水晶原理、水晶延甲、水晶雕塑 |
| 4 | 彩繪技法 | Nail Art Techniques | 手繪彩繪、漸層與暈染、大理石與紋理、法式美甲、進階技法 |
| 5 | 款式風格 | Nail Styles | 流行款式、極簡與商務、場合款式、個性風格 |
| 6 | 延甲與矯正 | Extension & Correction | 延甲技法、甲型矯正、甲片應用 |
| 7 | 卸甲與保養 | Removal & Care | 正確卸甲、指甲健康、手部保養 |
| 8 | 產品與工具 | Products & Tools | 色膠選擇、工具挑選、設備與環境 |
| 9 | 沙龍經營 | Salon Business | 定價與成本、服務流程與客訴、行銷與社群、衛生法規與證照 |
| 10 | NailPut專欄 | NailPut Column | 起翹與掉落、變黃與染色、過敏與刺激、新手失誤、技法對照、選用指南 |

> 「選用比較」已併入 NailPut專欄（troubleshoot/compare + troubleshoot/choose）。

## 網站功能清單

| 需求 | 實作 |
|---|---|
| Breadcrumb → BreadcrumbList schema | 每頁麵包屑＋JSON-LD |
| 內頁卡片 accordion | 首頁章節卡片手風琴展開 |
| Sidebar treemap + TOC | 左欄樹狀導覽＋右欄本頁目錄 |
| 預設白天 | localStorage `art-theme` 預設 light |
| MegaMenu | 頂部主題群 Mega Menu（3 層內下拉） |
| Tag System | tags/ 標籤頁＋標籤雲 |
| 全站搜尋＋自動完成 | 頂欄即時建議（文章/主題/標籤） |
| 多面向篩選 Faceted Search | search.html 左側主題/難度/關鍵字 |
| 相關文章推薦 | 每篇末尾「相關文章」卡片 |
| 最新文章卡片 | 首頁顯示 6 篇：長標題＋作者＋摘要 |
| OG Favicon／OG | 完整 OG/Twitter Card/Canonical＋SVG favicon（粉底白字N） |
| FAQPage JSON-LD 大白話 | 每篇 Q/A 自動結構化 |
| 3 段結構化資料 | BreadcrumbList＋Article/CollectionPage＋FAQPage/WebSite |
| sitemap/robots/404/manifest | 全數產出 |
| SEO 長尾標題 | 比較/選用文章標題含關鍵字＋問句 |
| Footer | © 2026 NailPut美甲知識與選購指南 · nailput.com · Line: 331.today |

## 交付檔案

- `index.html` … 全站首頁
- `build.py / seed.py / gen_images.py / gen_excel.py`：可重跑的生成器
- `data_master.py`：主題/SITE 設定
- `styles_data.py`：128 篇文章資料
- `content_overrides.py`：客製內文
- `CONTENT-SPEC.md`：內容撰寫規範
- `網站地圖.xlsx`：全部頁面清單
- `網站數據與網站導覽.xlsx`：全站變數＋導覽樹＋標籤索引

## DNS 設定（GoDaddy）

- A 紀錄 @ → 185.199.108.153 / 109.153 / 110.153 / 111.153（TTL 600 秒）
- CNAME www → 10returncom-boop.github.io.
