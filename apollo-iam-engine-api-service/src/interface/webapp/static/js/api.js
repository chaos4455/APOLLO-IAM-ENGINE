const API_BASE = 'http://localhost:8000';
async function apiRequest(method, path, body = null, token = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Erro na requisicao');
  }
  return res.status === 204 ? null : res.json();
}
function getToken() { return localStorage.getItem('apollo_token'); }
function setToken(t) { localStorage.setItem('apollo_token', t); }
function clearToken() { localStorage.removeItem('apollo_token'); }
