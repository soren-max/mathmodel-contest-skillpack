# Validation Patterns

| Problem Type | Recommended Validation |
|---|---|
| regression | [CROSS-PAPER PATTERN] Honest grouped/held-out split, simple baseline, residuals by range/group, MAE/RMSE plus scale-free metric, uncertainty/calibration |
| classification | [CROSS-PAPER PATTERN] Freeze positive class, leakage-safe stratified/group split, confusion matrix and classwise precision/recall, calibration, repeated CV |
| time series | [CROSS-PAPER PATTERN] Rolling-origin or forward split, naive/seasonal baseline, horizon-wise errors, residual autocorrelation, regime checks |
| optimization | [CROSS-PAPER PATTERN] Independent constraint/objective replay, exact bound or reduced exact case, gap/status, seed/weight/scenario sensitivity, post-optimum reality check |
| simulation | [CROSS-PAPER PATTERN] Analytical moments/limiting cases, many seeds and confidence bands, step-size/sample-size convergence, distributional tests, external trace when available |
| mechanism | [CROSS-PAPER PATTERN] Units/reference frames, invariants/conservation, limiting cases, component magnitude budget, benchmark calculation |
| scheduling | [CROSS-PAPER PATTERN] Full rule replay, exact small instances/lower bounds, uncovered-demand report, runtime/scaling, disruption scenarios |
| stochastic | [CROSS-PAPER PATTERN] Distribution justification, count/interarrival/quantile checks, Monte Carlo error/convergence, parameter-uncertainty propagation |

## Evidence That Actually Helps

- [CROSS-PAPER PATTERN] Exact-small versus heuristic-large comparison (GMCM-2021-F) distinguishes feasibility from optimality.
- [CROSS-PAPER PATTERN] Lower bounds plus constructive coordinates (GMCM-2022-B) anchor both quality and validity.
- [CROSS-PAPER PATTERN] Conservation invariants and correction magnitudes (GMCM-2024-F) test mechanism, not just output appearance.
- [CROSS-PAPER PATTERN] Sampling-density curves (GMCM-2025-C) test numerical stability.
- [CROSS-PAPER PATTERN] Multiple metrics and a simple physical baseline (GMCM-2024-C) help, provided splits and domains are honest.
- [CROSS-PAPER PATTERN] Negative results are evidence: failed small-data ML in GMCM-2025-C and 0.45 accuracy in GMCM-2023-E should remain visible.

## Validation Theater

- [CROSS-PAPER PATTERN] Randomly splitting adjacent minutes, then reporting R², does not validate forecasting (GMCM-2024-E).
- [CROSS-PAPER PATTERN] A noisy copy of the same random test distribution is not a distribution-shift test (GMCM-2024-C).
- [CROSS-PAPER PATTERN] One attractive stochastic plot does not validate a point process (GMCM-2024-F).
- [CROSS-PAPER PATTERN] Calling multiple datasets “robustness” without perturbations/seeds is weak (GMCM-2022-B/GMCM-2021-F).
- [CROSS-PAPER PATTERN] Renaming/swapping TP and TN to improve metrics is invalid, not an alternative convention (GMCM-2023-E).

[ANALYST INFERENCE] Never alter labels or metric denominators for appearance. State NOT FOUND when evidence is absent, retain negative results, and downgrade conclusions to the strongest level the validation supports.
