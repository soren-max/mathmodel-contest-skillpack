# Synthetic single-machine scheduling task

This small original fixture is not an official GMCM problem or a real contest rehearsal.
Schedule all three jobs on ONE machine. Each job runs without interruption, starts at or
after its release time, and cannot overlap another job. Duration is in hours.
Minimize total tardiness first, then minimize makespan among ties (lexicographic objective).
Report the actual computation method and independently check feasibility. A claim of global
optimality requires a valid exhaustive proof, bound/certificate or appropriate solver status.
Run `python3 src/schedule.py` then `python3 src/check_feasibility.py` from the fixture root.
