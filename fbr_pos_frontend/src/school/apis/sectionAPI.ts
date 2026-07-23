import axiosInstance from '@/apis/axiosInstance'

export interface Section {
  id: string
  grade_id: string
  academic_session_id: string
  name: string
  room_number: string | null
  class_teacher_id: string | null
  capacity: number | null
  // Related fields (if returned by backend)
  grade_name?: string
  session_name?: string
  teacher_name?: string
}

export interface SectionPayload {
  grade_id: string
  academic_session_id: string
  name: string
  room_number?: string
  class_teacher_id?: string
  capacity?: number
}

export const sectionAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Section[]; count: number }>('/sections/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Section>(`/sections/${id}/`),

  create: (payload: SectionPayload) =>
    axiosInstance.post<Section>('/sections/', payload),

  update: (id: string, payload: Partial<SectionPayload>) =>
    axiosInstance.patch<Section>(`/sections/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/sections/${id}/`),
}
