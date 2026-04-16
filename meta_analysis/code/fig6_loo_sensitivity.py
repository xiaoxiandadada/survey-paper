"""
Fig 6 — Leave-One-Out (LOO) Sensitivity Analysis
For each study, re-runs DL random-effects meta-analysis with that study removed.
Horizontal bar chart of LOO pooled AUC, sorted ascending.
Dashed line = full pooled AUC. Top-3 most influential studies annotated.
Output: fig6_loo_sensitivity.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import expit

# ── Paths ─────────────────────────────────────────────────────────────────────
LOO_LDCT  = "../loo_LDCT_traditional.csv"
LOO_CFDNA = "../loo_cfDNA_traditional.csv"
OUT_PNG   = "../fig6_loo_sensitivity.png"

FULL_AUC = {
    "LDCT_traditional":  0.860,
    "cfDNA_traditional": 0.859,
}
CAT_COLORS = {
    "LDCT_traditional":  "#2166ac",
    "cfDNA_traditional": "#d73027",
}
CAT_LABELS = {
    "LDCT_traditional":  "LDCT + Traditional ML",
    "cfDNA_traditional": "cfDNA + Traditional ML",
}

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

for ax, (cat, loo_path) in zip(axes, [
        ("LDCT_traditional",  LOO_LDCT),
        ("cfDNA_traditional", LOO_CFDNA)]):

    loo   = pd.read_csv(loo_path).sort_values("pooled_auc_loo")
    y     = np.arange(len(loo))
    color = CAT_COLORS[cat]

    ax.barh(y, loo["pooled_auc_loo"], color=color, alpha=0.55, height=0.7, zorder=2)
    ax.axvline(FULL_AUC[cat], color="#333333", lw=1.5, ls="--", zorder=3,
               label=f"Full pooled AUC = {FULL_AUC[cat]:.3f}")

    ax.set_yticks([])
    ax.set_xlabel("Pooled AUC (leave-one-out)", fontsize=10)
    ax.set_title(
        f"{CAT_LABELS[cat]}\n"
        f"Range: [{loo['pooled_auc_loo'].min():.3f}, {loo['pooled_auc_loo'].max():.3f}]",
        fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)

    # Annotate top-3 most influential studies
    top3 = loo.nlargest(3, "abs_delta")
    for _, r in top3.iterrows():
        idx_pos = list(loo.index).index(loo[loo["paper_id"] == r["paper_id"]].index[0])
        ax.text(r["pooled_auc_loo"] + 0.0005, y[idx_pos],
                str(r["title"])[:30] + "...",
                va="center", fontsize=5.5, color="#333333")

plt.suptitle("Leave-One-Out Sensitivity Analysis - Lung Cancer Meta-Analysis",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight")
plt.close()
print(f"Saved: {OUT_PNG}")
