"""
Fig 7 — Summary Panel: Pooled AUC and I2 by Category
Left panel: bar chart of pooled AUC with 95% CI error bars, k labels,
  hatching for descriptive-only categories (k<10), significance bracket.
Right panel: bar chart of I2 heterogeneity with reference lines at 50% and 75%.
Output: fig7_summary_panel.png
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Data (from pooled_auc_results.csv, Step 2) ────────────────────────────────
SUMMARY = [
    {"cat": "LDCT\n+ Traditional ML",        "k": 68,  "auc": 0.860, "lo": 0.842, "hi": 0.877, "I2": 99.3, "color": "#2166ac", "full": True},
    {"cat": "LDCT\n+ LLM",                   "k": 5,   "auc": 0.855, "lo": 0.768, "hi": 0.913, "I2": 99.4, "color": "#74add1", "full": False},
    {"cat": "cfDNA\n+ Traditional ML",        "k": 29,  "auc": 0.859, "lo": 0.799, "hi": 0.903, "I2": 98.7, "color": "#d73027", "full": True},
    {"cat": "cfDNA + LDCT\n+ Traditional ML", "k": 18,  "auc": 0.902, "lo": 0.879, "hi": 0.922, "I2": 87.4, "color": "#4dac26", "full": False},
]

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
x = np.arange(len(SUMMARY))

# ── Left: Pooled AUC ─────────────────────────────────────────────────────────
for i, s in enumerate(SUMMARY):
    ax1.bar(i, s["auc"], color=s["color"],
            alpha=0.75 if s["full"] else 0.45,
            width=0.55, zorder=2, edgecolor="white", lw=0.5)
    ax1.errorbar(i, s["auc"],
                 yerr=[[s["auc"] - s["lo"]], [s["hi"] - s["auc"]]],
                 fmt="none", color="#333333", capsize=5, lw=1.5, zorder=3)
    ax1.text(i, s["hi"] + 0.008, f"{s['auc']:.3f}",
             ha="center", va="bottom", fontsize=9, fontweight="bold",
             color=s["color"])
    ax1.text(i, s["lo"] - 0.015, f"k={s['k']}",
             ha="center", va="top", fontsize=8, color="#555555")

# Significance bracket: LDCT_trad vs cfDNA_LDCT_trad (p=0.005)
y_br = 0.945
ax1.plot([0, 3], [y_br, y_br], color="#333333", lw=1)
ax1.plot([0, 0], [y_br - 0.005, y_br], color="#333333", lw=1)
ax1.plot([3, 3], [y_br - 0.005, y_br], color="#333333", lw=1)
ax1.text(1.5, y_br + 0.003, "p = 0.005 **",
         ha="center", va="bottom", fontsize=8.5, color="#333333")

# Hatching for descriptive-only
for i, s in enumerate(SUMMARY):
    if not s["full"]:
        ax1.bar(i, s["auc"], color="none", width=0.55, hatch="///",
                edgecolor="#aaaaaa", lw=0.5, zorder=4, alpha=0.5)

ax1.set_xticks(x)
ax1.set_xticklabels([s["cat"] for s in SUMMARY], fontsize=9)
ax1.set_ylim(0.65, 0.98)
ax1.set_ylabel("Pooled AUC (95% CI)", fontsize=10)
ax1.set_title("Pooled AUC by Category", fontsize=11, fontweight="bold")
ax1.axhline(0.5, color="#cccccc", lw=0.7, ls=":", zorder=0)
ax1.spines[["top", "right"]].set_visible(False)
ax1.tick_params(axis="y", labelsize=8)

full_patch = mpatches.Patch(color="#555555", alpha=0.75,
                             label="Full meta-analysis")
desc_patch = mpatches.Patch(color="#aaaaaa", alpha=0.45, hatch="///",
                             label="Descriptive only (k<10)")
ax1.legend(handles=[full_patch, desc_patch], fontsize=8, loc="lower right")

# ── Right: I2 ────────────────────────────────────────────────────────────────
for i, s in enumerate(SUMMARY):
    ax2.bar(i, s["I2"], color=s["color"],
            alpha=0.75 if s["full"] else 0.45,
            width=0.55, zorder=2, edgecolor="white", lw=0.5)
    ax2.text(i, s["I2"] + 0.8, f"{s['I2']:.1f}%",
             ha="center", va="bottom", fontsize=9, fontweight="bold",
             color=s["color"])

ax2.axhline(75, color="#d73027", lw=1, ls="--", alpha=0.6,
            label="I2=75% (high heterogeneity)")
ax2.axhline(50, color="#f4a582", lw=1, ls="--", alpha=0.6,
            label="I2=50% (moderate)")
ax2.set_xticks(x)
ax2.set_xticklabels([s["cat"] for s in SUMMARY], fontsize=9)
ax2.set_ylim(0, 105)
ax2.set_ylabel("I2 (%)", fontsize=10)
ax2.set_title("Heterogeneity (I2) by Category", fontsize=11, fontweight="bold")
ax2.spines[["top", "right"]].set_visible(False)
ax2.tick_params(axis="y", labelsize=8)
ax2.legend(fontsize=8, loc="lower right")

plt.suptitle("Lung Cancer Screening Meta-Analysis - Summary",
             fontsize=12.5, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("../fig7_summary_panel.png", dpi=180, bbox_inches="tight")
plt.close()
print("Saved: ../fig7_summary_panel.png")
