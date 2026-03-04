from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class CohortDocument(Base):
    __tablename__ = "cohort_documents"

    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"))
    
    document_type = Column(String(100), index=True)  # welcome_mail, checklist, template, report, etc.
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    
    # Template info
    is_template = Column(Boolean, default=False)
    template_variables = Column(String(1000), nullable=True)  # JSON list of variables
    
    # Recipient tracking
    recipients = Column(String(255), nullable=True)  # comma-separated emails
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String(50), default="draft")  # draft, generated, sent, archived
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cohort = relationship("Cohort", back_populates="documents")


class DocumentTemplate(Base):
    __tablename__ = "document_templates"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), unique=True, index=True)
    template_type = Column(String(100))  # mom, warning_mail, feedback_reminder, status_tracker, etc.
    content = Column(Text, nullable=False)
    
    # Variables like {{trainee_name}}, {{cohort_name}}, etc.
    required_variables = Column(String(1000), nullable=True)  # JSON array
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=True)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), nullable=True)
    
    alert_type = Column(String(50))  # delay, risk, action_item, escalation, etc.
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Recipient
    assigned_to = Column(String(100), nullable=True)  # role or email
    
    # Status
    status = Column(String(50), default="open")  # open, acknowledged, resolved
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"))
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    task_type = Column(String(50))  # action_item, mitigation, operational, etc.
    
    # Assignment
    assigned_to = Column(String(100), nullable=True)  # role or email
    
    # Timeline
    due_date = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String(50), default="pending")  # pending, in_progress, completed, overdue
    priority = Column(String(20), default="medium")  # low, medium, high
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
