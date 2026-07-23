import axiosInstance from '@/apis/axiosInstance'

export interface StudentGuardian {
  id: string
  student_id: string
  guardian_id: string
  relation: string | null
  relationship: string | null
  is_primary_billing_contact: boolean
  is_emergency_contact?: boolean
  can_pickup_student?: boolean
  
  // Related
  student_name?: string
  guardian_name?: string
}

export type StudentGuardianAssignment = StudentGuardian

export interface StudentGuardianPayload {
  student_id: string
  guardian_id: string
  relation?: string
  is_primary_billing_contact?: boolean
}

export const studentGuardianAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: StudentGuardian[]; count: number }>('/student-guardian-assignments/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<StudentGuardian>(`/student-guardian-assignments/${id}/`),

  create: (payload: StudentGuardianPayload) =>
    axiosInstance.post<StudentGuardian>('/student-guardian-assignments/', payload),

  update: (id: string, payload: Partial<StudentGuardianPayload>) =>
    axiosInstance.patch<StudentGuardian>(`/student-guardian-assignments/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/student-guardian-assignments/${id}/`),
}
