from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class IssueStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IssuePriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueCategory(str, enum.Enum):
    TECHNICAL = "technical"
    SOFTWARE = "software"
    HARDWARE = "hardware"
    NETWORK = "network"
    ACCOUNT = "account"
    OTHER = "other"


class Issue(Base):
    """IT issue/ticket tracking system"""
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=False)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), nullable=True)
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(IssueCategory), default=IssueCategory.OTHER)
    priority = Column(Enum(IssuePriority), default=IssuePriority.MEDIUM)
    status = Column(Enum(IssueStatus), default=IssueStatus.OPEN)
    
    resolution_notes = Column(Text, nullable=True)
    resolved_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cohort = relationship("Cohort")
    trainee = relationship("Trainee", back_populates="issues")
    reported_by = relationship("User", foreign_keys=[reported_by_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])


class Query(Base):
    """Query/Support ticket system for trainee questions"""
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=False)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), nullable=False)
    raised_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), default="general")  # academic, technical, personal, other
    
    status = Column(String(20), default="open")  # open, assigned, resolved, closed
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    resolution = Column(Text, nullable=True)
    resolved_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cohort = relationship("Cohort")
    trainee = relationship("Trainee", back_populates="queries")
    raised_by = relationship("User", foreign_keys=[raised_by_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
