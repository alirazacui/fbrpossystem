<template>
  <div v-if="!loading && branch" class="space-y-6 pb-10">
    <div class="flex items-start justify-between gap-4">
      <div class="space-y-2">
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <RouterLink to="/admin/branches" class="hover:text-gray-900">Tenants</RouterLink>
          <span class="text-gray-300">›</span>
          <RouterLink to="/admin/branches" class="hover:text-gray-900">Branches</RouterLink>
          <span class="text-gray-300">›</span>
          <span class="text-gray-900 font-medium">{{ branch.code }} — {{ branch.name }}</span>
        </div>
        <div class="flex items-center gap-3 flex-wrap">
          <button type="button" class="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="goBack">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.22em] text-teal-600">Branch details</p>
            <h1 class="mt-1 text-3xl font-bold text-gray-900">{{ branch.code }} — {{ branch.name }}</h1>
            <p class="mt-1 text-sm text-gray-500">Edit the branch, move it to another tenant, or jump to tenant pages.</p>
          </div>
        </div>
      </div>

      <div class="relative branch-menu-anchor" @click.stop>
        <button type="button" class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-gray-300 bg-white text-gray-600 shadow-sm hover:bg-gray-50" @click="menuOpen = !menuOpen">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01" />
          </svg>
        </button>

        <div v-if="menuOpen" class="absolute right-0 z-20 mt-2 w-56 rounded-xl border border-gray-200 bg-white py-2 shadow-xl">
          <button type="button" class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50" @click="openTenantEdit">Change selected tenant</button>
          <button type="button" class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50" @click="openTenantDetail">View selected tenant</button>
          <button type="button" class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50" @click="openTenantCreate">Add another tenant</button>
        </div>
      </div>
    </div>

    <div class="grid gap-6 xl:grid-cols-[minmax(0,1.7fr)_minmax(320px,0.9fr)]">
      <div class="rounded-2xl border border-gray-200 bg-white shadow-sm">
        <div class="border-b border-gray-200 px-6 py-4">
          <h2 class="text-lg font-bold text-gray-900">Branch form</h2>
          <p class="text-sm text-gray-500">Changes are saved to the current branch record.</p>
        </div>

        <form class="space-y-6 p-6" @submit.prevent="saveBranch">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Tenant</label>
            <div class="flex gap-3">
              <select v-model="form.company" class="flex-1 rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500">
                <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.business_name }}</option>
              </select>
            </div>
            <p class="mt-2 text-xs text-gray-500">The branch belongs to the selected tenant.</p>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Name</label>
              <input v-model="form.name" type="text" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500" />
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Code</label>
              <input v-model="form.code" type="text" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500" />
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Address</label>
            <textarea v-model="form.address" rows="3" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500"></textarea>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">City</label>
              <input v-model="form.city" type="text" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500" />
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Province</label>
              <select v-model="form.province" class="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm focus:border-teal-500 focus:ring-teal-500">
                <option v-for="province in provinceOptions" :key="province.value" :value="province.value">{{ province.label }}</option>
              </select>
            </div>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <label class="flex items-center gap-3 rounded-xl border border-gray-200 px-4 py-3">
              <input v-model="form.is_active" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
              <span>
                <span class="block text-sm font-medium text-gray-900">Is active</span>
                <span class="block text-xs text-gray-500">Show this branch in POS selection.</span>
              </span>
            </label>
            <label class="flex items-center gap-3 rounded-xl border border-gray-200 px-4 py-3">
              <input v-model="form.is_default" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
              <span>
                <span class="block text-sm font-medium text-gray-900">Is default</span>
                <span class="block text-xs text-gray-500">Primary branch for the tenant.</span>
              </span>
            </label>
          </div>

          <div class="flex flex-wrap items-center gap-3 pt-2">
            <button type="submit" class="rounded-xl bg-teal-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-teal-700">
              Save branch
            </button>
            <button type="button" class="rounded-xl border border-red-200 bg-red-50 px-5 py-2.5 text-sm font-semibold text-red-700 hover:bg-red-100" @click="deleteBranch">
              Delete branch
            </button>
          </div>
        </form>
      </div>

      <div class="space-y-6">
        <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 class="text-lg font-bold text-gray-900">Summary</h2>
          <dl class="mt-4 space-y-4 text-sm">
            <div>
              <dt class="text-gray-500">Id</dt>
              <dd class="font-medium text-gray-900">{{ branch.id }}</dd>
            </div>
            <div>
              <dt class="text-gray-500">Tenant</dt>
              <dd class="font-medium text-gray-900">{{ selectedCompanyName }}</dd>
            </div>
            <div>
              <dt class="text-gray-500">Created at</dt>
              <dd class="font-medium text-gray-900">{{ branch.created_at || 'N/A' }}</dd>
            </div>
          </dl>
        </div>

        <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 class="text-lg font-bold text-gray-900">Record status</h2>
          <div class="mt-4 space-y-4 text-sm">
            <div class="flex items-center justify-between">
              <span class="text-gray-500">Active</span>
              <span :class="form.is_active ? 'bg-emerald-50 text-emerald-700 ring-emerald-200' : 'bg-rose-50 text-rose-700 ring-rose-200'" class="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ring-1">
                <svg v-if="form.is_active" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <svg v-else class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                {{ form.is_active ? 'Yes' : 'No' }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">Default</span>
              <span :class="form.is_default ? 'bg-blue-50 text-blue-700 ring-blue-200' : 'bg-gray-50 text-gray-400 ring-gray-200'" class="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ring-1">
                <svg v-if="form.is_default" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <svg v-else class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                {{ form.is_default ? 'Yes' : 'No' }}
              </span>
            </div>
            <p class="text-xs text-gray-500">Tenant-related actions are available in the three-dot menu at the top-right.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="flex min-h-[50vh] items-center justify-center">
    <div class="h-8 w-8 animate-spin rounded-full border-4 border-teal-600 border-t-transparent"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import companyAPI from '@/apis/admin/companyAPI'
import { branchesAPI } from '@/apis/tenant/branchesAPI'

interface BranchFormState {
  company: number
  name: string
  code: string
  city: string
  province: string
  address: string
  is_active: boolean
  is_default: boolean
}

const route = useRoute()
const router = useRouter()
const branchId = Number(route.params.id)

const loading = ref(true)
const menuOpen = ref(false)
const error = ref('')
const branch = ref<any | null>(null)
const companies = ref<any[]>([])
const form = reactive<BranchFormState>({
  company: 0,
  name: '',
  code: '',
  city: '',
  province: 'PUNJAB',
  address: '',
  is_active: true,
  is_default: false,
})

const provinceOptions = [
  { value: 'PUNJAB', label: 'Punjab' },
  { value: 'SINDH', label: 'Sindh' },
  { value: 'KPK', label: 'Khyber Pakhtunkhwa' },
  { value: 'BALOCHISTAN', label: 'Balochistan' },
  { value: 'ICT', label: 'Islamabad Capital Territory' },
  { value: 'GB', label: 'Gilgit-Baltistan' },
  { value: 'AJK', label: 'Azad Jammu & Kashmir' },
]

const selectedCompanyName = computed(() => {
  return companies.value.find((company) => company.id === form.company)?.business_name || 'N/A'
})

const loadData = async () => {
  loading.value = true
  error.value = ''

  try {
    const [branchResponse, companyResponse] = await Promise.all([
      branchesAPI.getById(branchId),
      companyAPI.getCompanies(),
    ])

    branch.value = branchResponse.data
    companies.value = companyResponse

    form.company = branch.value.company
    form.name = branch.value.name || ''
    form.code = branch.value.code || ''
    form.city = branch.value.city || ''
    form.province = branch.value.province || 'PUNJAB'
    form.address = branch.value.address || ''
    form.is_active = !!branch.value.is_active
    form.is_default = !!branch.value.is_default
  } catch (err: any) {
    console.error('Failed to load branch details', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to load branch details'
  } finally {
    loading.value = false
  }
}

const saveBranch = async () => {
  await branchesAPI.update(branchId, { ...form })
  await loadData()
  alert('Branch saved successfully.')
}

const deleteBranch = async () => {
  const confirmed = window.confirm('Delete this branch? This action cannot be undone.')
  if (!confirmed) return
  await branchesAPI.delete(branchId)
  router.push('/admin/branches')
}

const goBack = () => router.push('/admin/branches')

const openTenantInNewWindow = (path: string) => {
  window.open(path, '_blank', 'noopener,noreferrer')
}

const openTenantEdit = () => {
  openTenantInNewWindow(`/admin/tenants/${form.company}/edit`)
}

const openTenantDetail = () => {
  openTenantInNewWindow(`/admin/tenants/${form.company}`)
}

const openTenantCreate = () => {
  openTenantInNewWindow('/admin/tenants/create')
}

onMounted(() => {
  if (!Number.isNaN(branchId)) {
    loadData()
  }
})

onBeforeUnmount(() => {
  menuOpen.value = false
})
</script>