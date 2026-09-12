"""Validate fixture reproducibility and planted facts, not LLM reasoning."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'benchmarks/e2e'


class E2EFixtureTests(unittest.TestCase):
    def test_reproducible_results_and_label_anchors(self):
        cases = {'case_a_engineering': ['forecast.py'], 'case_b_scheduling': ['schedule.py', 'check_feasibility.py']}
        for case, scripts in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory(prefix='mm-e2e-test-') as tmp:
                source = ROOT / case
                dest = Path(tmp) / 'project'
                shutil.copytree(source, dest)
                expected = {p.name: p.read_bytes() for p in (source / 'results').iterdir()}
                for p in (dest / 'results').iterdir():
                    p.unlink()
                for script in scripts:
                    r = subprocess.run([sys.executable, str(dest / 'src' / script)], cwd=dest,
                                       text=True, capture_output=True, timeout=15)
                    self.assertEqual(r.returncode, 0, r.stderr)
                actual = {p.name: p.read_bytes() for p in (dest / 'results').iterdir()}
                self.assertEqual(actual, expected)
                labels = json.loads((source / 'expected_findings.json').read_text())
                for finding in labels['findings']:
                    self.assertIn(finding['anchor']['quote'], (source / finding['anchor']['path']).read_text())
                    for file in finding['supporting_files']:
                        self.assertTrue((source / file).is_file())

    def test_planted_facts_are_present(self):
        a = json.loads((ROOT / 'case_a_engineering/results/metrics.json').read_text())
        self.assertEqual(a['mae'], 0)
        self.assertNotEqual(a['model_origins'], a['baseline_origins'])
        b = json.loads((ROOT / 'case_b_scheduling/results/feasibility.json').read_text())
        self.assertFalse(b['single_machine_feasible'])
        self.assertEqual(len(b['overlapping_pairs']), 3)
        result = json.loads((ROOT / 'case_b_scheduling/results/schedule.json').read_text())
        self.assertEqual(result['solver_status'], 'HEURISTIC_CANDIDATE')
        self.assertIsNone(result['optimality_gap'])


if __name__ == '__main__':
    unittest.main()
