/**
 * User Types
 */
export interface User {
  id: number
  email: string
  username: string
  first_name: string
  last_name: string
  role: 'admin' | 'admin_staff' | 'owner' | 'manager' | 'cashier' | 'salesperson'
  status: 'active' | 'inactive' | 'suspended'
  company_id?: number
  created_at: string
  updated_at: string
}

/**
 * Company Types
 */
export interface Company {
  id: number
  business_name: string
  ntn: string
  address: string
  logo_url?: string
  fbr_sector: string
  business_nature: string
  status: 'active' | 'inactive'
  is_active?: boolean
  owner_email?: string
  owner_id?: number
  created_at: string
  updated_at: string
  fbr_sandbox_token?: string
  fbr_production_token?: string
  fbr_sandbox_complete?: boolean
  fbr_scenario_sn001?: boolean
  fbr_scenario_sn002?: boolean
  fbr_scenario_sn003?: boolean
  fbr_scenario_sn004?: boolean
  fbr_scenario_sn005?: boolean
  fbr_scenario_sn006?: boolean
  fbr_scenario_sn007?: boolean
  fbr_scenario_sn008?: boolean
  fbr_scenario_sn009?: boolean
  fbr_scenario_sn010?: boolean
  fbr_scenario_sn011?: boolean
  fbr_scenario_sn012?: boolean
  fbr_scenario_sn013?: boolean
  fbr_scenario_sn014?: boolean
  fbr_scenario_sn015?: boolean
  fbr_scenario_sn016?: boolean
  fbr_scenario_sn017?: boolean
  fbr_scenario_sn018?: boolean
  fbr_scenario_sn019?: boolean
  fbr_scenario_sn020?: boolean
  fbr_scenario_sn021?: boolean
  fbr_scenario_sn022?: boolean
  fbr_scenario_sn023?: boolean
  fbr_scenario_sn024?: boolean
  fbr_scenario_sn025?: boolean
  fbr_scenario_sn026?: boolean
  fbr_scenario_sn027?: boolean
  fbr_scenario_sn028?: boolean
}

/**
 * Product Types
 */
export interface Category {
  id: number
  name: string
  company_id: number
  created_at: string
}

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

/**
 * Customer Types
 */
export interface Customer {
  id: number
  name: string
  ntn_cnic?: string
  phone?: string
  email?: string
  address?: string
  registration_type: 'Registered' | 'Unregistered'
  province: string
  status: 'active' | 'inactive'
  created_at: string
}

/**
 * Sales Types
 */
export interface CashSession {
  id: number
  company_id: number
  cashier_id: number
  status: 'OPEN' | 'CLOSED' | 'RECONCILED'
  opening_balance: number
  expected_balance: number
  actual_balance?: number
  opened_at: string
  closed_at?: string
  reconciled_at?: string
}

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

export interface SaleReturn {
  id: number
  sale_id: number
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'COMPLETED'
  reason: string
  created_at: string
}

export interface DebitNote {
  id: number
  sale_id: number
  fbr_invoice_number?: string
  status: 'DRAFT' | 'COMPLETED' | 'CANCELLED'
  created_at: string
}

/**
 * Subscription Types
 */
export interface SubscriptionPlan {
  id: number
  name: string
  price: number
  duration: number
  max_products: number
  max_users: number
  max_customers: number
  includes_fbr_di: boolean
  includes_inventory: boolean
  includes_restaurant_fnb: boolean
  created_at: string
}

export interface CompanySubscription {
  id: number
  company_id: number
  plan_id: number
  status: 'ACTIVE' | 'TRIAL' | 'EXPIRED' | 'SUSPENDED' | 'CANCELLED'
  expiry_date: string
  created_at: string
}

/**
 * Report Types
 */
export interface SalesReport {
  total_sales: number
  total_revenue: number
  total_tax: number
  total_discount: number
  payment_breakdown: Record<string, number>
  hourly_breakdown?: Record<string, number>
  fbr_status: Record<string, number>
}

export interface InventoryReport {
  total_products: number
  low_stock_items: number
  total_stock_value: number
  products: Product[]
}

/**
 * Response Types
 */
export interface ApiResponse<T> {
  data: T
  message?: string
  status: number
}

export interface PaginatedResponse<T> {
  count: number
  next?: string
  previous?: string
  results: T[]
}

/**
 * Error Types
 */
export interface ApiError {
  detail?: string
  [key: string]: any
}
