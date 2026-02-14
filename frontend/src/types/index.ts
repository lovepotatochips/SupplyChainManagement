export interface User {
  id: number
  username: string
  real_name?: string
  email?: string
  phone?: string
  avatar?: string
  status: boolean
  department_id?: number
  department_name?: string
  is_superuser: boolean
  created_at: string
  updated_at: string
}

export interface Role {
  id: number
  name: string
  code: string
  description?: string
  status: boolean
  created_at: string
  updated_at: string
}

export interface Permission {
  id: number
  name: string
  code: string
  type: string
  description?: string
  created_at: string
  updated_at: string
}

export interface Department {
  id: number
  name: string
  code: string
  parent_id?: number
  sort_order: number
  leader?: string
  phone?: string
  address?: string
  description?: string
  status: number
  created_at: string
  updated_at: string
  children?: Department[]
}

export interface Supplier {
  id: number
  code: string
  name: string
  type: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
  address?: string
  tax_number?: string
  bank_name?: string
  bank_account?: string
  credit_level: string
  credit_limit: number
  balance: number
  status: boolean
  remark?: string
  created_at: string
  updated_at: string
}

export interface Customer {
  id: number
  code: string
  name: string
  type: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
  address?: string
  tax_number?: string
  bank_name?: string
  bank_account?: string
  credit_limit: number
  balance: number
  status: boolean
  remark?: string
  created_at: string
  updated_at: string
}

export interface Product {
  id: number
  code: string
  name: string
  category_id?: number
  specification?: string
  unit?: string
  purchase_price: number
  sale_price: number
  min_stock: number
  max_stock: number
  current_stock: number
  status: string
  remark?: string
  created_at: string
  updated_at: string
}

export interface PurchaseOrder {
  id: number
  code: string
  supplier_id: number
  purchase_date?: string
  expected_date?: string
  total_amount: number
  paid_amount: number
  status: string
  approval_status: string
  approved_by?: number
  approved_at?: string
  remark?: string
  created_at: string
  updated_at: string
}

export interface SalesOrder {
  id: number
  code: string
  customer_id: number
  sale_date?: string
  delivery_date?: string
  total_amount: number
  paid_amount: number
  status: string
  approval_status: string
  approved_by?: number
  approved_at?: string
  remark?: string
  created_at: string
  updated_at: string
}

export interface Warehouse {
  id: number
  code: string
  name: string
  type: string
  address?: string
  manager?: string
  phone?: string
  capacity: number
  status: number
  remark?: string
  created_at: string
  updated_at: string
}

export interface Payment {
  id: number
  code: string
  type: string
  amount: number
  payment_method?: string
  payment_date?: string
  reference_code?: string
  reference_type?: string
  supplier_id?: number
  customer_id?: number
  bank_account?: string
  status: string
  approval_status: string
  approved_by?: number
  approved_at?: string
  operator_id?: number
  remark?: string
  created_at: string
  updated_at: string
}

export interface Bill {
  id: number
  code: string
  type: string
  amount: number
  bill_date?: string
  due_date?: string
  reference_code?: string
  reference_type?: string
  supplier_id?: number
  customer_id?: number
  paid_amount: number
  remaining_amount: number
  status: string
  remark?: string
  created_at: string
  updated_at: string
}

export interface ApiResponse<T = any> {
  data?: T
  message?: string
  detail?: string
}

export interface PageResult<T = any> {
  total: number
  items: T[]
}
