from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ProgressLog
from app.models.user import User
from app.schemas import ProgressCreate, ProgressResponse
from app.security import decode_token

router = APIRouter(prefix="/api/progress", tags=["progress"])

def get_current_user(token: str, db: Session = Depends(get_db)):
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=ProgressResponse)
def log_progress(progress: ProgressCreate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    
    db_progress = ProgressLog(
        user_id=user.id,
        weight=progress.weight,
        body_measurements=progress.body_measurements,
        workout_streak=progress.workout_streak,
        total_workouts=progress.total_workouts,
        total_calories_burned=progress.total_calories_burned,
        mood_score=progress.mood_score,
        energy_level=progress.energy_level,
        sleep_hours=progress.sleep_hours,
        water_intake_liters=progress.water_intake_liters,
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.get("/user", response_model=list[ProgressResponse])
def get_user_progress(token: str, skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    progress_logs = db.query(ProgressLog).filter(
        ProgressLog.user_id == user.id
    ).order_by(ProgressLog.created_at.desc()).offset(skip).limit(limit).all()
    return progress_logs

@router.get("/stats")
def get_progress_stats(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    
    latest_progress = db.query(ProgressLog).filter(
        ProgressLog.user_id == user.id
    ).order_by(ProgressLog.created_at.desc()).first()
    
    total_workouts = db.query(ProgressLog).filter(
        ProgressLog.user_id == user.id
    ).count()
    
    total_calories = db.query(ProgressLog).filter(
        ProgressLog.user_id == user.id
    ).first()
    
    stats = {
        "total_workouts": total_workouts,
        "total_calories_burned": total_calories.total_calories_burned if total_calories else 0,
        "current_weight": latest_progress.weight if latest_progress else user.current_weight,
        "average_mood": latest_progress.mood_score if latest_progress else 0,
        "workout_streak": latest_progress.workout_streak if latest_progress else 0,
    }
    return stats

@router.delete("/{progress_id}")
def delete_progress(progress_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    progress = db.query(ProgressLog).filter(
        ProgressLog.id == progress_id,
        ProgressLog.user_id == user.id
    ).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress log not found")
    
    db.delete(progress)
    db.commit()
    return {"message": "Progress log deleted successfully"}
