<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      :title="session?.name || 'Session Detail'"
      subtitle="View session information."
      backTo="/school/sessions"
      backLabel="Sessions"
    >
      <template #actions>
        <router-link
          v-if="session"
          :to="`/school/sessions/${session.id}/edit`"
          class="px-6 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          Edit Session
        </router-link>
      </template>
    </SchoolPageHeader>

    <div class="p-8 flex-1 max-w-4xl mx-auto w-full">
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      </div>
      
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-xl px-5 py-4 text-sm flex items-start gap-3">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        {{ error }}
      </div>

      <div v-else-if="session" class="grid grid-cols-3 gap-6">
        <!-- Main Details -->
        <div class="col-span-2">
          <SchoolFormCard title="Overview" subtitle="Session dates and configuration.">
            <div class="grid grid-cols-2 gap-y-6 gap-x-4">
              <div>
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Session Name</p>
                <p class="text-sm font-semibold text-gray-900">{{ session.name }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Status</p>
                <span :class="session.is_active ? 'bg-green-100 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-bold border">
                  {{ session.is_active ? 'Active' : 'Inactive' }}
                </span>
              </div>
              <div>
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Start Date</p>
                <p class="text-sm font-medium text-gray-800">{{ session.start_date || '—' }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">End Date</p>
                <p class="text-sm font-medium text-gray-800">{{ session.end_date || '—' }}</p>
              </div>
            </div>
          </SchoolFormCard>
        </div>

        <!-- Sidebar Widgets -->
        <div class="space-y-6">
          <div class="bg-indigo-50 border border-indigo-100 rounded-xl p-5 shadow-sm">
            <h3 class="text-sm font-bold text-indigo-900 mb-2">Year End Actions</h3>
            <p class="text-xs text-indigo-700 mb-4">When this session ends, you can promote students to the next grade.</p>
            <button class="w-full px-4 py-2 bg-indigo-600 text-white text-xs font-bold rounded-lg hover:bg-indigo-700 shadow-sm opacity-50 cursor-not-allowed">
              Promote Students
            </button>
            <p class="text-[10px] text-indigo-500 mt-2 text-center">Coming soon in Phase 2</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import SchoolPageHeader from '@/school/components/SchoolPageHeader.vue'
import SchoolFormCard from '@/school/components/SchoolFormCard.vue'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'

const route = useRoute()
const sessionId = route.params.id as string

const session = ref<AcademicSession | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await academicSessionAPI.retrieve(sessionId)
    session.value = res.data
  } catch {
    error.value = 'Failed to load session details.'
  } finally {
    loading.value = false
  }
})
</script>
