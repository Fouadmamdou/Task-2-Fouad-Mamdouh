import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Setup ─────────────────────────────────────────────────────────────────────
df = pd.read_excel("Task-1/Dataset_Cleaned.xlsx")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")
df["Year"] = df["Date"].dt.year

PURPLE = "#7F77DD"
TEAL   = "#1D9E75"
CORAL  = "#D85A30"
BLUE   = "#378ADD"
AMBER  = "#EF9F27"
GRAY   = "#888780"
LIGHT  = "#F1EFE8"

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
})

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 22))
fig.patch.set_facecolor("white")
gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.55, wspace=0.38)

# ── KPI banner ────────────────────────────────────────────────────────────────
ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.axis("off")
kpis = [
    ("Total Revenue",        f"${df['TotalPrice'].sum():,.0f}",      "Jan 2023 – Jun 2025"),
    ("Mean Order Value",     f"${df['TotalPrice'].mean():,.0f}",      f"Median ${df['TotalPrice'].median():,.0f}"),
    ("Total Orders",         f"{len(df):,}",                          "7 product categories"),
    ("Cancel + Return Rate", f"{(df['OrderStatus'].isin(['Cancelled','Returned']).sum()/len(df)*100):.1f}%",
                             f"Only {(df['OrderStatus'].eq('Delivered').sum()/len(df)*100):.1f}% delivered ⚠"),
]
for i, (label, value, sub) in enumerate(kpis):
    x = 0.125 + i * 0.25
    rect = plt.Rectangle((x - 0.115, 0.05), 0.23, 0.9,
                          transform=ax_kpi.transAxes, color=LIGHT,
                          zorder=0, clip_on=False, linewidth=0)
    ax_kpi.add_patch(rect)
    color = CORAL if i == 3 else "#2C2C2A"
    ax_kpi.text(x, 0.72, label, transform=ax_kpi.transAxes,
                ha="center", va="center", fontsize=10, color=GRAY)
    ax_kpi.text(x, 0.45, value, transform=ax_kpi.transAxes,
                ha="center", va="center", fontsize=22, fontweight="bold", color=color)
    ax_kpi.text(x, 0.18, sub, transform=ax_kpi.transAxes,
                ha="center", va="center", fontsize=9, color=GRAY)
ax_kpi.set_title("E-commerce Analytics Report", fontsize=16, fontweight="bold",
                 pad=18, color="#2C2C2A", loc="left")

# ── 1. Monthly Revenue Trend ──────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[1, :2])
monthly = df.groupby("Month")["TotalPrice"].sum().reset_index()
monthly["Month_dt"] = monthly["Month"].dt.to_timestamp()
monthly["year"] = monthly["Month_dt"].dt.year
colors_bar = monthly["year"].map({2023: "#B5D4F4", 2024: "#378ADD", 2025: "#0C447C"})
bars = ax1.bar(range(len(monthly)), monthly["TotalPrice"], color=colors_bar, width=0.75, zorder=2)
ax1.set_xticks(range(len(monthly)))
ax1.set_xticklabels(
    [m.strftime("%b %y") if m.month in (1, 6, 12) else "" for m in monthly["Month_dt"]],
    fontsize=8, rotation=0
)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
ax1.set_title("Monthly revenue", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")
ax1.tick_params(axis="y", labelsize=9)
from matplotlib.patches import Patch
legend_els = [Patch(color="#B5D4F4", label="2023"),
              Patch(color="#378ADD", label="2024"),
              Patch(color="#0C447C", label="2025")]
ax1.legend(handles=legend_els, fontsize=8, frameon=False, loc="upper right")

# ── 2. Order Status ───────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 2])
status_counts = df["OrderStatus"].value_counts()
status_colors = {"Cancelled": CORAL, "Returned": AMBER, "Pending": BLUE,
                 "Shipped": TEAL, "Delivered": PURPLE}
wedge_colors = [status_colors[s] for s in status_counts.index]
wedges, texts, autotexts = ax2.pie(
    status_counts.values, labels=None, colors=wedge_colors,
    autopct="%1.1f%%", startangle=90,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=1.5),
    pctdistance=0.78
)
for at in autotexts:
    at.set_fontsize(8)
    at.set_color("white")
    at.set_fontweight("bold")
ax2.legend(status_counts.index, loc="lower center", fontsize=8,
           frameon=False, ncol=2, bbox_to_anchor=(0.5, -0.12))
ax2.set_title("Order status", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")

# ── 3. Revenue by Product ─────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2, 0])
prod = df.groupby("Product")["TotalPrice"].sum().sort_values()
bar_colors = [TEAL if v == prod.max() else "#9FE1CB" for v in prod.values]
ax3.barh(prod.index, prod.values, color=bar_colors, height=0.65, zorder=2)
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
ax3.tick_params(axis="both", labelsize=9)
ax3.set_title("Revenue by product", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")
for i, (val, name) in enumerate(zip(prod.values, prod.index)):
    ax3.text(val + 1500, i, f"${val/1000:.0f}k", va="center", fontsize=8, color=GRAY)

# ── 4. Cart Size vs AOV ───────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[2, 1])
cart = df.groupby("CartSize")["TotalPrice"].mean()
ax4.plot(cart.index, cart.values, color=PURPLE, linewidth=2.5, marker="o",
         markersize=6, markerfacecolor="white", markeredgewidth=2, zorder=3)
ax4.fill_between(cart.index, cart.values, alpha=0.12, color=PURPLE)
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax4.set_xlabel("Cart size", fontsize=9, color=GRAY)
ax4.tick_params(axis="both", labelsize=9)
ax4.set_title("Cart size vs avg order value", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")
ax4.annotate("5× lift\ncart 1→10", xy=(10, 1743), xytext=(7.5, 1600),
             fontsize=8, color=PURPLE, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.2))

# ── 5. Referral Source AOV ────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, 2])
ref = df.groupby("ReferralSource")["TotalPrice"].mean().sort_values(ascending=False)
bar_colors_ref = [BLUE if v == ref.max() else "#B5D4F4" for v in ref.values]
ax5.bar(ref.index, ref.values, color=bar_colors_ref, width=0.6, zorder=2)
ax5.set_ylim(990, 1120)
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax5.tick_params(axis="x", labelsize=8, rotation=15)
ax5.tick_params(axis="y", labelsize=9)
ax5.set_title("Referral source — avg order value", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")
for i, (val, name) in enumerate(zip(ref.values, ref.index)):
    ax5.text(i, val + 2, f"${val:,.0f}", ha="center", fontsize=8, color=GRAY)

# ── 6. Year-over-Year ─────────────────────────────────────────────────────────
ax6 = fig.add_subplot(gs[3, 0])
yoy = df.groupby("Year").agg(Orders=("OrderID", "count"), AOV=("TotalPrice", "mean")).reset_index()
x = np.arange(len(yoy))
bars6 = ax6.bar(x, yoy["Orders"], color=["#B5D4F4", "#378ADD", "#0C447C"], width=0.55, zorder=2)
ax6b = ax6.twinx()
ax6b.plot(x, yoy["AOV"], color=TEAL, marker="D", markersize=7,
          linewidth=2, markerfacecolor="white", markeredgewidth=2)
ax6b.set_ylim(950, 1150)
ax6b.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax6b.tick_params(axis="y", labelsize=9, colors=TEAL)
ax6b.spines["right"].set_visible(True)
ax6b.spines["top"].set_visible(False)
ax6.set_xticks(x)
ax6.set_xticklabels(["2023", "2024", "2025*"], fontsize=9)
ax6.tick_params(axis="y", labelsize=9)
ax6.set_title("Year-over-year: orders & AOV", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")
ax6.text(0.02, 0.06, "*2025 partial year", transform=ax6.transAxes, fontsize=7, color=GRAY)
from matplotlib.lines import Line2D
l1 = Patch(color="#B5D4F4", label="Orders")
l2 = Line2D([0], [0], color=TEAL, marker="D", markersize=6, label="AOV")
ax6.legend(handles=[l1, l2], fontsize=8, frameon=False)

# ── 7. TotalPrice Distribution + Outliers ────────────────────────────────────
ax7 = fig.add_subplot(gs[3, 1])
Q1, Q3 = df["TotalPrice"].quantile(0.25), df["TotalPrice"].quantile(0.75)
IQR = Q3 - Q1
upper = Q3 + 1.5 * IQR
ax7.hist(df["TotalPrice"], bins=40, color=PURPLE, alpha=0.75, edgecolor="white", zorder=2)
ax7.axvline(df["TotalPrice"].mean(), color=CORAL, linestyle="--", linewidth=1.5, label=f"Mean ${df['TotalPrice'].mean():,.0f}")
ax7.axvline(df["TotalPrice"].median(), color=TEAL, linestyle="--", linewidth=1.5, label=f"Median ${df['TotalPrice'].median():,.0f}")
ax7.axvline(upper, color=AMBER, linestyle=":", linewidth=1.5, label=f"Outlier threshold ${upper:,.0f}")
ax7.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax7.tick_params(axis="x", labelsize=8, rotation=15)
ax7.tick_params(axis="y", labelsize=9)
ax7.set_title("Order value distribution & outliers", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")
ax7.legend(fontsize=8, frameon=False)

# ── 8. Payment Method ─────────────────────────────────────────────────────────
ax8 = fig.add_subplot(gs[3, 2])
pay = df["PaymentMethod"].value_counts()
pay_colors = [BLUE, GRAY, PURPLE, TEAL, AMBER]
ax8.barh(pay.index[::-1], pay.values[::-1], color=pay_colors[::-1], height=0.6, zorder=2)
ax8.tick_params(axis="both", labelsize=9)
ax8.set_title("Payment method", fontsize=11, fontweight="bold", color="#2C2C2A", loc="left")
for i, val in enumerate(pay.values[::-1]):
    ax8.text(val + 1, i, str(val), va="center", fontsize=9, color=GRAY)
ax8.set_xlim(0, pay.max() + 30)
ax8.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x)}"))

plt.suptitle("", y=1)
plt.savefig("EDA_Report.png",
            dpi=160, bbox_inches="tight", facecolor="white")
print("Saved → EDA_Report.png")

# ── Print summary stats ───────────────────────────────────────────────────────
print("\n── Basic Statistics ──────────────────────────────────────")
print(df[["Quantity", "UnitPrice", "TotalPrice", "CartSize"]].describe().round(2))

print("\n── Revenue by Product ────────────────────────────────────")
print(df.groupby("Product").agg(
    Orders=("OrderID", "count"),
    Revenue=("TotalPrice", "sum"),
    AOV=("TotalPrice", "mean")
).round(2).sort_values("Revenue", ascending=False))

print("\n── Outliers (IQR method) ─────────────────────────────────")
outliers = df[(df["TotalPrice"] < Q1 - 1.5*IQR) | (df["TotalPrice"] > upper)]
print(f"Count: {len(outliers)}")
print(outliers[["OrderID","Product","Quantity","UnitPrice","TotalPrice"]].sort_values("TotalPrice", ascending=False))

print("\n── Key Observations ──────────────────────────────────────")
cancel_return = df["OrderStatus"].isin(["Cancelled", "Returned"]).sum()
delivered = df["OrderStatus"].eq("Delivered").sum()
print(f"  Cancel+Return rate : {cancel_return/len(df)*100:.1f}%  ⚠ Critical")
print(f"  Delivered rate     : {delivered/len(df)*100:.1f}%")
print(f"  Mean vs Median AOV : ${df['TotalPrice'].mean():,.0f} vs ${df['TotalPrice'].median():,.0f}  (right-skewed)")
print(f"  CartSize-AOV range : ${cart.min():,.0f} (size 1) → ${cart.max():,.0f} (size 10)")
print(f"  Top referral AOV   : {ref.idxmax()} (${ref.max():,.0f})")
print(f"  YoY AOV decline    : 2023 ${yoy[yoy.Year==2023].AOV.values[0]:,.0f} → 2024 ${yoy[yoy.Year==2024].AOV.values[0]:,.0f}")
