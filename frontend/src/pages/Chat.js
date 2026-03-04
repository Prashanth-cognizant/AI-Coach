import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { chatService } from '../services/api';

export default function Chat() {
  const [message, setMessage] = useState('');
  const [history, setHistory] = useState([]);
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  if (!token) {
    navigate('/login');
    return null;
  }

  const sendMessage = async () => {
    if (!message) return;
    try {
      const res = await chatService.sendMessage({ message, message_type: 'query' }, token);
      setHistory(prev => [...prev, { user: message, bot: res.data.response }]);
      setMessage('');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>AI Coach Chat</h1>
      <div style={{ maxHeight: '300px', overflowY: 'auto', marginBottom: '1rem' }}>
        {history.map((h, i) => (
          <div key={i}>
            <strong>You:</strong> {h.user}
            <br />
            <strong>Coach:</strong> {h.bot}
            <hr />
          </div>
        ))}
      </div>
      <input
        value={message}
        onChange={e => setMessage(e.target.value)}
        style={{ width: '80%' }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
