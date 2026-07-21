import axiosInstance from '@/apis/axiosInstance'

export interface FeePayment {
  id: string
  fee_invoice_id: string
  amount_paid: string
  payment_date: string
  payment_mode: 'cash' | 'bank' | 'online' | 'cheque'
  received_by_id: string | null
  reference_no: string | null

  // Related
  invoice_info?: string
  received_by_name?: string
}

export interface FeePaymentPayload {
  fee_invoice_id: string
  amount_paid: number
  payment_date?: string
  payment_mode?: 'cash' | 'bank' | 'online' | 'cheque'
  received_by_id?: string
  reference_no?: string
}

export const feePaymentAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ results: FeePayment[]; count: number }>('/school/fee-payments/', { params }),

  retrieve: (id: string) =>
    axiosInstance.get<FeePayment>(`/school/fee-payments/${id}/`),

  create: (payload: FeePaymentPayload) =>
    axiosInstance.post<FeePayment>('/school/fee-payments/', payload),

  update: (id: string, payload: Partial<FeePaymentPayload>) =>
    axiosInstance.patch<FeePayment>(`/school/fee-payments/${id}/`, payload),

  delete: (id: string) =>
    axiosInstance.delete(`/school/fee-payments/${id}/`),
}
