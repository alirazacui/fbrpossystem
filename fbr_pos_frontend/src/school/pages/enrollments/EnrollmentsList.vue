<template>
  <div class="p-8 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Enrollments</h1>
        <p class="text-sm text-gray-500 mt-1">Manage student enrollments across academic sessions.</p>
      </div>
      <router-link to="/school/enrollments/create" class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        New Enrollment
      </router-link>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    
    <div v-else-if="enrollments.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center">
      <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
      <h3 class="text-base font-semibold text-gray-700 mb-1">No enrollments found</h3>
      <router-link to="/school/enrollments/create" class="text-sm text-indigo-600 font-semibold hover:underline">Create Enrollment →</router-link>
    </div>
    
    <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Student</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Session</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Grade & Section</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
            <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="e in enrollments" :key="e.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 font-semibold text-gray-900">{{ e.student_name || 'Unknown' }}</td>
            <td class="px-6 py-4 text-gray-600">{{ e.session_name || 'Unknown' }}</td>
            <td class="px-6 py-4 text-gray-600">{{ e.grade_name || 'Grade' }} — {{ e.section_name || 'Section' }}</td>
            <td class="px-6 py-4">
              <span class="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-full text-xs font-semibold capitalize">{{ e.status }}</span>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex items-center justify-end gap-2">
                <router-link :to="`/school/enrollments/${e.id}/edit`" class="text-xs text-gray-500 hover:text-gray-800 font-semibold">Edit</router-link>
                <button @click="confirmDelete(e)" class="text-xs text-red-500 hover:text-red-700 font-semibold">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Modal -->
    <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-sm mx-4">
        <h3 class="text-base font-bold text-gray-900 mb-2">Delete Enrollment?</h3>
        <p class="text-sm text-gray-500 mb-5">Delete enrollment for <strong>{{ deleteTarget.student_name }}</strong>?</p>
        <div class="flex gap-3 justify-end">
          <button @click="deleteTarget = null" class="px-4 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</button>
          <button @click="handleDelete" :disabled="deleting" class="px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { enrollmentAPI, type Enrollment } from '@/school/apis/enrollmentAPI'

const enrollments = ref<Enrollment[]>([])
const loading = ref(true)
const error = ref('')
const deleteTarget = ref<Enrollment | null>(null)
const deleting = ref(false)

const fetchEnrollments = async () => {
  loading.value = true
  try {
    const res = await enrollmentAPI.list()
    enrollments.value = res.data.results || (res.data as any)
  } catch { error.value = 'Failed to load enrollments.' }
  finally { loading.value = false }
}

const confirmDelete = (e: Enrollment) => { deleteTarget.value = e }
const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await enrollmentAPI.delete(deleteTarget.value.id)
    enrollments.value = enrollments.value.filter(x => x.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch { error.value = 'Failed to delete.' }
  finally { deleting.value = false }
}

onMounted(fetchEnrollments)
</script>
