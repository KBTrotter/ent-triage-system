import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000",
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      throw new Error(data?.message || `Request failed with status ${status}`);
    } else if (error.request) {
      throw new Error('Unable to reach server');
    } else {
      throw error;
    }
  }
);

export default apiClient;
