import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, unwrap } from '../api.js';

export default function Dashboard() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState('');

  async function load() {
    setLoading(true);
    setErr('');
    try {
      const res = await api.get('/tasks');
      const data = unwrap(res);
      setItems(data.items || []);
    } catch (e) {
      setErr(e.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }

  async function remove(id) {
    if (!confirm('Delete this task?')) return;
    try {
      await api.delete(`/tasks/${id}`);
      await load();
    } catch (e) {
      setErr(e.message || 'Delete failed');
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <div className="row" style={{ justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h2 style={{ margin: 0 }}>Tasks</h2>
        <Link to="/tasks/new">
          <button className="primary" type="button">
            New task
          </button>
        </Link>
      </div>
      {loading ? <p className="muted">Loading…</p> : null}
      {err ? <p className="error">{err}</p> : null}
      {!loading && !items.length ? <div className="card muted">No tasks yet.</div> : null}
      {items.map((t) => (
        <div key={t.id} className="card">
          <div className="row" style={{ justifyContent: 'space-between' }}>
            <div>
              <strong>{t.title}</strong>
              {t.is_reusable ? <span className="muted"> · reusable</span> : null}
            </div>
            <div className="row">
              <Link to={`/tasks/${t.id}`}>Edit</Link>
              <button type="button" onClick={() => remove(t.id)}>
                Delete
              </button>
            </div>
          </div>
          <p className="muted" style={{ margin: '0.5rem 0 0' }}>
            {(t.prompt_body || '').slice(0, 200)}
            {(t.prompt_body || '').length > 200 ? '…' : ''}
          </p>
        </div>
      ))}
    </div>
  );
}
