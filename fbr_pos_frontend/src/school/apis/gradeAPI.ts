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
    axiosInstance.get<{ results: Grade[]; count: number }>('/school/grades/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Grade>(`/school/grades/${id}/`),

  create: (payload: GradePayload) =>
    axiosInstance.post<Grade>('/school/grades/', payload),

  update: (id: string, payload: Partial<GradePayload>) =>
    axiosInstance.patch<Grade>(`/school/grades/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/grades/${id}/`),
}
