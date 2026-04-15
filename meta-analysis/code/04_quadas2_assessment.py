#!/usr/bin/env python3
"""
04_quadas2_assessment.py
========================
Map existing fields to QUADAS-2 four-domain risk-of-bias ratings for the
38 core-library papers, and generate a traffic-light heatmap.

Reads:  data/tsv/included_papers.tsv  (from repo root)
Writes: meta-analysis/results/quadas2_ratings.csv
        meta-analysis/results/fig_quadas2_traffic_light.png

Mapping rules (see ANALYSIS_PLAN.md §2 for full rationale):
  Domain 1 – Patient selection
    LOW    : prospective_cohort or RCT, cohort_size >= 100
    HIGH   : case_control
    UNCLEAR: otherwise

  Domain 2 – Index test
    LOW    : key_limitations does not mention threshold/cutoff post-hoc
    HIGH   : key_limitations mentions "threshold" or "cutoff" post-hoc
    UNCLEAR: key_limitations is missing

  Domain 3 – Reference standard
    LOW    : task_type == "diagnosis" AND stage_info not "late"
    HIGH   : task_type == "screening" with no pathology confirmation noted
    UNCLEAR: otherwise

  Domain 4 – Flow and timing
    LOW    : validation_type == "external_validation"
    HIGH   : validation_type == "none" AND study_design == "retrospective_cohort"
    UNCLEAR: otherwise

Usage (run from repo root):
    python meta-analysis/code/04_quadas2_assessment.py \
        --tsv data/tsv/included_papers.tsv \
        --outdir meta-analysis/results
"""

import argparse
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

RISK_COLORS = {'LOW': '#75A025', 'HIGH': '#E63946', 'UNCLEAR': '#FF9400'}
DOMAINS = ['D1: Patient\nSelection', 'D2: Index\nTest',
           'D3: Reference\nStandard', 'D4: Flow &\nTiming']


# ── domain rating functions ───────────────────────────────────────────────────

def rate_d1(row):
    """Domain 1: Patient selection."""
    design = str(row.get('study_design', '')).lower()
    size   = pd.to_numeric(row.get('cohort_size', None), errors='coerce')
    if design in ('case_control',):
        return 'HIGH'
    if design in ('prospective_cohort', 'rct'):
        return 'LOW' if (pd.notna(size) and size >= 100) else 'UNCLEAR'
    return 'UNCLEAR'


def rate_d2(row):
    """Domain 2: Index test."""
    lim = str(row.get('key_limitations', '')).lower()
    if not lim or lim in ('nan', ''):
        return 'UNCLEAR'
    post_hoc_terms = ['threshold', 'cutoff', 'cut-off', 'post-hoc', 'post hoc',
                      'optimized', 'selected after']
    if any(t in lim for t in post_hoc_terms):
        return 'HIGH'
    return 'LOW'


def rate_d3(row):
    """Domain 3: Reference standard."""
    task  = str(row.get('task_type', '')).lower()
    stage = str(row.get('stage_info', '')).lower()
    if task == 'diagnosis':
        return 'HIGH' if 'late' in stage else 'LOW'
    if task == 'screening':
        return 'UNCLEAR'
    return 'UNCLEAR'


def rate_d4(row):
    """Domain 4: Flow and timing."""
    val    = str(row.get('validation_type', '')).lower()
    design = str(row.get('study_design', '')).lower()
    if val == 'external_validation':
        return 'LOW'
    if val == 'none' and design == 'retrospective_cohort':
        return 'HIGH'
    return 'UNCLEAR'


# ── mapping for non-core papers (design_quality score) ───────────────────────

def score_to_risk(score):
    """Map design_quality (0-24) to overall risk level."""
    try:
        s = float(score)
    except (TypeError, ValueError):
        return 'UNCLEAR'
    if s >= 18:
        return 'LOW'
    if s >= 12:
        return 'UNCLEAR'
    return 'HIGH'


# ── main ──────────────────────────────────────────────────────────────────────

def main(tsv_path: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(tsv_path, sep='\t', dtype=str)
    core = df[df['core_library'].str.strip().str.lower() == 'true'].copy()
    print(f"Core library papers: {len(core)}")

    # apply domain ratings
    core['D1'] = core.apply(rate_d1, axis=1)
    core['D2'] = core.apply(rate_d2, axis=1)
    core['D3'] = core.apply(rate_d3, axis=1)
    core['D4'] = core.apply(rate_d4, axis=1)

    # short label for y-axis: first author + year
    def short_label(row):
        authors = str(row.get('authors', ''))
        year    = str(row.get('pub_year', ''))
        pmid    = str(row.get('pmid', ''))
        first   = authors.split(',')[0].strip() if authors and authors != 'nan' else pmid
        return f"{first} {year}" if year and year != 'nan' else pmid

    core['label'] = core.apply(short_label, axis=1)

    # save ratings CSV
    out_cols = ['pmid', 'label', 'title', 'pub_year', 'D1', 'D2', 'D3', 'D4']
    out_cols = [c for c in out_cols if c in core.columns]
    core[out_cols].to_csv(os.path.join(outdir, 'quadas2_ratings.csv'), index=False)
    print("Saved: quadas2_ratings.csv")

    # ── traffic-light heatmap ─────────────────────────────────────────────────
    domain_cols = ['D1', 'D2', 'D3', 'D4']
    matrix = core[domain_cols].values  # shape (n_papers, 4)
    n = len(core)

    fig, ax = plt.subplots(figsize=(6, max(8, n * 0.35)))
    for i, row_vals in enumerate(matrix):
        for j, risk in enumerate(row_vals):
            color = RISK_COLORS.get(risk, '#CCCCCC')
            rect = mpatches.FancyBboxPatch(
                (j + 0.05, n - i - 0.95), 0.9, 0.9,
                boxstyle="round,pad=0.05",
                facecolor=color, edgecolor='white', linewidth=1.5
            )
            ax.add_patch(rect)
            ax.text(j + 0.5, n - i - 0.5, risk[0],
                    ha='center', va='center',
                    fontsize=7, fontweight='bold', color='white')

    ax.set_xlim(0, 4)
    ax.set_ylim(0, n)
    ax.set_xticks([0.5, 1.5, 2.5, 3.5])
    ax.set_xticklabels(DOMAINS, fontsize=9)
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_yticklabels(core['label'].values[::-1], fontsize=7)
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='both', length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # legend
    legend_patches = [
        mpatches.Patch(color=RISK_COLORS['LOW'],     label='Low risk'),
        mpatches.Patch(color=RISK_COLORS['HIGH'],    label='High risk'),
        mpatches.Patch(color=RISK_COLORS['UNCLEAR'], label='Unclear risk'),
    ]
    ax.legend(handles=legend_patches, loc='lower center',
              bbox_to_anchor=(0.5, -0.04), ncol=3, fontsize=9,
              frameon=False)

    ax.set_title('QUADAS-2 Risk of Bias Assessment\n(Core Library, n=38)',
                 fontsize=11, pad=20)
    plt.tight_layout()
    out_path = os.path.join(outdir, 'fig_quadas2_traffic_light.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: fig_quadas2_traffic_light.png")

    # summary counts
    for d in domain_cols:
        counts = core[d].value_counts()
        print(f"  {d}: {dict(counts)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QUADAS-2 assessment')
    parser.add_argument('--tsv',    default='data/tsv/included_papers.tsv')
    parser.add_argument('--outdir', default='meta-analysis/results')
    args = parser.parse_args()
    main(args.tsv, args.outdir)
