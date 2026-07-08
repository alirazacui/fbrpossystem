<template>
  <div class="space-y-6">
    <div v-if="createdNotice" class="rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-green-800">
      Tenant {{ createdNotice }} created successfully.
    </div>

    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Tenants Management</h1>
        <p class="text-gray-600 mt-1">Manage all your business clients and their subscriptions</p>
      </div>
      <router-link
        to="/admin/tenants/create"
        class="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition font-medium flex items-center space-x-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>Add New Business</span>
      </router-link>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">Total Tenants</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ companies.length }}</p>
          </div>
          <div class="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">Active</p>
            <p class="text-3xl font-bold text-green-600 mt-2">{{ activeCount }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">Inactive</p>
            <p class="text-3xl font-bold text-gray-600 mt-2">{{ inactiveCount }}</p>
          </div>
          <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16H7v-4m0 0H3m4 0V7m0 0h6m0 0v6m0 0h4m-4 0V7" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">Trial</p>
            <p class="text-3xl font-bold text-blue-600 mt-2">{{ trialCount }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Search & Filter -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center space-x-4">
        <div class="flex-1 relative">
          <svg class="absolute left-3 top-3 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by business name or NTN..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
        </div>

        <select
          v-model="filterStatus"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
        >
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>

        <select
          v-model="filterPlan"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
        >
          <option value="">All Plans</option>
          <option value="trial">Trial</option>
          <option value="starter">Starter</option>
          <option value="pro">Pro</option>
          <option value="premium">Premium</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg shadow p-12 text-center">
      <div class="inline-block">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600"></div>
      </div>
      <p class="mt-4 text-gray-600">Loading tenants...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
      <p class="text-red-700 font-medium">{{ error }}</p>
    </div>

    <!-- Companies Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Business Name</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">NTN</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Owner</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Plan</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Status</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Created</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr
            v-for="company in filteredCompanies"
            :key="company.id"
            class="hover:bg-teal-50 transition"
          >
            <td class="px-6 py-4">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-br from-teal-400 to-teal-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                  {{ company.business_name.charAt(0).toUpperCase() }}
                </div>
                <span class="font-medium text-gray-900">{{ company.business_name }}</span>
              </div>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ company.ntn }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ company.owner_email || '-' }}</td>
            <td class="px-6 py-4 text-sm">
              <span :class="getPlanBadgeClass(company.subscription_plan)">
                {{ capitalize(company.subscription_plan) }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm">
              <span :class="getStatusBadgeClass(company.is_active)">
                {{ company.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">
              {{ formatDate(company.created_at) }}
            </td>
            <td class="px-6 py-4 text-sm space-x-2">
              <button
                @click="viewCompany(company.id)"
                class="px-3 py-1 text-teal-600 hover:bg-teal-50 rounded transition"
              >
                View
              </button>
              <button
                @click="editCompany(company.id)"
                class="px-3 py-1 text-blue-600 hover:bg-blue-50 rounded transition"
              >
                Edit
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredCompanies.length === 0" class="text-center py-12">
        <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <p class="text-gray-600 text-lg">No tenants found</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import companyAPI, { type Company } from '@/apis/admin/companyAPI'

const route = useRoute()
const router = useRouter()

const companies = ref<Company[]>([])
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')
const filterStatus = ref('')
const filterPlan = ref('')
const createdNotice = ref('')

const activeCount = computed(() => companies.value.filter(c => c.is_active).length)
const inactiveCount = computed(() => companies.value.filter(c => !c.is_active).length)
const trialCount = computed(() => companies.value.filter(c => c.subscription_plan === 'trial').length)

const filteredCompanies = computed(() => {
  return companies.value.filter(company => {
    const matchesSearch = !searchQuery.value || 
      company.business_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      company.ntn.includes(searchQuery.value)

    const matchesStatus = !filterStatus.value ||
      (filterStatus.value === 'active' ? company.is_active : !company.is_active)

    const matchesPlan = !filterPlan.value ||
      company.subscription_plan === filterPlan.value

    return matchesSearch && matchesStatus && matchesPlan
  })
})

const loadCompanies = async () => {
  loading.value = true
  error.value = ''
  try {
    companies.value = await companyAPI.getCompanies()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load tenants'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const viewCompany = (id: number) => {
  router.push(`/admin/tenants/${id}`)
}

const editCompany = (id: number) => {
  router.push(`/admin/tenants/${id}/edit`)
}

const capitalize = (str: string) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

const getPlanBadgeClass = (plan: string) => {
  const baseClass = 'px-3 py-1 rounded-full text-sm font-medium'
  switch (plan) {
    case 'trial':
      return `${baseClass} bg-blue-100 text-blue-800`
    case 'starter':
      return `${baseClass} bg-purple-100 text-purple-800`
    case 'pro':
      return `${baseClass} bg-green-100 text-green-800`
    case 'premium':
      return `${baseClass} bg-yellow-100 text-yellow-800`
    default:
      return `${baseClass} bg-gray-100 text-gray-800`
  }
}

const getStatusBadgeClass = (isActive: boolean) => {
  const baseClass = 'px-3 py-1 rounded-full text-sm font-medium'
  return isActive
    ? `${baseClass} bg-green-100 text-green-800`
    : `${baseClass} bg-gray-100 text-gray-800`
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const consumeTenantCreateFlash = () => {
  const flash = sessionStorage.getItem('tenantCreateSuccess')
  if (!flash) {
    return ''
  }

  sessionStorage.removeItem('tenantCreateSuccess')
  try {
    const parsed = JSON.parse(flash)
    return typeof parsed?.name === 'string' && parsed.name.trim() ? parsed.name.trim() : 'New tenant'
  } catch {
    return 'New tenant'
  }
}

onMounted(() => {
  loadCompanies()
  const routeCreated = route.query.created === '1' ? (typeof route.query.name === 'string' && route.query.name.trim() ? route.query.name.trim() : 'New tenant') : ''
  const flashCreated = consumeTenantCreateFlash()
  createdNotice.value = routeCreated || flashCreated
  if (routeCreated) {
    router.replace({ path: '/admin/tenants', query: {} })
  }
})
</script>
