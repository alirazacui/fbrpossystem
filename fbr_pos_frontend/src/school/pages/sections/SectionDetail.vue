<template>
  <div class="p-8 space-y-6 max-w-3xl">
    <div class="flex items-center gap-3">
      <router-link to="/school/sections" class="text-gray-400 hover:text-gray-700">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </router-link>
      <h1 class="text-2xl font-bold text-gray-900">Section Detail</h1>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    
    <template v-else-if="section">
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-6">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ section.name }}</h2>
            <p class="text-sm font-semibold text-indigo-600 mt-0.5">{{ section.grade_name || 'Grade' }} &middot; {{ section.session_name || 'Session' }}</p>
          </div>
          <router-link :to="`/school/sections/${section.id}/edit`" class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-indigo-700 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            Edit
          </router-link>
        </div>
        
        <div class="grid grid-cols-3 gap-6 border-t border-gray-100 pt-5">
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Class Teacher</p>
            <p class="text-sm font-medium text-gray-800">{{ section.teacher_name || 'Unassigned' }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Room Number</p>
            <p class="text-sm font-medium text-gray-800">{{ section.room_number || '—' }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Capacity</p>
            <p class="text-sm font-medium text-gray-800">{{ section.capacity || '—' }}</p>
          </div>
        </div>
      </div>
      
      <!-- Link to class subject assignments could go here -->
      <div class="bg-gray-50 border border-gray-200 rounded-xl p-6 flex items-center justify-between">
        <div>
          <h3 class="font-bold text-gray-900">Subject Assignments</h3>
          <p class="text-sm text-gray-500 mt-1">Manage which subjects are taught in this section.</p>
        </div>
        <router-link to="/school/class-subjects" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">Manage Subjects →</router-link>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'

const route = useRoute()
const sectionId = route.params.id as string
const section = ref<Section | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await sectionAPI.retrieve(sectionId)
    section.value = res.data
  } catch {
    error.value = 'Failed to load section detail.'
  } finally {
    loading.value = false
  }
})
</script>
