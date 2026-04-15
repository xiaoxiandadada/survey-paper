#!/usr/bin/env python3
"""
06_rq3_narrative_table.py
=========================
Generate Table 3 for RQ3: cfDNA methylation + deep learning studies.
Produces a structured CSV and a formatted PNG table for the manuscript.

NOTE: RQ3 is a NARRATIVE REVIEW only (n=6 studies).
      No meta-analysis is performed.

Reads:  meta-analysis/data/rq3_narrative_data.csv
Writes: meta-analysis/results/rq3_table3.csv
        meta-analysis/results/fig_rq3_table3.png

Usage (run from repo root):
    python meta-analysis/code/06_rq3_narrative_table.py \
        --csv meta-analysis/data/rq3_narrative_data.csv \
        --outdir meta-analysis/results
"""

import argparse
import os
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# ── architecture classification ───────────────────────────────────────────────
ARCH_MAP = {
    '41323119': 'CNN + clinical fusion',
    '39380154': 'Transformer + MIL',
    '37598236': 'Deep learning (unspecified)',
    '35600397': 'Deep learning (unspecified)',
    '38926407': 'CNN (fragment size)',
    '38961476': 'Graph CNN (GCN)',
}

INPUT_MAP = {
    '41323119': 'Methylation + LDCT + imaging',
    '39380154': 'Bisulfite cfDNA (genome-wide)',
    '37598236': 'cfDNA methylation panel',
    '35600397': 'cfDNA methylation + ctDNA',
    '38926407': 'Methylation + fragment size',
    '38961476': 'Methylation atlas (low-depth)',
}


def wrap(text, width=30):
    if pd.isna(text) or str(text).strip() in ('', 'nan'):
        return '—'
    return '\n'.join(textwrap.wrap(str(text), width))


def main(csv_path: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(csv_path, dtype=str)
    df['pmid'] = df['pmid'].astype(str).str.strip()

    # enrich with architecture and input info
    df['architecture'] = df['pmid'].map(ARCH_MAP).fillna('Deep learning')
    df['input_detail'] = df['pmid'].map(INPUT_MAP).fillna(df['input_modalities'])

    # format AUC
    df['auc_display'] = df['auc_raw'].apply(
        lambda x: f"{float(x):.3f}" if pd.notna(x) and str(x) not in ('', 'nan') else '—'
    )

    # validation display
    df['val_display'] = df['validation_type'].apply(
        lambda x: 'External' if str(x) == 'external_validation'
                  else ('Internal CV' if str(x) == 'internal_CV' else 'None')
    )

    # cohort size
    df['n_display'] = df['cohort_size_num'].apply(
        lambda x: f"{int(float(x)):,}" if pd.notna(x) and str(x) not in ('', 'nan') else '—'
    )

    # short title (first 55 chars)
    df['title_short'] = df['title'].apply(
        lambda x: str(x)[:55] + '…' if pd.notna(x) and len(str(x)) > 55 else str(x)
    )

    # ── CSV output ────────────────────────────────────────────────────────────
    table_cols = {
        'pmid':          'PMID',
        'pub_year_num':  'Year',
        'title_short':   'Title (abbreviated)',
        'architecture':  'DL Architecture',
        'input_detail':  'Input Features',
        'n_display':     'N (cohort)',
        'auc_display':   'AUC',
        'val_display':   'Validation',
        'design_quality':'Quality Score',
    }
    out_df = df[[c for c in table_cols if c in df.columns]].rename(columns=table_cols)
    out_df.to_csv(os.path.join(outdir, 'rq3_table3.csv'), index=False)
    print(f"Saved: rq3_table3.csv  ({len(out_df)} rows)")

    # ── PNG table ─────────────────────────────────────────────────────────────
    display_cols = ['PMID', 'Year', 'DL Architecture', 'Input Features',
                    'N (cohort)', 'AUC', 'Validation']
    display_df = out_df[[c for c in display_cols if c in out_df.columns]]

    fig, ax = plt.subplots(figsize=(16, max(4, len(display_df) * 1.1 + 1.5)))
    ax.axis('off')

    col_widths = [0.07, 0.05, 0.18, 0.22, 0.09, 0.07, 0.10]
    col_widths = col_widths[:len(display_df.columns)]

    tbl = ax.table(
        cellText  = display_df.values,
        colLabels = display_df.columns,
        cellLoc   = 'left',
        loc       = 'center',
        colWidths = col_widths,
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 2.2)

    # header styling
    for j in range(len(display_df.columns)):
        cell = tbl[0, j]
        cell.set_facecolor('#0279EE')
        cell.set_text_props(color='white', fontweight='bold')

    # alternating row colors
    for i in range(1, len(display_df) + 1):
        bg = '#F5F5F5' if i % 2 == 0 else 'white'
        for j in range(len(display_df.columns)):
            tbl[i, j].set_facecolor(bg)

    ax.set_title(
        'Table 3. Studies on Deep Learning + cfDNA Methylation for Lung Cancer Detection (RQ3)\n'
        'Narrative review only — insufficient studies (n=6) for quantitative meta-analysis.',
        fontsize=10, pad=12, loc='left'
    )

    plt.tight_layout()
    out_path = os.path.join(outdir, 'fig_rq3_table3.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: fig_rq3_table3.png")

    # ── narrative summary ─────────────────────────────────────────────────────
    print("\n── RQ3 Narrative Summary ──")
    print(f"  Total studies: {len(df)}")
    auc_vals = pd.to_numeric(df['auc_raw'], errors='coerce').dropna()
    if len(auc_vals) > 0:
        print(f"  Studies with AUC: {len(auc_vals)}, "
              f"range [{auc_vals.min():.3f}, {auc_vals.max():.3f}]")
    ext_val = (df['validation_type'] == 'external_validation').sum()
    print(f"  With external validation: {ext_val}")
    print(f"  Architecture types: {df['architecture'].value_counts().to_dict()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate RQ3 narrative table')
    parser.add_argument('--csv',    default='meta-analysis/data/rq3_narrative_data.csv')
    parser.add_argument('--outdir', default='meta-analysis/results')
    args = parser.parse_args()
    main(args.csv, args.outdir)
