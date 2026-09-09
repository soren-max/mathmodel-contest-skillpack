# Metadata

- [PAPER EVIDENCE] contest: 中国研究生数学建模竞赛
- [PAPER EVIDENCE] year: 2022
- [PAPER EVIDENCE] problem code: B
- [PAPER EVIDENCE] paper title: 基于整数规划的方形件排样和组批优化问题研究
- [PAPER EVIDENCE] source PDF: `/home/soren/zhonghui/skillpack/B2022.pdf`
- [PAPER EVIDENCE] page count: 41
- [PAPER EVIDENCE] award level: null
- [PAPER EVIDENCE] award verified: false

# One-Sentence Value

[ANALYST INFERENCE] Learn how to turn guillotine cutting and order batching into explicit discrete objects and feasibility rules, while treating a fast heuristic solution as a feasible solution rather than a proved optimum.

# Problem Decomposition

## Q1

- [PAPER EVIDENCE] Original requirement: arrange rectangular parts on 1220×2440 sheets under three-stage guillotine cutting and minimize sheet use.
- [ANALYST INFERENCE] Mathematical essence: constrained two-dimensional cutting-stock/bin-packing.
- [PAPER EVIDENCE] Input: part types, width, height and required counts in four A datasets; output: sheet count, utilization and cutting coordinates.
- [PAPER EVIDENCE] Key variables describe whether a stack belongs to a stripe, whether a stripe belongs to a sheet, and counts of parts/stacks.
- [ANALYST INFERENCE] The output becomes the within-material packing engine used by Q2.

## Q2

- [PAPER EVIDENCE] Original requirement: assign indivisible orders to batches with at most 1000 pieces and 250 m², then pack parts of the same material.
- [ANALYST INFERENCE] Mathematical essence: capacitated clustering followed by Q1 packing.
- [PAPER EVIDENCE] Input: order/material composition and capacities; output: batches, sheets and utilization for B1–B5.
- [PAPER EVIDENCE] Key quantities are order-to-batch membership, Jaccard material distance and batch capacity.
- [ANALYST INFERENCE] The questions form a chain, but batching and packing are optimized sequentially rather than jointly.

# Overall Modeling Chain

[PAPER EVIDENCE] Orders and part dimensions → three-stage cut-tree abstraction → integer feasibility model → 3-SHST packing heuristic → material-set clustering under capacities → reuse packing heuristic → layouts, coordinates and utilization.

# Mathematical Structure

## State Variables

- [PAPER EVIDENCE] Remaining width/height in a sheet, stripe or stack; current batch piece count, area and material set.

## Decision Variables

- [PAPER EVIDENCE] Binary stack–stripe and stripe–sheet assignments; integer part counts; implicit order–batch assignments.

## Parameters

- [PAPER EVIDENCE] Sheet size 1220×2440, item dimensions/demand, three-stage cut order, batch limits 1000 pieces and 250 m².

## Objective Functions

- [PAPER EVIDENCE] Q1 minimizes used sheets (equivalently raises utilization for fixed demand); Q2 seeks batches that improve same-material packing and then minimizes sheets within each group.

## Constraints

- [PAPER EVIDENCE] Exact demand fulfillment, width/height capacities, hierarchical membership, unique placement, indivisible orders, batch piece/area caps and material compatibility.

## Core Relationships

- [PAPER EVIDENCE] Total occupied area divided by sheet area gives utilization; total area supplies a lower bound on sheet count; Jaccard distance measures mismatch between material sets.

## Assumptions

- [PAPER EVIDENCE] Parts are rectangular, orientation is fixed, three guillotine stages are required, and orders cannot be split.

# Model Selection Logic

- [PAPER EVIDENCE] The paper introduces integer programming because membership and count choices are discrete and capacity constrained.
- [PAPER EVIDENCE] It uses a custom search-tree heuristic because exact large-scale cutting is computationally difficult, sorting parts by decreasing width before greedy insertion.
- [ANALYST INFERENCE] A simple baseline was available: area lower bound plus first-fit/decreasing packing; only the lower bound is reported, so heuristic value is not isolated.
- [PAPER EVIDENCE] Agglomerative clustering is chosen to group orders with similar material sets while checking capacities.
- [ANALYST INFERENCE] Jaccard similarity matches set overlap but ignores material quantities, and the clustering threshold lacks empirical justification.

# Solver / Algorithm

- [PAPER EVIDENCE] Model: hierarchical 0–1/integer formulation of three-stage guillotine packing and capacitated order batching.
- [PAPER EVIDENCE] Solver: 3-SHST greedy search-tree traversal, stated complexity O(m²), followed by average-linkage agglomerative clustering with capacity checks.
- [ANALYST INFERENCE] The heuristic constructs feasible layouts quickly; it does not certify global optimality.

# Validation Audit

| Validation | Found? | Evidence | Assessment |
|---|---|---|---|
| baseline | PARTIAL | [PAPER EVIDENCE] Area lower bounds of 84/83/84/82 sheets for A1–A4 | [ANALYST INFERENCE] Useful bound, but no competing constructive baseline or optimality gap discussion |
| train/test | NOT FOUND | NOT FOUND | Not applicable to fitting; no holdout notion needed |
| time split | NOT FOUND | NOT FOUND | Not applicable |
| residual | NOT FOUND | NOT FOUND | Not applicable |
| error metric | PARTIAL | [PAPER EVIDENCE] Sheet count and utilization | Direct outcome metrics, not approximation error |
| model comparison | NOT FOUND | NOT FOUND | No exact solver or alternative heuristic comparison |
| sensitivity | NOT FOUND | NOT FOUND | Clustering threshold and sort rule are not varied |
| perturbation | NOT FOUND | NOT FOUND | No demand/dimension perturbation |
| robustness | NOT FOUND | NOT FOUND | Multiple datasets are solved, but stochastic stability is not tested |
| simulation | FOUND | [PAPER EVIDENCE] Cut layouts and coordinates are generated | Constructive execution evidence |
| feasibility check | FOUND | [PAPER EVIDENCE] Counts, coordinates, sheet capacities and a 96.43% example-sheet area check | Strongest validation element |
| practical validation | PARTIAL | [PAPER EVIDENCE] Runtime and manufacturing-style cut diagrams | No shop-floor or independent implementation test |

# Figures and Tables

- [PAPER EVIDENCE] Three-stage cut tree and algorithm flow (mechanism/workflow, Q1): explain how a feasible hierarchy is constructed.
- [PAPER EVIDENCE] Sheet layouts plus coordinate table (result/feasibility, Q1): make non-overlap and cutting order auditable.
- [PAPER EVIDENCE] Area lower-bound/utilization tables (validation, Q1): expose distance from a theoretical bound.
- [PAPER EVIDENCE] Batch-count, sheet-count and utilization tables (decision/result, Q2): summarize operational output across B1–B5.

# Abstract Architecture

- [PAPER EVIDENCE] Background is short; the abstract is organized by question, names the integer/heuristic and clustering routes, and reports principal sheet/utilization results.
- [ANALYST INFERENCE] Worth copying: method–output pairing for each question. Avoid: language that lets “optimization” imply proven optimality when only a heuristic was run.

# Strengths

- [PAPER EVIDENCE] Discrete membership variables, demand constraints and capacity constraints are explicit.
- [PAPER EVIDENCE] Layout coordinates connect the mathematical solution to a physically inspectable cut plan.
- [PAPER EVIDENCE] Area lower bounds prevent utilization numbers from floating without context.

# Weaknesses

- [ANALYST INFERENCE] The formulation and actual heuristic are not compared through an optimality gap.
- [ANALYST INFERENCE] Sequential batching then packing can miss globally better batches.
- [PAPER EVIDENCE] The paper acknowledges no rotation, local heuristic behavior and weak material similarity; threshold sensitivity remains NOT FOUND.

# Reusable Lessons

- [ANALYST INFERENCE] Write the placement hierarchy before choosing a solver; publish coordinates and capacity checks; compare every feasible heuristic to a lower bound; identify where staged optimization sacrifices global optimality.

# Do NOT Copy

- [ANALYST INFERENCE] Do not reuse sheet dimensions, three-stage geometry, fixed orientation, Jaccard distance or clustering threshold unless the current manufacturing rules support them. Do not label a best-found heuristic result “optimal.”
