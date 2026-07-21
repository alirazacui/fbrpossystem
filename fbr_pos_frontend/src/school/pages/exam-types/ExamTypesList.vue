<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Exam Types"
      subtitle="Manage the types of examinations (e.g. Midterm, Final)."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Exam Type
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

      <div v-else-if="types.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No exam types found</h3>
        <p class="text-sm text-gray-400 mb-4">Create your first exam type to start scheduling exams.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Add Exam Type →</button>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Exam Type Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Description</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Max Marks</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Passing Marks</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="type in types" :key="type.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ type.name }}</td>
              <td class="px-6 py-4 text-gray-600 truncate max-w-xs">{{ type.description || '—' }}</td>
              <td class="px-6 py-4 text-gray-600">{{ type.max_marks }}</td>
              <td class="px-6 py-4 text-gray-600">{{ type.passing_marks || '—' }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <button @click="openEditModal(type)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(type)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      :title="editingType ? 'Edit Exam Type' : 'Create Exam Type'"
      :subtitle="editingType ? 'Update exam settings' : 'Define a new type of examination'"
      :submitLabel="editingType ? 'Save Changes' : 'Create Exam Type'"
      :loading="saving"
      maxWidth="md"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Exam Type Name <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="e.g. Midterm, Final, Unit Test" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Max Marks <span class="text-red-500">*</span></label>
            <input v-model.number="form.max_marks" type="number" min="1" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            <p v-if="validationErrors.max_marks" class="text-red-500 text-xs mt-1">{{ validationErrors.max_marks }}</p>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Passing Marks</label>
            <input v-model.number="form.passing_marks" type="number" min="0" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Description</label>
          <textarea v-model="form.description" rows="2" placeholder="Optional notes about this exam type..." class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
        </div>

        <div v-if="serverError" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
          {{ serverError }}
        </div>
      </div>
    </SchoolModal>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Delete Exam Type"
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
import { examTypeAPI, type ExamType } from '@/school/apis/examTypeAPI'

const types = ref<ExamType[]>([])
const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<ExamType | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingType = ref<ExamType | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  description: '',
  max_marks: 100,
  passing_marks: null as number | null
})

const fetchTypes = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await examTypeAPI.list()
    types.value = res.data.results || (res.data as any)
  } catch {
    error.value = 'Failed to load exam types.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingType.value = null
  form.value = { name: '', description: '', max_marks: 100, passing_marks: null }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (type: ExamType) => {
  editingType.value = type
  form.value = {
    name: type.name,
    description: type.description || '',
    max_marks: type.max_marks,
    passing_marks: type.passing_marks
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
  
  if (!form.value.name) validationErrors.value.name = 'Exam type name is required'
  if (!form.value.max_marks) validationErrors.value.max_marks = 'Max marks is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    if (editingType.value) {
      const res = await examTypeAPI.update(editingType.value.id, form.value)
      const index = types.value.findIndex(s => s.id === editingType.value!.id)
      if (index !== -1) types.value[index] = res.data
    } else {
      const res = await examTypeAPI.create(form.value)
      types.value.push(res.data)
    }
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save exam type.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (type: ExamType) => { deleteTarget.value = type }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await examTypeAPI.delete(deleteTarget.value.id)
    types.value = types.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete exam type.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchTypes)
</script>
