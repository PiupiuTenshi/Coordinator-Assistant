from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    AppointmentBookingRequest,
    AppointmentResponse,
    DoctorRecommendation,
    FeedbackRequest,
    HospitalNearbyRequest,
    HospitalRecommendation,
    SpecialtyRecommendation,
)
from backend.app.services.appointment_service import appointment_service
from backend.app.services.doctor_service import doctor_service
from backend.app.services.feedback_service import save_feedback
from backend.app.services.hospital_service import hospital_service
from backend.app.services.specialty_service import specialty_service
from backend.app.services.symptom_service import symptom_service


router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "medical-symptom-qr-ai", "version": "0.4.0"}


@router.post("/symptom/analyze", response_model=AnalyzeResponse)
def analyze_symptom(payload: AnalyzeRequest) -> AnalyzeResponse:
    return symptom_service.analyze(payload)


@router.get("/specialties/recommend", response_model=list[SpecialtyRecommendation])
def recommend_specialties(symptoms: str = "") -> list[SpecialtyRecommendation]:
    symptom_list = [item.strip() for item in symptoms.split(",") if item.strip()]
    return specialty_service.recommend(symptom_list)


@router.get("/doctors/recommend", response_model=list[DoctorRecommendation])
def recommend_doctors(specialty: str = "", patient_type: str = "first_visit") -> list[DoctorRecommendation]:
    return doctor_service.recommend(specialty=specialty, patient_type=patient_type)


@router.get("/doctors/{doctor_id}/available-slots", response_model=list[str])
def available_slots(doctor_id: str) -> list[str]:
    slots = doctor_service.available_slots(doctor_id)
    if not slots:
        raise HTTPException(status_code=404, detail="Doctor not found or no slots available.")
    return slots


@router.post("/appointments/book", response_model=AppointmentResponse)
def book_appointment(payload: AppointmentBookingRequest) -> AppointmentResponse:
    return appointment_service.book(payload)


@router.get("/appointments/{appointment_code}", response_model=AppointmentResponse)
def get_appointment(appointment_code: str) -> AppointmentResponse:
    appointment = appointment_service.get(appointment_code)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return appointment


@router.post("/appointments/{appointment_code}/cancel", response_model=AppointmentResponse)
def cancel_appointment(appointment_code: str) -> AppointmentResponse:
    appointment = appointment_service.cancel(appointment_code)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return appointment


@router.post("/appointments/{appointment_code}/reschedule", response_model=AppointmentResponse)
def reschedule_appointment(appointment_code: str, appointment_time: str) -> AppointmentResponse:
    appointment = appointment_service.reschedule(appointment_code, appointment_time)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return appointment


@router.post("/hospitals/nearby", response_model=list[HospitalRecommendation])
def nearby_hospitals(payload: HospitalNearbyRequest) -> list[HospitalRecommendation]:
    return hospital_service.nearby(
        payload.location,
        emergency_only=payload.emergency_only,
        limit=payload.limit,
        target_specialty=payload.target_specialty,
    )


@router.get("/hospitals/{hospital_id}/directions")
def hospital_directions(hospital_id: str, lat: float | None = None, lng: float | None = None, specialty: str = "") -> dict:
    directions = hospital_service.directions(hospital_id, lat=lat, lng=lng, specialty=specialty)
    if directions is None:
        raise HTTPException(status_code=404, detail="Hospital not found.")
    return directions


@router.post("/feedback")
def feedback(payload: FeedbackRequest) -> dict:
    save_feedback(payload)
    return {"status": "received"}
