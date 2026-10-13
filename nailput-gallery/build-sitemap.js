// build-sitemap.js
// 掃描 ./assets 底下所有 *.webp，自動產生 gallery-sitemap.xml（含 image:image 標籤）
// 用法：node build-sitemap.js
const fs = require('fs');
const path = require('path');

// ========== 【請修改這裡的設定】 ==========
const SITE_DOMAIN = "https://nailput.com";       // 替換成正式網域
const GALLERY_PATH = "/美甲圖庫";                // 圖庫目錄
const ASSET_FOLDER = "assets";                  // assets 目錄（不含 ./ 前綴）
const OUTPUT_FILE = "./gallery-sitemap.xml";
const LASTMOD = new Date().toISOString().split('T')[0];  // 自動今天日期 YYYY-MM-DD
const CHANGEFREQ = "weekly";
const PRIORITY = "0.7";
// ==========================================

// 色系 / 款式中文對照（與 assets 檔名 {color}-{style}.webp 對應）
const COLORS = {
  celadon:"青瓷綠",champagne:"香檳金",cocoa:"可可棕",coral:"珊瑚橘",gray:"灰調",
  lavender:"薰衣草",lemon:"檸檬黃",midnight:"午夜藍",milk:"奶白",mint:"薄荷綠",
  misty:"霧藍",moonlight:"月光銀",morandi:"莫蘭迪",navy:"墨藍",nude:"裸粉",
  obsidian:"黑曜",peach:"蜜桃",pure:"純白",rose:"玫瑰粉",wine:"酒紅"
};
const STYLES = {
  animal:"動物紋",cateye:"貓眼",colorblock:"撞色",french:"法式",geometric:"幾何",
  glitter:"亮片",gradient:"漸層",handpainted:"手繪",jelly:"果凍",marble:"大理石",
  matte:"霧面",metallic:"金屬",minimal:"極簡",mirror:"鏡面",mosaic:"馬賽克",
  ombre:"暈染",pearl:"珍珠",plaid:"格紋",polka:"點點",rainbow:"彩虹",
  retro:"復古",starry:"星空",woodgrain:"木紋"
};

fs.readdir(ASSET_FOLDER, (err, files) => {
  if (err) { console.error("讀取資料夾失敗：", err); return; }
  const webpList = files.filter(f => path.extname(f).toLowerCase() === ".webp");
  console.log(`找到 ${webpList.length} 張 WebP 美甲圖片`);

  let urlBlocks = "";
  webpList.forEach(filename => {
    const base = path.parse(filename).name;            // 例如 celadon-animal
    const parts = base.split("-");
    const colorZh = COLORS[parts[0]] || parts[0];
    const styleZh = STYLES[parts[parts.length-1]] || parts[parts.length-1];
    const pageUrl  = `${SITE_DOMAIN}${GALLERY_PATH}/${base}.html`;
    const imgUrl   = `${SITE_DOMAIN}${GALLERY_PATH}/${ASSET_FOLDER}/${filename}`;
    const title    = `${colorZh}${styleZh}美甲`;
    const caption  = `${colorZh}色系${styleZh}美甲，${colorZh}${styleZh}設計，美甲款式參考圖`;

    urlBlocks += `
  <url>
    <loc>${pageUrl}</loc>
    <lastmod>${LASTMOD}</lastmod>
    <changefreq>${CHANGEFREQ}</changefreq>
    <priority>${PRIORITY}</priority>
    <image:image>
      <image:loc>${imgUrl}</image:loc>
      <image:caption>${caption}</image:caption>
      <image:title>${title}</image:title>
    </image:image>
  </url>`;
  });

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">${urlBlocks}
</urlset>
`;
  fs.writeFile(OUTPUT_FILE, xml, "utf8", we => {
    if (we) { console.error("寫入 XML 失敗：", we); }
    else { console.log(`✅ ${OUTPUT_FILE} 建立完成，總共 ${webpList.length} 筆圖庫頁`); }
  });
});
