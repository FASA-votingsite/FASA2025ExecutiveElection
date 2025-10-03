import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Add token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
};

// Elections API - Only positions endpoint (includes candidates)
export const electionsAPI = {
  getElections: () => api.get('/elections/'),
  getPositions: () => api.get('/elections/positions/'),
  // REMOVED: getCandidates - not needed since positions include candidates
};

// Votes API
export const votesAPI = {
  castVote: (voteData) => api.post('/votes/cast/', voteData),
  getMyVotes: () => api.get('/votes/'),
  getResults: () => api.get('/votes/results/'),
};

export default api;