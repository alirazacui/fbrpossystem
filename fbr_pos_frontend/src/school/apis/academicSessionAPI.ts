import axiosInstance from '@/apis/axiosInstance'

export interface AcademicSession {
  id: string
  tennant_id: number
  name: string
  start_date: string
  end_date: string
  is_active: boolean
}

export interface AcademicSessionPayload {
  name: string
  start_date: string
  end_date: string
  is_active?: boolean
}

export const academicSessionAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: AcademicSession[]; count: number }>('/academic-sessions/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<AcademicSession>(`/academic-sessions/${id}/`),

  create: (payload: AcademicSessionPayload) =>
    axiosInstance.post<AcademicSession>('/academic-sessions/', payload),

  update: (id: string, payload: Partial<AcademicSessionPayload>) =>
    axiosInstance.patch<AcademicSession>(`/academic-sessions/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/academic-sessions/${id}/`),
}
