from __future__ import annotations

from backend.app.data.sample_data import DOCTORS
from backend.app.models.schemas import DoctorRecommendation
from backend.app.services.hospital_service import hospital_service


class DoctorService:
    def recommend(self, specialty: str = "", patient_type: str = "first_visit", limit: int = 3) -> list[DoctorRecommendation]:
        specialty = specialty.strip().lower()
        doctors = [
            doctor
            for doctor in DOCTORS
            if not specialty or doctor["specialty"].lower() == specialty or specialty in doctor["specialty"].lower()
        ]
        if not doctors:
            doctors = DOCTORS
        return [self._to_recommendation(doctor) for doctor in doctors[:limit]]

    def available_slots(self, doctor_id: str) -> list[str]:
        doctor = self.get_doctor(doctor_id)
        return list(doctor.get("slots", [])) if doctor else []

    def get_doctor(self, doctor_id: str) -> dict | None:
        return next((doctor for doctor in DOCTORS if doctor["id"] == doctor_id), None)

    def _to_recommendation(self, doctor: dict) -> DoctorRecommendation:
        slots = doctor.get("slots", [])
        return DoctorRecommendation(
            id=doctor["id"],
            name=doctor["name"],
            degree=doctor["degree"],
            specialty=doctor["specialty"],
            hospital_id=doctor["hospital_id"],
            hospital_name=hospital_service.name_for(doctor["hospital_id"]),
            next_available_slot=slots[0] if slots else None,
        )


doctor_service = DoctorService()
