import React, { useState, useEffect } from 'react';
import { API_URL } from '../services/api';
import '../styles/Sessions.css';

export default function CoachSessions() {
  const [cohorts, setCohorts] = useState([]);
  const [selectedCohort, setSelectedCohort] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    session_type: 'other',
    scheduled_date: '',
    facilitator_id: 1,
    location: '',
    meeting_link: ''
  });

  useEffect(() => {
    fetchCohorts();
  }, []);

  useEffect(() => {
    if (selectedCohort) {
      fetchSessions(selectedCohort);
    }
  }, [selectedCohort]);

  const fetchCohorts = async () => {
    try {
      const response = await fetch(`${API_URL}/cohorts/`);
      const data = await response.json();
      setCohorts(data);
      if (data.length > 0) {
        setSelectedCohort(data[0].id);
      }
    } catch (error) {
      console.error('Error fetching cohorts:', error);
    }
  };

  const fetchSessions = async (cohortId) => {
    try {
      const response = await fetch(`${API_URL}/sessions/cohort/${cohortId}/schedule`);
      const data = await response.json();
      setSessions(data);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const handleCreateSession = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/sessions/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cohort_id: selectedCohort,
          ...formData
        })
      });
      
      if (response.ok) {
        setShowCreateForm(false);
        fetchSessions(selectedCohort);
        setFormData({
          title: '',
          description: '',
          session_type: 'other',
          scheduled_date: '',
          facilitator_id: 1,
          location: '',
          meeting_link: ''
        });
      }
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const markSessionComplete = async (sessionId) => {
    try {
      const response = await fetch(`${API_URL}/sessions/${sessionId}/mark-complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipients: 'admin@company.com',
          discussion_points: 'Session completed successfully'
        })
      });
      
      if (response.ok) {
        fetchSessions(selectedCohort);
        alert('Session marked complete. MoM generation in progress...');
      }
    } catch (error) {
      console.error('Error marking session complete:', error);
    }
  };

  return (
    <div className="sessions-container">
      <h1>Session Management</h1>
      
      <div className="cohort-selector">
        <label>Select Cohort: </label>
        <select value={selectedCohort || ''} onChange={(e) => setSelectedCohort(parseInt(e.target.value))}>
          {cohorts.map(cohort => (
            <option key={cohort.id} value={cohort.id}>
              {cohort.name}
            </option>
          ))}
        </select>
        <button 
          className="btn btn-primary" 
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancel' : '+ Schedule New Session'}
        </button>
      </div>

      {showCreateForm && (
        <form className="create-session-form" onSubmit={handleCreateSession}>
          <h3>Schedule New Session</h3>
          <div className="form-group">
            <label>Title:</label>
            <input 
              type="text" 
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              required
            />
          </div>
          <div className="form-group">
            <label>Description:</label>
            <textarea 
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Session Type:</label>
            <select 
              value={formData.session_type}
              onChange={(e) => setFormData({...formData, session_type: e.target.value})}
            >
              <option value="platform_walkthrough">Platform Walkthrough</option>
              <option value="solutions_team">Solutions Team</option>
              <option value="bu_leader_connect">BU Leader Connect</option>
              <option value="mentor_intro">Mentor Intro</option>
              <option value="weekly_feedback">Weekly Feedback</option>
              <option value="graduation">Graduation</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div className="form-group">
            <label>Scheduled Date:</label>
            <input 
              type="datetime-local" 
              value={formData.scheduled_date}
              onChange={(e) => setFormData({...formData, scheduled_date: e.target.value})}
              required
            />
          </div>
          <div className="form-group">
            <label>Location:</label>
            <input 
              type="text" 
              value={formData.location}
              onChange={(e) => setFormData({...formData, location: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Meeting Link:</label>
            <input 
              type="url" 
              value={formData.meeting_link}
              onChange={(e) => setFormData({...formData, meeting_link: e.target.value})}
            />
          </div>
          <button type="submit" className="btn btn-primary">Create Session</button>
        </form>
      )}

      <div className="sessions-list">
        <h3>Scheduled Sessions</h3>
        {sessions.length > 0 ? (
          <div className="session-cards">
            {sessions.map(session => (
              <div key={session.id} className="session-card">
                <h4>{session.title}</h4>
                <p><strong>Type:</strong> {session.session_type}</p>
                <p><strong>Scheduled:</strong> {new Date(session.scheduled_date).toLocaleString()}</p>
                <p><strong>Location:</strong> {session.location || 'Virtual'}</p>
                <p><strong>Status:</strong> <span className={`status ${session.status}`}>{session.status}</span></p>
                {session.meeting_link && (
                  <p><a href={session.meeting_link} target="_blank" rel="noopener noreferrer">Join Meeting</a></p>
                )}
                {session.status === 'scheduled' && (
                  <button 
                    className="btn btn-secondary"
                    onClick={() => markSessionComplete(session.id)}
                  >
                    Mark Complete
                  </button>
                )}
                {session.mom_generated && (
                  <p className="mom-indicator">✓ MoM Generated</p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p>No sessions scheduled for this cohort.</p>
        )}
      </div>
    </div>
  );
}
