from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class ExitType(str, enum.Enum):
    VOLUNTARY = "voluntary"
    INVOLUNTARY = "involuntary"
    EARLY_COMPLETION = "early_completion"
    MEDICAL = "medical"
    OTHER = "other"


class ExitStatus(str, enum.Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class Exit(Base):
    """Handle trainee exit, resignation, and early release"""
    __tablename__ = "exits"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=False)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), nullable=False)
    
    exit_type = Column(Enum(ExitType), nullable=False)
    requested_date = Column(DateTime, default=datetime.utcnow)
    exit_date = Column(Date, nullable=True)
    
    reason = Column(Text, nullable=True)
    status = Column(Enum(ExitStatus), default=ExitStatus.REQUESTED)
    
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_date = Column(DateTime, nullable=True)
    approval_notes = Column(Text, nullable=True)
    
    # Final evaluation & feedback before exit
    final_evaluation = Column(Text, nullable=True)
    exit_feedback = Column(Text, nullable=True)
    
    # Clearance & handover
    is_clearance_complete = Column(String(20), default="pending")  # pending, in_progress, complete
    clearance_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cohort = relationship("Cohort")
    trainee = relationship("Trainee", back_populates="exits")
    approved_by = relationship("User")


class ConsequenceType(str, enum.Enum):
    MALPRACTICE = "malpractice"
    PERFORMANCE_ISSUE = "performance_issue"
    ATTENDANCE_VIOLATION = "attendance_violation"
    CODE_OF_CONDUCT = "code_of_conduct"
    OTHER = "other"


class ConsequenceSeverity(str, enum.Enum):
    WARNING = "warning"
    SUSPENSION = "suspension"
    EXIT = "exit"


class ConsequenceManagement(Base):
    """Track violations, consequences, and remedial actions"""
    __tablename__ = "consequence_management"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=False)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), nullable=False)
    
    consequence_type = Column(Enum(ConsequenceType), nullable=False)
    severity = Column(Enum(ConsequenceSeverity), default=ConsequenceSeverity.WARNING)
    
    incident_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=False)
    
    action_taken = Column(Text, nullable=True)
    action_date = Column(DateTime, nullable=True)
    
    # Remedial measures
    remedial_plan = Column(Text, nullable=True)
    remedial_completion_date = Column(Date, nullable=True)
    
    # Appeal & review
    appeal_raised = Column(String(20), default="no")  # yes, no, pending
    appeal_notes = Column(Text, nullable=True)
    appeal_decision = Column(String(50), nullable=True)  # approved, rejected
    
    # Documentation
    summary_document = Column(Text, nullable=True)  # Auto-generated summary
    evidence_file = Column(String(200), nullable=True)
    
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    handled_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cohort = relationship("Cohort")
    trainee = relationship("Trainee", back_populates="consequences")
    reported_by = relationship("User", foreign_keys=[reported_by_id])
    handled_by = relationship("User", foreign_keys=[handled_by_id])
