#!/usr/bin/env python3
"""Small stdlib-only implementation shared by the installation Bash entry points."""
import argparse
import contextlib
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OWN = ('contest-project-bootstrap', 'modeling-reviewer', 'exemplar-paper-retriever',
       'data-contract-auditor', 'result-auditor', 'verified-number-registry',
       'structured-optimization', 'repo-paper-auditor', 'question-completion-gate',
       'paper-handoff', 'gmcm-final-reviewer')
NAMES = ('MathModel-Skill', 'sci-box', 'PaperSpine', 'scientific-agent-skills')
LAYOUT = ('data/raw', 'data/processed', 'src', 'results', 'figures', 'notes',
          'reports', 'paper', 'materials', 'project', 'problem_files', '.agents/skills')


def say(status, message):
    print(f'{status}: {message}', flush=True)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(*args, cwd=None):
    result = subprocess.run([str(a) for a in args], cwd=cwd, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=180)
    require(result.returncode == 0, f'{args[0]} failed: {result.stderr.strip()}')
    return result.stdout.strip()


def git(path, *args):
    return run('git', '-C', path, *args)


def exists(path):
    return path.exists() or path.is_symlink()


def safe_child(root, relative):
    path = root / relative
    require(path.resolve().is_relative_to(root.resolve()), f'Path escapes root: {path}')
    # Do not write through user-supplied directory symlinks, even inside root.
    for part in (path, *path.parents):
        if part == root:
            break
        require(not part.is_symlink(), f'Refusing symlink path: {part}')
    return path


def write_new(path, content):
    if exists(path):
        say('WARN', f'Preserved existing {path}')
        return
    with path.open('x', encoding='utf-8') as stream:
        stream.write(content)


def atomic_json(path, value):
    require(not path.is_symlink(), f'Refusing symlink: {path}')
    with tempfile.NamedTemporaryFile('w', dir=path.parent, prefix='.mm-',
                                     encoding='utf-8', delete=False) as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


class Stack:
    def __init__(self):
        require(sys.version_info >= (3, 10), 'Python 3.10+ is required')
        require(shutil.which('git'), 'git is required')
        self.cache = Path(os.environ.get('MM_STACK_HOME', '~/.local/share/mathmodel-stack')).expanduser().absolute()
        self.codex = Path(os.environ.get('MM_CODEX_HOME', os.environ.get('CODEX_HOME', '~/.codex'))).expanduser().absolute()
        self.bindir = Path(os.environ.get('MM_BIN_DIR', '~/.local/bin')).expanduser().absolute()
        self.skills = self.codex / 'skills'
        self.lockpath = ROOT / 'config/sources.lock'
        self.lock = json.loads(self.lockpath.read_text(encoding='utf-8'))
        require(self.lock.get('schema_version') == 1, 'Unsupported sources.lock schema')
        self.sources = self.lock['sources']
        require(tuple(s['name'] for s in self.sources) == NAMES, 'Unexpected source names/order')
        for source in self.sources:
            require(re.fullmatch(r'[0-9a-f]{40}', source['commit']), 'Commit must be a full SHA')
            require(source['repo'].startswith('https://github.com/') and
                    re.fullmatch(r'https://github.com/[\w.-]+/[\w.-]+\.git', source['repo']),
                    'Sources must use official GitHub HTTPS URLs')
            run('git', 'check-ref-format', '--branch', source['branch'])
            require(source.get('license') and source.get('purpose') and source.get('install_mode'),
                    f'Incomplete provenance metadata: {source["name"]}')
            require(not set(source.get('optional_skills', [])) & set(source['skills']),
                    f'Enabled/optional skill overlap: {source["name"]}')

    def repo(self, source):
        return self.cache / source['name']

    def check_repo(self, source, pinned=True):
        path = self.repo(source)
        require(path.is_dir() and not path.is_symlink() and (path / '.git').is_dir(),
                f'Missing or unmanaged cache: {path}; run install.sh')
        require(Path(git(path, 'rev-parse', '--show-toplevel')).resolve() == path.resolve(),
                f'Not a standalone cache repo: {path}')
        require(git(path, 'config', '--get', 'remote.origin.url') == source['repo'], f'Origin mismatch: {path}')
        require(not git(path, 'status', '--porcelain', '--untracked-files=all'),
                f'Cache has local changes; preserve/review them before continuing: {path}')
        if pinned:
            require(git(path, 'rev-parse', 'HEAD') == source['commit'],
                    f'Commit differs from sources.lock: {path}; run install.sh')

    def source_skills(self, source):
        base = safe_child(self.repo(source), source['skills_path'])
        require(base.is_dir(), f'Upstream layout changed: {base}')
        expected = source['skills']
        if (base / 'SKILL.md').is_file():
            paths = [base]
        elif source.get('allow_extra_skills'):
            paths = [safe_child(base, name) for name in sorted(expected)]
        else:
            paths = sorted(p for p in base.iterdir()
                           if p.is_dir() and (p / 'SKILL.md').is_file())
        require([p.name for p in paths] == sorted(expected), f'Unexpected skills in {base}')
        checked = paths + [safe_child(base, name) for name in source.get('optional_skills', [])]
        for path in checked:
            require((path / 'SKILL.md').is_file(), f'Missing selected skill: {path}')
            require(not any(p.is_symlink() for p in path.rglob('*')),
                    f'Upstream skill contains symlinks; review before installing: {path}')
        return paths

    def links(self):
        pairs = [(self.skills / name, ROOT / 'skills' / name) for name in OWN]
        for source in self.sources[1:]:
            pairs.extend((self.skills / name, self.repo(source) / source['skills_path'] /
                          (name if len(source['skills']) > 1 else '')) for name in source['skills'])
        pairs.extend((self.bindir / name, ROOT / 'bin' / name) for name in ('mm-init', 'mm'))
        return pairs

    def check_links(self, targets=False):
        for destination, source in self.links():
            require(not exists(destination) or (destination.is_symlink() and
                    destination.resolve() == source.resolve()),
                    f'Existing file/link conflicts: {destination}; move it aside yourself, then retry')
            if targets:
                require(source.exists(), f'Missing link target: {source}')

    def duplicates(self):
        for base in {self.skills, Path.home() / '.agents/skills'}:
            for name in self.sources[0]['skills'] + ['mathmodel-lite']:
                require(not exists(base / name), f'Global MathModel routing conflict: {base / name}; review/remove it manually')

    @contextlib.contextmanager
    def exclusive(self):
        self.cache.mkdir(parents=True, exist_ok=True)
        lockfile = safe_child(self.cache, '.skillpack-operation.lock')
        with lockfile.open('a') as stream:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise RuntimeError('Another install/update/init is running') from error
            yield

    def install(self):
        self.check_links()
        self.duplicates()
        for directory in (self.codex, self.skills, self.bindir):
            require(not exists(directory) or directory.is_dir(), f'Not a directory: {directory}')
        # Preflight all existing caches before changing any of them.
        for source in self.sources:
            if exists(self.repo(source)):
                self.check_repo(source, pinned=False)
        for source in self.sources:
            path = self.repo(source)
            if not exists(path):
                say('INFO', f'Cloning {source["repo"]}')
                run('git', 'clone', '--no-checkout', '--single-branch', '--branch',
                    source['branch'], source['repo'], path)
            present = subprocess.run(['git', '-C', str(path), 'cat-file', '-e',
                                      source['commit'] + '^{commit}'], capture_output=True).returncode == 0
            if not present:
                git(path, 'fetch', '--no-tags', 'origin', source['commit'])
            git(path, 'checkout', '--detach', source['commit'])
            self.check_repo(source)
            self.source_skills(source)
        self.check_links(targets=True)
        for directory in (self.skills, self.bindir):
            directory.mkdir(parents=True, exist_ok=True)
        for destination, source in self.links():
            if not exists(destination):
                destination.symlink_to(source)
            say('PASS', f'Installed {destination}')
        return 0  # install.sh runs verify.sh after releasing the operation lock.

    def verify(self):
        failures = 0

        def check(label, operation):
            nonlocal failures
            try:
                operation()
                say('PASS', label)
            except (RuntimeError, OSError) as error:
                failures += 1
                say('FAIL', str(error))

        for source in self.sources:
            check(source['name'] + ' @ ' + source['commit'], lambda s=source: self.check_repo(s))
            check(source['name'] + ' skill layout', lambda s=source: self.source_skills(s))
        for destination, source in self.links():
            check(str(destination), lambda d=destination, s=source: require(
                d.is_symlink() and d.resolve() == s.resolve() and
                ((d / 'SKILL.md').is_file() if d.name not in {'mm-init', 'mm'} else os.access(d, os.X_OK)),
                f'Missing, incorrect, or broken installation: {d}'))
        check('No global MathModel routing conflict', self.duplicates)
        path_dirs = {Path(p).expanduser().resolve() for p in os.get_exec_path() if p}
        say('PASS' if self.bindir.resolve() in path_dirs else 'WARN', f'PATH contains {self.bindir}'
            if self.bindir.resolve() in path_dirs else f'Add {self.bindir} to PATH in your shell profile')
        say('PASS' if shutil.which('codex') else 'WARN', 'Codex CLI available' if shutil.which('codex')
            else 'Codex CLI not found; install it separately before starting a contest')
        # Requested legacy path is preserved; current Codex also documents ~/.agents/skills.
        say('WARN', 'Global skills use CODEX_HOME/skills as requested; check /skills in your Codex version (see README).')
        say('PASS' if failures == 0 else 'FAIL', f'Verification complete: {failures} failure(s)')
        return 1 if failures else 0

    def update(self):
        self.check_links()
        for source in self.sources:
            self.check_repo(source)
        proposed = json.loads(json.dumps(self.lock))
        for source in proposed['sources']:
            path = self.repo(source)
            git(path, 'fetch', '--no-tags', 'origin', 'refs/heads/' + source['branch'])
            new = git(path, 'rev-parse', 'FETCH_HEAD^{commit}')
            say('INFO', f'{source["name"]}: current {source["commit"]} -> new {new}')
            source['commit'] = new
        changed = []
        try:
            for old, new in zip(self.sources, proposed['sources']):
                git(self.repo(old), 'checkout', '--detach', new['commit'])
                changed.append(old)
                self.source_skills(new)
            atomic_json(self.lockpath, proposed)
        except Exception:
            for old in reversed(changed):
                git(self.repo(old), 'checkout', '--detach', old['commit'])
            raise
        self.lock = proposed
        self.sources = proposed['sources']
        say('WARN', 'Global linked tools now use the new versions. Existing project MathModel copies stay frozen.')
        say('INFO', 'Review git diff config/sources.lock; run install.sh and commit the lock before the contest.')
        return 0

    def init(self, directory):
        project = Path(directory).expanduser().absolute()
        require(not project.is_symlink(), f'Refusing symlink project root: {project}')
        project = project.resolve()
        require(project != ROOT and not project.is_relative_to(ROOT), 'Choose a contest project outside this SkillPack repo')
        require(project != self.cache and not project.is_relative_to(self.cache), 'Project cannot be inside upstream cache')
        self.duplicates()
        for source in self.sources:
            self.check_repo(source)
        paths = self.source_skills(self.sources[0])
        for relative in (*LAYOUT, 'AGENTS.md', 'README.md', 'project/project-layout.md',
                         'materials/gmcm.md', 'materials/gmcm_year_override.md',
                         'results/paper_metrics.yaml', 'project/contest_state.json',
                         'notes/toolchain_versions.md', '.agents/mathmodel-source.json',
                         '.agents/third-party/MathModel-Skill/LICENSE'):
            safe_child(project, relative)
        marker = project / '.agents/mathmodel-source.json'
        require(not exists(project / '.agents/skills/mathmodel-lite'), 'Do not mix Standard and Lite')
        installed = exists(marker)
        if installed:
            previous = json.loads(marker.read_text())
            require(previous['repo'] == self.sources[0]['repo'] and
                    re.fullmatch(r'[0-9a-f]{40}', previous['commit']), 'Invalid project source record')
            for name in previous['skills']:
                skill = safe_child(project, '.agents/skills/' + name)
                require((skill / 'SKILL.md').is_file(), f'Existing project installation incomplete: {skill}')
            say('WARN', f'Preserving project MathModel @ {previous["commit"]}; no automatic project upgrade')
        else:
            require(not exists(project / 'notes/toolchain_versions.md'), 'Version note exists without source record; review project before initializing')
            for path in paths:
                require(not exists(project / '.agents/skills' / path.name), f'Existing project skill conflicts: {path.name}')
        project.mkdir(parents=True, exist_ok=True)
        inside = subprocess.run(['git', '-C', str(project), 'rev-parse', '--show-toplevel'],
                                capture_output=True, text=True)
        require(inside.returncode != 0 or Path(inside.stdout.strip()).resolve() == project,
                'Target is inside another Git repo; choose its root or a separate directory')
        if inside.returncode != 0:
            run('git', 'init', project)
        for relative in LAYOUT:
            (project / relative).mkdir(parents=True, exist_ok=True)
        if not installed:
            # Copy only the official Codex skill package, never the complete upstream repository.
            for path in paths:
                shutil.copytree(path, project / '.agents/skills' / path.name)
            legal = project / '.agents/third-party/MathModel-Skill'
            legal.mkdir(parents=True, exist_ok=True)
            write_new(legal / 'LICENSE', (self.repo(self.sources[0]) / 'LICENSE').read_text())
            atomic_json(marker, {key: self.sources[0][key] for key in ('repo', 'branch', 'commit', 'skills')})
        for name, target in [('AGENTS.md', 'AGENTS.md'), ('README.md', 'README.md'),
                             ('project-layout.md', 'project/project-layout.md')]:
            write_new(project / target, (ROOT / 'templates' / name).read_text())
        write_new(project / 'materials/gmcm.md', (ROOT / 'rubrics/gmcm.md').read_text())
        write_new(project / 'materials/gmcm_year_override.md',
                  (ROOT / 'rubrics/gmcm_year_override.md').read_text())
        write_new(project / 'results/paper_metrics.yaml',
                  (ROOT / 'templates/paper_metrics.yaml').read_text())
        write_new(project / 'project/contest_state.json',
                  (ROOT / 'templates/contest_state.json').read_text())
        own_commit = git(ROOT, 'rev-parse', 'HEAD')
        dirty = bool(git(ROOT, 'status', '--porcelain'))
        content = '# Toolchain versions\n\nInitialized (UTC): ' + dt.datetime.now(dt.timezone.utc).isoformat() + '\n\n'
        content += '| Tool | Commit |\n| --- | --- |\n'
        content += ''.join(f'| {s["name"]} | `{s["commit"]}` |\n' for s in self.sources)
        content += f'| SkillPack | `{own_commit}`' + (' (dirty working tree)' if dirty else '') + ' |\n'
        content += '\nMathModel is copied into .agents/skills; license: .agents/third-party/MathModel-Skill/LICENSE.\n'
        content += 'Global tools are linked to the cache and may change after update.sh; freeze all updates during a contest.\n'
        write_new(project / 'notes/toolchain_versions.md', content)
        say('PASS', f'Project initialized: {project}')
        say('INFO', 'Next: add official problems to problem_files/, original data to data/raw/, and rules to materials/.')
        say('INFO', f'cd {str(project)!r}; codex — start with $contest-project-bootstrap and set J/F/L owners.')
        return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('install', 'update', 'verify', 'init'))
    parser.add_argument('project', nargs='?')
    args = parser.parse_args()
    if (args.command == 'init') != (args.project is not None):
        parser.error('Usage: mm-init <project-directory>; other commands take no arguments')
    try:
        stack = Stack()
        if args.command == 'verify':
            return stack.verify()
        with stack.exclusive():
            return stack.init(args.project) if args.command == 'init' else getattr(stack, args.command)()
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        say('FAIL', str(error))
        return 1


if __name__ == '__main__':
    sys.exit(main())
