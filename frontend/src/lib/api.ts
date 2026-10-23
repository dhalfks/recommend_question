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
  affiliation?: string | null;
  academic_year?: number | null;
  course_name?: string | null;
  professor_id?: number | null;
};

export type BillingPlan = {
  id: number;
  code: 'STUDENT_PRO' | 'TEACHER_PRO';
  name: string;
  audience_role: 'STUDENT' | 'PROFESSOR';
  price: number;
  currency: 'KRW';
  billing_period: 'ONE_TIME' | 'MONTHLY';
  entitlement_days: number;
  features: Record<string, { daily_limit: number }>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type BillingOrder = {
  order_id: string;
  order_name: string;
  amount: number;
  currency: 'KRW';
  status: 'READY' | 'PAID' | 'FAILED' | 'CANCELED' | 'REFUNDED';
  created_at: string;
  customer_key?: string | null;
};

export type FeatureEntitlement = {
  daily_limit: number | null;
  used_today: number;
  remaining_today: number | null;
  is_available: boolean;
};

export type BillingMe = {
  plan_code: string;
  plan_name: string;
  subscription?: {
    id: number;
    plan_code: string;
    plan_name: string;
    status: 'ACTIVE';
    current_period_start: string;
    current_period_end: string;
  } | null;
  features: Record<string, FeatureEntitlement>;
};

export type BillingPayment = {
  order_id: string;
  plan_code: string;
  plan_name: string;
  amount: number;
  currency: 'KRW';
  status: 'READY' | 'PAID' | 'FAILED' | 'CANCELED' | 'REFUNDED';
  created_at: string;
  paid_at?: string | null;
};

export type AdminBillingPayment = BillingPayment & {
  user_id: number;
  user_name: string;
  user_email: string;
  user_role: UserRole;
  can_close: boolean;
  can_recover: boolean;
};

export type ProfessorOption = {
  id: number;
  name: string;
  affiliation?: string | null;
  course_name?: string | null;
};

export type QuestionBankQuestion = {
  id: number;
  subject_id: number;
  professor_id?: number | null;
  question_type: 'EXCEL' | 'CODE';
  title: string;
  content: string;
  answer_type: 'MULTIPLE_CHOICE' | 'SUBJECTIVE' | 'CODE_INPUT';
  difficulty: 'EASY' | 'MEDIUM' | 'HARD' | 'EXPERT';
  options?: string | null;
  correct_answer?: string | null;
  correct_option?: number | null;
  explanation?: string | null;
  code_snippet?: string | null;
  answer_code_snippet?: string | null;
  subject_unit?: string | null;
  is_required: boolean;
};

export type ExamPaperItem = {
  id: number;
  question_id: number;
  display_order: number;
  subject_id: number;
  subject_name: string;
  title: string;
  content: string;
  answer_type: 'MULTIPLE_CHOICE' | 'SUBJECTIVE' | 'CODE_INPUT';
  options?: string[] | null;
  code_snippet?: string | null;
  correct_answer?: string | null;
  correct_option?: number | null;
  explanation?: string | null;
};

export type ExamPaper = {
  id: number;
  title: string;
  description?: string | null;
  created_at: string;
  updated_at: string;
  items: ExamPaperItem[];
};

export type ExamPaperSummary = Omit<ExamPaper, 'items'> & { item_count: number };

export type PublicExam = {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type PublicExamRound = {
  id: number;
  exam_id: number;
  exam_year: number;
  round_identifier: string;
  display_name?: string | null;
  held_on?: string | null;
  is_published: boolean;
  created_at: string;
  updated_at: string;
};

export type PublicExamSubject = {
  id: number;
  round_id: number;
  code?: string | null;
  name: string;
  display_order: number;
  created_at: string;
  updated_at: string;
};

export type PublicExamQuestion = {
  id: number;
  subject_id: number;
  question_number: number;
  content: string;
  options?: string[] | null;
  question_type: 'MULTIPLE_CHOICE' | 'SHORT_ANSWER';
};

export type PublicExamQuestionAdmin = PublicExamQuestion & {
  source_document_id?: number | null;
  correct_option?: number | null;
  correct_answer?: string | null;
  explanation?: string | null;
  source_page?: number | null;
  answer_verification_status: 'MISSING' | 'UNVERIFIED' | 'VERIFIED';
  publication_status: 'DRAFT' | 'READY' | 'PUBLISHED' | 'ARCHIVED';
  review_notes?: string | null;
  created_at: string;
  updated_at: string;
};

export type PublicExamSourceDocument = {
  id: number;
  round_id: number;
  original_file_name: string;
  source_url?: string | null;
  source_organization?: string | null;
  source_notes?: string | null;
  sha256?: string | null;
  uploaded_by: number;
  uploaded_at: string;
  question_count: number;
  verified_count: number;
  published_count: number;
};

export type PublicExamSourceDocumentDetail = PublicExamSourceDocument & {
  questions: PublicExamQuestionAdmin[];
  extraction_message?: string;
};

export type PublicExamAttemptAnswer = {
  question: PublicExamQuestion;
  sequence_number: number;
  selected_option?: number | null;
  written_answer?: string | null;
  elapsed_seconds: number;
  answered_at?: string | null;
};

export type PublicExamAttempt = {
  id: string;
  subject_id: number;
  status: 'IN_PROGRESS' | 'SUBMITTED' | 'ABANDONED';
  started_at: string;
  last_activity_at: string;
  total_questions: number;
  answers: PublicExamAttemptAnswer[];
};

export type PublicExamResultItem = {
  question_id: number;
  sequence_number: number;
  question_number: number;
  content: string;
  options?: string[] | null;
  question_type: 'MULTIPLE_CHOICE' | 'SHORT_ANSWER';
  selected_option?: number | null;
  written_answer?: string | null;
  correct_option?: number | null;
  correct_answer?: string | null;
  explanation?: string | null;
  elapsed_seconds: number;
  is_correct: boolean;
};

export type PublicExamResult = {
  attempt_id: string;
  exam_name: string;
  exam_year: number;
  round_identifier: string;
  subject_name: string;
  status: 'SUBMITTED';
  started_at: string;
  submitted_at: string;
  total_elapsed_seconds: number;
  total_questions: number;
  correct_answers: number;
  incorrect_answers: number;
  score_percent: number;
  items: PublicExamResultItem[];
};

export const authAPI = {
  register: (data: {
    name: string;
    phone: string;
    email: string;
    password: string;
    role: UserRole;
    affiliation?: string;
    academic_year?: number;
    course_name?: string;
    professor_id?: number;
    admin_signup_code?: string;
  }) => api.post('/auth/register', data),
  professors: () => api.get<ProfessorOption[]>('/auth/professors'),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
  updateMe: (data: {
    name?: string;
    phone?: string;
    email?: string;
    current_password?: string;
    new_password?: string;
    affiliation?: string;
    academic_year?: number;
    course_name?: string;
  }) => api.put('/auth/me', data),
};

export const billingAPI = {
  plans: () => api.get<BillingPlan[]>('/billing/plans'),
  me: () => api.get<BillingMe>('/billing/me'),
  payments: () => api.get<BillingPayment[]>('/billing/payments'),
  adminPayments: (status?: BillingPayment['status']) =>
    api.get<AdminBillingPayment[]>('/billing/admin/payments', { params: status ? { status } : undefined }),
  closeAdminPayment: (orderId: string) =>
    api.post(`/billing/admin/payments/${encodeURIComponent(orderId)}/close`),
  recoverAdminPayment: (orderId: string) =>
    api.post(`/billing/admin/payments/${encodeURIComponent(orderId)}/recover`, undefined, { timeout: 30000 }),
  refundAdminPayment: (orderId: string, reason: string) =>
    api.post(`/billing/admin/payments/${encodeURIComponent(orderId)}/refund`, { reason }, { timeout: 30000 }),
  createOrder: (planCode: string) =>
    api.post<BillingOrder>('/billing/orders', { plan_code: planCode }),
  confirm: (data: { payment_key: string; order_id: string; amount: number }) =>
    api.post('/billing/payments/confirm', data, { timeout: 30000 }),
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
  getAll: (params?: any) => api.get<QuestionBankQuestion[]>('/questions', { params }),
  getById: (id: number) => api.get(`/questions/${id}`),
  create: (data: any) => api.post('/questions', data),
  update: (id: number, data: any) => api.put(`/questions/${id}`, data),
  delete: (id: number) => api.delete(`/questions/${id}`),
  getSubjectUnits: (subjectId: number) =>
    api.get('/questions/subject-units', { params: { subject_id: subjectId } }),
  getRandomQuestions: (data: any) => api.post('/questions/random/quiz', data),
  getDifficultyStats: (params?: any) => api.get('/questions/stats/difficulty', { params }),
};

export const examPapersAPI = {
  list: () => api.get<ExamPaperSummary[]>('/exam-papers'),
  get: (paperId: number) => api.get<ExamPaper>(`/exam-papers/${paperId}`),
  create: (data: { title: string; description?: string | null; question_ids: number[] }) =>
    api.post<ExamPaper>('/exam-papers', data),
  update: (paperId: number, data: { title: string; description?: string | null; question_ids: number[] }) =>
    api.put<ExamPaper>(`/exam-papers/${paperId}`, data),
  delete: (paperId: number) => api.delete(`/exam-papers/${paperId}`),
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
  }) => api.post('/progress/submit', data, { timeout: 120000 }),
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

export const publicExamsAPI = {
  getExams: () => api.get<PublicExam[]>('/public-exams'),
  getRounds: (examId: number) =>
    api.get<PublicExamRound[]>(`/public-exams/${examId}/rounds`),
  getSubjects: (roundId: number) =>
    api.get<PublicExamSubject[]>(`/public-exams/rounds/${roundId}/subjects`),
  startAttempt: (subjectId: number) =>
    api.post<PublicExamAttempt>(`/public-exams/subjects/${subjectId}/attempts`),
  getInProgressAttempts: (subjectId?: number) =>
    api.get<PublicExamAttempt[]>('/public-exams/attempts/in-progress', {
      params: subjectId ? { subject_id: subjectId } : undefined,
    }),
  getAttempt: (attemptId: string) =>
    api.get<PublicExamAttempt>(`/public-exams/attempts/${attemptId}`),
  saveAnswer: (
    attemptId: string,
    questionId: number,
    data: {
      selected_option: number | null;
      written_answer: string | null;
      elapsed_seconds: number;
    },
  ) => api.put<PublicExamAttemptAnswer>(
    `/public-exams/attempts/${attemptId}/answers/${questionId}`,
    data,
  ),
  submitAttempt: (attemptId: string) =>
    api.post<PublicExamResult>(`/public-exams/attempts/${attemptId}/submit`),
  getResult: (attemptId: string) =>
    api.get<PublicExamResult>(`/public-exams/attempts/${attemptId}/result`),
  getWrongAnswers: (attemptId: string) =>
    api.get<{ attempt_id: string; items: PublicExamResultItem[] }>(
      `/public-exams/attempts/${attemptId}/wrong-answers`,
    ),
  adminGetExams: () => api.get<PublicExam[]>('/public-exams/admin/exams'),
  adminGetRounds: (examId: number) =>
    api.get<PublicExamRound[]>(`/public-exams/admin/exams/${examId}/rounds`),
  adminGetSubjects: (roundId: number) =>
    api.get<PublicExamSubject[]>(`/public-exams/admin/rounds/${roundId}/subjects`),
  adminCreateExam: (data: { code: string; name: string; description?: string; is_active: boolean }) =>
    api.post<PublicExam>('/public-exams', data),
  adminUpdateExam: (examId: number, data: Partial<Pick<PublicExam, 'code' | 'name' | 'description' | 'is_active'>>) =>
    api.put<PublicExam>(`/public-exams/${examId}`, data),
  adminCreateRound: (examId: number, data: { exam_year: number; round_identifier: string; display_name?: string; is_published: boolean }) =>
    api.post<PublicExamRound>(`/public-exams/${examId}/rounds`, data),
  adminUpdateRound: (roundId: number, data: Partial<Pick<PublicExamRound, 'exam_year' | 'round_identifier' | 'display_name' | 'held_on' | 'is_published'>>) =>
    api.put<PublicExamRound>(`/public-exams/rounds/${roundId}`, data),
  adminCreateSubject: (roundId: number, data: { code?: string; name: string; display_order: number }) =>
    api.post<PublicExamSubject>(`/public-exams/rounds/${roundId}/subjects`, data),
  adminUpdateSubject: (subjectId: number, data: Partial<Pick<PublicExamSubject, 'code' | 'name' | 'display_order'>>) =>
    api.put<PublicExamSubject>(`/public-exams/subjects/${subjectId}`, data),
  adminGetDocuments: (roundId?: number) => api.get<PublicExamSourceDocument[]>(
    '/public-exams/admin/documents', { params: roundId ? { round_id: roundId } : undefined },
  ),
  adminGetDocument: (documentId: number) =>
    api.get<PublicExamSourceDocumentDetail>(`/public-exams/admin/documents/${documentId}`),
  adminUploadDocument: (subjectId: number, data: FormData) =>
    api.post<PublicExamSourceDocumentDetail>(`/public-exams/admin/subjects/${subjectId}/documents`, data, {
      headers: { 'Content-Type': 'multipart/form-data' }, timeout: 120000,
    }),
  adminOpenDocument: (documentId: number) =>
    api.get<Blob>(`/public-exams/admin/documents/${documentId}/file`, { responseType: 'blob' }),
  adminUpdateQuestion: (questionId: number, data: Partial<PublicExamQuestionAdmin>) =>
    api.put<PublicExamQuestionAdmin>(`/public-exams/questions/${questionId}`, data),
  adminPublishDocument: (documentId: number) =>
    api.post<{ document_id: number; published_count: number }>(`/public-exams/admin/documents/${documentId}/publish`),
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
