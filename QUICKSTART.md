# AI Coach - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload --port 8000
```

✅ Backend running at: `http://localhost:8000`

### Step 2: Frontend Setup (2 minutes)

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start frontend
npm start
```

✅ Frontend running at: `http://localhost:3000`

### Step 3: API Documentation (1 minute)

Open `http://localhost:8000/docs` in your browser to see interactive API documentation.

---

## 📋 Core Concepts

### Cohort
A training batch/group with a fixed duration
```
Batch 2024-Q1
├─ Start: 2024-03-01
├─ End: 2024-05-31
├─ Trainees: 50
└─ Manager: John Lead
```

### Session
Training activities (Platform walkthrough, Mentor intro, etc.)
```
Session → Attendees → Attendance → L1 Feedback → MoM (Auto-Generated)
```

### Progress Tracking
Monitor trainee learning journey
```
Self-Learning (75%) + Hands-On (60%) + Assessment Ready (Yes/No)
```

### Evaluations
Interim, Final, and Remedial assessments
```
Evaluation → Scores → Pass/Fail → Remedial Needed?
```

---

## 🎯 Common Workflows

### Workflow 1: Schedule a Session & Generate MoM

```bash
# 1. Schedule session
POST /sessions/
{
  "cohort_id": 1,
  "title": "Platform Walkthrough",
  "session_type": "platform_walkthrough",
  "scheduled_date": "2024-03-05T10:00:00",
  "facilitator_id": 2
}

# 2. After session completes, mark as complete
POST /sessions/1/mark-complete
{
  "discussion_points": "Covered features...",
  "recipients": "team@company.com"
}

# 3. MoM auto-generated and available at:
GET /sessions/1/mom
```

### Workflow 2: Track Trainee Progress

```bash
# 1. Get trainee progress
GET /progress/trainee/5

# 2. Update progress
POST /progress/trainee/5/update
{
  "self_learning_percentage": 75,
  "hands_on_percentage": 60,
  "prerequisites_completed": true
}

# 3. Get cohort weekly summary
GET /progress/cohort/1/weekly-summary
```

### Workflow 3: Manage Evaluations

```bash
# 1. Create evaluation
POST /evaluations/
{
  "cohort_id": 1,
  "name": "Final Assessment",
  "evaluation_type": "final"
}

# 2. Submit score for trainee
POST /evaluations/1/score
{
  "trainee_id": 5,
  "score": 78,
  "feedback": "Good performance..."
}

# 3. View all scores
GET /evaluations/cohort/1/scores
```

### Workflow 4: Generate Automated Documents

```bash
# 1. Generate welcome mail
POST /documents/generate
{
  "cohort_id": 1,
  "doc_type": "welcome_mail",
  "variables": {
    "cohort_name": "Batch 2024-Q1",
    "trainee_name": "John Doe"
  }
}

# 2. Send document
POST /documents/send
{
  "document_id": 1,
  "recipients": "john@company.com"
}
```

### Workflow 5: Create Alerts & Reminders

```bash
# 1. Check for low progress and create alerts
POST /reminders/check-progress-alerts/1

# 2. Check for low attendance
POST /reminders/check-attendance-alerts/1

# 3. Schedule session reminder
POST /reminders/session-reminder/1?hours_before=24

# 4. Get pending reminders
GET /reminders/pending/1
```

---

## 📊 Dashboard Views

### Cohort Dashboard
- Total trainees, active, graduated, exited
- Average attendance percentage
- Days remaining
- Quick actions: Schedule session, view progress

### Session Management
- Scheduled vs completed sessions
- MoM generation status
- Attendance tracking
- Feedback collection

### Progress Tracking
- Self-learning completion %
- Hands-on completion %
- Assessment readiness
- Weekly cohort summary

### Evaluations
- Upcoming evaluations
- Score tracking
- Pass/fail distribution
- Remedial required count

### Documents
- Auto-generated templates
- Document history
- Sent status
- Alert dashboard

---

## 🔌 API Endpoints Summary

| Feature | Method | Endpoint |
|---------|--------|----------|
| **Cohorts** |
| List cohorts | GET | `/cohorts/` |
| Create cohort | POST | `/cohorts/` |
| Get dashboard | GET | `/cohorts/{id}/dashboard` |
| **Sessions** |
| Create session | POST | `/sessions/` |
| Mark complete | POST | `/sessions/{id}/mark-complete` |
| Get MoM | GET | `/sessions/{id}/mom` |
| **Progress** |
| Get progress | GET | `/progress/trainee/{id}` |
| Weekly summary | GET | `/progress/cohort/{id}/weekly-summary` |
| **Evaluations** |
| Submit score | POST | `/evaluations/{id}/score` |
| L1 Feedback | POST | `/evaluations/l1-feedback/` |
| **Documents** |
| Generate doc | POST | `/documents/generate` |
| Send doc | POST | `/documents/send` |
| Create alert | POST | `/documents/alerts/` |
| **Reminders** |
| Session reminder | POST | `/reminders/session-reminder/{id}` |
| Check alerts | POST | `/reminders/check-attendance-alerts/{cohort_id}` |

---

## 💡 Tips & Tricks

### Tip 1: Use Mock Data for Testing
AI service automatically uses mock responses if OpenAI API is not configured.

### Tip 2: Automated MoM Generation
Just mark a session complete - MoM generates automatically in background!

### Tip 3: Weekly Cohort Summary
Get AI-powered insights into cohort performance:
```bash
GET /progress/cohort/1/weekly-summary
```

### Tip 4: Create Custom Document Templates
```bash
POST /documents/templates/
{
  "name": "custom_mail",
  "template_type": "mail",
  "content": "Dear {{trainee_name}}, ...",
  "required_variables": ["trainee_name", "cohort_name"]
}
```

---

## 🔧 Troubleshooting

### Issue: "Database connection error"
**Solution:** Check DATABASE_URL in .env file
```bash
# SQLite (default)
DATABASE_URL=sqlite:///./ai_coach.db

# MySQL
DATABASE_URL=mysql://user:password@localhost/ai_coach
```

### Issue: "MoM not generating"
**Solution:** Check if OpenAI API key is set (optional - uses mock fallback)
```bash
# .env
OPENAI_API_KEY=sk-...
```

### Issue: "Frontend can't connect to backend"
**Solution:** Update API URL in frontend .env
```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000/api
```

### Issue: CORS errors
**Solution:** Already configured in app - backend allows all origins. Check browser console for specific errors.

---

## 📚 Next Steps

1. ✅ Setup complete!
2. 📖 Read [full README](README_NEW.md) for detailed documentation
3. 🎓 Explore [API documentation](/docs) - auto-generated by FastAPI
4. 🧪 Try sample workflows above
5. 🚀 Build custom features

---

## 🎬 Sample Use Case

**Scenario:** Managing a 50-person training cohort for 3 months

**Week 1:**
- Create cohort: `POST /cohorts/`
- Add trainees: `POST /cohorts/1/trainees` (50 times)
- Schedule platform walkthrough: `POST /sessions/`

**Weekly:**
- Mark sessions complete: `POST /sessions/{id}/mark-complete`
- MoM auto-generated ✓
- Check progress alerts: `POST /reminders/check-attendance-alerts/1`
- Get weekly summary: `GET /progress/cohort/1/weekly-summary`

**Evaluations:**
- Create evaluation: `POST /evaluations/`
- Submit scores: `POST /evaluations/1/score`
- Generate graduation checklist: `POST /documents/generate`

**Result:**
- All sessions tracked
- MoMs auto-generated
- Progress monitored
- Evaluations managed
- Documents automated
- Alerts sent automatically

---

## 📞 Support

- **API Docs:** http://localhost:8000/docs
- **README:** [README_NEW.md](README_NEW.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Version:** 2.0.0  
**Last Updated:** March 2024
