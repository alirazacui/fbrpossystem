import axiosInstance from '@/apis/axiosInstance'

export interface Product {
  id: number
  name: string
  sku: string
  barcode: string
  category_id: number
  price: number
  current_stock: number
  image_url?: string
  hs_code?: string
  fbr_sale_type: string
  tax_rate_percent: number
  created_at: string
  updated_at: string
}

export interface ProductCreatePayload {
  name: string
  sku: string
  barcode: string
  category_id?: number
  selling_price: number
  current_stock: number
  hs_code?: string
  fbr_sale_type: string
  tax_rate_percent: string
}

export const productsAPI = {
  // List products
  list: (params?: Record<string, any>) =>
    axiosInstance.get<{ count: number; results: Product[] }>('/products/', { params }),

  // Get single product
  retrieve: (id: number) =>
    axiosInstance.get<Product>(`/products/${id}/`),

  // Create product
  create: (payload: ProductCreatePayload) =>
    axiosInstance.post<Product>('/products/', payload),

  // Update product
  update: (id: number, payload: Partial<ProductCreatePayload>) =>
    axiosInstance.patch<Product>(`/products/${id}/`, payload),

  // Delete product
  delete: (id: number) =>
    axiosInstance.delete(`/products/${id}/`),

  // Search products by name/barcode
  search: (query: string) =>
    axiosInstance.get<Product[]>('/products/search/', { params: { q: query } }),

  // Get by barcode
  getByBarcode: (barcode: string) =>
    axiosInstance.get<Product>('/products/by_barcode/', { params: { barcode } }),

  // Adjust stock
  adjustStock: (id: number, quantity: number) =>
    axiosInstance.post(`/products/${id}/adjust_stock/`, { quantity }),
}
