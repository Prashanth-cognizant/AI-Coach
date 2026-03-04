from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    role = Column(String(50), default="trainee")  # trainee, mentor, trainer, admin, bu_pm, location_lead
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    fitness_goal = Column(String(255), nullable=True)
    current_weight = Column(Float, nullable=True)
    target_weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    mentor_profile = relationship("Mentor", back_populates="user", uselist=False)

    # Fitness progress logs
    progress_logs = relationship("ProgressLog", back_populates="user")

