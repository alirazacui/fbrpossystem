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
    axiosInstance.get<{ results: StudentGuardian[]; count: number }>('/school/student-guardians/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<StudentGuardian>(`/school/student-guardians/${id}/`),

  create: (payload: StudentGuardianPayload) =>
    axiosInstance.post<StudentGuardian>('/school/student-guardians/', payload),

  update: (id: string, payload: Partial<StudentGuardianPayload>) =>
    axiosInstance.patch<StudentGuardian>(`/school/student-guardians/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/student-guardians/${id}/`),
}
