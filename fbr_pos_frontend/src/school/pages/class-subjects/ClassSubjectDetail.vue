<template>
  <div class="p-8 space-y-6 max-w-3xl">
    <div class="flex items-center gap-3">
      <router-link to="/school/class-subjects" class="text-gray-400 hover:text-gray-700">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </router-link>
      <h1 class="text-2xl font-bold text-gray-900">Assignment Detail</h1>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    
    <template v-else-if="assignment">
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-6">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ assignment.subject_name }}</h2>
            <p class="text-sm font-semibold text-indigo-600 mt-0.5">Assigned to: {{ assignment.section_name }}</p>
          </div>
          <router-link :to="`/school/class-subjects/${assignment.id}/edit`" class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-indigo-700 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            Edit
          </router-link>
        </div>
        
        <div class="grid grid-cols-1 gap-6 border-t border-gray-100 pt-5">
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Assigned Teacher</p>
            <p class="text-sm font-medium text-gray-800">{{ assignment.teacher_name || 'Unassigned' }}</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { classSubjectAssignmentAPI, type ClassSubjectAssignment } from '@/school/apis/classSubjectAssignmentAPI'

const route = useRoute()
const assignmentId = route.params.id as string
const assignment = ref<ClassSubjectAssignment | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await classSubjectAssignmentAPI.retrieve(assignmentId)
    assignment.value = res.data
  } catch {
    error.value = 'Failed to load assignment detail.'
  } finally {
    loading.value = false
  }
})
</script>
