# 內容撰寫規範 CONTENT-SPEC — 美甲圖庫知識網

本檔是全站內容的**唯一格式標準**。所有美甲知識內容由 `seed.py` 依 `styles_data.py` 展開，
要新增／修改文章，只改 `styles_data.py` 與 `content_overrides.py`，**不要動 build.py 模板**。

## 1. 架構（改資料不用動模板）

```
data_master.py      11 大主題、子分類定義（chapter/sub）
styles_data.py      100+ 篇美甲知識明細（每筆 12 欄位，見下）
content_overrides.py 重點文章的大白話客製內文（去 AI 化）
seed.py             → 產生 data/site.json + data/articles/<ch>/<sub>/<slug>.md
build.py            → 讀 site.json + md，產生全站 HTML
gen_images.py       → PIL 產生 assets/images/*.webp（章節＋每篇辨識卡）
gen_excel.py        → 產出「網站地圖.xlsx」「網站變數與網站導覽.xlsx」
```

單一檔案一頁：`data/articles/<chapter>/<sub>/<slug>.md` → `<chapter>/<sub>/<slug>.html`。
一個大主題＝一個資料夾，一次點擊＝一頁專業分析。

## 2. 每筆文章資料欄位（styles_data.py tuple）

```
(ch, sub, slug, zh, en, level, origin, cat, rep_tech, rep_style, traits, tags)
```

- `ch/sub`    ：必須存在於 `data_master.py` 的 CHAPTERS / subs
- `level`     ：入門 / 中階 / 進階
- `origin`    ：日系 / 韓系 / 歐美 / 台式 / 通用（流派／技法源流）
- `cat`       ：適用對象或場合（一句話）
- `rep_tech`  ：代表品牌／工法／工具
- `rep_style` ：代表款式／作品
- `traits`    ：3 條辨識重點（`|` 隔開），自動產生辨識表格
- `tags`      ：4~6 個短標籤（逗號隔開），驅動 Tag System 與相關推薦

## 3. 每篇自動產生的章節（build.py / seed.py 已內建）

1. 一句話搞懂（定義，大白話）
2. 它到底是什麼（原理）
3. 適合誰、什麼場合用
4. 怎麼做（步驟）
5. 優點與缺點（比較表格）
6. 新手常見雷區（Callout 注意）
7. 容易搞混的相似做法
8. 常見問題 FAQ（Q/A，自動轉 FAQPage JSON-LD）

`comparison` 章節走「對照版型」：兩者差在哪／為什麼常被搞混／記憶口訣／該怎麼選。

## 4. 驗證

```
python build.py --check        # 驗證全部 md 完整性
python build.py                # 完整建置
python build.py --list         # 列出每篇數
```

## 5. 重新產出流程（批次更新）

改完 `styles_data.py` / `content_overrides.py` 後依序執行：

```
python seed.py        # 更新 site.json 與全部 md
python gen_images.py  # 若新增文章，補 webp
python build.py       # 重建全站 HTML
python gen_excel.py   # 更新兩份 Excel
```
