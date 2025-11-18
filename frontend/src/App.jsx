import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AdminPortal from "./pages/AdminPortal.jsx";


function App() {
  return (
    <AuthProvider>
      <Router>

        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />

          <Route path="/login" element={<Login />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin"
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminPortal />
              </ProtectedRoute>
            }
          />
        </Routes>
        
      </Router>
    </AuthProvider>
  );
}

export default App;
