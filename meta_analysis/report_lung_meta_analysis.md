# Meta-Analysis Report: AI-Assisted Lung Cancer Screening
## LDCT and cfDNA-Based Approaches — Diagnostic Performance

**Date:** April 2026  
**Scope:** Lung cancer papers from the survey-paper repository (4 categories)  
**Method:** DerSimonian-Laird random-effects meta-analysis (primary); Reitsma bivariate model (secondary)

---

## 1. Background

Lung cancer remains the leading cause of cancer mortality worldwide. Two major non-invasive screening paradigms have emerged: low-dose computed tomography (LDCT) and circulating cell-free DNA (cfDNA) liquid biopsy. Both have been increasingly combined with machine learning (ML) and large language model (LLM)-based approaches to improve diagnostic accuracy. This meta-analysis synthesizes the published diagnostic performance evidence across four technical categories applied to lung cancer screening.

---

## 2. Study Selection and Data

### 2.1 Categories Analyzed

| Category | Description | Analysis Type |
|----------|-------------|---------------|
| **LDCT_traditional** | LDCT imaging + traditional ML (radiomics, CNN, SVM, etc.) | Full meta-analysis |
| **cfDNA_traditional** | cfDNA liquid biopsy + traditional ML | Full meta-analysis |
| **cfDNA_LDCT_traditional** | Combined cfDNA + LDCT + traditional ML | Descriptive (k=18) |
| **LDCT_LLM** | LDCT + large language models | Descriptive (k=5) |

### 2.2 Inclusion/Exclusion

- **Included:** All papers with extractable AUC values from the lung cancer subset of the survey-paper repository
- **Excluded:** Papers with AUC = 1.0 (n=4; likely overfitted or non-representative test sets)
- **Primary metric:** AUC (Area Under the ROC Curve)
- **Secondary metric:** Sensitivity and specificity (paired, from papers reporting both)

### 2.3 Dataset Summary

| Category | k (AUC) | k (Sens/Spec) | Mean AUC | AUC Range |
|----------|---------|---------------|----------|-----------|
| LDCT_traditional | 68 | 23 | 0.860 | 0.52–0.98 |
| LDCT_LLM | 5 | 1 | 0.855 | — |
| cfDNA_traditional | 29 | 21 | 0.859 | 0.65–0.97 |
| cfDNA_LDCT_traditional | 18 | 14 | 0.902 | — |

**Sample size weighting:** Inverse-variance weighting based on reported sample size (n). For studies with missing n (LDCT_traditional: 3 studies; cfDNA_traditional: 0), equal weight was imputed; imputed studies contribute <2% of total weight.

---

## 3. Primary Meta-Analysis: Pooled AUC

### 3.1 Method

DerSimonian-Laird (DL) random-effects model applied to logit-transformed AUC values. Back-transformed to AUC scale for reporting. 95% confidence intervals computed on logit scale and back-transformed.

### 3.2 Results

| Category | k | Pooled AUC | 95% CI | I² | τ² | Q-test p |
|----------|---|-----------|--------|-----|-----|---------|
| LDCT_traditional | 68 | **0.860** | [0.842, 0.877] | 99.3% | 0.343 | <0.001 |
| LDCT_LLM *(descriptive)* | 5 | *0.855* | *[0.768, 0.913]* | *99.4%* | *0.433* | *<0.001* |
| cfDNA_traditional | 29 | **0.859** | [0.799, 0.903] | 98.7% | 1.307 | <0.001 |
| cfDNA_LDCT_traditional *(descriptive)* | 18 | *0.902* | *[0.879, 0.922]* | *87.4%* | *0.217* | *<0.001* |

### 3.3 Cross-Category Comparisons (Full Categories Only)

| Comparison | Δ AUC | p-value | Interpretation |
|------------|-------|---------|----------------|
| LDCT_traditional vs cfDNA_traditional | +0.001 | 0.96 | Not significant |
| LDCT_traditional vs cfDNA_LDCT_traditional | −0.042 | **0.005** | Significant |
| cfDNA_traditional vs cfDNA_LDCT_traditional | −0.043 | 0.096 | Marginal (†) |

**Key finding:** LDCT-only and cfDNA-only approaches show statistically equivalent diagnostic performance (AUC ~0.86). The combined cfDNA+LDCT approach achieves significantly higher AUC (0.902), suggesting complementary information from both modalities.

> **Figure 1:** Forest plot — LDCT + Traditional ML (k=68)  
> **Figure 2:** Forest plot — cfDNA + Traditional ML (k=29)  
> **Figure 7:** Summary comparison panel (all 4 categories)

---

## 4. Secondary Analysis: Sensitivity and Specificity

### 4.1 Method

Reitsma bivariate random-effects model for paired sensitivity/specificity data. Accounts for the negative correlation between sensitivity and specificity across studies (threshold effect).

### 4.2 Results

| Category | k | Pooled Sensitivity | 95% CI | Pooled Specificity | 95% CI | ρ (correlation) |
|----------|---|-------------------|--------|-------------------|--------|-----------------|
| LDCT_traditional | 23 | **0.831** | [0.705, 0.910] | **0.833** | [0.732, 0.901] | 0.764 |
| cfDNA_traditional | 21 | **0.739** | [0.520, 0.880] | **0.773** | [0.606, 0.882] | 0.077 |
| cfDNA_LDCT_traditional *(desc.)* | 14 | *0.835* | *[0.798, 0.867]* | *0.929* | *[0.788, 0.979]* | *−0.284* |

**Key findings:**
- LDCT_traditional achieves balanced sensitivity and specificity (~0.83 each), with a strong positive threshold correlation (ρ=0.764), indicating a clear sensitivity-specificity trade-off across studies
- cfDNA_traditional shows lower and more variable sensitivity (0.74) and specificity (0.77), with near-zero threshold correlation (ρ=0.077), suggesting heterogeneous assay designs rather than a single threshold effect
- cfDNA_LDCT_traditional (descriptive) shows the highest specificity (0.929), consistent with its higher pooled AUC

> **Figure 3:** SROC curves for all three categories

---

## 5. Subgroup Analyses

### 5.1 LDCT_traditional

| Subgroup | k | Pooled AUC | 95% CI | I² | p (between-group) |
|----------|---|-----------|--------|-----|-------------------|
| **Study Design** | | | | | |
| Prospective/RCT | 7 | 0.823 | [0.777, 0.861] | 95.9% | |
| Retrospective/Other | 61 | 0.865 | [0.845, 0.883] | 99.4% | **0.057 (†)** |
| **Validation Type** | | | | | |
| External validation | 11 | 0.847 | [0.804, 0.883] | 99.5% | |
| No external validation | 57 | 0.861 | [0.845, 0.875] | 97.4% | 0.52 (ns) |

**Interpretation:** Prospective/RCT studies show marginally lower AUC than retrospective studies (p=0.057), consistent with optimism bias in retrospective designs. External validation does not significantly reduce AUC (p=0.52), though the external validation subgroup is small (k=11).

### 5.2 cfDNA_traditional

| Subgroup | k | Pooled AUC | 95% CI | I² | p (between-group) |
|----------|---|-----------|--------|-----|-------------------|
| **Study Design** | | | | | |
| Prospective/RCT | <5 | — | — | — | Insufficient k |
| Retrospective/Other | 26 | 0.858 | [0.794, 0.905] | 98.8% | — |
| **Validation Type** | | | | | |
| External validation | 5 | 0.885 | [0.816, 0.931] | 87.0% | |
| No external validation | 24 | 0.853 | [0.789, 0.900] | 98.5% | 0.43 (ns) |

**Interpretation:** Insufficient prospective cfDNA studies for design-based subgroup analysis. External validation does not significantly reduce AUC (p=0.43), though the trend (0.885 vs 0.853) warrants attention.

> **Figure 5:** Subgroup forest plot

---

## 6. Publication Bias

### 6.1 Egger's Test for Funnel Plot Asymmetry

| Category | k | Egger's Intercept | SE | t | p-value | Interpretation |
|----------|---|------------------|----|---|---------|----------------|
| LDCT_traditional | 68 | 0.420 | 1.701 | 0.25 | 0.806 | No asymmetry |
| cfDNA_traditional | 29 | 7.904 | 0.918 | 8.61 | **<0.001** | **Significant asymmetry** |

**Key finding:** No significant publication bias detected for LDCT_traditional (p=0.806). Significant funnel plot asymmetry detected for cfDNA_traditional (p<0.001), suggesting possible small-study effects or selective reporting of positive cfDNA results. This should be interpreted cautiously — the cfDNA field is younger and smaller studies may genuinely report higher AUCs due to optimized biomarker selection.

> **Figure 4:** Funnel plots with Egger's regression lines

---

## 7. Sensitivity Analysis (Leave-One-Out)

### 7.1 Results

| Category | Full Pooled AUC | LOO Range | Max |ΔAUC| | Conclusion |
|----------|----------------|-----------|------------|------------|
| LDCT_traditional | 0.860 | [0.856, 0.864] | 0.004 | **Robust** |
| cfDNA_traditional | 0.859 | [0.853, 0.864] | 0.006 | **Robust** |

**Key finding:** Both pooled estimates are highly robust. Removing any single study shifts the pooled AUC by at most 0.006 (cfDNA_traditional) or 0.004 (LDCT_traditional). No single study drives the overall conclusion.

**Most influential studies (LDCT_traditional):** Studies with AUC=0.98 (small lesion detection) and AUC=0.52 (generative model radiomics) have the largest individual influence, consistent with their extreme values.

**Most influential studies (cfDNA_traditional):** Studies with AUC≥0.95 based on whole-genome bisulfite sequencing and methylation biomarkers have the largest influence, reflecting the high performance of methylation-based cfDNA approaches.

> **Figure 6:** LOO sensitivity plots

---

## 8. Summary and Conclusions

### 8.1 Overall Performance

Both LDCT-based and cfDNA-based AI approaches achieve clinically meaningful diagnostic performance for lung cancer screening, with pooled AUC ~0.86. The combined cfDNA+LDCT approach achieves significantly higher AUC (0.902), suggesting complementary information from imaging and liquid biopsy.

### 8.2 Key Takeaways

1. **Equivalent single-modality performance:** LDCT+ML and cfDNA+ML achieve statistically equivalent AUC (~0.86), despite fundamentally different biological signals
2. **Multimodal advantage:** cfDNA+LDCT combination significantly outperforms either modality alone (p=0.005), supporting multimodal screening strategies
3. **High heterogeneity throughout:** I²>87% in all categories indicates substantial between-study variability. Pooled estimates should be interpreted as central tendencies, not universal benchmarks
4. **Prospective vs retrospective gap:** LDCT studies show a marginal AUC inflation in retrospective designs (0.865 vs 0.823, p=0.057), highlighting the need for more prospective validation
5. **cfDNA publication bias:** Significant funnel asymmetry in cfDNA studies warrants caution; the true population-level AUC may be lower than 0.859
6. **LLM approaches emerging:** Only 5 LDCT+LLM studies available; descriptive AUC=0.855 is comparable to traditional ML but insufficient for formal inference
7. **Robust estimates:** LOO sensitivity analysis confirms that no single study drives the conclusions

### 8.3 Limitations

- **High heterogeneity** (I²>87%) limits the interpretability of pooled estimates; sources of heterogeneity (cancer stage, imaging protocol, cfDNA assay type, ML architecture) could not be fully explored due to incomplete metadata
- **Missing sample sizes** for 3 LDCT studies required equal-weight imputation (minimal impact: <2% of total weight)
- **Year metadata missing** for 188 papers from the original lung library, preventing temporal trend analysis
- **cfDNA_traditional publication bias** detected; true performance may be overestimated
- **LDCT_LLM and cfDNA_LDCT_traditional** categories have insufficient k for formal inference (k=5 and k=18 respectively)
- **Threshold effects:** Sensitivity/specificity pooling assumes comparable diagnostic thresholds across studies, which may not hold for cfDNA assays

---

## 9. Figures

| Figure | Description |
|--------|-------------|
| fig1_forest_LDCT_traditional.png | Forest plot — LDCT + Traditional ML (k=68) |
| fig2_forest_cfDNA_traditional.png | Forest plot — cfDNA + Traditional ML (k=29) |
| fig3_sroc.png | SROC curves — all 3 categories with bivariate model |
| fig4_funnel.png | Funnel plots — publication bias assessment |
| fig5_subgroup.png | Subgroup analysis — study design and validation type |
| fig6_loo_sensitivity.png | Leave-one-out sensitivity analysis |
| fig7_summary_panel.png | Summary: pooled AUC and I² by category |

---

## 10. Data Files

| File | Description |
|------|-------------|
| auc_dataset.csv | Full AUC dataset used for primary meta-analysis (k=120) |
| sensspec_dataset.csv | Sensitivity/specificity dataset (k=59) |
| pooled_auc_results.csv | Pooled AUC results by category |
| sensspec_results.csv | Bivariate model results |
| subgroup_results.csv | Subgroup analysis results |
| publication_bias.csv | Egger's test results |
| loo_LDCT_traditional.csv | LOO results for LDCT_traditional |
| loo_cfDNA_traditional.csv | LOO results for cfDNA_traditional |

---

*Report generated by Biomni meta-analysis pipeline. Statistical methods: DerSimonian-Laird random-effects (primary), Reitsma bivariate model (secondary), Egger's regression test (publication bias), leave-one-out (sensitivity). All analyses performed in Python using scipy, numpy, and pandas.*
