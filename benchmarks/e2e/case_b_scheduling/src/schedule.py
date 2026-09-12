"""A tiny greedy dispatcher for repository audit exercises."""
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
jobs = list(csv.DictReader((root / 'data/jobs.csv').open()))
schedule = []
for job in jobs:
    start = int(job['release'])
    finish = start + int(job['duration'])
    schedule.append(dict(job=job['job'], start=start, finish=finish,
                         tardiness=max(0, finish - int(job['due']))))
makespan = max(row['finish'] for row in schedule)
tardiness = sum(row['tardiness'] for row in schedule)
result = dict(method='greedy_release_dispatch', schedule=schedule, makespan=makespan,
              total_tardiness=tardiness, objective=0.5 * tardiness + 0.5 * makespan,
              objective_definition='0.5 * total_tardiness + 0.5 * makespan',
              solver_status='HEURISTIC_CANDIDATE', optimality_gap=None)
(root / 'results').mkdir(exist_ok=True)
(root / 'results/schedule.json').write_text(json.dumps(result, indent=2) + '\n')
