<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      :title="grade?.name || 'Class Detail'"
      subtitle="View class information."
      backTo="/school/grades"
      backLabel="Classes"
    >
      <template #actions>
        <router-link
          v-if="grade"
          :to="`/school/grades/${grade.id}/edit`"
          class="px-6 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          Edit Class
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

      <div v-else-if="grade" class="grid grid-cols-3 gap-6">
        <!-- Main Details -->
        <div class="col-span-2">
          <SchoolFormCard title="Overview" subtitle="Class structure and levels.">
            <div class="grid grid-cols-2 gap-y-6 gap-x-4">
              <div>
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Class Name</p>
                <p class="text-sm font-semibold text-gray-900">{{ grade.name }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Level</p>
                <p class="text-sm font-medium text-gray-800 capitalize">{{ grade.level || '—' }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Display Order</p>
                <p class="text-sm font-medium text-gray-800">{{ grade.display_order }}</p>
              </div>
            </div>
          </SchoolFormCard>
        </div>

        <!-- Sidebar Widgets -->
        <div class="space-y-6">
          <div class="bg-blue-50 border border-blue-100 rounded-xl p-5 shadow-sm">
            <h3 class="text-sm font-bold text-blue-900 mb-2">Sections</h3>
            <p class="text-xs text-blue-700 mb-4">You need to add sections (like Section A, Section B) to this class before adding students.</p>
            <router-link to="/school/sections/create" class="block text-center w-full px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg hover:bg-blue-700 shadow-sm transition-colors">
              Add Section
            </router-link>
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
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'

const route = useRoute()
const gradeId = route.params.id as string

const grade = ref<Grade | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await gradeAPI.retrieve(gradeId)
    grade.value = res.data
  } catch {
    error.value = 'Failed to load class details.'
  } finally {
    loading.value = false
  }
})
</script>
