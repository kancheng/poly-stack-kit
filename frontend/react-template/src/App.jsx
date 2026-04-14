import { Link, Navigate, Route, Routes, useNavigate } from 'react-router-dom';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Dashboard from './pages/Dashboard.jsx';
import TaskEdit from './pages/TaskEdit.jsx';
import Executions from './pages/Executions.jsx';

function Shell({ children }) {
  const token = localStorage.getItem('polystack_token');
  const nav = useNavigate();
  return (
    <div className="layout">
      <header className="row" style={{ justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div>
          <strong>PolyStack React</strong>
          <span className="muted"> — AI Prompt Task Hub</span>
        </div>
        {token ? (
          <nav className="row">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/executions">Executions</Link>
            <button
              type="button"
              onClick={() => {
                localStorage.removeItem('polystack_token');
                nav('/login');
              }}
            >
              Logout
            </button>
          </nav>
        ) : (
          <nav className="row">
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </nav>
        )}
      </header>
      {children}
    </div>
  );
}

function Private({ children }) {
  const token = localStorage.getItem('polystack_token');
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <Shell>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <Private>
              <Dashboard />
            </Private>
          }
        />
        <Route
          path="/tasks/new"
          element={
            <Private>
              <TaskEdit />
            </Private>
          }
        />
        <Route
          path="/tasks/:id"
          element={
            <Private>
              <TaskEdit />
            </Private>
          }
        />
        <Route
          path="/executions"
          element={
            <Private>
              <Executions />
            </Private>
          }
        />
      </Routes>
    </Shell>
  );
}
