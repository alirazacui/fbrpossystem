import axiosInstance from '@/apis/axiosInstance'

export interface Grade {
  id: string
  tennant_id: number
  name: string
  description: string | null
  sort: number
}

export interface GradePayload {
  name: string
  description?: string
  sort?: number
}

export const gradeAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Grade[]; count: number }>('/grades/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Grade>(`/grades/${id}/`),

  create: (payload: GradePayload) =>
    axiosInstance.post<Grade>('/grades/', payload),

  update: (id: string, payload: Partial<GradePayload>) =>
    axiosInstance.patch<Grade>(`/grades/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/grades/${id}/`),
}
