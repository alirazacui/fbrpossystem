import axiosInstance from '@/apis/axiosInstance'

export interface Permission {
  id: number
  module: string
  module_display: string
  action: string
  action_display: string
  codename: string
  label: string
  description: string
  is_active: boolean
}

export interface PermissionPanelItem {
  id: number
  action: string
  label: string
  codename: string
  granted: boolean
}

export interface PermissionModule {
  module: string
  module_display: string
  permissions: PermissionPanelItem[]
}

class PermissionsAPI {
  // GET /api/permissions/ — full catalogue
  async getAllPermissions(): Promise<Permission[]> {
    const response = await axiosInstance.get('/permissions/')
    return response.data.results || response.data
  }

  // GET /api/user-permissions/{userId}/panel/ — structured panel for a user
  async getUserPermissionPanel(userId: number): Promise<PermissionModule[]> {
    const response = await axiosInstance.get(`/user-permissions/${userId}/panel/`)
    return response.data
  }

  // POST /api/user-permissions/{userId}/assign/ — bulk assign permissions
  async assignPermissions(userId: number, permissionIds: number[]): Promise<void> {
    await axiosInstance.post(`/user-permissions/${userId}/assign/`, {
      permission_ids: permissionIds,
    })
  }
}

export default new PermissionsAPI()
