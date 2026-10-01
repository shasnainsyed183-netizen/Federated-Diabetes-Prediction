from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True, index=True)
    disease = Column(String(50), nullable=False, index=True)  # diabetes, heart, stroke, kidney, thyroid
    probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)  # High Risk, Low Risk
    patient_data = Column(Text, nullable=True)  # JSON string of input features
    model_version = Column(String(20), default="v1.0")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    patient = relationship("Patient", backref="predictions")
    doctor = relationship("Doctor", backref="predictions")

    def __repr__(self):
        return f"<Prediction {self.disease} - {self.risk_level}>"