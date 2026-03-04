from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.support import Issue, Query, IssueStatus, IssuePriority, IssueCategory
from app.models.cohort import Cohort, Trainee
from app.models.user import User
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api/support", tags=["support"])

# ==================== ISSUE MANAGEMENT ====================

@router.post("/issues")
def create_issue(
    cohort_id: int,
    title: str,
    description: str,
    category: str,
    priority: str,
    trainee_id: int = None,
    reported_by_id: int = None,
    db: Session = Depends(get_db)
):
    """Create a new IT issue/ticket"""
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    try:
        issue = Issue(
            cohort_id=cohort_id,
            trainee_id=trainee_id,
            reported_by_id=reported_by_id or 1,
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=IssueStatus.OPEN
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return {"status": "success", "issue_id": issue.id, "message": "Issue created"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/issues")
def list_issues(cohort_id: int = None, status: str = None, priority: str = None, db: Session = Depends(get_db)):
    """List all issues with optional filters"""
    query = db.query(Issue)
    
    if cohort_id:
        query = query.filter(Issue.cohort_id == cohort_id)
    if status:
        query = query.filter(Issue.status == status)
    if priority:
        query = query.filter(Issue.priority == priority)
    
    issues = query.all()
    return {
        "total": len(issues),
        "issues": [
            {
                "id": i.id,
                "title": i.title,
                "category": i.category,
                "priority": i.priority,
                "status": i.status,
                "trainee_id": i.trainee_id,
                "created_at": i.created_at
            } for i in issues
        ]
    }

@router.get("/issues/{issue_id}")
def get_issue_details(issue_id: int, db: Session = Depends(get_db)):
    """Get detailed issue information"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    return {
        "id": issue.id,
        "title": issue.title,
        "description": issue.description,
        "category": issue.category,
        "priority": issue.priority,
        "status": issue.status,
        "trainee_id": issue.trainee_id,
        "reported_by_id": issue.reported_by_id,
        "assigned_to_id": issue.assigned_to_id,
        "resolution_notes": issue.resolution_notes,
        "resolved_date": issue.resolved_date,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at
    }

@router.put("/issues/{issue_id}/assign")
def assign_issue(
    issue_id: int,
    assigned_to_id: int,
    db: Session = Depends(get_db)
):
    """Assign issue to a staff member"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    try:
        issue.assigned_to_id = assigned_to_id
        issue.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Issue assigned"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/issues/{issue_id}/status")
def update_issue_status(
    issue_id: int,
    new_status: str,
    resolution_notes: str = None,
    db: Session = Depends(get_db)
):
    """Update issue status and mark as resolved if needed"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    try:
        issue.status = new_status
        if resolution_notes:
            issue.resolution_notes = resolution_notes
        if new_status == IssueStatus.RESOLVED or new_status == "resolved":
            issue.resolved_date = datetime.utcnow()
        
        issue.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": f"Issue status updated to {new_status}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/issues/cohort/{cohort_id}/summary")
def get_cohort_issue_summary(cohort_id: int, db: Session = Depends(get_db)):
    """Get issue summary for a cohort"""
    issues = db.query(Issue).filter(Issue.cohort_id == cohort_id).all()
    
    by_status = {}
    by_priority = {}
    by_category = {}
    
    for issue in issues:
        status = str(issue.status)
        priority = str(issue.priority)
        category = str(issue.category)
        
        by_status[status] = by_status.get(status, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
        by_category[category] = by_category.get(category, 0) + 1
    
    return {
        "cohort_id": cohort_id,
        "total_issues": len(issues),
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "critical_issues": len([i for i in issues if str(i.priority) == "critical"])
    }

# ==================== QUERY MANAGEMENT ====================

@router.post("/queries")
def create_query(
    cohort_id: int,
    trainee_id: int,
    subject: str,
    description: str,
    category: str = "general",
    raised_by_id: int = None,
    db: Session = Depends(get_db)
):
    """Create a new support query/ticket"""
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    trainee = db.query(Trainee).filter(Trainee.id == trainee_id).first()
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found")
    
    try:
        query = Query(
            cohort_id=cohort_id,
            trainee_id=trainee_id,
            raised_by_id=raised_by_id or trainee_id,
            subject=subject,
            description=description,
            category=category,
            status="open"
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return {"status": "success", "query_id": query.id, "message": "Query created"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queries")
def list_queries(cohort_id: int = None, trainee_id: int = None, status: str = None, db: Session = Depends(get_db)):
    """List queries with optional filters"""
    query = db.query(Query)
    
    if cohort_id:
        query = query.filter(Query.cohort_id == cohort_id)
    if trainee_id:
        query = query.filter(Query.trainee_id == trainee_id)
    if status:
        query = query.filter(Query.status == status)
    
    queries = query.all()
    return {
        "total": len(queries),
        "queries": [
            {
                "id": q.id,
                "subject": q.subject,
                "category": q.category,
                "status": q.status,
                "trainee_id": q.trainee_id,
                "assigned_to_id": q.assigned_to_id,
                "created_at": q.created_at
            } for q in queries
        ]
    }

@router.get("/queries/{query_id}")
def get_query_details(query_id: int, db: Session = Depends(get_db)):
    """Get detailed query information"""
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    return {
        "id": query.id,
        "subject": query.subject,
        "description": query.description,
        "category": query.category,
        "status": query.status,
        "trainee_id": query.trainee_id,
        "assigned_to_id": query.assigned_to_id,
        "resolution": query.resolution,
        "resolved_date": query.resolved_date,
        "created_at": query.created_at,
        "updated_at": query.updated_at
    }

@router.put("/queries/{query_id}/assign")
def assign_query(
    query_id: int,
    assigned_to_id: int,
    db: Session = Depends(get_db)
):
    """Assign query to a support staff"""
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    try:
        query.assigned_to_id = assigned_to_id
        query.status = "assigned"
        query.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Query assigned"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/queries/{query_id}/resolve")
def resolve_query(
    query_id: int,
    resolution: str,
    db: Session = Depends(get_db)
):
    """Resolve and close a query"""
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    try:
        query.status = "resolved"
        query.resolution = resolution
        query.resolved_date = datetime.utcnow()
        query.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Query resolved"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queries/trainee/{trainee_id}/summary")
def get_trainee_query_summary(trainee_id: int, db: Session = Depends(get_db)):
    """Get query summary for a trainee"""
    queries = db.query(Query).filter(Query.trainee_id == trainee_id).all()
    
    open_count = len([q for q in queries if q.status == "open"])
    assigned_count = len([q for q in queries if q.status == "assigned"])
    resolved_count = len([q for q in queries if q.status == "resolved"])
    
    return {
        "trainee_id": trainee_id,
        "total_queries": len(queries),
        "open": open_count,
        "assigned": assigned_count,
        "resolved": resolved_count,
        "average_resolution_time": "TBD"
    }
