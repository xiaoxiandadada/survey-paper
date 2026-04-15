# Analysis Plan: AI-Assisted Lung Cancer and Multi-Cancer Early Detection — Systematic Review & Meta-Analysis

**Version:** 1.0  
**Date:** 2026-04-15  
**Reporting standard:** PRISMA-DTA 2023  
**Target journal:** Top-tier (IF > 10, e.g. Lancet Digital Health / JAMA Network Open / Radiology)  
**Note:** PROSPERO pre-registration recommended before executing final analysis.

---

## 1. Overview

One paper, three research questions (RQ) as sub-analyses:

| RQ | Question | Analysis |
|----|----------|----------|
| RQ1 | Single-modal imaging AI vs multi-modal fusion AI for lung cancer screening | Quantitative meta-analysis |
| RQ2 | cfDNA methylation alone vs combined modalities | Quantitative meta-analysis |
| RQ3 | Deep learning + cfDNA methylation: evidence and future directions | Narrative review |

**Data basis** (`data/tsv/included_papers.tsv`):
- Total papers: 271 (core_library = True: 38)
- Papers with AUC: 67; with AUC + sensitivity + specificity: 14
- Papers with external validation: 40

---

## 2. Eligibility Criteria

### Inclusion (all RQs)
- Adults undergoing lung cancer screening or early detection
- Intervention: AI/ML model OR cfDNA methylation assay (including combinations)
- Outcome: at least one of AUC, sensitivity, specificity reported
- Language: English; publication years: 2018–2026

### Exclusion
- Narrative reviews, editorials, commentaries (no primary data)
- Late-stage / metastatic lung cancer treatment outcomes only
- No extractable diagnostic performance metrics
- Animal or in vitro studies

---

## 3. QUADAS-2 Risk of Bias Assessment

### Scope
- **Full QUADAS-2**: 38 core-library papers (core_library = True), all four domains
- **Score-mapped**: remaining 233 papers, design_quality → risk level

### Domain definitions and mapping rules

| Domain | Assesses | LOW | HIGH | UNCLEAR |
|--------|----------|-----|------|---------|
| D1: Patient selection | Consecutive/random enrolment; case-control design | prospective_cohort or RCT, n ≥ 100 | case_control | otherwise |
| D2: Index test | Pre-specified threshold; blinding | No post-hoc threshold in key_limitations | Post-hoc threshold mentioned | key_limitations missing |
| D3: Reference standard | Adequate gold standard (pathology vs imaging follow-up) | task_type = diagnosis, stage ≠ late | task_type = screening, no pathology confirmation | otherwise |
| D4: Flow and timing | All patients same reference standard; time interval | external_validation | none + retrospective_cohort | otherwise |

### Score-to-risk mapping (non-core papers)
- design_quality ≥ 18 → Low risk
- design_quality 12–17 → Unclear risk
- design_quality < 12 → High risk

**Output:** QUADAS-2 traffic-light heatmap (Fig 2), `quadas2_ratings.csv`

---

## 4. RQ1 — AI Models for Lung Cancer Screening

### Research question
Do single-modal imaging AI models (CT/LDCT only) and multi-modal fusion AI models
(CT + clinical features, or CT + liquid biopsy) differ in diagnostic accuracy?

### Study groups

| Group | Definition | n total | n with AUC | n ext. validated |
|-------|-----------|---------|------------|-----------------|
| imaging_only | model_type ∈ {deep_learning, other_ML} AND input_modalities ⊆ {LDCT, CT, imaging} | 76 | 19 | 6 |
| imaging+clinical | above + clinical_features, no liquid biomarker | 13 | 3 | 5 |
| imaging+liquid | above + any of cfDNA/ctDNA/blood_protein/miRNA/proteomics | 31 | 9 | 7 |

### Primary analysis: AUC random-effects meta-analysis
- **Model:** DerSimonian-Laird random-effects (`metafor::rma()`)
- **Effect measure:** logit(AUC); back-transformed for reporting
- **Variance:** `vi = 1/(n_cases × AUC × (1−AUC))` when SE not reported (flagged as `var_approx = TRUE`)
- **CI:** 95%, Knapp-Hartung correction (small-sample robustness)
- **Heterogeneity:** I², τ² (REML), Cochran's Q
- **Group comparison:** meta-regression with modality group as moderator

### Sensitivity/specificity pooling (conditional)
- Execute bivariate random-effects model (`mada::reitsma()`) only when n ≥ 4 studies
  have both sensitivity AND specificity in a group
- Current data: imaging+liquid has n=3 (below threshold); execute if updated data reaches n=4
- Output: pooled sensitivity, pooled specificity, SROC curve, AUC_SROC

### Subgroup analyses (both mandatory)

| Subgroup | Levels | Expected n (with AUC) |
|----------|--------|-----------------------|
| Validation type | External validation vs No external validation | 16 vs 51 |
| Application setting | Screening vs Clinical diagnosis vs Both/mixed | 10 vs 26 vs 31 |

Method: `rma(mods = ~factor(subgroup_var))`, report within-group pooled AUC and between-group Q-test p-value.

### Publication bias
- **Method:** Deeks funnel plot asymmetry test (uses inverse effective sample size as precision)
- **Condition:** n ≥ 10 studies (imaging_only group qualifies)
- **Fallback:** Egger's test via `metafor::regtest()` when raw 2×2 data unavailable

### Outputs
- Fig 3: Three-group AUC forest plot (layered)
- Fig 4: Validation-type subgroup forest plot
- Fig 5: Application-setting subgroup forest plot
- Fig 6: Deeks funnel plot (imaging_only)
- Fig 7: SROC curve (conditional)
- `rq1_summary_stats.csv`

---

## 5. RQ2 — cfDNA Methylation Combinations

### Research question
Does combining cfDNA methylation with other modalities (imaging, fragmentomics, ctDNA)
improve diagnostic accuracy over methylation alone? Which combination performs best?

### Study groups

| Group | Definition | n total | n with AUC | n with AUC+S+S |
|-------|-----------|---------|------------|----------------|
| meth_only | input_modalities = 'cfDNA_methylation' (no pipe) | 33 | 7 | 4 |
| meth+imaging | cfDNA_methylation + LDCT/CT | 11 | 5 | — |
| meth+fragmentomics | cfDNA_methylation + cfDNA_fragmentomics | 11 | 4 | — |
| meth+ctDNA | cfDNA_methylation + ctDNA | 7 | 1 | — (narrative only) |

### Primary analysis
Same DerSimonian-Laird + Knapp-Hartung approach as RQ1.

**Two core comparisons:**
1. Combined vs solo: meta-regression with `is_combo` as binary moderator
2. meth+imaging vs meth+fragmentomics: descriptive comparison of pooled AUCs
   (no statistical test if n < 5 per group)

### Sensitivity/specificity pooling
- meth_only: n=4 with AUC+S+S → execute bivariate model (note n=4 limitation in Methods)
- Combined subgroups: n ≤ 5 → report point estimates only, no SROC

### Subgroup analyses
Same two mandatory subgroups as RQ1 (validation type + application setting).

### Outputs
- Fig 8: Solo vs combined AUC forest plot
- Fig 9: Bubble plot — AUC by combination type (bubble size = cohort size)
- Fig 10: SROC curve — methylation-only group
- `rq2_summary_stats.csv`

---

## 6. RQ3 — Deep Learning + cfDNA Methylation (Narrative Review)

### Research question
How does deep learning enhance cfDNA methylation-based lung cancer detection?
What are the current technical approaches and limitations?

### Rationale for narrative approach
Only 6 studies meet criteria (cfDNA_methylation + deep_learning model_type).
This is below the minimum threshold of 5 studies for quantitative pooling.

### Included studies (n=6)

| PMID | Year | Architecture | AUC | Validation |
|------|------|-------------|-----|------------|
| 41323119 | 2025 | CNN + clinical fusion | 0.950 | External |
| 39380154 | 2024 | Transformer + MIL | 0.910 | None |
| 37598236 | 2023 | Deep learning | 0.956 | None |
| 35600397 | 2022 | Deep learning | — | None |
| 38926407 | 2024 | CNN (fragment size) | — | None |
| 38961476 | 2024 | Graph CNN (GCN) | — | None |

### Narrative structure
1. **Architecture taxonomy:** CNN / Transformer / GCN / MIL — use cases
2. **Input feature strategies:** genome-wide vs targeted panel vs fragmentomics fusion
3. **Performance summary:** 3 studies with AUC (0.910–0.956); validation status noted
4. **Limitations:** small cohorts (max n=5,389), lack of external validation, interpretability
5. **Future directions:** foundation models (RAD-DINO, BioViL) applied to methylation data

### Output
- Table 3: structured summary of 6 studies
- `fig_rq3_table3.png`

---

## 7. Statistical Implementation

### Software
```r
# R 4.3+
library(metafor)   # rma() — random-effects AUC model
library(mada)      # reitsma(), deeks.test() — bivariate model + Deeks test
library(ggplot2)   # custom figures
library(dplyr)     # data wrangling
```

### AUC preprocessing
```r
# 1. Parse AUC to numeric (handle "0.95", ".95", "95%")
# 2. Logit transform: yi = log(AUC / (1 - AUC))
# 3. Variance: vi = 1 / (n_cases * AUC * (1 - AUC))  [approximation]
# 4. Exclude AUC = 0 or AUC = 1 (infinite variance)
```

### Heterogeneity interpretation

| I² | Interpretation |
|----|----------------|
| < 25% | Low |
| 25–50% | Moderate |
| 50–75% | High |
| > 75% | Very high (explore sources) |

### Meta-regression moderators (single-variable, avoid overfitting)

| Moderator | Type | Expected direction |
|-----------|------|--------------------|
| Modality group | Categorical | Multi-modal > single-modal |
| Validation type | Binary | External < none (optimism bias) |
| Application setting | Categorical | Clinical > screening (prevalence difference) |
| Publication year | Continuous | Recent > earlier (technology improvement) |

---

## 8. GRADE Evidence Grading

Applied to primary outcomes of RQ1 and RQ2.

- Starting level: observational studies → Low quality
- Upgrade/downgrade based on: consistency (I²), precision (CI width), directness (population match), risk of bias (QUADAS-2 summary)

---

## 9. Paper Structure

```
1. Introduction
2. Methods
   2.1 Protocol & Registration (PROSPERO)
   2.2 Search Strategy
   2.3 Eligibility Criteria
   2.4 Data Extraction (dual independent)
   2.5 Quality Assessment (QUADAS-2)
   2.6 Statistical Analysis
3. Results
   3.1 Study Selection (PRISMA-DTA flow, Fig 1)
   3.2 Study Characteristics (Table 1)
   3.3 Quality Assessment (QUADAS-2 traffic light, Fig 2)
   3.4 RQ1: AI Models (Figs 3–7)
   3.5 RQ2: cfDNA Methylation Combinations (Figs 8–10)
   3.6 RQ3: Deep Learning + Methylation (Table 3)
4. Discussion
   4.1 Summary of findings
   4.2 Sources of heterogeneity
   4.3 Evidence quality and limitations (GRADE)
   4.4 Clinical implications and future directions
5. Conclusion
```

---

## 10. Key Assumptions and Limitations

1. **Variance approximation:** `vi = 1/(n × AUC × (1−AUC))` underestimates true variance when SE is not reported; flagged as `var_approx = TRUE` in data files.
2. **RQ1 AUC+S+S scarcity:** Only 1–3 studies per group have all three metrics; bivariate HSROC not feasible; sensitivity/specificity pooling results require cautious interpretation.
3. **RQ3 narrative only:** 6 studies below the 5-study minimum for quantitative pooling.
4. **meth+ctDNA subgroup:** Only 1 study with AUC; narrative only.
5. **PROSPERO pre-registration:** Strongly recommended before executing final analysis.
6. **Dual independent extraction:** QUADAS-2 and data extraction require a second reviewer; target κ > 0.7.
7. **PRISMA-DTA screening counts:** Update `COUNTS` dict in `05_prisma_flow.py` with actual numbers from your screening log before submission.
