import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { api, unwrap } from '../api.js';

export default function TaskEdit() {
  const { id } = useParams();
  const location = useLocation();
  const nav = useNavigate();
  const isNew = useMemo(() => location.pathname.endsWith('/tasks/new'), [location.pathname]);
  const [form, setForm] = useState({
    title: '',
    prompt_body: '',
    description: '',
    is_reusable: true,
  });
  const [err, setErr] = useState('');

  useEffect(() => {
    let cancelled = false;
    async function run() {
      if (isNew) return;
      try {
        const res = await api.get(`/tasks/${id}`);
        const t = unwrap(res);
        if (cancelled) return;
        setForm({
          title: t.title,
          prompt_body: t.prompt_body,
          description: t.description || '',
          is_reusable: !!t.is_reusable,
        });
      } catch (e) {
        if (!cancelled) setErr(e.message || 'Load failed');
      }
    }
    run();
    return () => {
      cancelled = true;
    };
  }, [id, isNew]);

  async function save(e) {
    e.preventDefault();
    setErr('');
    try {
      if (isNew) {
        const res = await api.post('/tasks', { ...form });
        const t = unwrap(res);
        nav(`/tasks/${t.id}`, { replace: true });
      } else {
        await api.put(`/tasks/${id}`, { ...form });
        nav('/dashboard');
      }
    } catch (e2) {
      setErr(e2.message || 'Save failed');
    }
  }

  return (
    <div className="card">
      <h2>{isNew ? 'New task' : 'Edit task'}</h2>
      <form onSubmit={save}>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Title</label>
          <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        </div>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Prompt body</label>
          <textarea
            rows={8}
            value={form.prompt_body}
            onChange={(e) => setForm({ ...form, prompt_body: e.target.value })}
            required
          />
        </div>
        <div style={{ marginBottom: '0.75rem' }}>
          <label>Description</label>
          <textarea rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        </div>
        <label className="row" style={{ gap: '0.5rem', marginBottom: '0.75rem' }}>
          <input
            type="checkbox"
            checked={form.is_reusable}
            onChange={(e) => setForm({ ...form, is_reusable: e.target.checked })}
          />
          Reusable prompt
        </label>
        {err ? <p className="error">{err}</p> : null}
        <button className="primary" type="submit">
          Save
        </button>
        <Link to="/dashboard" style={{ marginLeft: '0.5rem' }}>
          Cancel
        </Link>
      </form>
    </div>
  );
}
