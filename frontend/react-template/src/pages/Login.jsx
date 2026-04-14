import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, unwrap } from '../api.js';

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState('');

  async function submit(e) {
    e.preventDefault();
    setErr('');
    try {
      const res = await api.post('/auth/login', { email, password });
      const data = unwrap(res);
      localStorage.setItem('polystack_token', data.tokens.access_token);
      nav('/dashboard');
    } catch (e2) {
      setErr(e2.message || 'Login failed');
    }
  }

  return (
    <div className="card" style={{ maxWidth: 420 }}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required autoComplete="username" />
        </div>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Password</label>
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
            autoComplete="current-password"
          />
        </div>
        {err ? <p className="error">{err}</p> : null}
        <button className="primary" type="submit">
          Sign in
        </button>
      </form>
    </div>
  );
}
