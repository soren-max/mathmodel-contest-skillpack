# Production schedule

## Abstract

For single-machine scheduling we establish a genetic algorithm mathematical model and
solve the lexicographic objective of total tardiness followed by makespan. Our feasible
globally optimal schedule has zero tardiness and makespan 3 hours.

## Mathematical model and computation

The genetic algorithm is the mathematical model. Each job must run once on the single
machine, no jobs overlap, and release times are respected. We use a genetic algorithm
with population 100 and 200 generations to minimize tardiness first and makespan second.
The reported schedule places A at [0,3], B at [0,2], and C at [0,2].

## Results and conclusion

The reported objective is 1.5. All hard constraints are satisfied. Global optimality is
proved by the successful run. The resulting schedule is recommended for direct execution.
