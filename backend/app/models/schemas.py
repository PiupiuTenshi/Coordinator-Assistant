from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


TriageLabel = Literal["SELF_CARE", "BOOK_APPOINTMENT", "URGENT_CARE", "EMERGENCY"]
RiskLevel = Literal["low", "medium", "high", "critical"]
PatientType = Literal["first_visit", "follow_up"]


class Location(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class AnalyzeRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    gender: str = Field(default="unknown")
    patient_type: PatientType = "first_visit"
    symptom_text: str = Field(..., min_length=2, max_length=1500)
    duration: str = ""
    discomfort_level: int = Field(default=5, ge=1, le=10)
    risk_groups: list[str] = Field(default_factory=list)
    dangerous_symptoms: list[str] = Field(default_factory=list)
    location: Location | None = None
    consent: bool = False


class SpecialtyRecommendation(BaseModel):
    specialty: str
    department: str
    reason: str
    confidence: float = Field(..., ge=0, le=1)


class DoctorRecommendation(BaseModel):
    id: str
    name: str
    degree: str
    specialty: str
    hospital_id: str
    hospital_name: str
    next_available_slot: str | None = None


class DepartmentRoute(BaseModel):
    specialty: str
    department: str
    building: str
    floor: str
    room: str
    estimated_walk_minutes: int
    start_label: str
    end_label: str
    map_points: list[list[float]]
    steps: list[str]


class HospitalRecommendation(BaseModel):
    id: str
    name: str
    address: str
    lat: float
    lng: float
    distance_km: float | None = None
    phone: str
    has_emergency: bool
    opening_hours: str
    map_url: str
    osm_url: str
    embed_map_url: str
    department_route: DepartmentRoute | None = None


class AnalyzeResponse(BaseModel):
    recognized_symptoms: list[str]
    triage_label: TriageLabel
    risk_level: RiskLevel
    message: str
    temporary_advice: list[str]
    specialty_recommendations: list[SpecialtyRecommendation]
    doctor_recommendations: list[DoctorRecommendation]
    nearest_hospitals: list[HospitalRecommendation]
    disclaimer: str


class HospitalNearbyRequest(BaseModel):
    location: Location | None = None
    emergency_only: bool = False
    limit: int = Field(default=3, ge=1, le=10)
    target_specialty: str = ""


class AppointmentBookingRequest(BaseModel):
    patient_type: PatientType
    doctor_id: str
    specialty: str
    hospital_id: str
    appointment_time: str
    symptom_summary: str = Field(default="", max_length=1500)
    consent: bool = False


class AppointmentResponse(BaseModel):
    appointment_code: str
    patient_type: PatientType
    doctor_id: str
    specialty: str
    hospital_id: str
    appointment_time: str
    symptom_summary: str
    status: str


class FeedbackRequest(BaseModel):
    session_id: str = ""
    rating: Literal["useful", "not_useful", "unsafe", "other"] = "useful"
    comment: str = Field(default="", max_length=1000)
    triage_label: str = ""
