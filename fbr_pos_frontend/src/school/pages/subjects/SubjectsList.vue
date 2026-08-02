<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Subjects"
      subtitle="Manage the subjects offered at your school."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Subject
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

      <div v-else-if="subjects.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No subjects found</h3>
        <p class="text-sm text-gray-400 mb-4">Create your first subject to start building curriculum.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Add Subject →</button>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Subject Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Code</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Description</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="subject in subjects" :key="subject.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ subject.name }}</td>
              <td class="px-6 py-4 text-gray-600 font-mono text-xs">{{ subject.code || '—' }}</td>
              <td class="px-6 py-4 text-gray-600 truncate max-w-xs">{{ subject.description || '—' }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/subjects/${subject.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">View</router-link>
                  <button @click="openEditModal(subject)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(subject)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      :title="editingSubject ? 'Edit Subject' : 'Create Subject'"
      :subtitle="editingSubject ? 'Update subject details' : 'Add a new subject to your curriculum'"
      :submitLabel="editingSubject ? 'Save Changes' : 'Create Subject'"
      :loading="saving"
      maxWidth="md"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Subject Name <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="e.g. Mathematics" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Subject Code</label>
          <input v-model="form.code" type="text" placeholder="e.g. MATH-101" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono" />
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Description</label>
          <textarea v-model="form.description" rows="3" placeholder="Optional description..." class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
        </div>

        <div v-if="serverError" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
          {{ serverError }}
        </div>
      </div>
    </SchoolModal>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Delete Subject"
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
import { subjectAPI, type Subject } from '@/school/apis/subjectAPI'

const subjects = ref<Subject[]>([])
const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<Subject | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingSubject = ref<Subject | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  code: '',
  description: ''
})

const fetchSubjects = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await subjectAPI.list()
    subjects.value = res.data.results || (res.data as any)
  } catch {
    error.value = 'Failed to load subjects. Please try again.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingSubject.value = null
  form.value = { name: '', code: '', description: '' }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (subject: Subject) => {
  editingSubject.value = subject
  form.value = {
    name: subject.name,
    code: subject.code || '',
    description: subject.description || ''
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
  
  if (!form.value.name) validationErrors.value.name = 'Subject name is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    if (editingSubject.value) {
      const res = await subjectAPI.update(editingSubject.value.id, form.value)
      const index = subjects.value.findIndex(s => s.id === editingSubject.value!.id)
      if (index !== -1) subjects.value[index] = res.data
    } else {
      const res = await subjectAPI.create(form.value)
      subjects.value.push(res.data)
    }
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save subject.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (subject: Subject) => { deleteTarget.value = subject }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await subjectAPI.delete(deleteTarget.value.id)
    subjects.value = subjects.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete subject.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchSubjects)
</script>
