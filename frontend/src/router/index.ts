import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘', icon: 'DataAnalysis' }
      },
      {
        path: 'system',
        name: 'System',
        meta: { title: '系统管理', icon: 'Setting' },
        children: [
          {
            path: 'users',
            name: 'Users',
            component: () => import('@/views/system/Users.vue'),
            meta: { title: '用户管理', icon: 'User' }
          },
          {
            path: 'roles',
            name: 'Roles',
            component: () => import('@/views/system/Roles.vue'),
            meta: { title: '角色管理', icon: 'UserFilled' }
          },
          {
            path: 'departments',
            name: 'Departments',
            component: () => import('@/views/system/Departments.vue'),
            meta: { title: '部门管理', icon: 'OfficeBuilding' }
          }
        ]
      },
      {
        path: 'supply',
        name: 'Supply',
        meta: { title: '供应链管理', icon: 'Goods' },
        children: [
          {
            path: 'suppliers',
            name: 'Suppliers',
            component: () => import('@/views/supply/Suppliers.vue'),
            meta: { title: '供应商管理', icon: 'Shop' }
          },
          {
            path: 'purchase',
            name: 'Purchase',
            component: () => import('@/views/supply/Purchase.vue'),
            meta: { title: '采购管理', icon: 'ShoppingCart' }
          },
          {
            path: 'inventory',
            name: 'Inventory',
            component: () => import('@/views/supply/Inventory.vue'),
            meta: { title: '库存管理', icon: 'Box' }
          },
          {
            path: 'sales',
            name: 'Sales',
            component: () => import('@/views/supply/Sales.vue'),
            meta: { title: '销售管理', icon: 'Sell' }
          }
        ]
      },
      {
        path: 'finance',
        name: 'Finance',
        meta: { title: '财务管理', icon: 'Money' },
        children: [
          {
            path: 'payments',
            name: 'Payments',
            component: () => import('@/views/finance/Payments.vue'),
            meta: { title: '付款管理', icon: 'Wallet' }
          },
          {
            path: 'bills',
            name: 'Bills',
            component: () => import('@/views/finance/Bills.vue'),
            meta: { title: '账单管理', icon: 'Document' }
          },
          {
            path: 'accounts',
            name: 'Accounts',
            component: () => import('@/views/finance/Accounts.vue'),
            meta: { title: '账户管理', icon: 'CreditCard' }
          }
        ]
      },
      {
        path: 'analysis',
        name: 'Analysis',
        meta: { title: '数据分析', icon: 'TrendCharts' },
        children: [
          {
            path: 'supplier',
            name: 'SupplierAnalysis',
            component: () => import('@/views/analysis/SupplierAnalysis.vue'),
            meta: { title: '供应商分析', icon: 'Shop' }
          },
          {
            path: 'purchase',
            name: 'PurchaseAnalysis',
            component: () => import('@/views/analysis/PurchaseAnalysis.vue'),
            meta: { title: '采购分析', icon: 'ShoppingCart' }
          },
          {
            path: 'inventory',
            name: 'InventoryAnalysis',
            component: () => import('@/views/analysis/InventoryAnalysis.vue'),
            meta: { title: '库存分析', icon: 'Box' }
          },
          {
            path: 'sales',
            name: 'SalesAnalysis',
            component: () => import('@/views/analysis/SalesAnalysis.vue'),
            meta: { title: '销售分析', icon: 'Sell' }
          },
          {
            path: 'payment',
            name: 'PaymentAnalysis',
            component: () => import('@/views/analysis/PaymentAnalysis.vue'),
            meta: { title: '付款分析', icon: 'Wallet' }
          },
          {
            path: 'bill',
            name: 'BillAnalysis',
            component: () => import('@/views/analysis/BillAnalysis.vue'),
            meta: { title: '账单分析', icon: 'Document' }
          },
          {
            path: 'account',
            name: 'AccountAnalysis',
            component: () => import('@/views/analysis/AccountAnalysis.vue'),
            meta: { title: '账户分析', icon: 'CreditCard' }
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
