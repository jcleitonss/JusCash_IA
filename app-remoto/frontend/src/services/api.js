import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    console.log(`[API] Response:`, response.status);
    return response;
  },
  (error) => {
    console.error(`[API] Error:`, error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export const verificarProcesso = async (processo) => {
  const response = await api.post('/api/v1/verificar', processo);
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
