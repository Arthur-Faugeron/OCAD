#!/usr/bin/env node
"use strict";

/*
 * Regenerates index.html from the series folders on disk.
 *
 * Usage:  node scripts/build.js
 *
 * Run this after adding a new report PDF, then commit and push.
 * No dependencies beyond Node's built-in fs/path modules, on purpose,
 * so this keeps working with no maintenance for years.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");

// Canonical series list, exact spelling as used in CLAUDE.md / on report covers.
const SERIES_GROUPS = [
  {
    name: "Energy & Materials",
    series: ["Energy", "Mining & Material"],
  },
  {
    name: "Industrials, Aerospace & Transport",
    series: ["Industrial", "Aerospace & Defense", "Transportation", "Automotive"],
  },
  {
    name: "Consumer & Retail",
    series: ["Consumer Staple", "Consumer Discretionary", "Luxury", "Retail", "Food & Beverage"],
  },
  {
    name: "Healthcare & Life Sciences",
    series: ["Healthcare", "Pharma & Biotech", "Medical Device"],
  },
  {
    name: "Technology & Communications",
    series: ["Technology", "Semiconductor", "Software", "Internet & Digital", "Telecommunications & Media"],
  },
  {
    name: "Financials & Real Assets",
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

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function encodePath(segments) {
  return segments.map(encodeURIComponent).join("/");
}

// Map every directory actually present at repo root, normalized name -> real name on disk.
const rootEntries = fs.readdirSync(ROOT, { withFileTypes: true }).filter((e) => e.isDirectory());
const dirByNormalizedName = new Map();
for (const entry of rootEntries) {
  dirByNormalizedName.set(normalize(entry.name), entry.name);
}

const FILENAME_PATTERN = /^(\d{2})(\d{2})(\d{4})_(.+)$/i;

function readSeriesReports(actualDirName) {
  const dirPath = path.join(ROOT, actualDirName);
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
      date,
      href: encodePath([actualDirName, f.name]),
    };
  });

  reports.sort((a, b) => {
    if (a.date && b.date) return b.date - a.date;
    if (a.date) return -1;
    if (b.date) return 1;
    return a.label.localeCompare(b.label);
  });

  return reports;
}

const allSeries = [];
for (const group of SERIES_GROUPS) {
  for (const seriesName of group.series) {
    const actualDirName = dirByNormalizedName.get(normalize(seriesName));
    const reports = actualDirName ? readSeriesReports(actualDirName) : [];
    allSeries.push({ name: seriesName, group: group.name, reports });
  }
}

const totalReports = allSeries.reduce((sum, s) => sum + s.reports.length, 0);
const seriesActiveCount = allSeries.filter((s) => s.reports.length > 0).length;

let latest = null;
for (const s of allSeries) {
  for (const r of s.reports) {
    if (r.date && (!latest || r.date > latest.report.date)) {
      latest = { series: s, report: r };
    }
  }
}

// --- Render ---

function renderLatestBlock() {
  if (!latest) {
    return [
      '    <div class="latest-card latest-card--empty">',
      "      <p>No reports on file yet.</p>",
      "    </div>",
    ].join("\n");
  }
  const { series, report } = latest;
  return [
    '    <div class="latest-card">',
    `      <p class="latest-series">${escapeHtml(series.name)}</p>`,
    `      <h2 class="latest-title"><a href="${report.href}">${escapeHtml(report.label)}</a></h2>`,
    `      <p class="latest-date">${report.date ? formatDate(report.date) : "Undated"}</p>`,
    "    </div>",
  ].join("\n");
}

function renderReportRow(r) {
  const dateLabel = r.date ? formatDate(r.date) : "Undated";
  return [
    "        <li>",
    `          <a href="${r.href}">${escapeHtml(r.label)}</a>`,
    `          <span class="report-date">${dateLabel}</span>`,
    "        </li>",
  ].join("\n");
}

function renderSeriesEntry(s) {
  const hasReports = s.reports.length > 0;
  const countLabel = hasReports ? `${s.reports.length} ${s.reports.length === 1 ? "Report" : "Reports"}` : "Awaiting First Report";

  if (!hasReports) {
    return [
      '      <div class="series-entry series-entry--empty">',
      '        <span class="series-name">' + escapeHtml(s.name) + "</span>",
      '        <span class="series-fill" aria-hidden="true"></span>',
      `        <span class="series-count">${countLabel}</span>`,
      "      </div>",
    ].join("\n");
  }

  return [
    '      <details class="series-entry">',
    "        <summary>",
    '          <span class="series-name">' + escapeHtml(s.name) + "</span>",
    '          <span class="series-fill" aria-hidden="true"></span>',
    `          <span class="series-count">${countLabel}</span>`,
    "        </summary>",
    '        <ul class="report-list">',
    s.reports.map(renderReportRow).join("\n"),
    "        </ul>",
    "      </details>",
  ].join("\n");
}

function renderCoverageIndex() {
  const blocks = [];
  for (const group of SERIES_GROUPS) {
    const seriesInGroup = allSeries.filter((s) => s.group === group.name);
    blocks.push(
      [
        '    <div class="category">',
        `      <h3 class="category-title">${escapeHtml(group.name)}</h3>`,
        seriesInGroup.map(renderSeriesEntry).join("\n"),
        "    </div>",
      ].join("\n")
    );
  }
  return blocks.join("\n");
}

const template = fs.readFileSync(path.join(__dirname, "template.html"), "utf8");

const output = template
  .replace("{{LAST_UPDATED}}", latest ? formatDate(latest.report.date) : "No reports on file")
  .replace("{{TOTAL_REPORTS_LABEL}}", `${totalReports} ${totalReports === 1 ? "Report" : "Reports"} on File`)
  .replace("{{SERIES_ACTIVE_LABEL}}", `${seriesActiveCount} of ${allSeries.length} Series Active`)
  .replace("{{LATEST_REPORT_BLOCK}}", renderLatestBlock())
  .replace("{{COVERAGE_INDEX}}", renderCoverageIndex());

fs.writeFileSync(path.join(ROOT, "index.html"), output, "utf8");

console.log(`Built index.html: ${totalReports} report(s) across ${seriesActiveCount} of ${allSeries.length} series.`);
