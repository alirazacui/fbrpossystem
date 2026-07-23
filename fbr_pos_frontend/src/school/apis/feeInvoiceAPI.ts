import axiosInstance from '@/apis/axiosInstance'

export interface FeeInvoice {
  id: string
  student_id: string
  fee_structure_id: string
  enrollement_id: string
  academic_session_id: string
  grade_id: string
  guardian_id: string | null
  invoice_date: string
  due_date: string | null
  total_amount: string
  total_concession_amount: string
  total_payable_amount: string
  status: 'unpaid' | 'paid' | 'partial'
  invoice_status_fbr: 'draft' | 'sent_to_fbr' | 'failed'
  generated_by: 'auto' | 'manual'
  fbr_invoice_number: string | null
  core_invoice_id: string | null

  // Nested (read-only)
  items?: FeeInvoiceItem[]
  payments?: any[]

  // Related
  student_name?: string
  session_name?: string
  grade_name?: string
  payment_status?: 'unpaid' | 'paid' | 'partial'  // alias for status
  invoice_number?: string
}

export interface FeeInvoiceItem {
  id: string
  description: string | null
  quantity: string
  unit_price: string
  discount_amount: string
  tax_rate: string
  tax_amount: string
  total_amount: string
  pct_code: string | null
}

export interface FeeInvoicePayload {
  student_id: string
  fee_structure_id: string
  enrollement_id: string
  academic_session_id: string
  grade_id: string
  guardian_id?: string
  invoice_date?: string
  due_date?: string
  total_amount: number
  total_concession_amount?: number
  total_payable_amount: number
  status?: 'unpaid' | 'paid' | 'partial'
}

export const feeInvoiceAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: FeeInvoice[]; count: number }>('/fee-invoices/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<FeeInvoice>(`/fee-invoices/${id}/`),

  create: (payload: FeeInvoicePayload) =>
    axiosInstance.post<FeeInvoice>('/fee-invoices/', payload),

  update: (id: string, payload: Partial<FeeInvoicePayload>) =>
    axiosInstance.patch<FeeInvoice>(`/fee-invoices/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/fee-invoices/${id}/`),

  generateFbr: (id: string) =>
    axiosInstance.post<{ message: string; core_invoice_id: string }>(`/fee-invoices/${id}/generate-fbr/`),
}
