from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class MentorStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    RETIRED = "retired"


class Mentor(Base):
    """Mentor profile and availability"""
    __tablename__ = "mentors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    expertise_areas = Column(String(500), nullable=True)  # Comma-separated
    experience_years = Column(Integer, nullable=True)
    status = Column(Enum(MentorStatus), default=MentorStatus.ACTIVE)
    available_hours_per_week = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="mentor_profile")
    mentoring_sessions = relationship("MentorSession", back_populates="mentor")
    availability = relationship("MentorAvailability", back_populates="mentor", cascade="all, delete-orphan")


class MentorAvailability(Base):
    """Mentor schedule and availability slots"""
    __tablename__ = "mentor_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id"), nullable=False)
    day_of_week = Column(String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = Column(String(10), nullable=False)  # HH:MM format
    end_time = Column(String(10), nullable=False)    # HH:MM format
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    mentor = relationship("Mentor", back_populates="availability")


class MentorSession(Base):
    """Individual mentoring sessions between mentor and trainee"""
    __tablename__ = "mentor_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id"), nullable=False)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), nullable=False)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(String(20), default="scheduled")  # scheduled, completed, cancelled
    topics_covered = Column(Text, nullable=True)
    feedback_from_mentor = Column(Text, nullable=True)
    feedback_from_trainee = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    mentor = relationship("Mentor", back_populates="mentoring_sessions")
    trainee = relationship("Trainee", back_populates="mentoring_sessions")
    cohort = relationship("Cohort")
