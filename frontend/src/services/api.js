import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance
const apiClient = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth token management
let authToken = localStorage.getItem('authToken');

// Add auth token to requests if available
apiClient.interceptors.request.use((config) => {
  if (authToken) {
    config.headers.Authorization = `Bearer ${authToken}`;
  }
  return config;
});

// Handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      authToken = null;
      localStorage.removeItem('authToken');
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login', credentials);
    if (response.data.access_token) {
      authToken = response.data.access_token;
      localStorage.setItem('authToken', authToken);
    }
    return response.data;
  },

  verify: async () => {
    const response = await apiClient.get('/auth/verify');
    return response.data;
  },

  logout: async () => {
    const response = await apiClient.post('/auth/logout');
    authToken = null;
    localStorage.removeItem('authToken');
    return response.data;
  },

  isAuthenticated: () => {
    return !!authToken;
  }
};

// Resume API
export const resumeAPI = {
  // Get complete resume
  getResume: async () => {
    const response = await apiClient.get('/resume');
    return response.data;
  },

  // Update personal information
  updatePersonalInfo: async (personalInfo) => {
    const response = await apiClient.put('/resume/personal-info', personalInfo);
    return response.data;
  },

  // Update highlights
  updateHighlights: async (highlights) => {
    const response = await apiClient.put('/resume/highlights', { highlights });
    return response.data;
  },

  // Update skills
  updateSkills: async (skills) => {
    const response = await apiClient.put('/resume/skills', { skills });
    return response.data;
  },

  // Download PDF
  downloadPDF: async () => {
    const response = await apiClient.get('/resume/download-pdf', {
      responseType: 'blob'
    });
    return response.data;
  }
};

// Experience API
export const experienceAPI = {
  // Get all experiences
  getExperiences: async () => {
    const response = await apiClient.get('/resume/experience');
    return response.data.experiences;
  },

  // Add new experience
  addExperience: async (experience) => {
    const response = await apiClient.post('/resume/experience', experience);
    return response.data;
  },

  // Update experience
  updateExperience: async (id, experience) => {
    const response = await apiClient.put(`/resume/experience/${id}`, experience);
    return response.data;
  },

  // Delete experience
  deleteExperience: async (id) => {
    const response = await apiClient.delete(`/resume/experience/${id}`);
    return response.data;
  }
};

// Education API
export const educationAPI = {
  // Get all education
  getEducation: async () => {
    const response = await apiClient.get('/resume/education');
    return response.data.education;
  },

  // Add new education
  addEducation: async (education) => {
    const response = await apiClient.post('/resume/education', education);
    return response.data;
  },

  // Update education
  updateEducation: async (id, education) => {
    const response = await apiClient.put(`/resume/education/${id}`, education);
    return response.data;
  },

  // Delete education
  deleteEducation: async (id) => {
    const response = await apiClient.delete(`/resume/education/${id}`);
    return response.data;
  }
};

// Contact API
export const contactAPI = {
  // Submit contact form
  submitContact: async (contactData) => {
    const response = await apiClient.post('/contact', contactData);
    return response.data;
  }
};

// Admin API
export const adminAPI = {
  // Get contact messages
  getContactMessages: async (limit = 50) => {
    const response = await apiClient.get(`/admin/contact-messages?limit=${limit}`);
    return response.data.messages;
  },

  // Mark message as read
  markMessageRead: async (messageId) => {
    const response = await apiClient.put(`/admin/contact-messages/${messageId}/read`);
    return response.data;
  }
};

export default {
  auth: authAPI,
  resume: resumeAPI,
  experience: experienceAPI,
  education: educationAPI,
  contact: contactAPI,
  admin: adminAPI
};