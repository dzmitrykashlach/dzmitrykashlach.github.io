import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const [lang] = process.argv.slice(2);

if (!lang || !["en", "ru"].includes(lang)) {
  console.error("Usage: node scripts/export-resume-pdf.mjs <en|ru>");
  process.exit(1);
}

const root = process.cwd();
const inputHtml = resolve(root, `_site/resume/${lang}.html`);
const outputPdf = resolve(root, `_site/resume/resume_${lang}.pdf`);

const html = readFileSync(inputHtml, "utf8");
const injectedStyle = `
<style>
  .site-header, .post-header, .site-footer { display: none !important; }
  .post-content .pdf-name {
    display: block !important;
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin: 0 0 22px;
  }
</style>
`;

let patchedHtml = html.replace("</head>", `${injectedStyle}\n</head>`);
patchedHtml = patchedHtml.replace(
  '<div class="post-content">',
  '<div class="post-content"><p class="pdf-name">Dzmitry Kashlach</p>'
);
const tempDir = mkdtempSync(join(tmpdir(), "resume-pdf-"));
const tempHtml = join(tempDir, `resume-${lang}-pdf.html`);

try {
  writeFileSync(tempHtml, patchedHtml, "utf8");
  execFileSync(
    "chrome-headless-render-pdf",
    [
      "--window-size",
      "1280,2000",
      "--url",
      `file://${tempHtml}`,
      "--pdf",
      outputPdf,
    ],
    { stdio: "inherit" }
  );
} finally {
  rmSync(tempDir, { recursive: true, force: true });
}
