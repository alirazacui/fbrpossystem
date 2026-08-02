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
    axiosInstance.get<{ results: Attendance[]; count: number }>('/attendance/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Attendance>(`/attendance/${id}/`),

  create: (payload: AttendancePayload) =>
    axiosInstance.post<Attendance>('/attendance/', payload),

  update: (id: string, payload: Partial<AttendancePayload>) =>
    axiosInstance.patch<Attendance>(`/attendance/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/attendance/${id}/`),
    
  bulkMark: (payload: { date: string, section_id: string, attendances: any[] }) =>
    axiosInstance.post<{ message: string, created: number, updated: number }>('/attendance/bulk-mark/', payload),
}
