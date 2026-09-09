# Optimization Patterns

## Nine-Part Optimization Contract

1. **Decision Variables.** [CROSS-PAPER PATTERN] Use variables for controllable actions: crew–flight binaries, stack memberships, operating settings. Observed treatments and objective weights are not ordinary design choices.
2. **Objective.** [CROSS-PAPER PATTERN] State direction, unit and priority. GMCM-2023-B exposes RMSE–hardware conflict; GMCM-2021-F exposes coverage–cost–balance priorities.
3. **Constraints.** [CROSS-PAPER PATTERN] Translate every validity rule, including domain, capacity, continuity, qualification, safety and categorical choices.
4. **Feasibility.** [CROSS-PAPER PATTERN] Define an independent checker before solving. Layout coordinates in GMCM-2022-B and exact-small cases in GMCM-2021-F are useful forms.
5. **Solver.** [CROSS-PAPER PATTERN] Explain why exact, continuous local, decomposition or heuristic search matches size/structure. A GA is not the mathematical model.
6. **Optimal Solution.** [CROSS-PAPER PATTERN] Report objective vector, variables, units, runtime and status/gap. Say “best found” when no certificate exists.
7. **Post-Optimization Validation.** [CROSS-PAPER PATTERN] Replay constraints, recompute objectives outside solver code, and validate surrogate candidates with mechanism/experiment.
8. **Sensitivity/Robustness.** [CROSS-PAPER PATTERN] Vary weights, bounds, uncertain coefficients, seeds and demand/scenario inputs.
9. **Practical Interpretation.** [CROSS-PAPER PATTERN] Convert variables to a layout, roster, operating condition or rule with assumptions visible.

## Recurring Structures

- [CROSS-PAPER PATTERN] **Hierarchical assignment:** part→stack→stripe→sheet and crew→flight→duty→rotation reduce conceptual complexity but require link constraints.
- [CROSS-PAPER PATTERN] **Lexicographic priorities:** coverage before deadhead/cost should be solved lexicographically or with proved dominating weights; subjective AHP can change intent.
- [CROSS-PAPER PATTERN] **Multiobjective fronts:** loss versus energy and error versus hardware need Pareto reporting before selecting a compromise.
- [CROSS-PAPER PATTERN] **Surrogate optimization:** encode every decision input exactly as during training, restrict to validated support, quantify predictive uncertainty near candidates, then post-check.
- [CROSS-PAPER PATTERN] **Sequential decomposition:** batching→packing can scale, but report the lost joint-search opportunity.

## Stop Conditions

- [ANALYST INFERENCE] Do not publish an optimum if any bound is violated, units disagree, the objective weight is self-selected without policy meaning, or a surrogate has not been checked near the solution.
- [ANALYST INFERENCE] Do not infer solver robustness from one run; do not infer global optimality from convergence; do not call a heuristic sensor layout an optimization without an objective and alternatives.
