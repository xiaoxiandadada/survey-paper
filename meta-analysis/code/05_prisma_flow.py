#!/usr/bin/env python3
"""
05_prisma_flow.py
=================
Generate a PRISMA-DTA 2023 flow diagram for the systematic review.

The node counts below reflect the current state of the literature search.
Update the COUNTS dictionary with your actual screening numbers before
submitting the manuscript.

Reads:  data/tsv/included_papers.tsv  (to auto-fill final inclusion count)
Writes: meta-analysis/results/fig_prisma_flow.png

Usage (run from repo root):
    python meta-analysis/code/05_prisma_flow.py \
        --tsv data/tsv/included_papers.tsv \
        --outdir meta-analysis/results
"""

import argparse
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import pandas as pd

# ── update these counts with your actual screening numbers ────────────────────
COUNTS = {
    'pubmed_records':       1603,   # PubMed initial hits (update after final search)
    'supplementary':         200,   # supplementary / hand-search records
    'duplicates_removed':    300,   # estimated duplicates
    'title_abstract_screened': 1503,
    'title_abstract_excluded': 1100,
    'fulltext_assessed':      403,
    'fulltext_excluded':      132,
    'fulltext_excl_reason1':   60,  # No diagnostic performance metrics
    'fulltext_excl_reason2':   40,  # Review / editorial / no primary data
    'fulltext_excl_reason3':   20,  # Animal / in vitro study
    'fulltext_excl_reason4':   12,  # Late-stage treatment outcomes only
    # final inclusion is read from TSV automatically
}

BOX_W, BOX_H = 3.2, 0.7
FONT = 9
BLUE  = '#0279EE'
GREEN = '#75A025'
GREY  = '#888888'
WHITE = '#FFFFFF'


def draw_box(ax, x, y, text, color=BLUE, fontsize=FONT, width=BOX_W, height=BOX_H):
    rect = mpatches.FancyBboxPatch(
        (x - width / 2, y - height / 2), width, height,
        boxstyle="round,pad=0.05",
        facecolor=WHITE, edgecolor=color, linewidth=1.8
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, wrap=True,
            multialignment='center',
            color='#222222')


def arrow(ax, x1, y1, x2, y2, color='#444444'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))


def main(tsv_path: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(tsv_path, sep='\t', dtype=str)
    n_included = len(df)
    n_core     = (df['core_library'].str.strip().str.lower() == 'true').sum()

    fig, ax = plt.subplots(figsize=(11, 14))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 14)
    ax.axis('off')

    # ── Identification ────────────────────────────────────────────────────────
    ax.text(5.5, 13.5, 'PRISMA-DTA Flow Diagram', ha='center', va='center',
            fontsize=13, fontweight='bold', color='#222222')

    ax.text(0.3, 13.0, 'Identification', ha='left', va='center',
            fontsize=9, fontweight='bold', color=GREY,
            rotation=90, transform=ax.transData)

    draw_box(ax, 3.5, 12.8,
             f"Records from PubMed\n(n = {COUNTS['pubmed_records']:,})",
             color=BLUE)
    draw_box(ax, 7.5, 12.8,
             f"Supplementary / hand-search\n(n = {COUNTS['supplementary']:,})",
             color=BLUE)

    draw_box(ax, 5.5, 11.5,
             f"Records after duplicate removal\n(n = {COUNTS['pubmed_records'] + COUNTS['supplementary'] - COUNTS['duplicates_removed']:,})",
             color=BLUE, width=4.0)

    arrow(ax, 3.5, 12.45, 3.5, 11.85)
    arrow(ax, 7.5, 12.45, 7.5, 11.85)
    ax.annotate('', xy=(5.5, 11.85), xytext=(3.5, 11.85),
                arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))
    ax.annotate('', xy=(5.5, 11.85), xytext=(7.5, 11.85),
                arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))

    # ── Screening ─────────────────────────────────────────────────────────────
    ax.text(0.3, 10.5, 'Screening', ha='left', va='center',
            fontsize=9, fontweight='bold', color=GREY,
            rotation=90, transform=ax.transData)

    draw_box(ax, 4.0, 10.5,
             f"Records screened\n(title & abstract)\n(n = {COUNTS['title_abstract_screened']:,})",
             color=BLUE)
    draw_box(ax, 8.5, 10.5,
             f"Records excluded\n(n = {COUNTS['title_abstract_excluded']:,})",
             color='#CC4444', width=2.8)

    arrow(ax, 5.5, 11.15, 4.0, 10.85)
    arrow(ax, 4.0, 10.15, 4.0, 9.55)
    ax.annotate('', xy=(7.1, 10.5), xytext=(5.6, 10.5),
                arrowprops=dict(arrowstyle='->', color='#CC4444', lw=1.5))

    # ── Eligibility ───────────────────────────────────────────────────────────
    ax.text(0.3, 8.8, 'Eligibility', ha='left', va='center',
            fontsize=9, fontweight='bold', color=GREY,
            rotation=90, transform=ax.transData)

    draw_box(ax, 4.0, 9.2,
             f"Full-text articles assessed\n(n = {COUNTS['fulltext_assessed']:,})",
             color=BLUE)

    excl_text = (
        f"Full-text excluded (n = {COUNTS['fulltext_excluded']})\n"
        f"  · No diagnostic metrics: {COUNTS['fulltext_excl_reason1']}\n"
        f"  · Review / no primary data: {COUNTS['fulltext_excl_reason2']}\n"
        f"  · Animal / in vitro: {COUNTS['fulltext_excl_reason3']}\n"
        f"  · Treatment outcomes only: {COUNTS['fulltext_excl_reason4']}"
    )
    draw_box(ax, 8.5, 9.2, excl_text,
             color='#CC4444', width=3.8, height=1.2, fontsize=7.5)

    arrow(ax, 4.0, 8.85, 4.0, 8.15)
    ax.annotate('', xy=(6.6, 9.2), xytext=(5.6, 9.2),
                arrowprops=dict(arrowstyle='->', color='#CC4444', lw=1.5))

    # ── Included ──────────────────────────────────────────────────────────────
    ax.text(0.3, 7.2, 'Included', ha='left', va='center',
            fontsize=9, fontweight='bold', color=GREY,
            rotation=90, transform=ax.transData)

    draw_box(ax, 4.0, 7.8,
             f"Studies included in systematic review\n(n = {n_included})",
             color=GREEN, width=4.2)

    draw_box(ax, 4.0, 6.7,
             f"Core library (high-quality subset)\n(n = {n_core}, total_score ≥ 50)",
             color=GREEN, width=4.2)

    arrow(ax, 4.0, 7.45, 4.0, 7.05)

    # RQ breakdown boxes
    rq_y = 5.5
    for i, (label, color) in enumerate([
        (f"RQ1: AI models\n(imaging-only vs multi-modal)\nn = 121", BLUE),
        (f"RQ2: cfDNA methylation\n(solo vs combined)\nn = 65",    '#FF9400'),
        (f"RQ3: DL + methylation\n(narrative review)\nn = 6",      '#888888'),
    ]):
        x = 2.0 + i * 3.0
        draw_box(ax, x, rq_y, label, color=color, width=2.6, height=1.0, fontsize=8)
        arrow(ax, 4.0, 6.35, x, rq_y + 0.5)

    plt.tight_layout()
    out_path = os.path.join(outdir, 'fig_prisma_flow.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: fig_prisma_flow.png  (n_included={n_included}, n_core={n_core})")
    print("NOTE: Update COUNTS dict with actual screening numbers before submission.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate PRISMA-DTA flow diagram')
    parser.add_argument('--tsv',    default='data/tsv/included_papers.tsv')
    parser.add_argument('--outdir', default='meta-analysis/results')
    args = parser.parse_args()
    main(args.tsv, args.outdir)
