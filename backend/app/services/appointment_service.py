from __future__ import annotations

from uuid import uuid4

from backend.app.models.schemas import AppointmentBookingRequest, AppointmentResponse


class AppointmentService:
    def __init__(self) -> None:
        self._appointments: dict[str, AppointmentResponse] = {}

    def book(self, payload: AppointmentBookingRequest) -> AppointmentResponse:
        code = "APT-" + uuid4().hex[:8].upper()
        appointment = AppointmentResponse(
            appointment_code=code,
            patient_type=payload.patient_type,
            doctor_id=payload.doctor_id,
            specialty=payload.specialty,
            hospital_id=payload.hospital_id,
            appointment_time=payload.appointment_time,
            symptom_summary=payload.symptom_summary,
            status="pending_confirmation",
        )
        self._appointments[code] = appointment
        return appointment

    def get(self, appointment_code: str) -> AppointmentResponse | None:
        return self._appointments.get(appointment_code)

    def cancel(self, appointment_code: str) -> AppointmentResponse | None:
        appointment = self._appointments.get(appointment_code)
        if appointment is None:
            return None
        updated = appointment.model_copy(update={"status": "cancelled"})
        self._appointments[appointment_code] = updated
        return updated

    def reschedule(self, appointment_code: str, appointment_time: str) -> AppointmentResponse | None:
        appointment = self._appointments.get(appointment_code)
        if appointment is None:
            return None
        updated = appointment.model_copy(update={"appointment_time": appointment_time, "status": "pending_confirmation"})
        self._appointments[appointment_code] = updated
        return updated


appointment_service = AppointmentService()
