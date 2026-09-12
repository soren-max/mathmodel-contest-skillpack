"""Offline behavior tests in disposable contest repositories and isolated HOME."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('contest', ROOT / 'scripts/contest.py')
contest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contest)


class ContestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='mm-contest-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'project with spaces'
        self.root.mkdir()
        self.env = os.environ.copy()
        self.env.update(HOME=str(self.base / 'home'), MM_CODEX_HOME=str(self.base / 'codex'),
                        MM_STACK_HOME=str(self.base / 'cache'), MM_BIN_DIR=str(self.base / 'bin'),
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
        self.cfg = dict(questions=['q1'], questions_verified=True, competition_mode=True,
                        final_paper='paper/final.pdf', reproduction_entry='src/reproduce.py')
        self.config()

    def put(self, path, content):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(content) if isinstance(content, (dict, list)) else content)

    def config(self):
        self.put('project/project-layout.md', '```mm-layout\n' + json.dumps(self.cfg) + '\n```\n')

    def cli(self, command, *args, expected=0):
        result = subprocess.run(['bash', str(ROOT / 'bin/mm'), '--project', str(self.root), command, *args, '--json'],
                                text=True, capture_output=True, env=self.env, timeout=30)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout) if result.returncode != 2 else result.stderr

    def intake(self):
        self.put('notes/bootstrap.md', 'Official problem reviewed; J/F/L assigned.\n')
        self.put('reports/data_contract.md', 'verdict: PASS\nData fields checked.\n')

    def ready(self):
        self.intake()
        for p, value in {
            'notes/q1_model_plan.md': 'Predict target from lagged measurement. Baseline: persistence.',
            'src/q1.py': 'print("reproducible fixture")\n',
            'results/q1_config.json': {'seed': 42},
            'data/processed/input.csv': 'x,y\n1,2\n',
            'results/q1_result.json': {'rmse': 1.0},
            'results/q1_table.csv': 'metric,value\nrmse,1.0\n',
            'results/q1_validation.json': {'holdout_rmse': 1.0},
            'reports/q1_validation.md': 'verdict: PASS\nevidence: results/q1_validation.json\nHeld-out error independently checked.\n',
            'notes/q1_audit.md': 'verdict: PASS\nRaw result, command and holdout checked.\n',
            'notes/handoff_q1.md': 'Prediction error 1.0; limited to measured operating range. See registry.',
            'reports/evidence_matrix.md': '| Claim | Question | Status |\n|---|---|---|\n| rmse | Q1 | PASS |\n',
        }.items():
            self.put(p, value)
        self.put('results/q1_run.json', dict(entry='src/q1.py', command='python3 src/q1.py', exit_code=0,
                                           inputs=['data/processed/input.csv'], config='results/q1_config.json',
                                           outputs=['results/q1_result.json'], figures=['results/q1_table.csv']))
        self.metric = dict(question='q1', metric_id='q1.rmse', description='test error', value=1.0,
                           unit='unit', definition='root mean squared error on heldout rows', source_script='src/q1.py',
                           source_result='results/q1_result.json', source_field='rmse', rounding='1 decimal',
                           validation_status='PASS', approved_for_paper=True, notes='audited')
        self.put('results/paper_metrics.yaml', dict(schema_version=1, metrics=[self.metric]))

    def close(self, verdict='MVP_CLOSED'):
        fingerprint = self.cli('gate', 'q1')['artifact_sha256']
        self.put('reports/question_status.md', '<!-- mm-gate ' + json.dumps(dict(question='q1', verdict=verdict,
                  artifact_sha256=fingerprint)) + ' -->\n')

    def git(self, *args):
        r = subprocess.run(['git', '-C', str(self.root), *args], env=self.env, capture_output=True, text=True, timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def save(self):
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')

    def final_ready(self):
        self.ready()
        self.put('materials/gmcm_year_override.md', 'year: 2025\nofficial_source: fixture-official-material\nverified: true\n')
        self.put('paper/final.pdf', '%PDF-1.4\nSynthetic existence-only fixture, not a rendered paper.\n')
        self.put('src/reproduce.py', 'print("fixture")\n')
        self.close()
        report = self.cli('final-check', expected=1)
        self.put('reports/gmcm_final_review.md', 'review_mode: full\nverdict: PASS\nartifact_sha256: ' + report['artifact_sha256'] + '\nReviewed synthetic fixture.\n')
        self.cli('refresh')
        self.git('init', '-q')
        self.save()

    def snapshot(self):
        return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob('*') if p.is_file()}

    def test_empty_project(self):
        (self.root / 'project/project-layout.md').unlink()
        out = self.cli('status')
        self.assertEqual(len(out['state']['questions']), 4)
        self.assertTrue(all(q['status'] == 'NOT_STARTED' for q in out['state']['questions'].values()))
        self.assertEqual(out['recommended_next_action'], 'contest-project-bootstrap')

    def test_partial_and_next_audit(self):
        self.ready()
        (self.root / 'notes/q1_audit.md').unlink()
        item = self.cli('status')['state']['questions']['q1']
        self.assertEqual(item['status'], 'PARTIAL')
        self.assertEqual(self.cli('next')['recommended_next_action'], 'Q1 → result-auditor')
        self.assertEqual(self.cli('gate', 'q1', expected=1)['precheck'], 'PRECHECK_PARTIAL')

    def test_readiness_does_not_certify_closure(self):
        self.ready()
        out = self.cli('gate', 'q1')
        self.assertEqual(out['precheck'], 'PRECHECK_CLOSED_READY')
        self.assertEqual(out['status'], 'MVP_READY')
        self.assertIn('question-completion-gate', out['authority'])
        (self.root / 'reports/evidence_matrix.md').unlink()
        self.assertEqual(self.cli('gate', 'q1')['precheck'], 'PRECHECK_MVP_READY')

    def test_reviewed_closure_and_result_invalidation(self):
        self.ready()
        self.close('CLOSED')
        self.assertEqual(self.cli('status')['state']['questions']['q1']['status'], 'CLOSED')
        self.put('results/q1_result.json', {'rmse': 99})
        out = self.cli('status')['state']['questions']['q1']
        self.assertEqual(out['status'], 'MVP_READY')
        self.assertFalse(out['review_fresh'])
        self.cli('refresh')
        self.assertEqual(self.cli('next')['recommended_next_action'], 'Q1 → question-completion-gate')

    def test_state_drift_manual_cache_cannot_close_or_hide_question(self):
        self.intake()
        self.put('notes/q1_model_plan.md', 'plan')
        self.cli('refresh')
        path = self.root / 'project/contest_state.json'
        state = json.loads(path.read_text())
        state['questions']['q1']['status'] = 'CLOSED'
        self.put('project/contest_state.json', state)
        out = self.cli('status')
        self.assertIn('questions.q1.status', out['state_drift'])
        self.assertEqual(out['state']['questions']['q1']['status'], 'PARTIAL')
        self.put('project/contest_state.json', {'schema_version': 1, 'questions': {}})
        self.assertIn('q1', self.cli('status')['state']['questions'])

    def test_missing_unapproved_and_duplicate_metric(self):
        self.ready()
        self.put('results/paper_metrics.yaml', {'schema_version': 1, 'metrics': []})
        self.assertEqual(self.cli('gate', 'q1', expected=1)['checks']['metrics'], 'UNVERIFIED')
        self.metric['approved_for_paper'] = False
        self.put('results/paper_metrics.yaml', {'schema_version': 1, 'metrics': [self.metric]})
        self.assertIn('unapproved', str(self.cli('status')['blocking_issues']))
        self.metric['approved_for_paper'] = True
        self.put('results/paper_metrics.yaml', {'schema_version': 1, 'metrics': [self.metric, self.metric]})
        self.assertIn('CONFLICT', str(self.cli('status')['blocking_issues']))

    def test_blocked_audit_and_gate(self):
        self.ready()
        self.put('notes/q1_audit.md', 'verdict: BLOCKED\nLeakage.\n')
        self.assertEqual(self.cli('gate', 'q1', expected=1)['precheck'], 'PRECHECK_BLOCKED')
        self.put('notes/q1_audit.md', 'verdict: PASS\n')
        self.close('BLOCKED')
        self.assertEqual(self.cli('status')['state']['questions']['q1']['status'], 'BLOCKED')

    def test_final_check_unverified_year(self):
        self.final_ready()
        self.put('materials/gmcm_year_override.md', 'year: 2025\nofficial_source: official\nverified: false\n')
        self.assertIn('gmcm_year_override unverified', str(self.cli('final-check', expected=1)['failures']))

    def test_final_check_raw_pdf_and_corpus_tracked(self):
        self.final_ready()
        self.put('problem_files/source.PDF', '%PDF raw')
        self.put('corpus/extracted/raw.txt', 'raw copyrighted text fixture')
        self.put('corpus/raw/raw.txt', 'raw fixture')
        self.save()
        failures = str(self.cli('final-check', expected=1)['failures'])
        for name in ('source.PDF', 'corpus/extracted/raw.txt', 'corpus/raw/raw.txt'):
            self.assertIn(name, failures)
        self.assertNotIn('tracked: paper/final.pdf', failures)

    def test_next_earliest_unresolved_stage(self):
        self.ready()
        self.cfg['questions'] = ['q1', 'q2', 'q3']
        self.config()
        self.close()
        for src, dst in [('notes/q1_model_plan.md', 'notes/q2_model_plan.md'), ('results/q1_run.json', 'results/q2_run.json')]:
            self.put(dst, (self.root / src).read_text())
        self.assertEqual(self.cli('next')['recommended_next_action'], 'Q2 → result-auditor')

    def test_unique_workflow_partial_gate_then_handoff_then_regate(self):
        self.ready()
        (self.root / 'notes/handoff_q1.md').unlink()
        self.assertEqual(self.cli('next')['recommended_next_action'], 'Q1 → question-completion-gate')
        self.put('reports/question_status.md', '<!-- mm-gate {"question":"q1","verdict":"PARTIAL"} -->\n')
        (self.root / 'reports/evidence_matrix.md').unlink()
        self.assertEqual(self.cli('next')['recommended_next_action'], 'Q1 → repo-paper-auditor')
        self.put('reports/evidence_matrix.md', '| Claim | Question | Status |\n|---|---|---|\n| error | q1 | PASS |\n')
        self.assertEqual(self.cli('next')['recommended_next_action'], 'Q1 → paper-handoff')

    def test_readonly_commands_do_not_mutate_even_git_index(self):
        self.final_ready()
        before = self.snapshot()
        self.cli('status')
        self.cli('next')
        self.cli('gate', 'q1')
        self.assertEqual(self.cli('final-check')['verdict'], 'READY FOR HUMAN FINAL REVIEW')
        self.cli('doctor', expected=1)
        self.assertEqual(before, self.snapshot())

    def test_refresh_atomic_and_failure_preserves_old_bytes(self):
        self.ready()
        self.cli('refresh')
        path = self.root / 'project/contest_state.json'
        before = path.read_bytes()
        state = contest.inspect(self.root)[0]
        with patch.object(contest.os, 'replace', side_effect=OSError('injected replacement failure')):
            with self.assertRaises(OSError):
                contest.refresh(self.root, state)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(list(path.parent.glob('.mm-state-*')), [])
        self.put('notes/q1_model_plan.md', 'changed plan')
        out = self.cli('status', '--refresh')
        self.assertTrue(out['refreshed'])
        self.assertTrue(out['changed_fields'])
        self.assertEqual(self.cli('status')['state_drift'], [])

    def test_refresh_refuses_symlink(self):
        self.cli('refresh')
        path = self.root / 'project/contest_state.json'
        path.unlink()
        outside = self.base / 'outside.json'
        outside.write_text('preserve')
        path.symlink_to(outside)
        self.assertIn('symlink', self.cli('refresh', expected=2))
        self.assertEqual(outside.read_text(), 'preserve')

    def test_legacy_closed_gate_cannot_certify(self):
        self.ready()
        self.put('reports/question_status.md', '| Question | Status |\n|---|---|\n| Q1 | CLOSED |\n')
        self.assertEqual(self.cli('status')['state']['questions']['q1']['status'], 'MVP_READY')

    def test_critical_resolution_and_high_risk_todo(self):
        self.final_ready()
        self.put('reports/evidence_matrix.md', (self.root / 'reports/evidence_matrix.md').read_text() +
                 '\n| Question | Finding | Severity | Resolution |\n|---|---|---|---|\n| q1 | leakage | CRITICAL | OPEN |\n')
        out = self.cli('final-check', expected=1)
        self.assertIn('CRITICAL unresolved', str(out['failures']))
        self.assertEqual(self.cli('status')['state']['questions']['q1']['status'], 'BLOCKED')
        self.put('src/unfinished.py', '# TODO HIGH_RISK constraint checker missing\n')
        self.assertIn('high-risk TODO/HACK', str(self.cli('final-check', expected=1)['failures']))

    def test_missing_final_paper_and_stale_final_review(self):
        self.final_ready()
        self.put('paper/final.pdf', 'changed manuscript')
        self.assertIn('final review unbound/stale', str(self.cli('final-check', expected=1)['failures']))
        (self.root / 'paper/final.pdf').unlink()
        self.assertIn('final_paper missing', str(self.cli('final-check', expected=1)['failures']))

    def test_contradictory_gate_table_cannot_close(self):
        self.ready()
        self.close()
        path = self.root / 'reports/question_status.md'
        self.put('reports/question_status.md', path.read_text() + '| Question | Status |\n|---|---|\n| Q1 | BLOCKED |\n')
        self.assertIn('verdict conflict', self.cli('status', expected=2))

    def test_staged_whitespace_and_dirty_workspace_fail(self):
        self.final_ready()
        self.put('notes/new_note.md', 'trailing space  \n')
        self.git('add', 'notes/new_note.md')
        failures = str(self.cli('final-check', expected=1)['failures'])
        self.assertIn('git diff --check', failures)
        self.assertIn('Git working tree not clean', failures)

    def test_invalid_metric_schema_cannot_pass(self):
        self.ready()
        self.metric['value'] = {'invented': 1}
        self.put('results/paper_metrics.yaml', {'schema_version': 1, 'metrics': [self.metric]})
        self.assertEqual(self.cli('gate', 'q1', expected=1)['checks']['metrics'], 'UNVERIFIED')

    def test_source_path_escape_rejected(self):
        self.ready()
        self.metric['source_result'] = '../outside.json'
        self.put('results/paper_metrics.yaml', {'schema_version': 1, 'metrics': [self.metric]})
        output = self.cli('status')
        self.assertIn('Path escapes project', str(output['blocking_issues']))
        self.assertEqual(output['state']['questions']['q1']['status'], 'PARTIAL')
        self.assertEqual(self.cli('gate', 'q1', expected=1)['checks']['metrics'], 'UNVERIFIED')

    def test_unverified_question_scope_fails(self):
        self.final_ready()
        self.cfg['questions_verified'] = False
        self.config()
        self.assertIn('question scope unverified', str(self.cli('final-check', expected=1)['failures']))

    def test_unknown_question_and_malformed_manifest_fail_closed(self):
        self.ready()
        self.assertIn('Unknown question', self.cli('gate', 'q99', expected=2))
        self.put('results/q1_run.json', {'entry': 'src/q1.py'})
        self.assertEqual(self.cli('gate', 'q1', expected=1)['checks']['code_run'], 'UNVERIFIED')

    def test_doctor_optional_missing_warn_required_missing_fail(self):
        self.cfg['required_python_modules'] = ['mm_nonexistent_fixture_dependency']
        self.config()
        checks = self.cli('doctor', expected=1)
        required = next(c for c in checks if 'mm_nonexistent_fixture_dependency' in c['message'])
        self.assertEqual(required['status'], 'FAIL')
        # Mock lookup to exercise absence without relying on packages on this machine.
        with patch.dict(os.environ, self.env, clear=True), patch.object(contest.importlib.util, 'find_spec', return_value=None):
            sys.path.insert(0, str(ROOT / 'scripts'))
            try:
                checks = contest.doctor(self.root)
            finally:
                sys.path.pop(0)
        optional = [c for c in checks if c['message'].startswith('optional dependency:')]
        self.assertTrue(optional)
        self.assertTrue(all(c['status'] == 'WARN' for c in optional))


if __name__ == '__main__':
    unittest.main()
