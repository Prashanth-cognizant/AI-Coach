# AI Coach - Cohort Management & Training Support System

## 🎯 Overview

AI Coach is an intelligent assistant designed to help manage training cohort operations, track training activities, send reminders, automate documentation, and streamline communication between trainees, trainers, mentors, and managers.

**Version:** 2.0.0

## 📋 Key Features

### 1. **Session & Communication Management**
- Schedule and manage coaching sessions (Platform walkthrough, Solutions team, BU Leader connects, etc.)
- Auto-generate Minutes of Meeting (MoM) after sessions
- Send session reminders to participants
- Track session attendance and feedback

### 2. **Cohort Tracking & Performance Support**
- Monitor trainee progress (attendance, self-learning, hands-on completion)
- Track L1 feedback submissions
- Monitor evaluation schedules and scores
- Track asset allocation and software installation status
- Track buddy mentor utilization
- Generate weekly cohort performance summaries with AI insights

### 3. **Evaluation & Assessment Management**
- Create and manage interim, final, and remedial evaluations
- Track evaluation scores and grades
- Identify trainees requiring remedial sessions
- Collect and analyze L1 feedback

### 4. **Document Automation**
- Auto-generate welcome mails
- Create performance warning communications
- Generate graduation checklists
- Send feedback reminders
- Create status trackers and reports
- Customizable document templates

### 5. **Operational Support**
- Create alerts for delays, risks, and action items
- Manage tasks and track completion
- Escalation notifications
- Generate cohort performance insights

## 🏗️ Architecture

### Backend Stack
- **Framework:** FastAPI (Python)
- **Database:** MySQL/SQLite
- **ORM:** SQLAlchemy
- **AI/LLM:** OpenAI GPT-3.5 (optional, with mock fallback)

### Frontend Stack
- **Framework:** React
- **Styling:** CSS3
- **API Client:** Fetch API

## 📂 Project Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── cohort.py        # Cohort and Trainee models
│   │   ├── session.py       # Session and MoM models
│   │   ├── progress.py      # Progress and Attendance models
│   │   ├── evaluation.py    # Evaluation and Feedback models
│   │   ├── documents.py     # Documents, Templates, Alerts, Tasks
│   │   └── user.py
│   ├── routes/
│   │   ├── cohorts.py       # Cohort management APIs
│   │   ├── sessions.py      # Session and MoM APIs
│   │   ├── progress_tracking.py  # Progress APIs
│   │   ├── evaluations.py   # Evaluation APIs
│   │   ├── documents.py     # Document and Alert APIs
│   │   ├── auth.py
│   │   └── chat.py
│   ├── services/
│   │   ├── ai_service_v2.py # MoM generation, summaries, document generation
│   │   └── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── database.py          # Database configuration
│   ├── config.py
│   └── schemas.py

frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard_v2.js     # Cohort overview & metrics
│   │   ├── CoachSessions.js    # Session management
│   │   ├── Chat.js
│   │   ├── Login.js
│   │   └── Profile.js
│   ├── services/
│   │   └── api.js
│   ├── styles/
│   │   ├── Dashboard_v2.css
│   │   ├── Sessions_v2.css
│   │   └── ...
│   └── App.js
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 5.7+ or SQLite

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and OpenAI API key (optional)

# Initialize database
python main.py  # First run creates tables

# Run server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure API URL
cp .env.example .env
# Adjust REACT_APP_API_URL if needed

# Start development server
npm start
```

The application will be available at `http://localhost:3000`

## 📚 API Documentation

### Cohort Management
- `GET /cohorts/` - List all cohorts
- `POST /cohorts/` - Create new cohort
- `GET /cohorts/{cohort_id}` - Get cohort details
- `GET /cohorts/{cohort_id}/dashboard` - Get cohort overview
- `GET /cohorts/{cohort_id}/trainees` - Get trainees in cohort
- `POST /cohorts/{cohort_id}/trainees` - Add trainee to cohort

### Session Management
- `POST /sessions/` - Create session
- `GET /sessions/{session_id}` - Get session details
- `POST /sessions/{session_id}/attendees` - Add attendee
- `POST /sessions/{session_id}/mark-complete` - Complete session & generate MoM
- `GET /sessions/{session_id}/mom` - Get generated MoM
- `GET /sessions/cohort/{cohort_id}/schedule` - Get cohort schedule

### Progress Tracking
- `GET /progress/trainee/{trainee_id}` - Get trainee progress
- `POST /progress/trainee/{trainee_id}/update` - Update progress
- `GET /progress/cohort/{cohort_id}/weekly-summary` - Get weekly summary
- `GET /progress/attendance/trainee/{trainee_id}` - Get attendance records
- `POST /progress/attendance/{trainee_id}/mark` - Mark attendance

### Evaluations
- `POST /evaluations/` - Create evaluation
- `GET /evaluations/{evaluation_id}` - Get evaluation details
- `POST /evaluations/{evaluation_id}/score` - Submit evaluation score
- `POST /evaluations/l1-feedback/` - Submit L1 feedback
- `GET /evaluations/l1-feedback/session/{session_id}` - Get session feedback

### Documents & Alerts
- `POST /documents/generate` - Generate document from template
- `POST /documents/send` - Send document
- `GET /documents/cohort/{cohort_id}` - Get cohort documents
- `GET /documents/templates/` - List all templates
- `POST /documents/alerts/` - Create alert
- `GET /documents/alerts/cohort/{cohort_id}` - Get cohort alerts
- `POST /documents/tasks/` - Create task
- `GET /documents/tasks/cohort/{cohort_id}` - Get cohort tasks

## 🧠 AI Features

### MoM Generation
Automatically generates comprehensive Minutes of Meeting from session details:
```python
session_data = {
    "title": "Platform Walkthrough",
    "date": "2024-03-01",
    "facilitator": "John Trainer",
    "attendees": "Team A, Team B",
    "discussion_points": "...content..."
}

mom = generate_mom(session_data)
# Returns: summary, key_decisions, action_items, risks_identified
```

### Cohort Performance Summary
AI-powered weekly summaries with recommendations:
```python
cohort_data = {
    "cohort_name": "Batch 2024-Q1",
    "total_trainees": 50,
    "avg_attendance": 92,
    "self_learning_progress": 75,
    "hands_on_completion": 60
}

summary = summarize_cohort_progress(cohort_data)
```

### Document Generation
Auto-generate professional documents:
```python
# Welcome mail
welcome = generate_document("welcome_mail", {
    "cohort_name": "Batch 2024-Q1",
    "trainee_name": "John Doe",
    "start_date": "2024-03-01"
})

# Warning mail
warning = generate_document("warning_mail", {
    "trainee_name": "Jane Smith",
    "issue_1": "Low attendance",
    "due_date": "2024-03-15"
})
```

## 📊 Data Models

### Core Entities
- **Cohort** - Training batch/group
- **Trainee** - Individual learner
- **Session** - Training session
- **MoM** - Minutes of Meeting
- **Evaluation** - Assessment event
- **EvaluationScore** - Trainee evaluation results
- **Progress** - Learning progress tracking
- **Attendance** - Session attendance
- **CohortDocument** - Generated documents
- **Alert** - System alerts and notifications
- **Task** - Operational tasks

## 🔐 Security

- JWT-based authentication for API endpoints
- Password hashing with bcrypt
- CORS configuration for frontend-backend communication
- Environment-based configuration for sensitive data

## 📝 Environment Variables

```env
# Database
DATABASE_URL=mysql://user:password@localhost/ai_coach
# or
DATABASE_URL=sqlite:///./ai_coach.db

# OpenAI (optional)
OPENAI_API_KEY=sk-...

# JWT
SECRET_KEY=your-secret-key-here

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

## 🧪 Testing

Run tests for backend:
```bash
cd backend
pytest tests/
```

## 📖 Usage Examples

### Create a Cohort
```bash
curl -X POST http://localhost:8000/cohorts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Batch 2024-Q1",
    "batch_code": "B2024Q1",
    "start_date": "2024-03-01T09:00:00",
    "end_date": "2024-05-31T17:00:00",
    "location": "Mumbai"
  }'
```

### Schedule a Session
```bash
curl -X POST http://localhost:8000/sessions/ \
  -H "Content-Type: application/json" \
  -d '{
    "cohort_id": 1,
    "title": "Platform Walkthrough",
    "session_type": "platform_walkthrough",
    "scheduled_date": "2024-03-05T10:00:00",
    "facilitator_id": 2,
    "location": "Room 101"
  }'
```

### Generate MoM
```bash
curl -X POST http://localhost:8000/sessions/1/mark-complete \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": "team@company.com",
    "discussion_points": "Covered platform features 1-5..."
  }'
```

## 🛠️ Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Ensure MySQL server is running
- Check user permissions

### OpenAI API Issues
- Verify OPENAI_API_KEY is set
- Check API rate limits
- The system falls back to mock responses if API fails

### Frontend API Connection
- Ensure backend is running on port 8000
- Check REACT_APP_API_URL is correct
- Verify CORS is enabled

## 📞 Support

For issues and questions:
1. Check the [troubleshooting guide](TROUBLESHOOTING.md)
2. Review [API documentation](/docs)
3. Check logs for error details

## 📄 License

This project is provided as-is for training and educational purposes.

## 🎓 Learning Path

1. **Setup & Configuration** - Get the project running
2. **Cohort Management** - Create and manage cohorts
3. **Session Scheduling** - Plan and track sessions
4. **Progress Monitoring** - Track trainee performance
5. **Evaluations** - Create and manage assessments
6. **Document Automation** - Auto-generate communications
7. **Advanced Features** - Custom workflows and integrations

## 📈 Future Enhancements

- Email integration for sending MoMs and alerts
- Calendar integrations (Google Calendar, Outlook)
- Advanced analytics and reporting
- Mobile app for trainee access
- Integration with Learning Management Systems (LMS)
- Multi-language support
- Advanced scheduling and conflict detection
- Predictive analytics for trainee success

---

**Last Updated:** March 2024
**Version:** 2.0.0
