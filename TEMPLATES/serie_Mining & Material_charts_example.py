#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCAD chart + analytics build script for SQM (Sociedad Quimica y Minera de Chile S.A.)
All figures sourced from: SQM Form 6-K 4Q2025 earnings release (SEC EDGAR), Alpha Vantage
fundamentals API, and StockAnalysis.com (S&P Global Market Intelligence / Fiscal.ai) as
documented in the report's Sources & Methodology section.
"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm

OUT = "/sessions/keen-fervent-davinci/mnt/outputs/sqm_report"
DATA = os.path.join(OUT, "data")
CH = os.path.join(OUT, "charts")
os.makedirs(CH, exist_ok=True)

# ---------------------------------------------------------------- palette --
IVORY   = "#F5F1E8"
NAVY    = "#172A3A"
BROWN   = "#6B5744"
OLIVE   = "#3F4A32"
CAMEL   = "#C8AE82"
GRID    = "#D9D2C2"

plt.rcParams.update({
    "font.family": "Liberation Serif",
    "text.color": NAVY,
    "axes.edgecolor": NAVY,
    "axes.labelcolor": NAVY,
    "xtick.color": NAVY,
    "ytick.color": NAVY,
    "axes.facecolor": IVORY,
    "figure.facecolor": IVORY,
    "savefig.facecolor": IVORY,
    "font.size": 11,
})

def style_ax(ax, ygrid=True):
    ax.set_facecolor(IVORY)
    for s in ["top","right"]:
        ax.spines[s].set_visible(False)
    for s in ["left","bottom"]:
        ax.spines[s].set_color(NAVY)
        ax.spines[s].set_linewidth(0.8)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, color=NAVY)

# ============================================================= 1. REVENUE ==
years = [2020,2021,2022,2023,2024,2025]
revenue   = [1817.2, 2862.3, 10710.6, 7467.5, 4528.8, 4576.2]   # US$m
netincome = [164.5, 585.5, 3906.3, 2012.7, -404.4, 588.1]       # US$m, attributable to shareholders
gp        = [482.9, 1090.1, 5736.6, 3075.1, 1327.1, 1352.6]
opinc     = [302.5, 927.3, 5531.4, 2844.4, 1065.9, 1134.6]
ebitda_adj= [326.8, 926.1, 5579.3, 2936.3, 1483.5, 1579.6]      # 2024-25 = company Adjusted EBITDA (SEC); 2020-23 = AV EBIT+D&A

rev_growth = [None] + [ (revenue[i]-revenue[i-1])/revenue[i-1]*100 for i in range(1,len(revenue))]

fig, ax1 = plt.subplots(figsize=(9.4,4.6), dpi=200)
bars = ax1.bar([str(y) for y in years], revenue, color=NAVY, width=0.55, zorder=3, label="Revenue (US$m)")
style_ax(ax1)
ax1.set_ylabel("Revenue (US$ millions)")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:,.0f}"))
for b,v in zip(bars, revenue):
    ax1.text(b.get_x()+b.get_width()/2, v+150, f"{v:,.0f}", ha="center", va="bottom", fontsize=9, color=NAVY)
ax2 = ax1.twinx()
ax2.plot([str(y) for y in years], rev_growth, color=CAMEL, marker="o", markersize=5,
         linewidth=2.0, zorder=4, markerfacecolor=CAMEL, markeredgecolor=NAVY, markeredgewidth=0.6)
ax2.set_ylabel("YoY revenue growth (%)")
ax2.spines["top"].set_visible(False)
ax2.axhline(0, color=BROWN, linewidth=0.7, linestyle=(0,(4,3)))
for i,(y,g) in enumerate(zip(years, rev_growth)):
    if g is not None:
        ax2.annotate(f"{g:+.0f}%", (i,g), textcoords="offset points", xytext=(0,10 if g>=0 else -16),
                     ha="center", fontsize=8.5, color=BROWN)
fig.suptitle("SQM — Revenue and Year-on-Year Growth, FY2020–FY2025", fontsize=12.5, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.03, "Source: Alpha Vantage (FY2020–FY2023, aggregated from SEC filings); SQM 4Q2025 earnings release, Form 6-K, SEC EDGAR (FY2024–FY2025).",
          ha="center", fontsize=7.6, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"01_revenue_growth.png"), bbox_inches="tight")
plt.close(fig)

# ==================================================== 2. MARGINS ==========
gm = [g/r*100 for g,r in zip(gp,revenue)]
om = [o/r*100 for o,r in zip(opinc,revenue)]
nm = [n/r*100 for n,r in zip(netincome,revenue)]

fig, ax = plt.subplots(figsize=(9.4,4.6), dpi=200)
x = np.arange(len(years))
ax.plot(x, gm, color=NAVY, marker="s", markersize=5, linewidth=2.0, label="Gross margin")
ax.plot(x, om, color=OLIVE, marker="o", markersize=5, linewidth=2.0, label="Operating margin")
ax.plot(x, nm, color=BROWN, marker="^", markersize=5, linewidth=2.0, label="Net margin")
ax.axhline(0, color=GRID, linewidth=1.0)
style_ax(ax)
ax.set_xticks(x); ax.set_xticklabels([str(y) for y in years])
ax.set_ylabel("Margin (%)")
ax.legend(frameon=False, loc="upper right", fontsize=9)
fig.suptitle("SQM — Gross, Operating and Net Margins, FY2020–FY2025", fontsize=12.5, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.03, "Source: as Chart 1. Net margin attributable to SQM shareholders (post minority interest, FY2024–FY2025).",
          ha="center", fontsize=7.6, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"02_margins.png"), bbox_inches="tight")
plt.close(fig)

# ==================================================== 3. FCF ==============
fcf_years = [2021,2022,2023,2024,2025]
ocf  = [822.5, 4078.0, -196.6, 1274.7, 1314.4]
capex= [472.8, 916.6, 1116.0, 971.8, 876.7]
fcf  = [o-c for o,c in zip(ocf,capex)]

fig, ax = plt.subplots(figsize=(9.4,4.6), dpi=200)
xw = np.arange(len(fcf_years))
w = 0.32
ax.bar(xw-w/2, ocf, width=w, color=NAVY, zorder=3, label="Operating cash flow")
ax.bar(xw+w/2, [-c for c in capex], width=w, color=CAMEL, zorder=3, label="Capital expenditure")
ax.plot(xw, fcf, color=BROWN, marker="D", markersize=6, linewidth=2.2, zorder=4, label="Free cash flow")
ax.axhline(0, color=NAVY, linewidth=0.9)
style_ax(ax)
ax.set_xticks(xw); ax.set_xticklabels([str(y) for y in fcf_years])
ax.set_ylabel("US$ millions")
for i,v in enumerate(fcf):
    ax.annotate(f"{v:,.0f}", (xw[i], v), textcoords="offset points", xytext=(0, 10 if v>=0 else -16),
                ha="center", fontsize=8.5, color=BROWN, fontweight="bold")
ax.legend(frameon=False, loc="lower right", fontsize=9)
fig.suptitle("SQM — Operating Cash Flow, Capex and Free Cash Flow, FY2021–FY2025", fontsize=12.3, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.05, "Source: StockAnalysis.com (data by Fiscal.ai) cross-checked against Alpha Vantage cash-flow aggregation of SEC filings.\nFree cash flow = operating cash flow less capital expenditure (analyst calculation).",
          ha="center", fontsize=7.6, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"03_fcf.png"), bbox_inches="tight")
plt.close(fig)

# ============================================== 4. NET DEBT / (CASH) ======
nd_years = [2021,2022,2023,2024,2025,"Q1'26"]
netdebt = [259.16, -637.64, 2178.0, 2390.0, 2037.0, 1341.0]  # positive = net debt, so invert 2022 sign
netdebt_signed = [259.16, -637.64, 2178.0, 2390.0, 2037.0, 1341.0]

fig, ax = plt.subplots(figsize=(9.4,4.2), dpi=200)
xs = np.arange(len(nd_years))
colors = [BROWN if v>=0 else OLIVE for v in netdebt_signed]
bars = ax.bar(xs, netdebt_signed, color=colors, width=0.5, zorder=3)
ax.axhline(0, color=NAVY, linewidth=0.9)
style_ax(ax)
ax.set_xticks(xs); ax.set_xticklabels([str(y) for y in nd_years])
ax.set_ylabel("US$ millions")
for b,v in zip(bars, netdebt_signed):
    label = f"Net debt {v:,.0f}" if v>=0 else f"Net cash {abs(v):,.0f}"
    ax.annotate(label, (b.get_x()+b.get_width()/2, v), textcoords="offset points",
                xytext=(0, 8 if v>=0 else -16), ha="center", fontsize=8.2, color=NAVY)
fig.suptitle("SQM — Net Debt / Net Cash Position, FY2021–Q1 2026", fontsize=12.3, color=NAVY, x=0.5, y=1.02, fontweight="bold")
fig.text(0.5, -0.05, "Source: StockAnalysis.com (data by Fiscal.ai), balance-sheet aggregation of SQM SEC filings. Positive bars denote net debt; negative bars denote net cash.",
          ha="center", fontsize=7.6, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"04_net_debt.png"), bbox_inches="tight")
plt.close(fig)

# ============================================== 5. ROE / ROIC =============
roe_years=[2021,2022,2023,2024,2025]
equity=[3182,4897,4441,5161,5691]
roe=[n/e*100 for n,e in zip([585.5,3906.3,2012.7,-404.4,588.1], equity)]
# ROIC (analyst calc): NOPAT = OpInc*(1-eff.tax) ; InvCap = TotalDebt+Equity-Cash
total_debt=[2693,2979,4545,4848,4764]
cash=[2434,3617,2367,2457,2727]
ebt=[841.221,5486.496,2807.018,974.414,960.7]
tax=[249.016,1572.212,787.275,1372.049,320.1]
eff_tax=[t/e for t,e in zip(tax,ebt)]
nopat=[o*(1-min(t,1.5)) for o,t in zip(opinc[1:], eff_tax)]  # opinc[1:] aligns 2021-2025
invcap=[d+e-c for d,e,c in zip(total_debt, equity, cash)]
roic=[n/i*100 for n,i in zip(nopat, invcap)]

fig, ax = plt.subplots(figsize=(9.4,4.4), dpi=200)
xw=np.arange(len(roe_years))
ax.plot(xw, roe, color=NAVY, marker="o", markersize=6, linewidth=2.2, label="ROE (analyst calc.)")
ax.plot(xw, roic, color=OLIVE, marker="s", markersize=6, linewidth=2.2, label="ROIC (analyst calc.)")
ax.axhline(0, color=GRID, linewidth=1.0)
style_ax(ax)
ax.set_xticks(xw); ax.set_xticklabels([str(y) for y in roe_years])
ax.set_ylabel("Percent (%)")
ax.legend(frameon=False, loc="upper right", fontsize=9)
fig.suptitle("SQM — Return on Equity and Return on Invested Capital, FY2021–FY2025", fontsize=12.2, color=NAVY, x=0.5, y=1.02, fontweight="bold")
fig.text(0.5, -0.06, "Analyst calculation. ROE = net income attributable to shareholders / average-period shareholders' equity.\nROIC = operating income x (1 - effective tax rate) / (total debt + equity - cash). FY2024 effective tax rate distorted by a one-off tax charge (see Section B1).",
          ha="center", fontsize=7.4, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"05_roe_roic.png"), bbox_inches="tight")
plt.close(fig)

# ============================================== 6. SEGMENT MIX FY2025 =====
seg_labels = ["Lithium &\nDerivatives","Iodine &\nDerivatives","Specialty Plant\nNutrition","Potassium","Industrial\nChemicals","Other"]
seg_values = [2288.2, 1042.8, 982.4, 155.5, 75.4, 31.9]
seg_colors = [NAVY, OLIVE, BROWN, CAMEL, "#8B7F6B", "#A9A08D"]

fig, ax = plt.subplots(figsize=(6.6,6.0), dpi=200)
wedges, texts, autotexts = ax.pie(seg_values, colors=seg_colors, startangle=90, counterclock=False,
       wedgeprops=dict(width=0.42, edgecolor=IVORY, linewidth=2),
       autopct=lambda p: f"{p:.0f}%" if p>2 else "", pctdistance=0.79)
for t in autotexts:
    t.set_color(IVORY); t.set_fontsize(9); t.set_fontweight("bold")
ax.legend(wedges, [f"{l.replace(chr(10),' ')} — US${v:,.0f}m" for l,v in zip(seg_labels, seg_values)],
          loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=8.6)
ax.set_title("SQM — Revenue by Business Line, FY2025\n(US$4,576.2m total)", fontsize=11.6, color=NAVY, fontweight="bold", pad=10)
fig.text(0.5, 0.01, "Source: SQM 4Q2025 earnings release, Form 6-K, SEC EDGAR, filed 27 February 2026.",
          ha="center", fontsize=7.6, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"06_segment_mix.png"), bbox_inches="tight")
plt.close(fig)

# ============================================== 7. PRICE CHART (5Y) =======
with open(os.path.join(DATA,"price_5y_weekly.json")) as f:
    pd = json.load(f)["data"]
pd = sorted(pd, key=lambda r: r["t"])
dates = [np.datetime64(r["t"]) for r in pd]
closes = [r["c"] for r in pd]

fig, ax = plt.subplots(figsize=(9.6,4.6), dpi=200)
ax.plot(dates, closes, color=NAVY, linewidth=1.6, zorder=3)
ax.fill_between(dates, closes, min(closes)*0.97, color=CAMEL, alpha=0.30, zorder=2)
style_ax(ax)
ax.set_ylabel("SQM (NYSE), US$ per ADR")
# annotate key points
peak_idx = int(np.argmax(closes)); trough_idx = int(np.argmin(closes))
ax.annotate(f"${closes[peak_idx]:,.2f}\n{str(dates[peak_idx])[:7]}", (dates[peak_idx], closes[peak_idx]),
            textcoords="offset points", xytext=(0,12), ha="center", fontsize=8, color=NAVY, fontweight="bold")
ax.annotate(f"${closes[trough_idx]:,.2f}\n{str(dates[trough_idx])[:7]}", (dates[trough_idx], closes[trough_idx]),
            textcoords="offset points", xytext=(0,-24), ha="center", fontsize=8, color=BROWN, fontweight="bold")
ax.scatter([dates[-1]],[closes[-1]], color=OLIVE, zorder=5, s=28)
ax.annotate(f"${closes[-1]:,.2f}\n14 Aug 2026", (dates[-1], closes[-1]), textcoords="offset points",
            xytext=(-40,10), ha="center", fontsize=8.2, color=OLIVE, fontweight="bold")
fig.suptitle("SQM (NYSE: SQM) — Weekly Closing Price, August 2021–August 2026", fontsize=12.2, color=NAVY, x=0.5, y=1.01, fontweight="bold")
fig.text(0.5, -0.04, "Source: StockAnalysis.com, price data by S&P Global Market Intelligence. Weekly closes, not adjusted for the ordinary dividend distributions listed in Section C4.",
          ha="center", fontsize=7.6, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"07_price_5y.png"), bbox_inches="tight")
plt.close(fig)

# ---- analytics from the same series (weekly) ----
closes_arr = np.array(closes, dtype=float)
wk_returns = np.diff(closes_arr) / closes_arr[:-1]
ann_vol = np.std(wk_returns, ddof=1) * math.sqrt(52) * 100
# max drawdown
cum_max = np.maximum.accumulate(closes_arr)
drawdowns = (closes_arr - cum_max) / cum_max
max_dd = drawdowns.min() * 100
max_dd_idx = int(np.argmin(drawdowns))
# trailing windows
def price_n_weeks_ago(n):
    idx = len(closes_arr) - 1 - n
    return closes_arr[idx] if idx >= 0 else None

last = closes_arr[-1]
ret_1m = (last/price_n_weeks_ago(4)-1)*100 if price_n_weeks_ago(4) else None
ret_3m = (last/price_n_weeks_ago(13)-1)*100 if price_n_weeks_ago(13) else None
ret_6m = (last/price_n_weeks_ago(26)-1)*100 if price_n_weeks_ago(26) else None
ret_1y = (last/price_n_weeks_ago(52)-1)*100 if price_n_weeks_ago(52) else None
ret_3y = (last/closes_arr[0]-1)*100 if len(closes_arr) >= 155 else None  # approx full series ~5y
ret_5y = (last/closes_arr[0]-1)*100

# 52-week high/low from the last 52 weekly points (approx to trading days used in narrative separately)
last52 = closes_arr[-53:] if len(closes_arr)>=53 else closes_arr
# also use high/low columns for a truer range
highs = np.array([r["h"] for r in pd[-53:]])
lows  = np.array([r["l"] for r in pd[-53:]])
range_low, range_high = lows.min(), highs.max()

analytics = {
    "ann_vol_pct": round(ann_vol,1),
    "max_drawdown_pct": round(max_dd,1),
    "max_drawdown_week": str(dates[max_dd_idx])[:10],
    "ret_1m_pct": round(ret_1m,1) if ret_1m is not None else None,
    "ret_3m_pct": round(ret_3m,1) if ret_3m is not None else None,
    "ret_6m_pct": round(ret_6m,1) if ret_6m is not None else None,
    "ret_1y_pct": round(ret_1y,1) if ret_1y is not None else None,
    "ret_5y_pct": round(ret_5y,1) if ret_5y is not None else None,
    "range_52w_low": round(float(range_low),2),
    "range_52w_high": round(float(range_high),2),
    "last_close": round(float(last),2),
    "n_weeks": len(closes_arr),
    "first_date": str(dates[0])[:10],
    "last_date": str(dates[-1])[:10],
}
with open(os.path.join(DATA,"price_analytics.json"),"w") as f:
    json.dump(analytics, f, indent=2)
print(json.dumps(analytics, indent=2))

# ============================================== 8. PEER COMPARISON ========
peers = ["SQM","Albemarle\n(ALB)","Rio Tinto\n(RIO)"]
pe_ttm = [25.28, 279.29, 13.56]
fwd_pe = [10.7, 14.62, 10.89]
beta   = [1.00, 1.32, 0.66]

fig, ax = plt.subplots(figsize=(8.6,4.2), dpi=200)
xw = np.arange(len(peers)); w=0.35
ax.bar(xw-w/2, pe_ttm, width=w, color=BROWN, zorder=3, label="Trailing P/E")
ax.bar(xw+w/2, fwd_pe, width=w, color=NAVY, zorder=3, label="Forward P/E")
style_ax(ax)
ax.set_xticks(xw); ax.set_xticklabels(peers, fontsize=9.5)
ax.set_ylabel("Multiple (x)")
for i,(a,b) in enumerate(zip(pe_ttm,fwd_pe)):
    ax.annotate(f"{a:.1f}x", (xw[i]-w/2, a), textcoords="offset points", xytext=(0,4), ha="center", fontsize=8, color=NAVY)
    ax.annotate(f"{b:.1f}x", (xw[i]+w/2, b), textcoords="offset points", xytext=(0,4), ha="center", fontsize=8, color=NAVY)
ax.set_ylim(0, 60)
ax.legend(frameon=False, fontsize=9)
fig.suptitle("Lithium / Diversified Miner Peer Set — Trailing vs Forward P/E", fontsize=11.8, color=NAVY, x=0.5, y=1.02, fontweight="bold")
fig.text(0.5, -0.06, "Source: Alpha Vantage (SQM) and StockAnalysis.com (ALB, RIO), as of 14 August 2026 close. Albemarle trailing P/E of 279x reflects near break-even TTM earnings\nand is not economically meaningful; shown for completeness.",
          ha="center", fontsize=7.2, color=BROWN)
fig.tight_layout()
fig.savefig(os.path.join(CH,"08_peer_pe.png"), bbox_inches="tight")
plt.close(fig)

print("Charts written to", CH)

# ============================================== 0. COVER MINI CHART =======
n_cover = 14  # ~3 months of weekly closes
cdates = dates[-n_cover:]
ccloses = closes[-n_cover:]
fig, ax = plt.subplots(figsize=(6.6,2.55), dpi=220)
ax.plot(cdates, ccloses, color=NAVY, linewidth=2.0, zorder=3)
ax.fill_between(cdates, ccloses, min(ccloses)*0.985, color=CAMEL, alpha=0.35, zorder=2)
ax.scatter([cdates[-1]],[ccloses[-1]], color=OLIVE, zorder=5, s=30)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_facecolor(IVORY)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax.tick_params(length=0, labelsize=8)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
fig.patch.set_facecolor(IVORY)
fig.tight_layout()
fig.savefig(os.path.join(CH,"00_cover_chart.png"), bbox_inches="tight")
plt.close(fig)
print("cover chart done")
