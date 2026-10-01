// Theme assets used by the inner pages (news, projects, services, contact, factories)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const U = "https://minhcuongsteel.com/wp-content/uploads/";
const T = "https://minhcuongsteel.com/wp-content/themes/beit/assets/images/";

const list = [
  ...["icon-date-v-2.png", "icon-da-1.png", "icon-da-2.png", "icon-da-3.png", "share-fb.png", "cate-icon.svg",
    "bg-cate-duan.jpg", "bg-main-dich-vu.png", "bg-dv-lq.png", "bg-detail-dv.png", "dots-22.png",
    "green-arrow.png", "current-location.png"].map((f) => [T + f, "images/theme/" + f]),
  [U + "2023/08/Vector-7.png", "images/theme/select-arrow.png"],
  [U + "2023/10/map-pin-2-fill-2.png", "images/contact/map-pin.png"],
  [U + "2023/10/time-fill.png", "images/contact/time.png"],
  [U + "2023/10/mail-open-fill.png", "images/contact/mail.png"],
  [U + "2023/10/phone-fill.png", "images/contact/phone.png"],
  [U + "2023/11/CBCNV-nha-may-5-scaled.jpg", "images/contact/bg-contact-hero.jpg"],
  [U + "2023/10/7d78f2806968eb80dde3d01b795b449d-compressed-scaled.jpg", "images/factories/bg-factories.jpg"],
];

const headers = { "User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36", Referer: "https://minhcuongsteel.com/" };

async function one([url, dest]) {
  const out = path.join(root, dest);
  if (fs.existsSync(out) && fs.statSync(out).size > 0) return console.log("skip", dest);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const res = await fetch(url, { headers });
  if (!res.ok) return console.error("FAIL", res.status, url);
  fs.writeFileSync(out, Buffer.from(await res.arrayBuffer()));
  console.log("ok  ", dest);
}

let i = 0;
await Promise.all(Array.from({ length: 4 }, async () => { while (i < list.length) await one(list[i++]); }));
