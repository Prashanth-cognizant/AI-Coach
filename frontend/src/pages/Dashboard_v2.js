import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../services/api';
import '../styles/Dashboard.css';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [cohorts, setCohorts] = useState([]);
  const [selectedCohort, setSelectedCohort] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCohorts();
  }, []);

  const fetchCohorts = async () => {
    try {
      const response = await fetch(`${API_URL}/cohorts/`);
      if (response.status === 401) {
        // token missing/expired
        navigate('/login');
        return;
      }
      const data = await response.json();
      setCohorts(data);
      if (data.length > 0) {
        setSelectedCohort(data[0].id);
        fetchCohortDashboard(data[0].id);
      }
    } catch (error) {
      console.error('Error fetching cohorts:', error);
    } finally {
      // ensure we always leave loading state after first attempt
      setLoading(false);
    }
  };

  const fetchCohortDashboard = async (cohortId) => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/cohorts/${cohortId}/dashboard`);
      if (response.status === 401) {
        navigate('/login');
        return;
      }
      const data = await response.json();
      setDashboardData(data);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCohortChange = (e) => {
    const cohortId = parseInt(e.target.value);
    setSelectedCohort(cohortId);
    fetchCohortDashboard(cohortId);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard-container">
      <h1>AI Coach - Cohort Dashboard</h1>
      
      <div className="cohort-selector">
        <label>Select Cohort: </label>
        <select value={selectedCohort || ''} onChange={handleCohortChange}>
          {cohorts.map(cohort => (
            <option key={cohort.id} value={cohort.id}>
              {cohort.name} - {cohort.batch_code}
            </option>
          ))}
        </select>
      </div>

      {dashboardData && (
        <>
          <div className="dashboard-header">
            <h2>{dashboardData.name}</h2>
            <div className="cohort-info">
              <span>Status: <strong>{dashboardData.status}</strong></span>
              <span>Duration: <strong>{dashboardData.days_remaining} days remaining</strong></span>
            </div>
          </div>

          <div className="tabs">
            <button 
              className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              Overview
            </button>
            <button 
              className={`tab-btn ${activeTab === 'sessions' ? 'active' : ''}`}
              onClick={() => setActiveTab('sessions')}
            >
              Sessions
            </button>
            <button 
              className={`tab-btn ${activeTab === 'progress' ? 'active' : ''}`}
              onClick={() => setActiveTab('progress')}
            >
              Progress Tracking
            </button>
            <button 
              className={`tab-btn ${activeTab === 'evaluations' ? 'active' : ''}`}
              onClick={() => setActiveTab('evaluations')}
            >
              Evaluations
            </button>
            <button 
              className={`tab-btn ${activeTab === 'documents' ? 'active' : ''}`}
              onClick={() => setActiveTab('documents')}
            >
              Documents
            </button>
          </div>

          {activeTab === 'overview' && (
            <div className="tab-content">
              <h3>Cohort Overview</h3>
              <div className="metrics-grid">
                <div className="metric-card">
                  <h4>Total Trainees</h4>
                  <p className="metric-value">{dashboardData.total_trainees}</p>
                </div>
                <div className="metric-card">
                  <h4>Active</h4>
                  <p className="metric-value">{dashboardData.active_trainees}</p>
                </div>
                <div className="metric-card">
                  <h4>Graduated</h4>
                  <p className="metric-value">{dashboardData.graduated}</p>
                </div>
                <div className="metric-card">
                  <h4>Exited</h4>
                  <p className="metric-value">{dashboardData.exited}</p>
                </div>
                <div className="metric-card">
                  <h4>Avg Attendance</h4>
                  <p className="metric-value">{dashboardData.average_attendance.toFixed(1)}%</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'sessions' && (
            <div className="tab-content">
              <h3>Sessions & Schedule</h3>
              <div className="session-list">
                <p>Session management features coming soon...</p>
                <button className="btn btn-primary">+ Schedule New Session</button>
                <button className="btn btn-secondary">View Calendar</button>
              </div>
            </div>
          )}

          {activeTab === 'progress' && (
            <div className="tab-content">
              <h3>Progress Tracking</h3>
              <div className="progress-section">
                <p>Track trainee progress, attendance, and learning completion...</p>
                <button className="btn btn-primary">View Detailed Progress</button>
              </div>
            </div>
          )}

          {activeTab === 'evaluations' && (
            <div className="tab-content">
              <h3>Evaluations</h3>
              <div className="evaluation-section">
                <p>Manage interim, final, and remedial evaluations...</p>
                <button className="btn btn-primary">+ Create Evaluation</button>
                <button className="btn btn-secondary">View Scores</button>
              </div>
            </div>
          )}

          {activeTab === 'documents' && (
            <div className="tab-content">
              <h3>Document Management</h3>
              <div className="document-section">
                <p>Auto-generate and manage documentation...</p>
                <button className="btn btn-primary">+ Generate Document</button>
                <button className="btn btn-secondary">View Templates</button>
                <button className="btn btn-secondary">View Alerts</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
