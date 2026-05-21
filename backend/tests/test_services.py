from __future__ import annotations

from backend.app.models.schemas import AnalyzeRequest, Location
from backend.app.services.hospital_service import hospital_service
from backend.app.services.symptom_service import symptom_service


def test_emergency_red_flag_analysis() -> None:
    response = symptom_service.analyze(
        AnalyzeRequest(
            age=45,
            gender="male",
            symptom_text="Tôi bị đau ngực dữ dội, khó thở và vã mồ hôi từ 30 phút trước.",
            duration="30 phút",
            discomfort_level=9,
            location=Location(lat=10.7769, lng=106.7009),
        )
    )

    assert response.triage_label == "EMERGENCY"
    assert response.risk_level == "critical"
    assert "đau ngực" in response.recognized_symptoms
    assert response.nearest_hospitals
    assert response.doctor_recommendations == []


def test_non_negated_red_flag_book_appointment() -> None:
    response = symptom_service.analyze(
        AnalyzeRequest(
            age=32,
            symptom_text="Tôi đau ngực nhẹ, không kèm khó thở, muốn đặt lịch khám.",
            discomfort_level=4,
        )
    )

    assert response.triage_label in {"BOOK_APPOINTMENT", "SELF_CARE"}
    assert response.triage_label != "EMERGENCY"


def test_nearby_hospitals_include_map_links_and_distance() -> None:
    hospitals = hospital_service.nearby(Location(lat=10.7769, lng=106.7009), emergency_only=True)

    assert hospitals
    assert hospitals[0].distance_km is not None
    assert hospitals[0].has_emergency is True
    assert hospitals[0].map_url.startswith("https://www.google.com/maps/dir/")
    assert hospitals[0].osm_url.startswith("https://www.openstreetmap.org/")
    assert "export/embed.html" in hospitals[0].embed_map_url


def test_nearby_hospitals_include_department_route() -> None:
    hospitals = hospital_service.nearby(
        Location(lat=10.7769, lng=106.7009),
        emergency_only=False,
        target_specialty="Tim mạch",
    )

    assert hospitals
    assert hospitals[0].department_route is not None
    assert hospitals[0].department_route.department == "Khoa Tim mạch"
    assert hospitals[0].department_route.steps
