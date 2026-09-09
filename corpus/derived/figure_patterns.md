# Figure Patterns

**Rule:** [CROSS-PAPER PATTERN] One Figure = One Evidence Purpose.

| Purpose | Useful figure/table | Evidence question | Corpus example/lesson |
|---|---|---|---|
| EDA | distributions, missingness, time/regime plot | What structure/problem is present? | [CROSS-PAPER PATTERN] Waveform features and traffic-state curves motivate later models |
| mechanism | geometry, state diagram, cut tree, dependency graph | Why does the equation/model follow? | [CROSS-PAPER PATTERN] DFT butterflies, cutting tree and coordinate frames |
| workflow | typed pipeline with reused artifacts | How do questions connect? | [CROSS-PAPER PATTERN] Image→trace→plane and video→state→rule chains |
| core result | compact answer table/layout/schedule/profile | What is the answer, with units? | [CROSS-PAPER PATTERN] Sheet layouts, CPLEX–GA roster metrics, folded profiles |
| validation | predicted-vs-actual, residuals, confusion matrix, invariant table | Is it correct/generalizable? | [CROSS-PAPER PATTERN] Energy/angular momentum and exact-small comparisons are stronger than decorative fits |
| sensitivity | parameter/step/sample-count response | Does the claim survive choices? | [CROSS-PAPER PATTERN] JRC sampling curve and DFT precision–complexity tables |
| optimization | Pareto front, gap/bound, convergence with seed bands | What trade-off/quality did search find? | [CROSS-PAPER PATTERN] Pareto fronts need feasible highlighted points and post-checks |
| decision | action map/roster/layout with trigger/assumption | How is the result used? | [CROSS-PAPER PATTERN] Lane rule, drilling map and cut coordinates |

## Figure Acceptance Test

1. [CROSS-PAPER PATTERN] Caption states question, sample/scenario, unit and evidence claim.
2. [CROSS-PAPER PATTERN] Axes/legends identify observed, fitted, validation and simulated data.
3. [CROSS-PAPER PATTERN] Numeric tables and plots agree.
4. [CROSS-PAPER PATTERN] A validation plot uses held-out/independent evidence where required.
5. [CROSS-PAPER PATTERN] An optimization plot marks feasible bounds and the selected point.
6. [CROSS-PAPER PATTERN] A stochastic plot includes repeated-run uncertainty, not one realization.
7. [ANALYST INFERENCE] Remove a figure if its claim is already made more precisely by a table and it adds no mechanism, comparison or diagnostic.

## Anti-Patterns

- [CROSS-PAPER PATTERN] Many near-duplicate preprocessing panels without quantitative selection evidence.
- [CROSS-PAPER PATTERN] Smooth surfaces/heatmaps called “validation” when they only visualize the model itself.
- [CROSS-PAPER PATTERN] Convergence curves without baselines, gaps or multiple seeds.
- [CROSS-PAPER PATTERN] Predicted-vs-actual plots based on leaked random splits.
- [ANALYST INFERENCE] Visual polish cannot repair a missing experimental control, probability calibration or feasibility check.
