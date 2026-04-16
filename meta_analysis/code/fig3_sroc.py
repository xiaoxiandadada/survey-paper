"""
Fig 3 — Summary ROC (SROC) Curves
Bivariate random-effects model pooled operating points for 3 categories.
Individual study scatter + pooled diamond markers + 95% CI ellipses.
Pooled sens/spec values taken from Reitsma bivariate model (sensspec_results.csv).
Output: fig3_sroc.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# ── Paths ─────────────────────────────────────────────────────────────────────
SENSSPEC_CSV = "../sensspec_dataset.csv"
RESULTS_CSV  = "../sensspec_results.csv"
OUT_PNG      = "../fig3_sroc.png"

# ── Bivariate model results (from Reitsma model, Step 3) ─────────────────────
# Loaded from sensspec_results.csv; hard-coded here for clarity
bivar_results = {
    "LDCT_traditional": {
        "sens": 0.831, "sens_lo": 0.705, "sens_hi": 0.910,
        "spec": 0.833, "spec_lo": 0.732, "spec_hi": 0.901, "k": 23,
    },
    "cfDNA_traditional": {
        "sens": 0.739, "sens_lo": 0.520, "sens_hi": 0.880,
        "spec": 0.773, "spec_lo": 0.606, "spec_hi": 0.882, "k": 21,
    },
    "cfDNA_LDCT_traditional": {
        "sens": 0.835, "sens_lo": 0.798, "sens_hi": 0.867,
        "spec": 0.929, "spec_lo": 0.788, "spec_hi": 0.979, "k": 14,
    },
}

CAT_COLORS = {
    "LDCT_traditional":       "#2166ac",
    "cfDNA_traditional":      "#d73027",
    "cfDNA_LDCT_traditional": "#4dac26",
}
CAT_LABELS = {
    "LDCT_traditional":       "LDCT + Traditional ML",
    "cfDNA_traditional":      "cfDNA + Traditional ML",
    "cfDNA_LDCT_traditional": "cfDNA + LDCT + Traditional ML",
}

# ── Plot ──────────────────────────────────────────────────────────────────────
sens_df = pd.read_csv(SENSSPEC_CSV)

fig, ax = plt.subplots(figsize=(7, 7))

for cat, res in bivar_results.items():
    color  = CAT_COLORS[cat]
    sens_p = res["sens"]
    spec_p = res["spec"]
    fpr_p  = 1 - spec_p

    # Individual study scatter
    sub    = sens_df[sens_df["category"] == cat]
    fpr_i  = 1 - sub["specificity"].values
    sens_i = sub["sensitivity"].values
    ax.scatter(fpr_i, sens_i, color=color, alpha=0.35, s=28, zorder=2,
               edgecolors="none")

    # Pooled operating point
    ax.scatter(fpr_p, sens_p, color=color, s=180, zorder=5,
               edgecolors="white", lw=1.5, marker="D",
               label=f"{CAT_LABELS[cat]} (k={res['k']})\n"
                     f"Sens={sens_p:.2f}, Spec={spec_p:.2f}")

    # 95% CI ellipse (width = spec CI width, height = sens CI height)
    w = res["spec_hi"] - res["spec_lo"]
    h = res["sens_hi"] - res["sens_lo"]
    ellipse = Ellipse(xy=(fpr_p, sens_p), width=w, height=h,
                      edgecolor=color, facecolor="none",
                      lw=1.5, ls="--", zorder=4, alpha=0.75)
    ax.add_patch(ellipse)

# Reference diagonal
ax.plot([0, 1], [0, 1], color="#aaaaaa", lw=1, ls=":", zorder=0)

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_xlabel("1 - Specificity (False Positive Rate)", fontsize=11)
ax.set_ylabel("Sensitivity (True Positive Rate)", fontsize=11)
ax.set_title("Summary ROC (SROC) - Lung Cancer\nBivariate Random-Effects Model",
             fontsize=11.5, fontweight="bold")
ax.legend(loc="lower right", fontsize=8, framealpha=0.9,
          title="Category", title_fontsize=8.5)
ax.spines[["top", "right"]].set_visible(False)
ax.set_xticks(np.arange(0, 1.1, 0.2))
ax.set_yticks(np.arange(0, 1.1, 0.2))
ax.grid(True, alpha=0.2, lw=0.5)

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight")
plt.close()
print(f"Saved: {OUT_PNG}")
