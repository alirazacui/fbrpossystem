import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'

// Import page components
import LoginChoicePage from '@/pages/auth/LoginChoicePage.vue'
import AdminLoginPage from '@/pages/auth/AdminLoginPage.vue'
import CompanyOwnerLoginPage from '@/pages/auth/CompanyOwnerLoginPage.vue'
import DashboardPage from '@/pages/dashboard/DashboardPage.vue'
import LandingPage from '@/pages/public/LandingPage.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    meta: { requiresAuth: false },
  },
  // ── Public Help Center ───────────────────────────────────────────────────
  {
    path: '/docs/:slug?',
    name: 'DocsPage',
    component: () => import('@/pages/public/DocsPage.vue'),
    meta: { requiresAuth: false },
  },
  // ────────────────────────────────────────────────────────────────────────

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
        path: 'leads',
        name: 'LeadsManagement',
        component: () => import('@/pages/admin/LeadsManagementPage.vue'),
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
        path: 'pos-setup',
        name: 'PosFbrSetup',
        component: () => import('@/pages/digital_invoicing/PosFbrSetup.vue'),
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
  
  // School Routes
  {
    path: '/school',
    children: [
      {
        path: 'dashboard',
        name: 'SchoolDashboard',
        component: () => import('@/school/pages/SchoolDashboard.vue'),
        meta: { requiresAuth: true },
      },
      // Academic Sessions
      { path: 'sessions', name: 'SessionsList', component: () => import('@/school/pages/sessions/SessionsList.vue'), meta: { requiresAuth: true } },
      { path: 'sessions/:id', name: 'SessionDetail', component: () => import('@/school/pages/sessions/SessionDetail.vue'), meta: { requiresAuth: true } },
      // Grades
      { path: 'grades', name: 'GradesList', component: () => import('@/school/pages/grades/GradesList.vue'), meta: { requiresAuth: true } },
      { path: 'grades/:id', name: 'GradeDetail', component: () => import('@/school/pages/grades/GradeDetail.vue'), meta: { requiresAuth: true } },
      // Subjects
      { path: 'subjects', name: 'SubjectsList', component: () => import('@/school/pages/subjects/SubjectsList.vue'), meta: { requiresAuth: true } },
      { path: 'subjects/:id', name: 'SubjectDetail', component: () => import('@/school/pages/subjects/SubjectDetail.vue'), meta: { requiresAuth: true } },
      // Staff
      { path: 'staff', name: 'StaffList', component: () => import('@/school/pages/staff/StaffList.vue'), meta: { requiresAuth: true } },
      { path: 'staff/create', name: 'CreateStaff', component: () => import('@/school/pages/staff/CreateStaff.vue'), meta: { requiresAuth: true } },
      { path: 'staff/:id', name: 'StaffDetail', component: () => import('@/school/pages/staff/StaffDetail.vue'), meta: { requiresAuth: true } },
      { path: 'staff/:id/edit', name: 'EditStaff', component: () => import('@/school/pages/staff/EditStaff.vue'), meta: { requiresAuth: true } },
      
      // Phase 2: Sections
      { path: 'sections', name: 'SectionsList', component: () => import('@/school/pages/sections/SectionsList.vue'), meta: { requiresAuth: true } },
      { path: 'sections/:id', name: 'SectionDetail', component: () => import('@/school/pages/sections/SectionDetail.vue'), meta: { requiresAuth: true } },
      
      // Phase 2: Class Subjects
      { path: 'class-subjects', name: 'ClassSubjectsList', component: () => import('@/school/pages/class-subjects/ClassSubjectsList.vue'), meta: { requiresAuth: true } },
      { path: 'class-subjects/:id', name: 'ClassSubjectDetail', component: () => import('@/school/pages/class-subjects/ClassSubjectDetail.vue'), meta: { requiresAuth: true } },
      
      // Phase 2: Guardians
      { path: 'guardians', name: 'GuardiansList', component: () => import('@/school/pages/guardians/GuardiansList.vue'), meta: { requiresAuth: true } },
      { path: 'guardians/create', name: 'CreateGuardian', component: () => import('@/school/pages/guardians/CreateGuardian.vue'), meta: { requiresAuth: true } },
      { path: 'guardians/:id', name: 'GuardianDetail', component: () => import('@/school/pages/guardians/GuardianDetail.vue'), meta: { requiresAuth: true } },
      { path: 'guardians/:id/edit', name: 'EditGuardian', component: () => import('@/school/pages/guardians/EditGuardian.vue'), meta: { requiresAuth: true } },

      // Phase 3: Students
      { path: 'students', name: 'StudentsList', component: () => import('@/school/pages/students/StudentsList.vue'), meta: { requiresAuth: true } },
      { path: 'students/create', name: 'CreateStudent', component: () => import('@/school/pages/students/CreateStudent.vue'), meta: { requiresAuth: true } },
      { path: 'students/:id', name: 'StudentDetail', component: () => import('@/school/pages/students/StudentDetail.vue'), meta: { requiresAuth: true } },
      { path: 'students/:id/edit', name: 'EditStudent', component: () => import('@/school/pages/students/EditStudent.vue'), meta: { requiresAuth: true } },
      
      // Phase 3: Student Guardians
      { path: 'student-guardians', name: 'StudentGuardiansList', component: () => import('@/school/pages/student-guardians/StudentGuardiansList.vue'), meta: { requiresAuth: true } },
      { path: 'student-guardians/create', name: 'CreateStudentGuardian', component: () => import('@/school/pages/student-guardians/CreateStudentGuardian.vue'), meta: { requiresAuth: true } },
      { path: 'student-guardians/:id/edit', name: 'EditStudentGuardian', component: () => import('@/school/pages/student-guardians/EditStudentGuardian.vue'), meta: { requiresAuth: true } },
      
      // Phase 3: Enrollments
      { path: 'enrollments', name: 'EnrollmentsList', component: () => import('@/school/pages/enrollments/EnrollmentsList.vue'), meta: { requiresAuth: true } },
      { path: 'enrollments/create', name: 'CreateEnrollment', component: () => import('@/school/pages/enrollments/CreateEnrollment.vue'), meta: { requiresAuth: true } },
      { path: 'enrollments/:id/edit', name: 'EditEnrollment', component: () => import('@/school/pages/enrollments/EditEnrollment.vue'), meta: { requiresAuth: true } },

      // Attendance
      { path: 'attendance', name: 'AttendanceList', component: () => import('@/school/pages/attendance/AttendanceList.vue'), meta: { requiresAuth: true } },
      { path: 'attendance/create', name: 'CreateAttendance', component: () => import('@/school/pages/attendance/CreateAttendance.vue'), meta: { requiresAuth: true } },
      { path: 'attendance/:id/edit', name: 'EditAttendance', component: () => import('@/school/pages/attendance/EditAttendance.vue'), meta: { requiresAuth: true } },

      // Phase 4: Fee Structures
      { path: 'fee-structures', name: 'FeeStructuresList', component: () => import('@/school/pages/fee-structures/FeeStructuresList.vue'), meta: { requiresAuth: true } },
      { path: 'fee-structures/:id', name: 'FeeStructureDetail', component: () => import('@/school/pages/fee-structures/FeeStructureDetail.vue'), meta: { requiresAuth: true } },

      // Phase 4: Fee Concessions
      { path: 'concessions', name: 'ConcessionsList', component: () => import('@/school/pages/concessions/ConcessionsList.vue'), meta: { requiresAuth: true } },
      { path: 'concessions/create', name: 'CreateConcession', component: () => import('@/school/pages/concessions/CreateConcession.vue'), meta: { requiresAuth: true } },
      { path: 'concessions/:id', name: 'ConcessionDetail', component: () => import('@/school/pages/concessions/ConcessionDetail.vue'), meta: { requiresAuth: true } },
      { path: 'concessions/:id/edit', name: 'EditConcession', component: () => import('@/school/pages/concessions/EditConcession.vue'), meta: { requiresAuth: true } },

      // Phase 4: Fee Invoices
      { path: 'invoices', name: 'InvoicesList', component: () => import('@/school/pages/invoices/InvoicesList.vue'), meta: { requiresAuth: true } },
      { path: 'invoices/create', name: 'CreateInvoice', component: () => import('@/school/pages/invoices/CreateInvoice.vue'), meta: { requiresAuth: true } },
      { path: 'invoices/:id', name: 'InvoiceDetail', component: () => import('@/school/pages/invoices/InvoiceDetail.vue'), meta: { requiresAuth: true } },

      // FBR
      { path: 'fbr', name: 'SchoolFbrSetup', component: () => import('@/school/pages/fbr/SchoolFbrSetup.vue'), meta: { requiresAuth: true } },
      { path: 'fbr/scenarios', name: 'SchoolFbrScenarios', component: () => import('@/school/pages/fbr/SchoolFbrScenarios.vue'), meta: { requiresAuth: true } },
      { path: 'fbr/submissions', name: 'SchoolFbrSubmissions', component: () => import('@/school/pages/fbr/SchoolFbrSubmissions.vue'), meta: { requiresAuth: true } },

      // Phase 5: Exam Types
      { path: 'exam-types', name: 'ExamTypesList', component: () => import('@/school/pages/exam-types/ExamTypesList.vue'), meta: { requiresAuth: true } },

      // Phase 5: Exams
      { path: 'exams', name: 'ExamsList', component: () => import('@/school/pages/exams/ExamsList.vue'), meta: { requiresAuth: true } },
      { path: 'exams/create', name: 'CreateExam', component: () => import('@/school/pages/exams/CreateExam.vue'), meta: { requiresAuth: true } },
      { path: 'exams/:id', name: 'ExamDetail', component: () => import('@/school/pages/exams/ExamDetail.vue'), meta: { requiresAuth: true } },
      { path: 'exams/:id/edit', name: 'EditExam', component: () => import('@/school/pages/exams/EditExam.vue'), meta: { requiresAuth: true } },

      // Phase 5: Exam Results
      { path: 'exam-results', name: 'ExamResultsList', component: () => import('@/school/pages/exam-results/ExamResultsList.vue'), meta: { requiresAuth: true } },
      { path: 'exam-results/create', name: 'CreateExamResult', component: () => import('@/school/pages/exam-results/CreateExamResult.vue'), meta: { requiresAuth: true } },
      { path: 'exam-results/:id/edit', name: 'EditExamResult', component: () => import('@/school/pages/exam-results/EditExamResult.vue'), meta: { requiresAuth: true } },

      // Fee Heads
      { path: 'fee-heads', name: 'FeeHeadsList', component: () => import('@/school/pages/fee-heads/FeeHeadsList.vue'), meta: { requiresAuth: true } },
      { path: 'fee-heads/:id', name: 'FeeHeadDetail', component: () => import('@/school/pages/fee-heads/FeeHeadDetail.vue'), meta: { requiresAuth: true } },
    ]
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
    if (authStore.user?.company_vertical === 'school') {
      next('/school/dashboard')
    } else {
      next('/dashboard')
    }
    return
  }

  // Redirect authenticated users from landing page to dashboard
  if (to.path === '/' && authStore.isAuthenticated) {
    if (authStore.user?.company_vertical === 'school') {
      next('/school/dashboard')
      return
    } else {
      next('/dashboard')
      return
    }
  }

  next()
})

export default router
