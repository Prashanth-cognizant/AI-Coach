from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models.session import Session as SessionModel
from app.models import Progress
from app.models.documents import Alert
from typing import List

router = APIRouter(prefix="/reminders", tags=["reminders"])

class ReminderService:
    @staticmethod
    def create_session_reminder(session_id: int, reminder_hours_before: int = 24) -> dict:
        """Create a reminder for an upcoming session"""
        return {
            "session_id": session_id,
            "reminder_type": "session",
            "schedule": f"{reminder_hours_before} hours before session",
            "message": "Upcoming coaching session reminder",
            "status": "scheduled"
        }
    
    @staticmethod
    def create_feedback_reminder(session_id: int) -> dict:
        """Create reminder for L1 feedback submission"""
        return {
            "session_id": session_id,
            "reminder_type": "l1_feedback",
            "schedule": "24 hours after session",
            "message": "Please submit your session feedback",
            "status": "scheduled"
        }
    
    @staticmethod
    def create_progress_alert(trainee_id: int, progress_metric: str, threshold: float) -> dict:
        """Create alert for low progress"""
        return {
            "trainee_id": trainee_id,
            "alert_type": "progress_warning",
            "metric": progress_metric,
            "threshold": threshold,
            "message": f"Progress in {progress_metric} is below {threshold}%",
            "severity": "high",
            "status": "open"
        }
    
    @staticmethod
    def create_attendance_alert(trainee_id: int, attendance_percentage: float) -> dict:
        """Create alert for low attendance"""
        if attendance_percentage < 75:
            severity = "critical"
        elif attendance_percentage < 85:
            severity = "high"
        else:
            severity = "medium"
        
        return {
            "trainee_id": trainee_id,
            "alert_type": "attendance_warning",
            "attendance": attendance_percentage,
            "message": f"Attendance at {attendance_percentage}% - at risk",
            "severity": severity,
            "status": "open"
        }
    
    @staticmethod
    def create_evaluation_reminder(evaluation_id: int, days_before: int = 3) -> dict:
        """Create reminder for upcoming evaluation"""
        return {
            "evaluation_id": evaluation_id,
            "reminder_type": "evaluation",
            "schedule": f"{days_before} days before evaluation",
            "message": "Upcoming evaluation - prepare trainees",
            "status": "scheduled"
        }
    
    @staticmethod
    def create_daily_digest(cohort_id: int) -> dict:
        """Create daily digest of cohort activities"""
        return {
            "cohort_id": cohort_id,
            "reminder_type": "daily_digest",
            "schedule": "09:00 AM daily",
            "message": "Daily cohort activity digest",
            "includes": [
                "Today's sessions",
                "Pending tasks",
                "Open alerts",
                "Progress updates"
            ],
            "status": "scheduled"
        }

reminder_service = ReminderService()

@router.post("/session-reminder/{session_id}")
def schedule_session_reminder(
    session_id: int,
    hours_before: int = 24,
    recipients: str = "admin@company.com",
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Schedule a reminder for an upcoming session"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    reminder = reminder_service.create_session_reminder(session_id, hours_before)
    
    if background_tasks:
        background_tasks.add_task(
            send_reminder_email,
            session_name=session.title,
            recipients=recipients,
            scheduled_date=session.scheduled_date,
            reminder_type="session"
        )
    
    return {
        **reminder,
        "scheduled_for": session.scheduled_date - timedelta(hours=hours_before)
    }

@router.post("/feedback-reminder/{session_id}")
def schedule_feedback_reminder(
    session_id: int,
    recipients: str = "admin@company.com",
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Schedule feedback submission reminder"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    reminder = reminder_service.create_feedback_reminder(session_id)
    
    if background_tasks:
        background_tasks.add_task(
            send_reminder_email,
            session_name=session.title,
            recipients=recipients,
            reminder_type="feedback",
            scheduled_for=session.actual_date + timedelta(hours=24) if session.actual_date else None
        )
    
    return reminder

@router.post("/check-progress-alerts/{cohort_id}")
def check_progress_alerts(
    cohort_id: int,
    progress_threshold: float = 50.0,
    db: Session = Depends(get_db)
):
    """Check and create alerts for low progress"""
    from app.models.cohort import Trainee
    
    trainees = db.query(Trainee).filter(Trainee.cohort_id == cohort_id).all()
    alerts_created = []
    
    for trainee in trainees:
        progress = db.query(Progress).filter(Progress.trainee_id == trainee.id).first()
        
        if progress:
            if progress.self_learning_percentage < progress_threshold:
                alert = reminder_service.create_progress_alert(
                    trainee.id,
                    "self_learning",
                    progress_threshold
                )
                alerts_created.append(alert)
            
            if progress.hands_on_percentage < progress_threshold:
                alert = reminder_service.create_progress_alert(
                    trainee.id,
                    "hands_on",
                    progress_threshold
                )
                alerts_created.append(alert)
    
    return {"alerts_created": len(alerts_created), "alerts": alerts_created}

@router.post("/check-attendance-alerts/{cohort_id}")
def check_attendance_alerts(
    cohort_id: int,
    attendance_threshold: float = 80.0,
    db: Session = Depends(get_db)
):
    """Check and create alerts for low attendance"""
    from app.models.cohort import Trainee
    
    trainees = db.query(Trainee).filter(Trainee.cohort_id == cohort_id).all()
    alerts_created = []
    
    for trainee in trainees:
        if trainee.attendance_percentage < attendance_threshold:
            alert = reminder_service.create_attendance_alert(
                trainee.id,
                trainee.attendance_percentage
            )
            
            # Create actual alert in database
            alert_record = Alert(
                cohort_id=cohort_id,
                trainee_id=trainee.id,
                alert_type=alert["alert_type"],
                severity=alert["severity"],
                title=f"Attendance Alert: {trainee.employee_id}",
                description=alert["message"],
                assigned_to="trainer@company.com"
            )
            db.add(alert_record)
            alerts_created.append(alert)
    
    db.commit()
    return {"alerts_created": len(alerts_created), "alerts": alerts_created}

@router.get("/pending/{cohort_id}")
def get_pending_reminders(cohort_id: int, db: Session = Depends(get_db)):
    """Get all pending reminders for a cohort"""
    from app.models.session import Session as SessionModel
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    upcoming_sessions = db.query(SessionModel).filter(
        SessionModel.cohort_id == cohort_id,
        SessionModel.scheduled_date > now,
        SessionModel.scheduled_date <= now + timedelta(days=7),
        SessionModel.status == "scheduled"
    ).all()
    
    reminders = []
    for session in upcoming_sessions:
        hours_until = (session.scheduled_date - now).total_seconds() / 3600
        reminders.append({
            "type": "session_upcoming",
            "session_id": session.id,
            "title": session.title,
            "scheduled_date": session.scheduled_date,
            "hours_until": hours_until
        })
    
    return {"pending_reminders": reminders}

@router.post("/daily-digest/{cohort_id}")
def generate_daily_digest(cohort_id: int, db: Session = Depends(get_db)):
    """Generate daily digest for cohort"""
    from app.models.session import Session as SessionModel
    from app.models.documents import Task
    from datetime import datetime, timedelta
    
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    
    # Today's sessions
    today_sessions = db.query(SessionModel).filter(
        SessionModel.cohort_id == cohort_id,
        SessionModel.scheduled_date >= today,
        SessionModel.scheduled_date < tomorrow
    ).all()
    
    # Pending tasks
    pending_tasks = db.query(Task).filter(
        Task.cohort_id == cohort_id,
        Task.status != "completed"
    ).all()
    
    # Open alerts
    open_alerts = db.query(Alert).filter(
        Alert.cohort_id == cohort_id,
        Alert.status == "open"
    ).all()
    
    digest = {
        "date": today,
        "cohort_id": cohort_id,
        "today_sessions": [
            {"id": s.id, "title": s.title, "time": s.scheduled_date}
            for s in today_sessions
        ],
        "pending_tasks": len(pending_tasks),
        "open_alerts": len(open_alerts),
        "summary": f"Digest for {today}: {len(today_sessions)} sessions, {len(pending_tasks)} pending tasks, {len(open_alerts)} alerts"
    }
    
    return digest

def send_reminder_email(
    session_name: str,
    recipients: str,
    scheduled_date: datetime = None,
    reminder_type: str = "session"
):
    """Background task to send reminder email"""
    # This would integrate with email service (SendGrid, AWS SES, etc.)
    print(f"[REMINDER EMAIL] {reminder_type.upper()}: {session_name} to {recipients}")
    if scheduled_date:
        print(f"[REMINDER EMAIL] Scheduled Date: {scheduled_date}")
