import api from '@/apis/axiosInstance'

export interface DashboardStats {
  products: { active: number }
  customers: { total: number }
  invoices: { this_month_count: number, this_month_total: number }
  stock: { value: number }
  sales_today: number
  avg_invoice: number
  fbr: { sent: number, pending: number }
  chart_data: { date: string, total: number }[]
  recent_invoices: any[]
  low_stock: any[]
  failed_fbr: any[]
}

export const dashboardAPI = {
  getStats: async (): Promise<DashboardStats> => {
    const response = await api.get('/dashboard/')
    return response.data
  }
}
