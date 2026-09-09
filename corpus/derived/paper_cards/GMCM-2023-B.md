# Metadata

- [PAPER EVIDENCE] contest: 中国研究生数学建模竞赛
- [PAPER EVIDENCE] year: 2023
- [PAPER EVIDENCE] problem code: B
- [PAPER EVIDENCE] paper title: DFT类矩阵的整数分解逼近：解析与优化方法
- [PAPER EVIDENCE] source PDF: `/home/soren/zhonghui/skillpack/B2023.pdf`
- [PAPER EVIDENCE] page count: 74
- [PAPER EVIDENCE] award level: null
- [PAPER EVIDENCE] award verified: false

# One-Sentence Value

[ANALYST INFERENCE] Learn to derive an algorithm from algebraic structure—exact factorization first, quantized approximation second—before reaching for generic optimization.

# Problem Decomposition

## Q1

- [PAPER EVIDENCE] Determine whether DFT matrices can be factored into sparse low-complexity factors and characterize hardware cost.
- [ANALYST INFERENCE] Essence: exact structured matrix factorization.
- [PAPER EVIDENCE] Input: F_N with N=2^t; output: radix-2 butterfly factors and permutation with zero reconstruction error.
- [ANALYST INFERENCE] Supplies support structure for later integer approximation.

## Q2

- [PAPER EVIDENCE] Approximate DFT factors when entries must lie in a bounded integer/complex grid but the two-nonzero constraint is relaxed.
- [ANALYST INFERENCE] Essence: nonconvex quantized matrix-factor approximation.
- [PAPER EVIDENCE] Output is product factors, scale β, RMSE and hardware complexity for F4–F32.

## Q3

- [PAPER EVIDENCE] Enforce both integer entries and at most two nonzeros per row.
- [ANALYST INFERENCE] Essence: fixed-support sparse quantization; it combines a Weyl-based analytic route for F8 with BSMHF numerical search.
- [ANALYST INFERENCE] Directly tightens Q1/Q2 rather than restarting.

## Q4

- [PAPER EVIDENCE] Approximate F4⊗F8 under a hardware-complexity cap.
- [ANALYST INFERENCE] Essence: exploit Kronecker structure and approximate only irrational subfactors; compare practical enumeration with high-precision Diophantine approximation.

## Q5

- [PAPER EVIDENCE] Establish arbitrary-accuracy existence for general DFT-like matrices and give F8/F16 constructions.
- [ANALYST INFERENCE] Essence: bridge constructive proof and bounded integer search, while exposing the cost of precision.

# Overall Modeling Chain

[PAPER EVIDENCE] DFT algebra → Cooley–Tukey butterfly factorization → isolate irrational entries → integer-grid projection/Diophantine approximation → fixed-support optimization → RMSE–hardware trade-off → existence argument.

# Mathematical Structure

## State Variables

- [PAPER EVIDENCE] Intermediate matrix products and residual matrices at each factorization layer.

## Decision Variables

- [PAPER EVIDENCE] Sparse factors A_k, their supports and integer complex entries, scale β, rotation/exponent counts and sometimes factor count K.

## Parameters

- [PAPER EVIDENCE] Matrix order N, integer bound q, allowed nonzeros per row, number of factors K, tolerance ε and hardware budget C=qL.

## Objective Functions

- [PAPER EVIDENCE] Minimize normalized Frobenius RMSE between F_N and β∏A_k, subject to representation/hardware restrictions.

## Constraints

- [PAPER EVIDENCE] Integer-grid complex entries, no more than two row nonzeros where required, positive β, prescribed support in BSMHF and hardware-complexity cap.

## Core Relationships

- [PAPER EVIDENCE] Radix-2 Cooley–Tukey decomposition gives exact sparse butterflies; Kronecker products localize approximation; Weyl equidistribution and Diophantine approximation supply integer approximants.

## Assumptions

- [PAPER EVIDENCE] N is often a power of two for the constructive route; β>0 prevents a trivial zero scaling; sequential hardware complexity is explicitly defined.

# Model Selection Logic

- [PAPER EVIDENCE] Exact algebra is used wherever DFT recursion exposes structure; this yields RMSE 0 for Q1 rather than an unnecessary search.
- [PAPER EVIDENCE] PALM/projection is used for alternating quantized factors; hierarchical initialization follows butterfly structure.
- [PAPER EVIDENCE] Weyl and Diophantine methods are used because only irrational rotations block exact integer factors.
- [ANALYST INFERENCE] Generic gradient or genetic search is a fallback, not the source of the model. This is highly matched to the mathematical problem.
- [ANALYST INFERENCE] Simple baselines should include nearest-grid rounding of exact butterfly factors and single-start alternating minimization; comparison is incomplete.

# Solver / Algorithm

- [PAPER EVIDENCE] Model: sparse integer matrix-product approximation under RMSE and hardware constraints.
- [PAPER EVIDENCE] Solvers/constructions: exact Cooley–Tukey factorization, PALM with grid projection, BSMHF fixed-support hierarchical fitting, SVD/gradient scale updates, Weyl search, prime-exponent genetic search and distributed GA.
- [ANALYST INFERENCE] Several algorithms implement distinct mathematical subcases; they are not interchangeable model names.

# Validation Audit

| Validation | Found? | Evidence | Assessment |
|---|---|---|---|
| baseline | PARTIAL | [PAPER EVIDENCE] A prior/simple gradient result is mentioned and exact Q1 is a reference | Baseline protocol is not consistently reproduced |
| train/test | NOT FOUND | NOT FOUND | Not relevant to deterministic approximation |
| time split | NOT FOUND | NOT FOUND | Not relevant |
| residual | PARTIAL | [PAPER EVIDENCE] Frobenius residual/RMSE is computed | No residual structure visualization |
| error metric | FOUND | [PAPER EVIDENCE] Normalized Frobenius RMSE and hardware complexity | Matches the stated approximation/cost objectives |
| model comparison | FOUND | [PAPER EVIDENCE] Analytic, PALM/BSMHF, enumeration and GA constructions are contrasted | Comparisons span different constraints, so read carefully |
| sensitivity | PARTIAL | [PAPER EVIDENCE] Factor/rotation counts and complexity–precision trade-offs are tabulated | Hyperparameter and initialization sensitivity are sparse |
| perturbation | NOT FOUND | NOT FOUND | No noisy-target perturbation |
| robustness | PARTIAL | [PAPER EVIDENCE] Several N and repeated GA convergence claims | Run distributions/seeds are NOT FOUND |
| simulation | FOUND | [PAPER EVIDENCE] Numerical matrix reconstructions for F4–F32 | Deterministic computational evidence |
| feasibility check | FOUND | [PAPER EVIDENCE] Entry bounds, support and complexity are checked for reported constructions | Giant Diophantine solutions are explicitly called impractical |
| practical validation | PARTIAL | [PAPER EVIDENCE] Hardware complexity is evaluated | No hardware implementation/runtime benchmark |

# Figures and Tables

- [PAPER EVIDENCE] Butterfly/Kronecker diagrams (mechanism, Q1/Q4): expose exact recursive structure.
- [PAPER EVIDENCE] RMSE and hardware tables across N/factor counts (result/comparison, Q2–Q5): show precision–cost trade-offs.
- [PAPER EVIDENCE] Rotation-number/error table and GA convergence plots (sensitivity/result): support numerical search behavior, but not global optimality.

# Abstract Architecture

- [PAPER EVIDENCE] The abstract proceeds question by question, names both analytic and optimization methods, and reports representative RMSE/complexity values.
- [ANALYST INFERENCE] Worth copying: foreground the mathematical insight, then quantitative trade-offs. Avoid compressing existence proofs and practical algorithms into one undifferentiated success claim.

# Strengths

- [PAPER EVIDENCE] Exact structure is exhausted before numerical optimization.
- [PAPER EVIDENCE] Precision and implementability are treated as competing objectives.
- [PAPER EVIDENCE] The paper explicitly rejects a very accurate but astronomically costly integer construction as practically useless.

# Weaknesses

- [ANALYST INFERENCE] Reproducible solver settings, seeds and runtimes are incomplete.
- [ANALYST INFERENCE] Some generality claims lean on proof sketches and fixed-support experiments rather than a fully comparable protocol.
- [PAPER EVIDENCE] Fixed supports create a precision floor and heuristic searches may be locally optimal.

# Reusable Lessons

- [ANALYST INFERENCE] Search for invariants, recursion and tensor structure first; isolate the truly hard irrational/discrete component; report both mathematical error and implementation cost; distinguish existence from practical construction.

# Do NOT Copy

- [ANALYST INFERENCE] Do not transplant butterfly supports, power-of-two assumptions, integer grids, hardware metric or GA exponent encoding to an unrelated matrix problem. Do not cite an existence construction as an executable design without a size/cost audit.
