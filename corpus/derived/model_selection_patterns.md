# Model Selection Patterns

## Choose from Structure and Evidence

| Model family | Use when | Required evidence before selection | Corpus anchors |
|---|---|---|---|
| Mechanism model | Conserved quantities, geometry or physical law determines relationships | Units, frames, assumptions, invariant/limit checks | [CROSS-PAPER PATTERN] GMCM-2024-F; Steinmetz baseline in GMCM-2024-C |
| Statistical model | Inference/uncertainty and interpretable covariate relations matter | Sampling unit, distribution/dependence, residuals, intervals | [CROSS-PAPER PATTERN] Weaknesses in GMCM-2023-E show the cost of ignoring dependence |
| Machine learning | Labeled data and genuine held-out generalization support flexible mapping | Leakage-safe split, simple baseline, calibration/shift test | [CROSS-PAPER PATTERN] GMCM-2025-C correctly abandons ML when labels/data do not support it |
| Surrogate model | A costly/unknown response must enter optimization | Decision coverage in training support, error near optima, post-check | [CROSS-PAPER PATTERN] GMCM-2024-C shows both the chain and the missing post-check risk |
| ODE/dynamic state | Rates, stocks and feedback evolve continuously | Initial conditions, conservation, identifiability, time validation | [CROSS-PAPER PATTERN] GMCM-2024-E uses a conservation stock; full ODE was not needed |
| Stochastic process | Random event times/counts or uncertainty are intrinsic | Distributional rationale, repeated simulation, moment/quantile checks | [CROSS-PAPER PATTERN] NHPP in GMCM-2024-F and parameter MC in GMCM-2025-C |
| Integer program | Choices, memberships, sequencing or activation are discrete | Complete variables/objectives/constraints and feasibility replay | [CROSS-PAPER PATTERN] GMCM-2022-B and GMCM-2021-F |
| Continuous optimization | Differentiable parameters or smooth geometry are estimated | Objective surface, bounds, initialization and residual checks | [CROSS-PAPER PATTERN] Sinusoid/plane fits in GMCM-2025-C |
| Heuristic solver | Exact search is demonstrably too costly | Exact/reduced baseline, repeated seeds, gaps/bounds and feasibility | [CROSS-PAPER PATTERN] GMCM-2021-F does exact-small/GA-large; GMCM-2022-B provides a lower bound |

## Model Selection Decision Checklist

1. [CROSS-PAPER PATTERN] Name the mathematical object before the algorithm.
2. [CROSS-PAPER PATTERN] Write the simplest mechanism/statistical baseline that could answer the deliverable.
3. [CROSS-PAPER PATTERN] Verify that sample size, labels, independence and variable support justify added flexibility.
4. [CROSS-PAPER PATTERN] Separate the mathematical model from the numerical solver.
5. [CROSS-PAPER PATTERN] State what evidence would falsify the choice: residual pattern, leakage-safe holdout, invariant failure, infeasibility or unstable seeds.
6. [CROSS-PAPER PATTERN] Prefer structural decomposition when algebra/geometry exposes one, as in GMCM-2023-B and GMCM-2025-C.
7. [ANALYST INFERENCE] Reject algorithm stacking whose incremental gain is smaller than its explanation, validation or reproducibility cost.
8. [ANALYST INFERENCE] Historical exemplars generate candidates only; current question, data and constraints make the final selection.
