# AI-Coach Demo Video Guide

## Quick Overview (1-2 minutes total)

This guide provides step-by-step instructions to create a demo video showcasing the AI-Coach system with practical test cases.

---

## Pre-Demo Setup

### Step 1: Start the Backend
```bash
cd backend
python -m pip install -r requirements.txt  # If not already installed
uvicorn app.main:app --reload
```
✅ Backend runs on `http://localhost:8000`

### Step 2: Start the Frontend
```bash
cd frontend
npm install  # If not already installed
npm start
```
✅ Frontend runs on `http://localhost:3000`

---

## Demo Test Cases (Choose 3-4 for video)

### TEST CASE 1: Create a New Cohort (30 seconds)
**What to show**: System initialization with a training cohort

**Steps:**
1. Open frontend at `http://localhost:3000/dashboard`
2. Click "Create Cohort" button
3. Fill in:
   - Cohort Name: `Q1 2026 Leadership Batch`
   - Duration: `12 weeks`
   - Total Trainees: `25`
   - Lead Coach: `Your Name`
4. Click "Create"

**Expected Outcome:**
- Cohort appears in dashboard with metrics (0 sessions, 0 attendees, etc.)
- Success message displays

**API Tested:** `POST /api/cohorts` (create new cohort)

---

### TEST CASE 2: Schedule a Training Session with MoM Generation (45 seconds)
**What to show**: Session creation and automatic Minutes of Meeting generation

**Steps:**
1. In dashboard, click "Add Session"
2. Fill in session details:
   - Title: `Week 1 - Platform Walkthrough`
   - Session Type: `platform_walkthrough`
   - Date: `2026-03-03`
   - Facilitator: `John Trainer`
   - Expected Attendees: `20`
   - Discussion Points: `Platform overview, navigation, account setup`
3. Click "Schedule Session"
4. In Sessions tab, click on the new session
5. Click "Generate MoM"

**Expected Outcome:**
- Session appears in list with status "Scheduled"
- MoM auto-generates with:
  ```
  Summary: "Session on Week 1 - Platform Walkthrough was conducted..."
  Key Decisions: [bullet points about training]
  Action Items: [owner-based task list with dates]
  Risks: [identified risks if any]
  ```

**APIs Tested:** 
- `POST /api/sessions` (create session)
- `POST /api/sessions/{id}/mom` (generate MoM)

---

### TEST CASE 3: Track Trainee Attendance & Generate Progress Report (45 seconds)
**What to show**: Attendance tracking and AI-based cohort summary

**Steps:**
1. In Progress Tracking tab, click "Mark Attendance"
2. Select the scheduled session
3. Mark attendance for 5 trainees:
   - 4 as "Present" (80%)
   - 1 as "Absent"
4. Click "Save Attendance"
5. Click "Generate Cohort Summary"

**Expected Outcome:**
- Attendance records show:
  ```
  Session: Week 1 - Platform Walkthrough
  Attendance: 4/5 (80%)
  ```
- AI-generated summary displays:
  ```
  Weekly Performance Summary:
  - Attendance: 80% (Good)
  - Self-learning: Pending
  - Hands-on: Pending
  - Recommendations: [action items]
  ```

**APIs Tested:**
- `POST /api/attendance` (record attendance)
- `GET /api/cohorts/{id}/summary` (generate cohort summary)

---

### TEST CASE 4: Auto-Generate Welcome Email for New Trainee (30 seconds)
**What to show**: Document template system in action

**Steps:**
1. Go to Documents tab
2. Click "Generate Document"
3. Select: `welcome_mail`
4. Fill variables:
   - Trainee Name: `Rajesh Kumar`
   - Start Date: `2026-03-03`
   - Location: `Virtual - Zoom`
   - Trainer Name: `John Trainer`
5. Click "Generate"
6. View the generated document

**Expected Outcome:**
- Professional welcome email appears with:
  ```
  Subject: Welcome to Q1 2026 Leadership Batch
  
  Dear Rajesh Kumar,
  
  Welcome to the training cohort! We are excited to have you on board.
  
  Important Information:
  - Program Start Date: 2026-03-03
  - Training Location: Virtual - Zoom
  - Your Training Lead: John Trainer
  ...
  ```

**APIs Tested:** `POST /api/documents/generate` (template-based document generation)

---

### TEST CASE 5: Create & Track Evaluation (45 seconds) - *Optional*
**What to show**: Assessment system with AI feedback

**Steps:**
1. Go to Evaluations tab
2. Click "Create Evaluation"
3. Fill:
   - Evaluation Type: `L1 Feedback`
   - For Session: `Week 1 - Platform Walkthrough`
4. Add scores (1-5):
   - Content Quality: 4
   - Facilitator: 5
   - Relevance: 4
   - Pacing: 5
5. Click "Save Evaluation"
6. View evaluation summary

**Expected Outcome:**
- Average score: 4.5/5
- Status: `Submitted`
- Feedback recorded and stored

**APIs Tested:** `POST /api/evaluations` (evaluation submission)

---

## Video Recording Script (2-3 minutes total)

### **Opening (20 seconds)**
```
"Welcome to AI-Coach, an enterprise training management system. 
Today we'll demonstrate how organizations can efficiently manage 
training cohorts, track progress, and automatically generate 
professional documents using AI. 

Our system is completely local and company-safe - no external APIs, 
100% secure data handling."
```

### **Demo Flow**
1. **Cohort Creation** (30 sec) - "First, we create a new training cohort..."
2. **Session Scheduling** (45 sec) - "Next, we schedule training sessions and auto-generate meeting notes..."
3. **Progress Tracking** (45 sec) - "The system tracks attendance and generates performance summaries..."
4. **Document Generation** (30 sec) - "Finally, professional documents are auto-generated from templates..."

### **Closing (20 seconds)**
```
"AI-Coach helps trainers focus on training quality while the system 
handles administrative tasks like documentation, summaries, and reports. 
All locally, all securely, all efficiently."
```

---

## API Endpoints Summary (Reference for Demo)

| Feature | Endpoint | Method |
|---------|----------|--------|
| Create Cohort | `/api/cohorts` | POST |
| Schedule Session | `/api/sessions` | POST |
| Generate MoM | `/api/sessions/{id}/mom` | POST |
| Mark Attendance | `/api/attendance` | POST |
| Generate Summary | `/api/cohorts/{id}/summary` | GET |
| Generate Document | `/api/documents/generate` | POST |
| Create Evaluation | `/api/evaluations` | POST |

---

## Quick API Testing (Using Postman/cURL)

### Test MoM Generation via API:
```bash
curl -X POST "http://localhost:8000/api/sessions/1/mom" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Week 1 Training",
    "facilitator": "John",
    "attendees": 20,
    "discussion_points": "Platform overview and navigation"
  }'
```

### Test Document Generation via API:
```bash
curl -X POST "http://localhost:8000/api/documents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_type": "welcome_mail",
    "variables": {
      "cohort_name": "Q1 2026 Batch",
      "trainee_name": "Rajesh Kumar",
      "start_date": "2026-03-03",
      "trainer_name": "John Trainer"
    }
  }'
```

---

## Video Recording Tips

1. **Slow down**: Record at 1.5x normal speed for clarity
2. **Use real data**: Fill in meaningful names and dates
3. **Highlight success**: Show success messages and generated outputs
4. **Voice-over**: Add narration explaining what's happening at each step
5. **Total time**: Keep demo under 3-5 minutes
6. **Tools**: Use OBS, ScreenFlow, or Camtasia for recording

---

## What NOT to Show
- ❌ Error messages or failures
- ❌ Backend code or infrastructure
- ❌ Database schema details
- ❌ API authentication tokens
- ❌ Slow network requests

---

## What TO Emphasize
- ✅ Professional, polished UI
- ✅ Quick, seamless workflows
- ✅ Automatic document generation
- ✅ Real-time progress tracking
- ✅ No external API calls (company-safe)
- ✅ Professional output quality

---

## Expected Outputs During Demo

**MoM Generation Output:**
```json
{
  "summary": "Session on Week 1 - Platform Walkthrough was conducted successfully...",
  "key_decisions": "• Training content was well-received\n• Follow-up session to be scheduled",
  "action_items": "• Share session materials - Owner: John Trainer - Due: Within 2 days",
  "risks_identified": "None identified"
}
```

**Welcome Email Output:**
```
Subject: Welcome to Q1 2026 Leadership Batch

Dear Rajesh Kumar,

Welcome to the training cohort! We are excited to have you on board.

Important Information:
- Program Start Date: 2026-03-03
- Training Location: Virtual - Zoom
- Your Training Lead: John Trainer
- Duration: 12 weeks

[Full welcome email with guidelines and support info]
```

**Cohort Summary Output:**
```
Weekly Performance Summary for Q1 2026 Leadership Batch:

The cohort is performing well with an average attendance of 80%. 
Self-learning completion is on track at 75% progress, 
and hands-on activities are progressing at 60% completion.

Recommendations:
• Conduct 1-on-1 sessions with trainees showing low attendance
• Schedule additional support sessions for hands-on activities
• Recognize and celebrate high performers
• Share best practices from top performers with the group
```

---

## Next Steps After Demo

1. **Edit video**: Trim intro/outro, add title cards, background music
2. **Add captions**: For accessibility
3. **Export**: 1080p, MP4 format
4. **Upload**: To internal platform or YouTube
5. **Share**: With stakeholders and team members

---

**Total Demo Duration: 3-5 minutes**
**Setup Time: 2-3 minutes**
**Recording Time: 5-10 minutes (with retakes)**
