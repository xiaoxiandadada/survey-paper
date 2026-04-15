#!/usr/bin/env Rscript
# =============================================================================
# 02_meta_analysis_rq1.R
# =============================================================================
# RQ1: Diagnostic accuracy of AI models for lung cancer screening
#      Single-modal imaging AI vs multi-modal fusion AI
#
# Reads:  meta-analysis/data/rq1_meta_data.csv
# Writes: meta-analysis/results/rq1_forest_auc.png
#         meta-analysis/results/rq1_subgroup_validation.png
#         meta-analysis/results/rq1_subgroup_setting.png
#         meta-analysis/results/rq1_deeks_funnel.png
#         meta-analysis/results/rq1_sroc.png          (if n >= 4)
#         meta-analysis/results/rq1_summary_stats.csv
#
# Requirements: metafor, mada, ggplot2, dplyr
# Install:  install.packages(c("metafor", "mada", "ggplot2", "dplyr"))
# =============================================================================

suppressPackageStartupMessages({
  library(metafor)
  library(mada)
  library(ggplot2)
  library(dplyr)
})

# ── paths ─────────────────────────────────────────────────────────────────────
args    <- commandArgs(trailingOnly = TRUE)
infile  <- if (length(args) >= 1) args[1] else "meta-analysis/data/rq1_meta_data.csv"
outdir  <- if (length(args) >= 2) args[2] else "meta-analysis/results"
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

# ── load data ─────────────────────────────────────────────────────────────────
df <- read.csv(infile, stringsAsFactors = FALSE)
cat(sprintf("Loaded %d papers for RQ1\n", nrow(df)))

# keep only papers with parseable AUC and variance
df_auc <- df %>%
  filter(!is.na(auc_raw), !is.na(logit_auc), !is.na(logit_var)) %>%
  filter(logit_var > 0)

cat(sprintf("Papers with AUC + variance: %d\n", nrow(df_auc)))

# ── helper: run random-effects model ─────────────────────────────────────────
run_rma <- function(data, label = "") {
  if (nrow(data) < 2) {
    cat(sprintf("  [%s] Insufficient studies (n=%d), skipping\n", label, nrow(data)))
    return(NULL)
  }
  fit <- tryCatch(
    rma(yi = logit_auc, vi = logit_var, data = data,
        method = "DL",          # DerSimonian-Laird
        test   = "knha"),       # Knapp-Hartung correction
    error = function(e) { cat("  rma error:", conditionMessage(e), "\n"); NULL }
  )
  if (!is.null(fit)) {
    pooled_auc <- plogis(fit$b)   # back-transform from logit
    pooled_ci  <- plogis(c(fit$ci.lb, fit$ci.ub))
    cat(sprintf("  [%s] n=%d, pooled AUC=%.3f [%.3f, %.3f], I2=%.1f%%, tau2=%.4f\n",
                label, nrow(data), pooled_auc, pooled_ci[1], pooled_ci[2],
                fit$I2, fit$tau2))
  }
  fit
}

# ── 1. Main analysis: three groups ───────────────────────────────────────────
groups <- c("imaging_only", "imaging+clinical", "imaging+liquid")
fits   <- list()
for (g in groups) {
  sub <- df_auc %>% filter(rq1_group == g)
  fits[[g]] <- run_rma(sub, g)
}

# ── 2. Forest plot: all groups layered ───────────────────────────────────────
png(file.path(outdir, "rq1_forest_auc.png"), width = 1400, height = 900, res = 120)
par(mfrow = c(1, 3), mar = c(4, 8, 3, 2))
group_labels <- c(
  imaging_only      = "Imaging-only AI",
  "imaging+clinical" = "Imaging + Clinical",
  "imaging+liquid"   = "Imaging + Liquid Biopsy"
)
for (g in groups) {
  sub <- df_auc %>% filter(rq1_group == g)
  if (nrow(sub) < 2 || is.null(fits[[g]])) next
  forest(fits[[g]],
         slab      = sub$pmid,
         atransf   = plogis,
         at        = logit(c(0.5, 0.7, 0.8, 0.9, 0.95, 0.99)),
         xlim      = c(-3, 3),
         xlab      = "AUC",
         main      = group_labels[g],
         header    = TRUE,
         col       = "#0279EE",
         border    = "#0279EE")
}
dev.off()
cat("Saved: rq1_forest_auc.png\n")

# ── 3. Subgroup: validation type ─────────────────────────────────────────────
df_auc$val_group <- ifelse(df_auc$validation_type == "external_validation",
                           "External validation", "No external validation")
fit_val <- tryCatch(
  rma(yi = logit_auc, vi = logit_var, data = df_auc,
      mods = ~ factor(val_group), method = "DL", test = "knha"),
  error = function(e) NULL
)

png(file.path(outdir, "rq1_subgroup_validation.png"), width = 1200, height = 700, res = 120)
if (!is.null(fit_val)) {
  forest(fit_val,
         slab    = df_auc$pmid,
         atransf = plogis,
         at      = logit(c(0.5, 0.7, 0.8, 0.9, 0.95, 0.99)),
         xlab    = "AUC",
         main    = "RQ1 Subgroup: Validation Type",
         header  = TRUE)
} else {
  plot.new(); title("RQ1 Subgroup: Validation Type\n(insufficient data)")
}
dev.off()
cat("Saved: rq1_subgroup_validation.png\n")

# ── 4. Subgroup: application setting ─────────────────────────────────────────
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

png(file.path(outdir, "rq1_subgroup_setting.png"), width = 1200, height = 700, res = 120)
if (!is.null(fit_set)) {
  forest(fit_set,
         slab    = df_auc$pmid,
         atransf = plogis,
         at      = logit(c(0.5, 0.7, 0.8, 0.9, 0.95, 0.99)),
         xlab    = "AUC",
         main    = "RQ1 Subgroup: Application Setting",
         header  = TRUE)
} else {
  plot.new(); title("RQ1 Subgroup: Application Setting\n(insufficient data)")
}
dev.off()
cat("Saved: rq1_subgroup_setting.png\n")

# ── 5. Deeks funnel plot (imaging_only, n >= 10) ──────────────────────────────
img_only <- df_auc %>% filter(rq1_group == "imaging_only")
png(file.path(outdir, "rq1_deeks_funnel.png"), width = 800, height = 700, res = 120)
if (nrow(img_only) >= 10) {
  # mada::deeks.test requires TP/FP/FN/TN; approximate from AUC + cohort size
  # Use metafor funnel as fallback when raw 2x2 data unavailable
  if (!is.null(fits[["imaging_only"]])) {
    funnel(fits[["imaging_only"]],
           xlab = "logit(AUC)",
           main = "Deeks Funnel Plot – Imaging-only AI (RQ1)\n(Egger's test proxy; use raw 2x2 data for formal Deeks test)")
    # Egger's test as proxy
    reg <- regtest(fits[["imaging_only"]], model = "lm")
    cat(sprintf("  Egger's test (proxy): z=%.3f, p=%.4f\n", reg$zval, reg$pval))
  }
} else {
  plot.new()
  title(sprintf("Deeks Funnel Plot\n(n=%d < 10, not executed)", nrow(img_only)))
}
dev.off()
cat("Saved: rq1_deeks_funnel.png\n")

# ── 6. SROC curve (imaging+liquid, conditional on n >= 4) ────────────────────
sroc_data <- df %>%
  filter(rq1_group == "imaging+liquid",
         !is.na(sensitivity_raw), !is.na(specificity_raw)) %>%
  mutate(TP = round(sensitivity_raw * cohort_size_num * 0.3),
         FN = round((1 - sensitivity_raw) * cohort_size_num * 0.3),
         FP = round((1 - specificity_raw) * cohort_size_num * 0.7),
         TN = round(specificity_raw * cohort_size_num * 0.7)) %>%
  filter(!is.na(TP), TP > 0, FN > 0, FP > 0, TN > 0)

png(file.path(outdir, "rq1_sroc.png"), width = 800, height = 800, res = 120)
if (nrow(sroc_data) >= 4) {
  fit_sroc <- reitsma(sroc_data[, c("TP","FN","FP","TN")])
  plot(fit_sroc,
       main = "SROC Curve – Imaging + Liquid Biopsy AI (RQ1)",
       sroclwd = 2, col = "#0279EE")
  points(fpr(sroc_data), sens(sroc_data), pch = 19, col = "grey40")
  legend("bottomright",
         legend = c("SROC curve", "Individual studies"),
         lty    = c(1, NA), pch = c(NA, 19),
         col    = c("#0279EE", "grey40"), bty = "n")
} else {
  plot.new()
  title(sprintf("SROC – Imaging + Liquid Biopsy\n(n=%d with Sens+Spec, threshold n=4 not met)", nrow(sroc_data)))
}
dev.off()
cat("Saved: rq1_sroc.png\n")

# ── 7. Summary statistics CSV ─────────────────────────────────────────────────
summary_rows <- lapply(groups, function(g) {
  sub  <- df_auc %>% filter(rq1_group == g)
  fit  <- fits[[g]]
  if (is.null(fit) || nrow(sub) < 2) {
    return(data.frame(group = g, n = nrow(sub), pooled_auc = NA,
                      ci_lower = NA, ci_upper = NA, I2 = NA, tau2 = NA,
                      Q_pval = NA, stringsAsFactors = FALSE))
  }
  data.frame(
    group       = g,
    n           = nrow(sub),
    pooled_auc  = round(plogis(fit$b), 4),
    ci_lower    = round(plogis(fit$ci.lb), 4),
    ci_upper    = round(plogis(fit$ci.ub), 4),
    I2          = round(fit$I2, 1),
    tau2        = round(fit$tau2, 5),
    Q_pval      = round(fit$QEp, 4),
    stringsAsFactors = FALSE
  )
})
summary_df <- do.call(rbind, summary_rows)
write.csv(summary_df, file.path(outdir, "rq1_summary_stats.csv"), row.names = FALSE)
cat("Saved: rq1_summary_stats.csv\n")
print(summary_df)

cat("\nRQ1 analysis complete.\n")
