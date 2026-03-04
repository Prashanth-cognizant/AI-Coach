# AI Coach Backend - Quick Start Guide

## Installation

### 1. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```sql
-- Create database
CREATE DATABASE ai_coach;
```

### 4. Run Server
```bash
python main.py
```

Server runs on: http://localhost:8000

### 5. View API Documentation
Open in browser: http://localhost:8000/docs

## Environment Variables (Optional)

Create `.env` file in backend folder:
```
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/ai_coach
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Quick Test

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "age": 25,
    "fitness_goal": "Weight Loss"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

## Database Models

### Users Table
- id, username, email, hashed_password
- full_name, age, gender
- fitness_goal, current_weight, target_weight, height
- is_active, created_at, updated_at

### Coaching Sessions
- id, user_id, session_type
- duration_minutes, exercises_completed, calories_burned
- mood_before, mood_after, notes
- ai_recommendation, difficulty_level
- created_at, updated_at

### Progress Logs
- id, user_id, weight
- body_measurements, workout_streak, total_workouts
- total_calories_burned, mood_score, energy_level
- sleep_hours, water_intake_liters
- created_at

### Chat Messages
- id, user_id, message, response
- message_type, created_at
