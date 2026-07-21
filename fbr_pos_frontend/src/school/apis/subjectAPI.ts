import axiosInstance from '@/apis/axiosInstance'

export interface Subject {
  id: string
  tennant_id: number
  name: string
  description: string | null
  code: string | null
}

export interface SubjectPayload {
  name: string
  description?: string
  code?: string
}

export const subjectAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Subject[]; count: number }>('/school/subjects/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Subject>(`/school/subjects/${id}/`),

  create: (payload: SubjectPayload) =>
    axiosInstance.post<Subject>('/school/subjects/', payload),

  update: (id: string, payload: Partial<SubjectPayload>) =>
    axiosInstance.patch<Subject>(`/school/subjects/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/subjects/${id}/`),
}
