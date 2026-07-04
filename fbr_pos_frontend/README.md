# FBR POS Frontend - Vue.js

A comprehensive, modular Vue.js 3 frontend for the FBR POS Platform Django backend.

## 📁 Folder Structure

```
src/
├── apis/                          # API Service Layer (organized by module)
│   ├── axiosInstance.ts          # Axios configuration with interceptors
│   ├── auth/                      # Authentication API
│   │   └── authAPI.ts
│   ├── companies/                 # Company Management API
│   ├── users/                     # User Management API
│   ├── pos/                       # Point of Sale APIs
│   │   ├── products/
│   │   │   └── productsAPI.ts
│   │   ├── categories/
│   │   ├── customers/
│   │   ├── sales/
│   │   │   └── salesAPI.ts
│   │   ├── cash-sessions/
│   │   ├── returns/
│   │   └── debit-notes/
│   ├── digital_invoicing/         # FBR Invoicing API
│   ├── subscriptions/             # Subscription API
│   ├── reports/                   # Reports API
│   ├── permissions/               # Permissions API
│   └── receipt/                   # Receipt Generation API
│
├── components/                     # Reusable Vue Components (organized by module)
│   ├── common/                    # Shared components
│   │   ├── StatCard.vue
│   │   ├── LoadingSpinner.vue
│   │   ├── Pagination.vue
│   │   ├── NavLink.vue
│   │   └── ...
│   ├── auth/                      # Authentication components
│   ├── companies/                 # Company components
│   ├── users/                     # User components
│   ├── pos/                       # POS components
│   │   ├── products/
│   │   │   ├── ProductsFilter.vue
│   │   │   └── ProductForm.vue
│   │   ├── categories/
│   │   ├── customers/
│   │   ├── sales/
│   │   ├── cash-sessions/
│   │   ├── returns/
│   │   └── debit-notes/
│   ├── digital_invoicing/
│   ├── subscriptions/
│   ├── reports/
│   ├── permissions/
│   └── receipt/
│
├── pages/                         # Page/View Components (organized by module)
│   ├── auth/                      # Authentication pages
│   │   └── LoginPage.vue
│   ├── dashboard/                 # Dashboard
│   │   └── DashboardPage.vue
│   ├── companies/                 # Company pages
│   │   ├── CompaniesList.vue
│   │   └── CompanyDetail.vue
│   ├── users/                     # User pages
│   ├── pos/                       # POS pages
│   │   ├── products/
│   │   │   ├── ProductsList.vue
│   │   │   └── CreateProduct.vue
│   │   ├── categories/
│   │   ├── customers/
│   │   ├── sales/
│   │   │   ├── SalesList.vue
│   │   │   └── CreateSale.vue
│   │   ├── cash-sessions/
│   │   ├── returns/
│   │   └── debit-notes/
│   ├── digital_invoicing/
│   ├── subscriptions/
│   ├── reports/
│   ├── permissions/
│   └── receipt/
│
├── stores/                        # Pinia State Management (organized by module)
│   ├── auth/
│   │   └── authStore.ts
│   ├── companies/
│   ├── users/
│   ├── pos/
│   │   └── productsStore.ts
│   └── subscriptions/
│
├── router/                        # Vue Router Configuration
│   └── index.ts                   # Route definitions for all modules
│
├── layouts/                       # Layout Components
│   └── AppLayout.vue              # Main application layout
│
├── types/                         # TypeScript Type Definitions
│   └── index.ts                   # All shared types
│
├── utils/                         # Helper Functions & Utilities
│   └── helpers.ts                 # Formatting, validation, etc.
│
├── styles/                        # Global Styles
│   └── main.css                   # Global CSS + Tailwind
│
├── assets/                        # Static Assets
│   ├── images/
│   ├── icons/
│   └── fonts/
│
├── main.ts                        # Application Entry Point
├── App.vue                        # Root Component
└── index.html                     # HTML Template
```

## 🏗️ Architecture Pattern

### APIs (Service Layer)
```
apis/[moduleName]/[feature]/[featureName]API.ts

Example:
apis/pos/products/productsAPI.ts
└─ Exports functions: list(), retrieve(), create(), update(), delete(), search()
└─ Uses axiosInstance with interceptors
└─ Type definitions for request/response payloads
```

### Components (Reusable UI)
```
components/[moduleName]/[feature]/[ComponentName].vue

Example:
components/pos/products/ProductsFilter.vue
└─ Stateless/presentational components
└─ Emit events to parent pages
└─ Use Tailwind CSS for styling
```

### Pages (Views)
```
pages/[moduleName]/[feature]/[FeatureName]Page.vue

Example:
pages/pos/products/ProductsList.vue
└─ Use Pinia stores for state
└─ Call APIs through stores
└─ Compose reusable components
└─ Handle page logic and routing
```

### Stores (State Management - Pinia)
```
stores/[moduleName]/[featureName]Store.ts

Example:
stores/pos/productsStore.ts
└─ State: products, selectedProduct, loading, error
└─ Getters: computed properties (hasProducts, etc.)
└─ Actions: async methods (fetchProducts, createProduct, etc.)
└─ Called from pages/components
```

## 🚀 Key Features

- **Multi-Tenant**: Organized by company with authorization checks
- **Type-Safe**: Full TypeScript support with shared types
- **Modular**: Each backend app has its own api/component/page/store structure
- **Reactive**: Pinia for state management, Vue 3 Composition API
- **API Integration**: Axios with JWT interceptors, error handling, token refresh
- **Responsive**: Tailwind CSS for mobile-friendly design
- **Organized**: Consistent file naming and folder structure

## 📦 Installation & Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Lint code
npm run lint
```

## 🔐 Authentication Flow

1. User enters credentials on LoginPage
2. authAPI.login() is called → gets JWT tokens
3. Tokens stored in localStorage
4. axiosInstance automatically adds Bearer token to requests
5. On token expiry, interceptor triggers refresh flow
6. Router guard checks authentication before route access

## 📡 API Request Pattern

```typescript
// In stores/pos/productsStore.ts
const fetchProducts = async (page = 1) => {
  loading.value = true
  try {
    const response = await productsAPI.list({ page, page_size: 20 })
    products.value = response.data.results
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// In pages/pos/products/ProductsList.vue
const { products, loading } = storeToRefs(productsStore)
onMounted(() => productsStore.fetchProducts())
```

## 🎨 Component Pattern

All components follow:
- Single Responsibility Principle
- Prop-driven (parent → child)
- Event emission (child → parent)
- Tailwind CSS styling
- TypeScript props/emits

## 📱 Responsive Design

- Mobile-first Tailwind utilities
- Grid layouts for multi-column views
- Collapsible navigation for mobile
- Touch-friendly button sizes

## 🔄 State Management Pattern

```typescript
// Store
export const useMyStore = defineStore('my', () => {
  const data = ref([])
  const loading = ref(false)
  
  const fetchData = async () => {
    loading.value = true
    data.value = await api.list()
    loading.value = false
  }
  
  return { data, loading, fetchData }
})

// Component
const store = useMyStore()
const { data, loading } = storeToRefs(store)

onMounted(() => store.fetchData())
```

## 📝 Adding a New Module Feature

1. Create API service: `apis/moduleName/feature/featureAPI.ts`
2. Create Pinia store: `stores/moduleName/featureStore.ts`
3. Create page component: `pages/moduleName/feature/FeaturePage.vue`
4. Create reusable components: `components/moduleName/feature/*.vue`
5. Add routes to `router/index.ts`

## 🎯 Next Steps

- [ ] Setup backend environment variables
- [ ] Install dependencies: `npm install`
- [ ] Start dev server: `npm run dev`
- [ ] Connect to Django backend on localhost:8000
- [ ] Implement specific page components
- [ ] Add more reusable components as needed
- [ ] Configure Tailwind for custom theme
- [ ] Add authentication guards to all routes
- [ ] Implement error handling UI
- [ ] Add loading states and animations

---

**Backend API Base**: http://localhost:8000/api
**Frontend Dev Server**: http://localhost:5173
