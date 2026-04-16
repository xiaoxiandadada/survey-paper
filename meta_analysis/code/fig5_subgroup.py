"""
Fig 5 — Subgroup Analysis
Pooled AUC (95% CI) by study design and validation type for
LDCT_traditional and cfDNA_traditional.
Between-group p-values from z-test on logit scale.
Output: fig5_subgroup.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Paths ─────────────────────────────────────────────────────────────────────
SUBGROUP_CSV = "../subgroup_results.csv"
OUT_PNG      = "../fig5_subgroup.png"

# ── Between-group p-values (from Step 4 z-test on logit scale) ───────────────
PVALS = {
    ("LDCT_traditional",  "Study Design"):    0.057,
    ("LDCT_traditional",  "Validation Type"): 0.52,
    ("cfDNA_traditional", "Validation Type"): 0.43,
}

COLORS = {
    "Prospective/RCT":         "#2166ac",
    "Retrospective/Other":     "#d73027",
    "External validation":     "#4dac26",
    "No external validation":  "#f4a582",
}

CAT_LABELS = {
    "LDCT_traditional":  "LDCT + Traditional ML",
    "cfDNA_traditional": "cfDNA + Traditional ML",
}

# ── Plot ──────────────────────────────────────────────────────────────────────
subgroup_df = pd.read_csv(SUBGROUP_CSV)

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=False)

for ax_idx, cat in enumerate(["LDCT_traditional", "cfDNA_traditional"]):
    ax  = axes[ax_idx]
    sub = subgroup_df[subgroup_df["category"] == cat].dropna(subset=["pooled_auc"])

    y_counter = 0
    prev_type = None

    for _, row in sub.iterrows():
        if row["subgroup_type"] != prev_type:
            if prev_type is not None:
                y_counter -= 0.5
            ax.text(-0.01, y_counter, row["subgroup_type"],
                    ha="right", va="center", fontsize=8.5, fontweight="bold",
                    color="#333333", transform=ax.get_yaxis_transform())
            y_counter -= 1
            prev_type = row["subgroup_type"]

        color = COLORS.get(row["subgroup"], "#888888")
        ax.plot([row["ci_lo"], row["ci_hi"]], [y_counter, y_counter],
                color=color, lw=2.5, solid_capstyle="round", zorder=2)
        ax.scatter(row["pooled_auc"], y_counter, color=color, s=80, zorder=3,
                   edgecolors="white", lw=1)

        label = f"{row['subgroup']} (k={int(row['k'])})"
        ax.text(row["ci_lo"] - 0.005, y_counter, label,
                ha="right", va="center", fontsize=8, color=color)
        ax.text(row["ci_hi"] + 0.005, y_counter,
                f"{row['pooled_auc']:.3f} [{row['ci_lo']:.3f}-{row['ci_hi']:.3f}]",
                ha="left", va="center", fontsize=7.5, color="#555555")
        y_counter -= 1

    # p-value annotations
    y_counter -= 0.3
    for (c, st), pv in PVALS.items():
        if c == cat:
            sig = "dagger" if pv < 0.10 else "ns"
            sig_sym = "+" if pv < 0.10 else "ns"
            ax.text(0.98, y_counter,
                    f"{st}: p={pv:.3f} ({sig_sym})",
                    ha="right", va="center", fontsize=8, color="#555555",
                    transform=ax.transAxes)
            y_counter -= 0.8

    ax.axvline(0.5, color="#cccccc", lw=0.7, ls=":", zorder=0)
    ax.set_xlim(0.60, 1.02)
    ax.set_yticks([])
    ax.set_xlabel("Pooled AUC (95% CI)", fontsize=10)
    ax.set_title(CAT_LABELS[cat], fontsize=10.5, fontweight="bold")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)

plt.suptitle("Subgroup Analysis - Lung Cancer Meta-Analysis",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight")
plt.close()
print(f"Saved: {OUT_PNG}")
