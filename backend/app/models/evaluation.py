from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"))
    name = Column(String(255), index=True)
    evaluation_type = Column(String(50))  # interim, final, remedial, L1_feedback
    
    scheduled_date = Column(DateTime, nullable=False)
    actual_date = Column(DateTime, nullable=True)
    
    # Content & Guidelines
    guidelines = Column(Text, nullable=True)
    rubric = Column(Text, nullable=True)
    
    status = Column(String(50), default="scheduled")  # scheduled, in_progress, completed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cohort = relationship("Cohort", back_populates="evaluations")
    scores = relationship("EvaluationScore", back_populates="evaluation")


class EvaluationScore(Base):
    __tablename__ = "evaluation_scores"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    trainee_id = Column(Integer, ForeignKey("trainees.id"))
    
    score = Column(Float, nullable=True)  # 0-100
    grade = Column(String(2), nullable=True)  # A, B, C, F
    feedback = Column(Text, nullable=True)
    passed = Column(Boolean, default=False)
    requires_remedial = Column(Boolean, default=False)
    
    evaluated_by = Column(String(255), nullable=True)  # evaluator name/email
    evaluated_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    evaluation = relationship("Evaluation", back_populates="scores")
    trainee = relationship("Trainee", back_populates="evaluation_scores")


class L1Feedback(Base):
    __tablename__ = "l1_feedback"

    id = Column(Integer, primary_key=True, index=True)
    trainee_id = Column(Integer, ForeignKey("trainees.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    
    # Feedback questions (1-5 scale)
    content_quality = Column(Integer, nullable=True)
    facilitator_effectiveness = Column(Integer, nullable=True)
    relevance = Column(Integer, nullable=True)
    pacing = Column(Integer, nullable=True)
    
    # Free text
    strengths = Column(Text, nullable=True)
    improvements = Column(Text, nullable=True)
    additional_comments = Column(Text, nullable=True)
    
    submitted_at = Column(DateTime, default=datetime.utcnow)
