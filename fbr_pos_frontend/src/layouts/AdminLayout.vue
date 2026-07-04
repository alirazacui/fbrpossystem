<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <div class="w-64 bg-teal-700 text-white overflow-y-auto">
      <!-- Logo -->
      <div class="p-6 border-b border-teal-600">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-teal-500 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <h2 class="text-lg font-bold">POS System</h2>
            <p class="text-xs text-teal-200">Platform control pane</p>
          </div>
        </div>
      </div>

      <!-- Search -->
      <div class="p-4">
        <div class="relative">
          <input
            type="text"
            placeholder="Search apps and model..."
            class="w-full px-3 py-2 bg-teal-600 text-white placeholder-teal-200 rounded-lg text-sm focus:outline-none focus:bg-teal-500"
          />
          <svg class="w-4 h-4 absolute right-3 top-3 text-teal-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="px-4 py-6 space-y-8 pb-32">
        <!-- Overview -->
        <div>
          <h3 class="text-xs font-semibold text-teal-200 uppercase tracking-wide mb-3">Overview</h3>
          <ul class="space-y-2">
            <li>
              <RouterLink
                to="/dashboard/admin"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/dashboard/admin') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-3m0 0l7-4 7 4M5 9v10a1 1 0 001 1h12a1 1 0 001-1V9m-9 11l4-4m-4 4l-4-4m9-5l4 4m-4-4l-4 4" />
                </svg>
                <span>Dashboard</span>
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Tenants -->
        <div>
          <h3 class="text-xs font-semibold text-teal-200 uppercase tracking-wide mb-3">Tenants</h3>
          <ul class="space-y-2">
            <li>
              <RouterLink
                to="/admin/tenants"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/tenants') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span>Tenants</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/branches"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/branches') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <span>Branches</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/terminals"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/terminals') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Terminals</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/cashiers"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/cashiers') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2.25a1 1 0 001-1V9m0 0a2 2 0 012-2m2 4V7m4 6h.01M19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span>Cashiers</span>
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Billing -->
        <div>
          <h3 class="text-xs font-semibold text-teal-200 uppercase tracking-wide mb-3">Billing</h3>
          <ul class="space-y-2">
            <li>
              <RouterLink
                to="/admin/subscription-plans"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/subscription-plans') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Subscription plans</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/subscriptions"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/subscriptions') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span>Subscriptions</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/platform-settings"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/platform-settings') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>Platform settings</span>
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- People -->
        <div>
          <h3 class="text-xs font-semibold text-teal-200 uppercase tracking-wide mb-3">People</h3>
          <ul class="space-y-2">
            <li>
              <RouterLink
                to="/admin/users"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/users') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 8.048M12 4.354L8.646 7.708M12 4.354l3.354 3.354M9 12a4 4 0 11-8 0 4 4 0 018 0zm12 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <span>Users</span>
              </RouterLink>
            </li>
            <li>
              <a href="#" class="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 8.048M12 4.354L8.646 7.708M12 4.354l3.354 3.354M9 12a4 4 0 11-8 0 4 4 0 018 0zm12 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <span>Groups</span>
              </a>
            </li>
          </ul>
        </div>

        <!-- Operations -->
        <div>
          <h3 class="text-xs font-semibold text-teal-200 uppercase tracking-wide mb-3">Operations</h3>
          <ul class="space-y-2">
            <li>
              <RouterLink
                to="/admin/fbr-submissions"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/fbr-submissions') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>FBR submissions</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/fbr-tokens"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/fbr-tokens') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                <span>FBR tokens</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/invoices"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/invoices') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span>Invoices</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/audit-logs"
                :class="['flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-teal-600 transition', isActive('/admin/audit-logs') ? 'bg-teal-600' : '']"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
                <span>Audit log</span>
              </RouterLink>
            </li>
          </ul>
        </div>
      </nav>

      <!-- Footer -->
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-teal-600 bg-teal-800 w-64">
        <div class="flex items-center space-x-2 text-xs">
          <div class="w-8 h-8 bg-teal-600 rounded-full flex items-center justify-center font-bold">
            {{ authStore.user?.email?.charAt(0).toUpperCase() || 'A' }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium truncate">{{ authStore.user?.email }}</p>
            <p class="text-teal-200 text-xs truncate capitalize">{{ authStore.user?.role || 'Admin' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Bar -->
      <div class="bg-white border-b border-gray-200 px-8 py-4 flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Admin Panel</h2>
        <button @click="handleLogout" class="px-4 py-2 text-red-600 hover:text-red-700 font-medium">
          Logout
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-auto bg-gray-50 p-8">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isActive = (path: string) => {
  return route.path === path
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Smooth transitions */
* {
  transition: background-color 0.2s ease;
}
</style>
