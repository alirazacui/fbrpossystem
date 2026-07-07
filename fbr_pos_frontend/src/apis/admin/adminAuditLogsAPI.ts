import axiosInstance from '@/apis/axiosInstance'

export interface AdminAuditLogItem {
  id: number
  created_at: string
  tenant_name: string
  user_email: string
  entity_type: string
  entity_id: string
  action: string
}

export const adminAuditLogsAPI = {
  getAll: () => axiosInstance.get('/admin-dashboard/audit-logs/'),
  getById: (id: string) => axiosInstance.get(`/admin-dashboard/audit-logs/${id}/`),
}
