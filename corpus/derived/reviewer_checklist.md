# Corpus-Informed Reviewer Checklist

Mark each item **PASS**, **FAIL**, **NOT FOUND** or **NOT APPLICABLE**, with an artifact/page/table reference.

## CRITICAL

- [CROSS-PAPER PATTERN] Every question has an explicit, traceable answer and units.
- [CROSS-PAPER PATTERN] State, decision variables, parameters, objectives and constraints are not conflated.
- [CROSS-PAPER PATTERN] Labels, positive class and metric formulas are fixed and internally consistent.
- [CROSS-PAPER PATTERN] Train/test separation respects patient, time, group and preprocessing boundaries; no leakage.
- [CROSS-PAPER PATTERN] Reported optimum/schedule/layout passes an independent feasibility and objective replay.
- [CROSS-PAPER PATTERN] Abstract, body, tables, figures and conclusion agree numerically.
- [CROSS-PAPER PATTERN] Probability/causal/optimality claims have calibration, identification or certificates; otherwise wording is downgraded.
- [CROSS-PAPER PATTERN] Mechanism equations have coherent units, frames, signs and limiting/invariant checks.

## MAJOR

- [CROSS-PAPER PATTERN] Model choice is justified by structure/data and compared with a simpler baseline.
- [CROSS-PAPER PATTERN] Solver is distinguished from model; exact status, gap or “best found” language is reported.
- [CROSS-PAPER PATTERN] Parameters, bounds, weights and thresholds have data/rule sources and sensitivity analysis.
- [CROSS-PAPER PATTERN] Regression/classification/time-series validation uses suitable residuals, metrics, split and uncertainty.
- [CROSS-PAPER PATTERN] Simulation/stochastic outputs have repeated seeds, moment/distribution checks and convergence.
- [CROSS-PAPER PATTERN] Multi-question handoffs preserve units, schema and uncertainty.
- [CROSS-PAPER PATTERN] Figures each support one necessary evidence claim with readable labels.
- [CROSS-PAPER PATTERN] Decision recommendations state assumptions, trade-offs and practical limits.
- [CROSS-PAPER PATTERN] Negative/weak results are reported without changing definitions or cherry-picking.

## MINOR

- [CROSS-PAPER PATTERN] Notation is defined once and used consistently.
- [CROSS-PAPER PATTERN] Captions identify sample/scenario, metric and purpose.
- [CROSS-PAPER PATTERN] Significant digits reflect input/model uncertainty.
- [CROSS-PAPER PATTERN] Background and generic algorithm exposition do not crowd out formulation/evidence.
- [CROSS-PAPER PATTERN] Limitations name observed weaknesses rather than generic future work.
- [CROSS-PAPER PATTERN] Reproduction records code, data provenance, environment, seeds and generated artifact paths.

## Verdict Rule

[ANALYST INFERENCE] Any unresolved CRITICAL item blocks submission. MAJOR items require repair or an explicit, scope-limiting caveat. MINOR items can remain only when they do not obscure verification.
