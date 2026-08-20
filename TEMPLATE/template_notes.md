# OCAD PDF Template — Design System Reference

This is the single shared template for every OCAD report. Do not create
alternate templates; extend `ocad_style.css` if a new component is needed.

## Build pipeline
1. Generate all charts as PNG (300 dpi) using the OCAD palette via matplotlib,
   saved into a per-report `charts/` folder.
2. Assemble the report as one HTML document that links `ocad_style.css`.
3. Render to PDF with WeasyPrint (`weasyprint report.html report.pdf`).
4. QC the PDF (page count, no overflow, no broken tables) before delivery.

## Palette
- Ivory White `#F5F1E8` — page background
- Oxford Navy `#172A3A` — headings, rules, table headers, chart primary
- Tweed Brown `#6B5744` — secondary text, captions, running headers
- Deep Olive `#3F4A32` — secondary accent, sub-subsection titles
- Camel Beige `#C8AE82` — table rules, borders, zebra tint (mixed into `#EFE8D8`)

## Typography
- Display / section titles: Lora (serif), weight 600-700
- Body text: Liberation Serif (Times-compatible), justified
- Tables, captions, running headers/footers, footnotes: Liberation Sans

## Page structure
- A4, 30mm top / 20mm sides / 22mm bottom margins
- Running header: "OCAD — ONE COMPANY A DAY" (left), section label (right)
- Running footer: report identifier (left), "Page X of Y" (right)
- Cover page uses the `cover` page context (no running header/footer, full bleed ivory with a double navy/camel frame)
- All pages must have a full bleed ivory background `#F5F1E8` (no white page margins).

## Components available in ocad_style.css
`.cover-page`, `.section` (auto page break), `h1.section-title`,
`h2.subsection-title`, `h3.sub-subsection-title`, standard `table` styling,
`.chart-block` / `.chart-row`, `.callout`, `.framework-grid`,
`.disclaimer`, `.footnote-block`, `.source-list`.

## Fonts confirmed available in the render environment
Lora, Liberation Serif, Liberation Sans (all installed system fonts —
no external font loading required, keeping renders reproducible offline).
