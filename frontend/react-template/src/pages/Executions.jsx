import { useEffect, useState } from 'react';
import { api, unwrap } from '../api.js';

export default function Executions() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState('');
  const [taskFilter, setTaskFilter] = useState('');

  async function load() {
    setLoading(true);
    setErr('');
    try {
      const params = {};
      if (taskFilter) params.task_id = Number(taskFilter);
      const res = await api.get('/executions', { params });
      const data = unwrap(res);
      setItems(data.items || []);
    } catch (e) {
      setErr(e.message || 'Failed to load');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <h2>Executions</h2>
      <div className="row" style={{ marginBottom: '0.75rem' }}>
        <label style={{ margin: 0 }}>Filter task id</label>
        <input
          style={{ maxWidth: 120 }}
          type="number"
          min={1}
          value={taskFilter}
          onChange={(e) => setTaskFilter(e.target.value)}
        />
        <button type="button" onClick={load}>
          Apply
        </button>
      </div>
      {loading ? <p className="muted">Loading…</p> : null}
      {err ? <p className="error">{err}</p> : null}
      {!loading && !items.length ? <div className="card muted">No executions.</div> : null}
      {items.map((e) => (
        <div key={e.id} className="card">
          <div className="muted">
            #{e.id} · task {e.task_id} · {e.created_at}
          </div>
          <p>
            <strong>Input</strong>
          </p>
          <pre style={{ margin: '0 0 0.5rem' }}>{e.input_payload}</pre>
          <p>
            <strong>Output</strong>
          </p>
          <pre style={{ margin: 0 }}>{e.output_payload}</pre>
        </div>
      ))}
    </div>
  );
}
