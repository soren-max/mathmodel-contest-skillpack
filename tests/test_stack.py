"""Offline integration tests: real Git repos, isolated paths, no user settings changes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd=None, env=None):
    return subprocess.run([str(a) for a in args], cwd=cwd, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)


def commit(repo, message):
    for args in [('add', '.'), ('-c', 'user.name=SkillPack test', '-c',
                 'user.email=test@example.invalid', 'commit', '-qm', message)]:
        result = run('git', '-C', repo, *args)
        assert result.returncode == 0, result.stdout
    return run('git', '-C', repo, 'rev-parse', 'HEAD').stdout.strip()


class StackTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='mm-stack-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.pack = self.base / 'pack with spaces'
        self.pack.mkdir()
        for name in ('config', 'scripts', 'skills', 'templates', 'bin', 'rubrics', 'schemas'):
            shutil.copytree(ROOT / name, self.pack / name, ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('install.sh', 'update.sh', 'verify.sh'):
            shutil.copy2(ROOT / name, self.pack / name)
        self.env = os.environ.copy()
        self.env.update(MM_STACK_HOME=str(self.base / 'cache'),
                        MM_CODEX_HOME=str(self.base / 'codex'),
                        MM_BIN_DIR=str(self.base / 'bin'),
                        GIT_TERMINAL_PROMPT='0', HOME=str(self.base / 'home'),
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        self.env['PATH'] = str(self.base / 'bin') + os.pathsep + self.env['PATH']
        self.lock = json.loads((self.pack / 'config/sources.lock').read_text())
        self.env['GIT_CONFIG_COUNT'] = str(len(self.lock['sources']) + 1)
        self.remotes = []
        for i, source in enumerate(self.lock['sources']):
            repo = self.base / ('upstream-' + source['name'])
            run('git', 'init', '-q', '--initial-branch=' + source['branch'], repo)
            skillbase = repo / source['skills_path']
            for name in source['skills'] + source.get('optional_skills', []):
                folder = skillbase if skillbase.name == name else skillbase / name
                folder.mkdir(parents=True)
                (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Test fixture.\n---\nFixture v1\n')
            (repo / 'LICENSE').write_text('Test fixture license\n')
            source['commit'] = commit(repo, 'v1')
            self.remotes.append(repo)
            self.env[f'GIT_CONFIG_KEY_{i}'] = f'url.{repo.as_uri()}.insteadOf'
            self.env[f'GIT_CONFIG_VALUE_{i}'] = source['repo']
        protocol_index = len(self.lock['sources'])
        self.env[f'GIT_CONFIG_KEY_{protocol_index}'] = 'protocol.file.allow'
        self.env[f'GIT_CONFIG_VALUE_{protocol_index}'] = 'always'
        (self.pack / 'config/sources.lock').write_text(json.dumps(self.lock))
        run('git', 'init', '-q', self.pack)
        commit(self.pack, 'fixture pack')

    def command(self, name, *args, success=True):
        result = run('bash', self.pack / name, *args, env=self.env)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result.stdout

    def test_install_init_idempotency_and_provenance(self):
        before = (self.pack / 'config/sources.lock').read_bytes()
        self.command('install.sh')
        self.command('install.sh')
        self.assertEqual(before, (self.pack / 'config/sources.lock').read_bytes())
        self.assertIn('0 failure(s)', self.command('verify.sh'))
        project = self.base / 'Contest with spaces'
        self.command('bin/mm-init', project)
        self.assertTrue((self.base / 'bin/mm').is_symlink())
        state = (project / 'project/contest_state.json').read_bytes()
        notes = (project / 'notes/toolchain_versions.md').read_bytes()
        (project / 'AGENTS.md').write_text('Keep my instructions\n')
        (project / 'README.md').write_text('Keep my README\n')
        self.assertIn('WARN', self.command('bin/mm-init', project))
        self.assertEqual((project / 'AGENTS.md').read_text(), 'Keep my instructions\n')
        self.assertEqual((project / 'README.md').read_text(), 'Keep my README\n')
        self.assertEqual(notes, (project / 'notes/toolchain_versions.md').read_bytes())
        self.assertEqual(state, (project / 'project/contest_state.json').read_bytes())
        self.assertEqual(len(list((project / '.agents/skills').glob('*/SKILL.md'))), 10)
        self.assertTrue((project / 'materials/gmcm.md').is_file())
        self.assertIn('verified: false', (project / 'materials/gmcm_year_override.md').read_text())
        self.assertEqual(json.loads((project / 'results/paper_metrics.yaml').read_text()),
                         {'schema_version': 1, 'metrics': []})
        self.assertTrue((project / '.agents/third-party/MathModel-Skill/LICENSE').is_file())
        for name in self.lock['sources'][0]['skills']:
            self.assertFalse((self.base / 'codex/skills' / name).exists())
        self.assertEqual(run('git', '-C', project, 'rev-parse', '--show-toplevel').stdout.strip(), str(project))

    def test_preserves_existing_global_file(self):
        target = self.base / 'codex/skills/modeling-reviewer'
        target.mkdir(parents=True)
        (target / 'user.txt').write_text('user data')
        self.assertIn('conflicts', self.command('install.sh', success=False))
        self.assertEqual((target / 'user.txt').read_text(), 'user data')
        self.assertFalse((self.base / 'cache/MathModel-Skill').exists())

    def test_broken_global_symlink_not_overwritten(self):
        target = self.base / 'bin/mm-init'
        target.parent.mkdir()
        target.symlink_to(self.base / 'missing-user-program')
        self.command('install.sh', success=False)
        self.assertEqual(target.readlink(), self.base / 'missing-user-program')

    def test_cache_dirt_and_wrong_commit_detected(self):
        self.command('install.sh')
        cache = self.base / 'cache/MathModel-Skill'
        (cache / 'user-data.txt').write_text('preserve me')
        self.assertIn('local changes', self.command('install.sh', success=False))
        self.command('verify.sh', success=False)
        self.assertEqual((cache / 'user-data.txt').read_text(), 'preserve me')
        commit(cache, 'local change')
        self.assertIn('differs', self.command('verify.sh', success=False))

    def test_update_is_explicit_and_projects_stay_frozen(self):
        self.command('install.sh')
        project = self.base / 'contest'
        self.command('bin/mm-init', project)
        skill = next((project / '.agents/skills').glob('*/SKILL.md'))
        original = skill.read_bytes()
        old_note = (project / 'notes/toolchain_versions.md').read_bytes()
        remote = self.remotes[0]
        upstream_skill = next((remote / self.lock['sources'][0]['skills_path']).glob('*/SKILL.md'))
        upstream_skill.write_text(upstream_skill.read_text() + '\nv2\n')
        new = commit(remote, 'v2')
        self.command('install.sh')
        cache = self.base / 'cache/MathModel-Skill'
        self.assertEqual(run('git', '-C', cache, 'rev-parse', 'HEAD').stdout.strip(), self.lock['sources'][0]['commit'])
        self.assertIn('-> new ' + new, self.command('update.sh'))
        self.command('install.sh')
        self.assertEqual(run('git', '-C', cache, 'rev-parse', 'HEAD').stdout.strip(), new)
        self.command('bin/mm-init', project)
        self.assertEqual(skill.read_bytes(), original)
        self.assertEqual((project / 'notes/toolchain_versions.md').read_bytes(), old_note)

    def test_fresh_install_uses_pin_when_upstream_is_ahead(self):
        remote = self.remotes[0]
        (remote / 'new-upstream-file').write_text('v2')
        new = commit(remote, 'ahead of lock')
        self.command('install.sh')
        actual = run('git', '-C', self.base / 'cache/MathModel-Skill', 'rev-parse', 'HEAD').stdout.strip()
        self.assertEqual(actual, self.lock['sources'][0]['commit'])
        self.assertNotEqual(actual, new)

    def test_global_mathmodel_conflict_is_rejected(self):
        duplicate = self.base / 'codex/skills' / self.lock['sources'][0]['skills'][0]
        duplicate.mkdir(parents=True)
        self.assertIn('routing conflict', self.command('install.sh', success=False))
        self.assertTrue(duplicate.is_dir())

    def test_update_layout_failure_rolls_back(self):
        self.command('install.sh')
        old = (self.pack / 'config/sources.lock').read_bytes()
        target = next((self.remotes[1] / 'skills').glob('*/SKILL.md'))
        target.rename(target.with_name('REMOVED.md'))
        commit(self.remotes[1], 'break layout')
        self.command('update.sh', success=False)
        self.assertEqual(old, (self.pack / 'config/sources.lock').read_bytes())
        self.command('verify.sh')

    def test_symlink_path_does_not_write_outside_project(self):
        self.command('install.sh')
        project = self.base / 'contest'
        project.mkdir()
        outside = self.base / 'outside'
        outside.mkdir()
        (project / 'data').symlink_to(outside)
        self.command('bin/mm-init', project, success=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_existing_project_skill_preserved(self):
        self.command('install.sh')
        project = self.base / 'contest'
        target = project / '.agents/skills' / self.lock['sources'][0]['skills'][0]
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('User skill')
        self.command('bin/mm-init', project, success=False)
        self.assertEqual((target / 'SKILL.md').read_text(), 'User skill')

    def test_nested_git_repo_rejected(self):
        self.command('install.sh')
        parent = self.base / 'parent'
        run('git', 'init', '-q', parent)
        self.assertIn('inside another Git repo', self.command('bin/mm-init', parent / 'child', success=False))
        self.assertFalse((parent / 'child/.agents').exists())

    def test_path_warning_does_not_fail(self):
        self.command('install.sh')
        self.env['PATH'] = os.environ['PATH']
        self.assertIn('WARN: Add ', self.command('verify.sh'))


if __name__ == '__main__':
    unittest.main()
