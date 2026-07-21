<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Class Subjects"
      subtitle="Assign subjects and teachers to specific sections."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Assign Subject
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

      <div v-else-if="assignments.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No subjects assigned</h3>
        <p class="text-sm text-gray-400 mb-4">Assign subjects to classes and designate teachers.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Assign Subject →</button>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Subject</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Section / Class</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Assigned Teacher</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="assignment in assignments" :key="assignment.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ assignment.subject_name || '—' }}</td>
              <td class="px-6 py-4 text-gray-600">{{ assignment.section_name || '—' }}</td>
              <td class="px-6 py-4 text-gray-600">{{ assignment.teacher_name || 'Unassigned' }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <button @click="openEditModal(assignment)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(assignment)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      :title="editingAssignment ? 'Edit Subject Assignment' : 'Assign Subject'"
      :subtitle="editingAssignment ? 'Update teacher or section' : 'Assign a subject to a section'"
      :submitLabel="editingAssignment ? 'Save Changes' : 'Assign Subject'"
      :loading="saving"
      maxWidth="md"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Section <span class="text-red-500">*</span></label>
          <select v-model="form.section_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
            <option value="" disabled>Select Section</option>
            <option v-for="s in sections" :key="s.id" :value="s.id">{{ s.name }} ({{ s.grade_name || 'No Grade' }})</option>
          </select>
          <p v-if="validationErrors.section_id" class="text-red-500 text-xs mt-1">{{ validationErrors.section_id }}</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Subject <span class="text-red-500">*</span></label>
          <select v-model="form.subject_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
            <option value="" disabled>Select Subject</option>
            <option v-for="sub in subjects" :key="sub.id" :value="sub.id">{{ sub.name }}</option>
          </select>
          <p v-if="validationErrors.subject_id" class="text-red-500 text-xs mt-1">{{ validationErrors.subject_id }}</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Teacher</label>
          <select v-model="form.teacher_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
            <option value="">None / Unassigned</option>
            <option v-for="t in staff" :key="t.id" :value="t.id">{{ t.fullname }}</option>
          </select>
        </div>

        <div v-if="serverError" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
          {{ serverError }}
        </div>
      </div>
    </SchoolModal>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Remove Assignment"
      submitLabel="Delete"
      :loading="deleting"
      maxWidth="sm"
      @close="deleteTarget = null"
      @submit="handleDelete"
    >
      <template v-if="deleteTarget">
        <p class="text-sm text-gray-600">
          Are you sure you want to remove <strong>{{ deleteTarget.subject_name }}</strong> from <strong>{{ deleteTarget.section_name }}</strong>?<br>
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
import { classSubjectAssignmentAPI, type ClassSubjectAssignment } from '@/school/apis/classSubjectAssignmentAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { subjectAPI, type Subject } from '@/school/apis/subjectAPI'
import { staffAPI, type Staff } from '@/school/apis/staffAPI'

const assignments = ref<ClassSubjectAssignment[]>([])
const sections = ref<Section[]>([])
const subjects = ref<Subject[]>([])
const staff = ref<Staff[]>([])

const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<ClassSubjectAssignment | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingAssignment = ref<ClassSubjectAssignment | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  section_id: '',
  subject_id: '',
  teacher_id: ''
})

const fetchData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [assnRes, secRes, subRes, stfRes] = await Promise.all([
      classSubjectAssignmentAPI.list(),
      sectionAPI.list(),
      subjectAPI.list(),
      staffAPI.list()
    ])
    assignments.value = assnRes.data.results || (assnRes.data as any)
    sections.value = secRes.data.results || (secRes.data as any)
    subjects.value = subRes.data.results || (subRes.data as any)
    staff.value = stfRes.data.results || (stfRes.data as any)
  } catch {
    error.value = 'Failed to load assignments.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingAssignment.value = null
  form.value = { section_id: '', subject_id: '', teacher_id: '' }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (assignment: ClassSubjectAssignment) => {
  editingAssignment.value = assignment
  form.value = {
    section_id: assignment.section_id,
    subject_id: assignment.subject_id,
    teacher_id: assignment.teacher_id || ''
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
  
  if (!form.value.section_id) validationErrors.value.section_id = 'Section is required'
  if (!form.value.subject_id) validationErrors.value.subject_id = 'Subject is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    const payload = { ...form.value }
    if (!payload.teacher_id) delete (payload as any).teacher_id

    if (editingAssignment.value) {
      const res = await classSubjectAssignmentAPI.update(editingAssignment.value.id, payload)
      const index = assignments.value.findIndex(s => s.id === editingAssignment.value!.id)
      if (index !== -1) assignments.value[index] = res.data
    } else {
      const res = await classSubjectAssignmentAPI.create(payload)
      assignments.value.push(res.data)
    }
    fetchData() // Refresh relations
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save assignment.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (assignment: ClassSubjectAssignment) => { deleteTarget.value = assignment }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await classSubjectAssignmentAPI.delete(deleteTarget.value.id)
    assignments.value = assignments.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete assignment.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchData)
</script>
