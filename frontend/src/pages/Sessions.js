import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { sessionService } from '../services/api';
import '../styles/Sessions.css';

const Sessions = () => {
  const [formData, setFormData] = useState({
    session_type: 'workout',
    duration_minutes: 30,
    exercises_completed: 5,
    calories_burned: 200,
    mood_before: 'neutral',
    mood_after: 'good',
    difficulty_level: 'medium',
    notes: '',
  });
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchSessions();
  }, [token, navigate]);

  const fetchSessions = async () => {
    try {
      const response = await sessionService.getUserSessions(token);
      setSessions(response.data);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'duration_minutes' || name === 'exercises_completed' || name === 'calories_burned'
        ? parseInt(value) || value
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await sessionService.createSession(formData, token);
      setFormData({
        session_type: 'workout',
        duration_minutes: 30,
        exercises_completed: 5,
        calories_burned: 200,
        mood_before: 'neutral',
        mood_after: 'good',
        difficulty_level: 'medium',
        notes: '',
      });
      fetchSessions();
      alert('Session recorded successfully! 🎉');
    } catch (error) {
      alert('Error creating session: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (sessionId) => {
    if (window.confirm('Delete this session?')) {
      try {
        await sessionService.deleteSession(sessionId, token);
        fetchSessions();
      } catch (error) {
        alert('Error deleting session');
      }
    }
  };

  return (
    <div className="sessions-container">
      <header className="sessions-header">
        <button onClick={() => navigate('/dashboard')} className="back-btn">← Back to Dashboard</button>
        <h1>📝 Coaching Sessions</h1>
      </header>

      <div className="sessions-layout">
        <div className="form-section">
          <h2>Log New Session</h2>
          <form onSubmit={handleSubmit}>
            <select name="session_type" value={formData.session_type} onChange={handleChange} required>
              <option value="workout">🏃 Workout</option>
              <option value="nutrition">🥗 Nutrition</option>
              <option value="mental_health">🧠 Mental Health</option>
              <option value="recovery">😴 Recovery</option>
            </select>

            <label>Duration (minutes)</label>
            <input type="number" name="duration_minutes" value={formData.duration_minutes} onChange={handleChange} required />

            <label>Exercises Completed</label>
            <input type="number" name="exercises_completed" value={formData.exercises_completed} onChange={handleChange} required />

            <label>Calories Burned</label>
            <input type="number" name="calories_burned" value={formData.calories_burned} onChange={handleChange} required />

            <div className="mood-selector">
              <label>Mood Before</label>
              <select name="mood_before" value={formData.mood_before} onChange={handleChange}>
                <option value="very_bad">😞 Very Bad</option>
                <option value="bad">😟 Bad</option>
                <option value="neutral">😐 Neutral</option>
                <option value="good">😊 Good</option>
                <option value="very_good">🤩 Very Good</option>
              </select>

              <label>Mood After</label>
              <select name="mood_after" value={formData.mood_after} onChange={handleChange}>
                <option value="very_bad">😞 Very Bad</option>
                <option value="bad">😟 Bad</option>
                <option value="neutral">😐 Neutral</option>
                <option value="good">😊 Good</option>
                <option value="very_good">🤩 Very Good</option>
              </select>
            </div>

            <label>Difficulty Level</label>
            <select name="difficulty_level" value={formData.difficulty_level} onChange={handleChange}>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
              <option value="extreme">Extreme</option>
            </select>

            <label>Notes</label>
            <textarea name="notes" value={formData.notes} onChange={handleChange} placeholder="How did the session go?"></textarea>

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Saving...' : 'Save Session'}
            </button>
          </form>
        </div>

        <div className="sessions-list-section">
          <h2>Your Sessions ({sessions.length})</h2>
          {sessions.length > 0 ? (
            <div className="sessions-grid">
              {sessions.map(session => (
                <div key={session.id} className="session-item">
                  <div className="session-type">
                    {session.session_type === 'workout' && '🏃'}
                    {session.session_type === 'nutrition' && '🥗'}
                    {session.session_type === 'mental_health' && '🧠'}
                    {session.session_type === 'recovery' && '😴'}
                    <span>{session.session_type}</span>
                  </div>
                  <p><strong>Duration:</strong> {session.duration_minutes} min</p>
                  <p><strong>Exercises:</strong> {session.exercises_completed}</p>
                  <p><strong>Calories:</strong> {session.calories_burned}</p>
                  <p><strong>Difficulty:</strong> {session.difficulty_level}</p>
                  <p><strong>Before → After:</strong> {session.mood_before} → {session.mood_after}</p>
                  <p className="ai-recommendation">
                    <strong>AI Coach:</strong> {session.ai_recommendation}
                  </p>
                  <button onClick={() => handleDelete(session.id)} className="delete-btn">Delete</button>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data">No sessions yet. Start your first session!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Sessions;
