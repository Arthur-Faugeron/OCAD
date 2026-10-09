# OCAD report template (LaTeX)

This is the only template for OCAD reports. Every report in `SERIES/` uses `ocad.sty` unchanged.

## Files
- `ocad.sty`        the style: palette, fonts, header and footer, headings, tables, charts, boxes, cover page.
- `template.tex`    the report skeleton in OCAD order (Cover, Executive Summary, A to G). Replace every bracketed item.
- `chart_style.py`  matplotlib palette and save helper for charts. Run it to rebuild the sample charts.
- `charts/`         sample charts used by the skeleton. Replace with the report's own charts (PNG, 220 dpi).
- `template.pdf`    the compiled skeleton, kept as the visual reference.

## Build
Needs XeLaTeX (TeX Live or MiKTeX) and the fonts Liberation Serif, Liberation Sans, TeX Gyre Pagella.

    latexmk -xelatex template.tex

Run it twice if page totals in the footer look wrong. Clean up with `latexmk -c`.

## New report
1. Copy `ocad.sty`, `template.tex` and `charts/` to a working folder and rename `template.tex`.
2. Replace the bracketed items, build the charts with `chart_style.py`, and compile.
3. Save only the final PDF to `SERIES/[Series]/DDMMYYYY_company.pdf` (for example `09102026_rtx.pdf`).

## Components
- Cover: `\ocadcoversetup{...}` then `\makeocadcover`. Leave out `logo=` when no official logo exists.
- Sections: `\section`, `\subsection`, `\subsubsection`. Titles carry their own letters. Sections flow continuously (no forced page break) to avoid blank space; the cover is the only page that stands alone.
- Table: `\begin{ocadtable}{Caption}{columns}`, header with `\ocadtablehead{\ocadH{A}&\ocadH{B}}`, rows end with `\ocadhr`, then `\ocadtablenote{Source: ...}`. Column types: L left, R right, C centre, or `>{\raggedright\arraybackslash}p{30mm}` for a fixed text column.
- Long table with a repeated header: see section F of `template.tex`. Fixed widths plus 2.4 mm padding per column must stay under 170 mm.
- Chart: `\ocadchart{file.png}{Title}{Source, period, units}`; two side by side: `\ocadchartpair`.
- Callout: `\begin{ocadcallout}{Title}...\end{ocadcallout}`. Framework grid: `\fwrow{Label}{Text}`. Flow diagram: `\begin{ocadflow}{n}\flowbox{Title}{Text}...`.
- Footnote block `ocadfootnotes`, sources `\ocadsourcegroup` and `\ocadsource{Org}{Title}{Date}{URL}{Information}`, disclaimer `ocaddisclaimer`.

## Rules
- Palette: Ivory F5F1E8 (background), Oxford Navy 172A3A, Tweed Brown 6B5744, Deep Olive 3F4A32, Camel Beige C8AE82.
- No em dashes, hash signs, asterisks, arrows or other symbols in text. Escape ampersands and percent signs in LaTeX.
- Numbers right aligned, text left aligned. State the currency and unit in every table and chart.
- Do not print Sourced, Reasoned or Calculated tags in the report; state the source in table notes, chart captions and section G instead.
- Do not mention how the report was produced anywhere except the standard disclaimer.
- Every source URL must open publicly (no 404, login or paywall page).
