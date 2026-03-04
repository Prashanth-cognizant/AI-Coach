from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    trainee_id = Column(Integer, ForeignKey("trainees.id"))
    cohort_id = Column(Integer, ForeignKey("cohorts.id"))
    
    # Self-learning tracking
    self_learning_percentage = Column(Integer, default=0)
    self_learning_completed = Column(Boolean, default=False)
    
    # Hands-on/Project tracking
    hands_on_percentage = Column(Integer, default=0)
    hands_on_completed = Column(Boolean, default=False)
    
    # Assessment readiness
    prerequisites_completed = Column(Boolean, default=False)
    ready_for_assessment = Column(Boolean, default=False)
    
    # Weekly summary
    week_number = Column(Integer, nullable=True)
    week_summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trainee = relationship("Trainee", back_populates="progress_records")
    cohort = relationship("Cohort", back_populates="progress_records")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    trainee_id = Column(Integer, ForeignKey("trainees.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    date = Column(DateTime, nullable=False)
    present = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    trainee = relationship("Trainee", back_populates="attendance_records")


class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    weight = Column(Float, nullable=True)
    body_measurements = Column(Text, nullable=True)
    workout_streak = Column(Integer, default=0)
    total_workouts = Column(Integer, default=0)
    total_calories_burned = Column(Float, default=0.0)
    mood_score = Column(Integer, nullable=True)
    energy_level = Column(Integer, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    water_intake_liters = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_logs")
