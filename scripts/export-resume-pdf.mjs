import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const RESUME_SLUGS = ["en", "ru", "non-it-ru"];

const [slug] = process.argv.slice(2);

if (!slug || !RESUME_SLUGS.includes(slug)) {
  console.error(`Usage: node scripts/export-resume-pdf.mjs <${RESUME_SLUGS.join("|")}>`);
  process.exit(1);
}

const root = process.cwd();
const inputHtml = resolve(root, `_site/resume/${slug}.html`);
const outputPdf = resolve(root, `_site/resume/resume_${slug.replace(/-/g, "_")}.pdf`);

if (!existsSync(inputHtml)) {
  console.error(`Resume HTML not found: ${inputHtml}`);
  console.error("Run: npm run build:site");
  process.exit(1);
}

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
const tempHtml = join(tempDir, `resume-${slug}-pdf.html`);

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
