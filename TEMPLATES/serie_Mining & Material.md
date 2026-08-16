# OCAD Template — Series: Mining & Material

First established: 16 August 2026, with the SQM (Sociedad Química y Minera de Chile S.A.) report.

## Build method

Reports in this series are built as a single HTML document styled with `serie_Mining & Material.css`
(CSS Paged Media, in this same folder) and rendered to PDF with WeasyPrint:

```
python3 -m weasyprint report.html output.pdf
```

The stylesheet implements the OCAD house design system in full: `@page` rules for a 216mm x 279mm
page with running header (company / series+date) and footer (OCAD wordmark / page x of y), a
dedicated `@page cover` with no running header/footer, the Ivory/Oxford Navy/Tweed Brown/Deep
Olive/Camel Beige palette, Liberation Serif for headings (metric-compatible classical serif) and
Liberation Sans for body/tables/footnotes, justified body text, and minimalist navy-header /
camel-striped-row tables. Reuse the CSS file as-is for every report in this series; do not fork it
per report. If a new series needs a template, copy this file as a starting point and adjust only
what the CLAUDE.md design system permits (palette and typography stay constant across all series).

## Page structure produced by the template

1. Cover (`<section class="cover">`) — eyebrow, company title/subtitle, ticker/country/series/date/
   analyst meta row, latest-close price box, price chart panel with source caption, footer.
2. Executive Summary — Business / Financial condition / Market position / Valuation / Investment
   framework prose blocks, closed by an `Investment Profile` table (`.framework-grid`).
3. Section A (About the Business) — A1-A7 exactly as specified in the master CLAUDE.md prompt.
4. Section B (Financial Statements) — B1-B3, each with a `table.data` summary and an embedded chart.
5. Section C (Evaluation) — C1-C4: ratios, a structured risk table, valuation (multiples + DCF
   scenario table), and market/technical statistics.
6. Section D (Investment Thesis) — three-column Bull/Base/Bear (`.thesis-cols`), catalysts, and a
   monitoring table.
7. Section E (Final Investment Framework) — `.framework-grid` table plus a `.callout` block for
   Thesis Invalidation.
8. Section F (Data Table) — standardized snapshot, `table.data`.
9. Section G (Sources & Methodology) — Primary/Secondary/Market Data/Calculations subsections,
   each source as a `.src-item` block with organization, title, URL and what it was used for,
   followed by the standard `.disclaimer` block.

## Charts

Charts are built with matplotlib against the same five hex colors, Liberation Serif titles, ivory
background, and a source/methodology caption baked into every figure (`fig.text(...)`) so captions
survive image embedding. See `build_charts.py` in the SQM report's working files for the reusable
chart functions (revenue/growth, margins, FCF, net debt, ROE/ROIC, segment mix pie, 5-year price
line, peer P/E bars, and a compact cover-page price panel).

## Known constraints to disclose, not silently work around

* This sandboxed environment cannot download arbitrary binary images (company logos) or take live
  browser screenshots — outbound `bash` network access is allowlist-restricted and `web_fetch`
  does not pass through binary/image payloads. Do not fabricate or redraw a logo to compensate.
  Disclose the limitation on the cover/executive summary (as done in the SQM report) and point the
  reader to the company's own site for the real mark. If a future session has browser tooling
  connected (Claude in Chrome, with an active connected browser), prefer a real screenshot of the
  official site and the exchange's price chart instead of this workaround.
* Prefer primary filings (SEC 6-K/20-F, company press releases) fetched and verified directly via
  `web_fetch` over search-snippet synthesis; only cite a URL in Section G if it was actually
  fetched in the session and rendered real content (not a blank/JS-only page).
