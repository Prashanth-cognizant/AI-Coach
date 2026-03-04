import axios from 'axios';

export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth services
export const authService = {
  register: (userData) => api.post('/api/auth/register', userData),
  // login expects an object { username, password } for convenience
  login: (credentials) => api.post('/api/auth/login', credentials),
  getProfile: (userId) => api.get(`/api/auth/profile/${userId}`),
  updateProfile: (userId, data) => api.put(`/api/auth/profile/${userId}`, data),
};

// Sessions services
export const sessionService = {
  createSession: (sessionData, token) => 
    api.post('/sessions/', sessionData, { params: { token } }),
  // old fitness-specific endpoint removed: /sessions/user does not exist
  getSession: (sessionId, token) => 
    api.get(`/sessions/${sessionId}`, { params: { token } }),
  deleteSession: (sessionId, token) => 
    api.delete(`/sessions/${sessionId}`, { params: { token } }),
};

// Progress services
export const progressService = {
  logProgress: (progressData, token) => 
    api.post('/api/progress/', progressData, { params: { token } }),
  getUserProgress: (token) => 
    api.get('/api/progress/user', { params: { token } }),
  getStats: (token) => 
    api.get('/api/progress/stats', { params: { token } }),
  deleteProgress: (progressId, token) => 
    api.delete(`/api/progress/${progressId}`, { params: { token } }),
};

// Chat services
export const chatService = {
  sendMessage: (payload, token) => 
    api.post('/chat/message', payload, { params: { token } }),
  getChatHistory: (token) => 
    api.get('/chat/history', { params: { token } }),
  deleteMessage: (messageId, token) => 
    api.delete(`/chat/message/${messageId}`, { params: { token } }),
};

export default api;
