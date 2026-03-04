from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.session import Session as SessionModel, SessionAttendee, MoM, SessionType
from app.services.ai_service_v2 import generate_mom
from typing import List

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=dict)
def create_session(
    cohort_id: int,
    session_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new coaching session"""
    db_session = SessionModel(
        cohort_id=cohort_id,
        title=session_data.get("title"),
        description=session_data.get("description"),
        session_type=session_data.get("session_type", SessionType.OTHER),
        scheduled_date=datetime.fromisoformat(session_data.get("scheduled_date")),
        facilitator_id=session_data.get("facilitator_id"),
        location=session_data.get("location"),
        meeting_link=session_data.get("meeting_link")
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get session details"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/{session_id}/attendees")
def add_attendee(
    session_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Add attendee to session"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    attendee = SessionAttendee(session_id=session_id, user_id=user_id)
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee

@router.post("/{session_id}/mark-complete")
def mark_session_complete(
    session_id: int,
    session_notes: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Mark session as complete and generate MoM"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.status = "completed"
    session.actual_date = datetime.utcnow()
    
    # Generate MoM in background
    background_tasks.add_task(
        generate_mom_task,
        session_id=session_id,
        db=db,
        session_notes=session_notes
    )
    
    db.commit()
    db.refresh(session)
    return {"message": "Session marked complete. MoM generation in progress..."}

def generate_mom_task(session_id: int, db: Session, session_notes: dict):
    """Background task to generate MoM"""
    mom_content = generate_mom(session_notes)
    
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    mom = MoM(
        session_id=session_id,
        summary=mom_content.get("summary"),
        action_items=mom_content.get("action_items"),
        key_decisions=mom_content.get("key_decisions"),
        risks_identified=mom_content.get("risks_identified"),
        attendee_list=mom_content.get("attendee_list"),
        recipients=session_notes.get("recipients")
    )
    
    session.mom_generated = True
    session.mom_content = str(mom_content)
    
    db.add(mom)
    db.commit()

@router.get("/{session_id}/mom")
def get_session_mom(session_id: int, db: Session = Depends(get_db)):
    """Get MoM for session"""
    mom = db.query(MoM).filter(MoM.session_id == session_id).first()
    if not mom:
        raise HTTPException(status_code=404, detail="MoM not generated yet")
    return mom

@router.get("/cohort/{cohort_id}/schedule")
def get_cohort_schedule(cohort_id: int, db: Session = Depends(get_db)):
    """Get all sessions for a cohort"""
    sessions = db.query(SessionModel).filter(SessionModel.cohort_id == cohort_id).all()
    return sessions
