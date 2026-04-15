#!/usr/bin/env python3
"""
01_data_preparation.py
======================
Prepare analysis datasets for RQ1, RQ2, and RQ3 meta-analyses.

Reads:  data/tsv/included_papers.tsv  (from repo root)
Writes: meta-analysis/data/rq1_meta_data.csv
        meta-analysis/data/rq2_meta_data.csv
        meta-analysis/data/rq3_narrative_data.csv

Usage (run from repo root):
    python meta-analysis/code/01_data_preparation.py \
        --tsv data/tsv/included_papers.tsv \
        --outdir meta-analysis/data
"""

import argparse
import math
import os
import re

import numpy as np
import pandas as pd


# ── helpers ───────────────────────────────────────────────────────────────────

def parse_auc(val):
    """Parse AUC value to float in (0, 1). Returns NaN on failure."""
    if pd.isna(val):
        return np.nan
    s = re.sub(r'%$', '', str(val).strip())
    try:
        v = float(s)
    except ValueError:
        return np.nan
    if v > 1.0:          # reported as percentage (e.g. 95 → 0.95)
        v = v / 100.0
    return v if 0.0 < v < 1.0 else np.nan


def logit(p):
    return math.log(p / (1.0 - p))


def logit_var_approx(auc, n_total, prevalence=0.5):
    """
    Approximate variance of logit(AUC).
    vi ≈ 1 / (n_cases * AUC * (1 - AUC))
    where n_cases = n_total * prevalence.

    NOTE: underestimates true variance when original SE is not reported.
    Flagged in the 'var_approx' column (True = approximated).
    """
    n_cases = max(n_total * prevalence, 1)
    denom = n_cases * auc * (1.0 - auc)
    return (1.0 / denom) if denom > 0 else np.nan


def is_imaging_only(s):
    if pd.isna(s):
        return False
    return set(str(s).split('|')).issubset({'LDCT', 'CT', 'imaging'})


def has_liquid(s):
    if pd.isna(s):
        return False
    return any(x in str(s) for x in ['cfDNA', 'ctDNA', 'blood_protein', 'miRNA', 'proteomics'])


def has_clinical(s):
    return (not pd.isna(s)) and ('clinical_features' in str(s))


def rq1_group(row):
    s = row['input_modalities']
    if is_imaging_only(s):
        return 'imaging_only'
    if has_liquid(s):
        return 'imaging+liquid'
    if has_clinical(s):
        return 'imaging+clinical'
    return 'other'


def rq2_subgroup(s):
    if pd.isna(s):
        return 'other'
    if 'LDCT' in s or ('CT' in s and 'cfDNA' in s):
        return 'meth+imaging'
    if 'cfDNA_fragmentomics' in s:
        return 'meth+fragmentomics'
    if 'ctDNA' in s:
        return 'meth+ctDNA'
    if 'clinical_features' in s:
        return 'meth+clinical'
    return 'other'


# ── main ──────────────────────────────────────────────────────────────────────

def main(tsv_path: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(tsv_path, sep='\t', dtype=str)
    print(f"Loaded {len(df)} papers from {tsv_path}")

    # numeric coercions
    df['auc_raw']         = df['auc'].apply(parse_auc)
    df['sensitivity_raw'] = pd.to_numeric(df['sensitivity'], errors='coerce')
    df['specificity_raw'] = pd.to_numeric(df['specificity'], errors='coerce')
    df['cohort_size_num'] = pd.to_numeric(df['cohort_size'],  errors='coerce')
    df['pub_year_num']    = pd.to_numeric(df['pub_year'],     errors='coerce')

    # logit-AUC and approximate variance
    df['logit_auc'] = df['auc_raw'].apply(
        lambda x: logit(x) if pd.notna(x) else np.nan)
    df['logit_var'] = df.apply(
        lambda r: logit_var_approx(r['auc_raw'], r['cohort_size_num'])
        if pd.notna(r['auc_raw']) and pd.notna(r['cohort_size_num']) else np.nan,
        axis=1)
    df['var_approx'] = df['logit_var'].notna()

    # ── RQ1: AI models (single-modal vs multi-modal) ──────────────────────────
    rq1 = df[df['model_type'].isin(['deep_learning', 'other_ML'])].copy()
    rq1['rq1_group'] = rq1.apply(rq1_group, axis=1)

    rq1_cols = [
        'pmid', 'title', 'pub_year_num', 'journal', 'cancer_type',
        'study_design', 'screening_or_clinical', 'cohort_size_num',
        'input_modalities', 'model_type', 'validation_type', 'rq1_group',
        'auc_raw', 'logit_auc', 'logit_var', 'var_approx',
        'sensitivity_raw', 'specificity_raw',
        'design_quality', 'core_library', 'total_score',
    ]
    rq1_out = rq1[[c for c in rq1_cols if c in rq1.columns]]
    rq1_out.to_csv(os.path.join(outdir, 'rq1_meta_data.csv'), index=False)
    print(f"\nRQ1: {len(rq1_out)} papers → rq1_meta_data.csv")
    for g in ['imaging_only', 'imaging+clinical', 'imaging+liquid', 'other']:
        sub = rq1_out[rq1_out['rq1_group'] == g]
        print(f"  {g:22s}: n={len(sub):3d}, with AUC={sub['auc_raw'].notna().sum()}")

    # ── RQ2: cfDNA methylation combinations ───────────────────────────────────
    rq2 = df[df['input_modalities'].str.contains('cfDNA_methylation', na=False)].copy()
    rq2['is_combo']  = rq2['input_modalities'].str.contains(r'\|', na=False)
    rq2['rq2_group'] = rq2.apply(
        lambda r: rq2_subgroup(r['input_modalities']) if r['is_combo'] else 'meth_only',
        axis=1)

    rq2_cols = [
        'pmid', 'title', 'pub_year_num', 'journal', 'cancer_type',
        'study_design', 'screening_or_clinical', 'cohort_size_num',
        'input_modalities', 'model_type', 'validation_type',
        'is_combo', 'rq2_group',
        'auc_raw', 'logit_auc', 'logit_var', 'var_approx',
        'sensitivity_raw', 'specificity_raw',
        'design_quality', 'core_library', 'total_score',
    ]
    rq2_out = rq2[[c for c in rq2_cols if c in rq2.columns]]
    rq2_out.to_csv(os.path.join(outdir, 'rq2_meta_data.csv'), index=False)
    print(f"\nRQ2: {len(rq2_out)} papers → rq2_meta_data.csv")
    for g in rq2_out['rq2_group'].value_counts().index:
        sub = rq2_out[rq2_out['rq2_group'] == g]
        print(f"  {g:22s}: n={len(sub):3d}, with AUC={sub['auc_raw'].notna().sum()}")

    # ── RQ3: cfDNA methylation + deep learning (narrative only) ───────────────
    rq3 = df[
        df['input_modalities'].str.contains('cfDNA_methylation', na=False) &
        df['model_type'].isin(['deep_learning'])
    ].copy()

    rq3_cols = [
        'pmid', 'title', 'pub_year_num', 'journal', 'doi',
        'cancer_type', 'study_design', 'cohort_size_num',
        'input_modalities', 'model_type', 'validation_type',
        'auc_raw', 'sensitivity_raw', 'specificity_raw',
        'key_limitations', 'design_quality', 'total_score',
    ]
    rq3_out = rq3[[c for c in rq3_cols if c in rq3.columns]]
    rq3_out.to_csv(os.path.join(outdir, 'rq3_narrative_data.csv'), index=False)
    print(f"\nRQ3: {len(rq3_out)} papers → rq3_narrative_data.csv (narrative only, no meta-analysis)")

    # ── global AUC summary ────────────────────────────────────────────────────
    all_auc = df['auc_raw'].dropna()
    print(f"\nAll papers with AUC: n={len(all_auc)}, "
          f"median={all_auc.median():.3f}, "
          f"range=[{all_auc.min():.3f}, {all_auc.max():.3f}]")
    print("\nDone. Output files written to:", outdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare meta-analysis datasets')
    parser.add_argument('--tsv',    default='data/tsv/included_papers.tsv')
    parser.add_argument('--outdir', default='meta-analysis/data')
    args = parser.parse_args()
    main(args.tsv, args.outdir)
