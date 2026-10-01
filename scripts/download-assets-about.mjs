// Assets for the "Giới thiệu" page (gioi-thieu.html)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const U = "https://minhcuongsteel.com/wp-content/uploads/";
const T = "https://minhcuongsteel.com/wp-content/themes/beit/assets/images/";

const list = [
  [U + "2023/11/Anh-toa-nha-tru-so-1-1737x1080.jpg", "images/about/banner.jpg"],
  [U + "2023/10/Header-%E2%86%92-rs-module-wrap-%E2%86%92-rs-module-%E2%86%92-rs-slides-%E2%86%92-rs-slide.png", "images/about/bg-banner.png"],
  [U + "2023/11/316538359_614595350667043_8775414342635265938_n-1536x1024.jpg", "images/about/team.jpg"],
  [U + "2024/05/DJI_0663-1536x1062.jpg", "images/about/factory.jpg"],
  [U + "2023/11/z4331215631225_f215d476311e1eb2ecddefd0c27370a8-768x1024.jpg", "images/about/machines.jpg"],
  [U + "2023/10/Layer_1-5.svg", "images/about/icon-vision.svg"],
  [U + "2023/10/Layer_1-6.svg", "images/about/icon-social.svg"],
  [U + "2023/10/div.section_wrapper-1.png", "images/about/bg-certificates.png"],
  [T + "line.svg", "images/theme/line.svg"],
];

const awards = [
  ["2023/11/Giay-chung-nhan-hop-chuan-thep-keo-nguoi_page-0001", ".jpg", "-495x700"],
  ["2023/11/Chung-chi-Chung-nhan-LTH-Top-100_page-0001", ".jpg", "-495x700"],
  ["2023/10/ISO9001-2015-Tieng-Viet-T-1-1", ".jpg", "-495x700", "-scaled"],
  ["2023/12/Chung-chi-nang-luc-thi-cong-hang", ".jpg", "-495x700", "-scaled"],
  ["2024/08/Chung-nhan-SP-cong-nghiep-chu-luc-TP-HN", ".jpg", "-700x512", "-scaled"],
];
const certs = [
  ["2023/11/27330b0156d047dbb782574e6ae6b4ccTXgK2FcJL1tFDuKZ-2-2", ".png", "-495x700"],
  ["2023/11/27330b0156d047dbb782574e6ae6b4ccTXgK2FcJL1tFDuKZ-0-2", ".png", "-495x700"],
  ["2023/11/2.-Chung-chi-nang-luc-Lap-dat-thiet-bi_page-0001", ".jpg", "-495x700"],
  ["2023/11/Chung-nhan-5S-NM5-1", ".png", "-495x700"],
  ["2023/11/Chung-nhan-5S-NM3_1-1", ".png", "-495x700"],
];
for (const [name, set] of [["award", awards], ["cert", certs]]) {
  set.forEach(([p, ext, thumb, full = ""], i) => {
    list.push([U + p + thumb + ext, `images/about/${name}-${i + 1}${ext}`]);
    list.push([U + p + full + ext, `images/about/${name}-${i + 1}-full${ext}`]);
  });
}

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
await Promise.all(Array.from({ length: 4 }, async () => { while (i < list.length) await one(list[i++]); }));
