# 美甲圖庫知識網 — 建置規格書 README

> 一個大主題一個資料夾、一次點擊一頁專業分析；改資料不用動模板，N 頁一次到位。

## 標準執行步驟

1. **探查版型**：沿用 `+300種藝術風格` 驗證過的 `build.py + data/ + CONTENT-SPEC.md` 生成器架構。
2. **建立資料層**：`data_master.py`（11 主題/31 子分類）＋ `styles_data.py`（100+ 篇美甲知識）。
3. **內容展開**：`seed.py` 產生 `data/site.json` 與全部 `.md`。
4. **視覺素材**：`gen_images.py` 用 PIL 產生 WebP（章節＋每篇主視覺＋辨識卡）。
5. **頁面生成**：`build.py` 產出全站 HTML。
6. **文件交付**：`gen_excel.py` 產出兩份 Excel；本檔為規格書。
7. **驗收**：`python build.py --check` 須通過全部篇數。

## 明確執行項目指令

```powershell
cd D:\_WWW_325\美甲圖庫知識網
python seed.py         # 展開內容
python gen_images.py   # 產生 WebP
python build.py        # 建置全站
python gen_excel.py    # 產出 Excel
python build.py --check
```

## 網站功能清單（對照需求）

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
| 知識圖譜／收藏清單 | 右側收藏抽屜＋相關標籤關聯 |
| 右下站內導航／回上頁/首頁／分頁 | float-dock＋上一篇/下一篇 pager |
| OG Favicon／OG=9 | 9 個 OG 標籤＋SVG favicon |
| Webp 圖文並茂 | 每篇文章兩張以上 WebP（主視覺＋辨識卡） |
| FAQPage JSON-LD 大白話 | 每篇 Q/A 自動結構化 |
| 3 段結構化資料 | BreadcrumbList＋Article/CollectionPage＋FAQPage/WebSite |
| sitemap/robots/404/manifest | 全數產出 |
| build.py + data/ + CONTENT-SPEC | 生成器架構，改資料不動模板 |
| Topic-Cluster 主題群聚 | 11 主題分 6 大群（新手入門/凝膠水晶/技法款式/延甲保養/經營疑難/比較選用） |
| AEO/RAG 檢索佳 | 每頁 H1/H2、摘要、JSON-LD、純靜態語意清晰 |

## 交付檔案

- `index.html` … 全站靜態頁（直接部署即可）
- `網站地圖.xlsx`：全部頁面清單
- `網站變數與網站導覽.xlsx`：全站變數＋導覽樹＋標籤索引
- `CONTENT-SPEC.md`：內容撰寫規範
- `build.py / seed.py / gen_images.py / gen_excel.py`：可重跑的生成器

## 升級路徑（Astro / Next content collections）

目前為零依賴靜態站，可直接托管。未來要升級：把 `data/articles/**/*.md` 作為
Astro content collections（`src/content/`），`site.json` 對應 `config.ts` collection
schema，組件沿用本樣板（CSS/JS 已與框架無耦合）。

## 404／連結健檢

`python build.py --check` 驗證內容完整性；另可跑下列掃描腳本比對本機檔案，抓出
HTML 內所有內外連結與圖片路徑的 404（見 `check_links.py`）。
