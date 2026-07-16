import axiosInstance from '@/apis/axiosInstance'

export interface Product {
  id: number
  name: string
  sku: string
  barcode: string
  category: number | null
  category_name?: string
  price: number
  selling_price?: number
  cost_price?: number
  fbr_fixed_retail_price?: number
  min_sale_price?: number
  current_stock: number
  image_url?: string
  hs_code?: string
  fbr_sale_type: string
  tax_rate_percent: string | number
  unit_of_measure?: string
  fbr_sro_schedule_no?: string
  fbr_sro_item_serial_no?: string
  is_active?: boolean
  created_at: string
  updated_at: string
}

export interface ProductCreatePayload {
  name: string
  sku: string
  barcode: string
  category?: number
  selling_price: number
  cost_price?: number
  fbr_fixed_retail_price?: number
  min_sale_price?: number
  current_stock: number
  hs_code?: string
  fbr_sale_type: string
  tax_rate_percent: string
  unit_of_measure?: string
  fbr_sro_schedule_no?: string
  fbr_sro_item_serial_no?: string
  is_active?: boolean
}

export const productsAPI = {
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ count: number; results: Product[] }>('/products/', { params }),
  retrieve: (id: number) =>
    axiosInstance.get<Product>(`/products/${id}/`),
  create: (payload: ProductCreatePayload) =>
    axiosInstance.post<Product>('/products/', payload),
  update: (id: number, payload: Partial<ProductCreatePayload>) =>
    axiosInstance.patch<Product>(`/products/${id}/`, payload),
  delete: (id: number) =>
    axiosInstance.delete(`/products/${id}/`),
  search: (query: string) =>
    axiosInstance.get<Product[]>('/products/search/', { params: { q: query } }),
  getByBarcode: (barcode: string) =>
    axiosInstance.get<Product>('/products/by_barcode/', { params: { barcode } }),
  adjustStock: (id: number, quantity: number) =>
    axiosInstance.post(`/products/${id}/adjust_stock/`, { quantity }),
}