<template>
  <div class="flex flex-col pb-12 h-full bg-gray-50/50 min-h-screen">
    <!-- Welcome Section -->
    <div class="px-8 pt-8 pb-6 flex justify-between items-end border-b border-gray-200 bg-white">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 mb-1">Welcome to the School Portal, {{ userFullName }}.</h1>
        <p class="text-sm text-gray-500">Managing <span class="font-medium text-gray-700">{{ companyName }}</span>.</p>
      </div>
      <p class="text-xs text-gray-400 font-medium tracking-wide">Ready for FBR Submission</p>
    </div>

    <!-- Dashboard Content Placeholder -->
    <div class="px-8 py-8 w-full space-y-6">
      
      <!-- Top KPIs -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Students -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Students</h3>
            <div class="p-1.5 bg-indigo-50 rounded text-indigo-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">--</div>
          <p class="text-xs text-gray-500">Active enrollments</p>
        </div>

        <!-- Teachers/Staff -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Staff</h3>
            <div class="p-1.5 bg-gray-50 rounded text-gray-500">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">--</div>
          <p class="text-xs text-gray-500">Registered</p>
        </div>

        <!-- Pending Invoices -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Unpaid Fees</h3>
            <div class="p-1.5 bg-indigo-50 rounded text-indigo-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">--</div>
          <p class="text-xs text-gray-500">Awaiting collection</p>
        </div>

        <!-- FBR Fails -->
        <div class="bg-white border border-orange-200 rounded-xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xs font-bold text-orange-600 uppercase tracking-wider">FBR Issues</h3>
            <div class="p-1.5 bg-orange-50 rounded text-orange-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
          <div class="text-2xl font-bold text-gray-900 mb-1">--</div>
          <p class="text-xs text-gray-500">Needs attention</p>
        </div>
      </div>
      
      <div class="bg-indigo-50 border border-indigo-100 rounded-xl p-8 flex flex-col items-center justify-center text-center mt-10">
        <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-sm mb-4">
          <svg class="w-8 h-8 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">School Dashboard setup in progress</h2>
        <p class="text-sm text-gray-500 max-w-md">Your API endpoints are ready. This dashboard will soon display real-time charts of your admissions, fee collections, and digital invoice sync status with FBR.</p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth/authStore'

const authStore = useAuthStore()

// User text
const companyName = computed(() => authStore.user?.company_name || 'My School')
const userFullName = computed(() => {
  if (authStore.user?.first_name || authStore.user?.last_name) {
    return `${authStore.user.first_name} ${authStore.user.last_name}`.trim()
  }
  return authStore.user?.email || 'Admin'
})
</script>
