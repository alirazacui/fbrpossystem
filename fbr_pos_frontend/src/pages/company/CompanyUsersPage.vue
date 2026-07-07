<template>
  <div class="space-y-6 pb-10">
    <div class="flex items-start justify-between gap-4">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-teal-600">Company</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-900">Users</h1>
        <p class="mt-1 text-sm text-gray-500">Manager, cashier, and salesperson accounts created by you.</p>
      </div>
      <button
        class="inline-flex items-center gap-2 rounded-xl bg-teal-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-700"
        @click="showForm = true"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add User
      </button>
    </div>

    <div v-if="error" class="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
      {{ error }}
    </div>

    <div v-if="terminalError" class="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
      {{ terminalError }}
    </div>

    <div class="grid gap-4 md:grid-cols-3">
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Total users</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ filteredUsers.length }}</p>
      </div>
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Managers</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ countByRole('manager') }}</p>
      </div>
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Cashiers</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ countByRole('cashier') }}</p>
      </div>
    </div>

    <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
      <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div class="relative flex-1">
          <svg class="absolute left-3 top-3 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input v-model="searchQuery" type="text" placeholder="Search users" class="w-full rounded-xl border border-gray-200 bg-gray-50 py-3 pl-10 pr-4 text-sm outline-none transition focus:border-teal-500 focus:bg-white" />
        </div>
        <select v-model="roleFilter" class="rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm outline-none focus:border-teal-500">
          <option value="">All roles</option>
          <option value="manager">Manager</option>
          <option value="cashier">Cashier</option>
          <option value="salesperson">Salesperson</option>
        </select>
      </div>
    </div>

    <div class="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div v-if="loading" class="p-10 text-center text-sm text-gray-500">Loading users...</div>
      <div v-else-if="filteredUsers.length === 0" class="p-10 text-center text-sm text-gray-500">No company users found.</div>
      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Email</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Name</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Role</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Terminal</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 bg-white">
          <tr v-for="user in filteredUsers" :key="user.id">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ user.email }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ user.full_name || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 capitalize">{{ user.role }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ user.terminal_name || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 capitalize">{{ user.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-3xl bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-4 border-b border-gray-100 pb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">Add User</h2>
            <p class="mt-1 text-sm text-gray-500">Create a manager, cashier, or salesperson for this company.</p>
          </div>
          <button class="rounded-lg px-3 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100" @click="showForm = false">Close</button>
        </div>

        <form class="mt-6 grid gap-4 md:grid-cols-2" @submit.prevent="createUser">
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Email</span>
            <input v-model="form.email" type="email" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">First name</span>
            <input v-model="form.first_name" type="text" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Last name</span>
            <input v-model="form.last_name" type="text" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Phone</span>
            <input v-model="form.phone" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Role</span>
            <select v-model="form.role" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500">
              <option value="manager">Manager</option>
              <option value="cashier">Cashier</option>
              <option value="salesperson">Salesperson</option>
            </select>
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Terminal</span>
            <select v-model="form.terminal" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500">
              <option value="">Select terminal</option>
              <option v-for="terminal in terminals" :key="terminal.id" :value="terminal.id">{{ terminal.name }} - {{ terminal.branch_name || 'Branch' }}</option>
            </select>
              <p class="text-xs text-gray-500">Terminal is required for managers and cashiers.</p>
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Password</span>
            <input v-model="form.password" type="password" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Confirm password</span>
            <input v-model="form.confirm_password" type="password" required class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <div class="md:col-span-2 flex items-center justify-end gap-3 pt-2">
            <button type="button" class="rounded-xl border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50" @click="showForm = false">Cancel</button>
            <button type="submit" class="rounded-xl bg-teal-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-teal-700">Create user</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import userAPI, { type User, type CreateCompanyUserRequest } from '@/apis/admin/userAPI'
import { terminalsAPI, type Terminal } from '@/apis/tenant/terminalsAPI'

const users = ref<User[]>([])
const terminals = ref<Terminal[]>([])
const loading = ref(false)
const error = ref('')
const terminalError = ref('')
const showForm = ref(false)
const searchQuery = ref('')
const roleFilter = ref('')

const form = ref<CreateCompanyUserRequest>({
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  role: 'cashier',
  terminal: null,
  password: '',
  confirm_password: '',
})

const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    users.value = await userAPI.getCompanyUsers()
    terminalError.value = ''
    try {
      const terminalsResponse = await terminalsAPI.getAll()
      terminals.value = terminalsResponse.data?.results || terminalsResponse.data || []
    } catch (terminalErr: any) {
      terminals.value = []
      terminalError.value = terminalErr.response?.data?.detail || 'Terminals are not available yet for this company.'
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.error || 'Unable to load company users.'
  } finally {
    loading.value = false
  }
}

const filteredUsers = computed(() => {
  return users.value.filter((user) => {
    const matchesSearch = !searchQuery.value || [user.email, user.full_name, user.terminal_name].join(' ').toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesRole = !roleFilter.value || user.role === roleFilter.value
    return matchesSearch && matchesRole
  })
})

const countByRole = (role: string) => users.value.filter((user) => user.role === role).length

const createUser = async () => {
  error.value = ''
  try {
    await userAPI.createCompanyUser(form.value)
    form.value = {
      email: '',
      first_name: '',
      last_name: '',
      phone: '',
      role: 'cashier',
      terminal: null,
      password: '',
      confirm_password: '',
    }
    showForm.value = false
    await loadData()
  } catch (err: any) {
    const payload = err.response?.data
    error.value = payload?.detail || payload?.terminal || payload?.role || payload?.password || 'Failed to create user.'
  }
}

onMounted(loadData)
</script>