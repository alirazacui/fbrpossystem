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
    axiosInstance.get<{ results: Subject[]; count: number }>('/subjects/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Subject>(`/subjects/${id}/`),

  create: (payload: SubjectPayload) =>
    axiosInstance.post<Subject>('/subjects/', payload),

  update: (id: string, payload: Partial<SubjectPayload>) =>
    axiosInstance.patch<Subject>(`/subjects/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/subjects/${id}/`),
}
