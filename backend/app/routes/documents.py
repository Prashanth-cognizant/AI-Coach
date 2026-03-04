from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.documents import CohortDocument, DocumentTemplate, Alert, Task
from app.services.ai_service_v2 import generate_document
from typing import List

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/generate")
def generate_document_route(
    cohort_id: int,
    doc_type: str,
    variables: dict,
    db: Session = Depends(get_db)
):
    """Generate a document from template"""
    content = generate_document(doc_type, variables)
    
    document = CohortDocument(
        cohort_id=cohort_id,
        document_type=doc_type,
        title=variables.get("title", f"{doc_type} - Auto-generated"),
        content=content,
        status="generated"
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

@router.post("/send")
def send_document(
    document_id: int,
    recipients: str,
    db: Session = Depends(get_db)
):
    """Send generated document to recipients"""
    from datetime import datetime
    
    document = db.query(CohortDocument).filter(CohortDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    document.recipients = recipients
    document.sent = True
    document.sent_at = datetime.utcnow()
    document.status = "sent"
    
    db.commit()
    db.refresh(document)
    return {"message": f"Document sent to {recipients}"}

@router.get("/cohort/{cohort_id}")
def get_cohort_documents(cohort_id: int, db: Session = Depends(get_db)):
    """Get all documents for a cohort"""
    documents = db.query(CohortDocument).filter(CohortDocument.cohort_id == cohort_id).all()
    return documents

@router.get("/templates/")
def list_templates(db: Session = Depends(get_db)):
    """List all document templates"""
    templates = db.query(DocumentTemplate).all()
    return templates

@router.post("/templates/")
def create_template(
    template_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new document template"""
    template = DocumentTemplate(
        name=template_data.get("name"),
        template_type=template_data.get("template_type"),
        content=template_data.get("content"),
        required_variables=template_data.get("required_variables")
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

@router.post("/alerts/")
def create_alert(
    alert_data: dict,
    db: Session = Depends(get_db)
):
    """Create an alert"""
    alert = Alert(
        cohort_id=alert_data.get("cohort_id"),
        trainee_id=alert_data.get("trainee_id"),
        alert_type=alert_data.get("alert_type"),
        severity=alert_data.get("severity", "medium"),
        title=alert_data.get("title"),
        description=alert_data.get("description"),
        assigned_to=alert_data.get("assigned_to")
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.get("/alerts/cohort/{cohort_id}")
def get_cohort_alerts(cohort_id: int, db: Session = Depends(get_db)):
    """Get all alerts for a cohort"""
    alerts = db.query(Alert).filter(Alert.cohort_id == cohort_id).all()
    return alerts

@router.put("/alerts/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    resolution: dict,
    db: Session = Depends(get_db)
):
    """Resolve an alert"""
    from datetime import datetime
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = "resolved"
    alert.resolved_at = datetime.utcnow()
    alert.resolution_notes = resolution.get("notes")
    
    db.commit()
    db.refresh(alert)
    return alert

@router.post("/tasks/")
def create_task(
    cohort_id: int,
    task_data: dict,
    db: Session = Depends(get_db)
):
    """Create a task for cohort management"""
    from datetime import datetime
    
    task = Task(
        cohort_id=cohort_id,
        title=task_data.get("title"),
        description=task_data.get("description"),
        task_type=task_data.get("task_type"),
        assigned_to=task_data.get("assigned_to"),
        due_date=datetime.fromisoformat(task_data.get("due_date")),
        priority=task_data.get("priority", "medium")
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/tasks/cohort/{cohort_id}")
def get_cohort_tasks(
    cohort_id: int,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get tasks for a cohort"""
    query = db.query(Task).filter(Task.cohort_id == cohort_id)
    if status:
        query = query.filter(Task.status == status)
    return query.all()

@router.put("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """Mark task as completed"""
    from datetime import datetime
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(task)
    return task
