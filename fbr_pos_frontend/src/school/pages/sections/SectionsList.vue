<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Sections"
      subtitle="Manage sections for your classes."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Section
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
      <div v-else-if="sections.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No sections found</h3>
        <p class="text-sm text-gray-400 mb-4">Create your first section to organize students within a class.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Add Section →</button>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Section Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Class / Grade</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Session</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Room & Teacher</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="section in sections" :key="section.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ section.name }}</td>
              <td class="px-6 py-4 text-gray-600">{{ section.grade_name || '—' }}</td>
              <td class="px-6 py-4 text-gray-600">{{ section.session_name || '—' }}</td>
              <td class="px-6 py-4">
                <div class="text-gray-900">{{ section.teacher_name || 'No Teacher' }}</div>
                <div class="text-xs text-gray-500">Room: {{ section.room_number || '—' }}</div>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/sections/${section.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">View</router-link>
                  <button @click="openEditModal(section)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(section)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      :title="editingSection ? 'Edit Section' : 'Create Section'"
      :subtitle="editingSection ? 'Update section details.' : 'Create a new section for a class.'"
      :submitLabel="editingSection ? 'Save Changes' : 'Create Section'"
      :loading="saving"
      maxWidth="lg"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Section Name <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="e.g. Section A, Rose" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Academic Session <span class="text-red-500">*</span></label>
            <select v-model="form.academic_session_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
              <option value="" disabled>Select Session</option>
              <option v-for="s in academicSessions" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <p v-if="validationErrors.academic_session_id" class="text-red-500 text-xs mt-1">{{ validationErrors.academic_session_id }}</p>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Class / Grade <span class="text-red-500">*</span></label>
            <select v-model="form.grade_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
              <option value="" disabled>Select Grade</option>
              <option v-for="g in grades" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
            <p v-if="validationErrors.grade_id" class="text-red-500 text-xs mt-1">{{ validationErrors.grade_id }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Class Teacher</label>
            <select v-model="form.class_teacher_id" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
              <option value="">None / Unassigned</option>
              <option v-for="t in staff" :key="t.id" :value="t.id">{{ t.fullname }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Room Number</label>
            <input v-model="form.room_number" type="text" placeholder="e.g. 101" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Capacity</label>
          <input v-model.number="form.capacity" type="number" placeholder="e.g. 40" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div v-if="serverError" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
          {{ serverError }}
        </div>
      </div>
    </SchoolModal>

    <!-- Delete Confirm Modal -->
    <SchoolModal
      :isOpen="!!deleteTarget"
      title="Delete Section"
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
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'
import { staffAPI, type Staff } from '@/school/apis/staffAPI'

const sections = ref<Section[]>([])
const grades = ref<Grade[]>([])
const academicSessions = ref<AcademicSession[]>([])
const staff = ref<Staff[]>([])

const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<Section | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingSection = ref<Section | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  grade_id: '',
  academic_session_id: '',
  class_teacher_id: '',
  room_number: '',
  capacity: null as number | null
})

const fetchData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [secRes, gRes, sRes, tRes] = await Promise.all([
      sectionAPI.list(),
      gradeAPI.list(),
      academicSessionAPI.list(),
      staffAPI.list()
    ])
    sections.value = secRes.data.results || (secRes.data as any)
    grades.value = gRes.data.results || (gRes.data as any)
    academicSessions.value = sRes.data.results || (sRes.data as any)
    staff.value = tRes.data.results || (tRes.data as any)
  } catch {
    error.value = 'Failed to load sections. Please try again.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingSection.value = null
  const activeSession = academicSessions.value.find(s => s.is_active)
  
  form.value = { 
    name: '', 
    grade_id: '', 
    academic_session_id: activeSession ? activeSession.id : '', 
    class_teacher_id: '', 
    room_number: '', 
    capacity: null 
  }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (section: Section) => {
  editingSection.value = section
  form.value = {
    name: section.name,
    grade_id: section.grade_id,
    academic_session_id: section.academic_session_id,
    class_teacher_id: section.class_teacher_id || '',
    room_number: section.room_number || '',
    capacity: section.capacity
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
  
  if (!form.value.name) validationErrors.value.name = 'Section name is required'
  if (!form.value.grade_id) validationErrors.value.grade_id = 'Grade is required'
  if (!form.value.academic_session_id) validationErrors.value.academic_session_id = 'Session is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    const payload = { ...form.value }
    if (!payload.class_teacher_id) delete (payload as any).class_teacher_id
    
    if (editingSection.value) {
      const res = await sectionAPI.update(editingSection.value.id, payload)
      const index = sections.value.findIndex(s => s.id === editingSection.value!.id)
      if (index !== -1) sections.value[index] = res.data
    } else {
      const res = await sectionAPI.create(payload)
      sections.value.push(res.data)
    }
    
    // Refresh to get related names populated
    fetchData()
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save section.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (section: Section) => { deleteTarget.value = section }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await sectionAPI.delete(deleteTarget.value.id)
    sections.value = sections.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete section.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchData)
</script>
