<template>
  <div class="px-8 py-8 w-full">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Branches</h1>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-md">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-red-800">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Add Branch Form -->
    <div class="bg-white border border-gray-200 rounded-lg shadow-sm mb-6">
      <div class="px-6 py-4 border-b border-gray-100">
        <h2 class="text-lg font-bold text-gray-900">{{ editingId ? 'Edit branch' : 'Add branch' }}</h2>
      </div>
      <div class="p-6">
        <form @submit.prevent="saveBranch">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <!-- Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name *</label>
              <input type="text" v-model="form.name" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="e.g. Main Branch" />
            </div>
            
            <!-- Code -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Code *</label>
              <input type="text" v-model="form.code" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="e.g. 1234" />
            </div>
            
            <!-- City -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">City *</label>
              <input type="text" v-model="form.city" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="e.g. Lahore" />
            </div>
            
            <!-- Province -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Province *</label>
              <input type="text" v-model="form.province" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50 focus:ring-teal-500 focus:border-teal-500 sm:text-sm" />
            </div>
          </div>
          
          <!-- Address -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-1">Address *</label>
            <input type="text" v-model="form.address" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm" placeholder="Full address" />
          </div>

          <div class="flex items-center gap-3">
            <button type="submit" :disabled="saving" class="inline-flex items-center justify-center px-6 py-2.5 bg-[#198754] border border-transparent rounded shadow-sm text-sm font-medium text-white hover:bg-green-700 focus:outline-none disabled:opacity-50 transition-colors">
              <span v-if="saving">Saving...</span>
              <span v-else class="flex items-center">
                <span class="text-lg mr-2 font-light">+</span> {{ editingId ? 'Update' : 'Add' }}
              </span>
            </button>
            <button v-if="editingId" type="button" @click="cancelEdit" class="inline-flex items-center px-6 py-2.5 bg-white border border-gray-300 rounded shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none transition-colors">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Branches List -->
    <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Name</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Code</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">City</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Province</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Active</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="6" class="px-6 py-10 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
              </td>
            </tr>
            <tr v-else-if="branches.length === 0">
              <td colspan="6" class="px-6 py-10 text-center text-sm text-gray-500 italic">No branches found.</td>
            </tr>
            <tr v-else v-for="branch in branches" :key="branch.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ branch.name }}
                <span v-if="branch.is_default" class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">Default</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">{{ branch.code }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ branch.city }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ branch.province }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span v-if="branch.is_active" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Yes</span>
                <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">No</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="editBranch(branch)" class="text-teal-600 hover:text-teal-900 mr-4 focus:outline-none">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                </button>
                <button v-if="!branch.is_default" @click="confirmDelete(branch)" class="text-red-500 hover:text-red-700 focus:outline-none">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { branchesAPI, type Branch } from '@/apis/tenant/branchesAPI'

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const branches = ref<Branch[]>([])

const initialFormState = {
  name: '',
  code: '',
  city: '',
  province: 'PUNJAB',
  address: '',
  is_active: true
}

const form = reactive({ ...initialFormState })
const editingId = ref<number | null>(null)

const fetchBranches = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await branchesAPI.getAll()
    branches.value = res.data.results || res.data
  } catch (err: any) {
    console.error("Failed to fetch branches", err)
    error.value = err.response?.data?.detail || 'Failed to load branches.'
  } finally {
    loading.value = false
  }
}

const saveBranch = async () => {
  saving.value = true
  error.value = ''
  try {
    if (editingId.value) {
      await branchesAPI.update(editingId.value, form)
    } else {
      await branchesAPI.create(form)
    }
    await fetchBranches()
    cancelEdit()
  } catch (err: any) {
    console.error("Failed to save branch", err)
    error.value = err.response?.data?.detail || err.response?.data?.name?.[0] || 'Failed to save branch. Ensure code is unique.'
  } finally {
    saving.value = false
  }
}

const editBranch = (branch: Branch) => {
  editingId.value = branch.id!
  form.name = branch.name
  form.code = branch.code
  form.city = branch.city
  form.province = branch.province
  form.address = branch.address
  form.is_active = branch.is_active
  
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const cancelEdit = () => {
  editingId.value = null
  Object.assign(form, initialFormState)
  error.value = ''
}

const confirmDelete = async (branch: Branch) => {
  if (confirm(`Are you sure you want to delete branch "${branch.name}"?`)) {
    try {
      await branchesAPI.delete(branch.id!)
      await fetchBranches()
    } catch (err: any) {
      console.error("Failed to delete branch", err)
      alert(err.response?.data?.detail || 'Failed to delete branch.')
    }
  }
}

onMounted(() => {
  fetchBranches()
})
</script>
