<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Classes & Grades"
      subtitle="Manage the academic classes offered at your school."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Class
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
      <div v-else-if="grades.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No classes yet</h3>
        <p class="text-sm text-gray-400 mb-4">Create your first class to start organizing students.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Add Class →</button>
      </div>

      <!-- Table -->
      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Class Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Level</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Order</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="grade in grades" :key="grade.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ grade.name }}</td>
              <td class="px-6 py-4 text-gray-600 capitalize">{{ grade.level || '—' }}</td>
              <td class="px-6 py-4 text-gray-600">{{ grade.display_order }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/grades/${grade.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">View</router-link>
                  <button @click="openEditModal(grade)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(grade)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      :title="editingGrade ? 'Edit Class' : 'Create Class'"
      :subtitle="editingGrade ? 'Update class level or ordering' : 'Add a new class to your school structure'"
      :submitLabel="editingGrade ? 'Save Changes' : 'Create Class'"
      :loading="saving"
      maxWidth="md"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Class Name <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="e.g. Grade 1" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Level</label>
          <select v-model="form.level" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
            <option value="">Select Level (Optional)</option>
            <option value="preschool">Preschool / Kindergarten</option>
            <option value="primary">Primary (1-5)</option>
            <option value="middle">Middle (6-8)</option>
            <option value="high">High (9-10)</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Display Order <span class="text-red-500">*</span></label>
          <input v-model.number="form.display_order" type="number" min="1" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p class="text-xs text-gray-500 mt-1">Used for promotion ordering (e.g. 1 goes to 2)</p>
          <p v-if="validationErrors.display_order" class="text-red-500 text-xs mt-1">{{ validationErrors.display_order }}</p>
        </div>

        <div v-if="serverError" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
          {{ serverError }}
        </div>
      </div>
    </SchoolModal>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Delete Class"
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
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'

const grades = ref<Grade[]>([])
const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<Grade | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingGrade = ref<Grade | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  level: '',
  display_order: 1
})

const fetchGrades = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await gradeAPI.list()
    grades.value = res.data.results || (res.data as any)
  } catch {
    error.value = 'Failed to load classes. Please try again.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingGrade.value = null
  form.value = { name: '', level: '', display_order: 1 }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (grade: Grade) => {
  editingGrade.value = grade
  form.value = {
    name: grade.name,
    level: grade.level || '',
    display_order: grade.display_order
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
  
  if (!form.value.name) validationErrors.value.name = 'Class name is required'
  if (!form.value.display_order) validationErrors.value.display_order = 'Display order is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    const payload = { ...form.value }
    if (!payload.level) payload.level = null as any

    if (editingGrade.value) {
      const res = await gradeAPI.update(editingGrade.value.id, payload)
      const index = grades.value.findIndex(g => g.id === editingGrade.value!.id)
      if (index !== -1) grades.value[index] = res.data
    } else {
      const res = await gradeAPI.create(payload)
      grades.value.push(res.data)
    }
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save class.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (grade: Grade) => { deleteTarget.value = grade }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await gradeAPI.delete(deleteTarget.value.id)
    grades.value = grades.value.filter(g => g.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete class. It might be in use by students or sections.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchGrades)
</script>
