(function () {
  "use strict";

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function countLabel(n, singular, plural) {
    return `${n} ${n === 1 ? singular : plural}`;
  }

  function downloadName(r) {
    return `${r.label} - ${r.dateLabel}.pdf`.replace(/\s+/g, " ");
  }

  function loadManifest() {
    return fetch("reports.json", { cache: "no-store" }).then((res) => {
      if (!res.ok) throw new Error(`reports.json: HTTP ${res.status}`);
      return res.json();
    });
  }

  function renderLatestBlock(data) {
    if (!data.latest) {
      return '<div class="latest-card latest-card--empty"><p>No reports on file yet.</p></div>';
    }
    const r = data.latest;
    return [
      '<div class="latest-card">',
      `<p class="latest-series">${escapeHtml(r.series)}</p>`,
      `<h2 class="latest-title"><a href="${r.href}" target="_blank" rel="noopener noreferrer">${escapeHtml(r.label)}</a></h2>`,
      '<p class="latest-date">',
      escapeHtml(r.dateLabel),
      ' <span class="meta-sep">&middot;</span> ',
      `<a class="download-link" href="${r.href}" download="${escapeHtml(downloadName(r))}">Download</a>`,
      "</p>",
      "</div>",
    ].join("");
  }

  function initHome() {
    const metaEl = document.getElementById("masthead-meta");
    const latestEl = document.getElementById("latest-report");
    if (!metaEl && !latestEl) return;

    loadManifest()
      .then((data) => {
        if (metaEl) {
          metaEl.innerHTML = [
            `<span>Last Updated: ${escapeHtml(data.lastUpdatedLabel)}</span>`,
            '<span class="meta-sep">&middot;</span>',
            `<span>${countLabel(data.totalReports, "Report", "Reports")} on File</span>`,
            '<span class="meta-sep">&middot;</span>',
            `<span>${data.seriesActive} of ${data.seriesTotal} Series Active</span>`,
          ].join("");
        }
        if (latestEl) {
          latestEl.innerHTML = renderLatestBlock(data);
        }
      })
      .catch((err) => {
        if (latestEl) latestEl.innerHTML = '<div class="latest-card latest-card--empty"><p>Unable to load reports right now.</p></div>';
        console.error(err);
      });
  }

  function renderReportRow(r) {
    return [
      "<li>",
      `<a href="${r.href}" target="_blank" rel="noopener noreferrer">${escapeHtml(r.label)}</a>`,
      '<span class="report-date">',
      escapeHtml(r.dateLabel),
      ' <span class="meta-sep">&middot;</span> ',
      `<a class="download-link" href="${r.href}" download="${escapeHtml(downloadName(r))}">Download</a>`,
      "</span>",
      "</li>",
    ].join("");
  }

  function renderSeriesEntry(s) {
    const hasReports = s.reports.length > 0;
    const countText = hasReports ? countLabel(s.reports.length, "Report", "Reports") : "Awaiting First Report";

    if (!hasReports) {
      return [
        `<div class="series-entry series-entry--empty" data-series="${escapeHtml(s.name.toLowerCase())}">`,
        `<span class="series-name">${escapeHtml(s.name)}</span>`,
        '<span class="series-fill" aria-hidden="true"></span>',
        `<span class="series-count">${countText}</span>`,
        "</div>",
      ].join("");
    }

    const searchBlob = escapeHtml(
      [s.name, ...s.reports.map((r) => r.label)].join(" ").toLowerCase()
    );

    return [
      `<details class="series-entry" data-series="${escapeHtml(s.name.toLowerCase())}" data-search="${searchBlob}">`,
      "<summary>",
      `<span class="series-name">${escapeHtml(s.name)}</span>`,
      '<span class="series-fill" aria-hidden="true"></span>',
      `<span class="series-count">${countText}</span>`,
      "</summary>",
      '<ul class="report-list">',
      s.reports.map(renderReportRow).join(""),
      "</ul>",
      "</details>",
    ].join("");
  }

  function renderGroups(groups) {
    return groups
      .map((group) => {
        return [
          '<div class="category">',
          `<h3 class="category-title">${escapeHtml(group.name)}</h3>`,
          group.series.map(renderSeriesEntry).join(""),
          "</div>",
        ].join("");
      })
      .join("");
  }

  function initArchive() {
    const container = document.getElementById("archive-groups");
    if (!container) return;

    const searchInput = document.getElementById("archive-search");
    const emptyState = document.getElementById("archive-empty");

    loadManifest()
      .then((data) => {
        container.innerHTML = renderGroups(data.groups);
        if (searchInput) {
          searchInput.disabled = false;
          searchInput.addEventListener("input", () => applyFilter(container, emptyState, searchInput.value));
        }
      })
      .catch((err) => {
        container.innerHTML = "<p>Unable to load the archive right now. Please try again shortly.</p>";
        console.error(err);
      });
  }

  function applyFilter(container, emptyState, rawQuery) {
    const query = rawQuery.trim().toLowerCase();
    let anyVisible = false;

    container.querySelectorAll(".category").forEach((category) => {
      let categoryHasVisible = false;

      category.querySelectorAll(".series-entry").forEach((entry) => {
        let visible = true;
        if (query) {
          const haystack = entry.dataset.search || entry.dataset.series || "";
          visible = haystack.includes(query);
        }
        entry.style.display = visible ? "" : "none";
        if (visible) categoryHasVisible = true;
        if (visible && query && entry.tagName === "DETAILS") {
          entry.open = true;
        } else if (!query && entry.tagName === "DETAILS") {
          entry.open = false;
        }
      });

      category.style.display = categoryHasVisible ? "" : "none";
      if (categoryHasVisible) anyVisible = true;
    });

    if (emptyState) emptyState.hidden = anyVisible || !query;
  }

  document.addEventListener("DOMContentLoaded", () => {
    initHome();
    initArchive();
  });
})();
