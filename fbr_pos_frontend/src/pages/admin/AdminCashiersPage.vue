<template>
  <div class="space-y-6">
    <div class="flex items-start justify-between gap-4">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-teal-600">Company Staff</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-900">Cashiers, Managers, Salespersons</h1>
        <p class="mt-1 text-sm text-gray-500">Browse staff users created across all companies.</p>
      </div>
    </div>

    <div class="grid gap-4 md:grid-cols-3">
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Managers</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ countByRole('manager') }}</p>
      </div>
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Cashiers</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ countByRole('cashier') }}</p>
      </div>
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Salespersons</p>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ countByRole('salesperson') }}</p>
      </div>
    </div>

    <div class="grid gap-3 md:grid-cols-4">
      <button type="button" @click="setRoleFilter('')" :class="roleButtonClass('')">All staff</button>
      <button type="button" @click="setRoleFilter('manager')" :class="roleButtonClass('manager')">Managers</button>
      <button type="button" @click="setRoleFilter('cashier')" :class="roleButtonClass('cashier')">Cashiers</button>
      <button type="button" @click="setRoleFilter('salesperson')" :class="roleButtonClass('salesperson')">Salespersons</button>
    </div>

    <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
      <div class="relative">
        <svg class="absolute left-3 top-3 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search staff by email, name, company, or terminal"
          class="w-full rounded-xl border border-gray-200 bg-gray-50 py-3 pl-10 pr-4 text-sm outline-none transition focus:border-teal-500 focus:bg-white"
        />
      </div>
    </div>

    <div class="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div v-if="loading" class="p-10 text-center text-sm text-gray-500">Loading staff...</div>
      <div v-else-if="filteredUsers.length === 0" class="p-10 text-center text-sm text-gray-500">No staff users found.</div>
      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Email</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Name</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Role</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Company</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Terminal</th>
            <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="user in filteredUsers" :key="user.id" class="cursor-pointer hover:bg-teal-50" @click="goToUserDetail(user.id)">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ user.email }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ user.full_name || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 capitalize">{{ user.role }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ user.company_name || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ user.terminal_name || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 capitalize">{{ user.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import userAPI, { type User } from '@/apis/admin/userAPI'

const route = useRoute()
const router = useRouter()

const users = ref<User[]>([])
const loading = ref(false)
const searchQuery = ref('')
const roleFilter = ref('')

const loadUsers = async () => {
  loading.value = true
  try {
    const response = await userAPI.getAllUsers()
    users.value = response.filter((user) => ['manager', 'cashier', 'salesperson'].includes(user.role))
  } finally {
    loading.value = false
  }
}

const filteredUsers = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  return users.value.filter((user) => {
    const matchesRole = !roleFilter.value || user.role === roleFilter.value
    const matchesSearch = !query || [user.email, user.full_name, user.company_name, user.terminal_name].join(' ').toLowerCase().includes(query)
    return matchesRole && matchesSearch
  })
})

const countByRole = (role: string) => users.value.filter((user) => user.role === role).length

const setRoleFilter = (role: string) => {
  roleFilter.value = role
  const query = { ...route.query }
  if (role) {
    query.role = role
  } else {
    delete query.role
  }
  router.replace({ query })
}

const roleButtonClass = (role: string) => {
  const base = 'rounded-xl border px-4 py-3 text-sm font-semibold transition text-left'
  const isActive = roleFilter.value === role
  const palette: Record<string, string> = {
    '': isActive ? 'border-teal-500 bg-teal-50 text-teal-700' : 'border-gray-200 bg-white text-gray-700 hover:bg-gray-50',
    manager: isActive ? 'border-orange-500 bg-orange-50 text-orange-700' : 'border-gray-200 bg-white text-gray-700 hover:bg-gray-50',
    cashier: isActive ? 'border-yellow-500 bg-yellow-50 text-yellow-700' : 'border-gray-200 bg-white text-gray-700 hover:bg-gray-50',
    salesperson: isActive ? 'border-indigo-500 bg-indigo-50 text-indigo-700' : 'border-gray-200 bg-white text-gray-700 hover:bg-gray-50',
  }
  return `${base} ${palette[role] || palette['']}`
}

const goToUserDetail = (userId: number) => {
  router.push(`/admin/users/${userId}`)
}

onMounted(() => {
  const queryRole = route.query.role
  if (typeof queryRole === 'string' && ['manager', 'cashier', 'salesperson'].includes(queryRole)) {
    roleFilter.value = queryRole
  }
  loadUsers()
})
</script>