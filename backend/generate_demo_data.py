"""
Demo data generator for AI Coach application
Run this after starting the backend to populate with sample data
"""

import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8000/api"

# Sample users
SAMPLE_USERS = [
    {
        "username": "alex_fitness",
        "email": "alex@example.com",
        "password": "password123",
        "full_name": "Alex Johnson",
        "age": 28,
        "gender": "male",
        "fitness_goal": "Muscle Gain",
        "current_weight": 75.5,
        "target_weight": 82.0,
        "height": 180
    },
    {
        "username": "sarah_healthy",
        "email": "sarah@example.com",
        "password": "password123",
        "full_name": "Sarah Williams",
        "age": 25,
        "gender": "female",
        "fitness_goal": "Weight Loss",
        "current_weight": 68.0,
        "target_weight": 60.0,
        "height": 165
    }
]

# Sample sessions
SAMPLE_SESSIONS = [
    {
        "session_type": "workout",
        "duration_minutes": 45,
        "exercises_completed": 8,
        "calories_burned": 350,
        "mood_before": "neutral",
        "mood_after": "very_good",
        "difficulty_level": "hard",
        "notes": "Great workout! Felt energized throughout"
    },
    {
        "session_type": "nutrition",
        "duration_minutes": 30,
        "exercises_completed": 0,
        "calories_burned": 0,
        "mood_before": "good",
        "mood_after": "very_good",
        "difficulty_level": "medium",
        "notes": "Meal planning session"
    },
    {
        "session_type": "mental_health",
        "duration_minutes": 20,
        "exercises_completed": 0,
        "calories_burned": 0,
        "mood_before": "bad",
        "mood_after": "good",
        "difficulty_level": "easy",
        "notes": "Meditation and breathing exercises"
    }
]

# Sample progress logs
SAMPLE_PROGRESS = [
    {
        "weight": 75.2,
        "mood_score": 8,
        "energy_level": 8,
        "sleep_hours": 7.5,
        "water_intake_liters": 3.0,
        "total_workouts": 1,
        "workout_streak": 1,
        "total_calories_burned": 350
    },
    {
        "weight": 74.8,
        "mood_score": 8,
        "energy_level": 9,
        "sleep_hours": 8.0,
        "water_intake_liters": 3.5,
        "total_workouts": 2,
        "workout_streak": 2,
        "total_calories_burned": 700
    }
]

# Sample chat messages
SAMPLE_MESSAGES = [
    "How can I improve my workout routine?",
    "What should I eat after my exercise?",
    "How many calories should I consume daily?",
    "I'm feeling tired, any advice?",
    "What's the best time to exercise?",
]

def register_user(user_data):
    """Register a new user"""
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 200:
            print(f"✓ Registered user: {user_data['username']}")
            return response.json()
        else:
            print(f"✗ Failed to register {user_data['username']}: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error registering user: {e}")
        return None

def login_user(username, password):
    """Login user and get token"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Logged in: {username}")
            return data['access_token'], data['user_id']
        else:
            print(f"✗ Failed to login: {response.text}")
            return None, None
    except Exception as e:
        print(f"✗ Error logging in: {e}")
        return None, None

def create_session(token, session_data):
    """Create a coaching session"""
    try:
        response = requests.post(
            f"{BASE_URL}/sessions/",
            json=session_data,
            params={"token": token}
        )
        if response.status_code == 200:
            print(f"✓ Created session: {session_data['session_type']}")
            return response.json()
        else:
            print(f"✗ Failed to create session: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error creating session: {e}")
        return None

def log_progress(token, progress_data):
    """Log progress"""
    try:
        response = requests.post(
            f"{BASE_URL}/progress/",
            json=progress_data,
            params={"token": token}
        )
        if response.status_code == 200:
            print(f"✓ Logged progress: weight={progress_data['weight']}kg")
            return response.json()
        else:
            print(f"✗ Failed to log progress: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error logging progress: {e}")
        return None

def send_message(token, message_text):
    """Send chat message"""
    try:
        response = requests.post(
            f"{BASE_URL}/chat/message",
            json={"message": message_text, "message_type": "query"},
            params={"token": token}
        )
        if response.status_code == 200:
            print(f"✓ Sent message: {message_text[:30]}...")
            return response.json()
        else:
            print(f"✗ Failed to send message: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error sending message: {e}")
        return None

def main():
    """Generate demo data"""
    print("\n" + "="*50)
    print("🚀 AI Coach Demo Data Generator")
    print("="*50 + "\n")

    # Register users
    print("📝 Registering users...")
    tokens = {}
    for user in SAMPLE_USERS:
        register_user(user)
        token, user_id = login_user(user['username'], user['password'])
        if token:
            tokens[user['username']] = (token, user_id)
    
    print("\n")
    
    # Create sessions and progress logs
    for username, (token, user_id) in tokens.items():
        print(f"📊 Creating data for {username}...")
        
        # Create sessions
        for i, session in enumerate(SAMPLE_SESSIONS):
            create_session(token, session)
        
        # Log progress
        for progress in SAMPLE_PROGRESS:
            log_progress(token, progress)
        
        # Send chat messages
        for msg in SAMPLE_MESSAGES:
            send_message(token, msg)
        
        print()
    
    print("="*50)
    print("✅ Demo data generation complete!")
    print("="*50)
    print("\n🎯 You can now:")
    print("   1. Login with any user from the demo")
    print("   2. View charts with real data")
    print("   3. See multiple sessions and progress logs")
    print("   4. Test the AI chat functionality")
    print("\n")

if __name__ == "__main__":
    main()
