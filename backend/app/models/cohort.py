from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class CohortStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    PLANNING = "planning"

class Cohort(Base):
    __tablename__ = "cohorts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(CohortStatus), default=CohortStatus.ACTIVE)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    batch_code = Column(String(100), unique=True, index=True)
    
    # Leadership
    location_lead_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    bu_pm_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainees = relationship("Trainee", back_populates="cohort")
    sessions = relationship("Session", back_populates="cohort")
    evaluations = relationship("Evaluation", back_populates="cohort")
    progress_records = relationship("Progress", back_populates="cohort")
    documents = relationship("CohortDocument", back_populates="cohort")
    
    location_lead = relationship("User", foreign_keys=[location_lead_id])
    bu_pm = relationship("User", foreign_keys=[bu_pm_id])


class Trainee(Base):
    __tablename__ = "trainees"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"))
    employee_id = Column(String(100), unique=True, index=True)
    
    # Tracking
    attendance_percentage = Column(Integer, default=0)
    l1_feedback_submitted = Column(Boolean, default=False)
    asset_allocation_status = Column(String(50), default="pending")  # pending, allocated, completed
    software_installation_status = Column(String(50), default="pending")  # pending, in_progress, completed
    buddy_mentor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    status = Column(String(50), default="active")  # active, graduated, exited, on_hold
    exit_reason = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cohort = relationship("Cohort", back_populates="trainees")
    user = relationship("User", foreign_keys=[user_id])
    buddy_mentor = relationship("User", foreign_keys=[buddy_mentor_id])
    progress_records = relationship("Progress", back_populates="trainee")
    evaluation_scores = relationship("EvaluationScore", back_populates="trainee")
    attendance_records = relationship("Attendance", back_populates="trainee")
    mentoring_sessions = relationship("MentorSession", back_populates="trainee")
    issues = relationship("Issue", back_populates="trainee")
    queries = relationship("Query", back_populates="trainee")
    exits = relationship("Exit", back_populates="trainee")
    consequences = relationship("ConsequenceManagement", back_populates="trainee")
