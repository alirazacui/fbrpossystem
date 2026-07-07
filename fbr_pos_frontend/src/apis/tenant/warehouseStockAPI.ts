import axiosInstance from '@/apis/axiosInstance'

export interface WarehouseStock {
  id?: number
  warehouse: number
  warehouse_name?: string
  product: number
  product_name?: string
  product_sku?: string
  product_barcode?: string
  quantity: number | string
  low_stock_threshold: number | string
  notes?: string
  is_low?: boolean
  updated_at?: string
}

export const warehouseStockAPI = {
  getAll: (params?: any) => axiosInstance.get('/warehouse-stocks/', { params }),
  getById: (id: number) => axiosInstance.get(`/warehouse-stocks/${id}/`),
  update: (id: number, data: Partial<WarehouseStock>) => axiosInstance.patch(`/warehouse-stocks/${id}/`, data),
}
