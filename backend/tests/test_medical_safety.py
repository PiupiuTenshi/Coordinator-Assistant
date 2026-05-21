from __future__ import annotations

import pytest

from safety.run_safety_suite import evaluate_case, read_cases


@pytest.mark.parametrize("case", read_cases(__import__("pathlib").Path("data/safety/red_flag_cases.jsonl")))
def test_medical_safety_case(case: dict) -> None:
    result = evaluate_case(case)
    assert result["passed"], result["failures"]
