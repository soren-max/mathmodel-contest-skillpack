"""Offline structural checks for the reusable exemplar corpus."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "corpus" / "derived"
PAPER_IDS = (
    "GMCM-2022-B", "GMCM-2023-B", "GMCM-2024-C", "GMCM-2025-C",
    "GMCM-2023-E", "GMCM-2024-E", "GMCM-2021-F", "GMCM-2024-F",
)
CARD_HEADINGS = (
    "# Metadata", "# One-Sentence Value", "# Problem Decomposition",
    "# Overall Modeling Chain", "# Mathematical Structure",
    "## State Variables", "## Decision Variables", "## Parameters",
    "## Objective Functions", "## Constraints", "## Core Relationships",
    "## Assumptions", "# Model Selection Logic", "# Solver / Algorithm",
    "# Validation Audit", "# Figures and Tables", "# Abstract Architecture",
    "# Strengths", "# Weaknesses", "# Reusable Lessons", "# Do NOT Copy",
)
DERIVED_FILES = (
    "core_corpus.md", "problem_decomposition_patterns.md",
    "model_selection_patterns.md", "optimization_patterns.md",
    "validation_patterns.md", "abstract_patterns.md", "figure_patterns.md",
    "paper_structure_patterns.md", "common_mistakes.md", "reviewer_checklist.md",
)


class CorpusTests(unittest.TestCase):
    def test_all_paper_cards_have_required_sections_and_tags(self):
        cards = DERIVED / "paper_cards"
        self.assertEqual({path.stem for path in cards.glob("*.md")}, set(PAPER_IDS))
        for paper_id in PAPER_IDS:
            text = (cards / f"{paper_id}.md").read_text(encoding="utf-8")
            for heading in CARD_HEADINGS:
                self.assertIn(heading, text, f"{paper_id} missing {heading}")
            self.assertIn("[PAPER EVIDENCE]", text)
            self.assertIn("[ANALYST INFERENCE]", text)
            for validation in (
                "baseline", "train/test", "time split", "residual", "error metric",
                "model comparison", "sensitivity", "perturbation", "robustness",
                "simulation", "feasibility check", "practical validation",
            ):
                self.assertIn(f"| {validation} |", text, f"{paper_id} missing {validation}")

    def test_derived_corpus_is_complete_and_tagged(self):
        self.assertEqual(
            {path.name for path in DERIVED.glob("*.md")}, set(DERIVED_FILES)
        )
        for name in DERIVED_FILES:
            text = (DERIVED / name).read_text(encoding="utf-8")
            self.assertIn("[CROSS-PAPER PATTERN]", text, f"{name} lacks pattern tags")
            self.assertIn("[ANALYST INFERENCE]", text, f"{name} lacks inference tags")

    def test_retriever_and_skill_corpus_paths(self):
        retriever = ROOT / "skills" / "exemplar-paper-retriever" / "SKILL.md"
        self.assertTrue(retriever.is_file())
        text = retriever.read_text(encoding="utf-8")
        self.assertIn("最多选三篇", text)
        self.assertIn("../../corpus/derived/", text)
        self.assertEqual((retriever.parent / "../../corpus/derived").resolve(), DERIVED)
        for name in DERIVED_FILES:
            self.assertTrue((DERIVED / name).is_file())
        for skill_name in ("modeling-reviewer", "gmcm-final-reviewer"):
            skill = ROOT / "skills" / skill_name / "SKILL.md"
            self.assertEqual((skill.parent / "../../corpus/derived").resolve(), DERIVED)

    def test_inventory_and_ignore_policy(self):
        inventory = (ROOT / "corpus" / "source_inventory.md").read_text(encoding="utf-8")
        for paper_id in PAPER_IDS:
            self.assertIn(paper_id, inventory)
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/corpus/work/", ignore)
        self.assertIn("/corpus/extracted/", ignore)
        tracked = set()
        git_index = ROOT / ".git" / "index"
        if git_index.exists():
            import subprocess
            result = subprocess.run(
                ["git", "-C", str(ROOT), "ls-files"], text=True,
                stdout=subprocess.PIPE, check=True,
            )
            tracked = set(result.stdout.splitlines())
        self.assertFalse(any(path.lower().endswith(".pdf") for path in tracked))
        self.assertFalse(any(path.startswith("corpus/extracted/") for path in tracked))


if __name__ == "__main__":
    unittest.main()
