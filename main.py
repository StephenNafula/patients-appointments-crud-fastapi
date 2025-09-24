from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./patients_appointments.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=True)
    patient = relationship("Patient", back_populates="appointments")

# Schemas
class AppointmentBase(BaseModel):
    patient_id: int
    date: datetime
    reason: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    date: Optional[datetime] = None
    reason: Optional[str] = None

class AppointmentRead(AppointmentBase):
    id: int
    class Config:
        orm_mode = True

class PatientBase(BaseModel):
    name: str = Field(..., example="John Doe")
    age: Optional[int] = None
    gender: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class PatientRead(PatientBase):
    id: int
    created_at: datetime
    appointments: List[AppointmentRead] = []
    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create DB tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="Single-file Patients & Appointments API")

@app.get("/")
def root():
    return {"msg": "Welcome to Patients & Appointments API. See /docs for API documentation."}

# Patients endpoints
@app.post("/patients/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(name=patient.name, age=patient.age, gender=patient.gender)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=List[PatientRead])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Patient).offset(skip).limit(limit).all()

@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: int, updates: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if updates.name is not None:
        patient.name = updates.name
    if updates.age is not None:
        patient.age = updates.age
    if updates.gender is not None:
        patient.gender = updates.gender
    db.commit()
    db.refresh(patient)
    return patient

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return None

# Appointments endpoints
@app.post("/appointments/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient does not exist")
    db_appointment = Appointment(patient_id=appointment.patient_id, date=appointment.date, reason=appointment.reason)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.get("/appointments/", response_model=List[AppointmentRead])
def list_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Appointment).offset(skip).limit(limit).all()

@app.get("/appointments/{appointment_id}", response_model=AppointmentRead)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.put("/appointments/{appointment_id}", response_model=AppointmentRead)
def update_appointment(appointment_id: int, updates: AppointmentUpdate, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if updates.date is not None:
        appointment.date = updates.date
    if updates.reason is not None:
        appointment.reason = updates.reason
    db.commit()
    db.refresh(appointment)
    return appointment

@app.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return None

