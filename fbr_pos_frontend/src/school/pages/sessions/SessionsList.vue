<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Academic Sessions"
      subtitle="Manage your school's academic years and terms."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Session
        </button>
      </template>
    </SchoolPageHeader>

    <div class="p-8 flex-1">
      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 text-sm flex items-start gap-3">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        {{ error }}
      </div>

      <!-- Empty -->
      <div v-else-if="sessions.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No sessions yet</h3>
        <p class="text-sm text-gray-400 mb-4">Create your first academic session to get started.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Add Session →</button>
      </div>

      <!-- Table -->
      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Session Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Start Date</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">End Date</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="session in sessions" :key="session.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ session.name }}</td>
              <td class="px-6 py-4 text-gray-600">{{ formatDate(session.start_date) }}</td>
              <td class="px-6 py-4 text-gray-600">{{ formatDate(session.end_date) }}</td>
              <td class="px-6 py-4">
                <span
                  :class="session.is_active ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'"
                  class="px-2.5 py-0.5 rounded-full text-xs font-bold border"
                >
                  {{ session.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/sessions/${session.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">View</router-link>
                  <button @click="openEditModal(session)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(session)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <SchoolModal
      :isOpen="isModalOpen"
      :title="editingSession ? 'Edit Session' : 'Create Session'"
      :subtitle="editingSession ? 'Update session details' : 'Define a new academic year or term'"
      :submitLabel="editingSession ? 'Save Changes' : 'Create Session'"
      :loading="saving"
      maxWidth="lg"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="grid grid-cols-2 gap-4">
        <div class="col-span-2">
          <label class="block text-sm font-semibold text-gray-700 mb-1">Session Name <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="e.g. 2026-2027" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Start Date <span class="text-red-500">*</span></label>
          <input v-model="form.start_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.start_date" class="text-red-500 text-xs mt-1">{{ validationErrors.start_date }}</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">End Date <span class="text-red-500">*</span></label>
          <input v-model="form.end_date" type="date" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.end_date" class="text-red-500 text-xs mt-1">{{ validationErrors.end_date }}</p>
        </div>

        <div class="col-span-2 mt-2">
          <label class="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
            <input v-model="form.is_active" type="checkbox" class="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
            <div>
              <span class="block text-sm font-semibold text-gray-900">Set as Active Session</span>
              <span class="block text-xs text-gray-500">Make this the current active academic session.</span>
            </div>
          </label>
        </div>

        <div v-if="serverError" class="col-span-2 bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
          {{ serverError }}
        </div>
      </div>
    </SchoolModal>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Delete Session"
      submitLabel="Delete"
      :loading="deleting"
      maxWidth="sm"
      @close="deleteTarget = null"
      @submit="handleDelete"
    >
      <template v-if="deleteTarget">
        <p class="text-sm text-gray-600">
          Are you sure you want to delete <strong>"{{ deleteTarget.name }}"</strong>?<br>
          <span class="text-red-600 mt-2 block font-medium">This action cannot be undone.</span>
        </p>
      </template>
    </SchoolModal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SchoolPageHeader from '@/school/components/SchoolPageHeader.vue'
import SchoolModal from '@/school/components/SchoolModal.vue'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'

const sessions = ref<AcademicSession[]>([])
const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<AcademicSession | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingSession = ref<AcademicSession | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  start_date: '',
  end_date: '',
  is_active: false
})

const formatDate = (d: string) => d ? new Date(d).toLocaleDateString('en-PK', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'

const fetchSessions = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await academicSessionAPI.list()
    sessions.value = res.data.results || (res.data as any)
  } catch {
    error.value = 'Failed to load sessions. Please try again.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingSession.value = null
  form.value = { name: '', start_date: '', end_date: '', is_active: false }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (session: AcademicSession) => {
  editingSession.value = session
  form.value = {
    name: session.name,
    start_date: session.start_date || '',
    end_date: session.end_date || '',
    is_active: session.is_active
  }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const handleModalSubmit = async () => {
  validationErrors.value = {}
  serverError.value = ''
  
  if (!form.value.name) validationErrors.value.name = 'Session name is required'
  if (!form.value.start_date) validationErrors.value.start_date = 'Start date is required'
  if (!form.value.end_date) validationErrors.value.end_date = 'End date is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    if (editingSession.value) {
      const res = await academicSessionAPI.update(editingSession.value.id, form.value)
      const index = sessions.value.findIndex(s => s.id === editingSession.value!.id)
      if (index !== -1) sessions.value[index] = res.data
    } else {
      const res = await academicSessionAPI.create(form.value)
      sessions.value.push(res.data)
    }
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save session.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (session: AcademicSession) => { deleteTarget.value = session }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await academicSessionAPI.delete(deleteTarget.value.id)
    sessions.value = sessions.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete session.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchSessions)
</script>
