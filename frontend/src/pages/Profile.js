import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';

export default function Profile() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchProfile();
  }, [token, navigate]);

  const fetchProfile = async () => {
    try {
      const res = await authService.getProfile(token);
      setUser(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (!user) return <div>Loading profile...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h1>My Profile</h1>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Full name:</strong> {user.full_name}</p>
      <p><strong>Role:</strong> {user.role}</p>
    </div>
  );
}
