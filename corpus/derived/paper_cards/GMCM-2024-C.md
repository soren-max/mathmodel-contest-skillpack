# Metadata

- [PAPER EVIDENCE] contest: 中国研究生数学建模竞赛
- [PAPER EVIDENCE] year: 2024
- [PAPER EVIDENCE] problem code: C
- [PAPER EVIDENCE] paper title: 基于多因素分析与深度学习的磁芯损耗建模
- [PAPER EVIDENCE] source PDF: `/home/soren/zhonghui/skillpack/C2024.pdf`
- [PAPER EVIDENCE] page count: 71
- [PAPER EVIDENCE] award level: null
- [PAPER EVIDENCE] award verified: false

# One-Sentence Value

[ANALYST INFERENCE] A rich prediction-to-optimization chain showing both how a surrogate can enter a multiobjective design problem and why every surrogate optimum needs domain, feasibility and out-of-distribution checks.

# Problem Decomposition

## Q1

- [PAPER EVIDENCE] Classify three excitation waveforms from 1024-point magnetic-flux-density sequences.
- [ANALYST INFERENCE] Essence: supervised time-series feature classification.
- [PAPER EVIDENCE] Input: aligned waveforms; output: class labels using time/frequency features, PCA and classifiers.
- [ANALYST INFERENCE] Supplies the categorical waveform variable used downstream.

## Q2

- [PAPER EVIDENCE] Correct the Steinmetz loss equation for temperature using material-1 sinusoidal samples.
- [ANALYST INFERENCE] Essence: nonlinear physical-law calibration with candidate temperature functions.
- [PAPER EVIDENCE] Output: fitted parameters and R²/RMSE/MAPE; cubic correction reaches R² 0.9955, RMSE 11564.95, MAPE 22.10%.

## Q3

- [PAPER EVIDENCE] Analyze material, temperature and waveform effects singly and pairwise using grouped statistics and rank tests.
- [ANALYST INFERENCE] Essence: association/exploratory factorial analysis, not causal interaction identification.

## Q4

- [PAPER EVIDENCE] Predict loss from ten inputs including Bmax, temperature, frequency and one-hot material/waveform.
- [PAPER EVIDENCE] Output: log-target Conv–BiLSTM predictor compared with XGBoost and CNN; test R² 0.9956.
- [ANALYST INFERENCE] This becomes the Q5 surrogate objective.

## Q5

- [PAPER EVIDENCE] Minimize predicted loss while maximizing transmitted magnetic energy f·Bmax under observed-design bounds.
- [ANALYST INFERENCE] Essence: mixed discrete–continuous surrogate multiobjective optimization.
- [PAPER EVIDENCE] Weighted GA/PSO and Pareto NSGA-II/MOPSO solutions are reported.

# Overall Modeling Chain

[PAPER EVIDENCE] Raw waveform → preprocessing/classification → physical-law correction and factor associations → multivariable loss surrogate → mixed-variable multiobjective search → candidate operating condition.

# Mathematical Structure

## State Variables

- [PAPER EVIDENCE] Waveform samples/features and predicted magnetic-core loss at an operating condition.

## Decision Variables

- [PAPER EVIDENCE] Q5 temperature and material/waveform categories, frequency, Bmax and—in the weighted formulation—the weight a.

## Parameters

- [PAPER EVIDENCE] Steinmetz coefficients, temperature correction coefficients, learned network weights, data-derived variable bounds and optimizer settings.

## Objective Functions

- [PAPER EVIDENCE] Classification/prediction loss in Q1/Q4; regression error in Q2; Q5 minimizes surrogate loss Fs and maximizes Fe=fBmax, or minimizes aFs−(1−a)Fe.

## Constraints

- [PAPER EVIDENCE] Categorical choices and frequency/Bmax/temperature ranges drawn from data; optimizer bounds are stated.

## Core Relationships

- [PAPER EVIDENCE] Steinmetz power law links frequency and peak flux to loss; the learned surrogate maps all decision inputs to loss; fBmax is used as transmitted-energy proxy.

## Assumptions

- [PAPER EVIDENCE] Missing/outlying records can be repaired; selected factors explain loss; a trained predictor remains usable inside the stated Q5 domain.

# Model Selection Logic

- [PAPER EVIDENCE] FFT/time features are selected because waveform shape differs in both domains; nonparametric tests address non-normal feature distributions.
- [PAPER EVIDENCE] Steinmetz is used as a mechanistic baseline, with low-order temperature corrections compared rather than abandoned immediately.
- [PAPER EVIDENCE] A learned surrogate is used after simple equations cannot incorporate all variables; XGBoost and CNN are comparison models.
- [ANALYST INFERENCE] BiLSTM treats engineered feature positions as a sequence without a defensible temporal order; its interpretation is weak even though metrics are strong.
- [ANALYST INFERENCE] Q5 appropriately embeds the predictor, but a decision weight chosen by the same optimizer and inconsistent bounds make the formulation vulnerable.

# Solver / Algorithm

- [PAPER EVIDENCE] Models: feature classifier, temperature-corrected Steinmetz regression, factor association analysis, nonlinear loss surrogate and constrained bi-objective design.
- [PAPER EVIDENCE] Solvers: SVM/tree/stacking, least squares/SA/PSO/dynamic PSO, Conv–BiLSTM training, GA/PSO and NSGA-II/MOPSO.
- [ANALYST INFERENCE] The optimizer searches the surrogate; it does not independently verify physical loss.

# Validation Audit

| Validation | Found? | Evidence | Assessment |
|---|---|---|---|
| baseline | FOUND | [PAPER EVIDENCE] Original Steinmetz, XGBoost and CNN | Strong inclusion; simple fit algorithms often produce nearly identical results |
| train/test | FOUND | [PAPER EVIDENCE] Q4 uses 8:1:1 split (9920/1240/1240) | Random record split may leak operating conditions |
| time split | NOT FOUND | NOT FOUND | No grouped/material/operating-point holdout |
| residual | PARTIAL | [PAPER EVIDENCE] Fit plots/errors appear | Systematic residual diagnosis is limited |
| error metric | FOUND | [PAPER EVIDENCE] Accuracy/recall/F1 and R²/RMSE/MAPE | Multiple metrics improve interpretability |
| model comparison | FOUND | [PAPER EVIDENCE] Several classifiers, optimizers and predictors | Some stacking is not justified by meaningful gain |
| sensitivity | NOT FOUND | NOT FOUND | Weight a and optimizer/network choices lack systematic sensitivity |
| perturbation | FOUND | [PAPER EVIDENCE] Gaussian noise test changes R² from 0.9956 to 0.9952 | Narrow robustness check only |
| robustness | PARTIAL | [PAPER EVIDENCE] Noise test and several optimizer runs/variants | No distribution-shift validation |
| simulation | PARTIAL | [PAPER EVIDENCE] Surrogate-based design search | Not a physical simulation |
| feasibility check | FAILED | [PAPER EVIDENCE] A reported MOPSO point violates stated frequency/Bmax ranges; text also states 5,000,000 versus table 500,000 | Critical numeric/domain inconsistency |
| practical validation | NOT FOUND | NOT FOUND | No experimental measurement at optimized settings |

# Figures and Tables

- [PAPER EVIDENCE] FFT/PCA/feature distributions (EDA, Q1): justify separability.
- [PAPER EVIDENCE] Steinmetz correction metric table (comparison/validation, Q2): reveals cubic least squares performs best despite more elaborate solvers.
- [PAPER EVIDENCE] Predicted-versus-actual and model metric table (validation, Q4): supports surrogate accuracy.
- [PAPER EVIDENCE] Pareto fronts (optimization/decision, Q5): expose trade-offs, but do not prove physical feasibility.

# Abstract Architecture

- [PAPER EVIDENCE] Brief background, then question-wise methods with several key metrics and a final operating condition.
- [ANALYST INFERENCE] Worth copying: numeric results tied to each question. Avoid: claiming the dynamic optimizer is best when its table does not support that, or presenting an unchecked optimum as deployable.

# Strengths

- [PAPER EVIDENCE] The questions form an explicit data→model→decision chain.
- [PAPER EVIDENCE] A mechanistic baseline is retained and multiple error metrics are reported.
- [PAPER EVIDENCE] Q4 includes held-out testing and a noise perturbation.

# Weaknesses

- [ANALYST INFERENCE] Random splitting likely overstates generalization across operating conditions.
- [ANALYST INFERENCE] “Synergy” in Q3 is not backed by a controlled interaction model.
- [ANALYST INFERENCE] Q5 contains degenerate weight treatment, bound inconsistencies and no post-optimization experiment.

# Reusable Lessons

- [ANALYST INFERENCE] Preserve a physical baseline, make every decision variable an explicit surrogate input, compare Pareto alternatives, and validate the selected point against ranges and the real mechanism.

# Do NOT Copy

- [ANALYST INFERENCE] Do not reuse Conv–BiLSTM because it scored highest, interpret grouped association as causation, optimize an objective weight as an ordinary design variable, or trust a surrogate optimum outside its validated support.
