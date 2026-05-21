from __future__ import annotations

import argparse
import json
import sys
import urllib.request


def get_text(url: str, timeout: int = 5) -> str:
    return urllib.request.urlopen(url, timeout=timeout).read().decode("utf-8")


def post_json(url: str, payload: dict, timeout: int = 5) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return json.loads(urllib.request.urlopen(request, timeout=timeout).read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test deployed MVP endpoints.")
    parser.add_argument("--backend", default="http://127.0.0.1:8000")
    parser.add_argument("--frontend", default="http://127.0.0.1:5173")
    args = parser.parse_args()

    checks: list[tuple[str, bool, str]] = []

    health = get_text(f"{args.backend}/api/health")
    checks.append(("backend health", '"status":"ok"' in health, health))

    analyze = post_json(
        f"{args.backend}/api/symptom/analyze",
        {
            "age": 45,
            "gender": "male",
            "patient_type": "first_visit",
            "symptom_text": "Tôi bị đau ngực, khó thở và vã mồ hôi từ 30 phút trước.",
            "duration": "30 phút",
            "discomfort_level": 9,
            "risk_groups": [],
            "dangerous_symptoms": [],
            "location": {"lat": 10.7769, "lng": 106.7009},
            "consent": False,
        },
    )
    checks.append(("emergency analyze", analyze.get("triage_label") == "EMERGENCY", analyze.get("triage_label", "")))
    checks.append(("hospital map fields", bool(analyze.get("nearest_hospitals", [{}])[0].get("embed_map_url")), "embed_map_url"))
    checks.append(
        (
            "department route",
            bool(analyze.get("nearest_hospitals", [{}])[0].get("department_route", {}).get("steps")),
            "department_route.steps",
        )
    )

    frontend = get_text(args.frontend)
    checks.append(("frontend index", "Sàng lọc triệu chứng" in frontend, "index loaded"))

    failed = [name for name, ok, _detail in checks if not ok]
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")

    if failed:
        print("Smoke test failed: " + ", ".join(failed), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
