# 📚 Survey Paper — Lung Cancer Screening Literature Support Library

> **Research Question:** In lung cancer screening, how does LDCT / routine physical exam multimodal / AI model performance compare with cfDNA methylation-based multi-cancer early detection (MCED)?

---

## 🎯 Scope & Inclusion Criteria

| Field | Value |
|-------|-------|
| **Search database** | PubMed |
| **Date range** | 2018–2026 |
| **Language** | English only |
| **Papers searched** | 500 |
| **Papers included** | 271 (54.2%) |
| **Core library** | 38 papers (score ≥ 50) |
| **Last updated** | 2026-04-15 |

**Inclusion:** Original research; reports AUC / sensitivity / specificity; related to screening, early detection, risk assessment, or multimodal fusion.

**Exclusion:** Pure reviews, systematic reviews, meta-analyses, non-cancer screening, non-human studies, no performance metrics.

---

## 📂 Repository Structure

```
survey-paper/
├── README.md                          # This file
├── schema.json                        # Complete field definitions
├── data/
│   ├── raw_search_results.json        # 500 raw PubMed records
│   ├── filer_results.json             # 500 papers with include/exclude decisions
│   ├── extracted_fields.json          # 271 included papers, 13 extracted fields
│   ├── scored_results.json            # 271 papers with 5-dimension scores
│   ├── full_library.json              # 271 papers, all fields merged
│   └── tsv/
│       ├── all_papers.tsv             # All 500 papers (filer fields)
│       ├── included_papers.tsv        # 271 included papers (all fields)
│       ├── core_library.tsv           # 38 core papers (score ≥ 50)
│       ├── cat1_cfdna_methylation_mced.tsv
│       ├── cat2_single_modality_screening.tsv
│       ├── cat3_physical_exam_traditional_model.tsv
│       ├── cat4_physical_exam_ai_model.tsv
│       └── cat5_methylation_multimodal.tsv
└── categories/
    ├── cat1_cfdna_methylation_mced.md
    ├── cat2_single_modality_screening.md
    ├── cat3_physical_exam_traditional_model.md
    ├── cat4_physical_exam_ai_model.md
    └── cat5_methylation_multimodal.md
```

---

## 🗂️ Categories

| # | Category | Papers | Core |
|---|----------|--------|------|
| 1 | [cfDNA Methylation & MCED](categories/cat1_cfdna_methylation_mced.md) | 27 | 3 |
| 2 | [Single-Modality Screening (LDCT/Imaging)](categories/cat2_single_modality_screening.md) | 77 | 5 |
| 3 | [Physical Exam + Traditional Model](categories/cat3_physical_exam_traditional_model.md) | 9 | 2 |
| 4 | [Physical Exam / Imaging + AI Model](categories/cat4_physical_exam_ai_model.md) | 120 | 19 |
| 5 | ⭐ [Methylation + Multimodal Integration](categories/cat5_methylation_multimodal.md) | 38 | 9 |

---

## 📋 Field Schema

### Filer Fields (all 500 papers)
| Field | Type | Description |
|-------|------|-------------|
| `pmid` | string | PubMed ID |
| `title` | string | Paper title |
| `abstract` | string | Full abstract |
| `doi` | string\|null | DOI |
| `journal` | string | Journal name |
| `pub_year` | integer | Publication year |
| `authors` | list | Author list |
| `cancer_type` | string | lung / multi_cancer / other |
| `modality` | string | Primary modality |
| `task_type` | string | screening / diagnosis / risk_assessment / early_detection |
| `include_decision` | boolean | true = passes inclusion criteria |
| `exclusion_reason` | string\|null | Reason if excluded |
| `probable_relevance_score` | float 0–1 | Estimated relevance |

### Extraction Fields (271 included papers)
| Field | Type | Description |
|-------|------|-------------|
| `study_design` | string | RCT / prospective_cohort / retrospective_cohort / case_control / cross_sectional / other |
| `screening_or_clinical` | string | screening / clinical_diagnosis / both |
| `cohort_size` | integer\|null | Total participants |
| `cancer_type` | string | lung / multi_cancer / other |
| `stage_info` | string\|null | early / late / mixed |
| `input_modalities` | list | cfDNA_methylation / LDCT / CT / blood_protein / clinical_features / imaging / other |
| `model_type` | string\|null | deep_learning / logistic_regression / Cox / SVM / random_forest / ensemble / other |
| `comparator` | string\|null | Description of comparison arm |
| `auc` | float\|null | Area under ROC curve (0–1) |
| `sensitivity` | float\|null | Sensitivity (0–1) |
| `specificity` | float\|null | Specificity (0–1) |
| `validation_type` | string | internal_CV / external_validation / prospective / none |
| `key_limitations` | string\|null | Key study limitations |

### Scoring Fields (271 included papers)
| Field | Max | Description |
|-------|-----|-------------|
| `relevance` | 25 | Direct relevance to lung cancer screening / cfDNA / MCED / LDCT / AI |
| `design_quality` | 25 | Study design quality (design type + sample size + validation) |
| `metric_comparability` | 20 | Completeness of AUC/sensitivity/specificity reporting |
| `generalizability` | 15 | Multi-center / external validation / population representativeness |
| `impact` | 15 | Journal tier / landmark study status / recency |
| `total_score` | 100 | Sum of all dimensions |
| `core_library` | bool | true if total_score ≥ 50 |
| `category` | string | One of 5 category keys |

> **Note on scoring:** Scores are derived from abstract text only (full-text unavailable via API). Metric fields (AUC/sensitivity/specificity) have ~15–25% abstract extraction coverage; values in full text are marked `null` but the paper is not penalized. The `core_library` threshold of 50/100 is calibrated for abstract-only scoring.

---

## 🔍 Search Strategies

Six complementary PubMed queries (2018–2026, English, human studies):

1. **cfDNA methylation:** `(cfDNA OR "cell-free DNA") AND methylation AND ("lung cancer") AND (screening OR detection) AND (AUC OR sensitivity OR specificity)`
2. **LDCT + AI:** `(LDCT OR "low-dose CT") AND ("lung cancer") AND ("artificial intelligence" OR "deep learning" OR "machine learning" OR multimodal) AND (screening OR detection)`
3. **MCED:** `("multi-cancer early detection" OR MCED) AND (methylation OR cfDNA) AND ("lung cancer" OR lung)`
4. **Physical exam + model:** `("physical examination" OR "health checkup") AND ("lung cancer") AND ("risk model" OR "prediction model") AND (screening OR detection)`
5. **Checkup + broad:** `("lung cancer") AND ("risk prediction" OR "risk stratification") AND ("clinical features" OR "biomarker") AND (screening OR "early detection")`
6. **Methylation + multimodal:** `(methylation OR "cfDNA methylation") AND ("lung cancer") AND (multimodal OR "multi-omics" OR "liquid biopsy" OR imaging) AND (screening OR detection)`

---

## ⚠️ Limitations

- **Abstract-only extraction:** Numeric metrics (AUC, sensitivity, specificity) extracted from abstracts only; ~75% of values are in full text and marked `null`.
- **Rule-based pipeline:** Filer, extraction, and scoring use regex/rule-based logic, not LLM. Manual review of core library papers is recommended before citation.
- **Category assignment:** Based on abstract signals; papers with ambiguous modality descriptions may be miscategorized.
- **No full-text access:** Study design, cohort size, and validation type may be underreported.

---

*Generated by Biomni automated literature pipeline · 2026-04-15*
