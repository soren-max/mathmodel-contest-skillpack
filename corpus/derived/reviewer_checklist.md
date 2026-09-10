# Corpus-Informed Reviewer Checklist

Mark each item **PASS**, **FAIL**, **NOT FOUND** or **NOT APPLICABLE**, with an artifact/page/table reference.

[ANALYST INFERENCE] Apply the current [Evidence-Calibrated Communication Policy](../../rubrics/evidence_calibrated_communication.md) for communication findings and severity. Evidence > Rhetoric; retain supported limitations and negative results.

## CRITICAL

- [CROSS-PAPER PATTERN] Every question has an explicit, traceable answer and units.
- [CROSS-PAPER PATTERN] State, decision variables, parameters, objectives and constraints are not conflated.
- [CROSS-PAPER PATTERN] Labels, positive class and metric formulas are fixed and internally consistent.
- [CROSS-PAPER PATTERN] Train/test separation respects patient, time, group and preprocessing boundaries; no leakage.
- [CROSS-PAPER PATTERN] Reported optimum/schedule/layout passes an independent feasibility and objective replay.
- [CROSS-PAPER PATTERN] Abstract, body, tables, figures and conclusion agree numerically.
- [ANALYST INFERENCE] Every key abstract number is an approved registry metric; evidence strength, negative results and causal boundaries survive rewriting.
- [CROSS-PAPER PATTERN] Probability/causal/optimality claims have calibration, identification or certificates; otherwise wording is downgraded.
- [CROSS-PAPER PATTERN] Mechanism equations have coherent units, frames, signs and limiting/invariant checks.

## MAJOR

- [ANALYST INFERENCE] Every question in the abstract has Problem, Method and a concrete Result. A missing element is MAJOR and still fails that question's abstract hard gate.
- [ANALYST INFERENCE] Extensive algorithm exposition, uninterpreted results, severe repeated claims and disconnected question narratives require content repair.
- [CROSS-PAPER PATTERN] Model choice is justified by structure/data and compared with a simpler baseline.
- [CROSS-PAPER PATTERN] Solver is distinguished from model; exact status, gap or “best found” language is reported.
- [CROSS-PAPER PATTERN] Parameters, bounds, weights and thresholds have data/rule sources and sensitivity analysis.
- [CROSS-PAPER PATTERN] Regression/classification/time-series validation uses suitable residuals, metrics, split and uncertainty.
- [CROSS-PAPER PATTERN] Simulation/stochastic outputs have repeated seeds, moment/distribution checks and convergence.
- [CROSS-PAPER PATTERN] Multi-question handoffs preserve units, schema and uncertainty.
- [CROSS-PAPER PATTERN] Figures each support one necessary evidence claim with readable labels.
- [ANALYST INFERENCE] Every core equation has a local reason before it and variable/meaning/downstream-use explanation after it.
- [ANALYST INFERENCE] Every core figure/table states Purpose, Observation, Interpretation and Implication.
- [ANALYST INFERENCE] Every question closes with answer, strongest verified result, conclusion, limitation and the artifact passed to the next question.
- [CROSS-PAPER PATTERN] Decision recommendations state assumptions, trade-offs and practical limits.
- [CROSS-PAPER PATTERN] Negative/weak results are reported without changing definitions or cherry-picking.

## MINOR

- [CROSS-PAPER PATTERN] Notation is defined once and used consistently.
- [CROSS-PAPER PATTERN] Captions identify sample/scenario, metric and purpose.
- [CROSS-PAPER PATTERN] Significant digits reflect input/model uncertainty.
- [CROSS-PAPER PATTERN] Background and generic algorithm exposition do not crowd out formulation/evidence.
- [ANALYST INFERENCE] Local awkward phrasing, mechanical connectors and isolated repeated sentence structures can be edited without changing evidence strength; extensive algorithm encyclopedia belongs under MAJOR.
- [CROSS-PAPER PATTERN] Limitations name observed weaknesses rather than generic future work.
- [CROSS-PAPER PATTERN] Reproduction records code, data provenance, environment, seeds and generated artifact paths.

## Verdict Rule

[ANALYST INFERENCE] Any unresolved CRITICAL item blocks submission. Abstract PMR and per-question narrative gates must pass even when the missing content is MAJOR; a caveat cannot replace a missing answer. Other MAJOR items require repair or an evidence-supported scope limitation. MINOR items can remain when they do not obscure verification; competition mode should not spend substantial time on them. VALID_LIMITATION is a supported boundary to retain, not a defect.
