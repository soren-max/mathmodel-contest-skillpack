"""GMCM-first v0.9 architecture, schema, and benchmark tests."""
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "contest-project-bootstrap", "modeling-reviewer", "exemplar-paper-retriever",
    "data-contract-auditor", "result-auditor", "verified-number-registry",
    "structured-optimization", "repo-paper-auditor", "question-completion-gate",
    "paper-handoff", "gmcm-final-reviewer",
}


class GmcmV09Tests(unittest.TestCase):
    def test_expected_core_skills_exist_exactly(self):
        actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, EXPECTED_SKILLS)

    def test_gmcm_rubrics_exist_and_year_rules_are_unverified(self):
        stable = (ROOT / "rubrics/gmcm.md").read_text(encoding="utf-8")
        override = (ROOT / "rubrics/gmcm_year_override.md").read_text(encoding="utf-8")
        for heading in (
            "Problem Understanding", "Mathematical Modeling", "Model Selection",
            "Multi-question Progression", "Computation", "Validation", "Optimization",
            "Innovation", "Engineering Value", "Paper Quality",
        ):
            self.assertIn(f"## {heading}", stable)
        self.assertIn("verified: false", override)
        self.assertIn("official_source: null", override)

    def test_paper_metric_template_and_schema(self):
        template = json.loads((ROOT / "templates/paper_metrics.yaml").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/paper_metrics.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(template, {"schema_version": 1, "metrics": []})
        self.assertEqual(schema["properties"]["schema_version"]["const"], 1)
        required = set(schema["properties"]["metrics"]["items"]["required"])
        self.assertTrue({"metric_id", "value", "unit", "definition", "source_result",
                         "validation_status", "approved_for_paper"}.issubset(required))

    def test_benchmark_fixtures_trigger_expected_issues(self):
        result = subprocess.run(
            ["python3", str(ROOT / "benchmarks/run_benchmarks.py")],
            cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        outputs = json.loads(result.stdout)
        self.assertEqual(len(outputs), 5)
        self.assertTrue(all(item["pass"] for item in outputs))
        statuses = {status for item in outputs for status in item["actual"]}
        self.assertTrue({"CONFLICT", "DEFINITION_RISK", "CAUSALITY_RISK", "PARTIAL",
                         "BLOCKED", "CRITICAL", "METHOD_MISMATCH"}.issubset(statuses))

    def test_atomic_source_is_selective_and_pinned(self):
        lock = json.loads((ROOT / "config/sources.lock").read_text(encoding="utf-8"))
        for source in lock["sources"]:
            self.assertRegex(source["commit"], r"^[0-9a-f]{40}$")
            self.assertIn("purpose", source)
            self.assertIn("install_mode", source)
        atomic = next(s for s in lock["sources"] if s["name"] == "scientific-agent-skills")
        self.assertEqual(set(atomic["skills"]), {
            "scientific-critical-thinking", "statistical-analysis", "statsmodels",
            "uncertainty-and-units",
        })
        self.assertEqual(set(atomic["optional_skills"]), {"shap", "simpy"})
        self.assertTrue(atomic["allow_extra_skills"])

    def test_optional_dependencies_are_not_forced(self):
        entrypoints = "\n".join(
            (ROOT / name).read_text(encoding="utf-8")
            for name in ("install.sh", "update.sh", "verify.sh", "bin/mm-init")
        )
        for package in ("pyomo", "ortools", "pymoo", "pandera", "shap", "simpy", "statsmodels"):
            self.assertNotIn(f"pip install {package}", entrypoints.lower())

    def test_paper_narrative_contract_is_wired_into_handoff_and_review(self):
        contract = (ROOT / "rubrics/paper_narrative.md").read_text(encoding="utf-8")
        handoff = (ROOT / "skills/paper-handoff/SKILL.md").read_text(encoding="utf-8")
        reviewer = (ROOT / "skills/gmcm-final-reviewer/SKILL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "docs/workflow.md").read_text(encoding="utf-8")

        for token in (
            "Problem", "Mathematical abstraction", "Model selection reason",
            "Numerical results", "Question conclusion", "Link to next question",
            "Before equation", "After equation", "Purpose", "Observation",
            "Interpretation", "Implication", "approved_for_paper: true",
        ):
            self.assertIn(token, contract)
        self.assertIn("| Question | Problem | Method | Result | Status |", contract)
        self.assertIn("Formula Context Ledger", handoff)
        self.assertIn("Abstract-ready Problem–Method–Result", handoff)
        self.assertIn("PAPER NARRATIVE", reviewer)
        self.assertIn("Model–result–paper consistency", reviewer)
        self.assertIn("PaperSpine integration", workflow)

    def test_no_raw_papers_or_extracted_text_tracked(self):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files"], text=True,
            stdout=subprocess.PIPE, check=True,
        )
        tracked = result.stdout.splitlines()
        self.assertFalse(any(path.lower().endswith(".pdf") for path in tracked))
        self.assertFalse(any(path.startswith("corpus/extracted/") for path in tracked))


if __name__ == "__main__":
    unittest.main()
