# Metadata

- [PAPER EVIDENCE] contest: 中国研究生数学建模竞赛
- [PAPER EVIDENCE] year: 2021
- [PAPER EVIDENCE] problem code: F
- [PAPER EVIDENCE] paper title: 航空公司机组优化排班问题探析
- [PAPER EVIDENCE] source PDF: `/home/soren/zhonghui/skillpack/F2021.pdf`
- [PAPER EVIDENCE] page count: 33
- [PAPER EVIDENCE] award level: null
- [PAPER EVIDENCE] award verified: false

# One-Sentence Value

[ANALYST INFERENCE] Learn incremental large-scale scheduling—assignment, then duties, then rotations—with explicit binary constraints and small-instance exact-solver checks, while preserving lexicographic priorities and feasibility.

# Problem Decomposition

## Q1

- [PAPER EVIDENCE] Assign crew directly to flights, prioritizing covered flights, then fewer deadheads, then fewer substitute qualifications.
- [ANALYST INFERENCE] Essence: integrated 0–1 multicommodity path/assignment scheduling.
- [PAPER EVIDENCE] Inputs include crew qualifications/bases and flight time/location; output x_ijt plus role, coverage and connection decisions.
- [ANALYST INFERENCE] Establishes identities, spatial continuity and minimum connection constraints inherited by Q2/Q3.

## Q2

- [PAPER EVIDENCE] Add duties, duty cost and balance while retaining Q1 goals.
- [ANALYST INFERENCE] Essence: multiobjective assignment with duty-duration, flight-time and rest constraints.
- [PAPER EVIDENCE] Output includes coverage, utilization, duration distribution and total duty cost.

## Q3

- [PAPER EVIDENCE] Add rotations beginning/ending at base, rotation cost and balance.
- [ANALYST INFERENCE] Essence: integrated crew rostering with multi-day resource constraints.
- [PAPER EVIDENCE] New limits cover rotation duration, intervening days off and consecutive duty days.

# Overall Modeling Chain

[PAPER EVIDENCE] Crew/flight network → role and connection assignment → add duty time/rest/cost/balance → add base-return rotations/cost/balance → scalarize priorities → exact CPLEX on small A and improved GA on A/B → coverage/cost/utilization reports.

# Mathematical Structure

## State Variables

- [PAPER EVIDENCE] Crew location, active connection/duty/rotation, accumulated flight/duty/rotation time and qualification role.

## Decision Variables

- [PAPER EVIDENCE] x_ijt crew–flight–date assignment; y_j flight covered; m/n/k/z captain/copilot/deadhead/substitute roles; l_ijj't flight succession; nonnegative u_i balance auxiliaries.

## Parameters

- [PAPER EVIDENCE] Flight times/airports, crew bases/qualifications and costs; MinCT, MaxBlk, MaxDP, MinRest, MaxDH, MaxTAFB, MaxSuccon and MinVacDay.

## Objective Functions

- [PAPER EVIDENCE] Lexical prose priority expands from three objectives in Q1 to five in Q2 and seven in Q3: maximize covered flights; minimize deadheads/substitutions, duty cost/imbalance and rotation cost/imbalance.

## Constraints

- [PAPER EVIDENCE] Exactly one qualified captain/copilot on a covered flight; no crew on uncovered flights; role exclusivity; airport continuity; predecessor/successor; base departure/return; minimum connection/rest; maximum duty/flight/rotation/consecutive-day limits.

## Core Relationships

- [PAPER EVIDENCE] Binary succession variables link space-time paths; absolute deviations from mean time are linearized with u_i; utilization is covered-flight time divided by duty time.

## Assumptions

- [PAPER EVIDENCE] Crew can combine freely; uncovered flights are allowed and then carry no crew; deadheading is allowed; scheduled times are fixed.

# Model Selection Logic

- [PAPER EVIDENCE] Linear binary modeling is selected to state business rules explicitly and avoid limitations of two-stage pairing/allocation.
- [PAPER EVIDENCE] GA is used because the integrated problem is NP-hard and B is too large for CPLEX; custom matrix coding, adaptive crossover/mutation and parent–child fusion target premature convergence.
- [PAPER EVIDENCE] AHP supplies weights to scalarize multiple objectives.
- [ANALYST INFERENCE] The question states objective priority, so lexicographic optimization or provably dominating weights would be safer than subjective AHP trade-offs.
- [ANALYST INFERENCE] A constructive greedy/network baseline and repeated GA runs are missing.

# Solver / Algorithm

- [PAPER EVIDENCE] Model: 0–1 linear integrated crew assignment/duty/rotation formulation with seven weighted objectives.
- [PAPER EVIDENCE] Solvers: IBM ILOG CPLEX 12.8 exact optimization for A, and MATLAB improved GA (1500 generations, crossover 0.8, mutation 0.1) for A/B.
- [ANALYST INFERENCE] A feasible GA schedule is not an optimum certificate; on Q2/Q3 A, CPLEX is explicitly better.

# Validation Audit

| Validation | Found? | Evidence | Assessment |
|---|---|---|---|
| baseline | FOUND | [PAPER EVIDENCE] CPLEX exact solution for A compared with GA | Strong small-instance reference |
| train/test | NOT FOUND | NOT FOUND | Not applicable |
| time split | NOT FOUND | NOT FOUND | No rolling operational test |
| residual | NOT FOUND | NOT FOUND | Not applicable |
| error metric | FOUND | [PAPER EVIDENCE] Coverage, deadheads, substitutions, costs, utilization and runtime | Direct multiobjective outcomes |
| model comparison | FOUND | [PAPER EVIDENCE] CPLEX vs GA on all A questions | Q1 equal; CPLEX better Q2/Q3 |
| sensitivity | NOT FOUND | NOT FOUND | AHP weights and GA parameters are not varied |
| perturbation | NOT FOUND | NOT FOUND | No delays, absences or demand disruption |
| robustness | NOT FOUND | NOT FOUND | “Robust” is claimed without multi-seed distributions |
| simulation | NOT FOUND | NOT FOUND | Schedule construction is optimization, not simulation |
| feasibility check | PARTIAL | [PAPER EVIDENCE] Constraint repair and aggregate schedule metrics | Full independent constraint replay is NOT FOUND; table has impossible min/mean/max ordering in Q2 |
| practical validation | PARTIAL | [PAPER EVIDENCE] B-scale runtimes 191–199 minutes and operational indicators | No airline deployment or disruption test |

# Figures and Tables

- [PAPER EVIDENCE] Chromosome/crossover diagrams (solver mechanism, Q1): explain the crew×flight encoding.
- [PAPER EVIDENCE] CPLEX–GA tables for A (comparison/validation, Q1–Q3): distinguish exact and heuristic quality.
- [PAPER EVIDENCE] B coverage/cost/utilization tables (result/decision): show scale feasibility and operational trade-offs.
- [ANALYST INFERENCE] Q2 reports maximum duty duration 4.4 below mean 4.8, a numeric-consistency warning visible only because the table is detailed.

# Abstract Architecture

- [PAPER EVIDENCE] Minimal background, then Q1–Q3 increments, model/solver names and coverage counts for A/B.
- [ANALYST INFERENCE] Worth copying: make added constraints/objectives visible per question. Avoid: calling GA robust based on one run or blurring a weighted sum with the stated priority order.

# Strengths

- [PAPER EVIDENCE] Complex engineering rules are explicitly represented rather than hidden in a generator.
- [PAPER EVIDENCE] Each later question reuses and extends the earlier formulation.
- [PAPER EVIDENCE] Small-instance CPLEX comparison candidly shows where GA is worse.

# Weaknesses

- [ANALYST INFERENCE] Subjective AHP weights can violate lexicographic priorities and receive no sensitivity analysis.
- [ANALYST INFERENCE] Aggregate outputs do not prove every large schedule constraint was replayed independently.
- [ANALYST INFERENCE] One-run GA claims and inconsistent duration statistics weaken robustness/numeric credibility.
- [ANALYST INFERENCE] Q3’s added constraints drastically reduce A coverage, but trade-off interpretation is limited.

# Reusable Lessons

- [ANALYST INFERENCE] Build scheduling models in layers; name every operational rule; compare a heuristic to exact solutions on reduced instances; report feasibility and priority outcomes separately; replay constraints after solving.

# Do NOT Copy

- [ANALYST INFERENCE] Do not copy aviation duration limits, role assumptions, AHP matrices, chromosome size or GA settings. Do not replace a lexicographic requirement with weights unless dominance is proved or stakeholders authorize trade-offs.
