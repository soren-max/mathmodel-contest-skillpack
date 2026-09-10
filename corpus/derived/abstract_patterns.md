# Abstract Patterns

## Competition Abstract Blueprint

1. [CROSS-PAPER PATTERN] **Background (1–2 sentences):** define the decision/scientific need and overall mathematical object; omit field history.
2. [CROSS-PAPER PATTERN] **Q1:** state Problem → Method → concrete Result. Model is part of Method; validation and meaning may strengthen the Result but do not replace it.
3. [CROSS-PAPER PATTERN] **Q2:** state Problem → Method → concrete Result, including what Q1 artifact is reused when material.
4. [CROSS-PAPER PATTERN] **Q3/Q4/Q5:** repeat Problem → Method → concrete Result, making dependencies and decision outputs explicit.
5. [CROSS-PAPER PATTERN] **Overall value:** one sentence on what the full chain enables, with its decisive assumption/limitation when material.
6. [CROSS-PAPER PATTERN] **Keywords:** mathematical objects and application, not an indiscriminate algorithm list.

## What the Corpus Shows

- [CROSS-PAPER PATTERN] Question-wise abstracts in GMCM-2022-B, GMCM-2021-F and GMCM-2024-F are easy to map back to deliverables.
- [CROSS-PAPER PATTERN] Core numbers make claims falsifiable: sheets/utilization, coverage/cost, RMSE/complexity and state vectors/delays.
- [CROSS-PAPER PATTERN] A final decision number is valuable only when feasibility and evidence survive audit; GMCM-2024-C and GMCM-2024-E show how an impressive number can overstate validation.
- [ANALYST INFERENCE] If body and abstract numbers differ, repair the body/result provenance first; do not choose the more attractive value.

## Common Abstract Failures

- [CROSS-PAPER PATTERN] Algorithm names without the mathematical object or selection reason.
- [CROSS-PAPER PATTERN] No concrete answer such as a number, class/rank/threshold or decision; when a result claim depends on a comparator or validation condition, omitting that support also makes the claim incomplete.
- [CROSS-PAPER PATTERN] Background longer than the actual question answers.
- [CROSS-PAPER PATTERN] Describing work performed while failing to answer the requested decision.
- [ANALYST INFERENCE] “Good performance”, “significant improvement” or “the model is effective” without a number, class/rank/threshold or engineering strategy does not count as a Result.
- [CROSS-PAPER PATTERN] “Significant/accurate/robust/optimal” without a supporting test, metric, bound or certificate.
- [CROSS-PAPER PATTERN] Turning correlation or conditional simulation into a causal/practical conclusion.
- [CROSS-PAPER PATTERN] Omitting negative outcomes that materially bound generalization.

## Final Abstract Audit

[ANALYST INFERENCE] Build `| Question | Problem | Method | Result | Status |`. A question passes only when all three required cells exist and agree with the body. Model stays inside Method; interpretation, engineering value and validation are optional strengthening. Every key number must map to a current `approved_for_paper: true` registry entry or be removed pending upstream verification.
