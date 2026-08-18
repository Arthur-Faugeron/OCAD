# OCAD Template — Series: Transportation

First established: 18 August 2026, with the LATAM Airlines Group S.A. report.

## Build method

Reports in this series are built as a single HTML document styled with `serie_Transportation.css`
(CSS Paged Media, in this same folder) and rendered to PDF with WeasyPrint:

```
python3 -m weasyprint report.html output.pdf
```

The stylesheet is copied verbatim from the Mining & Material / Semiconductor series templates and
implements the OCAD house design system in full: `@page` rules for a 216mm x 279mm page with
running header (company / series+date) and footer (OCAD wordmark / page x of y), a dedicated
`@page cover` with no running header/footer, the Ivory/Oxford Navy/Tweed Brown/Deep Olive/Camel
Beige palette, Liberation Serif for headings (metric-compatible classical serif) and Liberation
Sans for body/tables/footnotes, justified body text, and minimalist navy-header / camel-striped-row
tables. This is the same design system as every other OCAD series — palette and typography stay
constant across all series per CLAUDE.md. Reuse this CSS file as-is for every report in this
series; do not fork it beyond the two `@page` running-header strings, which should be updated per
report to name that report's company and date.

## Page structure produced by the template

1. Cover (`<section class="cover">`) — eyebrow, company title/subtitle, ticker/country/series/date/
   analyst meta row, latest-close price box, price chart panel with source caption, footer.
2. Executive Summary — Business / Financial condition / Market position / Valuation / Investment
   framework prose blocks, closed by an `Investment Profile` table (`.framework-grid`).
3. Section A (About the Business) — A1-A7 exactly as specified in the master CLAUDE.md prompt.
4. Section B (Financial Statements) — B1-B3, each with a `table.data` summary and an embedded chart.
5. Section C (Evaluation) — C1-C4: ratios, a structured risk table, valuation (multiples + DCF
   sensitivity table), and market/technical statistics.
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
survive image embedding. See `build_charts.py` in the LATAM report's working files for the reusable
chart functions relevant to a transportation/airline operator: revenue/growth, margins, operating
cash flow vs. capex vs. FCF, net debt and leverage, ROIC/ROE, a 5-year weekly price line with a
short moving average, a compact 1-year cover-page price panel, peer EV/EBITDA and margin bars, and
an ownership/shareholder-pact pie chart (useful for transportation names with concentrated
strategic/JV shareholders, e.g. airline alliance partners).

## Known constraints to disclose, not silently work around

* This sandboxed environment cannot download arbitrary binary images (company logos) or take live
  browser screenshots in a scheduled/background run where Claude in Chrome is not connected —
  outbound `bash` network access is allowlist-restricted and `web_fetch` does not pass through
  binary/image payloads (confirmed again on the LATAM report: both `curl` to Alpha Vantage's logo
  CDN and `web_fetch` to the same URL failed). Do not fabricate or redraw a logo to compensate.
  Disclose the limitation on the cover/executive summary and point the reader to the company's own
  site for the real mark. Substitute a sourced, dated, analyst-built price chart (matplotlib, real
  OHLC/close data with citation) in place of a literal browser screenshot, and label it plainly as
  a data chart, not a screenshot. If a future session has browser tooling connected (Claude in
  Chrome, with an active connected browser), prefer a real screenshot instead of this workaround.
* The Alpha Vantage MCP connector's TIME_SERIES_DAILY_ADJUSTED endpoint returned a premium-tier
  rate-limit error on this run even though other fundamentals endpoints worked; TIME_SERIES_WEEKLY_
  ADJUSTED (full history) worked and was used instead for all price-history analysis and charts.
  Disclose this substitution wherever a daily-basis figure might otherwise be expected (e.g., exact
  "1 month ago" price points become "nearest weekly observation").
* Several Alpha Vantage fundamentals endpoints (INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW,
  TIME_SERIES_WEEKLY_ADJUSTED) exceed the tool's inline token limit and are saved to a local
  tool-results file instead. That file *is* reachable from the `bash` sandbox (unlike its Windows
  path might suggest) — `find / -iname "*INCOME_STATEMENT*"` locates it under
  `~/.claude/projects/<escaped-cwd>/<session>/tool-results/`. Parse it there with Python/regex
  rather than re-requesting the tool or trying to open the Windows path directly.
* Per-share metrics (EPS, book value/share) can break in comparability across a capital-structure
  event (LATAM cancelled ~30.2bn treasury shares in a 2025 "capital optimization" transaction).
  Check share-count history before building any EPS/BVPS trend chart or table; when a break is
  found, disclose it explicitly rather than silently splicing an inconsistent series, and prefer
  aggregate $ figures (not per-share) for multi-year trend charts spanning the event.
* Prefer primary filings (SEC 20-F/6-K, company press releases) fetched and verified directly via
  `web_fetch` over search-snippet synthesis; only cite a URL in Section G if it was actually
  fetched in the session and rendered real content (not a blank/JS-only page). LATAM's own investor
  relations "Executive Management" page is JS-rendered and returned no usable bios via `web_fetch` —
  management background was instead sourced from the primary press release (CEO, quoted directly)
  and cross-verified secondary reporting (CFO appointment) rather than fabricated or left uncited.
