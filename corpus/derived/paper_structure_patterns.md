# Paper Structure Patterns

## Evidence-Led Spine

1. [CROSS-PAPER PATTERN] **Problem and deliverables:** restate outputs, not narrative.
2. [CROSS-PAPER PATTERN] **Global dependency map:** show Q1→Qn artifacts and units.
3. [CROSS-PAPER PATTERN] **Assumptions and notation:** localize assumptions by question; define state/decision/parameter roles.
4. [CROSS-PAPER PATTERN] **Per-question module:** problem → mathematical abstraction → assumptions/variables → formulation → selection rationale → solver/computation → numerical result → interpretation → validation → question conclusion → handoff to next question.
5. [CROSS-PAPER PATTERN] **Cross-question audit:** reconcile numbers, units, domains and inherited uncertainty.
6. [CROSS-PAPER PATTERN] **Decision/conclusion:** answer each prompt at the supported confidence level.
7. [CROSS-PAPER PATTERN] **Limitations/reproducibility:** parameters, seeds, code/data artifacts and failed routes.

## Strong Structural Moves

- [CROSS-PAPER PATTERN] Incremental formulation avoids repetition: GMCM-2021-F adds only duty then rotation components.
- [CROSS-PAPER PATTERN] A structural lemma can organize the whole solution: GMCM-2023-B’s butterfly factorization.
- [CROSS-PAPER PATTERN] Intermediate outputs should be inspectable: GMCM-2022-B coordinates and GMCM-2025-C trace/plane artifacts.
- [CROSS-PAPER PATTERN] Mechanism and correction budgets belong before simulation: GMCM-2024-F.
- [CROSS-PAPER PATTERN] A prediction chapter must explain how predictions become decisions: GMCM-2024-C/GMCM-2024-E.

## Structural Failure Modes

- [CROSS-PAPER PATTERN] Repeating a model family for each question without an artifact dependency creates fragmentation.
- [CROSS-PAPER PATTERN] Mixing formulation and solver language hides what was optimized.
- [CROSS-PAPER PATTERN] Placing validation only in a generic final “model evaluation” section leaves individual claims unaudited.
- [ANALYST INFERENCE] A core equation needs a local reason before it and variable/meaning/downstream-use explanation after it; a detached equation sequence is not mathematical narrative.
- [ANALYST INFERENCE] Each question should close with its answer, strongest verified result, supported conclusion, limitation and concrete artifact passed forward.
- [CROSS-PAPER PATTERN] A long strengths section cannot substitute for limitations tied to actual results.
- [ANALYST INFERENCE] Each major numeric claim should have one provenance route: question → run/artifact → table/figure → abstract/conclusion. Duplicate manual transcription invites inconsistency.
