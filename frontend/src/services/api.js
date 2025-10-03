import axios from 'axios';

// Use HTTP for development
const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`Response received: ${response.status}`);
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
};

// Elections API
export const electionsAPI = {
  getElections: () => api.get('/elections/'),
  getPositions: () => api.get('/elections/positions/'),
  getCandidates: () => api.get('/elections/candidates/'),
};

// Votes API
export const votesAPI = {
  castVote: (voteData) => api.post('/votes/cast/', voteData),
  getMyVotes: () => api.get('/votes/'),
  getResults: () => api.get('/votes/results/'),
};

export default api;