# One Company A Day

A private, dated compendium of institutional-grade equity research. Published via GitHub Pages.

## Adding a new report

1. Drop the PDF into the matching series folder under `SERIES/`, using the exact folder
   name from the list below. Name the file:

   ```
   DDMMYYYY_SYMBOL.pdf
   ```

   Example: `SERIES/Bank/16082026_SANTANDER.pdf` (16 August 2026, Santander).

   If a ticker symbol is not natural, a short company name works too
   (underscores or hyphens are treated as spaces on the site), e.g.
   `SERIES/Luxury/03092026_Hermes.pdf`.

2. Commit and push:

   ```
   git add SERIES
   git commit -m "Add SERIES report for SYMBOL"
   git push
   ```

That's the entire workflow. There is nothing to edit by hand, and nothing to run
locally. A GitHub Action (`.github/workflows/deploy.yml`) picks up the push, scans
`SERIES/` with `scripts/build.js`, and republishes the site with the new report
included, usually within a minute or two.

The homepage and the archive page are both static HTML that fetch a generated
`reports.json` at load time and render themselves from it - so nothing about the
site's markup ever needs to change when a report is added.

## Series

Folder names under `SERIES/` must match exactly (spelling and punctuation) for the
build script to recognize them:

Energy, Mining & Material, Industrial, Aerospace & Defense, Transportation, Automotive,
Consumer Staple, Consumer Discretionary, Luxury, Retail, Food & Beverage, Healthcare,
Pharma & Biotech, Medical Device, Technology, Semiconductor, Software, Internet & Digital,
Telecommunications & Media, Financial, Bank, Insurance, Asset Management, Real Estate,
Utilities, Infrastructure

A series with no folder, or no PDFs yet, simply appears as "Awaiting First Report" in
the archive. There is nothing to pre-create.

## Site structure

```
index.html                     home page - masthead, last-updated line, latest report
archive.html                   full coverage index with a search box
assets/css/style.css           shared styling
assets/js/site.js              fetches reports.json and renders both pages
scripts/build.js               scans SERIES/ and writes reports.json (CI runs this)
.github/workflows/deploy.yml   builds and deploys to GitHub Pages on every push to main
SERIES/<Series>/DDMMYYYY_*.pdf the reports themselves
```

`reports.json` is a build artifact, not checked into the repository - it is generated
fresh on every deploy. To preview the site locally before pushing, generate it once
yourself and serve the folder statically:

```
node scripts/build.js
python -m http.server 8000
```

Then open `http://localhost:8000`. The local `reports.json` this creates is gitignored
and won't be committed.

## Publishing

GitHub Pages is configured with its build/deploy source set to "GitHub Actions" (not a
branch). The workflow builds a clean `_site/` folder (site files and PDFs only - no git
internals) and deploys it via the official `actions/deploy-pages` action.
