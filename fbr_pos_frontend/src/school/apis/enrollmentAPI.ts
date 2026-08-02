import axiosInstance from '@/apis/axiosInstance'

export interface Enrollment {
  id: string
  student_id: string
  section_id: string
  academic_session_id: string
  grade_id: string
  enrollment_date: string
  status: 'ongoing' | 'promoted' | 'repeated' | 'left'
  student_registration_number: string | null
  
  // Related
  student_name?: string
  section_name?: string
  session_name?: string
  grade_name?: string
}

export interface EnrollmentPayload {
  student_id: string
  section_id: string
  academic_session_id: string
  grade_id: string
  enrollment_date?: string
  status?: 'ongoing' | 'promoted' | 'repeated' | 'left'
  student_registration_number?: string
}

export const enrollmentAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: Enrollment[]; count: number }>('/enrollments/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<Enrollment>(`/enrollments/${id}/`),

  create: (payload: EnrollmentPayload) =>
    axiosInstance.post<Enrollment>('/enrollments/', payload),

  update: (id: string, payload: Partial<EnrollmentPayload>) =>
    axiosInstance.patch<Enrollment>(`/enrollments/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/enrollments/${id}/`),
}
