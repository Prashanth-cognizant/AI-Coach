from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Progress, Attendance
from app.models.session import Session as SessionModel
from app.services.ai_service_v2 import summarize_cohort_progress
from typing import List

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/trainee/{trainee_id}")
def get_trainee_progress(trainee_id: int, db: Session = Depends(get_db)):
    """Get trainee's progress records"""
    progress_records = db.query(Progress).filter(Progress.trainee_id == trainee_id).all()
    if not progress_records:
        raise HTTPException(status_code=404, detail="No progress records found")
    return progress_records

@router.post("/trainee/{trainee_id}/update")
def update_trainee_progress(
    trainee_id: int,
    progress_data: dict,
    db: Session = Depends(get_db)
):
    """Update trainee progress"""
    progress = db.query(Progress).filter(Progress.trainee_id == trainee_id).first()
    
    if not progress:
        progress = Progress(trainee_id=trainee_id)
        db.add(progress)
    
    for key, value in progress_data.items():
        if hasattr(progress, key):
            setattr(progress, key, value)
    
    db.commit()
    db.refresh(progress)
    return progress

@router.get("/cohort/{cohort_id}/weekly-summary")
def get_cohort_weekly_summary(cohort_id: int, db: Session = Depends(get_db)):
    """Get weekly cohort performance summary"""
    from app.models.cohort import Cohort, Trainee
    
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    trainees = db.query(Trainee).filter(Trainee.cohort_id == cohort_id).all()
    total = len(trainees)
    
    if total == 0:
        return {"message": "No trainees in this cohort"}
    
    # Calculate metrics
    avg_attendance = sum(t.attendance_percentage for t in trainees) / total if total > 0 else 0
    l1_submissions = sum(1 for t in trainees if t.l1_feedback_submitted)
    
    progress_records = db.query(Progress).filter(Progress.cohort_id == cohort_id).all()
    avg_self_learning = sum(p.self_learning_percentage for p in progress_records) / len(progress_records) if progress_records else 0
    avg_hands_on = sum(p.hands_on_percentage for p in progress_records) / len(progress_records) if progress_records else 0
    
    cohort_data = {
        "cohort_name": cohort.name,
        "total_trainees": total,
        "avg_attendance": avg_attendance,
        "l1_submissions": l1_submissions,
        "self_learning_progress": avg_self_learning,
        "hands_on_completion": avg_hands_on,
        "issues": "Pending - needs evaluation"
    }
    
    summary = summarize_cohort_progress(cohort_data)
    
    return {
        "cohort_id": cohort_id,
        "cohort_name": cohort.name,
        "metrics": cohort_data,
        "ai_summary": summary
    }

@router.post("/attendance/{trainee_id}/mark")
def mark_attendance(
    trainee_id: int,
    session_id: int,
    present: bool,
    db: Session = Depends(get_db)
):
    """Mark trainee attendance for a session"""
    from datetime import datetime
    
    attendance = Attendance(
        trainee_id=trainee_id,
        session_id=session_id,
        date=datetime.utcnow(),
        present=present
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/attendance/trainee/{trainee_id}")
def get_trainee_attendance(trainee_id: int, db: Session = Depends(get_db)):
    """Get trainee's attendance records"""
    records = db.query(Attendance).filter(Attendance.trainee_id == trainee_id).all()
    
    total = len(records)
    present = sum(1 for r in records if r.present)
    percentage = (present / total * 100) if total > 0 else 0
    
    return {
        "trainee_id": trainee_id,
        "total_sessions": total,
        "present": present,
        "absent": total - present,
        "attendance_percentage": percentage,
        "records": records
    }
