# OCAD Template — Series: Semiconductor

First established: 17 August 2026, with the ASML Holding N.V. report.

## Build method

Reports in this series are built as a single HTML document styled with `serie_Semiconductor.css`
(CSS Paged Media, in this same folder) and rendered to PDF with WeasyPrint:

```
python3 -m weasyprint report.html output.pdf
```

The stylesheet implements the OCAD house design system in full: `@page` rules for a 216mm x 279mm
page with running header (company / series+date) and footer (OCAD wordmark / page x of y), a
dedicated `@page cover` with no running header/footer, the Ivory/Oxford Navy/Tweed Brown/Deep
Olive/Camel Beige palette, Liberation Serif for headings (metric-compatible classical serif) and
Liberation Sans for body/tables/footnotes, justified body text, and minimalist navy-header /
camel-striped-row tables. This is the same design system as `serie_Mining & Material.css` — palette
and typography stay constant across every series per CLAUDE.md. Reuse this CSS file as-is for every
report in this series; do not fork it beyond the two @page running-header strings, which should be
updated per report to name that report's company and date.

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
survive image embedding. See `build_charts.py`, `build_charts2.py` and `build_charts3.py` in the
ASML report's working files for the reusable chart functions (revenue/growth, margins, cash flow,
net cash/debt, ROE/ROIC, price line with moving average, peer market-cap/revenue bars, peer
margin/valuation bars, geographic mix pie, product-segment mix pie, and historical valuation
multiples).

## Known constraints to disclose, not silently work around

* This sandboxed environment cannot download arbitrary binary images (company logos) or take live
  browser screenshots in a scheduled/background run where Claude in Chrome is not connected —
  outbound `bash` network access is allowlist-restricted and `web_fetch` does not pass through
  binary/image payloads. Do not fabricate or redraw a logo to compensate. Disclose the limitation
  on the cover/executive summary and point the reader to the company's own site for the real mark.
  Substitute a sourced, dated, analyst-built price chart (matplotlib, real OHLC data with citation)
  in place of a literal browser screenshot, and label it plainly as a data chart, not a screenshot.
  If a future session has browser tooling connected (Claude in Chrome, with an active connected
  browser), prefer a real screenshot of the official site and the exchange's price chart instead of
  this workaround.
* The Alpha Vantage MCP connector available in this project has a hard daily cap (25 requests/day)
  that is frequently already exhausted by the time a scheduled run starts. Do not depend on it for
  the primary data pull — treat it as a bonus source if capacity happens to be available, and default
  to fetching company press releases/6-K/20-F filings and reputable secondary aggregators
  (StockAnalysis.com, backed by S&P Global Market Intelligence) directly via `web_fetch`.
* Prefer primary filings (SEC 6-K/20-F, company press releases) fetched and verified directly via
  `web_fetch` over search-snippet synthesis; only cite a URL in Section G if it was actually
  fetched in the session and rendered real content (not a blank/JS-only page).
