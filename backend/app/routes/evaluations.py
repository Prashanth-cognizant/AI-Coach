from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.evaluation import Evaluation, EvaluationScore, L1Feedback
from typing import List

router = APIRouter(prefix="/evaluations", tags=["evaluations"])

@router.post("/")
def create_evaluation(
    cohort_id: int,
    eval_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new evaluation"""
    from datetime import datetime
    
    evaluation = Evaluation(
        cohort_id=cohort_id,
        name=eval_data.get("name"),
        evaluation_type=eval_data.get("evaluation_type"),
        scheduled_date=datetime.fromisoformat(eval_data.get("scheduled_date")),
        guidelines=eval_data.get("guidelines"),
        rubric=eval_data.get("rubric")
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation

@router.get("/{evaluation_id}")
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    """Get evaluation details"""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

@router.post("/{evaluation_id}/score")
def submit_evaluation_score(
    evaluation_id: int,
    score_data: dict,
    db: Session = Depends(get_db)
):
    """Submit evaluation score for a trainee"""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    score = EvaluationScore(
        evaluation_id=evaluation_id,
        trainee_id=score_data.get("trainee_id"),
        score=score_data.get("score"),
        grade=score_data.get("grade"),
        feedback=score_data.get("feedback"),
        passed=score_data.get("score", 0) >= 40,  # Assuming 40% is passing
        requires_remedial=score_data.get("score", 0) < 60,
        evaluated_by=score_data.get("evaluated_by")
    )
    from datetime import datetime
    score.evaluated_at = datetime.utcnow()
    
    db.add(score)
    db.commit()
    db.refresh(score)
    return score

@router.get("/cohort/{cohort_id}/scores")
def get_cohort_evaluation_scores(cohort_id: int, db: Session = Depends(get_db)):
    """Get all evaluation scores for a cohort"""
    evaluations = db.query(Evaluation).filter(Evaluation.cohort_id == cohort_id).all()
    scores = []
    for eval in evaluations:
        eval_scores = db.query(EvaluationScore).filter(EvaluationScore.evaluation_id == eval.id).all()
        scores.extend(eval_scores)
    return scores

@router.post("/{evaluation_id}/mark-complete")
def mark_evaluation_complete(evaluation_id: int, db: Session = Depends(get_db)):
    """Mark evaluation as complete"""
    from datetime import datetime
    
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation.status = "completed"
    evaluation.actual_date = datetime.utcnow()
    
    db.commit()
    db.refresh(evaluation)
    return evaluation

@router.post("/l1-feedback/")
def submit_l1_feedback(
    feedback_data: dict,
    db: Session = Depends(get_db)
):
    """Submit L1 feedback for a session"""
    feedback = L1Feedback(
        trainee_id=feedback_data.get("trainee_id"),
        session_id=feedback_data.get("session_id"),
        content_quality=feedback_data.get("content_quality"),
        facilitator_effectiveness=feedback_data.get("facilitator_effectiveness"),
        relevance=feedback_data.get("relevance"),
        pacing=feedback_data.get("pacing"),
        strengths=feedback_data.get("strengths"),
        improvements=feedback_data.get("improvements"),
        additional_comments=feedback_data.get("additional_comments")
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    # Mark l1_feedback_submitted on trainee
    from app.models.cohort import Trainee
    trainee = db.query(Trainee).filter(Trainee.id == feedback_data.get("trainee_id")).first()
    if trainee:
        trainee.l1_feedback_submitted = True
        db.commit()
    
    return feedback

@router.get("/l1-feedback/session/{session_id}")
def get_l1_feedback_for_session(session_id: int, db: Session = Depends(get_db)):
    """Get all L1 feedback for a session"""
    feedback_list = db.query(L1Feedback).filter(L1Feedback.session_id == session_id).all()
    
    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback found")
    
    # Calculate averages
    avg_content = sum(f.content_quality for f in feedback_list if f.content_quality) / len([f for f in feedback_list if f.content_quality]) if feedback_list else 0
    avg_facilitator = sum(f.facilitator_effectiveness for f in feedback_list if f.facilitator_effectiveness) / len([f for f in feedback_list if f.facilitator_effectiveness]) if feedback_list else 0
    
    return {
        "session_id": session_id,
        "total_responses": len(feedback_list),
        "average_content_quality": avg_content,
        "average_facilitator_effectiveness": avg_facilitator,
        "feedback_list": feedback_list
    }
