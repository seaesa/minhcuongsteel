import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const U = "https://minhcuongsteel.com/wp-content/uploads/";
const T = "https://minhcuongsteel.com/wp-content/themes/beit/assets/";

const list = [];
const add = (url, dest) => list.push([url, dest]);

// hero desktop (13) + mobile
[
  "2023/12/5b24ac6d-2768-4d37-9caa-d92705dd0204-1.jpg", "2023/12/2-compressed.jpg", "2023/12/3-compressed.jpg",
  "2023/12/4-compressed.jpg", "2023/12/5-compressed.jpg", "2023/12/6-compressed.jpg", "2023/12/7-compressed.jpg",
  "2023/12/8-compressed-1.jpg", "2023/12/9-compressed.jpg", "2023/12/10-compressed.jpg", "2023/12/11-compressed.jpg",
  "2023/12/12-compressed-1.jpg", "2023/12/13-compressed-2.jpg",
].forEach((p, i) => add(U + p, `images/hero/hero-${i + 1}.jpg`));
add(U + "2023/10/9-72-compressed-1.jpg", "images/hero/hero-mobile.jpg");

// section backgrounds / misc
add(U + "2023/10/div.wrap_.jpg", "images/bg-products.jpg");
add(U + "2023/10/sdaas-compressed.jpg", "images/bg-why.jpg");
add(U + "2023/10/rs-sbg-px-%E2%86%92-rs-sbg-wrap-%E2%86%92-rs-sbg.png", "images/bg-contact.png");
add(U + "2023/10/Years.png", "images/years.png");
add(U + "2023/10/Group-1.svg", "images/logo-footer.svg");
add(U + "2023/10/FacebookLogo.svg", "images/social/facebook.svg");
add(U + "2023/11/YoutubeLogo.svg", "images/social/youtube.svg");
add(U + "2023/11/icon-zalo-chat-white.png", "images/social/zalo.png");
add(U + "2023/11/linkedin-icon-512x512-a7sf08js.png", "images/social/linkedin.png");
add(U + "2023/11/whatsapp.png", "images/social/whatsapp.png");

// theme decorative assets
["dots.png", "dots2.png", "line-c.svg", "line-c2.svg", "play.png", "arr-right.svg", "arr-right-white.svg",
 "down.svg", "home.svg", "menu.svg", "polygon.svg", "mask-small.png", "map.svg", "phone.svg", "email.svg"]
  .forEach((f) => add(T + "images/" + f, "images/theme/" + f));
add(T + "fonts/Frakturika/FRAKS___.ttf", "fonts/frakturika-spamless.ttf");

// news (8)
[
  "2026/04/IMG_3461-Copy-700x525.jpg", "2026/02/IMG_1938-700x525.jpg",
  "2025/10/570424254_1454714433321793_3161449806321159204_n-700x370.jpg",
  "2025/10/z7108455788382_83ed257d6e3bb8fb13f950faa8a7c708-525x700.jpg",
  "2025/08/Anh-man-hinh-2025-08-25-luc-08.59.14-700x389.png",
  "2025/05/z6629737079217_730d64210ffe615ca192a0cf05a58bb4-700x467.jpg",
  "2025/01/474446186_1205649274894978_7943311239775058339_n.jpg",
  "2024/10/IMG_7616-700x394.jpg",
].forEach((p, i) => add(U + p, `images/news/news-${i + 1}${path.extname(p)}`));

// projects (12 + 12)
[
  "2026/04/IMG_3357-Copy.jpg", "2026/04/669848554_1598405268952708_7771879464407943998_n.jpg",
  "2026/03/z6564274312746_72877aa2efd454aef52e3b3d4dcd568b.jpg", "2025/05/z6220984371644_9c8be1e9e28154bfa385b20759e0bd6f.jpg",
  "2024/09/461075625_3946672172325563_8932366057759100322_n.jpg", "2023/11/Hanaka-26.jpg",
  "2023/11/53b32479a8e376bd2ff2-scaled.jpg", "2023/11/20230511161542-12edit-images2296695images2194234d-16415469000821500200287.jpg",
  "2023/11/z4677053922986_eb7cd14404e9bbd49ce29a257ef28556.jpg", "2023/11/DSC_7461.jpg",
  "2023/11/Du-an-nha-may-HuaYuan-Machinery-Viet-Nam-5-1278x800-1.jpg", "2023/11/z4869757608938_efd80bab245a6465be65255c7c113d6b.jpg",
].forEach((p, i) => add(U + p, `images/projects/noi-dia-${i + 1}.jpg`));
[
  "2026/04/IMG_3215-Copy.jpg", "2026/03/z7070185591626_5714595f9319c27078a3f8726e066740.jpg",
  "2026/03/z7401365828704_ddbd75c8150402dddf5806ebff49f0a8.jpg", "2025/05/495577090_1295706659222572_7419249348642844601_n.jpg",
  "2025/04/z6548725752311_1abfdbe6d3aac50e993a9b8f829072e3.jpg", "2024/12/WOONYOUNG-VINA-3-scaled.jpg",
  "2024/06/z5423197069022_dbf170608aa1bcc4cd5462eef9b0e641.jpg", "2023/11/img_1357-1024x768-1.jpg",
  "2023/11/350524605_2699683410174711_6166830143524248031_n.jpg", "2023/11/z4522950740166_9756fed6c23435de0f42c56c69e92ba4.jpg",
  "2024/06/DSC_7467-1208x800-1.jpg", "2024/06/Du-an-nha-may-HuaYuan-Machinery-Viet-Nam-4-1400x654-1.jpg",
].forEach((p, i) => add(U + p, `images/projects/xuat-khau-${i + 1}.jpg`));

// partners (24)
[
  "2023/11/logo-samsung-inkythuatso-01-29-08-50-42.jpg", "2023/11/logo-lg-vector-inkythuatso-01-30-13-53-58.jpg",
  "2023/11/238769969_132343489096053_1440886953195846736_n.jpg", "2023/11/134556companylogo-scaled.webp",
  "2023/11/tai-xuong.png", "2023/11/tai-xuong.jpg", "2023/11/tai-xuong-4.png", "2023/11/tai-xuong-3.png",
  "2023/11/tai-xuong-1.png", "2023/11/ogimg.png", "2023/11/Mapletree.jpg", "2023/11/logo.png", "2023/11/JFE.jpg",
  "2023/11/dfc.bmp", "2023/11/DELTA-Group-Logo-PNG-1.png", "2023/11/Cong-Ty-Co-Phan-Miza.jpg",
  "2023/11/20210717_OmE1MHvNDBvT.jpg", "2023/11/1200px-Durr_AG_logo.svg.png", "2023/10/0001.jpg", "2023/10/513789.jpg",
  "2023/10/Inox-Hoang-Vu-Logo.jpg.jpg", "2023/10/logo-cong-ty-02.png", "2023/10/logo-cdt-chung-cu-so-9-pham-hung.png",
  "2023/11/Group-9402-5.png",
].forEach((p, i) => add(U + p, `images/partners/partner-${String(i + 1).padStart(2, "0")}${path.extname(p)}`));

const headers = { "User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36", Referer: "https://minhcuongsteel.com/" };

async function one([url, dest]) {
  const out = path.join(root, dest);
  if (fs.existsSync(out) && fs.statSync(out).size > 0) return console.log("skip", dest);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  try {
    const res = await fetch(url, { headers });
    if (!res.ok) return console.error("FAIL", res.status, url);
    fs.writeFileSync(out, Buffer.from(await res.arrayBuffer()));
    console.log("ok  ", dest);
  } catch (e) {
    console.error("ERR ", url, e.message);
  }
}

let i = 0;
await Promise.all(Array.from({ length: 6 }, async () => { while (i < list.length) await one(list[i++]); }));
