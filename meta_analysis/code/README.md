# Meta-Analysis Code

Each script generates one figure. Run from this directory (`meta_analysis/code/`);
all paths are relative to the parent `meta_analysis/` folder.

## Dependencies

```
pip install pandas numpy matplotlib scipy
```

## Scripts

| Script | Output | Description |
|--------|--------|-------------|
| `fig1_forest_LDCT_traditional.py` | `fig1_forest_LDCT_traditional.png` | Forest plot — LDCT + Traditional ML (k=68), DL random-effects |
| `fig2_forest_cfDNA_traditional.py` | `fig2_forest_cfDNA_traditional.png` | Forest plot — cfDNA + Traditional ML (k=29), DL random-effects |
| `fig3_sroc.py` | `fig3_sroc.png` | SROC curves — bivariate model pooled operating points (3 categories) |
| `fig4_funnel.py` | `fig4_funnel.png` | Funnel plots + Egger's test (publication bias) |
| `fig5_subgroup.py` | `fig5_subgroup.png` | Subgroup analysis — study design & validation type |
| `fig6_loo_sensitivity.py` | `fig6_loo_sensitivity.png` | Leave-one-out sensitivity analysis |
| `fig7_summary_panel.py` | `fig7_summary_panel.png` | Summary panel — pooled AUC and I² by category |

## Input files (in `meta_analysis/`)

| File | Used by |
|------|---------|
| `auc_dataset.csv` | fig1, fig2, fig4, fig6 |
| `sensspec_dataset.csv` | fig3 |
| `sensspec_results.csv` | fig3 (reference) |
| `subgroup_results.csv` | fig5 |
| `publication_bias.csv` | fig4 |
| `loo_LDCT_traditional.csv` | fig6 |
| `loo_cfDNA_traditional.csv` | fig6 |

## Run all figures

```bash
cd meta_analysis/code
for f in fig*.py; do python "$f"; done
```
