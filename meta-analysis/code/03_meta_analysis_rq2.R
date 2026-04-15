#!/usr/bin/env Rscript
# =============================================================================
# 03_meta_analysis_rq2.R
# =============================================================================
# RQ2: Diagnostic accuracy of cfDNA methylation – solo vs combined modalities
#      Core comparisons:
#        (a) meth_only vs any combination (meta-regression)
#        (b) meth+imaging vs meth+fragmentomics (descriptive)
#
# Reads:  meta-analysis/data/rq2_meta_data.csv
# Writes: meta-analysis/results/rq2_forest_auc.png
#         meta-analysis/results/rq2_combination_bubble.png
#         meta-analysis/results/rq2_sroc_meth_only.png   (if n >= 4)
#         meta-analysis/results/rq2_subgroup_validation.png
#         meta-analysis/results/rq2_subgroup_setting.png
#         meta-analysis/results/rq2_summary_stats.csv
#
# Requirements: metafor, mada, ggplot2, dplyr
# =============================================================================

suppressPackageStartupMessages({
  library(metafor)
  library(mada)
  library(ggplot2)
  library(dplyr)
})

# ── paths ─────────────────────────────────────────────────────────────────────
args   <- commandArgs(trailingOnly = TRUE)
infile <- if (length(args) >= 1) args[1] else "meta-analysis/data/rq2_meta_data.csv"
outdir <- if (length(args) >= 2) args[2] else "meta-analysis/results"
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

df <- read.csv(infile, stringsAsFactors = FALSE)
cat(sprintf("Loaded %d papers for RQ2\n", nrow(df)))

df_auc <- df %>%
  filter(!is.na(auc_raw), !is.na(logit_auc), !is.na(logit_var), logit_var > 0)
cat(sprintf("Papers with AUC + variance: %d\n", nrow(df_auc)))

# ── helper ────────────────────────────────────────────────────────────────────
run_rma <- function(data, label = "") {
  if (nrow(data) < 2) {
    cat(sprintf("  [%s] n=%d < 2, skipping\n", label, nrow(data))); return(NULL)
  }
  fit <- tryCatch(
    rma(yi = logit_auc, vi = logit_var, data = data, method = "DL", test = "knha"),
    error = function(e) { cat("  rma error:", conditionMessage(e), "\n"); NULL }
  )
  if (!is.null(fit)) {
    p <- plogis(fit$b); ci <- plogis(c(fit$ci.lb, fit$ci.ub))
    cat(sprintf("  [%s] n=%d, AUC=%.3f [%.3f, %.3f], I2=%.1f%%\n",
                label, nrow(data), p, ci[1], ci[2], fit$I2))
  }
  fit
}

# ── 1. Per-group models ───────────────────────────────────────────────────────
groups <- c("meth_only", "meth+imaging", "meth+fragmentomics", "meth+ctDNA")
fits   <- list()
for (g in groups) {
  sub <- df_auc %>% filter(rq2_group == g)
  fits[[g]] <- run_rma(sub, g)
}

# ── 2. Meta-regression: combo vs solo ────────────────────────────────────────
df_auc$is_combo_fac <- factor(df_auc$is_combo, levels = c(FALSE, TRUE),
                               labels = c("meth_only", "combined"))
fit_combo <- tryCatch(
  rma(yi = logit_auc, vi = logit_var, data = df_auc,
      mods = ~ is_combo_fac, method = "DL", test = "knha"),
  error = function(e) NULL
)
if (!is.null(fit_combo)) {
  cat("\nMeta-regression: combined vs meth_only\n")
  print(summary(fit_combo))
}

# ── 3. Forest plot: solo vs combined ─────────────────────────────────────────
png(file.path(outdir, "rq2_forest_auc.png"), width = 1400, height = 900, res = 120)
par(mfrow = c(1, 2), mar = c(4, 8, 3, 2))

for (g in c("meth_only", "meth+imaging")) {
  sub <- df_auc %>% filter(rq2_group == g)
  fit <- fits[[g]]
  if (is.null(fit) || nrow(sub) < 2) {
    plot.new(); title(paste(g, "\n(insufficient data)")); next
  }
  forest(fit,
         slab    = sub$pmid,
         atransf = plogis,
         at      = logit(c(0.5, 0.7, 0.8, 0.9, 0.95, 0.99)),
         xlim    = c(-3, 3),
         xlab    = "AUC",
         main    = gsub("meth_only", "cfDNA Methylation Only",
                   gsub("meth\\+imaging", "Methylation + Imaging", g)),
         header  = TRUE,
         col     = "#75A025",
         border  = "#75A025")
}
dev.off()
cat("Saved: rq2_forest_auc.png\n")

# ── 4. Bubble plot: AUC by combination type ───────────────────────────────────
bubble_data <- df_auc %>%
  filter(rq2_group != "other") %>%
  mutate(
    group_label = dplyr::recode(rq2_group,
      meth_only          = "Methylation only",
      "meth+imaging"     = "Meth + Imaging",
      "meth+fragmentomics" = "Meth + Fragmentomics",
      "meth+ctDNA"       = "Meth + ctDNA",
      "meth+clinical"    = "Meth + Clinical"
    ),
    cohort_plot = pmax(cohort_size_num, 50, na.rm = TRUE)
  )

p_bubble <- ggplot(bubble_data,
                   aes(x = group_label, y = auc_raw,
                       size = cohort_plot, colour = group_label)) +
  geom_jitter(alpha = 0.7, width = 0.15) +
  stat_summary(fun = median, geom = "crossbar",
               width = 0.4, colour = "black", linewidth = 0.6) +
  scale_size_continuous(name = "Cohort size", range = c(3, 12)) +
  scale_colour_brewer(palette = "Set2", guide = "none") +
  labs(title    = "RQ2: AUC by cfDNA Methylation Combination Type",
       subtitle = "Crossbar = median; bubble size = cohort size",
       x = NULL, y = "AUC") +
  ylim(0.5, 1.0) +
  theme_bw(base_size = 13) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

ggsave(file.path(outdir, "rq2_combination_bubble.png"),
       p_bubble, width = 10, height = 6, dpi = 150)
cat("Saved: rq2_combination_bubble.png\n")

# ── 5. SROC: methylation-only (n >= 4 with Sens+Spec) ────────────────────────
sroc_data <- df %>%
  filter(rq2_group == "meth_only",
         !is.na(sensitivity_raw), !is.na(specificity_raw),
         !is.na(cohort_size_num)) %>%
  mutate(
    TP = round(sensitivity_raw * cohort_size_num * 0.4),
    FN = round((1 - sensitivity_raw) * cohort_size_num * 0.4),
    FP = round((1 - specificity_raw) * cohort_size_num * 0.6),
    TN = round(specificity_raw * cohort_size_num * 0.6)
  ) %>%
  filter(TP > 0, FN > 0, FP > 0, TN > 0)

png(file.path(outdir, "rq2_sroc_meth_only.png"), width = 800, height = 800, res = 120)
if (nrow(sroc_data) >= 4) {
  fit_sroc <- reitsma(sroc_data[, c("TP","FN","FP","TN")])
  plot(fit_sroc,
       main   = "SROC Curve – cfDNA Methylation Only (RQ2)",
       sroclwd = 2, col = "#75A025")
  points(fpr(sroc_data), sens(sroc_data), pch = 19, col = "grey40")
  legend("bottomright",
         legend = c("SROC curve", "Individual studies"),
         lty = c(1, NA), pch = c(NA, 19),
         col = c("#75A025", "grey40"), bty = "n")
  cat(sprintf("  SROC fitted on n=%d studies\n", nrow(sroc_data)))
} else {
  plot.new()
  title(sprintf("SROC – Methylation Only\n(n=%d with Sens+Spec, threshold n=4 not met)",
                nrow(sroc_data)))
}
dev.off()
cat("Saved: rq2_sroc_meth_only.png\n")

# ── 6. Subgroup: validation type ─────────────────────────────────────────────
df_auc$val_group <- ifelse(df_auc$validation_type == "external_validation",
                           "External validation", "No external validation")
fit_val <- tryCatch(
  rma(yi = logit_auc, vi = logit_var, data = df_auc,
      mods = ~ factor(val_group), method = "DL", test = "knha"),
  error = function(e) NULL
)
png(file.path(outdir, "rq2_subgroup_validation.png"), width = 1200, height = 700, res = 120)
if (!is.null(fit_val)) {
  forest(fit_val, slab = df_auc$pmid, atransf = plogis,
         at = logit(c(0.5, 0.7, 0.8, 0.9, 0.95, 0.99)),
         xlab = "AUC", main = "RQ2 Subgroup: Validation Type", header = TRUE)
} else {
  plot.new(); title("RQ2 Subgroup: Validation Type\n(insufficient data)")
}
dev.off()
cat("Saved: rq2_subgroup_validation.png\n")

# ── 7. Subgroup: application setting ─────────────────────────────────────────
df_auc$setting_group <- dplyr::recode(df_auc$screening_or_clinical,
  "screening"          = "Screening",
  "clinical_diagnosis" = "Clinical diagnosis",
  "both"               = "Both / mixed",
  .default             = "Both / mixed")
fit_set <- tryCatch(
  rma(yi = logit_auc, vi = logit_var, data = df_auc,
      mods = ~ factor(setting_group), method = "DL", test = "knha"),
  error = function(e) NULL
)
png(file.path(outdir, "rq2_subgroup_setting.png"), width = 1200, height = 700, res = 120)
if (!is.null(fit_set)) {
  forest(fit_set, slab = df_auc$pmid, atransf = plogis,
         at = logit(c(0.5, 0.7, 0.8, 0.9, 0.95, 0.99)),
         xlab = "AUC", main = "RQ2 Subgroup: Application Setting", header = TRUE)
} else {
  plot.new(); title("RQ2 Subgroup: Application Setting\n(insufficient data)")
}
dev.off()
cat("Saved: rq2_subgroup_setting.png\n")

# ── 8. Summary statistics CSV ─────────────────────────────────────────────────
summary_rows <- lapply(groups, function(g) {
  sub <- df_auc %>% filter(rq2_group == g)
  fit <- fits[[g]]
  if (is.null(fit) || nrow(sub) < 2) {
    return(data.frame(group = g, n = nrow(sub), pooled_auc = NA,
                      ci_lower = NA, ci_upper = NA, I2 = NA, tau2 = NA,
                      Q_pval = NA, stringsAsFactors = FALSE))
  }
  data.frame(group = g, n = nrow(sub),
             pooled_auc = round(plogis(fit$b), 4),
             ci_lower   = round(plogis(fit$ci.lb), 4),
             ci_upper   = round(plogis(fit$ci.ub), 4),
             I2         = round(fit$I2, 1),
             tau2       = round(fit$tau2, 5),
             Q_pval     = round(fit$QEp, 4),
             stringsAsFactors = FALSE)
})
summary_df <- do.call(rbind, summary_rows)
write.csv(summary_df, file.path(outdir, "rq2_summary_stats.csv"), row.names = FALSE)
cat("Saved: rq2_summary_stats.csv\n")
print(summary_df)

cat("\nRQ2 analysis complete.\n")
