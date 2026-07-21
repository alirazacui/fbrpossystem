import axiosInstance from '@/apis/axiosInstance'

export interface ClassSubjectAssignment {
  id: string
  section_id: string
  subject_id: string
  teacher_id: string | null
  
  // Related fields
  section_name?: string
  subject_name?: string
  teacher_name?: string
}

export interface ClassSubjectAssignmentPayload {
  section_id: string
  subject_id: string
  teacher_id?: string
}

export const classSubjectAssignmentAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: ClassSubjectAssignment[]; count: number }>('/school/class-subject-assignments/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<ClassSubjectAssignment>(`/school/class-subject-assignments/${id}/`),

  create: (payload: ClassSubjectAssignmentPayload) =>
    axiosInstance.post<ClassSubjectAssignment>('/school/class-subject-assignments/', payload),

  update: (id: string, payload: Partial<ClassSubjectAssignmentPayload>) =>
    axiosInstance.patch<ClassSubjectAssignment>(`/school/class-subject-assignments/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/class-subject-assignments/${id}/`),
}
