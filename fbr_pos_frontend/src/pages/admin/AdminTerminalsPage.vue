<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Terminals</h1>
        <p class="mt-1 text-sm text-gray-600">Manage all tenant terminals from one place.</p>
      </div>
      <button
        class="inline-flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700"
        @click="openCreate"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Terminal
      </button>
    </div>

    <div v-if="error" class="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
      {{ error }}
    </div>

    <div class="rounded-lg bg-white p-4 shadow">
      <div class="grid gap-3 md:grid-cols-3">
        <div class="relative md:col-span-2">
          <svg class="absolute left-3 top-3 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by terminal, branch, or tenant"
            class="w-full rounded-lg border border-gray-200 py-2.5 pl-10 pr-3 text-sm outline-none focus:border-teal-500"
          />
        </div>
        <select v-model="selectedCompanyId" class="rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-teal-500">
          <option value="">All tenants</option>
          <option v-for="company in companies" :key="company.id" :value="String(company.id)">{{ company.business_name }}</option>
        </select>
      </div>
    </div>

    <div class="overflow-hidden rounded-lg bg-white shadow">
      <div v-if="loading" class="p-10 text-center text-sm text-gray-500">Loading terminals...</div>
      <div v-else-if="filteredTerminals.length === 0" class="p-10 text-center text-sm text-gray-500">No terminals found.</div>
      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Name</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Branch</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Tenant</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Status</th>
            <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Last seen</th>
            <th class="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wide text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="terminal in filteredTerminals" :key="terminal.id">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ terminal.name }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ terminal.branch_name || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ terminal.company_name || '-' }}</td>
            <td class="px-6 py-4 text-sm">
              <span :class="terminal.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-600'" class="rounded-full px-2.5 py-1 text-xs font-semibold">
                {{ terminal.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(terminal.last_seen_at || terminal.created_at) }}</td>
            <td class="px-6 py-4 text-right text-sm">
              <div class="inline-flex items-center gap-2">
                <button class="rounded border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50" @click="openEdit(terminal)">Edit</button>
                <button class="rounded border border-rose-200 px-3 py-1.5 text-xs font-medium text-rose-700 hover:bg-rose-50" @click="removeTerminal(terminal)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
      <div class="w-full max-w-2xl rounded-2xl bg-white p-6 shadow-xl">
        <div class="mb-4 flex items-start justify-between">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ isEditMode ? 'Edit Terminal' : 'Add Terminal' }}</h2>
            <p class="mt-1 text-sm text-gray-500">Configure tenant, branch, and device details.</p>
          </div>
          <button class="rounded px-3 py-1 text-sm text-gray-500 hover:bg-gray-100" @click="closeModal">Close</button>
        </div>

        <form class="grid gap-4 md:grid-cols-2" @submit.prevent="saveTerminal">
          <label class="space-y-2 md:col-span-2">
            <span class="text-sm font-medium text-gray-700">Tenant</span>
            <select v-model="form.companyId" required class="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-teal-500" @change="refreshBranchOptions">
              <option value="">Select tenant</option>
              <option v-for="company in companies" :key="company.id" :value="String(company.id)">{{ company.business_name }}</option>
            </select>
          </label>

          <label class="space-y-2 md:col-span-2">
            <span class="text-sm font-medium text-gray-700">Branch</span>
            <select v-model="form.branch" required class="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-teal-500">
              <option value="">Select branch</option>
              <option v-for="branch in modalBranches" :key="branch.id" :value="String(branch.id)">{{ branch.name }} - {{ branch.code }}</option>
            </select>
          </label>

          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Name</span>
            <input v-model="form.name" type="text" required class="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-teal-500" />
          </label>

          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Terminal index</span>
            <input v-model="form.terminal_index" type="text" class="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-teal-500" />
          </label>

          <label class="space-y-2 md:col-span-2">
            <span class="text-sm font-medium text-gray-700">Device fingerprint</span>
            <input v-model="form.device_fingerprint" type="text" class="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-teal-500" />
          </label>

          <label class="flex items-center gap-3 md:col-span-2">
            <input v-model="form.customer_display_enabled" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-teal-600" />
            <span class="text-sm text-gray-700">Customer display enabled</span>
          </label>

          <label class="flex items-center gap-3 md:col-span-2">
            <input v-model="form.is_active" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-teal-600" />
            <span class="text-sm text-gray-700">Terminal active</span>
          </label>

          <div class="md:col-span-2 flex justify-end gap-3 pt-2">
            <button type="button" class="rounded-lg border border-gray-200 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="closeModal">Cancel</button>
            <button type="submit" class="rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700">{{ isEditMode ? 'Save changes' : 'Create terminal' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import companyAPI from '@/apis/admin/companyAPI'
import { branchesAPI, type Branch } from '@/apis/tenant/branchesAPI'
import { terminalsAPI, type Terminal } from '@/apis/tenant/terminalsAPI'

const terminals = ref<Terminal[]>([])
const companies = ref<any[]>([])
const allBranches = ref<Branch[]>([])
const loading = ref(false)
const error = ref('')

const searchQuery = ref('')
const selectedCompanyId = ref('')

const showModal = ref(false)
const isEditMode = ref(false)
const editingTerminalId = ref<string | null>(null)

const form = ref({
  companyId: '',
  branch: '',
  name: '',
  terminal_index: '',
  device_fingerprint: '',
  customer_display_enabled: false,
  is_active: true,
})

const filteredTerminals = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  return terminals.value.filter((terminal) => {
    const companyMatch = !selectedCompanyId.value || String(terminal.company) === selectedCompanyId.value
    const queryMatch =
      !q ||
      [terminal.name, terminal.branch_name, terminal.company_name, terminal.terminal_index, terminal.device_fingerprint]
        .join(' ')
        .toLowerCase()
        .includes(q)
    return companyMatch && queryMatch
  })
})

const modalBranches = computed(() => {
  if (!form.value.companyId) return []
  return allBranches.value.filter((branch) => String(branch.company) === form.value.companyId)
})

const formatDate = (value?: string | null) => (value ? new Date(value).toLocaleString() : '-')

const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [terminalResponse, companyList, branchResponse] = await Promise.all([
      terminalsAPI.getAll(),
      companyAPI.getCompanies(),
      branchesAPI.getAll(),
    ])
    terminals.value = terminalResponse.data?.results || terminalResponse.data || []
    companies.value = companyList
    allBranches.value = branchResponse.data?.results || branchResponse.data || []
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load terminals.'
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  isEditMode.value = false
  editingTerminalId.value = null
  form.value = {
    companyId: '',
    branch: '',
    name: '',
    terminal_index: '',
    device_fingerprint: '',
    customer_display_enabled: false,
    is_active: true,
  }
  showModal.value = true
}

const openEdit = (terminal: Terminal) => {
  isEditMode.value = true
  editingTerminalId.value = terminal.id
  form.value = {
    companyId: String(terminal.company || ''),
    branch: String(terminal.branch || ''),
    name: terminal.name,
    terminal_index: terminal.terminal_index || '',
    device_fingerprint: terminal.device_fingerprint || '',
    customer_display_enabled: Boolean(terminal.customer_display_enabled),
    is_active: Boolean(terminal.is_active),
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const refreshBranchOptions = () => {
  form.value.branch = ''
}

const saveTerminal = async () => {
  error.value = ''
  try {
    const payload = {
      branch: Number(form.value.branch),
      name: form.value.name,
      terminal_index: form.value.terminal_index || undefined,
      device_fingerprint: form.value.device_fingerprint || undefined,
      customer_display_enabled: form.value.customer_display_enabled,
      is_active: form.value.is_active,
    }

    if (isEditMode.value && editingTerminalId.value) {
      await terminalsAPI.update(editingTerminalId.value, payload)
    } else {
      await terminalsAPI.create(payload)
    }

    showModal.value = false
    await loadData()
  } catch (err: any) {
    const payload = err.response?.data
    error.value = payload?.detail || payload?.branch || payload?.name || 'Failed to save terminal.'
  }
}

const removeTerminal = async (terminal: Terminal) => {
  if (!confirm(`Delete terminal "${terminal.name}"?`)) return
  error.value = ''
  try {
    await terminalsAPI.delete(terminal.id)
    await loadData()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to delete terminal.'
  }
}

onMounted(loadData)
</script>