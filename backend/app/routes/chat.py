from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ChatMessageCreate, ChatMessageResponse
from app.database import get_db
from app.services.ai_service_v2 import AIService

router = APIRouter(prefix="/chat", tags=["chat"])

# instantiate service (could be singleton)
ai_service = AIService()

@router.post("/message", response_model=ChatMessageResponse)
def send_message(
    chat_message: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """Accept user chat and return AI coach response.

    This endpoint is intentionally simple. It doesn't store messages in the
    database, but the parameter `db` is included in case future enhancements
    want persistence or user context.
    """
    # generate a reply using the AIService chat helper
    try:
        from app.services.ai_service_v2 import chat as ai_chat
        reply = ai_chat(chat_message.message)
    except Exception:
        reply = f"I'm here to help! You said: {chat_message.message}"

    return ChatMessageResponse(
        message=chat_message.message,
        message_type=chat_message.message_type,
        response=reply
    )
