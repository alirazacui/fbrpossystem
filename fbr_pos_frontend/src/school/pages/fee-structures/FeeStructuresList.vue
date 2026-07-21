<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Fee Structures"
      subtitle="Manage fee templates assigned to classes."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Fee Structure
        </button>
      </template>
    </SchoolPageHeader>

    <div class="p-8 flex-1">
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 text-sm flex items-start gap-3">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        {{ error }}
      </div>

      <div v-else-if="structures.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No fee structures found</h3>
        <p class="text-sm text-gray-400 mb-4">Create fee structures to assign to classes for billing.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Add Fee Structure →</button>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Structure Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Academic Session</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Grade / Class</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="structure in structures" :key="structure.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ structure.name }}</td>
              <td class="px-6 py-4 text-gray-600">{{ structure.session_name || '—' }}</td>
              <td class="px-6 py-4 text-gray-600">{{ structure.grade_name || '—' }}</td>
              <td class="px-6 py-4">
                <span :class="structure.is_active ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="px-2.5 py-0.5 rounded-full text-xs font-bold border">
                  {{ structure.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/fee-structures/${structure.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">View Items</router-link>
                  <button @click="openEditModal(structure)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(structure)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      :title="editingStructure ? 'Edit Fee Structure' : 'Create Fee Structure'"
      :subtitle="editingStructure ? 'Update fee structure details' : 'Define a new fee structure for a grade'"
      :submitLabel="editingStructure ? 'Save Changes' : 'Create Structure'"
      :loading="saving"
      maxWidth="lg"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Structure Name <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="e.g. Grade 1 Annual Fee" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Academic Session <span class="text-red-500">*</span></label>
            <select v-model="form.academic_session_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
              <option value="" disabled>Select Session</option>
              <option v-for="s in sessions" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <p v-if="validationErrors.academic_session_id" class="text-red-500 text-xs mt-1">{{ validationErrors.academic_session_id }}</p>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Grade / Class <span class="text-red-500">*</span></label>
            <select v-model="form.grade_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
              <option value="" disabled>Select Grade</option>
              <option v-for="g in grades" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
            <p v-if="validationErrors.grade_id" class="text-red-500 text-xs mt-1">{{ validationErrors.grade_id }}</p>
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Description</label>
          <textarea v-model="form.description" rows="2" placeholder="Optional description..." class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
        </div>

        <div class="mt-2">
          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="form.is_active" type="checkbox" class="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
            <span class="text-sm font-medium text-gray-900">Active</span>
          </label>
        </div>

        <div v-if="serverError" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
          {{ serverError }}
        </div>
      </div>
    </SchoolModal>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Delete Fee Structure"
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
import { feeStructureAPI, type FeeStructure } from '@/school/apis/feeStructureAPI'
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'

const structures = ref<FeeStructure[]>([])
const grades = ref<Grade[]>([])
const sessions = ref<AcademicSession[]>([])

const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<FeeStructure | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingStructure = ref<FeeStructure | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  description: '',
  academic_session_id: '',
  grade_id: '',
  is_active: true
})

const fetchData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [strRes, gRes, sRes] = await Promise.all([
      feeStructureAPI.list(),
      gradeAPI.list(),
      academicSessionAPI.list()
    ])
    structures.value = strRes.data.results || (strRes.data as any)
    grades.value = gRes.data.results || (gRes.data as any)
    sessions.value = sRes.data.results || (sRes.data as any)
  } catch {
    error.value = 'Failed to load fee structures. Please try again.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingStructure.value = null
  const activeSession = sessions.value.find(s => s.is_active)
  
  form.value = { 
    name: '', 
    description: '',
    academic_session_id: activeSession ? activeSession.id : '', 
    grade_id: '', 
    is_active: true 
  }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (structure: FeeStructure) => {
  editingStructure.value = structure
  form.value = {
    name: structure.name,
    description: structure.description || '',
    academic_session_id: structure.academic_session_id,
    grade_id: structure.grade_id,
    is_active: structure.is_active
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
  
  if (!form.value.name) validationErrors.value.name = 'Structure name is required'
  if (!form.value.academic_session_id) validationErrors.value.academic_session_id = 'Session is required'
  if (!form.value.grade_id) validationErrors.value.grade_id = 'Grade is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    if (editingStructure.value) {
      const res = await feeStructureAPI.update(editingStructure.value.id, form.value)
      const index = structures.value.findIndex(s => s.id === editingStructure.value!.id)
      if (index !== -1) structures.value[index] = res.data
    } else {
      const res = await feeStructureAPI.create(form.value)
      structures.value.push(res.data)
    }
    fetchData() // Refresh to get related names
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save fee structure.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (structure: FeeStructure) => { deleteTarget.value = structure }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await feeStructureAPI.delete(deleteTarget.value.id)
    structures.value = structures.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete fee structure.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchData)
</script>
