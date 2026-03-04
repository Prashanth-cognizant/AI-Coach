from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class SessionType(str, enum.Enum):
    PLATFORM_WALKTHROUGH = "platform_walkthrough"
    SOLUTIONS_TEAM = "solutions_team"
    BU_LEADER_CONNECT = "bu_leader_connect"
    MENTOR_INTRO = "mentor_intro"
    WEEKLY_FEEDBACK = "weekly_feedback"
    GRADUATION = "graduation"
    OTHER = "other"

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"))
    title = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    session_type = Column(Enum(SessionType), default=SessionType.OTHER)
    
    # Scheduling
    scheduled_date = Column(DateTime, nullable=False)
    actual_date = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    # Participants
    facilitator_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String(255), nullable=True)
    meeting_link = Column(String(255), nullable=True)
    
    # Status
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled, postponed
    
    # Generated content
    mom_generated = Column(Boolean, default=False)
    mom_content = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cohort = relationship("Cohort", back_populates="sessions")
    facilitator = relationship("User", foreign_keys=[facilitator_id])
    attendees = relationship("SessionAttendee", back_populates="session")
    mom_record = relationship("MoM", uselist=False, back_populates="session")


class SessionAttendee(Base):
    __tablename__ = "session_attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    attended = Column(Boolean, default=False)
    feedback_score = Column(Float, nullable=True)  # 1-5 rating
    notes = Column(Text, nullable=True)
    
    session = relationship("Session", back_populates="attendees")
    user = relationship("User")


class MoM(Base):
    __tablename__ = "mom"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), unique=True)
    
    # Generated content
    summary = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    key_decisions = Column(Text, nullable=True)
    risks_identified = Column(Text, nullable=True)
    attendee_list = Column(Text, nullable=True)
    
    # Status
    generated_at = Column(DateTime, default=datetime.utcnow)
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    recipients = Column(String(255), nullable=True)  # comma-separated emails
    
    session = relationship("Session", back_populates="mom_record")
