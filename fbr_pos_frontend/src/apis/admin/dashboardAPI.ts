import axiosInstance from '@/apis/axiosInstance'

export interface DashboardStats {
  metrics: {
    total_tenants: number
    active_tenants: number
    total_users: number
    total_managers: number
    total_cashiers: number
    total_salespersons: number
    active_subscriptions: number
    successful_invoices: number
    total_fbr_submissions: number
  }
  chart_data: {
    labels: string[]
    values: number[]
  }
  expiring_subscriptions: {
    company_name: string
    plan: string
    expires_on: string
  }[]
  failed_fbr: {
    sale_id: number
    endpoint: string
    status_code: string
    attempted_at: string
  }[]
  recent_activity: {
    message: string
    date: string
  }[]
}

class AdminDashboardAPI {
  async getStats(): Promise<DashboardStats> {
    const response = await axiosInstance.get('/admin-dashboard/stats/')
    return response.data
  }
}

export default new AdminDashboardAPI()
