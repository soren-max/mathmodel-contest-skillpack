# Metadata

- [PAPER EVIDENCE] contest: 中国研究生数学建模竞赛
- [PAPER EVIDENCE] year: 2025
- [PAPER EVIDENCE] problem code: C
- [PAPER EVIDENCE] paper title: 基于 Frangi 滤波的钻孔裂隙识别与三维概率重构
- [PAPER EVIDENCE] source PDF: `/home/soren/zhonghui/skillpack/C2025.pdf`
- [PAPER EVIDENCE] page count: 91
- [PAPER EVIDENCE] award level: null
- [PAPER EVIDENCE] award verified: false

# One-Sentence Value

[ANALYST INFERENCE] Learn a coherent image→geometry→roughness→3D uncertainty pipeline, especially the value of abandoning a leaking ML route, while auditing whether a probability is genuinely calibrated.

# Problem Decomposition

## Q1

- [PAPER EVIDENCE] Identify fracture pixels in ten borehole images without ground-truth labels.
- [ANALYST INFERENCE] Essence: prior-guided unsupervised curvilinear segmentation.
- [PAPER EVIDENCE] Input: images; output: binary masks via illumination normalization, Frangi filtering, Otsu, morphology and component filters.
- [PAPER EVIDENCE] A handcrafted-feature RF/SVM/XGBoost attempt is abandoned after leave-one-out failure and same-image leakage is identified.

## Q2

- [PAPER EVIDENCE] Fit sinusoidal fracture traces and restore missing parts.
- [ANALYST INFERENCE] Essence: connected-component clustering plus robust nonlinear curve fitting.
- [PAPER EVIDENCE] DBSCAN clusters y-centroids; sinusoidal parameters are fitted, outliers beyond kσ removed, then refitted.

## Q3

- [PAPER EVIDENCE] Calculate joint roughness coefficient (JRC) and study sampling/width relations.
- [ANALYST INFERENCE] Essence: geometric feature functional with discretization sensitivity.
- [PAPER EVIDENCE] Centerlines are detrended, RMS slope Z2 maps to JRC, gaps are length-weighted, and sample counts 10–200 are compared.

## Q4

- [PAPER EVIDENCE] Transform cylindrical traces to 3D planes, estimate inter-fracture connectivity and propose three new drilling locations.
- [ANALYST INFERENCE] Essence: geometric reconstruction plus Monte Carlo uncertainty propagation and heuristic sensor placement.

# Overall Modeling Chain

[PAPER EVIDENCE] Borehole image → line enhancement/segmentation → component clustering and sinusoid restoration → centerline/JRC extraction → cylindrical-to-3D transform and plane fit → uncertain normals/Monte Carlo pair scores → uncertainty map → drilling recommendation.

# Mathematical Structure

## State Variables

- [PAPER EVIDENCE] Pixel mask, component/cluster membership, fitted trace, centerline, JRC, plane normal, pairwise angle/distance and spatial uncertainty.

## Decision Variables

- [PAPER EVIDENCE] Segmentation thresholds/filters, cluster assignments, trace parameters and proposed borehole coordinates; Q4 drilling choice is selected from high-uncertainty positions.

## Parameters

- [PAPER EVIDENCE] Frangi scales, morphology settings, DBSCAN settings, fixed circumference/period 94.25, outlier multiplier k, sampling density and assumed normal-component standard deviations.

## Objective Functions

- [PAPER EVIDENCE] Nonlinear least-squares trace and plane fitting; Q4 informally seeks higher uncertainty reduction/coverage rather than solving a stated costed objective.

## Constraints

- [PAPER EVIDENCE] Borehole geometry, sinusoidal unwrapping, image artifact orientations and candidate spatial positions constrain reconstruction.

## Core Relationships

- [PAPER EVIDENCE] Cylindrical surface coordinates map to Cartesian 3D; RMS slope maps empirically to JRC; plane-normal angles and distances become pairwise connectivity scores.

## Assumptions

- [PAPER EVIDENCE] No segmentation truth is available; fractures appear as curvilinear structures; plane-normal coefficients are normal; their standard deviations rise with JRC.
- [ANALYST INFERENCE] The JRC-to-standard-deviation map and angle/distance-to-probability map are analyst choices, not calibrated probabilities.

# Model Selection Logic

- [PAPER EVIDENCE] Frangi filtering is selected because the target is line-like and labels are absent; deep/supervised learning is explicitly rejected after a failed small-data test.
- [PAPER EVIDENCE] Sinusoids arise from intersecting planar fractures with an unwrapped cylindrical wall; least squares therefore follows geometry.
- [PAPER EVIDENCE] Monte Carlo is selected to propagate uncertain plane parameters into pairwise geometric measures.
- [ANALYST INFERENCE] These selections fit the data and mechanism well until Q4, where uncalibrated mappings are called probabilities and drilling is not formulated as expected information gain.

# Solver / Algorithm

- [PAPER EVIDENCE] Models: multiscale ridge segmentation, sinusoidal trace model, RMS-slope JRC functional, plane reconstruction and stochastic parameter propagation.
- [PAPER EVIDENCE] Algorithms: Frangi/Otsu/morphology, DBSCAN, nonlinear least squares with outlier refit, coordinate transformation and Monte Carlo sampling/interpolation.

# Validation Audit

| Validation | Found? | Evidence | Assessment |
|---|---|---|---|
| baseline | PARTIAL | [PAPER EVIDENCE] Four preprocessing routes and failed RF/SVM/XGBoost route | No labeled segmentation baseline |
| train/test | PARTIAL | [PAPER EVIDENCE] Leave-one-out used in rejected ML experiment | Strong negative-result lesson; production segmentation has no truth set |
| time split | NOT FOUND | NOT FOUND | Not applicable |
| residual | FOUND | [PAPER EVIDENCE] Sinusoid fit errors and missing ratios are tabulated | Some traces have 70–77% missingness and high error |
| error metric | PARTIAL | [PAPER EVIDENCE] Fit error, missing ratio and JRC | Q1 accuracy and Q4 calibration error are unavailable |
| model comparison | FOUND | [PAPER EVIDENCE] Preprocessing variants, ML failure and sampling schemes | Mostly qualitative in Q1 |
| sensitivity | FOUND | [PAPER EVIDENCE] JRC across 10–200 sampling points | Meaningful discretization stability analysis |
| perturbation | NOT FOUND | NOT FOUND | No image/noise or plane-parameter stress test beyond assumed MC distributions |
| robustness | PARTIAL | [PAPER EVIDENCE] Multiple images/traces and sampling densities | Threshold and DBSCAN sensitivity NOT FOUND |
| simulation | FOUND | [PAPER EVIDENCE] Monte Carlo plane sampling and uncertainty interpolation | Sampling count/convergence NOT FOUND |
| feasibility check | PARTIAL | [PAPER EVIDENCE] 3D geometry and candidate coordinates are produced | No simulated uncertainty reduction after drilling |
| practical validation | NOT FOUND | NOT FOUND | No field labels or follow-up drilling |

# Figures and Tables

- [PAPER EVIDENCE] Preprocessing ablations/masks (comparison, Q1): visually show artifact suppression.
- [PAPER EVIDENCE] Trace points, fitted sinusoids and error table (result/validation, Q2): reveal fit quality and missingness.
- [PAPER EVIDENCE] JRC–sample-count curves (sensitivity, Q3): identify a stable discretization region.
- [PAPER EVIDENCE] 3D planes, pair connections and uncertainty heatmap (mechanism/decision, Q4): connect reconstruction to drilling choices, but not calibrated success.

# Abstract Architecture

- [PAPER EVIDENCE] The abstract is question-wise and traces the same pipeline, naming methods and final JRC/drilling outputs.
- [ANALYST INFERENCE] Worth copying: visible inheritance of upstream outputs. Avoid: using “probability” for a normalized heuristic score without calibration evidence.

# Strengths

- [PAPER EVIDENCE] It documents a negative ML result and identifies sample leakage instead of hiding it.
- [PAPER EVIDENCE] Geometry gives strong reasons for sinusoidal and planar models.
- [PAPER EVIDENCE] Sampling-density sensitivity is tied to the reported JRC.

# Weaknesses

- [ANALYST INFERENCE] Q1 lacks quantitative ground truth; many thresholds are not stress-tested.
- [ANALYST INFERENCE] The trace period is fixed by circumference although surrounding prose can imply it was estimated.
- [ANALYST INFERENCE] Q4’s “unbiased connectivity probability” claim is unsupported: angle means and min–max scores are not probability calibration.
- [ANALYST INFERENCE] Recommended drilling points lack cost, coverage comparison and before/after uncertainty simulation.

# Reusable Lessons

- [ANALYST INFERENCE] Let known geometry determine the model family; preserve negative experiments; pass uncertainty as a distribution, not just a point estimate; test discretization; distinguish a heuristic risk score from probability.

# Do NOT Copy

- [ANALYST INFERENCE] Do not reuse Frangi settings, the 94.25 period, DBSCAN thresholds, JRC mappings, assumed normal variances or linear “connectivity probability” normalization without current labels, geometry and calibration.
