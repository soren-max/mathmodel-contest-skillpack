"""Small forecasting implementation for repository auditing; known defects are intentional."""
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / 'data/measurements.csv').open()))
loads = [float(row['load']) for row in rows]
# Construct a sensor-derived feature before splitting forecast origins.
features = [loads[t + 1] for t in range(len(loads) - 1)]
train_origins = list(range(0, 6))
test_origins = list(range(6, 11))
train_mean = sum(loads[t + 1] for t in train_origins) / len(train_origins)
predictions = [dict(origin=t, target=loads[t + 1], prediction=features[t]) for t in test_origins]
mae = sum(abs(r['target'] - r['prediction']) for r in predictions) / len(predictions)
baseline_mae = sum(abs(loads[t + 1] - train_mean) for t in train_origins) / len(train_origins)
metrics = dict(mae=mae, baseline_mae=baseline_mae, model_origins=test_origins,
               baseline_origins=train_origins, model='next_sensor_value', n_test=len(test_origins))
(root / 'results').mkdir(exist_ok=True)
(root / 'results/metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
with (root / 'results/predictions.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['origin', 'target', 'prediction'], lineterminator='\n')
    writer.writeheader()
    writer.writerows(predictions)
