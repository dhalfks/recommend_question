import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const getApiUrl = () => API_URL;

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = window.localStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export type UserRole = 'STUDENT' | 'PROFESSOR' | 'ADMIN';

export type AuthUser = {
  id: number;
  name: string;
  phone: string;
  email: string;
  role: UserRole;
};

export const authAPI = {
  register: (data: {
    name: string;
    phone: string;
    email: string;
    password: string;
    role: UserRole;
    admin_signup_code?: string;
  }) => api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
  updateMe: (data: {
    name?: string;
    phone?: string;
    email?: string;
    current_password?: string;
    new_password?: string;
  }) => api.put('/auth/me', data),
};

// 과목 API
export const subjectsAPI = {
  getAll: () => api.get('/subjects'),
  getById: (id: number) => api.get(`/subjects/${id}`),
  create: (data: any) => api.post('/subjects', data),
  update: (id: number, data: any) => api.put(`/subjects/${id}`, data),
  delete: (id: number) => api.delete(`/subjects/${id}`),
};

// 문제 API
export const questionsAPI = {
  getAll: (params?: any) => api.get('/questions', { params }),
  getById: (id: number) => api.get(`/questions/${id}`),
  create: (data: any) => api.post('/questions', data),
  update: (id: number, data: any) => api.put(`/questions/${id}`, data),
  delete: (id: number) => api.delete(`/questions/${id}`),
  getSubjectUnits: (subjectId: number) =>
    api.get('/questions/subject-units', { params: { subject_id: subjectId } }),
  getRandomQuestions: (data: any) => api.post('/questions/random/quiz', data),
  getDifficultyStats: (params?: any) => api.get('/questions/stats/difficulty', { params }),
};

export const progressAPI = {
  submit: (data: {
    session_id: string;
    total_seconds: number;
    answers: Array<{
      question_id: number;
      answer: number | string | null;
      sequence_number: number;
      elapsed_seconds: number;
    }>;
  }) => api.post('/progress/submit', data),
  dashboard: () => api.get('/progress/dashboard'),
  questionAnalytics: (params?: Record<string, string | number>) =>
    api.get('/progress/question-analytics', { params }),
  questionAnalyticsDetail: (questionId: number) =>
    api.get(`/progress/question-analytics/${questionId}`),
  studentAnalytics: (params?: Record<string, string | number>) =>
    api.get('/progress/student-analytics', { params }),
  studentAnalyticsDetail: (studentId: number) =>
    api.get(`/progress/student-analytics/${studentId}`),
};

export const recommendationsAPI = {
  getQuiz: (params: { count: number; subject_id?: number }) =>
    api.get('/recommendations/quiz', { params }),
  getPeerMissed: (params?: { count?: number; subject_id?: number }) =>
    api.get('/recommendations/peer-missed', { params }),
  getPeerMissedUnits: (params?: { count?: number; subject_id?: number }) =>
    api.get('/recommendations/peer-missed-units', { params }),
  getMyWrong: (params?: { count?: number }) =>
    api.get('/recommendations/my-wrong', { params }),
};

// 파일 API
export const filesAPI = {
  excelTemplateUrl: () => `${API_URL}/files/template/excel`,
  uploadExcel: (file: File, subjectId: number) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('subject_id', subjectId.toString());
    return api.post('/files/upload/excel', formData, {
      timeout: 120000,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  uploadCode: (file: File, subjectId: number, autoGenerate: boolean = true) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('subject_id', subjectId.toString());
    formData.append('auto_generate', autoGenerate.toString());
    return api.post('/files/upload/code', formData, {
      timeout: 120000,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  list: (params?: any) => api.get('/files/list', { params }),
  delete: (id: number) => api.delete(`/files/${id}`),
};

export default api;
