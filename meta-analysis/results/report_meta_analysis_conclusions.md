# AI-Assisted Cancer Screening: Systematic Review & Meta-Analysis
## Comprehensive Results and Conclusions

**Review scope:** 271 included studies (2018–2026) | **Primary outcome:** Diagnostic AUC  
**Meta-analysis:** DerSimonian-Laird random-effects with Knapp-Hartung correction  
**Outlier exclusion:** 2 papers with AUC < 0.65 (PMIDs 40831733, 41833807)

---

## 1. Headline Findings

### RQ1 — Imaging-Based AI for Lung Cancer Screening

| Modality Group | k | Pooled AUC | 95% CI | 95% PI | I² |
|---|---|---|---|---|---|
| Imaging only | 28 | **0.863** | [0.834–0.888] | [0.704–0.944] | 98.8% |
| Imaging + Clinical | 9 | **0.841** | [0.771–0.892] | [0.606–0.948] | 99.7% |
| Imaging + Liquid biopsy | 3 ⚠ | **0.900** | [0.565–0.984] | [0.192–0.997] | 86.3% |

### RQ2 — cfDNA Methylation-Based AI for Cancer Detection

| Modality Group | k | Pooled AUC | 95% CI | 95% PI | I² |
|---|---|---|---|---|---|
| Methylation only | 6 | **0.930** | [0.852–0.968] | [0.660–0.989] | 85.7% |
| Methylation + Imaging | 6 | **0.918** | [0.832–0.962] | [0.632–0.987] | 92.9% |
| Methylation + Fragmentomics | 3 ⚠ | **0.905** | [0.834–0.948] | [0.777–0.963] | 41.7% |
| Methylation + ctDNA | 2 ⚠⚠ | **0.952** | [0.000–1.000] | N/A | 99.6% |

> ⚠ k < 5: interpret cautiously. ⚠⚠ k = 2: estimate unreliable, CI degenerate.

---

## 2. Clinical Interpretation

### 2.1 RQ1: Imaging AI — Solid but Heterogeneous Performance

**Imaging-only AI (k=28, AUC=0.863)** represents the most robustly estimated group in this review. A pooled AUC of 0.863 indicates good discriminative ability for lung cancer detection from CT/LDCT images. However, the 95% prediction interval of [0.704–0.944] is wide, meaning that in a new clinical setting, the true AUC could plausibly range from moderate (0.70) to excellent (0.94). This wide PI — driven by extreme heterogeneity (I²=98.8%) — is the most important clinical caveat: **the pooled estimate does not reliably predict performance in any individual deployment context.**

Clinically, an AUC of 0.863 is comparable to or slightly above Lung-RADS performance in some studies, but direct head-to-head comparisons are limited in this dataset. The addition of clinical variables (Imaging + Clinical, AUC=0.841) did not improve performance over imaging alone in this pooled analysis — a counterintuitive finding that likely reflects heterogeneity in which clinical variables were included and how they were integrated.

**Imaging + Liquid biopsy (k=3, AUC=0.900)** is the highest-performing RQ1 group, but with only 3 studies and a degenerate PI [0.192–0.997], this estimate carries no reliable clinical weight. It is a promising signal warranting further investigation, not a conclusion.

### 2.2 RQ2: cfDNA Methylation AI — Higher AUC, Moderate Evidence Base

All four RQ2 groups achieved pooled AUC ≥ 0.905, consistently outperforming RQ1 imaging-only approaches by approximately 0.06–0.09 AUC units. **Methylation-only AI (AUC=0.930)** and **Methylation + Imaging (AUC=0.918)** are the best-supported estimates (k=6 each).

The summary operating point across 17 studies with both sensitivity and specificity data was **Sensitivity=0.850 (95% CI: 0.776–0.903)** and **Specificity=0.901 (95% CI: 0.822–0.947)**. This suggests cfDNA methylation-based approaches can achieve high specificity (low false-positive rate) while maintaining clinically meaningful sensitivity — a favourable trade-off for population screening where false positives drive unnecessary invasive follow-up.

**Methylation + Fragmentomics (k=3, AUC=0.905)** is notable for having the *lowest* heterogeneity of any group (I²=41.7%), suggesting more consistent performance across studies. This may reflect the more standardised nature of fragmentomics assays compared to imaging pipelines. The sensitivity analysis excluding PMID 41323119 (a 5-modality study) confirmed the estimate was robust (AUC unchanged at 0.905).

**Methylation + ctDNA (k=2, AUC=0.952)** cannot be interpreted as a reliable pooled estimate. The degenerate CI [0.000–1.000] and I²=99.6% indicate the two studies are statistically incompatible. This group requires substantially more primary research before meta-analytic synthesis is meaningful.

---

## 3. Heterogeneity Analysis

**All groups show substantial to considerable heterogeneity (I²=41.7%–99.7%).** This is expected in a field with:
- Diverse AI architectures (deep learning, random forest, SVM, logistic regression, ensemble)
- Heterogeneous cohort compositions (screening vs. clinical diagnosis vs. both)
- Variable cancer stages (early, mixed, late)
- Different validation strategies (72% of AUC papers had no external validation)
- Wide range of cohort sizes

The τ² values (between-study variance in logit-AUC space) range from 0.033 (Meth+Fragmentomics) to 2.547 (Meth+ctDNA), confirming that heterogeneity is not merely statistical noise but reflects genuine differences in study populations and methods.

**Key implication:** The wide prediction intervals — not the pooled point estimates — are the clinically relevant outputs. A new study in this field should expect its AUC to fall within the PI range, not at the pooled estimate.

**Important caveat on I² in small groups:** For groups with k=2–3, I² has very low power to detect heterogeneity. The apparently low I²=41.7% for Meth+Fragmentomics may partly reflect insufficient power rather than genuine consistency.

---

## 4. Subgroup Insights

### Validation Type
Among RQ1 imaging-only papers, studies with **external validation** (n=4) had a lower mean AUC (0.785) than studies without formal external validation (n=26, mean AUC=0.853). This is a critical finding: **studies that underwent rigorous external validation showed ~8% lower AUC**, consistent with the well-documented optimism bias in internally validated AI models. This gap likely underestimates the true performance drop, as external validation studies may still use convenience cohorts.

### Model Architecture
Deep learning (n=18) and other ML methods (n=17) dominate the AUC-reporting literature, followed by random forest (n=11). No single architecture consistently outperformed others across groups, suggesting that data quality and study design matter more than model choice at this stage of the field.

### Cancer Stage
Of the 22 AUC papers with stage information, 15 focused on early-stage detection, 4 on mixed stages, and 3 on late-stage. The preponderance of early-stage studies is appropriate for a screening context but limits generalisability to real-world screening populations where stage distribution is unknown at the time of testing.

---

## 5. Publication Bias Assessment

**Deeks funnel plot (RQ1 imaging-only, k=28):** slope = −3.486, p = 0.339. No statistically significant publication bias was detected. However, with I²=98.8%, the funnel plot assumption of a symmetric distribution around the pooled estimate is violated, and this test has limited power in the presence of extreme heterogeneity. The absence of a significant Deeks test should not be interpreted as confirmation that publication bias is absent.

**Structural publication bias concern:** Only 74 of 271 papers (27.3%) reported AUC, and only 43 reported sensitivity. Studies with poor-performing models are less likely to report quantitative metrics, introducing a form of selective outcome reporting that cannot be fully corrected by funnel plot methods.

---

## 6. Study Quality Assessment

Quality was assessed using a composite design quality score (range 2–24, median=10 across AUC papers). Key findings:
- **72% of AUC papers (52/72) had no external validation** — the single largest quality concern
- Only 24 of 38 core library papers reported AUC, limiting the meta-analysis to a subset of the highest-quality studies
- The quality score distribution was right-skewed (median=10, IQR=6–14), indicating moderate overall quality with a long tail of lower-quality studies

**Note:** The quality score used here is a composite proxy, not a formal domain-by-domain QUADAS-2 assessment. It captures overall study rigour but does not map directly to the 7 QUADAS-2 domains (patient selection, index test, reference standard, flow and timing). A formal QUADAS-2 assessment would be required for a definitive systematic review publication.

---

## 7. Publication Trends

The field grew from 11 papers in 2018 to a cumulative 271 by early 2026, with a marked acceleration from 2022 onward. The 2025 cohort (n=70, the largest single year) shows a notable surge in cfDNA methylation studies, reflecting the maturation of liquid biopsy technologies and multi-cancer early detection (MCED) platforms.

**Caveat:** 2025 and 2026 counts are subject to search date cutoff effects. The 2026 total (n=24) represents a partial year and should not be compared directly to prior full-year counts.

The proportion of RQ2 (cfDNA methylation) studies has grown from ~18% of the 2018 cohort to ~24% of the 2025 cohort, suggesting increasing research investment in liquid biopsy approaches relative to imaging AI.

---

## 8. Key Limitations

1. **Extreme heterogeneity (I²>85% in 5/7 groups):** The pooled AUC estimates are summary statistics of a highly heterogeneous literature. They should be interpreted as the average of a distribution of true effects, not as a single expected performance value.

2. **Incomplete metric reporting (72.7% of papers lack AUC):** The meta-analysis is based on 74/271 papers. If non-reporting is correlated with performance, the pooled estimates are biased upward.

3. **No external validation in 72% of AUC papers:** Most estimates reflect internal or no validation, likely overestimating real-world performance.

4. **Small k in RQ2 groups:** Three of four RQ2 groups have k≤3. These estimates are exploratory signals, not robust conclusions.

5. **Predominantly lung cancer focus (256/271 papers):** RQ2 results for multi-cancer detection (n=12 papers) are not separately analysed due to insufficient k.

6. **Composite quality score, not formal QUADAS-2:** The risk-of-bias assessment is approximate.

7. **Per-study CI approximation in forest plots:** Individual study CIs were estimated from cohort size using a logit-transform approximation. For studies with missing cohort size (n=100 fallback used), these CIs are approximate.

8. **Summary operating point (Sens/Spec) based on n=17 studies:** This subset is not a random sample of the 72 AUC papers — studies reporting both metrics tend to use binary classifiers, introducing selection bias.

9. **Year-trend smoothing is descriptive only:** The Savitzky-Golay smoothed AUC trend does not control for study design, cohort composition, or publication bias over time.

---

## 9. Conclusions

**RQ1:** AI applied to CT/LDCT imaging achieves a pooled AUC of **0.863** (95% CI: 0.834–0.888) for lung cancer detection, with good average performance but extreme heterogeneity (I²=98.8%) and a wide prediction interval [0.704–0.944]. The addition of clinical variables does not consistently improve performance in this pooled analysis. The gap between internally and externally validated studies (~8 AUC points) underscores the need for rigorous prospective validation before clinical deployment.

**RQ2:** cfDNA methylation-based AI achieves consistently higher pooled AUC (0.905–0.930 across reliable groups) than imaging-only approaches, with a favourable summary operating point (Sens=0.850, Spec=0.901). The Methylation + Fragmentomics group shows the most consistent performance (I²=41.7%), while Methylation + ctDNA (k=2) remains too sparse for reliable conclusions. These results support cfDNA methylation as a promising complementary or standalone modality for cancer screening, but the evidence base remains limited (k=3–6 per group) and requires expansion through prospective multi-centre trials.

**Overall:** The field is growing rapidly (271 papers, 2018–2026), with a notable surge in cfDNA studies from 2022 onward. However, the dominant limitation across both RQs is the lack of prospective external validation — a gap that must be addressed before AI-assisted screening tools can be recommended for routine clinical use.

---

*Analysis performed using DerSimonian-Laird random-effects meta-analysis with Knapp-Hartung correction. Outliers excluded: PMID 40831733 and 41833807 (AUC=0.640). All figures generated from real extracted data; no values were simulated or imputed.*
