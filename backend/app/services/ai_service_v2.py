import os
import json
from typing import Dict, Any

# Local AI Service - No external API calls (Company-safe)

class AIService:
    """
    Local AI Service using templates and rule-based generation.
    No external API calls - completely secure for company projects.
    """
    
    def generate_mom(self, session_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate Minutes of Meeting from session data (Template-based)"""
        return {
            "summary": f"Session on {session_data.get('title', 'Training')} was conducted successfully. "
                      f"Facilitated by {session_data.get('facilitator', 'Training Team')} with {session_data.get('attendees', 'multiple')} participants. "
                      f"Key topics discussed: {session_data.get('discussion_points', 'Training content')}.",
            
            "key_decisions": self._generate_decisions(session_data),
            "action_items": self._generate_action_items(session_data),
            "risks_identified": session_data.get('risks', 'None identified')
        }
    
    def _generate_decisions(self, session_data: Dict) -> str:
        """Generate key decisions from session"""
        decisions = [
            "• Training content was well-received by participants",
            "• Follow-up session to be scheduled",
            "• Resources/materials to be shared with all attendees"
        ]
        if session_data.get('decisions'):
            decisions.insert(0, f"• {session_data.get('decisions')}")
        return "\n".join(decisions)
    
    def _generate_action_items(self, session_data: Dict) -> str:
        """Generate action items from session"""
        items = [
            f"• Share session materials - Owner: {session_data.get('facilitator', 'Trainer')} - Due: Within 2 days",
            "• Collect feedback from participants - Owner: Admin - Due: Within 1 day",
            "• Schedule follow-up session - Owner: Coordinator - Due: Within 1 week"
        ]
        if session_data.get('action_items'):
            items.insert(0, f"• {session_data.get('action_items')}")
        return "\n".join(items)
    
    def summarize_cohort_progress(self, cohort_data: Dict[str, Any]) -> str:
        """Generate cohort performance summary (Rule-based)"""
        name = cohort_data.get('cohort_name', 'Cohort')
        attendance = cohort_data.get('avg_attendance', 85)
        learning = cohort_data.get('self_learning_progress', 75)
        hands_on = cohort_data.get('hands_on_completion', 60)
        
        # Generate status based on metrics
        attendance_status = "excellent" if attendance >= 90 else "good" if attendance >= 80 else "needs attention"
        learning_status = "on track" if learning >= 75 else "behind schedule"
        hands_on_status = "progressing" if hands_on >= 60 else "needs support"
        
        summary = f"""
Weekly Performance Summary for {name}:

The cohort is performing {attendance_status} with an average attendance of {attendance}%. 
Self-learning completion is {learning_status} at {learning}% progress, 
and hands-on activities are {hands_on_status} at {hands_on}% completion.

Recommendations:
• Conduct 1-on-1 sessions with trainees showing low attendance or progress
• Schedule additional support sessions for hands-on activities
• Recognize and celebrate high performers to boost team morale
• Share best practices from top performers with the group
• Review challenging topics and provide additional resources
• Consider peer learning groups for collaborative support
"""
        return summary
    
    def generate_document(self, doc_type: str, variables: Dict[str, str]) -> str:
        """Generate documents (Template-based)"""
        templates = {
            "welcome_mail": self._template_welcome_mail,
            "warning_mail": self._template_warning_mail,
            "graduation_checklist": self._template_graduation_checklist,
            "feedback_reminder": self._template_feedback_reminder,
            "project_details": self._template_project_details,
            "evaluation_guidelines": self._template_evaluation_guidelines,
            "feedback_closure_update": self._template_feedback_closure_update,
            "weekly_stakeholder_summary": self._template_weekly_stakeholder_summary,
        }
        
        generator = templates.get(doc_type)
        if generator:
            return generator(variables)
        return f"Template '{doc_type}' not found"

    def chat_response(self, message: str) -> str:
        """Simple AI chat responder (rule-based echo)."""
        # this could be replaced with more sophisticated logic or external API
        return f"AI Coach: I heard you say '{message}'"
    
    def _template_welcome_mail(self, vars: Dict[str, str]) -> str:
        return f"""
Subject: Welcome to {vars.get('cohort_name', 'Our Training Program')}

Dear {vars.get('trainee_name', 'Participant')},

Welcome to {vars.get('cohort_name', 'the training cohort')}! We are excited to have you on board.

Important Information:
- Program Start Date: {vars.get('start_date', 'To be confirmed')}
- Training Location: {vars.get('location', 'To be confirmed')}
- Your Training Lead: {vars.get('trainer_name', 'TBA')}
- Duration: {vars.get('duration', 'TBA')}

Before You Start:
✓ Set up your laptop with required software
✓ Review the pre-learning materials (available on the portal)
✓ Join our communication channels and groups
✓ Complete the onboarding survey
✓ Ensure you have all required documents

Important Guidelines:
- Maintain minimum 80% attendance
- Submit all assignments on time
- Participate actively in sessions
- Follow code of conduct at all times
- Reach out if you need any support

We look forward to your success!

Best regards,
Training & Development Team
"""
    
    def _template_warning_mail(self, vars: Dict[str, str]) -> str:
        return f"""
Subject: Performance Alert - Action Required

Dear {vars.get('trainee_name', 'Participant')},

We are reaching out to you as we have observed some concerns regarding your training progress.

Current Status:
- Attendance: {vars.get('attendance', 'Below target')}%
- Progress: {vars.get('progress', 'Behind schedule')}
- Outstanding: {vars.get('outstanding', 'Pending assignments')}

This is a friendly reminder to help you get back on track. Please take the following actions:

Action Items:
1. Schedule a meeting with your mentor to discuss challenges
2. Complete all pending assignments by {vars.get('due_date', 'next week')}
3. Commit to attending all upcoming sessions
4. Reach out to us if you need additional support or resources

Support Available:
- One-on-one mentoring sessions
- Remedial training modules
- Extended assignment deadlines (if needed)
- Peer learning groups

Deadline: {vars.get('deadline', 'End of this week')}

We are here to help you succeed!

Regards,
Training Management Team
"""
    
    def _template_graduation_checklist(self, vars: Dict[str, str]) -> str:
        return f"""
GRADUATION CHECKLIST FOR {vars.get('trainee_name', 'TRAINEE').upper()}

Trainee: {vars.get('trainee_name', 'N/A')}
Cohort: {vars.get('cohort_name', 'N/A')}
Target Graduation Date: {vars.get('completion_date', 'TBA')}

ACADEMIC REQUIREMENTS:
☐ All modules completed
☐ All assessments passed (scores ≥ 40%)
☐ Project submission completed and approved
☐ Final evaluation completed
☐ Attendance requirement met (≥ 80%)
☐ L1 feedback submitted

ADMINISTRATIVE REQUIREMENTS:
☐ All documents submitted
☐ Exit feedback collected
☐ Final evaluation form signed
☐ Contact information updated
☐ Feedback forms completed

GRADUATION CHECKLIST:
☐ Ceremony slot confirmed
☐ Certificate ready for printing
☐ Alumni information recorded
☐ Graduation pack prepared
☐ Final communication sent

Current Status: {vars.get('status', 'In Progress')}
Progress: {vars.get('progress_percent', 'TBA')}%

Next Steps: {vars.get('next_steps', 'Complete pending items and contact your coordinator')}
"""
    
    def _template_feedback_reminder(self, vars: Dict[str, str]) -> str:
        return f"""
Subject: Please Submit Your Feedback - {vars.get('session_title', 'Training Session')}

Hi {vars.get('trainee_name', 'there')},

We value your feedback! Your input helps us improve our training programs.

Session Details:
- Title: {vars.get('session_title', 'Training Session')}
- Date: {vars.get('session_date', 'N/A')}
- Facilitator: {vars.get('facilitator_name', 'N/A')}
- Duration: {vars.get('duration', 'N/A')}

Feedback Categories (Rate 1-5):
1. Content Quality - Was the content clear and relevant?
2. Facilitator Effectiveness - Was the trainer engaging and knowledgeable?
3. Relevance - How relevant was this to your learning goals?
4. Pacing - Was the session paced appropriately?

Additional Comments:
Please share any specific feedback, suggestions, or concerns.

How to Provide Feedback:
→ Link: {vars.get('feedback_link', 'https://feedback.yourcompany.com')}
→ Deadline: {vars.get('deadline', 'End of day')}
→ Time required: ~2 minutes

Why Your Feedback Matters:
• Helps us improve future sessions
• Identifies trainer strengths and areas for growth
• Ensures training remains relevant and effective
• Contributes to continuous quality improvement

Thank you for your valuable input!

Best regards,
Training Team
"""
    
    def _template_project_details(self, vars: Dict[str, str]) -> str:
        """Project details document before project phase"""
        return f"""
PROJECT DETAILS & GUIDELINES

Project Name: {vars.get('project_name', 'Project TBD')}
Project Phase: {vars.get('project_phase', 'Phase 1')}
Duration: {vars.get('duration', 'TBD')} weeks
Start Date: {vars.get('start_date', 'TBD')}
End Date: {vars.get('end_date', 'TBD')}

Learning Objectives:
{vars.get('objectives', '• Apply technical skills\n• Develop problem-solving abilities\n• Gain hands-on experience')}

Project Requirements:
{vars.get('requirements', '• Complete all modules\n• Collaborate with team members\n• Follow best practices')}

Tools & Technologies:
{vars.get('tools', 'To be shared in kickoff session')}

Team Composition:
Team Size: {vars.get('team_size', 'TBD')}
Team Lead: {vars.get('team_lead', 'TBD')}
Mentor: {vars.get('mentor', 'Assigned during kickoff')}

Success Criteria:
✓ {vars.get('criteria_1', 'Project delivered on time')}
✓ {vars.get('criteria_2', 'Meeting quality standards')}
✓ {vars.get('criteria_3', 'All team members contribute')}
✓ {vars.get('criteria_4', 'Documentation complete')}

Evaluation Method:
- Code review and quality assessment
- Functionality testing
- Presentation and documentation
- Peer and mentor feedback
- Self-assessment

Key Contacts:
Project Manager: {vars.get('pm_email', 'pm@company.com')}
Mentor: {vars.get('mentor_email', 'mentor@company.com')}
Support: {vars.get('support_email', 'support@company.com')}

Important Dates:
- Kickoff: {vars.get('kickoff_date', 'TBD')}
- Mid-point Review: {vars.get('midpoint_date', 'TBD')}
- Final Submission: {vars.get('submission_date', 'TBD')}
- Presentation: {vars.get('presentation_date', 'TBD')}

Resources Available:
• Project documentation and templates
• Code repositories and version control
• Communication channels (Slack/Teams)
• Knowledge base and FAQs
• Escalation support

Questions?
Please reach out to {vars.get('support_email', 'support@company.com')} anytime during the project.

Good luck and let's build something great together!
"""
    
    def _template_evaluation_guidelines(self, vars: Dict[str, str]) -> str:
        """Guidelines for evaluators on assessment process"""
        return f"""
EVALUATION GUIDELINES FOR EVALUATORS

Dear {vars.get('evaluator_name', 'Evaluator')},

Thank you for being an evaluator for this cohort. Below are guidelines to ensure consistent, fair, and comprehensive assessments.

EVALUATION TYPES COVERED:
1. Interim Evaluations - Mid-way checkpoint (Week {vars.get('interim_week', '6')})
2. Final Evaluations - End of cohort assessment
3. Remedial Evaluations - Follow-up for improvement areas

ASSESSMENT CRITERIA:

Technical Competency (40%)
- Demonstrates understanding of core concepts
- Applies knowledge to solve problems
- Shows improvement from interim to final evaluation
- Meets coding standards and best practices

Practical Application (30%)
- Completes hands-on assignments correctly
- Debugs and resolves issues effectively
- Optimizes solutions for performance
- Documents code properly

Soft Skills (20%)
- Communication and presentation abilities
- Collaboration with peers and mentors
- Problem-solving approach
- Learning agility

Compliance (10%)
- Meets attendance requirements
- Submits deliverables on time
- Follows company policies
- Professional conduct

SCORING SYSTEM:

Level 5: Exceeds Expectations
- Exceptional performance, ready for advanced roles
- Score: 85-100

Level 4: Meets Expectations
- Competent and confident, ready for deployment
- Score: 75-84

Level 3: Developing
- Shows potential, needs improvement in specific areas
- Score: 65-74

Level 2: Needs Support
- Significant gaps, requires remediation
- Score: 50-64

Level 1: Not Met
- Does not meet minimum standards
- Score: Below 50

EVALUATION PROCESS:

1. Review Pre-evaluation Materials
   - Candidate submission
   - Performance records
   - Attendance logs
   - Previous feedback

2. Conduct Assessment
   - Technical assessment (30-45 minutes)
   - Project review (20-30 minutes)
   - Discussion (15-20 minutes)

3. Document Findings
   - Score each criterion objectively
   - Provide specific examples
   - Note strengths and improvement areas
   - Recommend remediation if needed

4. Provide Feedback
   - Be constructive and supportive
   - Balance positive feedback with areas to improve
   - Suggest concrete next steps
   - Encourage growth mindset

COMMON PITFALLS TO AVOID:

❌ Bias - Evaluate only on merit, not on personalities
❌ Leniency - Apply same standards to all candidates
❌ Halo Effect - Don't let one skill override others
❌ Recency - Consider entire assessment period
❌ Vagueness - Be specific with examples

DO's & DON'Ts:

DO:
✓ Be objective and fair
✓ Base scores on evidence
✓ Provide constructive criticism
✓ Acknowledge effort and improvement
✓ Recommend support when needed

DON'T:
✗ Make assumptions without verification
✗ Let personal feelings influence scoring
✗ Compare candidates directly
✗ Rush the evaluation process
✗ Give scores without justification

REMEDIATION RECOMMENDATIONS:

If score < 70, recommend:
- Specific modules to revisit
- Additional mentoring sessions
- Practice projects to strengthen skills
- Remedial evaluation timeline

TIMELINE:

Interim Evaluation: Week {vars.get('interim_week', '6')}
Final Evaluation: Week {vars.get('final_week', '12')}
Remedial (if needed): Week {vars.get('remedial_week', '13-14')}

SUBMISSION:

- Complete evaluation by: {vars.get('deadline', 'Date TBD')}
- Submit to: {vars.get('submission_email', 'evaluations@company.com')}
- Format: Use provided evaluation template
- Confidentiality: Keep scores and comments confidential

SUPPORT:

If you have questions:
- Email: {vars.get('evaluation_lead_email', 'lead@company.com')}
- Phone: {vars.get('evaluation_lead_phone', 'Available on request')}
- Office Hours: {vars.get('office_hours', 'TBD')}

Thank you for your commitment to fair and thorough evaluation!

Best regards,
Evaluation Team
"""
    
    def _template_feedback_closure_update(self, vars: Dict[str, str]) -> str:
        """Feedback closure call update"""
        return f"""
FEEDBACK CLOSURE CALL UPDATE

Trainee: {vars.get('trainee_name', 'N/A')}
Cohort: {vars.get('cohort_name', 'N/A')}
Call Date: {vars.get('call_date', 'TBD')}
Facilitator: {vars.get('facilitator', 'TBD')}

SESSION SUMMARY:

Discussion Topics:
{vars.get('topics', '• Overall learning experience\n• Areas of strength\n• Areas for improvement\n• Future career goals')}

Key Feedback Received:
{vars.get('key_feedback', 'Summary to be filled by facilitator')}

STRENGTHS IDENTIFIED:
• {vars.get('strength_1', 'Strong technical foundation')}
• {vars.get('strength_2', 'Good collaboration skills')}
• {vars.get('strength_3', 'Consistent attendance and engagement')}

AREAS FOR IMPROVEMENT:
• {vars.get('improvement_1', 'Deepen knowledge in specific domain')}
• {vars.get('improvement_2', 'Enhance presentation skills')}
• {vars.get('improvement_3', 'Strengthen problem-solving approach')}

ACTION ITEMS FOR TRAINEE:

1. {vars.get('action_1', 'Complete advanced module')}
   Deadline: {vars.get('action_1_deadline', 'TBD')}
   
2. {vars.get('action_2', 'Practice coding challenges')}
   Deadline: {vars.get('action_2_deadline', 'TBD')}
   
3. {vars.get('action_3', 'Schedule mentor follow-up')}
   Deadline: {vars.get('action_3_deadline', 'TBD')}

NEXT STEPS:

Career Path: {vars.get('career_path', 'To be discussed with HR')}
Further Learning: {vars.get('further_learning', 'Recommended programs: TBD')}
Support Needed: {vars.get('support_needed', 'None / Specify as needed')}

FINAL RATING: {vars.get('final_rating', 'TBD')}/5.0

Overall Assessment:
{vars.get('overall_assessment', 'The trainee has completed the cohort successfully and is prepared for next phase.')}

Signed by: {vars.get('facilitator', 'TBD')}
Date: {vars.get('signature_date', 'TBD')}

For questions or clarification, please contact: {vars.get('contact_email', 'support@company.com')}
"""
    
    def _template_weekly_stakeholder_summary(self, vars: Dict[str, str]) -> str:
        """Weekly stakeholder feedback summary"""
        return f"""
WEEKLY STAKEHOLDER SUMMARY

Week: {vars.get('week', 'TBD')}
Cohort: {vars.get('cohort_name', 'N/A')}
Reporting Period: {vars.get('start_date', 'TBD')} to {vars.get('end_date', 'TBD')}

EXECUTIVE SUMMARY:

Cohort Status: {vars.get('cohort_status', 'On Track')}
Overall Progress: {vars.get('overall_progress', '75%')}
Key Highlight: {vars.get('key_highlight', 'Successful completion of Module 3')}

PERFORMANCE METRICS:

Attendance: {vars.get('attendance', '85%')}
On-time Completion: {vars.get('on_time_completion', '90%')}
Assessment Average: {vars.get('assessment_avg', '78%')}
Engagement Score: {vars.get('engagement_score', '8.2/10')}

WHAT'S GOING WELL:

✓ {vars.get('positive_1', 'Strong teamwork and collaboration')}
✓ {vars.get('positive_2', 'Excellent problem-solving mindset')}
✓ {vars.get('positive_3', 'Consistent progress in technical skills')}
✓ {vars.get('positive_4', 'Positive feedback from trainers')}

CHALLENGES & CONCERNS:

⚠ {vars.get('challenge_1', 'Some trainees struggling with advanced concepts')}
⚠ {vars.get('challenge_2', 'Need for additional hands-on support')}

ACTIONS TAKEN:

• {vars.get('action_1', 'Scheduled remedial sessions for struggling trainees')}
• {vars.get('action_2', 'Added peer mentoring program')}
• {vars.get('action_3', 'Provided additional resources and study materials')}

UPCOMING MILESTONES:

→ {vars.get('milestone_1', 'Mid-cohort evaluation: Week 6')}
→ {vars.get('milestone_2', 'Project phase kickoff: Week 8')}
→ {vars.get('milestone_3', 'Final assessments: Week 12')}

RECOMMENDATIONS FOR STAKEHOLDERS:

1. {vars.get('recommendation_1', 'Continue monitoring progress of identified struggling trainees')}
2. {vars.get('recommendation_2', 'Increase project mentor availability for hands-on phase')}
3. {vars.get('recommendation_3', 'Plan engagement activities to boost morale')}

STAKEHOLDER FEEDBACK HIGHLIGHTS:

From Training Lead:
"{vars.get('lead_feedback', 'Great engagement, trainee quality is good')}"

From HR:
"{vars.get('hr_feedback', 'Attendance and compliance are excellent')}"

From Business Unit:
"{vars.get('bu_feedback', 'Excited to receive trained workforce')}"

FINANCIAL IMPACT:

Budget Status: {vars.get('budget_status', 'On track')}
Cost per Trainee: {vars.get('cost_per_trainee', 'TBD')}
Training ROI: {vars.get('roi', 'Expected 250%')}

NEXT WEEK'S FOCUS:

Focus Area: {vars.get('next_focus', 'Hands-on project execution')}
Expected Outcome: {vars.get('expected_outcome', 'First project milestone completion')}

Prepared by: {vars.get('prepared_by', 'Training Management Team')}
Date: {vars.get('report_date', 'TBD')}
Distribution: {vars.get('distribution', 'Leadership, HR, BU Heads')}

For detailed metrics and questions: {vars.get('contact_email', 'reports@company.com')}
"""

# Initialize service
ai_service = AIService()

def generate_mom(session_data: Dict[str, Any]) -> Dict[str, str]:
    """Generate MoM (template-based, no external calls)"""
    return ai_service.generate_mom(session_data)

def summarize_cohort_progress(cohort_data: Dict[str, Any]) -> str:
    """Generate cohort summary (rule-based, no external calls)"""
    return ai_service.summarize_cohort_progress(cohort_data)

def generate_document(doc_type: str, variables: Dict[str, str]) -> str:
    """Generate documents (template-based, no external calls)"""
    return ai_service.generate_document(doc_type, variables)


def chat(message: str) -> str:
    """Return a chat-style response from the local AI service."""
    return ai_service.chat_response(message)
