import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children, requiredRole }) {
  const { user } = useAuth();

  //if no user is logged in, redirect to login
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  //if user is not admin and route requires admin, redirect to dashboard
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}
