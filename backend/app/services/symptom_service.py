from __future__ import annotations

from processing.symptoms import find_symptoms, load_symptoms
from backend.app.models.schemas import AnalyzeRequest, AnalyzeResponse
from backend.app.rules.triage_rules import classify_triage, temporary_advice_for
from backend.app.services.doctor_service import doctor_service
from backend.app.services.hospital_service import hospital_service
from backend.app.services.specialty_service import specialty_service


DISCLAIMER = (
    "Thông tin chỉ mang tính tham khảo, hỗ trợ sàng lọc ban đầu; "
    "không thay thế chẩn đoán, điều trị hoặc tư vấn trực tiếp của bác sĩ."
)


class SymptomService:
    def __init__(self) -> None:
        self.symptoms = load_symptoms()

    def analyze(self, payload: AnalyzeRequest) -> AnalyzeResponse:
        text = " ".join([payload.symptom_text, payload.duration, " ".join(payload.dangerous_symptoms)])
        recognized_symptoms = sorted(set(find_symptoms(text, self.symptoms)))
        triage_label, risk_level, message = classify_triage(
            text=payload.symptom_text,
            discomfort_level=payload.discomfort_level,
            age=payload.age,
            risk_groups=payload.risk_groups,
            explicit_flags=payload.dangerous_symptoms,
        )
        specialties = specialty_service.recommend(recognized_symptoms)
        primary_specialty = specialties[0].specialty if specialties else ""
        doctors = [] if triage_label == "EMERGENCY" else doctor_service.recommend(primary_specialty, payload.patient_type)
        hospitals = hospital_service.nearby(
            payload.location,
            emergency_only=triage_label == "EMERGENCY",
            target_specialty=primary_specialty,
        )
        return AnalyzeResponse(
            recognized_symptoms=recognized_symptoms,
            triage_label=triage_label,
            risk_level=risk_level,
            message=message,
            temporary_advice=temporary_advice_for(triage_label),
            specialty_recommendations=specialties,
            doctor_recommendations=doctors,
            nearest_hospitals=hospitals,
            disclaimer=DISCLAIMER,
        )


symptom_service = SymptomService()
