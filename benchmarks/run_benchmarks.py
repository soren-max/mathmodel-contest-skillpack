#!/usr/bin/env python3
"""Deterministic smoke checks for five GMCM evidence-audit failure modes."""
import json
from pathlib import Path
import sys


CAUSAL_WORDS = ("导致", "造成", "引起", "cause", "causes", "caused")
MVP_FIELDS = (
    "problem_understood", "mathematical_formulation", "code_exists", "code_ran",
    "numerical_result", "validation", "figure_or_table", "interpretation",
    "limitations", "paper_handoff",
)


def evaluate(case):
    kind = case["kind"]
    if kind == "numeric_registry":
        statuses = set()
        grouped = {}
        for metric in case["metrics"]:
            grouped.setdefault(metric["metric_id"], []).append(metric)
        for metrics in grouped.values():
            if len({json.dumps(m["value"], sort_keys=True) for m in metrics}) > 1:
                statuses.add("CONFLICT")
            if len({m["definition"] for m in metrics}) > 1:
                statuses.add("DEFINITION_RISK")
            if len({m["unit"] for m in metrics}) > 1:
                statuses.add("UNIT_CONFLICT")
        return sorted(statuses)
    if kind == "claim":
        causal = any(word in case["claim"].lower() for word in CAUSAL_WORDS)
        return ["CAUSALITY_RISK"] if causal and case["evidence_type"] != "causal" else ["PASS"]
    if kind == "completion":
        complete = all(case["artifacts"].get(field) is True for field in MVP_FIELDS)
        return ["MVP_CLOSED"] if complete else ["PARTIAL"]
    if kind == "optimization":
        for constraint in case["hard_constraints"]:
            lhs, rhs, tol = constraint["lhs"], constraint["rhs"], constraint.get("tolerance", 0)
            op = constraint["operator"]
            violated = ((op == "<=" and lhs > rhs + tol) or
                        (op == ">=" and lhs < rhs - tol) or
                        (op == "==" and abs(lhs - rhs) > tol))
            if violated:
                return ["BLOCKED", "CRITICAL"]
        return ["PASS"]
    if kind == "method":
        if case["paper_method"].strip().lower() != case["code_method"].strip().lower():
            return ["METHOD_MISMATCH", "CRITICAL"]
        return ["PASS"]
    raise ValueError(f"Unknown benchmark kind: {kind}")


def run(fixtures):
    failures = []
    outputs = []
    for path in sorted(fixtures.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        actual = evaluate(case)
        expected = case["expected"]
        passed = set(actual) == set(expected)
        outputs.append({"case": case["case"], "actual": actual, "expected": expected, "pass": passed})
        if not passed:
            failures.append(path.name)
    return outputs, failures


if __name__ == "__main__":
    fixture_dir = Path(__file__).resolve().parent / "fixtures"
    results, failed = run(fixture_dir)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    sys.exit(1 if failed else 0)
