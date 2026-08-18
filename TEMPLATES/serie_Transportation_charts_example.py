#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCAD chart build script for LATAM Airlines Group S.A. (NYSE: LTM)
Figures sourced from Alpha Vantage fundamentals API (SEC-taxonomy-normalized filings data),
LATAM Airlines Group 4Q25 earnings release (ir.latam.com, 3 Feb 2026), and StockAnalysis.com
(S&P Global Market Intelligence), as documented in the report Sources & Methodology section.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

OUT = "/sessions/focused-sleepy-cray/mnt/outputs/latam"
CH = os.path.join(OUT, "charts")
os.makedirs(CH, exist_ok=True)

IVORY, NAVY, BROWN, OLIVE, CAMEL, GRID = "#F5F1E8","#172A3A","#6B5744","#3F4A32","#C8AE82","#D9D2C2"

plt.rcParams.update({
    "font.family": "Liberation Serif", "text.color": NAVY, "axes.edgecolor": NAVY,
    "axes.labelcolor": NAVY, "xtick.color": NAVY, "ytick.color": NAVY,
    "axes.facecolor": IVORY, "figure.facecolor": IVORY, "savefig.facecolor": IVORY,
    "font.size": 11,
})

def style_ax(ax, ygrid=True):
    ax.set_facecolor(IVORY)
    for s in ["top","right"]:
        ax.spines[s].set_visible(False)
    for s in ["left","bottom"]:
        ax.spines[s].set_color(NAVY); ax.spines[s].set_linewidth(0.8)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, color=NAVY)

years = [2021,2022,2023,2024,2025]
revenue   = [4884.0, 9362.5, 11640.5, 12833.0, 14265.1]
gp        = [-79.5, 1259.0, 2824.0, 3267.1, 4160.2]
opinc     = [-3425.8, 1211.6, 1078.2, 1541.0, 2335.5]
ebitda    = [-2347.4, 3223.1, 2277.7, 2614.3, 3278.0]
netinc    = [-4647.5, 1339.2, 581.8, 977.0, 1460.0]
ocf       = [-184.1, 96.8, 2263.6, 3106.3, 3260.3]
capex     = [675.8, 830.7, 795.8, 1419.9, 1773.0]
fcf       = [o-c for o,c in zip(ocf,capex)]
totdebt   = [10540.1, 6865.6, 7037.0, 7150.5, 8088.5]
cash      = [1046.8, 1216.7, 1714.8, 1957.8, 2150.1]
netdebt   = [d-c for d,c in zip(totdebt,cash)]
equity    = [-7056.5, 42.3, 450.3, 723.3, 1345.6]

rev_growth = [None]+[ (revenue[i]-revenue[i-1])/revenue[i-1]*100 for i in range(1,len(revenue))]

# ============ 1. Revenue & growth ============
fig, ax1 = plt.subplots(figsize=(9.4,4.6), dpi=200)
bars = ax1.bar([str(y) for y in years], revenue, color=NAVY, width=0.55, zorder=3)
style_ax(ax1); ax1.set_ylabel("Total revenue (US$ millions)")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:,.0f}"))
for b,v in zip(bars, revenue):
    ax1.text(b.get_x()+b.get_width()/2, v+250, f"{v:,.0f}", ha="center", va="bottom", fontsize=9, color=NAVY)
ax2 = ax1.twinx()
ax2.plot([str(y) for y in years], rev_growth, color=CAMEL, marker="o", markersize=5, linewidth=2.0,
         zorder=4, markerfacecolor=CAMEL, markeredgecolor=NAVY, markeredgewidth=0.6)
ax2.set_ylabel("YoY revenue growth (%)"); ax2.spines["top"].set_visible(False)
for i,(y,g) in enumerate(zip(years, rev_growth)):
    if g is not None:
        ax2.annotate(f"{g:+.0f}%", (i,g), textcoords="offset points", xytext=(0,10), ha="center", fontsize=8.5, color=BROWN)
fig.suptitle("LATAM Airlines Group — Revenue and Year-on-Year Growth, FY2021–FY2025", fontsize=12, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.03, "Source: Alpha Vantage (SEC-taxonomy-normalized filings data). Revenue per audited financial statements; excludes management's headline"
                     " “total operating revenues” figure, which nets in other operating income.", ha="center", fontsize=7.3, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"01_revenue_growth.png"), bbox_inches="tight"); plt.close(fig)

# ============ 2. Margins ============
gm=[g/r*100 for g,r in zip(gp,revenue)]; om=[o/r*100 for o,r in zip(opinc,revenue)]; nm=[n/r*100 for n,r in zip(netinc,revenue)]
fig, ax = plt.subplots(figsize=(9.4,4.6), dpi=200)
x=np.arange(len(years))
ax.plot(x, gm, color=NAVY, marker="s", markersize=5, linewidth=2.0, label="Gross margin")
ax.plot(x, om, color=OLIVE, marker="o", markersize=5, linewidth=2.0, label="Operating margin")
ax.plot(x, nm, color=BROWN, marker="^", markersize=5, linewidth=2.0, label="Net margin")
ax.axhline(0, color=GRID, linewidth=1.0)
style_ax(ax); ax.set_xticks(x); ax.set_xticklabels([str(y) for y in years]); ax.set_ylabel("Margin (%)")
ax.legend(frameon=False, loc="lower right", fontsize=8.5)
fig.suptitle("LATAM Airlines Group — Profitability Margins, FY2021–FY2025", fontsize=12, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.03, "Source: Alpha Vantage (SEC-taxonomy-normalized filings data). Analyst calculation: margin = line item / total revenue.",
          ha="center", fontsize=7.3, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"02_margins.png"), bbox_inches="tight"); plt.close(fig)

# ============ 3. OCF / Capex / FCF ============
fig, ax = plt.subplots(figsize=(9.4,4.6), dpi=200)
w=0.32
ax.bar(x-w/2, ocf, width=w, color=NAVY, label="Operating cash flow", zorder=3)
ax.bar(x+w/2, [-c for c in capex], width=w, color=CAMEL, label="Capital expenditure (outflow)", zorder=3)
ax.plot(x, fcf, color=BROWN, marker="D", markersize=5.5, linewidth=2.0, label="Free cash flow", zorder=4)
ax.axhline(0, color=NAVY, linewidth=0.8)
style_ax(ax); ax.set_xticks(x); ax.set_xticklabels([str(y) for y in years]); ax.set_ylabel("US$ millions")
ax.legend(frameon=False, loc="upper left", fontsize=8)
fig.suptitle("LATAM Airlines Group — Operating Cash Flow, Capex and Free Cash Flow, FY2021–FY2025", fontsize=11.6, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.03, "Source: Alpha Vantage (SEC-taxonomy-normalized filings data). FCF = operating cash flow − capital expenditure (analyst calculation).",
          ha="center", fontsize=7.3, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"03_fcf.png"), bbox_inches="tight"); plt.close(fig)

# ============ 4. Net debt & leverage ============
ndebt_ebitda = [nd/e if e>0 else None for nd,e in zip(netdebt, ebitda)]
fig, ax1 = plt.subplots(figsize=(9.4,4.6), dpi=200)
bars = ax1.bar([str(y) for y in years], netdebt, color=NAVY, width=0.5, zorder=3)
style_ax(ax1); ax1.set_ylabel("Net debt (US$ millions)")
for b,v in zip(bars, netdebt):
    ax1.text(b.get_x()+b.get_width()/2, v+120, f"{v:,.0f}", ha="center", va="bottom", fontsize=9, color=NAVY)
ax2=ax1.twinx()
ax2.plot([str(y) for y in years], ndebt_ebitda, color=CAMEL, marker="o", markersize=5, linewidth=2.0, markeredgecolor=NAVY, markeredgewidth=0.6)
ax2.set_ylabel("Net debt / EBITDA (x)"); ax2.spines["top"].set_visible(False)
for i,(y,v) in enumerate(zip(years, ndebt_ebitda)):
    if v is not None:
        ax2.annotate(f"{v:.1f}x", (i,v), textcoords="offset points", xytext=(0,9), ha="center", fontsize=8.5, color=BROWN)
fig.suptitle("LATAM Airlines Group — Net Debt and Leverage, FY2021–FY2025", fontsize=12, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.03, "Source: Alpha Vantage (SEC-taxonomy-normalized filings data). Net debt = total debt (incl. finance-lease liabilities) − cash;"
                     " leverage uses AV-derived EBITDA. LATAM's own ‘adjusted net leverage’ (1.5x FY25, per 4Q25 release) uses a"
                     " rent-adjusted EBITDAR denominator and is not directly comparable — see Section C1.",
          ha="center", fontsize=7.1, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"04_netdebt.png"), bbox_inches="tight"); plt.close(fig)

# ============ 5. ROE / ROIC (approx) ============
roe = []
for i in range(len(years)):
    e = equity[i]
    roe.append(netinc[i]/e*100 if e and e>50 else None)
taxrate = 0.27
nopat = [o*(1-taxrate) for o in opinc]
invested_capital = [d+e for d,e in zip(totdebt, equity)]
roic = [n/ic*100 if ic>0 else None for n,ic in zip(nopat, invested_capital)]
fig, ax = plt.subplots(figsize=(9.4,4.6), dpi=200)
ax.plot(x, roic, color=OLIVE, marker="o", markersize=5.5, linewidth=2.0, label="ROIC (analyst estimate)")
roe_x = [xi for xi,v in zip(x,roe) if v is not None]; roe_y=[v for v in roe if v is not None]
ax.plot(roe_x, roe_y, color=BROWN, marker="^", markersize=5.5, linewidth=2.0, linestyle="--", label="ROE (reported equity basis)")
ax.axhline(0, color=GRID, linewidth=1.0)
style_ax(ax); ax.set_xticks(x); ax.set_xticklabels([str(y) for y in years]); ax.set_ylabel("Percent (%)")
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
fig.suptitle("LATAM Airlines Group — ROIC and ROE, FY2021–FY2025", fontsize=12.2, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.05, "Source: analyst calculation from Alpha Vantage data. ROIC = NOPAT (EBIT × (1−27% assumed statutory tax)) / (total debt + equity).\n"
                     "ROE distorted through 2022 by fresh-start/negative-equity accounting following the Nov-2022 Chapter 11 exit; shown only where equity is not near-zero/negative.",
          ha="center", fontsize=7.1, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"05_roic_roe.png"), bbox_inches="tight"); plt.close(fig)

# ============ 6. Price chart (5yr, from weekly series) ============
import re, json as _json, datetime
F = "/sessions/focused-sleepy-cray/mnt/.claude/projects/C--Users-fauge-AppData-Roaming-Claude-local-agent-mode-sessions-9ebf666e-4a57-4607-9edd-d17a2cf7f325-96e3af48-7d10-4136-8b59-c57eb2526745-local-0d933393-5d5b-4c77-b34d-49e057198468-outputs/30277eb5-8fe2-497e-9fa7-fc9835f20dac/tool-results/mcp-1ff3a3bb-0ce9-4997-be2f-a945b1516665-TIME_SERIES_WEEKLY_ADJUSTED-1787050231891.txt"
raw = open(F).read()
start = raw.find('{')
d = _json.loads(raw[start:])
csv = d['result']
lines = csv.strip().split('\n')
rows = [l.split(',') for l in lines[1:]]
dates = [r[0] for r in rows][::-1]
closes = [float(r[4]) for r in rows][::-1]
dts = [datetime.datetime.strptime(dd,"%Y-%m-%d") for dd in dates]
cutoff = dts[-1]-datetime.timedelta(days=5*365)
idx0 = next(i for i,dd in enumerate(dts) if dd>=cutoff)
dts5, cl5 = dts[idx0:], closes[idx0:]
ma50 = np.convolve(cl5, np.ones(10)/10, mode='same')
fig, ax = plt.subplots(figsize=(9.4,4.2), dpi=200)
ax.plot(dts5, cl5, color=NAVY, linewidth=1.4, label="LTM close (weekly)")
ax.plot(dts5, ma50, color=CAMEL, linewidth=1.6, label="10-week moving average")
style_ax(ax); ax.set_ylabel("Price (US$)")
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
fig.suptitle("LATAM Airlines Group (NYSE: LTM) — Share Price, 5-Year", fontsize=12.4, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.04, "Source: Alpha Vantage TIME_SERIES_WEEKLY_ADJUSTED, weekly closes; chart built by analyst (not a broker/exchange screenshot). Data through 17 Aug 2026.",
          ha="center", fontsize=7.3, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"06_price_5y.png"), bbox_inches="tight"); plt.close(fig)

# ============ 6b. cover chart: 1-year ============
cutoff1 = dts[-1]-datetime.timedelta(days=370)
idx1 = next(i for i,dd in enumerate(dts) if dd>=cutoff1)
dts1, cl1 = dts[idx1:], closes[idx1:]
fig, ax = plt.subplots(figsize=(8.6,2.6), dpi=200)
ax.plot(dts1, cl1, color=NAVY, linewidth=1.6)
ax.fill_between(dts1, cl1, min(cl1)*0.97, color=CAMEL, alpha=0.28)
style_ax(ax, ygrid=True)
ax.set_ylabel("US$", fontsize=8.5)
fig.text(0.01, 0.02, "LTM (NYSE) — weekly close, trailing 12 months to 17 Aug 2026. Source: Alpha Vantage.", fontsize=6.8, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"07_cover_1y.png"), bbox_inches="tight"); plt.close(fig)

# ============ 8. Peer comparison bars (EV/EBITDA, Op margin) ============
peers = ["LATAM\n(LTM)","Copa Holdings\n(CPA)","Azul\n(AZUL)"]
ev_ebitda = [9.39, 9.03, 22.42]
op_margin = [5.3, 8.65, 27.5]
fig, axs = plt.subplots(1,2, figsize=(9.4,4.0), dpi=200)
axs[0].bar(peers, ev_ebitda, color=[NAVY,OLIVE,CAMEL], width=0.55, zorder=3)
style_ax(axs[0]); axs[0].set_ylabel("EV / EBITDA (x, TTM)")
for i,v in enumerate(ev_ebitda): axs[0].text(i, v+0.2, f"{v:.1f}x", ha="center", fontsize=9, color=NAVY)
axs[1].bar(peers, op_margin, color=[NAVY,OLIVE,CAMEL], width=0.55, zorder=3)
style_ax(axs[1]); axs[1].set_ylabel("Operating margin (%, TTM)")
for i,v in enumerate(op_margin): axs[1].text(i, v+0.5, f"{v:.1f}%", ha="center", fontsize=9, color=NAVY)
fig.suptitle("Peer Comparison — Valuation and Profitability (TTM)", fontsize=12.2, color=NAVY, x=0.5, y=1.03, fontweight="bold")
fig.text(0.5, -0.05, "Source: Alpha Vantage COMPANY_OVERVIEW, trailing twelve months, retrieved 18 Aug 2026. Azul's TTM operating margin/EV-EBITDA reflect\n"
                     "a company under BRL devaluation and restructuring stress; net income and book value are negative — see Section A4/C3 for peer-selection rationale.",
          ha="center", fontsize=7.0, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"08_peers.png"), bbox_inches="tight"); plt.close(fig)

# ============ 9. Ownership / control-pact pie ============
labels = ["Banco de Chile o/b/o\nState Street (Cueto bloc)","Delta Air Lines","Qatar Airways","Other shareholders\n& free float"]
sizes = [15.83, 10.57, 10.56, 100-15.83-10.57-10.56]
fig, ax = plt.subplots(figsize=(6.4,4.6), dpi=200)
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct=lambda p: f"{p:.1f}%",
       colors=[NAVY, OLIVE, BROWN, CAMEL], startangle=90, pctdistance=0.75,
       wedgeprops=dict(edgecolor=IVORY, linewidth=1.2))
for at in autotexts: at.set_color(IVORY); at.set_fontsize(8.5)
ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1.0,0.5), frameon=False, fontsize=8)
fig.suptitle("LATAM Airlines Group — Principal Shareholders (Q1 2026)", fontsize=11.6, color=NAVY, y=1.02, fontweight="bold")
fig.text(0.5,-0.02, "Source: LATAM Airlines Group 20-F FY2025 / ownership disclosures (SEC EDGAR), as of 31 Mar 2026. Cueto family, Delta and Qatar Airways\nact under a joint shareholder pact governing board composition and key strategic decisions.",
          ha="center", fontsize=6.9, color=BROWN)
fig.tight_layout(); fig.savefig(os.path.join(CH,"09_ownership.png"), bbox_inches="tight"); plt.close(fig)

print("charts done:", os.listdir(CH))
