import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, unwrap } from '../api.js';

export default function Register() {
  const nav = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState('');

  async function submit(e) {
    e.preventDefault();
    setErr('');
    try {
      const res = await api.post('/auth/register', { name, email, password });
      const data = unwrap(res);
      localStorage.setItem('polystack_token', data.tokens.access_token);
      nav('/dashboard');
    } catch (e2) {
      setErr(e2.message || 'Register failed');
    }
  }

  return (
    <div className="card" style={{ maxWidth: 420 }}>
      <h2>Register</h2>
      <form onSubmit={submit}>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required autoComplete="email" />
        </div>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Password (min 8)</label>
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
            minLength={8}
            autoComplete="new-password"
          />
        </div>
        {err ? <p className="error">{err}</p> : null}
        <button className="primary" type="submit">
          Create account
        </button>
      </form>
    </div>
  );
}
