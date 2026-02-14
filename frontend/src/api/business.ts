import request from '@/utils/request'
import type { Supplier, Customer, Product, PurchaseOrder, SalesOrder, Warehouse, Payment, Bill, PageResult } from '@/types'

/**
 * 供应商相关API
 */
export const supplierApi = {
  /**
   * 获取供应商列表
   * @param params 查询参数（分页、关键词）
   * @returns 分页的供应商列表
   */
  getSuppliers(params?: { skip?: number; limit?: number; keyword?: string }) {
    return request.get<PageResult<Supplier>>('/suppliers/', { params })
  },
  
  /**
   * 获取单个供应商详情
   * @param id 供应商ID
   * @returns 供应商详细信息
   */
  getSupplier(id: number) {
    return request.get<Supplier>(`/suppliers/${id}`)
  },
  
  /**
   * 创建新供应商
   * @param data 供应商数据
   * @returns 创建成功的供应商信息
   */
  createSupplier(data: any) {
    return request.post<Supplier>('/suppliers/', data)
  },
  
  /**
   * 更新供应商信息
   * @param id 供应商ID
   * @param data 更新数据
   * @returns 更新后的供应商信息
   */
  updateSupplier(id: number, data: any) {
    return request.put<Supplier>(`/suppliers/${id}`, data)
  },
  
  /**
   * 删除供应商
   * @param id 供应商ID
   */
  deleteSupplier(id: number) {
    return request.delete(`/suppliers/${id}`)
  }
}

/**
 * 采购订单相关API
 */
export const purchaseApi = {
  /**
   * 获取采购订单列表
   * @param params 查询参数（分页、状态、供应商）
   * @returns 分页的采购订单列表
   */
  getPurchaseOrders(params?: { skip?: number; limit?: number; status?: string; supplier_id?: number }) {
    return request.get<PageResult<PurchaseOrder>>('/purchase/', { params })
  },
  
  /**
   * 获取采购订单详情
   * @param id 订单ID
   * @returns 订单详细信息
   */
  getPurchaseOrder(id: number) {
    return request.get<PurchaseOrder>(`/purchase/${id}`)
  },
  
  /**
   * 创建采购订单
   * @param data 订单数据
   * @returns 创建成功的订单信息
   */
  createPurchaseOrder(data: any) {
    return request.post<PurchaseOrder>('/purchase/', data)
  },
  
  /**
   * 更新采购订单
   * @param id 订单ID
   * @param data 更新数据
   * @returns 更新后的订单信息
   */
  updatePurchaseOrder(id: number, data: any) {
    return request.put<PurchaseOrder>(`/purchase/${id}`, data)
  },
  
  /**
   * 审批采购订单
   * @param id 订单ID
   * @param data 审批数据（审批状态、备注）
   */
  approvePurchaseOrder(id: number, data: { approval_status: string; remark?: string }) {
    return request.post(`/purchase/${id}/approve`, data)
  },
  
  /**
   * 删除采购订单
   * @param id 订单ID
   */
  deletePurchaseOrder(id: number) {
    return request.delete(`/purchase/${id}`)
  }
}

/**
 * 产品相关API
 */
export const productApi = {
  /**
   * 获取产品列表
   * @param params 查询参数（分页、关键词、分类）
   * @returns 分页的产品列表
   */
  getProducts(params?: { skip?: number; limit?: number; keyword?: string; category_id?: number }) {
    return request.get<PageResult<Product>>('/inventory/products/', { params })
  },
  
  /**
   * 获取产品详情
   * @param id 产品ID
   * @returns 产品详细的信息
   */
  getProduct(id: number) {
    return request.get<Product>(`/inventory/products/${id}`)
  },
  
  /**
   * 创建产品
   * @param data 产品数据
   * @returns 创建成功的产品信息
   */
  createProduct(data: any) {
    return request.post<Product>('/inventory/products/', data)
  },
  
  /**
   * 更新产品信息
   * @param id 产品ID
   * @param data 更新数据
   * @returns 更新后的产品信息
   */
  updateProduct(id: number, data: any) {
    return request.put<Product>(`/inventory/products/${id}`, data)
  },
  
  /**
   * 删除产品
   * @param id 产品ID
   */
  deleteProduct(id: number) {
    return request.delete(`/inventory/products/${id}`)
  }
}

/**
 * 仓库相关API
 */
export const warehouseApi = {
  /**
   * 获取仓库列表
   * @returns 所有仓库信息
   */
  getWarehouses() {
    return request.get<Warehouse[]>('/inventory/warehouses/')
  },
  
  /**
   * 创建仓库
   * @param data 仓库数据
   * @returns 创建成功的仓库信息
   */
  createWarehouse(data: any) {
    return request.post<Warehouse>('/inventory/warehouses/', data)
  },
  
  /**
   * 更新仓库信息
   * @param id 仓库ID
   * @param data 更新数据
   * @returns 更新后的仓库信息
   */
  updateWarehouse(id: number, data: any) {
    return request.put<Warehouse>(`/inventory/warehouses/${id}`, data)
  },
  
  /**
   * 删除仓库
   * @param id 仓库ID
   */
  deleteWarehouse(id: number) {
    return request.delete(`/inventory/warehouses/${id}`)
  }
}

/**
 * 库存记录相关API
 */
export const stockApi = {
  /**
   * 获取库存记录列表
   * @param params 查询参数（分页、仓库、类型）
   * @returns 分页的库存记录列表
   */
  getStockRecords(params?: { skip?: number; limit?: number; warehouse_id?: number; type?: string }) {
    return request.get<PageResult<any>>('/inventory/stock-records/', { params })
  },
  
  /**
   * 创建库存记录
   * @param data 库存记录数据
   * @returns 创建成功的库存记录
   */
  createStockRecord(data: any) {
    return request.post<any>('/inventory/stock-records/', data)
  },
  
  /**
   * 获取库存盘点列表
   * @returns 所有库存盘点记录
   */
  getStockChecks() {
    return request.get<any[]>('/inventory/stock-checks/')
  },
  
  /**
   * 创建库存盘点
   * @param data 盘点数据
   * @returns 创建成功的盘点记录
   */
  createStockCheck(data: any) {
    return request.post<any>('/inventory/stock-checks/', data)
  },
  
  /**
   * 完成库存盘点
   * @param id 盘点ID
   */
  completeStockCheck(id: number) {
    return request.put(`/inventory/stock-checks/${id}/complete`)
  }
}

/**
 * 客户相关API
 */
export const customerApi = {
  /**
   * 获取客户列表
   * @param params 查询参数（分页、关键词）
   * @returns 分页的客户列表
   */
  getCustomers(params?: { skip?: number; limit?: number; keyword?: string }) {
    return request.get<PageResult<Customer>>('/sales/customers/', { params })
  },
  
  /**
   * 获取客户详情
   * @param id 客户ID
   * @returns 客户详细信息
   */
  getCustomer(id: number) {
    return request.get<Customer>(`/sales/customers/${id}`)
  },
  
  /**
   * 创建客户
   * @param data 客户数据
   * @returns 创建成功的客户信息
   */
  createCustomer(data: any) {
    return request.post<Customer>('/sales/customers/', data)
  },
  
  /**
   * 更新客户信息
   * @param id 客户ID
   * @param data 更新数据
   * @returns 更新后的客户信息
   */
  updateCustomer(id: number, data: any) {
    return request.put<Customer>(`/sales/customers/${id}`, data)
  },
  
  /**
   * 删除客户
   * @param id 客户ID
   */
  deleteCustomer(id: number) {
    return request.delete(`/sales/customers/${id}`)
  }
}

/**
 * 销售订单相关API
 */
export const salesApi = {
  /**
   * 获取销售订单列表
   * @param params 查询参数（分页、状态、客户）
   * @returns 分页的销售订单列表
   */
  getSalesOrders(params?: { skip?: number; limit?: number; status?: string; customer_id?: number }) {
    return request.get<PageResult<SalesOrder>>('/sales/sales-orders/', { params })
  },
  
  /**
   * 获取销售订单详情
   * @param id 订单ID
   * @returns 订单详细信息
   */
  getSalesOrder(id: number) {
    return request.get<SalesOrder>(`/sales/sales-orders/${id}`)
  },
  
  /**
   * 创建销售订单
   * @param data 订单数据
   * @returns 创建成功的订单信息
   */
  createSalesOrder(data: any) {
    return request.post<SalesOrder>('/sales/sales-orders/', data)
  },
  
  /**
   * 更新销售订单
   * @param id 订单ID
   * @param data 更新数据
   * @returns 更新后的订单信息
   */
  updateSalesOrder(id: number, data: any) {
    return request.put<SalesOrder>(`/sales/sales-orders/${id}`, data)
  },
  
  /**
   * 审批销售订单
   * @param id 订单ID
   * @param data 审批数据（审批状态、备注）
   */
  approveSalesOrder(id: number, data: { approval_status: string; remark?: string }) {
    return request.post(`/sales/sales-orders/${id}/approve`, data)
  },
  
  /**
   * 删除销售订单
   * @param id 订单ID
   */
  deleteSalesOrder(id: number) {
    return request.delete(`/sales/sales-orders/${id}`)
  }
}

/**
 * 财务相关API
 */
export const financeApi = {
  /**
   * 获取付款单据列表
   * @param params 查询参数（分页、类型、状态）
   * @returns 分页的付款单据列表
   */
  getPayments(params?: { skip?: number; limit?: number; type?: string; status?: string }) {
    return request.get<PageResult<Payment>>('/finance/payments/', { params })
  },
  
  /**
   * 获取付款单据详情
   * @param id 单据ID
   * @returns 单据详细信息
   */
  getPayment(id: number) {
    return request.get<Payment>(`/finance/payments/${id}`)
  },
  
  /**
   * 创建付款单据
   * @param data 单据数据
   * @returns 创建成功的单据信息
   */
  createPayment(data: any) {
    return request.post<Payment>('/finance/payments/', data)
  },
  
  /**
   * 更新付款单据
   * @param id 单据ID
   * @param data 更新数据
   * @returns 更新后的单据信息
   */
  updatePayment(id: number, data: any) {
    return request.put<Payment>(`/finance/payments/${id}`, data)
  },
  
  /**
   * 审批付款单据
   * @param id 单据ID
   * @param data 审批数据（审批状态、备注）
   */
  approvePayment(id: number, data: { approval_status: string; remark?: string }) {
    return request.post(`/finance/payments/${id}/approve`, data)
  },
  
  /**
   * 获取账单列表
   * @param params 查询参数（分页、类型、状态）
   * @returns 分页的账单列表
   */
  getBills(params?: { skip?: number; limit?: number; type?: string; status?: string }) {
    return request.get<PageResult<Bill>>('/finance/bills/', { params })
  },
  
  /**
   * 获取账单详情
   * @param id 账单ID
   * @returns 账单详细信息
   */
  getBill(id: number) {
    return request.get<Bill>(`/finance/bills/${id}`)
  },
  
  /**
   * 创建账单
   * @param data 账单数据
   * @returns 创建成功的账单信息
   */
  createBill(data: any) {
    return request.post<Bill>('/finance/bills/', data)
  },
  
  /**
   * 更新账单
   * @param id 账单ID
   * @param data 更新数据
   * @returns 更新后的账单信息
   */
  updateBill(id: number, data: any) {
    return request.put<Bill>(`/finance/bills/${id}`, data)
  },
  
  /**
   * 获取账户列表
   * @returns 所有账户信息
   */
  getAccounts() {
    return request.get<any[]>('/finance/accounts/')
  },
  
  /**
   * 创建账户
   * @param data 账户数据
   * @returns 创建成功的账户信息
   */
  createAccount(data: any) {
    return request.post<any>('/finance/accounts/', data)
  },
  
  /**
   * 更新账户
   * @param id 账户ID
   * @param data 更新数据
   * @returns 更新后的账户信息
   */
  updateAccount(id: number, data: any) {
    return request.put<any>(`/finance/accounts/${id}`, data)
  },
  
  /**
   * 获取成本中心列表
   * @returns 所有成本中心信息
   */
  getCostCenters() {
    return request.get<any[]>('/finance/cost-centers/')
  },
  
  /**
   * 创建成本中心
   * @param data 成本中心数据
   * @returns 创建成功的成本中心信息
   */
  createCostCenter(data: any) {
    return request.post<any>('/finance/cost-centers/', data)
  },
  
  /**
   * 更新成本中心
   * @param id 成本中心ID
   * @param data 更新数据
   * @returns 更新后的成本中心信息
   */
  updateCostCenter(id: number, data: any) {
    return request.put<any>(`/finance/cost-centers/${id}`, data)
  }
}

/**
 * 报表相关API
 */
export const reportApi = {
  /**
   * 获取采购汇总报表
   * @param params 查询参数（开始日期、结束日期）
   * @returns 采购汇总数据
   */
  getPurchaseSummary(params?: { start_date?: string; end_date?: string }) {
    return request.get<any>('/reports/purchase-summary', { params })
  },
  
  /**
   * 获取销售汇总报表
   * @param params 查询参数（开始日期、结束日期）
   * @returns 销售汇总数据
   */
  getSalesSummary(params?: { start_date?: string; end_date?: string }) {
    return request.get<any>('/reports/sales-summary', { params })
  },
  
  /**
   * 获取库存状态报表
   * @returns 库存状态数据
   */
  getInventoryStatus() {
    return request.get<any>('/reports/inventory-status')
  },
  
  /**
   * 获取供应商绩效报表
   * @returns 供应商绩效数据
   */
  getSupplierPerformance() {
    return request.get<any>('/reports/supplier-performance')
  },
  
  /**
   * 获取客户分析报表
   * @returns 客户分析数据
   */
  getCustomerAnalysis() {
    return request.get<any>('/reports/customer-analysis')
  },
  
  /**
   * 获取财务汇总报表
   * @param params 查询参数（开始日期、结束日期）
   * @returns 财务汇总数据
   */
  getFinancialSummary(params?: { start_date?: string; end_date?: string }) {
    return request.get<any>('/reports/financial-summary', { params })
  },
  
  /**
   * 获取仪表板统计数据
   * @returns 仪表板统计数据
   */
  getDashboardStats() {
    return request.get<any>('/reports/dashboard')
  }
}
