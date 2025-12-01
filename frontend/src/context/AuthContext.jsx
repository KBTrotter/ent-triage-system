import { createContext, useContext, useState, useEffect } from "react";
import apiClient from "../api/axios";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // to prevent flash
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  // Load user on mount if token exists
  useEffect(() => {
    const fetchUser = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const response = await apiClient.get("/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUser(response.data);
      } catch (err) {
        setUser(null);
        localStorage.removeItem("token");
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [token]);

  // Login: fetch user info before storing token
  const login = async (accessToken) => {
    try {
      const response = await apiClient.get("/auth/me", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      localStorage.setItem("token", accessToken);
      setToken(accessToken);
      setUser(response.data);
    } catch (err) {
      setUser(null);
      localStorage.removeItem("token");
      setToken(null);
    }
  };

  // Logout
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
