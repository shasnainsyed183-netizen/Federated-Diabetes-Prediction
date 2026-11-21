from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime


class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str = Field(..., min_length=5, max_length=500)


class AppointmentStatusUpdate(BaseModel):
    status: str = Field(..., description="pending, approved, rejected, completed, cancelled")
    doctor_notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str
    status: str
    doctor_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True