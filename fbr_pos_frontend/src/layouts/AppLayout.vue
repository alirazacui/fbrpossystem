<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <!-- Sidebar Header -->
      <div class="h-16 flex items-center px-4 border-b border-gray-100">
        <div class="w-8 h-8 bg-teal-600 text-white rounded flex items-center justify-center font-bold text-lg mr-3">
          {{ companyInitials }}
        </div>
        <div class="flex flex-col">
          <span class="text-xs font-bold text-gray-900 truncate w-40" :title="companyName">{{ companyName }}</span>
          <span class="text-[10px] font-semibold text-gray-500 tracking-wider uppercase">{{ userRole }}</span>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 py-4 overflow-y-auto custom-scrollbar flex flex-col gap-1">
        <!-- Top Section -->
        <NavLink to="/dashboard" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z'/>" label="Dashboard" />
        <NavLink to="/pos/sales" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'/>" label="Invoices" />
        <NavLink to="/pos/sales/new" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z'/>" label="New invoice" />

        <div v-if="authStore.user?.role === 'owner'" class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Management</p>
        </div>
        <NavLink v-if="authStore.user?.role === 'owner'" to="/company/terminals" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'/>" label="Terminals" />
        <NavLink v-if="authStore.user?.role === 'owner'" to="/company/users" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M17 20h5v-2a4 4 0 00-5-3.87M9 20H4v-2a4 4 0 015-3.87m4-9a4 4 0 110 8 4 4 0 010-8zM15 7a4 4 0 11-8 0 4 4 0 018 0z'/>" label="Users" />

        <!-- CATALOG Section -->
        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Catalog</p>
        </div>
        <NavLink to="/pos/products" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4'/>" label="Products" />
        <NavLink to="/pos/categories" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z'/>" label="Categories" />
        <NavLink to="/pos/hs-codes" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'/>" label="HS codes" />
        <NavLink to="/pos/fbr-readiness" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'/>" label="FBR readiness" />

        <!-- WAREHOUSE Section -->
        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Warehouse</p>
        </div>
        <NavLink to="/pos/stock" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4'/>" label="Stock" />
        <NavLink to="/pos/warehouses" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4'/>" label="Warehouses" />

        <!-- ADMIN Section -->
        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Admin</p>
        </div>
        <NavLink to="/pos/branches" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6'/>" label="Branches" />
        <NavLink to="/pos/payment-methods" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z'/>" label="Payment methods" />
        <NavLink to="/pos/customers" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z'/>" label="Customers" />
        <NavLink to="/reports" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'/>" label="Reports" />

        <NavLink to="/invoicing" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M13 10V3L4 14h7v7l9-11h-7z'/>" label="FBR" />
        <NavLink to="/help" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'/>" label="Help" />
        <NavLink to="/settings" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'/><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 12a3 3 0 11-6 0 3 3 0 016 0z'/>" label="Settings" />
      </nav>

      <!-- Sidebar Footer -->
      <div class="p-4 border-t border-gray-100 flex items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-teal-500"></div>
        <span class="text-xs text-gray-500 font-medium">FBR compliant build</span>
      </div>
    </aside>

    <!-- Page Content -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Top Header Bar -->
      <header class="h-16 flex items-center px-8 bg-white border-b border-gray-100 flex-shrink-0">
        <div class="flex items-center">
          <!-- Lock Icon -->
          <svg class="w-4 h-4 text-teal-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          <span class="font-bold text-gray-800 text-sm tracking-wide mr-3">{{ companyName }}</span>
          <span class="text-xs text-gray-400 font-medium">NTN Available Soon</span>
        </div>
        <div class="ml-auto flex items-center gap-4">
          <button @click="handleLogout" class="text-xs font-semibold text-gray-500 hover:text-gray-800 transition-colors">
            Log out
          </button>
          <div class="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center text-teal-700 font-bold text-sm">
            {{ userInitials }}
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-auto bg-gray-50">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'
import NavLink from '@/components/common/NavLink.vue'

const router = useRouter()
const authStore = useAuthStore()

const companyName = computed(() => authStore.user?.company_name || 'My Company')
const companyInitials = computed(() => {
  if (companyName.value) {
    return companyName.value.substring(0, 1).toUpperCase()
  }
  return 'C'
})

const userRole = computed(() => {
  return authStore.user?.role?.replace('_', ' ') || 'User'
})

const userInitials = computed(() => {
  if (authStore.user?.first_name) {
    return authStore.user.first_name.substring(0, 1).toUpperCase()
  }
  return 'U'
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 20px;
}
</style>
