# Metadata

- [PAPER EVIDENCE] contest: 中国研究生数学建模竞赛
- [PAPER EVIDENCE] year: 2023
- [PAPER EVIDENCE] problem code: E
- [PAPER EVIDENCE] paper title: 出血性脑卒中临床智能诊疗建模
- [PAPER EVIDENCE] source PDF: `/home/soren/zhonghui/skillpack/E2023.pdf`
- [PAPER EVIDENCE] page count: 53
- [PAPER EVIDENCE] award level: null
- [PAPER EVIDENCE] award verified: false

# One-Sentence Value

[ANALYST INFERENCE] Use this primarily as a high-stakes audit exemplar: heterogeneous clinical prediction demands patient-level validation, metric integrity and noncausal wording, none of which model sophistication can replace.

# Problem Decomposition

## Q1

- [PAPER EVIDENCE] Label 48-hour hematoma expansion (absolute increase ≥6 mL or relative increase ≥33%) and predict it from clinical/imaging variables.
- [ANALYST INFERENCE] Essence: small-sample binary classification with heterogeneous features.
- [PAPER EVIDENCE] RF/SVM/logistic models use selected clinical, location and imaging descriptors; output includes individual probabilities.

## Q2

- [PAPER EVIDENCE] Describe edema-volume evolution, group trajectories, assess treatment relations and relate hematoma to edema.
- [ANALYST INFERENCE] Essence: irregular longitudinal modeling plus exploratory observational association.
- [PAPER EVIDENCE] Pooled time intervals are fitted with polynomials/Gaussians; K-means creates four trajectory groups; RF/gray relation and regressions rank factors/treatments.

## Q3

- [PAPER EVIDENCE] Predict 90-day mRS and analyze factor relationships using baseline and follow-up information.
- [ANALYST INFERENCE] Essence: ordinal-outcome prediction treated as classification, with multimethod feature voting.
- [PAPER EVIDENCE] Six selection methods vote features; RF predicts outcomes; time-varying model reports training accuracy 0.45.

# Overall Modeling Chain

[PAPER EVIDENCE] Clinical/imaging tables → cleaning/feature aggregation → event labeling/classification → pooled/grouped longitudinal curves → observational factor ranking → outcome feature voting/prediction → association summaries.

# Mathematical Structure

## State Variables

- [PAPER EVIDENCE] Hematoma/edema volumes over follow-up time, expansion label and 90-day mRS category.

## Decision Variables

- [ANALYST INFERENCE] There is no genuine treatment decision variable; treatments are observed covariates. Feature inclusion and cluster membership are analysis choices.

## Parameters

- [PAPER EVIDENCE] 48-hour/6 mL/33% labeling thresholds, polynomial/Gaussian coefficients, K=4 clusters, model weights and feature-vote cutoffs.

## Objective Functions

- [PAPER EVIDENCE] Classification losses/accuracy; curve-fitting error; within-cluster dispersion; regression fit and gray-relation ranking.

## Constraints

- [PAPER EVIDENCE] Observation-time windows and available visits constrain longitudinal fitting; clinical eligibility/measurement availability constrain samples.

## Core Relationships

- [PAPER EVIDENCE] Baseline/follow-up volume changes define labels/rates; fitted time functions represent mean trajectories; feature associations and predictors map covariates to outcomes.

## Assumptions

- [PAPER EVIDENCE] Outliers can be deleted, pooled observations can represent common trajectories, and treatment differences can be assessed while assuming treatment choice is driven only by illness.
- [ANALYST INFERENCE] The last assumption is not credible enough for causal treatment-effect claims.

# Model Selection Logic

- [PAPER EVIDENCE] RF/LightGBM and correlations reduce 72 variables before small-sample classifiers; multiple selection methods are voted in Q3.
- [PAPER EVIDENCE] Piecewise curves accommodate visibly changing edema trajectories; K-means seeks subgroups.
- [ANALYST INFERENCE] Simpler penalized logistic/ordinal models with repeated nested patient-level validation would provide a more defensible baseline.
- [ANALYST INFERENCE] High-order pooled curve fitting ignores within-patient dependence, and treatment ranking lacks confounding control; data do not support causal efficacy claims.

# Solver / Algorithm

- [PAPER EVIDENCE] Models: binary/ordinal prediction, piecewise longitudinal curve fits, trajectory clustering and observational association regressions.
- [PAPER EVIDENCE] Algorithms: RF, SVM, logistic regression, LightGBM, K-means, MATLAB FitTool, gray relational analysis and multimethod feature voting.

# Validation Audit

| Validation | Found? | Evidence | Assessment |
|---|---|---|---|
| baseline | PARTIAL | [PAPER EVIDENCE] RF, SVM and logistic are compared | No clinically simple/risk-score baseline |
| train/test | FOUND | [PAPER EVIDENCE] Q1 random 80/20 split | Only 100 labeled patients; repeated/nested validation NOT FOUND |
| time split | NOT FOUND | NOT FOUND | Longitudinal rows are not split by patient/time |
| residual | PARTIAL | [PAPER EVIDENCE] Q2 reports fit residual constructs | Some intervals have R² 0.1152 and 0.0309; fit claims remain too positive |
| error metric | FAILED | [PAPER EVIDENCE] Paper states TP/TN were swapped because positives were few; reported F1 values conflict with precision/recall | Critical metric-integrity failure |
| model comparison | PARTIAL | [PAPER EVIDENCE] Multiple classifiers/feature selectors | Same small data supports selection and comparison; no uncertainty intervals |
| sensitivity | NOT FOUND | NOT FOUND | Cluster count, vote threshold and deletion rules not stressed |
| perturbation | NOT FOUND | NOT FOUND | No missingness/outlier perturbation |
| robustness | NOT FOUND | NOT FOUND | No repeated seeds, bootstrap or external cohort |
| simulation | NOT FOUND | NOT FOUND | None |
| feasibility check | NOT FOUND | NOT FOUND | No treatment policy is actually optimized |
| practical validation | NOT FOUND | NOT FOUND | No external/clinical validation or calibration |

# Figures and Tables

- [PAPER EVIDENCE] Feature importance/correlation displays (EDA/model explanation, Q1/Q3): organize heterogeneous factors but do not establish effects.
- [PAPER EVIDENCE] Piecewise edema curves and group curves (result, Q2): show proposed trajectory summaries and visibly expose poor-fit regions.
- [PAPER EVIDENCE] Classifier metric tables (comparison, Q1/Q3): intended as validation, but internal metric inconsistencies make them audit evidence instead.

# Abstract Architecture

- [PAPER EVIDENCE] The abstract is organized by question and names preprocessing, predictors, curve fitting and feature analysis; it reports qualitative conclusions and some counts.
- [ANALYST INFERENCE] Worth copying: question-wise coverage. Avoid: presenting observational rankings as treatment effectiveness or metrics whose class definitions changed.

# Strengths

- [PAPER EVIDENCE] Clinical, anatomical location, imaging shape/gray and follow-up data are explicitly organized.
- [PAPER EVIDENCE] The weak time-varying Q3 model accuracy (0.45) is disclosed rather than hidden.
- [PAPER EVIDENCE] Several models/features are compared, creating material for scrutiny.

# Weaknesses

- [ANALYST INFERENCE] Swapping TP/TN to improve presentation invalidates metric interpretation.
- [ANALYST INFERENCE] Random small-sample splitting, preprocessing before robust validation and extensive feature search invite overfitting.
- [ANALYST INFERENCE] Treatment-outcome associations are written too causally despite confounding; chi-square nonsignificance conflicts with later strong claims.
- [ANALYST INFERENCE] Deleting true clinical extremes may remove signal and bias results.

# Reusable Lessons

- [ANALYST INFERENCE] Freeze label/metric definitions; split by patient; report weak and negative results; use calibrated uncertainty; distinguish prediction, association and causal effect in every conclusion.

# Do NOT Copy

- [ANALYST INFERENCE] Do not copy clinical thresholds to another cohort, delete extremes automatically, pool repeat measurements as independent, change positive-class conventions, or infer treatment efficacy from RF importance/gray relation/correlation.
