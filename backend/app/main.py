from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import auth, sessions, progress, chat, cohorts, evaluations, documents, progress_tracking, reminders, mentoring, support, compliance
import logging

logger = logging.getLogger(__name__)

# Create tables with error handling
if engine:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.warning(f"Could not create database tables: {e}")
        logger.info("This is OK - tables may already exist or database connection needs to be configured")
else:
    logger.warning("Database engine not initialized - some endpoints may not work until database is configured")

app = FastAPI(
    title="AI Coach - Cohort Management & Training Support",
    description="AI-powered assistant for managing training cohorts, sessions, progress tracking, document automation, and operational support",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(cohorts.router)
app.include_router(sessions.router)
app.include_router(progress_tracking.router)
app.include_router(evaluations.router)
app.include_router(documents.router)
app.include_router(reminders.router)
app.include_router(progress.router)
app.include_router(chat.router)
app.include_router(mentoring.router)
app.include_router(support.router)
app.include_router(compliance.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Coach API - Cohort Management & Training Support",
        "version": "2.0.0",
        "docs": "/docs",
        "features": [
            "Session & Communication Management",
            "Cohort Tracking & Performance Support",
            "Operational & Administrative Assistance",
            "Document Automation",
            "MoM Generation",
            "Progress Tracking",
            "Evaluations & Feedback",
            "Reminders & Notifications"
        ]
    }

@app.get("/health")
def health_check():
    db_status = "connected" if engine else "not configured"
    return {
        "status": "healthy",
        "database": db_status
    }
