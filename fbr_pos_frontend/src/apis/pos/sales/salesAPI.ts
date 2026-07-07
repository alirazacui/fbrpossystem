import axiosInstance from '@/apis/axiosInstance'

export interface Sale {
  id: number
  sale_number: string
  company_id: number
  customer_id?: number
  created_by_id: number
  status: 'DRAFT' | 'COMPLETED' | 'CANCELLED'
  type: 'Sale Invoice' | 'Debit Note' | 'Credit Note'
  subtotal: number
  total_discount: number
  total_tax: number
  total_amount: number
  total_paid: number
  change_amount: number
  fbr_invoice_number?: string
  fbr_submission_status?: 'SUCCESS' | 'FAILED' | 'PENDING'
  qr_code?: string
  created_at: string
  updated_at: string
}

export interface SaleLine {
  id: number
  sale_id: number
  product_id: number
  quantity: number
  unit_price: number
  discount_amount: number
  tax_amount: number
  total: number
}

export interface SalePayment {
  id: number
  sale_id: number
  payment_method: 'CASH' | 'CARD' | 'CHEQUE' | 'BANK_TRANSFER'
  amount: number
  created_at: string
}

export interface SaleCreatePayload {
  customer_id?: number
  sale_lines: Array<{
    product_id: number
    quantity: number
    unit_price: number
    discount_amount?: number
    tax_amount?: number
  }>
  payments: Array<{
    payment_method: string
    amount: number
  }>
}

export const salesAPI = {
  // List sales
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ count: number; results: Sale[] }>('/sales/list/', { params }),

  // Get single sale
  retrieve: (id: number) =>
    axiosInstance.get<Sale>(`/sales/${id}/detail/`),

  // Create sale (DRAFT)
  create: (payload: SaleCreatePayload) =>
    axiosInstance.post<Sale>('/sales/create_sale/', payload),

  // Update sale
  update: (id: number, payload: Partial<Sale>) =>
    axiosInstance.patch<Sale>(`/sales/${id}/detail/`, payload),

  // Add payment
  addPayment: (id: number, payload: { amount: number; payment_method: string }) =>
    axiosInstance.post(`/sales/${id}/add-payment/`, payload),

  // Complete sale (triggers FBR submission)
  complete: (id: number) =>
    axiosInstance.post(`/sales/${id}/complete/`, {}),

  // Validate sale with FBR (Dry-run without submission)
  validateFbr: (id: number) =>
    axiosInstance.post(`/sales/${id}/validate_fbr/`, {}),

  // Cancel sale
  cancel: (id: number) =>
    axiosInstance.post(`/sales/${id}/cancel/`, {}),

  // Print receipt
  printReceipt: (id: number) =>
    axiosInstance.get(`/receipts/${id}/a4/`, { responseType: 'blob' }),

  // Get sale lines
  getSaleLines: (saleId: number) =>
    axiosInstance.get<SaleLine[]>(`/sales/${saleId}/lines`),

  // Get sale payments
  getSalePayments: (saleId: number) =>
    axiosInstance.get<SalePayment[]>(`/sales/${saleId}/payments`),
}
