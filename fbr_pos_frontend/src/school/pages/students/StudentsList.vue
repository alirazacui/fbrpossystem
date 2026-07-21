<template>
  <div class="p-8 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Students</h1>
        <p class="text-sm text-gray-500 mt-1">Manage all enrolled students.</p>
      </div>
      <router-link to="/school/students/create" class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Add Student
      </router-link>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    
    <div v-else-if="students.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center">
      <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
      <h3 class="text-base font-semibold text-gray-700 mb-1">No students found</h3>
      <router-link to="/school/students/create" class="text-sm text-indigo-600 font-semibold hover:underline">Add Student →</router-link>
    </div>
    
    <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Name / Reg No.</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Current Section</th>
            <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
            <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="s in students" :key="s.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-sm">{{ s.fullname.charAt(0).toUpperCase() }}</div>
                <div>
                  <p class="font-semibold text-gray-900">{{ s.fullname }}</p>
                  <p class="text-xs text-gray-500">{{ s.registration_number || 'No Reg No.' }}</p>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 text-gray-600">{{ s.section_name || 'Unassigned' }}</td>
            <td class="px-6 py-4">
              <span :class="s.status === 'active' ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-500'" class="px-2 py-0.5 rounded-full text-xs font-semibold">{{ s.status === 'active' ? 'Active' : 'Inactive' }}</span>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex items-center justify-end gap-2">
                <router-link :to="`/school/students/${s.id}`" class="text-xs text-indigo-600 hover:text-indigo-800 font-semibold">View</router-link>
                <router-link :to="`/school/students/${s.id}/edit`" class="text-xs text-gray-500 hover:text-gray-800 font-semibold">Edit</router-link>
                <button @click="confirmDelete(s)" class="text-xs text-red-500 hover:text-red-700 font-semibold">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Modal -->
    <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-sm mx-4">
        <h3 class="text-base font-bold text-gray-900 mb-2">Delete Student?</h3>
        <p class="text-sm text-gray-500 mb-5">Delete <strong>{{ deleteTarget.fullname }}</strong>? This action cannot be undone.</p>
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
import { studentAPI, type Student } from '@/school/apis/studentAPI'

const students = ref<Student[]>([])
const loading = ref(true)
const error = ref('')
const deleteTarget = ref<Student | null>(null)
const deleting = ref(false)

const fetchStudents = async () => {
  loading.value = true
  try {
    const res = await studentAPI.list()
    students.value = res.data.results || (res.data as any)
  } catch { error.value = 'Failed to load students.' }
  finally { loading.value = false }
}

const confirmDelete = (s: Student) => { deleteTarget.value = s }
const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await studentAPI.delete(deleteTarget.value.id)
    students.value = students.value.filter(x => x.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch { error.value = 'Failed to delete.' }
  finally { deleting.value = false }
}

onMounted(fetchStudents)
</script>
