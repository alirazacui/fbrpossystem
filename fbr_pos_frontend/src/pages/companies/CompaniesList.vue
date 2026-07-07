<template>
  <div class="space-y-6 pb-10">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.24em] text-teal-600">Admin panel</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-900">Branches</h1>
        <p class="mt-1 text-sm text-gray-500">Browse every branch across all tenants, filter it, and jump into a tenant quickly.</p>
      </div>

      <div class="flex items-center gap-3">
        <button
          type="button"
          class="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm transition hover:bg-gray-50"
          @click="reloadData"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v6h6M20 20v-6h-6M5 19a9 9 0 0114-3.36M19 5a9 9 0 00-14 3.36" />
          </svg>
          Refresh
        </button>
      </div>
    </div>

    <div class="grid gap-4 md:grid-cols-3">
      <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Total branches</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ filteredBranches.length }}</p>
      </div>
      <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Tenants</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ companies.length }}</p>
      </div>
      <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Visible after filters</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ filteredBranches.length }}</p>
      </div>
    </div>

    <div class="flex flex-col gap-4 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm lg:flex-row lg:items-center lg:justify-between">
      <div class="relative w-full lg:max-w-2xl">
        <svg class="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          class="w-full rounded-xl border border-gray-300 bg-gray-50 py-3 pl-10 pr-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-teal-500 focus:bg-white focus:ring-2 focus:ring-teal-100"
          placeholder="Search by branch name, code, tenant, city, or province"
        />
      </div>

      <button
        type="button"
        class="inline-flex items-center justify-center gap-2 rounded-xl bg-teal-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-700"
        @click="isFilterPanelOpen = true"
      >
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        Filters
      </button>
    </div>

    <div class="flex flex-wrap gap-2">
      <span v-if="activeFilterCount === 0" class="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">No filters applied</span>
      <span v-else class="rounded-full bg-teal-50 px-3 py-1 text-xs font-medium text-teal-700">{{ activeFilterCount }} filter(s) active</span>
      <button
        v-if="activeFilterCount > 0"
        type="button"
        class="rounded-full bg-white px-3 py-1 text-xs font-medium text-gray-600 ring-1 ring-gray-200 transition hover:bg-gray-50"
        @click="clearFilters"
      >
        Clear filters
      </button>
    </div>

    <div class="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div v-if="loading" class="flex items-center justify-center py-16 text-gray-500">
        <div class="inline-flex items-center gap-3">
          <div class="h-5 w-5 animate-spin rounded-full border-2 border-teal-600 border-t-transparent"></div>
          Loading branches...
        </div>
      </div>

      <div v-else-if="error" class="p-6">
        <div class="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {{ error }}
        </div>
      </div>

      <div v-else-if="filteredBranches.length === 0" class="px-6 py-16 text-center">
        <p class="text-lg font-semibold text-gray-900">No branches found</p>
        <p class="mt-2 text-sm text-gray-500">Try changing your search or filter settings.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">Name</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">Code</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">Tenant</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">City</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">Province</th>
              <th class="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider text-gray-500">Active</th>
              <th class="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider text-gray-500">Default</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 bg-white">
            <tr v-for="branch in filteredBranches" :key="branch.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <RouterLink :to="`/admin/branches/${branch.id}`" class="font-semibold text-teal-700 hover:text-teal-800 hover:underline">
                  {{ branch.name }}
                </RouterLink>
                <div class="text-xs text-gray-500">ID #{{ branch.id }}</div>
              </td>
              <td class="px-6 py-4 text-sm font-mono text-gray-700">{{ branch.code }}</td>
              <td class="px-6 py-4 text-sm text-gray-700">
                <div class="font-medium text-gray-900">{{ getCompanyName(branch.company) }}</div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-700">{{ branch.city }}</td>
              <td class="px-6 py-4 text-sm text-gray-700">{{ formatProvince(branch.province) }}</td>
              <td class="px-6 py-4 text-center">
                <span
                  :class="branch.is_active ? 'bg-emerald-50 text-emerald-700 ring-emerald-200' : 'bg-rose-50 text-rose-700 ring-rose-200'"
                  class="inline-flex h-8 w-8 items-center justify-center rounded-full ring-1"
                >
                  <svg v-if="branch.is_active" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <svg v-else class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <span
                  :class="branch.is_default ? 'bg-blue-50 text-blue-700 ring-blue-200' : 'bg-gray-50 text-gray-400 ring-gray-200'"
                  class="inline-flex h-8 w-8 items-center justify-center rounded-full ring-1"
                >
                  <svg v-if="branch.is_default" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <svg v-else class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="isFilterPanelOpen" class="fixed inset-0 z-40">
        <div class="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" @click="isFilterPanelOpen = false"></div>
        <aside class="absolute right-0 top-0 h-full w-full max-w-md overflow-y-auto bg-white shadow-2xl">
          <div class="flex items-center justify-between border-b border-gray-200 px-6 py-5">
            <div>
              <h2 class="text-lg font-bold text-gray-900">Filter branches</h2>
              <p class="text-sm text-gray-500">Narrow the branch list using tenant and status filters.</p>
            </div>
            <button type="button" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700" @click="isFilterPanelOpen = false">
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-6 px-6 py-5">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Tenant</label>
              <select v-model="filters.companyId" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500">
                <option value="">All tenants</option>
                <option v-for="company in companies" :key="company.id" :value="String(company.id)">{{ company.business_name }}</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Province</label>
              <select v-model="filters.province" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500">
                <option value="">All provinces</option>
                <option v-for="province in provinceOptions" :key="province.value" :value="province.value">{{ province.label }}</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Active status</label>
              <select v-model="filters.isActive" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500">
                <option value="">All</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Default branch</label>
              <select v-model="filters.isDefault" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500">
                <option value="">All</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </div>

            <div class="flex gap-3 pt-2">
              <button type="button" class="flex-1 rounded-xl border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50" @click="clearFilters">
                Reset
              </button>
              <button type="button" class="flex-1 rounded-xl bg-teal-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-teal-700" @click="isFilterPanelOpen = false">
                Done
              </button>
            </div>
          </div>
        </aside>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import companyAPI from '@/apis/admin/companyAPI'
import { branchesAPI } from '@/apis/tenant/branchesAPI'

interface AdminBranchRecord {
  id: number
  company: number
  name: string
  code: string
  city: string
  province: string
  is_active: boolean
  is_default: boolean
  created_at?: string
}

interface AdminCompanySummary {
  id: number
  business_name: string
}

const loading = ref(true)
const error = ref('')
const branches = ref<AdminBranchRecord[]>([])
const companies = ref<AdminCompanySummary[]>([])
const searchQuery = ref('')
const isFilterPanelOpen = ref(false)
const filters = ref({
  companyId: '',
  province: '',
  isActive: '',
  isDefault: '',
})

const provinceOptions = [
  { value: 'PUNJAB', label: 'Punjab', aliases: ['Punjab', 'PUNJAB'] },
  { value: 'SINDH', label: 'Sindh', aliases: ['Sindh', 'SINDH'] },
  { value: 'KPK', label: 'Khyber Pakhtunkhwa', aliases: ['KPK', 'KP', 'Khyber Pakhtunkhwa'] },
  { value: 'BALOCHISTAN', label: 'Balochistan', aliases: ['Balochistan', 'BALOCHISTAN'] },
  { value: 'ICT', label: 'Islamabad Capital Territory', aliases: ['ICT', 'Islamabad', 'Islamabad Capital Territory'] },
  { value: 'GB', label: 'Gilgit-Baltistan', aliases: ['GB', 'Gilgit-Baltistan'] },
  { value: 'AJK', label: 'Azad Jammu & Kashmir', aliases: ['AJK', 'Azad Jammu & Kashmir'] },
]

const provinceLabelMap = new Map<string, string>()
provinceOptions.forEach((province) => {
  province.aliases.forEach((alias) => provinceLabelMap.set(alias.toLowerCase(), province.label))
  provinceLabelMap.set(province.value.toLowerCase(), province.label)
})

const activeFilterCount = computed(() => {
  return [filters.value.companyId, filters.value.province, filters.value.isActive, filters.value.isDefault].filter(Boolean).length
})

const companyNameMap = computed(() => {
  return new Map(companies.value.map((company) => [company.id, company.business_name]))
})

const getCompanyName = (companyId: number) => {
  return companyNameMap.value.get(companyId) || `Tenant #${companyId}`
}

const formatProvince = (province: string) => {
  return provinceLabelMap.get((province || '').toLowerCase()) || province || '-'
}

const provinceMatches = (branchProvince: string, selectedProvince: string) => {
  if (!selectedProvince) return true
  const normalizedBranchProvince = (branchProvince || '').toLowerCase()
  const selectedOption = provinceOptions.find((option) => option.value === selectedProvince)
  if (!selectedOption) return false
  return selectedOption.aliases.some((alias) => alias.toLowerCase() === normalizedBranchProvince)
}

const filteredBranches = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return [...branches.value]
    .filter((branch) => {
      if (filters.value.companyId && String(branch.company) !== filters.value.companyId) return false
      if (!provinceMatches(branch.province, filters.value.province)) return false
      if (filters.value.isActive !== '' && String(branch.is_active) !== filters.value.isActive) return false
      if (filters.value.isDefault !== '' && String(branch.is_default) !== filters.value.isDefault) return false

      if (!query) return true

      const tenantName = getCompanyName(branch.company).toLowerCase()
      const provinceName = formatProvince(branch.province).toLowerCase()
      return [branch.name, branch.code, branch.city, branch.province, provinceName, tenantName]
        .filter(Boolean)
        .some((value) => value.toLowerCase().includes(query))
    })
    .sort((left, right) => {
      const tenantComparison = getCompanyName(left.company).localeCompare(getCompanyName(right.company))
      if (tenantComparison !== 0) return tenantComparison

      if (left.is_default !== right.is_default) {
        return left.is_default ? -1 : 1
      }

      return left.name.localeCompare(right.name)
    })
})

const clearFilters = () => {
  searchQuery.value = ''
  filters.value = {
    companyId: '',
    province: '',
    isActive: '',
    isDefault: '',
  }
}

const reloadData = async () => {
  loading.value = true
  error.value = ''

  try {
    const [branchResponse, companyList] = await Promise.all([
      branchesAPI.getAll(),
      companyAPI.getCompanies(),
    ])

    const branchPayload = branchResponse.data?.results ?? branchResponse.data ?? []
    branches.value = branchPayload.map((branch: any) => ({
      id: branch.id,
      company: branch.company,
      name: branch.name,
      code: branch.code,
      city: branch.city,
      province: branch.province,
      is_active: branch.is_active,
      is_default: branch.is_default,
      created_at: branch.created_at,
    }))

    companies.value = companyList.map((company: any) => ({
      id: company.id,
      business_name: company.business_name,
    }))
  } catch (err: any) {
    console.error('Failed to load branches', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to load branches'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  reloadData()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
