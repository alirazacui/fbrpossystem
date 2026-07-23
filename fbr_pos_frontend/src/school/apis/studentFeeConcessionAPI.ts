import axiosInstance from '@/apis/axiosInstance'

export interface StudentFeeConcession {
  id: string
  student_id: string
  fee_head_id: string | null
  academic_session_id: string
  concession_type: 'percentage' | 'fixed_amount'
  amount: string
  percentage: string
  reason: string
  
  // Related info
  student_name?: string
  fee_head_name?: string
  session_name?: string
}

export interface StudentFeeConcessionPayload {
  student_id: string
  fee_head_id?: string | null
  academic_session_id: string
  concession_type: 'percentage' | 'fixed_amount'
  amount?: number
  percentage?: number
  reason?: string
}

export const studentFeeConcessionAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: StudentFeeConcession[]; count: number }>('/student-fee-concessions/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<StudentFeeConcession>(`/student-fee-concessions/${id}/`),

  create: (payload: StudentFeeConcessionPayload) =>
    axiosInstance.post<StudentFeeConcession>('/student-fee-concessions/', payload),

  update: (id: string, payload: Partial<StudentFeeConcessionPayload>) =>
    axiosInstance.patch<StudentFeeConcession>(`/student-fee-concessions/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/student-fee-concessions/${id}/`),
}
