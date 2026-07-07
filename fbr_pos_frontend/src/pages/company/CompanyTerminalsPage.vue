<template>
  <div class="space-y-6 pb-10">
    <div class="flex items-start justify-between gap-4">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-teal-600">Company</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-900">Terminals</h1>
        <p class="mt-1 text-sm text-gray-500">Create terminals first, then assign users to them during creation.</p>
      </div>
      <button
        class="inline-flex items-center gap-2 rounded-xl bg-teal-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-700"
        @click="showForm = true"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Terminal
      </button>
    </div>

    <div v-if="error" class="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
      {{ error }}
    </div>

    <div class="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div v-if="loading" class="p-10 text-center text-sm text-gray-500">Loading terminals...</div>
      <div v-else-if="terminals.length === 0" class="p-10 text-center text-sm text-gray-500">No terminals found.</div>
      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Name</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Branch</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Pairing code</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Last seen</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 bg-white">
          <tr v-for="terminal in terminals" :key="terminal.id">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ terminal.name }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ terminal.branch_name || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ terminal.pairing_code || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ terminal.is_active ? 'Active' : 'Inactive' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(terminal.last_seen_at || terminal.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-3xl bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-4 border-b border-gray-100 pb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">Add Terminal</h2>
            <p class="mt-1 text-sm text-gray-500">Create the terminal before assigning cashiers or managers.</p>
          </div>
          <button class="rounded-lg px-3 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100" @click="showForm = false">Close</button>
        </div>

        <form class="mt-6 grid gap-4 md:grid-cols-2" @submit.prevent="createTerminal">
          <label class="space-y-2 md:col-span-2">
            <span class="text-sm font-medium text-gray-700">Branch</span>
            <select v-model="form.branch" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500">
              <option value="">Select branch</option>
              <option v-for="branch in branches" :key="branch.id" :value="branch.id">{{ branch.name }} - {{ branch.code }}</option>
            </select>
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Name</span>
            <input v-model="form.name" type="text" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Terminal index</span>
            <input v-model="form.terminal_index" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Device fingerprint</span>
            <input v-model="form.device_fingerprint" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">OS version</span>
            <input v-model="form.os_version" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">App version</span>
            <input v-model="form.app_version" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="flex items-center gap-3 rounded-2xl border border-gray-200 px-4 py-3 md:col-span-2">
            <input v-model="form.customer_display_enabled" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-teal-600" />
            <div>
              <p class="text-sm font-medium text-gray-900">Customer display enabled</p>
              <p class="text-xs text-gray-500">Optional second-screen support for the terminal.</p>
            </div>
          </label>
          <div class="md:col-span-2 flex items-center justify-end gap-3 pt-2">
            <button type="button" class="rounded-xl border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50" @click="showForm = false">Cancel</button>
            <button type="submit" class="rounded-xl bg-teal-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-teal-700">Create terminal</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { branchesAPI } from '@/apis/tenant/branchesAPI'
import { terminalsAPI, type Terminal, type CreateTerminalRequest } from '@/apis/tenant/terminalsAPI'

const terminals = ref<Terminal[]>([])
const branches = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const showForm = ref(false)

const form = ref<CreateTerminalRequest>({
  branch: 0,
  name: '',
  device_fingerprint: '',
  terminal_index: '',
  os_version: '',
  app_version: '',
  printer_config: {},
  scanner_config: {},
  drawer_config: {},
  customer_display_enabled: false,
  is_active: true,
})

const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [terminalResponse, branchResponse] = await Promise.all([
      terminalsAPI.getAll(),
      branchesAPI.getAll(),
    ])
    terminals.value = terminalResponse.data?.results || terminalResponse.data || []
    branches.value = branchResponse.data?.results || branchResponse.data || []
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.error || 'Unable to load terminals.'
  } finally {
    loading.value = false
  }
}

const createTerminal = async () => {
  error.value = ''
  try {
    await terminalsAPI.create({
      ...form.value,
      branch: Number(form.value.branch),
    })
    form.value = {
      branch: 0,
      name: '',
      device_fingerprint: '',
      terminal_index: '',
      os_version: '',
      app_version: '',
      printer_config: {},
      scanner_config: {},
      drawer_config: {},
      customer_display_enabled: false,
      is_active: true,
    }
    showForm.value = false
    await loadData()
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.branch || 'Failed to create terminal.'
  }
}

const formatDate = (value?: string | null) => value ? new Date(value).toLocaleString() : '-'

onMounted(loadData)
</script>