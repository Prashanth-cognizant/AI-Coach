from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.mentoring import Mentor, MentorSession, MentorAvailability, MentorStatus
from app.models.user import User
from app.models.cohort import Trainee
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api/mentors", tags=["mentoring"])

# Mentor Management

@router.post("/register")
def register_mentor(
    user_id: int,
    expertise_areas: str,
    experience_years: int,
    available_hours_per_week: int = 10,
    db: Session = Depends(get_db)
):
    """Register a new mentor"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing = db.query(Mentor).filter(Mentor.user_id == user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already registered as mentor")
        
        mentor = Mentor(
            user_id=user_id,
            expertise_areas=expertise_areas,
            experience_years=experience_years,
            available_hours_per_week=available_hours_per_week
        )
        db.add(mentor)
        db.commit()
        db.refresh(mentor)
        return {"status": "success", "mentor_id": mentor.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def list_mentors(status: str = None, db: Session = Depends(get_db)):
    """List all mentors with optional status filter"""
    query = db.query(Mentor)
    if status:
        query = query.filter(Mentor.status == status)
    mentors = query.all()
    return {
        "count": len(mentors),
        "mentors": [
            {
                "id": m.id,
                "user_id": m.user_id,
                "expertise": m.expertise_areas,
                "experience_years": m.experience_years,
                "status": m.status,
                "available_hours": m.available_hours_per_week
            } for m in mentors
        ]
    }

@router.get("/{mentor_id}")
def get_mentor_profile(mentor_id: int, db: Session = Depends(get_db)):
    """Get mentor profile with availability"""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    return {
        "id": mentor.id,
        "user_id": mentor.user_id,
        "expertise": mentor.expertise_areas,
        "experience_years": mentor.experience_years,
        "status": mentor.status,
        "available_hours": mentor.available_hours_per_week,
        "total_sessions": len(mentor.mentoring_sessions),
        "created_at": mentor.created_at
    }

@router.put("/{mentor_id}")
def update_mentor_profile(
    mentor_id: int,
    expertise_areas: str = None,
    status: str = None,
    available_hours_per_week: int = None,
    db: Session = Depends(get_db)
):
    """Update mentor profile"""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    try:
        if expertise_areas:
            mentor.expertise_areas = expertise_areas
        if status:
            mentor.status = status
        if available_hours_per_week:
            mentor.available_hours_per_week = available_hours_per_week
        
        mentor.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Mentor profile updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Availability Management

@router.post("/{mentor_id}/availability")
def add_mentor_availability(
    mentor_id: int,
    day_of_week: str,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db)
):
    """Add mentor availability slot"""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    try:
        availability = MentorAvailability(
            mentor_id=mentor_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )
        db.add(availability)
        db.commit()
        return {"status": "success", "message": "Availability slot added"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{mentor_id}/availability")
def get_mentor_availability(mentor_id: int, db: Session = Depends(get_db)):
    """Get mentor availability schedule"""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    slots = db.query(MentorAvailability).filter(MentorAvailability.mentor_id == mentor_id).all()
    return {
        "mentor_id": mentor_id,
        "availability_slots": [
            {
                "day": s.day_of_week,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "available": s.is_available
            } for s in slots
        ]
    }

# Mentoring Sessions

@router.post("/{mentor_id}/sessions")
def schedule_mentoring_session(
    mentor_id: int,
    cohort_id: int,
    trainee_id: int,
    scheduled_date: str,
    duration_minutes: int = 60,
    db: Session = Depends(get_db)
):
    """Schedule a mentoring session between mentor and trainee"""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    trainee = db.query(Trainee).filter(Trainee.id == trainee_id).first()
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found")
    
    try:
        session = MentorSession(
            mentor_id=mentor_id,
            trainee_id=trainee_id,
            cohort_id=cohort_id,
            scheduled_date=datetime.fromisoformat(scheduled_date),
            duration_minutes=duration_minutes,
            status="scheduled"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return {"status": "success", "session_id": session.id, "message": "Mentoring session scheduled"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{mentor_id}/sessions")
def get_mentor_sessions(mentor_id: int, db: Session = Depends(get_db)):
    """Get all sessions for a mentor"""
    sessions = db.query(MentorSession).filter(MentorSession.mentor_id == mentor_id).all()
    return {
        "mentor_id": mentor_id,
        "total_sessions": len(sessions),
        "sessions": [
            {
                "id": s.id,
                "trainee_id": s.trainee_id,
                "cohort_id": s.cohort_id,
                "scheduled_date": s.scheduled_date,
                "status": s.status,
                "duration_minutes": s.duration_minutes
            } for s in sessions
        ]
    }

@router.post("/sessions/{session_id}/complete")
def complete_mentoring_session(
    session_id: int,
    topics_covered: str,
    feedback_from_mentor: str,
    db: Session = Depends(get_db)
):
    """Mark mentoring session as complete"""
    session = db.query(MentorSession).filter(MentorSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        session.status = "completed"
        session.topics_covered = topics_covered
        session.feedback_from_mentor = feedback_from_mentor
        session.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Session marked as completed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/{session_id}/feedback")
def submit_trainee_feedback(
    session_id: int,
    feedback: str,
    db: Session = Depends(get_db)
):
    """Submit trainee feedback for mentoring session"""
    session = db.query(MentorSession).filter(MentorSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        session.feedback_from_trainee = feedback
        session.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Feedback submitted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Statistics

@router.get("/{mentor_id}/statistics")
def get_mentor_statistics(mentor_id: int, db: Session = Depends(get_db)):
    """Get mentoring statistics"""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    sessions = db.query(MentorSession).filter(MentorSession.mentor_id == mentor_id).all()
    completed = len([s for s in sessions if s.status == "completed"])
    scheduled = len([s for s in sessions if s.status == "scheduled"])
    
    return {
        "mentor_id": mentor_id,
        "total_sessions": len(sessions),
        "completed_sessions": completed,
        "scheduled_sessions": scheduled,
        "cancellation_rate": f"{((len(sessions) - completed - scheduled) / len(sessions) * 100) if sessions else 0:.1f}%"
    }
