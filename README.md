# One Company A Day

A private, dated compendium of institutional-grade equity research. Published via GitHub Pages.

## Adding a new report

1. Drop the PDF into the matching series folder at the repository root, using the exact
   folder name from the Series list below. Name the file:

   ```
   DDMMYYYY_SYMBOL.pdf
   ```

   Example: `Bank/16082026_SANTANDER.pdf` (16 August 2026, Santander).

   If a ticker symbol is not natural, a short company name works too
   (underscores or hyphens are treated as spaces on the site), e.g.
   `Luxury/03092026_Hermes.pdf`.

2. Regenerate the homepage and push:

   ```
   node scripts/build.js
   git add -A
   git commit -m "Add SERIES report for SYMBOL"
   git push
   ```

That's the entire workflow. `scripts/build.js` scans every series folder, reads the PDFs
it finds there, and rewrites `index.html` from `scripts/template.html`. It has no
dependencies beyond Node's built-in modules, so there is nothing to install and nothing
to go stale.

## Series

Folder names must match exactly (spelling and punctuation) for the build script to
recognize them:

Energy, Mining & Material, Industrial, Aerospace & Defense, Transportation, Automotive,
Consumer Staple, Consumer Discretionary, Luxury, Retail, Food & Beverage, Healthcare,
Pharma & Biotech, Medical Device, Technology, Semiconductor, Software, Internet & Digital,
Telecommunications & Media, Financial, Bank, Insurance, Asset Management, Real Estate,
Utilities, Infrastructure

A series with no folder, or no PDFs yet, simply appears as "Awaiting First Report" on
the site. There is nothing to pre-create.

## Publishing

GitHub Pages is configured to serve from the `main` branch, root folder. Since
`index.html` is a plain static file (no build step at deploy time), any push to `main`
goes live within a minute or two, once `node scripts/build.js` has been run locally.

## Structure

```
index.html               generated homepage - do not hand-edit, run the build script instead
assets/css/style.css     site styling
scripts/build.js         regenerates index.html by scanning series folders
scripts/template.html    the HTML shell build.js fills in
<Series>/DDMMYYYY_*.pdf  the reports themselves
```
