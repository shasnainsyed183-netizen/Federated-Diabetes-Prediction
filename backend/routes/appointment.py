from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from backend.core.database import get_db
from backend.models.user import User
from backend.models.patient import Patient
from backend.models.doctor import Doctor
from backend.models.appointment import Appointment
from backend.schemas.appointment_schema import AppointmentCreate, AppointmentResponse, AppointmentStatusUpdate
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# Helper functions to get current patient/doctor profile
def get_current_patient(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Patient:
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can perform this action")
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient

def get_current_doctor(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Doctor:
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can perform this action")
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return doctor


# ========================================
# PATIENT ENDPOINTS
# ========================================

@router.post("/book", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def book_appointment(
    payload: AppointmentCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Patient books an appointment with a doctor"""
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if payload.appointment_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot book an appointment in the past")

    new_appt = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        appointment_date=payload.appointment_date,
        appointment_time=payload.appointment_time,
        reason=payload.reason,
        status="pending"
    )
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)
    return new_appt


@router.get("/my", response_model=List[AppointmentResponse])
def get_my_appointments(
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Patient views their own appointments"""
    appts = db.query(Appointment).filter(Appointment.patient_id == patient.id).order_by(Appointment.appointment_date.desc()).all()
    return appts


# ========================================
# DOCTOR ENDPOINTS
# ========================================

@router.get("/doctor", response_model=List[AppointmentResponse])
def get_doctor_appointments(
    doctor: Doctor = Depends(get_current_doctor),
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Doctor views their appointments (with optional status filter)"""
    query = db.query(Appointment).filter(Appointment.doctor_id == doctor.id)
    if status_filter:
        query = query.filter(Appointment.status == status_filter)
    appts = query.order_by(Appointment.appointment_date.asc()).all()
    return appts


@router.put("/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Doctor approves, rejects, or completes an appointment"""
    appt = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.doctor_id == doctor.id
    ).first()
    
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if payload.status not in ["approved", "rejected", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    appt.status = payload.status
    if payload.doctor_notes:
        appt.doctor_notes = payload.doctor_notes

    db.commit()
    db.refresh(appt)
    return appt