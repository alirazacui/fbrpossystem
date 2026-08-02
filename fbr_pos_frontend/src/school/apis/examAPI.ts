import axiosInstance from '@/apis/axiosInstance'

export interface Exam {
  id: string
  name: string
  exam_type_id: string
  academic_session_id: string
  grade_id: string
  section_id: string | null
  start_date: string
  end_date: string | null
  is_active: boolean

  // Related
  exam_type_name?: string
  session_name?: string
  grade_name?: string
  section_name?: string
}

export interface ExamPayload {
  name: string
  exam_type_id: string
  academic_session_id: string
  grade_id: string
  section_id?: string
  start_date: string
  end_date?: string
  is_active?: boolean
}

export const examAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Exam[]; count: number }>('/exams/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Exam>(`/exams/${id}/`),

  create: (payload: ExamPayload) =>
    axiosInstance.post<Exam>('/exams/', payload),

  update: (id: string, payload: Partial<ExamPayload>) =>
    axiosInstance.patch<Exam>(`/exams/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/exams/${id}/`),
}
