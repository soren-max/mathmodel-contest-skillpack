# Problem Decomposition Patterns

## The Translation Contract

[CROSS-PAPER PATTERN] Before naming an algorithm, translate each question through this contract:

| Layer | Required question | Evidence in corpus |
|---|---|---|
| Real requirement | What must be explained, predicted, constructed or decided? | Packing sheets, coverage, loss, connectivity, lane action and photon arrivals are distinct deliverables |
| Mathematical object | Graph, set, curve, field, matrix, state, point process or feasible region? | GMCM-2023-B starts from matrix recursion; GMCM-2021-F from a space-time assignment network |
| Input | What is observed/given, at what unit/granularity? | GMCM-2024-F’s reference frames and GMCM-2023-E’s patient/visit levels show why granularity matters |
| Output | What artifact answers the question? | Coordinate layouts, probabilities/scores, schedules, Pareto points, fitted planes or event times |
| State | What summarizes the system before action? | Traffic occupancy, remaining sheet capacity, satellite state, fracture plane |
| Decision | What can the solver actually choose? | Crew assignments, batches, operating settings, lane state; do not call observed treatment a decision |
| Objective | What direction and unit define “better”? | Coverage/cost, RMSE/complexity, loss/energy |
| Constraints | What makes an answer invalid? | Capacity, continuity, qualifications, domain bounds, geometry and safety |

## Multi-Question Progressions

- [CROSS-PAPER PATTERN] **Representation → construction → extension:** exact DFT structure in GMCM-2023-B Q1 becomes integer approximation in Q2/Q3 and broader construction in Q4/Q5.
- [CROSS-PAPER PATTERN] **Base feasibility → operational layers:** GMCM-2021-F adds duty then rotation rules; GMCM-2022-B reuses packing inside batching.
- [CROSS-PAPER PATTERN] **Measurement → state → prediction → decision:** GMCM-2024-E converts video into traffic state, forecast and control.
- [CROSS-PAPER PATTERN] **Feature extraction → geometry → derived index → uncertainty decision:** GMCM-2025-C propagates masks into traces, JRC, planes and drilling.
- [CROSS-PAPER PATTERN] **Physical baseline → multivariable surrogate → optimization:** GMCM-2024-C corrects Steinmetz, trains a broader predictor, then embeds it in Q5.
- [CROSS-PAPER PATTERN] **Mechanism → correction → stochastic simulation:** GMCM-2024-F builds state/frame conversion, delay corrections and photon arrivals.

## Dependency Ledger

[CROSS-PAPER PATTERN] For every edge Q_i→Q_j record: upstream artifact, units/schema, uncertainty, transformations, and downstream use. This exposes broken links such as a classifier never used in the decision, or a predictor optimized outside its training domain.

[ANALYST INFERENCE] A chain is not automatically good. GMCM-2024-C and GMCM-2025-C show that downstream stages can amplify upstream leakage or arbitrary probability mappings. Audit every interface.

## Decomposition Test

1. [CROSS-PAPER PATTERN] Can every question’s output be written as a file/table/number/decision?
2. [CROSS-PAPER PATTERN] Does each later question explicitly consume an earlier output or state why it is independent?
3. [CROSS-PAPER PATTERN] Are state variables separated from controllable decisions and observed covariates?
4. [CROSS-PAPER PATTERN] Is feasibility defined before the solver?
5. [CROSS-PAPER PATTERN] Is uncertainty retained rather than silently collapsed?
6. [ANALYST INFERENCE] If a question adds only another algorithm but no new mathematical object, constraint or evidence, the decomposition is probably algorithm-led.
