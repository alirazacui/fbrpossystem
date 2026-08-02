<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <!-- Sidebar Header -->
      <div class="h-16 flex items-center px-4 border-b border-gray-100">
        <div class="w-8 h-8 bg-indigo-600 text-white rounded flex items-center justify-center font-bold text-lg mr-3">
          {{ companyInitials }}
        </div>
        <div class="flex flex-col">
          <span class="text-xs font-bold text-gray-900 truncate w-40" :title="companyName">{{ companyName }}</span>
          <span class="text-[10px] font-semibold text-gray-500 tracking-wider uppercase">{{ userRole }} (School)</span>
        </div>
      </div>

      <nav class="flex-1 py-4 overflow-y-auto custom-scrollbar flex flex-col gap-1">
        <!-- Dashboard Section -->
        <NavLink to="/school/dashboard" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z'/>" label="Dashboard" />

        <!-- ACADEMICS Section -->
        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Academics</p>
        </div>
        <NavLink to="/school/sessions" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'/>" label="Academic Sessions" />
        <NavLink to="/school/grades" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4'/>" label="Classes & Grades" />
        <NavLink to="/school/sections" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z'/>" label="Sections" />
        <NavLink to="/school/subjects" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'/>" label="Subjects" />
        <NavLink to="/school/class-subjects" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01'/>" label="Class Subjects" />

        <!-- PEOPLE Section -->
        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">People</p>
        </div>
        <NavLink to="/school/students" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z'/>" label="Students" />
        <NavLink to="/school/attendance" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01'/>" label="Attendance" />
        <NavLink to="/school/guardians" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M17 20h5v-2a4 4 0 00-5-3.87M9 20H4v-2a4 4 0 015-3.87m4-9a4 4 0 110 8 4 4 0 010-8zM15 7a4 4 0 11-8 0 4 4 0 018 0z'/>" label="Guardians" />
        <NavLink to="/school/student-guardians" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1'/>" label="Guardian Links" />
        <NavLink to="/school/staff" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'/>" label="Staff" />

        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Registrations</p>
        </div>
        <NavLink to="/school/enrollments" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'/>" label="Enrollments" />

        <!-- BILLING Section -->
        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Billing</p>
        </div>
        <NavLink to="/school/fee-heads" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'/>" label="Fee Heads" />
        <NavLink to="/school/fee-structures" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'/>" label="Fee Structures" />
        <NavLink to="/school/concessions" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'/>" label="Fee Concessions" />
        <NavLink to="/school/invoices" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'/>" label="Fee Vouchers" />

        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">FBR Integration</p>
        </div>
        <NavLink to="/school/fbr" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'/>" label="Setup" />
        <NavLink to="/school/fbr/scenarios" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'/>" label="Scenarios" />
        <NavLink to="/school/fbr/submissions" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'/>" label="Logs" />

        <div class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Examinations</p>
        </div>
        <NavLink to="/school/exam-types" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01'/>" label="Exam Types" />
        <NavLink to="/school/exams" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'/>" label="Exams" />
        <NavLink to="/school/exam-results" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01'/>" label="Exam Results" />

        <div v-if="authStore.user?.role === 'owner'" class="mt-4 mb-1 px-6">
          <p class="text-[10px] font-bold tracking-wider text-gray-500 uppercase">Management</p>
        </div>
        <NavLink v-if="authStore.user?.role === 'owner'" to="/school/users" iconSvg="<path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'/>" label="Settings" />
      </nav>

      <!-- Sidebar Footer -->
      <div class="p-4 border-t border-gray-100 flex items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-indigo-500"></div>
        <span class="text-xs text-gray-500 font-medium">School Edition</span>
      </div>
    </aside>

    <!-- Page Content -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Top Header Bar -->
      <header class="h-16 flex items-center px-8 bg-white border-b border-gray-100 flex-shrink-0">
        <div class="flex items-center">
          <!-- Building Icon -->
          <svg class="w-4 h-4 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          <span class="font-bold text-gray-800 text-sm tracking-wide mr-3">{{ companyName }}</span>
          <span class="text-xs text-indigo-400 font-medium bg-indigo-50 px-2 py-0.5 rounded">School Portal</span>
        </div>
        <div class="ml-auto flex items-center gap-4">
          <button @click="handleLogout" class="text-xs font-semibold text-gray-500 hover:text-gray-800 transition-colors">
            Log out
          </button>
          <div class="w-8 h-8 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-700 font-bold text-sm">
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

const companyName = computed(() => authStore.user?.company_name || 'My School')
const companyInitials = computed(() => {
  if (companyName.value) {
    return companyName.value.substring(0, 1).toUpperCase()
  }
  return 'S'
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
