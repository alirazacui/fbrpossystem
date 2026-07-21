import axiosInstance from '@/apis/axiosInstance'

export interface ExamType {
  id: string
  name: string
  description: string | null
  max_marks: number
  passing_marks: number | null
}

export interface ExamTypePayload {
  name: string
  description?: string
  max_marks: number
  passing_marks?: number
}

export const examTypeAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: ExamType[]; count: number }>('/school/exam-types/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<ExamType>(`/school/exam-types/${id}/`),

  create: (payload: ExamTypePayload) =>
    axiosInstance.post<ExamType>('/school/exam-types/', payload),

  update: (id: string, payload: Partial<ExamTypePayload>) =>
    axiosInstance.patch<ExamType>(`/school/exam-types/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/exam-types/${id}/`),
}
