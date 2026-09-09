# Metadata

- [PAPER EVIDENCE] contest: 中国研究生数学建模竞赛
- [PAPER EVIDENCE] year: 2024
- [PAPER EVIDENCE] problem code: F
- [PAPER EVIDENCE] paper title: X射线脉冲星时间转换建模与光子序列仿真
- [PAPER EVIDENCE] source PDF: `/home/soren/zhonghui/skillpack/F2024.pdf`
- [PAPER EVIDENCE] page count: 53
- [PAPER EVIDENCE] award level: null
- [PAPER EVIDENCE] award verified: false

# One-Sentence Value

[ANALYST INFERENCE] Learn to grow a physical model from coordinate transforms to correction budgets and a nonhomogeneous Poisson simulator, while checking units, reference frames and stochastic fidelity at every interface.

# Problem Decomposition

## Q1

- [PAPER EVIDENCE] Convert orbital elements into XPNAV-1 GCRS position/velocity and validate consistency.
- [ANALYST INFERENCE] Essence: deterministic orbital mechanics plus orthogonal coordinate transformation.
- [PAPER EVIDENCE] Output is r=(1274.91341,−1848.8519,6507.2626) km and v=(−6.2107,3.7461,2.2763) km/s.

## Q2

- [PAPER EVIDENCE] Compute vacuum geometric (Roemer) delay from satellite to SSB at MJD 57062.
- [ANALYST INFERENCE] Essence: reference-frame translation and ray projection.
- [PAPER EVIDENCE] The model combines ephemeris Earth/Sun position, satellite position and pulsar RA/Dec direction.

## Q3

- [PAPER EVIDENCE] Refine delay for pulsar proper motion, Shapiro delay, gravitational redshift and special-relativistic clock dilation at another epoch.
- [ANALYST INFERENCE] Essence: additive path corrections plus multiplicative time-scale corrections.
- [PAPER EVIDENCE] Individual solar-system-body contributions are tabulated; the Sun dominates at about 10⁻⁴ s scale.

## Q4

- [PAPER EVIDENCE] Simulate 10 s of Crab photon arrivals, fold a pulse profile, and improve precision.
- [ANALYST INFERENCE] Essence: phase-modulated nonhomogeneous Poisson point process.
- [PAPER EVIDENCE] Intensity is background plus scaled profile; inverse cumulative sampling generates events; phase folding uses frequency derivatives and delay correction; refinement adds Doppler, second derivative and smaller satellite step.

# Overall Modeling Chain

[PAPER EVIDENCE] Orbital elements → PQW state → GCRS/SSB coordinates → vacuum projection delay → physical correction budget → corrected phase/intensity → nonhomogeneous Poisson event simulation → phase folding → finer physical/discretization model.

# Mathematical Structure

## State Variables

- [PAPER EVIDENCE] Satellite position/velocity, pulsar direction, propagation delay, pulse phase, instantaneous intensity and event times.

## Decision Variables

- [ANALYST INFERENCE] This is a forward physical/simulation problem; numerical step size, bin count and sampling scheme are method choices, not operational decisions.

## Parameters

- [PAPER EVIDENCE] Orbital elements, gravitational constants/masses/ephemerides, c, RA/Dec/proper motion, pulsar f/ḟ/f̈, detector area, λb=1.54 and λs=10λb, Tobs=10 s.

## Objective Functions

- [ANALYST INFERENCE] No optimization objective; accuracy is pursued by reducing omitted-physics and discretization errors.

## Constraints

- [PAPER EVIDENCE] Two-body orbit assumptions, reference-frame definitions, positive point-process intensity, observation interval and phase modulo one.

## Core Relationships

- [PAPER EVIDENCE] Orthogonal rotations preserve energy/angular momentum; Roemer delay is a projected distance divided by c; proper motion updates direction; relativistic terms correct delay/time scale; integrated intensity defines NHPP counts; polynomial phase folds events.

## Assumptions

- [PAPER EVIDENCE] Earth gravity is the only satellite force in Q1; body rotation/oblateness is negligible; pre-solar-system propagation errors cancel between satellite and SSB.

# Model Selection Logic

- [PAPER EVIDENCE] Each coordinate transform is chosen because inputs and desired outputs live in different frames; conservation laws are invariant checks.
- [PAPER EVIDENCE] Correction terms are added from explicit physical mechanisms and their magnitudes are tabulated.
- [PAPER EVIDENCE] NHPP is chosen because photon rate changes with pulse phase; phase folding recovers the periodic profile.
- [ANALYST INFERENCE] The architecture is well matched, but some formulas/units and the proposed exponential replacement for inverse-NHPP sampling need stricter derivation and benchmark validation.
- [ANALYST INFERENCE] A baseline should compare simulated count, interarrival and folded-profile statistics against analytical expectations over many seeds.

# Solver / Algorithm

- [PAPER EVIDENCE] Models: Keplerian state conversion, geometric/relativistic delay, polynomial spin phase and NHPP photon process.
- [PAPER EVIDENCE] Algorithms: matrix rotations, JPL ephemeris lookup, celestial-grid traversal, per-body correction summation, inverse cumulative intensity sampling, histogram phase folding and smaller-step refined simulation.

# Validation Audit

| Validation | Found? | Evidence | Assessment |
|---|---|---|---|
| baseline | PARTIAL | [PAPER EVIDENCE] Vacuum delay precedes corrected delay; simple and refined simulators are contrasted | No trusted timing package/analytical point-process benchmark |
| train/test | NOT FOUND | NOT FOUND | Not applicable |
| time split | NOT FOUND | NOT FOUND | Not a learned forecast |
| residual | NOT FOUND | NOT FOUND | No residual against observed arrival times |
| error metric | PARTIAL | [PAPER EVIDENCE] Component magnitudes and qualitative profile similarity | No quantitative profile distance or stochastic confidence interval |
| model comparison | PARTIAL | [PAPER EVIDENCE] Base vs corrected/finer variants | Improvements are not measured on repeated simulations |
| sensitivity | PARTIAL | [PAPER EVIDENCE] Satellite step is reduced from 1 s to a pulse-scale step | No convergence curve over multiple steps |
| perturbation | NOT FOUND | NOT FOUND | Ephemeris/parameter uncertainty not propagated |
| robustness | NOT FOUND | NOT FOUND | Random seeds/repetitions and confidence bands NOT FOUND |
| simulation | FOUND | [PAPER EVIDENCE] NHPP photon times and folded profiles are generated | Central evidence, but stochastic validation is weak |
| feasibility check | PARTIAL | [PAPER EVIDENCE] Energy/angular-momentum invariants and correction magnitudes | Unit and cross-section number inconsistencies remain |
| practical validation | NOT FOUND | NOT FOUND | No comparison with independent XPNAV-1 arrival data/software |

# Figures and Tables

- [PAPER EVIDENCE] Coordinate/propagation geometry and workflow (mechanism, Q1–Q3): make frame transformations auditable.
- [PAPER EVIDENCE] Energy/angular-momentum calculations (validation, Q1): invariant checks across rotation.
- [PAPER EVIDENCE] Per-body Shapiro/redshift table (mechanism/sensitivity, Q3): supports term prioritization.
- [PAPER EVIDENCE] Satellite displacement, phase, simulated and folded profiles (simulation/validation, Q4): show signal construction and recovery qualitatively.
- [PAPER EVIDENCE] RA/Dec delay heatmap (sensitivity/completeness, Q2): explores directional geometry, not empirical accuracy.

# Abstract Architecture

- [PAPER EVIDENCE] The abstract moves through all four questions, reports Q1 state vectors and delay values, and ends with three simulation refinements.
- [ANALYST INFERENCE] Worth copying: couple every physical refinement to a scale or output. Avoid: reporting inconsistent delay values (abstract/body) or “higher precision” without a quantitative comparison.

# Strengths

- [PAPER EVIDENCE] The four questions form one physical-computational chain.
- [PAPER EVIDENCE] Conservation invariants validate coordinate transformations.
- [PAPER EVIDENCE] Correction terms are decomposed by mechanism/body, enabling magnitude triage.
- [PAPER EVIDENCE] The stochastic process is stated explicitly instead of adding arbitrary noise.

# Weaknesses

- [ANALYST INFERENCE] Q1 angular-momentum notation/units are internally inconsistent in extracted text, and Q2 delay differs between abstract and body.
- [ANALYST INFERENCE] Q3’s corrected delay shift and additive/multiplicative formula need independent dimensional/physical verification.
- [ANALYST INFERENCE] Replacing uniform inverse-transform draws with exponential draws is not by itself a valid general NHPP improvement.
- [ANALYST INFERENCE] Visual profile resemblance, one random realization and ambiguous stated fine step (“0.033ms” versus surrounding pulse-period language) do not establish higher accuracy.

# Reusable Lessons

- [ANALYST INFERENCE] Track reference frames and units as types; validate transforms with invariants; build a correction budget by magnitude; validate a point-process simulator through counts, interarrivals and repeated folded profiles; run step-size convergence.

# Do NOT Copy

- [ANALYST INFERENCE] Do not copy Crab/XPNAV constants, two-body assumptions, correction composition, bin counts or exponential-event shortcut. Do not treat a dense heatmap or visually similar realization as correctness evidence.
