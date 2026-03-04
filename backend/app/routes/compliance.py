from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.compliance import Exit, ExitType, ExitStatus, ConsequenceManagement, ConsequenceSeverity
from app.models.cohort import Cohort, Trainee
from app.models.user import User
from app.services.ai_service_v2 import generate_document
from typing import List
from datetime import datetime, date

router = APIRouter(prefix="/api/compliance", tags=["compliance"])

# ==================== EXIT MANAGEMENT ====================

@router.post("/exits")
def request_exit(
    cohort_id: int,
    trainee_id: int,
    exit_type: str,
    reason: str = None,
    exit_date: str = None,
    db: Session = Depends(get_db)
):
    """Request trainee exit/resignation/early release"""
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    trainee = db.query(Trainee).filter(Trainee.id == trainee_id).first()
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found")
    
    try:
        exit_record = Exit(
            cohort_id=cohort_id,
            trainee_id=trainee_id,
            exit_type=exit_type,
            reason=reason,
            exit_date=datetime.fromisoformat(exit_date).date() if exit_date else None,
            status=ExitStatus.REQUESTED
        )
        db.add(exit_record)
        db.commit()
        db.refresh(exit_record)
        return {"status": "success", "exit_id": exit_record.id, "message": "Exit request created"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exits")
def list_exits(cohort_id: int = None, status: str = None, exit_type: str = None, db: Session = Depends(get_db)):
    """List exit requests with optional filters"""
    query = db.query(Exit)
    
    if cohort_id:
        query = query.filter(Exit.cohort_id == cohort_id)
    if status:
        query = query.filter(Exit.status == status)
    if exit_type:
        query = query.filter(Exit.exit_type == exit_type)
    
    exits = query.all()
    return {
        "total": len(exits),
        "exits": [
            {
                "id": e.id,
                "trainee_id": e.trainee_id,
                "exit_type": e.exit_type,
                "status": e.status,
                "requested_date": e.requested_date,
                "exit_date": e.exit_date,
                "created_at": e.created_at
            } for e in exits
        ]
    }

@router.get("/exits/{exit_id}")
def get_exit_details(exit_id: int, db: Session = Depends(get_db)):
    """Get exit request details"""
    exit_record = db.query(Exit).filter(Exit.id == exit_id).first()
    if not exit_record:
        raise HTTPException(status_code=404, detail="Exit request not found")
    
    return {
        "id": exit_record.id,
        "trainee_id": exit_record.trainee_id,
        "cohort_id": exit_record.cohort_id,
        "exit_type": exit_record.exit_type,
        "status": exit_record.status,
        "requested_date": exit_record.requested_date,
        "exit_date": exit_record.exit_date,
        "reason": exit_record.reason,
        "final_evaluation": exit_record.final_evaluation,
        "exit_feedback": exit_record.exit_feedback,
        "clearance_status": exit_record.is_clearance_complete,
        "created_at": exit_record.created_at,
        "updated_at": exit_record.updated_at
    }

@router.put("/exits/{exit_id}/approve")
def approve_exit(
    exit_id: int,
    approved_by_id: int,
    approval_notes: str = None,
    final_exit_date: str = None,
    db: Session = Depends(get_db)
):
    """Approve exit request"""
    exit_record = db.query(Exit).filter(Exit.id == exit_id).first()
    if not exit_record:
        raise HTTPException(status_code=404, detail="Exit request not found")
    
    try:
        exit_record.status = ExitStatus.APPROVED
        exit_record.approved_by_id = approved_by_id
        exit_record.approval_date = datetime.utcnow()
        exit_record.approval_notes = approval_notes
        if final_exit_date:
            exit_record.exit_date = datetime.fromisoformat(final_exit_date).date()
        
        exit_record.updated_at = datetime.utcnow()
        db.commit()
        
        # Update trainee status
        trainee = db.query(Trainee).filter(Trainee.id == exit_record.trainee_id).first()
        if trainee:
            trainee.status = "exited"
            trainee.exit_reason = exit_record.exit_type
            db.commit()
        
        return {"status": "success", "message": "Exit approved"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/exits/{exit_id}/reject")
def reject_exit(
    exit_id: int,
    approved_by_id: int,
    rejection_notes: str = None,
    db: Session = Depends(get_db)
):
    """Reject exit request"""
    exit_record = db.query(Exit).filter(Exit.id == exit_id).first()
    if not exit_record:
        raise HTTPException(status_code=404, detail="Exit request not found")
    
    try:
        exit_record.status = ExitStatus.REJECTED
        exit_record.approved_by_id = approved_by_id
        exit_record.approval_date = datetime.utcnow()
        exit_record.approval_notes = rejection_notes
        exit_record.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Exit rejected"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/exits/{exit_id}/clearance")
def update_clearance_status(
    exit_id: int,
    clearance_status: str,
    clearance_notes: str = None,
    db: Session = Depends(get_db)
):
    """Update exit clearance status"""
    exit_record = db.query(Exit).filter(Exit.id == exit_id).first()
    if not exit_record:
        raise HTTPException(status_code=404, detail="Exit request not found")
    
    try:
        exit_record.is_clearance_complete = clearance_status  # pending, in_progress, complete
        exit_record.clearance_notes = clearance_notes
        exit_record.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Clearance status updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/exits/{exit_id}/generate-summary")
def generate_exit_summary(
    exit_id: int,
    db: Session = Depends(get_db)
):
    """Generate exit summary document"""
    exit_record = db.query(Exit).filter(Exit.id == exit_id).first()
    if not exit_record:
        raise HTTPException(status_code=404, detail="Exit request not found")
    
    try:
        trainee = db.query(Trainee).filter(Trainee.id == exit_record.trainee_id).first()
        cohort = db.query(Cohort).filter(Cohort.id == exit_record.cohort_id).first()
        
        summary = f"""
EXIT SUMMARY - {exit_record.exit_type.upper()}

Trainee: {trainee.user.full_name if trainee.user else 'N/A'}
Cohort: {cohort.name if cohort else 'N/A'}
Exit Date: {exit_record.exit_date or 'TBD'}

Exit Reason: {exit_record.reason or 'Not specified'}
Approval Status: {exit_record.status}
Approved By: {exit_record.approved_by.full_name if exit_record.approved_by else 'Pending'}
Approval Notes: {exit_record.approval_notes or 'None'}

Final Evaluation: {exit_record.final_evaluation or 'Pending'}
Exit Feedback: {exit_record.exit_feedback or 'Not collected'}

Clearance Status: {exit_record.is_clearance_complete}
Clearance Notes: {exit_record.clearance_notes or 'N/A'}

Generated: {datetime.utcnow()}
"""
        
        exit_record.summary_document = summary
        db.commit()
        
        return {
            "status": "success",
            "summary": summary,
            "message": "Exit summary generated"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CONSEQUENCE MANAGEMENT ====================

@router.post("/consequences")
def create_consequence(
    cohort_id: int,
    trainee_id: int,
    consequence_type: str,
    severity: str,
    description: str,
    reported_by_id: int,
    incident_date: str = None,
    db: Session = Depends(get_db)
):
    """Record a violation or consequence"""
    trainee = db.query(Trainee).filter(Trainee.id == trainee_id).first()
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found")
    
    try:
        consequence = ConsequenceManagement(
            cohort_id=cohort_id,
            trainee_id=trainee_id,
            consequence_type=consequence_type,
            severity=severity,
            description=description,
            reported_by_id=reported_by_id,
            incident_date=datetime.fromisoformat(incident_date) if incident_date else datetime.utcnow()
        )
        db.add(consequence)
        db.commit()
        db.refresh(consequence)
        return {"status": "success", "consequence_id": consequence.id, "message": "Consequence recorded"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consequences")
def list_consequences(cohort_id: int = None, trainee_id: int = None, severity: str = None, db: Session = Depends(get_db)):
    """List consequences with optional filters"""
    query = db.query(ConsequenceManagement)
    
    if cohort_id:
        query = query.filter(ConsequenceManagement.cohort_id == cohort_id)
    if trainee_id:
        query = query.filter(ConsequenceManagement.trainee_id == trainee_id)
    if severity:
        query = query.filter(ConsequenceManagement.severity == severity)
    
    consequences = query.all()
    return {
        "total": len(consequences),
        "consequences": [
            {
                "id": c.id,
                "trainee_id": c.trainee_id,
                "consequence_type": c.consequence_type,
                "severity": c.severity,
                "incident_date": c.incident_date,
                "status": "open" if not c.remedial_completion_date else "resolved",
                "created_at": c.created_at
            } for c in consequences
        ]
    }

@router.get("/consequences/{consequence_id}")
def get_consequence_details(consequence_id: int, db: Session = Depends(get_db)):
    """Get detailed consequence information"""
    consequence = db.query(ConsequenceManagement).filter(ConsequenceManagement.id == consequence_id).first()
    if not consequence:
        raise HTTPException(status_code=404, detail="Consequence not found")
    
    return {
        "id": consequence.id,
        "trainee_id": consequence.trainee_id,
        "cohort_id": consequence.cohort_id,
        "consequence_type": consequence.consequence_type,
        "severity": consequence.severity,
        "description": consequence.description,
        "incident_date": consequence.incident_date,
        "action_taken": consequence.action_taken,
        "action_date": consequence.action_date,
        "remedial_plan": consequence.remedial_plan,
        "remedial_completion_date": consequence.remedial_completion_date,
        "appeal_raised": consequence.appeal_raised,
        "appeal_decision": consequence.appeal_decision,
        "created_at": consequence.created_at
    }

@router.put("/consequences/{consequence_id}/action")
def record_action_taken(
    consequence_id: int,
    action_taken: str,
    handled_by_id: int,
    db: Session = Depends(get_db)
):
    """Record action taken on consequence"""
    consequence = db.query(ConsequenceManagement).filter(ConsequenceManagement.id == consequence_id).first()
    if not consequence:
        raise HTTPException(status_code=404, detail="Consequence not found")
    
    try:
        consequence.action_taken = action_taken
        consequence.action_date = datetime.utcnow()
        consequence.handled_by_id = handled_by_id
        consequence.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Action recorded"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/consequences/{consequence_id}/remedial")
def update_remedial_plan(
    consequence_id: int,
    remedial_plan: str,
    completion_date: str = None,
    db: Session = Depends(get_db)
):
    """Update remedial plan and track completion"""
    consequence = db.query(ConsequenceManagement).filter(ConsequenceManagement.id == consequence_id).first()
    if not consequence:
        raise HTTPException(status_code=404, detail="Consequence not found")
    
    try:
        consequence.remedial_plan = remedial_plan
        if completion_date:
            consequence.remedial_completion_date = datetime.fromisoformat(completion_date).date()
        consequence.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": "Remedial plan updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/consequences/{consequence_id}/appeal")
def handle_appeal(
    consequence_id: int,
    appeal_notes: str,
    appeal_decision: str,
    db: Session = Depends(get_db)
):
    """Record appeal decision"""
    consequence = db.query(ConsequenceManagement).filter(ConsequenceManagement.id == consequence_id).first()
    if not consequence:
        raise HTTPException(status_code=404, detail="Consequence not found")
    
    try:
        consequence.appeal_notes = appeal_notes
        consequence.appeal_decision = appeal_decision
        consequence.updated_at = datetime.utcnow()
        db.commit()
        return {"status": "success", "message": f"Appeal {appeal_decision}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/consequences/{consequence_id}/generate-summary")
def generate_consequence_summary(
    consequence_id: int,
    db: Session = Depends(get_db)
):
    """Generate consequence management summary document"""
    consequence = db.query(ConsequenceManagement).filter(ConsequenceManagement.id == consequence_id).first()
    if not consequence:
        raise HTTPException(status_code=404, detail="Consequence not found")
    
    try:
        trainee = db.query(Trainee).filter(Trainee.id == consequence.trainee_id).first()
        
        summary = f"""
CONSEQUENCE MANAGEMENT SUMMARY

Trainee: {trainee.user.full_name if trainee.user else 'N/A'}
Cohort: {consequence.cohort.name if consequence.cohort else 'N/A'}

Incident Type: {consequence.consequence_type}
Severity: {consequence.severity}
Incident Date: {consequence.incident_date}

Description: {consequence.description}

Action Taken: {consequence.action_taken or 'Pending'}
Action Date: {consequence.action_date or 'N/A'}
Handled By: {consequence.handled_by.full_name if consequence.handled_by else 'Unassigned'}

Remedial Plan: {consequence.remedial_plan or 'Not specified'}
Completion Target: {consequence.remedial_completion_date or 'Not set'}

Appeal Status: {consequence.appeal_raised}
Appeal Decision: {consequence.appeal_decision or 'Pending'}
Appeal Notes: {consequence.appeal_notes or 'N/A'}

Generated: {datetime.utcnow()}
Status: {'Resolved' if consequence.remedial_completion_date else 'Open'}
"""
        
        consequence.summary_document = summary
        db.commit()
        
        return {
            "status": "success",
            "summary": summary,
            "message": "Consequence summary generated"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cohort/{cohort_id}/compliance-report")
def get_cohort_compliance_report(cohort_id: int, db: Session = Depends(get_db)):
    """Get compliance report for cohort"""
    exits = db.query(Exit).filter(Exit.cohort_id == cohort_id).all()
    consequences = db.query(ConsequenceManagement).filter(ConsequenceManagement.cohort_id == cohort_id).all()
    
    exit_types = {}
    for e in exits:
        exit_type = str(e.exit_type)
        exit_types[exit_type] = exit_types.get(exit_type, 0) + 1
    
    severity_dist = {}
    for c in consequences:
        severity = str(c.severity)
        severity_dist[severity] = severity_dist.get(severity, 0) + 1
    
    return {
        "cohort_id": cohort_id,
        "total_exits": len(exits),
        "exit_distribution": exit_types,
        "total_consequences": len(consequences),
        "consequence_severity": severity_dist,
        "pending_appeals": len([c for c in consequences if c.appeal_raised == "pending"]),
        "unresolved_consequences": len([c for c in consequences if not c.remedial_completion_date])
    }
