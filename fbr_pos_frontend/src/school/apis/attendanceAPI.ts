import axiosInstance from '@/apis/axiosInstance'

export interface Attendance {
  id: string
  student_id: string
  date: string
  status: 'present' | 'absent'
  enrollement_id: string
  marked_by?: string | null

  // Virtual/Serializer fields
  student_name?: string
  staff_name?: string
}

export interface AttendancePayload {
  student_id: string
  date: string
  status: 'present' | 'absent'
  enrollement_id: string
  marked_by?: string | null
}

export const attendanceAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Attendance[]; count: number }>('/school/attendances/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Attendance>(`/school/attendances/${id}/`),

  create: (payload: AttendancePayload) =>
    axiosInstance.post<Attendance>('/school/attendances/', payload),

  update: (id: string, payload: Partial<AttendancePayload>) =>
    axiosInstance.patch<Attendance>(`/school/attendances/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/attendances/${id}/`),
}
