import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { progressService, sessionService } from '../services/api';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [progressData, setProgressData] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchData();
  }, [token, navigate]);

  const fetchData = async () => {
    try {
      const [statsRes, progressRes, sessionsRes] = await Promise.all([
        progressService.getStats(token),
        progressService.getUserProgress(token),
        sessionService.getUserSessions(token),
      ]);
      
      setStats(statsRes.data);
      setProgressData(progressRes.data.slice(0, 10).reverse());
      setSessions(sessionsRes.data.slice(0, 5));
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading your dashboard...</div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>🏋️ AI Coach Dashboard</h1>
        <div className="header-actions">
          <button onClick={() => navigate('/sessions')} className="nav-btn">New Session</button>
          <button onClick={() => navigate('/chat')} className="nav-btn chat-btn">💬 Chat with Coach</button>
          <button onClick={() => navigate('/profile')} className="nav-btn profile-btn">Profile</button>
          <button onClick={() => {
            localStorage.removeItem('token');
            navigate('/login');
          }} className="nav-btn logout-btn">Logout</button>
        </div>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">💪</div>
          <div className="stat-content">
            <h3>Total Workouts</h3>
            <p className="stat-value">{stats?.total_workouts || 0}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <h3>Calories Burned</h3>
            <p className="stat-value">{stats?.total_calories_burned?.toFixed(0) || 0}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⚖️</div>
          <div className="stat-content">
            <h3>Current Weight</h3>
            <p className="stat-value">{stats?.current_weight?.toFixed(1) || 'N/A'} kg</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">😊</div>
          <div className="stat-content">
            <h3>Avg Mood</h3>
            <p className="stat-value">{stats?.average_mood || 0}/10</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <h3>Workout Streak</h3>
            <p className="stat-value">{stats?.workout_streak || 0} days</p>
          </div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-container">
          <h2>Weight Progress</h2>
          {progressData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={progressData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="id" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="weight" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="no-data">No progress data yet. Start logging your progress!</p>
          )}
        </div>

        <div className="chart-container">
          <h2>Workout Activity</h2>
          {sessions.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={sessions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="id" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="exercises_completed" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="no-data">No sessions recorded yet. Complete your first session!</p>
          )}
        </div>
      </div>

      <div className="recent-section">
        <h2>Recent Workouts</h2>
        {sessions.length > 0 ? (
          <div className="sessions-list">
            {sessions.map(session => (
              <div key={session.id} className="session-card">
                <div className="session-header">
                  <h3>{session.session_type.toUpperCase()}</h3>
                  <span className="difficulty">{session.difficulty_level}</span>
                </div>
                <p>Duration: {session.duration_minutes} min | Exercises: {session.exercises_completed}</p>
                <p>Calories: {session.calories_burned.toFixed(0)} | Mood: {session.mood_after}</p>
                <p className="ai-rec">{session.ai_recommendation}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data">No sessions yet. Start your first workout session!</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
