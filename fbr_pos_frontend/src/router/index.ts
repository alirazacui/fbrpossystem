import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'

// Import page components
import LoginChoicePage from '@/pages/auth/LoginChoicePage.vue'
import AdminLoginPage from '@/pages/auth/AdminLoginPage.vue'
import CompanyOwnerLoginPage from '@/pages/auth/CompanyOwnerLoginPage.vue'
import DashboardPage from '@/pages/dashboard/DashboardPage.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'LoginChoice',
    component: LoginChoicePage,
    meta: { requiresAuth: false },
  },
  {
    path: '/login/admin',
    name: 'AdminLogin',
    component: AdminLoginPage,
    meta: { requiresAuth: false },
  },
  {
    path: '/login/company',
    name: 'CompanyLogin',
    component: CompanyOwnerLoginPage,
    meta: { requiresAuth: false },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/company/users',
    name: 'CompanyUsersPage',
    component: () => import('@/pages/company/CompanyUsersPage.vue'),
    meta: { requiresAuth: true, requiredRole: ['owner'] },
  },
  {
    path: '/company/terminals',
    name: 'CompanyTerminalsPage',
    component: () => import('@/pages/company/CompanyTerminalsPage.vue'),
    meta: { requiresAuth: true, requiredRole: ['owner'] },
  },
  {
    path: '/dashboard/admin',
    name: 'AdminDashboard',
    component: () => import('@/pages/dashboard/AdminDashboardPage.vue'),
    meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
  },

  // Admin Routes
  {
    path: '/admin',
    children: [
      {
        path: 'tenants',
        name: 'AdminTenants',
        component: () => import('@/pages/admin/TenantsListPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'tenants/create',
        name: 'CreateTenant',
        component: () => import('@/pages/admin/CreateCompanyPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'tenants/:id',
        name: 'AdminTenantDetail',
        component: () => import('@/pages/companies/CompanyDetail.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'tenants/:id/edit',
        name: 'EditTenant',
        component: () => import('@/pages/admin/EditCompanyPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'tenants/:id/permissions',
        name: 'CompanyPermissions',
        component: () => import('@/pages/companies/CompanyPermissions.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'branches',
        name: 'AdminBranches',
        component: () => import('@/pages/companies/CompaniesList.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'branches/:id',
        name: 'AdminBranchDetail',
        component: () => import('@/pages/admin/BranchDetailPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'terminals',
        name: 'AdminTerminals',
        component: () => import('@/pages/admin/AdminTerminalsPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'fbr-tokens',
        name: 'AdminFbrTokens',
        component: () => import('@/pages/admin/FbrTokensPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'fbr-tokens/:id',
        name: 'AdminFbrTokenDetail',
        component: () => import('@/pages/admin/FbrTokenDetailPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'invoices',
        name: 'AdminInvoices',
        component: () => import('@/pages/admin/AdminInvoicesPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'audit-logs',
        name: 'AdminAuditLogs',
        component: () => import('@/pages/admin/AdminAuditLogsPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'audit-logs/:id',
        name: 'AdminAuditLogDetail',
        component: () => import('@/pages/admin/AdminAuditLogDetailPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/pages/admin/AdminUsersPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'cashiers',
        name: 'AdminCashiers',
        component: () => import('@/pages/admin/AdminCashiersPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'platform-settings',
        name: 'AdminPlatformSettings',
        component: () => import('@/pages/admin/PlatformSettingsPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'users/:id',
        name: 'UserDetail',
        component: () => import('@/pages/admin/UserDetailPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'users/:id/permissions',
        name: 'UserPermissions',
        component: () => import('@/pages/admin/UserPermissionsPage.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'subscription-plans',
        name: 'AdminSubscriptionPlans',
        component: () => import('@/pages/admin/subscriptions/SubscriptionPlansList.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'subscription-plans/create',
        name: 'CreateSubscriptionPlan',
        component: () => import('@/pages/admin/subscriptions/SubscriptionPlanDetail.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'subscription-plans/:id/edit',
        name: 'EditSubscriptionPlan',
        component: () => import('@/pages/admin/subscriptions/SubscriptionPlanDetail.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'subscriptions',
        name: 'AdminSubscriptions',
        component: () => import('@/pages/subscriptions/SubscriptionsList.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'fbr-submissions',
        name: 'AdminFbrSubmissions',
        component: () => import('@/pages/admin/FbrSubmissionsAdminList.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
      {
        path: 'fbr-submissions/:id',
        name: 'AdminFbrSubmissionDetail',
        component: () => import('@/pages/admin/FbrSubmissionAdminDetail.vue'),
        meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] },
      },
    ],
  },
  
  // Companies Routes
  {
    path: '/companies',
    children: [
      {
        path: '',
        name: 'CompaniesList',
        component: () => import('@/pages/companies/CompaniesList.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: ':id',
        name: 'CompanyDetail',
        component: () => import('@/pages/companies/CompanyDetail.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },

  // Users Routes
  {
    path: '/users',
    children: [
      {
        path: '',
        name: 'UsersList',
        component: () => import('@/pages/users/UsersList.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: ':id',
        name: 'GenericUserDetail',
        component: () => import('@/pages/users/UserDetail.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },

  // POS Routes
  {
    path: '/pos',
    children: [
      // Products
      {
        path: 'products',
        children: [
          {
            path: '',
            name: 'ProductsList',
            component: () => import('@/pages/pos/products/ProductsList.vue'),
            meta: { requiresAuth: true },
          },
          {
            path: 'create',
            name: 'CreateProduct',
            component: () => import('@/pages/pos/products/CreateProduct.vue'),
            meta: { requiresAuth: true },
          },
          {
            path: ':id',
            name: 'ProductDetail',
            component: () => import('@/pages/pos/products/ProductDetail.vue'),
            meta: { requiresAuth: true },
          },
        ],
      },
      // Categories
      {
        path: 'categories',
        name: 'CategoriesList',
        component: () => import('@/pages/pos/categories/CategoriesList.vue'),
        meta: { requiresAuth: true },
      },
      // HS Codes
      {
        path: 'hs-codes',
        name: 'HSCodesList',
        component: () => import('@/pages/pos/hscodes/HSCodesList.vue'),
        meta: { requiresAuth: true },
      },
      // Customers
      {
        path: 'customers',
        name: 'CustomersList',
        component: () => import('@/pages/pos/customers/CustomersList.vue'),
        meta: { requiresAuth: true },
      },
      // Sales
      {
        path: 'sales',
        children: [
          {
            path: '',
            name: 'SalesList',
            component: () => import('@/pages/pos/sales/SalesList.vue'),
            meta: { requiresAuth: true },
          },
          {
            path: 'new',
            name: 'CreateSale',
            component: () => import('@/pages/pos/sales/CreateSale.vue'),
            meta: { requiresAuth: true },
          },
          {
            path: ':id',
            name: 'SaleDetail',
            component: () => import('@/pages/pos/sales/SaleDetail.vue'),
            meta: { requiresAuth: true },
          },
        ],
      },
      // Cash Sessions
      {
        path: 'cash-sessions',
        name: 'CashSessionsList',
        component: () => import('@/pages/pos/cash-sessions/CashSessionsList.vue'),
        meta: { requiresAuth: true },
      },
      // Returns
      {
        path: 'returns',
        name: 'ReturnsList',
        component: () => import('@/pages/pos/returns/ReturnsList.vue'),
        meta: { requiresAuth: true },
      },
      // Debit Notes
      {
        path: 'debit-notes',
        name: 'DebitNotesList',
        component: () => import('@/pages/pos/debit-notes/DebitNotesList.vue'),
        meta: { requiresAuth: true },
      },
      // Payment Methods
      {
        path: 'payment-methods',
        name: 'PaymentMethods',
        component: () => import('@/pages/pos/PaymentMethods.vue'),
        meta: { requiresAuth: true },
      },
      // Branches
      {
        path: 'branches',
        name: 'BranchesPage',
        component: () => import('@/pages/pos/BranchesPage.vue'),
        meta: { requiresAuth: true },
      },
      // Warehouses
      {
        path: 'warehouses',
        name: 'WarehousesPage',
        component: () => import('@/pages/pos/WarehousesPage.vue'),
        meta: { requiresAuth: true },
      },
      // Warehouse Stock
      {
        path: 'stock',
        name: 'WarehouseStockPage',
        component: () => import('@/pages/pos/WarehouseStockPage.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },

  // Digital Invoicing Routes
  {
    path: '/invoicing',
    children: [
      {
        path: '',
        name: 'FbrOverview',
        component: () => import('@/pages/digital_invoicing/FbrOverview.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: 'setup',
        name: 'FbrSetup',
        component: () => import('@/pages/digital_invoicing/FbrSetup.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: 'scenarios',
        name: 'fbr-scenarios',
        component: () => import('@/pages/digital_invoicing/FbrScenarios.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: 'logs',
        name: 'fbr-logs',
        component: () => import('@/pages/digital_invoicing/FbrSubmissionLog.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },

  // Subscriptions Routes
  {
    path: '/subscriptions',
    name: 'SubscriptionsList',
    component: () => import('@/pages/subscriptions/SubscriptionsList.vue'),
    meta: { requiresAuth: true },
  },

  // Reports Routes
  {
    path: '/reports',
    children: [
      {
        path: '',
        name: 'ReportsIndex',
        component: () => import('@/pages/reports/ReportsIndex.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: ':id',
        name: 'ReportDetail',
        component: () => import('@/pages/reports/ReportDetail.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth
  const requiredRole = to.meta.requiredRole as string[] | undefined

  // Don't check auth until store is initialized
  if (!authStore.isInitialized) {
    next()
    return
  }

  // Check authentication
  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Check role if required
  if (requiredRole && authStore.isAuthenticated) {
    if (!requiredRole.includes(authStore.user?.role || '')) {
      next('/login')
      return
    }
  }

  // Redirect authenticated users away from login pages
  if ((to.path === '/login' || to.path === '/login/admin' || to.path === '/login/company') && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }

  next()
})

export default router
