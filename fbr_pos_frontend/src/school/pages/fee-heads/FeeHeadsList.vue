<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <SchoolPageHeader
      title="Fee Heads"
      subtitle="Manage different types of fees (Tuition, Admission, Transport, etc)."
    >
      <template #actions>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Add Fee Head
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

      <div v-else-if="feeHeads.length === 0" class="bg-white border border-gray-200 rounded-xl p-16 text-center shadow-sm">
        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No fee heads found</h3>
        <p class="text-sm text-gray-400 mb-4">Create fee categories to start structuring student billing.</p>
        <button @click="openCreateModal" class="text-sm text-indigo-600 font-semibold hover:underline">Add Fee Head →</button>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Fee Head Name</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Type</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">FBR PCT Code</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="head in feeHeads" :key="head.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-semibold text-gray-900">{{ head.name }}</td>
              <td class="px-6 py-4 text-gray-600">
                <span :class="head.is_recurring ? 'bg-blue-50 text-blue-700' : 'bg-gray-100 text-gray-600'" class="px-2 py-0.5 rounded-md text-xs font-medium">
                  {{ head.is_recurring ? 'Recurring' : 'One-Time' }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-600 font-mono text-xs">{{ head.default_pct_code || '—' }}</td>
              <td class="px-6 py-4">
                <span :class="head.is_active ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="px-2.5 py-0.5 rounded-full text-xs font-bold border">
                  {{ head.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="`/school/fee-heads/${head.id}`" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">View</router-link>
                  <button @click="openEditModal(head)" class="text-gray-500 hover:text-gray-900 font-medium text-sm">Edit</button>
                  <button @click="confirmDelete(head)" class="text-red-500 hover:text-red-700 font-medium text-sm">Delete</button>
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
      :title="editingFeeHead ? 'Edit Fee Head' : 'Create Fee Head'"
      :subtitle="editingFeeHead ? 'Update fee details' : 'Add a new type of fee'"
      :submitLabel="editingFeeHead ? 'Save Changes' : 'Create Fee Head'"
      :loading="saving"
      maxWidth="md"
      @close="closeModal"
      @submit="handleModalSubmit"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Fee Head Name <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="e.g. Tuition Fee" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Default FBR PCT Code</label>
          <input v-model="form.default_pct_code" type="text" placeholder="e.g. 98024000" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono" />
          <p class="text-xs text-gray-500 mt-1">If using FBR integration, set the PCT code for this fee type.</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Description</label>
          <textarea v-model="form.description" rows="2" placeholder="Optional description..." class="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
        </div>

        <div class="flex items-center gap-6 mt-2">
          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="form.is_recurring" type="checkbox" class="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
            <span class="text-sm font-medium text-gray-900">Recurring Fee</span>
          </label>

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
      title="Delete Fee Head"
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
import { feeHeadAPI, type FeeHead } from '@/school/apis/feeHeadAPI'

const feeHeads = ref<FeeHead[]>([])
const loading = ref(true)
const error = ref('')

// Delete State
const deleteTarget = ref<FeeHead | null>(null)
const deleting = ref(false)

// Create/Edit State
const isModalOpen = ref(false)
const editingFeeHead = ref<FeeHead | null>(null)
const saving = ref(false)
const serverError = ref('')
const validationErrors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  description: '',
  is_recurring: true,
  default_pct_code: '',
  is_active: true
})

const fetchFeeHeads = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await feeHeadAPI.list()
    feeHeads.value = res.data.results || (res.data as any)
  } catch {
    error.value = 'Failed to load fee heads. Please try again.'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingFeeHead.value = null
  form.value = { name: '', description: '', is_recurring: true, default_pct_code: '', is_active: true }
  validationErrors.value = {}
  serverError.value = ''
  isModalOpen.value = true
}

const openEditModal = (head: FeeHead) => {
  editingFeeHead.value = head
  form.value = {
    name: head.name,
    description: head.description || '',
    is_recurring: head.is_recurring,
    default_pct_code: head.default_pct_code || '',
    is_active: head.is_active
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
  
  if (!form.value.name) validationErrors.value.name = 'Fee head name is required'
  
  if (Object.keys(validationErrors.value).length > 0) return

  saving.value = true
  try {
    if (editingFeeHead.value) {
      const res = await feeHeadAPI.update(editingFeeHead.value.id, form.value)
      const index = feeHeads.value.findIndex(s => s.id === editingFeeHead.value!.id)
      if (index !== -1) feeHeads.value[index] = res.data
    } else {
      const res = await feeHeadAPI.create(form.value)
      feeHeads.value.push(res.data)
    }
    closeModal()
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        validationErrors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to save fee head.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (head: FeeHead) => { deleteTarget.value = head }

const handleDelete = async () => {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await feeHeadAPI.delete(deleteTarget.value.id)
    feeHeads.value = feeHeads.value.filter(s => s.id !== deleteTarget.value!.id)
    deleteTarget.value = null
  } catch {
    serverError.value = 'Failed to delete fee head.'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchFeeHeads)
</script>
