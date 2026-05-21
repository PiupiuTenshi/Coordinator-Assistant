from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

if __package__ is None or __package__ == "":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.models.schemas import AnalyzeRequest, Location
from backend.app.services.symptom_service import symptom_service
from crawler.config import DATA_DIR


DEFAULT_CASES = DATA_DIR / "safety" / "red_flag_cases.jsonl"
DEFAULT_REPORT = DATA_DIR / "reports" / "phase7_safety_report.md"


def read_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def evaluate_case(case: dict) -> dict:
    request = AnalyzeRequest(
        age=case.get("age", 35),
        gender=case.get("gender", "unknown"),
        patient_type=case.get("patient_type", "first_visit"),
        symptom_text=case["symptom_text"],
        duration=case.get("duration", ""),
        discomfort_level=case.get("discomfort_level", 5),
        risk_groups=case.get("risk_groups", []),
        dangerous_symptoms=case.get("dangerous_symptoms", []),
        location=Location(lat=10.7769, lng=106.7009),
        consent=False,
    )
    response = symptom_service.analyze(request)
    failures: list[str] = []

    expected = case.get("expected_triage")
    if expected and response.triage_label != expected:
        failures.append(f"expected {expected}, got {response.triage_label}")

    expected_not = case.get("expected_not_triage")
    if expected_not and response.triage_label == expected_not:
        failures.append(f"must not be {expected_not}")

    if case.get("must_not_recommend_doctor") and response.doctor_recommendations:
        failures.append("doctor recommendations must be hidden for emergency")

    if response.triage_label == "EMERGENCY":
        if not response.nearest_hospitals:
            failures.append("emergency response must include nearest hospitals")
        if not all(hospital.has_emergency for hospital in response.nearest_hospitals):
            failures.append("emergency hospitals must have emergency capability")
        if "không thay thế" not in response.disclaimer.lower():
            failures.append("disclaimer must be present")

    return {
        "case_id": case["case_id"],
        "note": case.get("note", ""),
        "expected": expected or f"not {expected_not}",
        "actual": response.triage_label,
        "risk_level": response.risk_level,
        "recognized_symptoms": response.recognized_symptoms,
        "passed": not failures,
        "failures": failures,
    }


def build_report(results: list[dict]) -> str:
    passed = sum(1 for result in results if result["passed"])
    total = len(results)
    emergency_total = sum(1 for result in results if result["expected"] == "EMERGENCY")
    emergency_passed = sum(1 for result in results if result["expected"] == "EMERGENCY" and result["actual"] == "EMERGENCY")
    lines = [
        "# Báo cáo kiểm thử an toàn y khoa Phase 7",
        "",
        f"- Thời điểm tạo: {datetime.now().isoformat(timespec='seconds')}",
        f"- Tổng số case: {total}",
        f"- Pass: {passed}/{total}",
        f"- Emergency recall seed: {emergency_passed}/{emergency_total}" if emergency_total else "- Emergency recall seed: N/A",
        "",
        "## Kết quả chi tiết",
        "",
        "| Case | Kỳ vọng | Thực tế | Risk | Kết quả | Ghi chú |",
        "|---|---|---|---|---|---|",
    ]
    for result in results:
        status = "PASS" if result["passed"] else "FAIL: " + "; ".join(result["failures"])
        lines.append(
            f"| {result['case_id']} | {result['expected']} | {result['actual']} | "
            f"{result['risk_level']} | {status} | {result['note']} |"
        )
    lines.extend(
        [
            "",
            "## Điều kiện chặn release MVP",
            "",
            "- Bất kỳ case `EMERGENCY` nào không trả về `EMERGENCY`.",
            "- Response `EMERGENCY` vẫn gợi ý đặt lịch/bác sĩ thay vì cấp cứu.",
            "- Response thiếu disclaimer y khoa.",
            "- Response không có bệnh viện cấp cứu gần nhất khi có vị trí.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase 7 medical safety validation suite.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    results = [evaluate_case(case) for case in read_cases(args.cases)]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(build_report(results), encoding="utf-8")
    failed = [result for result in results if not result["passed"]]
    print(f"Wrote safety report to {args.report}")
    print(f"Passed {len(results) - len(failed)}/{len(results)} cases")
    if failed:
        for result in failed:
            print(f"FAIL {result['case_id']}: {'; '.join(result['failures'])}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
