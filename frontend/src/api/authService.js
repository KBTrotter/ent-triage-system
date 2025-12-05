let accessToken = null; // store in memory (safe)

export const authService = {
  setAccessToken: (t) => (accessToken = t),
  getAccessToken: () => accessToken,

  async refreshToken() {
    const res = await fetch("http://localhost:8000/auth/refresh", {
      method: "POST",
      credentials: "include"
    });

    if (!res.ok) throw new Error("Refresh failed");

    const data = await res.json();
    accessToken = data.access_token;
    return accessToken;
  },

  logout() {
    accessToken = null;
  }
};
