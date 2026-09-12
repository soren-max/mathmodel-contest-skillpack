"""Independent single-machine overlap check, no optimization package needed."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = json.loads((root / 'results/schedule.json').read_text())['schedule']
overlap = []
for i, a in enumerate(rows):
    for b in rows[i + 1:]:
        if max(a['start'], b['start']) < min(a['finish'], b['finish']):
            overlap.append([a['job'], b['job']])
result = dict(single_machine_feasible=not overlap, overlapping_pairs=overlap)
(root / 'results/feasibility.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
