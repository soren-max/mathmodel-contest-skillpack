#!/usr/bin/env python3
"""Read-only deterministic contest navigation; refresh writes only its JSON cache."""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
Q = re.compile(r'q[1-9][0-9]*', re.I)
CLOSED = {'MVP_CLOSED', 'CLOSED'}


def read(path):
    return path.read_text(encoding='utf-8') if path.is_file() else ''


def json_read(path):
    return json.loads(read(path))


def child(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f'Expected project-relative path: {relative!r}')
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes project: {relative}')
    return path


def present(root, relative):
    p = child(root, relative)
    return p.is_file() and p.stat().st_size > 0


def marker(text, name='verdict'):
    values = re.findall(r'^' + re.escape(name) + r':\s*([^\n]+?)\s*$', text, re.M)
    return values[0].strip() if len(values) == 1 else None


def tables(text):
    header = None
    for line in text.splitlines():
        if not line.startswith('|'):
            header = None
            continue
        cells = [c.strip().strip('`').strip() for c in line.strip().strip('|').split('|')]
        if all(re.fullmatch(r'[: -]+', c) for c in cells):
            continue
        if header is None:
            header = [c.lower() for c in cells]
        elif len(cells) == len(header):
            yield dict(zip(header, cells))


def layout(root):
    blocks = re.findall(r'```mm-layout\s*\n(.*?)\n```', read(root / 'project/project-layout.md'), re.S)
    if len(blocks) > 1:
        raise ValueError('Multiple mm-layout blocks')
    cfg = json.loads(blocks[0]) if blocks else {}
    if not isinstance(cfg, dict):
        raise ValueError('mm-layout must be an object')
    questions = cfg.get('questions', ['q1', 'q2', 'q3', 'q4'])
    if not isinstance(questions, list) or not questions or any(not isinstance(q, str) or not Q.fullmatch(q) for q in questions):
        raise ValueError('mm-layout questions must be a nonempty qN list')
    for field in ('questions_verified', 'competition_mode'):
        if field in cfg and type(cfg[field]) is not bool:
            raise ValueError(f'{field} must be boolean')
    cfg['questions'] = [q.lower() for q in questions]
    mappings = cfg.get('artifacts', {})
    if not isinstance(mappings, dict):
        raise ValueError('artifacts must be a qN mapping')
    for q, paths in mappings.items():
        if not isinstance(q, str) or not Q.fullmatch(q) or not isinstance(paths, dict) or set(paths) - {'model_plan', 'run', 'audit', 'validation', 'handoff'}:
            raise ValueError('Invalid artifact mapping; Evidence Matrix cannot be remapped')
    required = cfg.get('required_python_modules', [])
    if not isinstance(required, list) or any(not isinstance(m, str) or not re.fullmatch(r'[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*', m) for m in required):
        raise ValueError('required_python_modules must list import names')
    return cfg


def registry(root):
    path = root / 'results/paper_metrics.yaml'
    try:
        try:
            data = json_read(path)
        except json.JSONDecodeError:
            # JSON is the installed default; ordinary YAML requires an existing optional parser.
            try:
                import yaml
            except ImportError:
                return [], ['UNVERIFIED registry: use JSON-compatible YAML or an existing PyYAML environment']
            try:
                data = yaml.safe_load(read(path))
            except yaml.YAMLError as error:
                raise ValueError(f'invalid YAML: {error}') from error
        if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('metrics'), list):
            raise ValueError('invalid registry schema')
        metrics = data['metrics']
        metric_schema = json_read(ROOT / 'schemas/paper_metrics.schema.json')['properties']['metrics']['items']
        required = metric_schema['required']
        problems, seen = [], {}
        for m in metrics:
            if not isinstance(m, dict) or any(k not in m for k in required):
                problems.append('UNVERIFIED malformed metric')
                continue
            if set(m) - set(metric_schema['properties']):
                problems.append('UNVERIFIED unexpected metric fields')
            for field, rule in metric_schema['properties'].items():
                value = m[field]
                kind = ('null' if value is None else 'boolean' if type(value) is bool else
                        'integer' if type(value) is int else 'number' if type(value) is float else
                        'string' if isinstance(value, str) else 'unsupported')
                allowed = rule.get('type', kind)
                allowed = [allowed] if isinstance(allowed, str) else allowed
                if kind not in allowed or ('enum' in rule and value not in rule['enum']):
                    problems.append(f'UNVERIFIED invalid metric field {field}')
                if isinstance(value, str) and (len(value) < rule.get('minLength', 0) or
                        ('pattern' in rule and not re.fullmatch(rule['pattern'], value))):
                    problems.append(f'UNVERIFIED invalid metric field {field}')
                if isinstance(value, float) and not math.isfinite(value):
                    problems.append(f'UNVERIFIED nonfinite metric field {field}')
            mid = m['metric_id']
            if not isinstance(mid, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_.-]*', mid):
                problems.append('UNVERIFIED invalid metric_id')
                continue
            if not isinstance(m['question'], str) or not Q.fullmatch(m['question']):
                problems.append(f'UNVERIFIED {mid}: invalid question')
            if mid in seen:
                problems.append(f'CONFLICT duplicate metric_id {mid}')
            seen[mid] = m
            if m['validation_status'] != 'PASS' or m['approved_for_paper'] is not True:
                problems.append(f'{mid}: {m["validation_status"]} / unapproved')
            if m['value'] is None or not m['definition'] or not m['source_field'] or not m['rounding']:
                problems.append(f'UNVERIFIED incomplete {mid}')
            for key in ('source_script', 'source_result'):
                if not present(root, m[key]):
                    problems.append(f'UNVERIFIED {mid}: missing {key}')
        return metrics, problems
    except (ValueError, TypeError, OSError) as error:
        return [], [f'UNVERIFIED registry: {error}']


def digest(root, paths):
    h = hashlib.sha256()
    for relative in sorted(set(paths)):
        p = child(root, relative)
        h.update(relative.encode() + b'\0')
        if p.is_file():
            with p.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(chunk)
        else:
            h.update(b'<MISSING>')
        h.update(b'\0')
    return h.hexdigest()


def gate_records(root):
    records = {}
    text = read(root / 'reports/question_status.md')
    for raw in re.findall(r'<!-- mm-gate\s+(.*?)\s+-->', text):
        record = json.loads(raw)
        if not isinstance(record, dict) or not isinstance(record.get('question'), str):
            raise ValueError('Invalid mm-gate record')
        q = record['question'].lower()
        if not Q.fullmatch(q) or q in records:
            raise ValueError('Invalid or duplicate mm-gate question')
        if record.get('verdict') not in {'BLOCKED', 'PARTIAL', *CLOSED}:
            raise ValueError('Invalid mm-gate verdict')
        records[q] = record
    # Legacy tables can block, but cannot certify closure without a reviewed digest.
    for row in tables(text):
        q = row.get('question', '').lower()
        if Q.fullmatch(q):
            verdict = row.get('status', row.get('verdict', 'UNVERIFIED'))
            if q in records and records[q]['verdict'] != verdict:
                raise ValueError(f'{q}: gate table and metadata verdict conflict')
            if q not in records:
                records[q] = {'verdict': verdict}
    return records


def inspect(root):
    cfg = layout(root)
    metrics, metric_issues = registry(root)
    gates = gate_records(root)
    questions = set(cfg['questions']) | set(gates) | {q.lower() for q in cfg.get('artifacts', {})}
    for folder in ('notes', 'results', 'src', 'code', 'reports'):
        for p in (root / folder).rglob('*'):
            if p.is_file():
                questions.update(m.lower() for m in re.findall(r'(?<![a-z0-9])q[1-9][0-9]*(?![0-9])', p.name, re.I))
    questions.update(m['question'].lower() for m in metrics if isinstance(m, dict) and isinstance(m.get('question'), str) and Q.fullmatch(m['question']))
    rows = list(tables(read(root / 'reports/evidence_matrix.md')))
    findings = [r for r in rows if r.get('severity', '').upper() == 'CRITICAL' and r.get('resolution', '').upper() not in {'RESOLVED', 'FIXED'}]
    result = {}
    for q in sorted(questions, key=lambda x: int(x[1:])):
        paths = dict(model_plan=f'notes/{q}_model_plan.md', run=f'results/{q}_run.json',
                     audit=f'notes/{q}_audit.md', validation=f'reports/{q}_validation.md',
                     handoff=f'notes/handoff_{q}.md', evidence='reports/evidence_matrix.md')
        paths.update(cfg.get('artifacts', {}).get(q, {}))
        checks = {k: 'PASS' if present(root, v) else 'MISSING' for k, v in paths.items()}
        anchors = list(paths.values()) + ['results/paper_metrics.yaml', 'project/project-layout.md',
                                                'notes/bootstrap.md', 'reports/data_contract.md']
        for folder in ('src', 'code', 'problem_files', 'materials'):
            anchors.extend(str(p.relative_to(root)) for p in (root / folder).rglob('*')
                           if p.is_file() and '__pycache__' not in p.parts)
        run = {}
        if checks['run'] == 'PASS':
            try:
                run = json_read(child(root, paths['run']))
                required = ('entry', 'command', 'exit_code', 'outputs', 'inputs', 'config')
                if not isinstance(run, dict) or any(k not in run for k in required):
                    raise ValueError('incomplete run manifest')
                if any(not isinstance(run[k], list) for k in ('inputs', 'outputs')):
                    raise ValueError('run inputs/outputs must be lists')
                if not isinstance(run['command'], str) or type(run['exit_code']) is not int:
                    raise ValueError('run command/exit_code type invalid')
                refs = [run['entry'], run['config'], *run['inputs'], *run['outputs']]
                anchors += refs
                checks['code_run'] = 'PASS' if run['exit_code'] == 0 and run['command'] and run['outputs'] and all(present(root, p) for p in refs) else 'UNVERIFIED'
                checks['code_entry'] = 'PASS' if present(root, run['entry']) else 'MISSING'
            except (ValueError, TypeError, KeyError):
                checks['code_run'] = checks['code_entry'] = 'UNVERIFIED'
        else:
            checks['code_run'] = checks['code_entry'] = 'MISSING'
        audit = marker(read(child(root, paths['audit'])))
        checks['audit'] = 'PASS' if audit in {'PASS', 'PASS WITH LIMITATIONS'} else ('BLOCKED' if audit == 'BLOCKED' else 'MISSING' if not audit else 'UNVERIFIED')
        validation = read(child(root, paths['validation']))
        checks['validation'] = 'PASS' if marker(validation) == 'PASS' and marker(validation, 'evidence') and present(root, marker(validation, 'evidence')) else 'MISSING'
        if marker(validation, 'evidence'):
            anchors.append(marker(validation, 'evidence'))
        figures = run.get('figures', []) if isinstance(run, dict) else []
        if not isinstance(figures, list):
            raise ValueError(f'{q}: figures must be a list of figure/table paths')
        anchors += figures
        checks['figure_table'] = 'PASS' if figures and all(present(root, p) for p in figures) else 'MISSING'
        for m in metrics:
            if isinstance(m, dict):
                anchors.extend(m[k] for k in ('source_script', 'source_result') if isinstance(m.get(k), str) and m[k])
        qm = [m for m in metrics if isinstance(m, dict) and str(m.get('question', '')).lower() == q]
        checks['metrics'] = 'PASS' if qm and not metric_issues else 'UNVERIFIED'
        erows = [r for r in rows if r.get('question', '').lower() == q and 'claim' in r]
        checks['evidence'] = 'PASS' if erows and all(r.get('status') == 'PASS' for r in erows) else 'MISSING'
        qcritical = any(r.get('question', '').lower() in {q, 'all', ''} for r in findings)
        blocked = audit == 'BLOCKED' or gates.get(q, {}).get('verdict') == 'BLOCKED' or qcritical
        essentials = ('model_plan', 'code_entry', 'code_run', 'audit', 'validation', 'figure_table', 'metrics')
        core_ready = all(checks[k] == 'PASS' for k in essentials)
        mvp = core_ready and checks['handoff'] == 'PASS'
        full = mvp and checks['evidence'] == 'PASS'
        precheck = 'PRECHECK_BLOCKED' if blocked else 'PRECHECK_CLOSED_READY' if full else 'PRECHECK_MVP_READY' if mvp else 'PRECHECK_PARTIAL'
        fingerprint = digest(root, anchors)
        record = gates.get(q, {})
        verdict = record.get('verdict', 'MISSING')
        fresh = record.get('artifact_sha256') == fingerprint
        started = any(present(root, paths[k]) for k in ('model_plan', 'run', 'audit', 'handoff')) or bool(qm)
        status = 'BLOCKED' if blocked else 'MVP_READY' if mvp else 'PARTIAL' if started else 'NOT_STARTED'
        if fresh and ((verdict == 'MVP_CLOSED' and mvp) or (verdict == 'CLOSED' and full)) and not blocked:
            status = verdict
        result[q] = dict(status=status, precheck=precheck, checks=checks, artifacts=paths,
                         review_verdict=verdict, review_fresh=fresh, artifact_sha256=fingerprint,
                         core_ready=core_ready)
    return dict(schema_version=1, competition='GMCM', competition_mode=cfg.get('competition_mode', True),
                questions=result), cfg, metric_issues, findings


def drift(root, state):
    path = root / 'project/contest_state.json'
    if not path.exists():
        return ['contest_state missing']
    try:
        old = json_read(path)
    except ValueError:
        return ['contest_state invalid JSON']
    changed = []
    def compare(a, b, prefix=''):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in sorted(set(a) | set(b)):
                compare(a.get(k), b.get(k), f'{prefix}.{k}'.strip('.'))
        elif a != b:
            changed.append(prefix)
    compare(old, state)
    return changed


def next_action(root, state):
    if not present(root, 'notes/bootstrap.md'):
        return 'contest-project-bootstrap', 'official materials, question scope and owners need intake'
    if not present(root, 'reports/data_contract.md') or marker(read(root / 'reports/data_contract.md'), 'verdict') != 'PASS':
        return 'data-contract-auditor', 'data contract missing or not PASS'
    for q, item in state['questions'].items():
        if item['status'] in CLOSED:
            # Downstream handoff/evidence may still be due for an MVP closure.
            if item['checks']['evidence'] != 'PASS':
                return f'{q.upper()} → repo-paper-auditor', 'MVP gate recorded; evidence matrix needs completion'
            continue
        c = item['checks']
        if item['status'] == 'BLOCKED':
            return f'{q.upper()} → result-auditor', 'BLOCKED: resolve evidence defect and re-run question-completion-gate'
        for key, skill in [('model_plan', 'modeling-reviewer'), ('code_run', 'MathModel model-code-and-result-generator'),
                           ('audit', 'result-auditor'), ('validation', 'result-auditor'),
                           ('figure_table', 'scibox-figure'), ('metrics', 'verified-number-registry')]:
            if c[key] != 'PASS':
                return f'{q.upper()} → {skill}', f'{key} {c[key]}; earliest unresolved question before later improvement'
        # Initial gate may record PARTIAL: maintain the unique workflow, then complete its downstream evidence/handoff and re-gate.
        if item['review_verdict'] == 'MISSING':
            return f'{q.upper()} → question-completion-gate', 'core artifacts ready; record verdict and downstream gaps'
        if c['evidence'] != 'PASS':
            return f'{q.upper()} → repo-paper-auditor', 'gate visited; evidence matrix missing or unresolved'
        if c['handoff'] != 'PASS':
            return f'{q.upper()} → paper-handoff', 'audit and registry ready; handoff missing'
        return f'{q.upper()} → question-completion-gate', 'closure missing or stale; review current artifact_sha256'
    cfg = layout(root)
    if not present(root, cfg.get('final_paper', 'paper/final.pdf')):
        return 'MathModel paper-formal-writer', 'all questions closed; assemble and render the final paper'
    if not present(root, 'reports/gmcm_final_review.md'):
        return 'gmcm-final-reviewer', 'rendered paper exists; final review missing'
    return 'mm final-check', 'question loops closed; deterministic preflight then human review'


def refresh(root, state):
    path = root / 'project/contest_state.json'
    if root.is_symlink() or path.is_symlink() or path.parent.is_symlink():
        raise ValueError('Refusing symlink cache path')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', dir=path.parent, prefix='.mm-state-', delete=False, encoding='utf-8') as f:
            temporary = Path(f.name)
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def git(root, *args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(root), *args], capture_output=True, text=True, timeout=30)


def final_digest(root, state, cfg):
    paths = ['reports/question_status.md', 'reports/evidence_matrix.md', 'results/paper_metrics.yaml',
             'materials/gmcm_year_override.md', cfg.get('final_paper', 'paper/final.pdf'), cfg.get('reproduction_entry', 'src/reproduce.py')]
    paths += [str(p.relative_to(root)) for p in (root / 'paper').rglob('*') if p.is_file()]
    combined = digest(root, paths) + ''.join(item['artifact_sha256'] for item in state['questions'].values())
    return hashlib.sha256(combined.encode()).hexdigest()


def final_check(root, state, cfg, metric_issues, findings, changes):
    failures, warnings = [], []
    if not present(root, 'notes/bootstrap.md') or marker(read(root / 'reports/data_contract.md')) != 'PASS':
        failures.append('bootstrap/data contract missing or not PASS')
    if changes:
        failures.append('STATE_DRIFT: run mm refresh')
    if cfg.get('questions_verified') is not True:
        failures.append('question scope unverified in mm-layout; reconcile with official materials')
    for q, item in state['questions'].items():
        if item['status'] not in CLOSED:
            failures.append(f'{q.upper()} {item["status"]}: not at least MVP_CLOSED')
        for key in ('handoff', 'evidence'):
            if item['checks'][key] != 'PASS':
                failures.append(f'{q.upper()} {key} missing/unresolved')
    failures.extend(metric_issues)
    if findings:
        failures.append('CRITICAL unresolved evidence matrix rows')
    year = read(root / 'materials/gmcm_year_override.md')
    if marker(year, 'verified') != 'true' or marker(year, 'official_source') in {None, '', 'null'} or marker(year, 'year') in {None, '', 'null'}:
        failures.append('gmcm_year_override unverified or lacks year/official_source')
    for key, default in [('final_paper', 'paper/final.pdf'), ('reproduction_entry', 'src/reproduce.py')]:
        if not present(root, cfg.get(key, default)):
            failures.append(f'{key} missing')
    fingerprint = final_digest(root, state, cfg)
    review = read(root / 'reports/gmcm_final_review.md')
    if marker(review, 'review_mode') not in {'fast', 'full'}:
        failures.append('final review_mode missing or invalid')
    if marker(review, 'review_mode') == 'fast' and cfg.get('competition_mode', True) is not True:
        failures.append('FAST final review requires competition_mode: true')
    if marker(review) not in {'PASS', 'PASS WITH LIMITATIONS'}:
        failures.append('final review missing or not PASS / PASS WITH LIMITATIONS')
    if marker(review, 'artifact_sha256') != fingerprint:
        failures.append('final review unbound/stale; review current final artifact_sha256')
    top = git(root, 'rev-parse', '--show-toplevel')
    if top.returncode or Path(top.stdout.strip()).resolve() != root.resolve():
        failures.append('project must be an independent Git root')
    else:
        tracked = git(root, 'ls-files', '-z')
        if tracked.returncode:
            failures.append('cannot inspect tracked files')
        for name in tracked.stdout.split('\0'):
            low = name.lower()
            if low.startswith(('corpus/raw/', 'corpus/extracted/')) or (low.endswith('.pdf') and not low.startswith('paper/') and name != cfg.get('final_paper', 'paper/final.pdf')):
                failures.append(f'raw PDF/corpus material tracked: {name}')
        diff = git(root, 'diff', '--check')
        staged = git(root, 'diff', '--cached', '--check')
        if diff.returncode or staged.returncode:
            failures.append('git diff --check: ' + diff.stdout + staged.stdout)
        status = git(root, 'status', '--porcelain', '--untracked-files=all')
        if status.returncode or status.stdout.strip():
            failures.append('Git working tree not clean: ' + status.stdout.strip())
    for folder in ('src', 'code', 'paper', 'notes', 'reports'):
        for p in (root / folder).rglob('*'):
            if p.is_file() and p.suffix.lower() in {'.py', '.sh', '.md', '.tex', '.txt', '.r', '.m'}:
                for n, line in enumerate(read(p).splitlines(), 1):
                    if re.search(r'\b(TODO|HACK)\b', line):
                        label = f'{p.relative_to(root)}:{n}: {line.strip()}'
                        if re.search(r'CRITICAL|HIGH_RISK|FIX_NOW', line):
                            failures.append('high-risk TODO/HACK ' + label)
                        else:
                            warnings.append('human triage TODO/HACK ' + label)
    return dict(verdict='NOT READY' if failures else 'READY FOR HUMAN FINAL REVIEW', failures=failures,
                warnings=warnings, artifact_sha256=fingerprint, human_confirmation_required=True)


def doctor(root):
    import stack
    checks = []
    def add(status, message):
        checks.append(dict(status=status, message=message))
    add('PASS' if sys.version_info >= (3, 10) else 'FAIL', 'Python ' + sys.version.split()[0])
    add('PASS' if shutil.which('git') else 'FAIL', 'Git')
    add('PASS' if shutil.which('codex') else 'WARN', 'Codex CLI availability')
    try:
        s = stack.Stack()
        for source in s.sources:
            try:
                s.check_repo(source)
                s.source_skills(source)
                add('PASS', f'upstream cache / pinned SHA: {source["name"]}')
            except (RuntimeError, OSError) as e:
                add('FAIL', str(e))
        try:
            s.duplicates()
            add('PASS', 'No global MathModel routing conflict')
        except RuntimeError as e:
            add('FAIL', str(e))
        if (root / '.agents/skills/mathmodel-lite').exists():
            add('FAIL', 'project MathModel Standard/Lite conflict')
        for dest, target in s.links():
            add('PASS' if dest.is_symlink() and dest.resolve() == target.resolve() and dest.exists() else 'FAIL', f'installation / broken symlink: {dest}')
        bases = {s.skills, Path.home() / '.agents/skills', root / '.agents/skills'}
        by_name = {}
        for base in bases:
            if base.is_dir():
                for p in base.iterdir():
                    if p.is_symlink() and not p.exists():
                        add('FAIL', f'broken skill symlink: {p}')
                    if (p / 'SKILL.md').is_file():
                        by_name.setdefault(p.name, set()).add(p.resolve())
        for name, paths in sorted(by_name.items()):
            if len(paths) > 1:
                add('FAIL', f'global/project duplicate skill conflict: {name}')
        record = json_read(root / '.agents/mathmodel-source.json')
        valid = re.fullmatch(r'[0-9a-f]{40}', record.get('commit', '')) and record.get('repo') == s.sources[0]['repo'] and record.get('skills') == s.sources[0]['skills']
        add('PASS' if valid else 'FAIL', 'project MathModel version record (project stays pinned independently)')
        for name in record.get('skills', []):
            add('PASS' if present(root, f'.agents/skills/{name}/SKILL.md') else 'FAIL', f'project Skill discovery: {name}')
    except (RuntimeError, OSError, ValueError, KeyError) as e:
        add('FAIL', str(e))
    for folder in stack.LAYOUT:
        add('PASS' if (root / folder).is_dir() else 'FAIL', f'required directory: {folder}')
    add('PASS' if present(root, 'notes/toolchain_versions.md') else 'FAIL', 'toolchain version note')
    cfg = layout(root)
    required = cfg.get('required_python_modules', [])
    for module in sorted(set(required) | {'numpy', 'scipy', 'matplotlib', 'yaml', 'pyomo', 'ortools', 'pymoo', 'pandera', 'shap', 'simpy', 'statsmodels'}):
        try:
            available = importlib.util.find_spec(module) is not None
        except (ModuleNotFoundError, ValueError):
            available = False
        add('PASS' if available else 'FAIL' if module in required else 'WARN', f'{"required" if module in required else "optional"} dependency: {module}')
    add('WARN', 'Filesystem discovery checked; confirm /skills in your installed Codex CLI; no API calls made')
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('status', 'next', 'gate', 'refresh', 'doctor', 'final-check'):
        p = sub.add_parser(name)
        p.add_argument('--json', action='store_true')
        if name == 'gate':
            p.add_argument('question')
        if name == 'status':
            p.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    root = args.project.absolute()
    try:
        if sys.version_info < (3, 10):
            raise ValueError('Python 3.10+ required')
        if args.command == 'doctor':
            output = doctor(root)
            code = int(any(c['status'] == 'FAIL' for c in output))
        else:
            state, cfg, metric_issues, findings = inspect(root)
            changes = drift(root, state)
            action, reason = next_action(root, state)
            target = action.split(' → ')[-1].removeprefix('MathModel ')
            output = dict(recommended_next_action=action, reason=reason,
                          command_or_skill=target if target.startswith('mm ') else '$' + target)
            code = 0
            if args.command == 'gate':
                q = args.question.lower()
                if q not in state['questions']:
                    raise ValueError(f'Unknown question: {q}')
                output.update(state['questions'][q])
                output['authority'] = '$question-completion-gate provides the final gate verdict'
                code = int(output['precheck'] in {'PRECHECK_BLOCKED', 'PRECHECK_PARTIAL'})
            elif args.command == 'final-check':
                output = final_check(root, state, cfg, metric_issues, findings, changes)
                code = int(bool(output['failures']))
            else:
                output['state_drift'] = changes
                if args.command == 'refresh' or getattr(args, 'refresh', False):
                    refresh(root, state)
                    output['changed_fields'] = changes
                    output['refreshed'] = True
                if args.command in {'status', 'refresh'}:
                    output['state'] = state
                    output['blocking_issues'] = metric_issues
        if args.json:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        elif args.command == 'doctor':
            for check in output:
                print(f'{check["status"]}: {check["message"]}')
        else:
            if 'state' in output:
                print('GMCM Competition Status')
                for q, item in output['state']['questions'].items():
                    print(f'\n{q.upper()}  {item["status"]} ({item["precheck"]})')
                    for key, value in item['checks'].items():
                        print(f'    {key:16} {value}')
                    if item['review_verdict'] in CLOSED and not item['review_fresh']:
                        print('    REVIEW_STALE: re-run $question-completion-gate')
            for key, value in output.items():
                if key == 'state':
                    continue
                label = 'STATE_DRIFT (run mm refresh)' if key == 'state_drift' and value else key.replace('_', ' ').capitalize()
                print(f'\n{label}: {json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value}')
        return code
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
