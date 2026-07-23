import axiosInstance from '@/apis/axiosInstance'

export interface StudentExamResult {
  id: string
  student_id: string
  exam_id: string
  subject_id: string
  marks_obtained: number
  max_marks: number
  grade_letter: string | null
  remarks: string | null

  // Related
  student_name?: string
  exam_name?: string
  subject_name?: string
  grade?: string  // alias for grade_letter
}

export interface StudentExamResultPayload {
  student_id: string
  exam_id: string
  subject_id: string
  marks_obtained: number
  max_marks: number
  grade_letter?: string
  remarks?: string
}

export const studentExamResultAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: StudentExamResult[]; count: number }>('/student-exam-results/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<StudentExamResult>(`/student-exam-results/${id}/`),

  create: (payload: StudentExamResultPayload) =>
    axiosInstance.post<StudentExamResult>('/student-exam-results/', payload),

  update: (id: string, payload: Partial<StudentExamResultPayload>) =>
    axiosInstance.patch<StudentExamResult>(`/student-exam-results/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/student-exam-results/${id}/`),
}
