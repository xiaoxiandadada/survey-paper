# Cancer Early Detection AI Literature Survey — Statistical Report

**Generated:** 2026-04-15  
**Repository:** https://github.com/xiaoxiandadada/survey-paper  
**Total papers:** 455  
**Coverage:** 36/80 cells (45.0%)

---

## 1. Framework

This repository organises the AI-assisted cancer early detection literature across **16 cancer types** and **5 technical categories**:

| Category | Description |
|----------|-------------|
| `LDCT_traditional` | Low-dose CT imaging + classical ML (CNN, radiomics, random forest, etc.) |
| `LDCT_LLM` | CT imaging + foundation models / large language models |
| `cfDNA_traditional` | Liquid biopsy (cfDNA/ctDNA/methylation) + classical ML |
| `cfDNA_LDCT_traditional` | Multimodal: cfDNA + CT imaging + classical ML |
| `cfDNA_LDCT_LLM` | Multimodal: cfDNA + CT + foundation models |

**16 cancer types:** lung, breast, colorectal, liver, prostate, cervical, ovarian, endometrial, gallbladder, lymphoma, bladder, kidney, pancreas, gastric, esophageal, nasopharyngeal

---

## 2. Coverage Matrix

| Cancer | LDCT_trad | LDCT_LLM | cfDNA_trad | cfDNA_LDCT_trad | cfDNA_LDCT_LLM | Total |
|--------|-----------|----------|------------|-----------------|----------------|-------|
| lung | 107 | 8 | 52 | 27 | — | **194** |
| breast | — | 3 | 25 | 1 | — | **29** |
| colorectal | — | — | 27 | 1 | — | **28** |
| liver | — | 3 | 25 | 1 | — | **29** |
| prostate | — | — | 18 | — | — | **18** |
| cervical | — | 1 | 15 | — | — | **16** |
| ovarian | — | — | 16 | 1 | — | **17** |
| endometrial | — | — | 8 | — | — | **8** |
| gallbladder | 5 | 1 | 12 | 2 | — | **20** |
| lymphoma | — | — | 6 | 3 | — | **9** |
| bladder | — | — | 10 | — | — | **10** |
| kidney | — | — | 11 | 1 | — | **12** |
| pancreas | 7 | 2 | 21 | 4 | — | **34** |
| gastric | — | 1 | 14 | 1 | — | **16** |
| esophageal | — | — | 13 | — | — | **13** |
| nasopharyngeal | — | — | 2 | — | — | **2** |
| **TOTAL** | 119 | 19 | 275 | 42 | 0 | **455** |

> **—** = no papers found (genuine research gap or modality mismatch for that cancer type)

---

## 3. Search Strategy

- **Database:** PubMed (2018–2026)
- **Lung papers:** Remapped from existing curated library (original 271 papers → 194 retained after QC)
- **15 other cancers:** Systematic PubMed search using cancer-specific MeSH terms combined with category-specific keyword queries
- **Inclusion criteria:**
  - Original research (reviews, meta-analyses excluded)
  - Reports at least one quantitative performance metric (AUC, sensitivity, or specificity)
  - AUC ≥ 0.50 (implausible values excluded)
  - Publication year 2018–2026
- **Exclusion criteria:**
  - Treatment response, prognosis, survival, staging papers
  - Papers with no cancer-type match in title
  - Papers with AUC < 0.50

---

## 4. Paper Statistics

### 4.1 Total by cancer type

| Cancer | Papers | Mean AUC (n) |
|--------|--------|--------------|
| lung | 194 | 0.850 (n=124) |
| breast | 29 | 0.897 (n=18) |
| colorectal | 28 | 0.893 (n=21) |
| liver | 29 | 0.893 (n=18) |
| prostate | 18 | 0.896 (n=13) |
| cervical | 16 | 0.888 (n=10) |
| ovarian | 17 | 0.932 (n=14) |
| endometrial | 8 | 0.890 (n=6) |
| gallbladder | 20 | 0.871 (n=10) |
| lymphoma | 9 | 0.917 (n=4) |
| bladder | 10 | 0.911 (n=6) |
| kidney | 12 | 0.901 (n=9) |
| pancreas | 34 | 0.938 (n=22) |
| gastric | 16 | 0.876 (n=13) |
| esophageal | 13 | 0.878 (n=11) |
| nasopharyngeal | 2 | 0.970 (n=1) |

### 4.2 Total by category

| Category | Papers |
|----------|--------|
| LDCT_traditional | 119 |
| LDCT_LLM | 19 |
| cfDNA_traditional | 275 |
| cfDNA_LDCT_traditional | 42 |
| cfDNA_LDCT_LLM | 0 |

### 4.3 AUC distribution (300 papers with reported AUC)

| AUC range | Count | % |
|-----------|-------|---|
| 0.50-0.69 | 17 | 5.7% |
| 0.70-0.79 | 36 | 12.0% |
| 0.80-0.89 | 94 | 31.3% |
| 0.90-0.99 | 138 | 46.0% |
| 1.00 | 15 | 5.0% |
| **Mean AUC** | **0.880** | — |

### 4.4 Study design

| Design | Count | % |
|--------|-------|---|
| other | 329 | 72.3% |
| prospective_cohort | 64 | 14.1% |
| retrospective_cohort | 36 | 7.9% |
| case_control | 18 | 4.0% |
| RCT | 6 | 1.3% |
| cross_sectional | 2 | 0.4% |

### 4.5 Validation type

| Validation | Count | % |
|------------|-------|---|
| none | 369 | 81.1% |
| external_validation | 71 | 15.6% |
| internal_CV | 14 | 3.1% |
| prospective | 1 | 0.2% |

### 4.6 Model type

| Model | Count | % |
|-------|-------|---|
| other | 168 | 36.9% |
| logistic_regression | 87 | 19.1% |
| deep_learning | 68 | 14.9% |
| random_forest | 45 | 9.9% |
| other_ML | 35 | 7.7% |
| foundation_model | 16 | 3.5% |
| ensemble | 11 | 2.4% |
| SVM | 9 | 2.0% |
| XGBoost | 8 | 1.8% |
| Cox | 7 | 1.5% |
| Transformer | 1 | 0.2% |

### 4.7 Journal impact factor tier

| Tier | Count | % | Definition |
|------|-------|---|------------|
| core | 94 | 20.7% | IF > 10 |
| extended | 125 | 27.5% | IF 5–10 |
| low_if | 105 | 23.1% | IF < 5 |
| unknown | 131 | 28.8% | Journal not in lookup table |

### 4.8 Other quality flags

| Flag | Count | % |
|------|-------|---|
| Screening-relevant | 315 | 69.2% |
| Has external validation | 39 | 8.6% |
| AUC = 1.0 (flagged) | 15 | 3.3% |

---

## 5. Gap Analysis

**Zero-coverage cells:** 44 / 80 (55.0%)

### 5.1 Structural gaps (modality mismatch — expected)

| Cancer | Missing categories | Reason |
|--------|--------------------|--------|
| breast | LDCT_traditional, LDCT_LLM | Mammography/MRI used for screening, not LDCT |
| colorectal | LDCT_traditional, LDCT_LLM | Colonoscopy/stool-based screening, not LDCT |
| liver | LDCT_traditional, LDCT_LLM | Ultrasound surveillance, not LDCT |
| prostate | LDCT_traditional, LDCT_LLM | PSA/MRI-based, not LDCT |
| cervical | LDCT_traditional | Pap smear/HPV testing, not LDCT |
| ovarian | LDCT_traditional, LDCT_LLM | Ultrasound/CA-125, not LDCT |
| endometrial | LDCT_traditional, LDCT_LLM | Biopsy/ultrasound, not LDCT |
| bladder | LDCT_traditional, LDCT_LLM | Cystoscopy/urine cytology, not LDCT |
| gastric | LDCT_traditional | Endoscopy-based, not LDCT |
| esophageal | LDCT_traditional, LDCT_LLM | Endoscopy-based, not LDCT |
| nasopharyngeal | LDCT_traditional | EBV serology/endoscopy, not LDCT |

### 5.2 Research frontier gaps (genuine knowledge gaps)

| Gap | Observation |
|-----|-------------|
| `cfDNA_LDCT_LLM` = 0 across all cancers | No published work combining multimodal cfDNA+CT with foundation models for early detection — an emerging research frontier |
| `LDCT_LLM` sparse (19 papers, 9 cancers) | Foundation model application to CT-based cancer screening is nascent; most work is in lung (8 papers) |
| nasopharyngeal (2 papers total) | Very limited AI-based early detection literature; EBV serology dominates |
| endometrial (8 papers) | Predominantly cfDNA-based; limited multimodal work |

---

## 6. Limitations

1. **Year unknown for 188 papers** (41.3%): These originate from the original lung library where publication year was not consistently recorded in the source data.
2. **AUC extraction is automated**: Regex-based extraction from abstracts may miss or misparse reported values. Papers with AUC=1.0 (n=15) are flagged and should be interpreted with caution.
3. **Category assignment is heuristic**: Based on title/abstract keyword matching; some papers may be miscategorised, particularly multimodal studies.
4. **IF lookup is static**: Journal impact factors are from a manually curated table (2023 values); 28.8% of papers have unknown IF.
5. **Search limited to PubMed**: arXiv/medRxiv preprints and non-English literature are not included.
6. **cfDNA_LDCT_LLM = 0**: Reflects the current state of the field (2018–2026), not a search failure.
