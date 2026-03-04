from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Cohort, Trainee, CohortStatus
from app.schemas import CohortCreate, CohortUpdate, TraineeCreate
from typing import List

router = APIRouter(prefix="/cohorts", tags=["cohorts"])

@router.post("/", response_model=dict)
def create_cohort(cohort: CohortCreate, db: Session = Depends(get_db)):
    """Create a new cohort"""
    db_cohort = Cohort(
        name=cohort.name,
        description=cohort.description,
        batch_code=cohort.batch_code,
        start_date=cohort.start_date,
        end_date=cohort.end_date,
        location=cohort.location,
        status=CohortStatus.PLANNING
    )
    db.add(db_cohort)
    db.commit()
    db.refresh(db_cohort)
    return db_cohort

@router.get("/{cohort_id}")
def get_cohort(cohort_id: int, db: Session = Depends(get_db)):
    """Get cohort details"""
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    return cohort

@router.get("/")
def list_cohorts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    """List all cohorts"""
    query = db.query(Cohort)
    if status:
        query = query.filter(Cohort.status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/{cohort_id}/trainees")
def get_cohort_trainees(cohort_id: int, db: Session = Depends(get_db)):
    """Get all trainees in a cohort"""
    trainees = db.query(Trainee).filter(Trainee.cohort_id == cohort_id).all()
    return trainees

@router.post("/{cohort_id}/trainees")
def add_trainee_to_cohort(
    cohort_id: int,
    trainee: TraineeCreate,
    db: Session = Depends(get_db)
):
    """Add a trainee to cohort"""
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    db_trainee = Trainee(
        cohort_id=cohort_id,
        user_id=trainee.user_id,
        employee_id=trainee.employee_id
    )
    db.add(db_trainee)
    db.commit()
    db.refresh(db_trainee)
    return db_trainee

@router.get("/{cohort_id}/dashboard")
def get_cohort_dashboard(cohort_id: int, db: Session = Depends(get_db)):
    """Get cohort overview dashboard"""
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    trainees = db.query(Trainee).filter(Trainee.cohort_id == cohort_id).all()
    
    total_trainees = len(trainees)
    active_trainees = sum(1 for t in trainees if t.status == "active")
    graduated = sum(1 for t in trainees if t.status == "graduated")
    exited = sum(1 for t in trainees if t.status == "exited")
    
    avg_attendance = sum(t.attendance_percentage for t in trainees) / total_trainees if total_trainees > 0 else 0
    
    return {
        "cohort_id": cohort.id,
        "name": cohort.name,
        "status": cohort.status,
        "start_date": cohort.start_date,
        "end_date": cohort.end_date,
        "total_trainees": total_trainees,
        "active_trainees": active_trainees,
        "graduated": graduated,
        "exited": exited,
        "average_attendance": avg_attendance,
        "days_remaining": (cohort.end_date - datetime.utcnow()).days
    }

@router.put("/{cohort_id}")
def update_cohort(
    cohort_id: int,
    cohort_update: CohortUpdate,
    db: Session = Depends(get_db)
):
    """Update cohort details"""
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    update_data = cohort_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cohort, field, value)
    
    db.commit()
    db.refresh(cohort)
    return cohort
