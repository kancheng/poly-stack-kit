import axios from 'axios';

const base = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const normalizedBase = String(base).replace(/\/$/, '');
const TOKEN_KEY = 'polystack_token';
const TOKEN_BASE_KEY = 'polystack_token_base';

export const api = axios.create({
  baseURL: `${normalizedBase}/api`,
});

if (localStorage.getItem(TOKEN_BASE_KEY) !== normalizedBase) {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.setItem(TOKEN_BASE_KEY, normalizedBase);
}

api.interceptors.request.use((config) => {
  const t = localStorage.getItem(TOKEN_KEY);
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
