# Cancer Early Detection AI — Literature Survey Repository

> A structured, machine-readable database of AI-assisted cancer early detection papers across **16 cancer types × 5 technical categories**.

**Last updated:** 2026-04-15 | **Total papers:** 455 | **Coverage:** 36/80 cells (45%)

---

## Repository Structure

```
survey-paper/
├── data/
│   ├── lung/
│   │   ├── LDCT_traditional/      # 107 papers
│   │   ├── LDCT_LLM/              #   8 papers
│   │   ├── cfDNA_traditional/     #  52 papers
│   │   ├── cfDNA_LDCT_traditional/#  27 papers
│   │   └── cfDNA_LDCT_LLM/        #   0 papers
│   ├── breast/
│   │   └── ...
│   └── [16 cancer type folders]
├── index.json              # Flat array of all 455 papers
├── coverage_matrix.json    # 16×5 matrix with counts, AUC stats, gap flags
├── coverage_report.md      # Full statistical report
└── schema.json             # JSON schema for individual paper files
```

---

## 5 Technical Categories

| Category | Description |
|----------|-------------|
| `LDCT_traditional` | Low-dose CT imaging + classical ML (CNN, radiomics, random forest, SVM, etc.) |
| `LDCT_LLM` | CT imaging + foundation models / large language models (GPT-4, SAM, vision-language models) |
| `cfDNA_traditional` | Liquid biopsy (cfDNA / ctDNA / methylation / fragmentomics) + classical ML |
| `cfDNA_LDCT_traditional` | Multimodal: cfDNA + CT imaging + classical ML |
| `cfDNA_LDCT_LLM` | Multimodal: cfDNA + CT + foundation models *(emerging frontier — 0 papers as of 2026)* |

---

## 16 Cancer Types

lung · breast · colorectal · liver · prostate · cervical · ovarian · endometrial · gallbladder · lymphoma · bladder · kidney · pancreas · gastric · esophageal · nasopharyngeal

---

## Coverage Matrix

| Cancer | LDCT_trad | LDCT_LLM | cfDNA_trad | cfDNA_LDCT_trad | cfDNA_LDCT_LLM | Total |
|--------|:---------:|:--------:|:----------:|:---------------:|:--------------:|------:|
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
| **TOTAL** | **119** | **19** | **275** | **42** | **0** | **455** |

> **—** = no papers (structural gap due to modality mismatch, or genuine research gap)

---

## Paper JSON Schema

Each paper is stored as an individual JSON file with the following fields:

```json
{
  "paper_id": "lung_cfDNA_traditional_001",
  "pmid": "12345678",
  "title": "...",
  "year": 2023,
  "journal": "Nature Communications",
  "doi": "10.1038/...",
  "cancer_type": "lung",
  "category": "cfDNA_traditional",
  "study_design": "prospective_cohort",
  "cohort_type": "screening",
  "sample_size": 1200,
  "input_modalities": ["cfDNA_methylation", "clinical_features"],
  "model_type": "random_forest",
  "performance_raw": {
    "auc": 0.921,
    "sensitivity": 0.847,
    "specificity": 0.912,
    "early_stage_sensitivity": 0.803
  },
  "has_stage_info": true,
  "validation_type": "external_validation",
  "notes": "...",
  "quality_flags": {
    "screening_relevant": true,
    "has_external_validation": true,
    "case_control_design": false,
    "impact_factor": 14.7,
    "if_above_10": true,
    "if_unknown": false,
    "tier": "core"
  }
}
```

See `schema.json` for the full JSON Schema definition.

---

## Quality Flags

| Flag | Description |
|------|-------------|
| `tier: core` | Journal IF > 10 |
| `tier: extended` | Journal IF 5–10 |
| `tier: low_if` | Journal IF < 5 |
| `tier: unknown` | Journal IF not in lookup table |
| `screening_relevant` | Abstract mentions screening / early detection / risk prediction |
| `has_external_validation` | Independent validation cohort reported |
| `case_control_design` | Case-control study design (potential ascertainment bias) |

---

## Inclusion Criteria

- Original research articles (reviews and meta-analyses excluded)
- Reports ≥ 1 quantitative performance metric (AUC, sensitivity, or specificity)
- AUC ≥ 0.50 (implausible values excluded)
- Publication year 2018–2026
- Topic: AI-assisted early detection / screening / diagnosis (treatment response, prognosis, staging excluded)

---

## Key Findings

- **cfDNA dominates** non-lung cancers (275/455 papers, 60.4%) — liquid biopsy is the primary modality for most cancer types
- **LDCT is lung-centric** (107/119 LDCT_traditional papers are lung) — other cancers rarely use LDCT for screening
- **Foundation models are nascent** (19 LDCT_LLM papers total; 0 cfDNA_LDCT_LLM papers) — a clear research frontier
- **Mean AUC = 0.880** across 300 papers with reported AUC; 66% achieve AUC ≥ 0.90
- **External validation is rare** — only a minority of papers report independent cohort validation
- **cfDNA_LDCT_LLM = 0** — no published work yet combines multimodal cfDNA+CT with foundation models for early detection

---

## Limitations

1. Year unknown for 188 papers (41%) from the original lung library
2. AUC values extracted automatically via regex — may contain parsing errors; AUC=1.0 papers (n=15) are flagged
3. Category assignment is heuristic (keyword-based); some multimodal papers may be miscategorised
4. Search limited to PubMed; arXiv/medRxiv preprints not included
5. Journal IF values from a static lookup table (2023); 29% of papers have unknown IF

---

## Citation

If you use this database, please cite the associated survey paper (forthcoming).
