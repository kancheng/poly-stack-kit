import axios from 'axios';

const base = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const api = axios.create({
  baseURL: `${String(base).replace(/\/$/, '')}/api`,
});

api.interceptors.request.use((config) => {
  const t = localStorage.getItem('polystack_token');
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

export function unwrap(res) {
  const d = res.data;
  if (!d || d.success !== true) {
    const msg = d?.message || 'Request failed';
    const err = new Error(msg);
    err.details = d?.error;
    throw err;
  }
  return d.data;
}
