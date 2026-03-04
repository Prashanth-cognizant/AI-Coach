from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str
    age: Optional[int] = None
    gender: Optional[str] = None
    fitness_goal: Optional[str] = None
    current_weight: Optional[float] = None
    target_weight: Optional[float] = None
    height: Optional[float] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    fitness_goal: Optional[str] = None
    current_weight: Optional[float] = None
    target_weight: Optional[float] = None
    height: Optional[float] = None

class UserResponse(UserBase):
    id: int
    fitness_goal: Optional[str]
    current_weight: Optional[float]
    target_weight: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    session_type: str
    duration_minutes: int
    exercises_completed: int
    calories_burned: float
    mood_before: Optional[str] = None
    mood_after: Optional[str] = None
    notes: Optional[str] = None
    difficulty_level: str = "medium"

class SessionResponse(SessionCreate):
    id: int
    user_id: int
    ai_recommendation: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ProgressCreate(BaseModel):
    weight: Optional[float] = None
    body_measurements: Optional[str] = None
    workout_streak: int = 0
    total_workouts: int = 0
    total_calories_burned: float = 0
    mood_score: Optional[int] = None
    energy_level: Optional[int] = None
    sleep_hours: Optional[float] = None
    water_intake_liters: Optional[float] = None

class ProgressResponse(ProgressCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    message: str
    message_type: str = "query"

class ChatMessageResponse(ChatMessageCreate):
    id: int
    user_id: int
    response: str
    created_at: datetime

    class Config:
        from_attributes = True

class CohortBase(BaseModel):
    name: str
    description: Optional[str] = None
    batch_code: str
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None

class CohortCreate(CohortBase):
    pass

class CohortUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    batch_code: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[str] = None

class TraineeCreate(BaseModel):
    user_id: int
    employee_id: str

class TraineeResponse(TraineeCreate):
    id: int
    cohort_id: int
    status: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
