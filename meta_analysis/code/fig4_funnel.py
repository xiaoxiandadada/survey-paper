"""
Fig 4 — Funnel Plots + Egger's Test
Publication bias assessment for LDCT_traditional and cfDNA_traditional.
x-axis: logit(AUC); y-axis: standard error (inverted, funnel convention).
Dashed lines: 95% pseudo-CI around pooled logit(AUC).
Egger's regression test: regresses standardised effect on precision.
Output: fig4_funnel.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import logit
from scipy import stats

# ── Paths ─────────────────────────────────────────────────────────────────────
AUC_CSV    = "../auc_dataset.csv"
BIAS_CSV   = "../publication_bias.csv"
OUT_PNG    = "../fig4_funnel.png"

# ── Pooled logit(AUC) from primary meta-analysis ──────────────────────────────
POOLED_AUC = {
    "LDCT_traditional":  0.860,
    "cfDNA_traditional": 0.859,
}
POOLED_LOGIT = {k: float(logit(v)) for k, v in POOLED_AUC.items()}

CAT_COLORS = {
    "LDCT_traditional":  "#2166ac",
    "cfDNA_traditional": "#d73027",
}
CAT_LABELS = {
    "LDCT_traditional":  "LDCT + Traditional ML",
    "cfDNA_traditional": "cfDNA + Traditional ML",
}

# ── Egger's test ──────────────────────────────────────────────────────────────
def eggers_test(logit_auc, var_logit):
    y  = np.array(logit_auc)
    se = np.sqrt(np.array(var_logit))
    z_score  = y / se
    precision = 1.0 / se
    slope, intercept, _, _, _ = stats.linregress(precision, z_score)
    n = len(y)
    y_pred = intercept + slope * precision
    resid  = z_score - y_pred
    s2     = np.sum(resid ** 2) / (n - 2)
    Sxx    = np.sum((precision - precision.mean()) ** 2)
    se_int = np.sqrt(s2 * (1 / n + precision.mean() ** 2 / Sxx))
    t_int  = intercept / se_int
    p_int  = 2 * (1 - stats.t.cdf(abs(t_int), df=n - 2))
    return {"intercept": intercept, "se_intercept": se_int,
            "t_intercept": t_int, "p_intercept": p_int}

# ── Plot ──────────────────────────────────────────────────────────────────────
auc_df   = pd.read_csv(AUC_CSV)
bias_df  = pd.read_csv(BIAS_CSV)

fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

for ax, cat in zip(axes, ["LDCT_traditional", "cfDNA_traditional"]):
    sub = auc_df[auc_df["category"] == cat]
    se  = np.sqrt(sub["var_logit"].values)
    y   = sub["logit_auc"].values

    ax.scatter(y, se, color=CAT_COLORS[cat], alpha=0.55, s=30,
               edgecolors="none", zorder=3)

    # Funnel lines
    se_range = np.linspace(0, se.max() * 1.05, 200)
    ax.plot(POOLED_LOGIT[cat] + 1.96 * se_range, se_range,
            color="#888888", lw=1, ls="--")
    ax.plot(POOLED_LOGIT[cat] - 1.96 * se_range, se_range,
            color="#888888", lw=1, ls="--")
    ax.axvline(POOLED_LOGIT[cat], color="#333333", lw=1.2, ls="-", alpha=0.7)

    ax.set_xlabel("logit(AUC)", fontsize=10)
    ax.set_ylabel("Standard Error", fontsize=10)
    ax.invert_yaxis()

    # Egger's result from saved CSV
    row = bias_df[bias_df["category"] == cat].iloc[0]
    p_str  = f"p = {row['egger_p']:.4f}" if row["egger_p"] >= 0.001 else "p < 0.001"
    sig_str = " *" if row["egger_p"] < 0.10 else ""
    ax.set_title(
        f"{CAT_LABELS[cat]}\n"
        f"Egger's test: intercept={row['egger_intercept']:.2f}, {p_str}{sig_str}",
        fontsize=9.5, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=8)

plt.suptitle("Funnel Plots - Publication Bias Assessment",
             fontsize=12, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight")
plt.close()
print(f"Saved: {OUT_PNG}")
