"""
Fig 2 — Forest Plot: cfDNA + Traditional ML (k=29)
DerSimonian-Laird random-effects meta-analysis on logit-transformed AUC.
Studies sorted by AUC; all 29 studies displayed (k <= 30).
Marker size proportional to RE weight; color by validation type.
Output: fig2_forest_cfDNA_traditional.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.special import expit
from scipy import stats

# ── Paths ─────────────────────────────────────────────────────────────────────
AUC_CSV  = "../auc_dataset.csv"
OUT_PNG  = "../fig2_forest_cfDNA_traditional.png"
CATEGORY = "cfDNA_traditional"

# ── DL random-effects helper ──────────────────────────────────────────────────
def dl_meta(y, v):
    k = len(y); w = 1.0 / v
    theta_fe = np.sum(w * y) / np.sum(w)
    Q = np.sum(w * (y - theta_fe) ** 2)
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (k - 1)) / c)
    w_re = 1.0 / (v + tau2)
    theta_re = np.sum(w_re * y) / np.sum(w_re)
    se_re = np.sqrt(1.0 / np.sum(w_re))
    return {
        "pooled_auc": float(expit(theta_re)),
        "ci_lo":      float(expit(theta_re - 1.96 * se_re)),
        "ci_hi":      float(expit(theta_re + 1.96 * se_re)),
        "tau2": tau2,
        "I2":   max(0, (Q - (k - 1)) / Q * 100) if Q > 0 else 0,
        "Q": Q,
        "Q_pval": 1 - stats.chi2.cdf(Q, k - 1),
        "w_re": w_re,
    }

# ── Color scheme ──────────────────────────────────────────────────────────────
VAL_COLORS = {
    "external_validation": "#2166ac",
    "none":                "#d73027",
    "internal_CV":         "#f4a582",
    "prospective":         "#4dac26",
}
VAL_NAMES = {
    "external_validation": "External validation",
    "none":                "No external validation",
    "internal_CV":         "Internal CV",
    "prospective":         "Prospective validation",
}

# ── Main ──────────────────────────────────────────────────────────────────────
auc_df = pd.read_csv(AUC_CSV)
sub = auc_df[auc_df["category"] == CATEGORY].copy()
sub = sub.sort_values("auc").reset_index(drop=True)

res = dl_meta(sub["logit_auc"].values, sub["var_logit"].values)
sub["w_re"] = res["w_re"]

# All studies shown (k=29 <= 30)
sub_show = sub.copy().reset_index(drop=True)
truncated = False
n_hidden = 0

w_show = sub_show["w_re"].values
w_norm = (w_show / w_show.max()) * 200 + 20

n_rows = len(sub_show) + 3
fig_h = max(8, n_rows * 0.30 + 2.5)
fig, ax = plt.subplots(figsize=(12, fig_h))
y_pos = list(range(len(sub_show), 0, -1))

# Per-study CIs
for i, (_, row) in enumerate(sub_show.iterrows()):
    lo = float(expit(row["logit_auc"] - 1.96 * np.sqrt(row["var_logit"])))
    hi = float(expit(row["logit_auc"] + 1.96 * np.sqrt(row["var_logit"])))
    color = VAL_COLORS.get(row.get("validation_type", "none"), "#888888")
    yp = y_pos[i]
    ax.plot([lo, hi], [yp, yp], color=color, lw=0.9, alpha=0.7, zorder=2)
    ax.scatter(row["auc"], yp, s=w_norm[i], color=color, zorder=3,
               edgecolors="white", lw=0.4)

# Pooled diamond
d_lo, d_hi, d_mid = res["ci_lo"], res["ci_hi"], res["pooled_auc"]
diamond = plt.Polygon(
    [[d_lo, 0], [d_mid, 0.45], [d_hi, 0], [d_mid, -0.45]],
    closed=True, color="#1a1a2e", zorder=5)
ax.add_patch(diamond)
ax.axvline(d_mid, color="#1a1a2e", lw=1.0, ls="--", alpha=0.5, zorder=1)
ax.axvline(0.5,   color="#aaaaaa", lw=0.7, ls=":",  zorder=0)

ax.set_xlim(0.35, 1.05)
ax.set_ylim(-1.5, len(sub_show) + 1.8)
ax.set_xlabel("AUC (Area Under the ROC Curve)", fontsize=10)
ax.set_yticks([])

# Study labels
for i, (_, row) in enumerate(sub_show.iterrows()):
    label = row["title"][:48] + ("..." if len(row["title"]) > 48 else "")
    yr = f" ({int(row['year'])})" if pd.notna(row["year"]) else ""
    ax.text(0.362, y_pos[i], label + yr, ha="left", va="center",
            fontsize=5.5, color="#333333")

ax.text(0.362, 0, f"Pooled (k={len(sub)})", ha="left", va="center",
        fontsize=8.5, fontweight="bold", color="#1a1a2e")
ax.text(d_mid, -0.9, f"AUC = {d_mid:.3f}\n[{d_lo:.3f}, {d_hi:.3f}]",
        ha="center", va="top", fontsize=7.5, color="#1a1a2e", fontweight="bold")

# Stats box
q_pval_str = "< 0.001" if res["Q_pval"] < 0.001 else f"= {res['Q_pval']:.3f}"
stats_txt = (f"k = {len(sub)}\n"
             f"Pooled AUC = {d_mid:.3f} [{d_lo:.3f}-{d_hi:.3f}]\n"
             f"tau2 = {res['tau2']:.3f}   I2 = {res['I2']:.1f}%\n"
             f"Q({len(sub)-1}) = {res['Q']:.1f},  p {q_pval_str}")
ax.text(1.04, len(sub_show) / 2, stats_txt, ha="left", va="center",
        fontsize=7.5, family="monospace",
        bbox=dict(boxstyle="round,pad=0.5", fc="#f8f8f8", ec="#cccccc", lw=0.8))

handles = [mpatches.Patch(color=c, label=VAL_NAMES[k])
           for k, c in VAL_COLORS.items() if k in sub["validation_type"].values]
ax.legend(handles=handles, loc="lower right", fontsize=7, framealpha=0.9,
          title="Validation type", title_fontsize=7.5)

ax.set_title("Forest Plot - cfDNA + Traditional ML\n"
             "(Random-effects, DerSimonian-Laird; AUC=1.0 excluded)",
             fontsize=10.5, fontweight="bold", pad=10)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="x", labelsize=8)

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight")
plt.close()
print(f"Saved: {OUT_PNG}")
