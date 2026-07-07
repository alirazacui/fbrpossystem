import axiosInstance from '@/apis/axiosInstance'

export interface AdminInvoiceItem {
  id: number
  tenant_name: string
  invoice_number: string
  fbr_invoice_number: string
  status: string
  fbr_status: string
  total_amount: number
  created_at: string
  document_ready?: boolean
}

export const adminInvoicesAPI = {
  getAll: () => axiosInstance.get('/admin-dashboard/invoices/'),

  getDocumentUrl: (saleId: number, download = false) =>
    axiosInstance.get(`/admin-dashboard/invoices/${saleId}/document/`, {
      params: { download: download ? '1' : '0' },
    }),
}
