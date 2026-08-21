#!/usr/bin/env node
"use strict";

/*
 * Scans SERIES/ and writes reports.json, the single data file both
 * index.html and archive.html fetch at runtime to render themselves.
 *
 * Runs automatically on every push via .github/workflows/deploy.yml.
 * You do not need to run this by hand - it's here mainly so you can
 * preview locally (python -m http.server, or similar) before pushing.
 *
 * No dependencies beyond Node's built-in fs/path modules, on purpose,
 * so this keeps working with no maintenance for years.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SERIES_ROOT = path.join(ROOT, "SERIES");

// Canonical series list, exact spelling as used in CLAUDE.md / on report covers.
const SERIES_GROUPS = [
  {
    name: "Energy and Materials",
    series: ["Energy", "Mining and Material"],
  },
  {
    name: "Industrials, Aerospace and Transport",
    series: ["Industrial", "Aerospace and Defense", "Transportation", "Automotive"],
  },
  {
    name: "Consumer and Retail",
    series: ["Consumer Staple", "Consumer Discretionary", "Luxury", "Retail", "Food and Beverage"],
  },
  {
    name: "Healthcare and Life Sciences",
    series: ["Healthcare", "Pharma and Biotech", "Medical Device"],
  },
  {
    name: "Technology and Communications",
    series: ["Technology", "Semiconductor", "Software", "Internet and Digital", "Telecommunications and Media"],
  },
  {
    name: "Financials and Real Assets",
    series: ["Financial", "Bank", "Insurance", "Asset Management", "Real Estate", "Utilities", "Infrastructure"],
  },
];

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function normalize(s) {
  return s.trim().toLowerCase().replace(/\s+/g, " ");
}

function formatDate(d) {
  return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

function encodePath(segments) {
  return segments.map(encodeURIComponent).join("/");
}

// Map every directory actually present under SERIES/, normalized name -> real name on disk.
const dirByNormalizedName = new Map();
if (fs.existsSync(SERIES_ROOT)) {
  const entries = fs.readdirSync(SERIES_ROOT, { withFileTypes: true }).filter((e) => e.isDirectory());
  for (const entry of entries) {
    dirByNormalizedName.set(normalize(entry.name), entry.name);
  }
}

const FILENAME_PATTERN = /^(\d{2})(\d{2})(\d{4})_(.+)$/i;

function readSeriesReports(actualDirName) {
  const dirPath = path.join(SERIES_ROOT, actualDirName);
  const files = fs.readdirSync(dirPath, { withFileTypes: true }).filter((e) => e.isFile() && /\.pdf$/i.test(e.name));

  const reports = files.map((f) => {
    const stem = f.name.replace(/\.pdf$/i, "");
    const match = stem.match(FILENAME_PATTERN);

    let date = null;
    let label;

    if (match) {
      const [, dd, mm, yyyy] = match;
      const candidate = new Date(Date.UTC(Number(yyyy), Number(mm) - 1, Number(dd)));
      if (!Number.isNaN(candidate.getTime())) date = candidate;
      label = match[4].replace(/[_-]+/g, " ").trim();
    } else {
      label = stem.replace(/[_-]+/g, " ").trim();
    }

    return {
      filename: f.name,
      label,
      dateIso: date ? date.toISOString().slice(0, 10) : null,
      dateLabel: date ? formatDate(date) : "Undated",
      href: encodePath(["SERIES", actualDirName, f.name]),
    };
  });

  reports.sort((a, b) => {
    if (a.dateIso && b.dateIso) return a.dateIso < b.dateIso ? 1 : -1;
    if (a.dateIso) return -1;
    if (b.dateIso) return 1;
    return a.label.localeCompare(b.label);
  });

  return reports;
}

const groups = SERIES_GROUPS.map((group) => ({
  name: group.name,
  series: group.series.map((seriesName) => {
    const actualDirName = dirByNormalizedName.get(normalize(seriesName));
    return {
      name: seriesName,
      reports: actualDirName ? readSeriesReports(actualDirName) : [],
    };
  }),
}));

const allSeries = groups.flatMap((g) => g.series);
const totalReports = allSeries.reduce((sum, s) => sum + s.reports.length, 0);
const seriesActiveCount = allSeries.filter((s) => s.reports.length > 0).length;

let latest = null;
for (const s of allSeries) {
  for (const r of s.reports) {
    if (r.dateIso && (!latest || r.dateIso > latest.dateIso)) {
      latest = { ...r, series: s.name };
    }
  }
}

const manifest = {
  generatedAt: new Date().toISOString(),
  totalReports,
  seriesActive: seriesActiveCount,
  seriesTotal: allSeries.length,
  lastUpdatedLabel: latest ? latest.dateLabel : "No reports on file",
  latest,
  groups,
};

fs.writeFileSync(path.join(ROOT, "reports.json"), JSON.stringify(manifest, null, 2), "utf8");

console.log(`Built reports.json: ${totalReports} report(s) across ${seriesActiveCount} of ${allSeries.length} series.`);
