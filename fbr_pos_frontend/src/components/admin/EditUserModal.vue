<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-gray-200 px-8 py-6 flex items-center justify-between">
        <h2 class="text-2xl font-bold text-gray-900">Edit User</h2>
        <button
          @click="closeModal"
          class="text-gray-400 hover:text-gray-600 transition"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Body -->
      <div class="px-8 py-6">
        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- Email (Read-only for edit) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
            <input
              :value="formData.email"
              type="email"
              disabled
              class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-600 cursor-not-allowed"
            />
          </div>

          <!-- First Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">First Name</label>
            <input
              v-model="formData.first_name"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              placeholder="John"
            />
          </div>

          <!-- Last Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
            <input
              v-model="formData.last_name"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              placeholder="Doe"
            />
          </div>

          <!-- Phone Number -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
            <input
              v-model="formData.phone"
              type="tel"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              placeholder="+92 300 1234567"
            />
          </div>

          <!-- Password (Optional) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">New Password (Leave blank to keep current)</label>
            <div class="relative">
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600 transition"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg whitespace-pre-wrap">
            {{ error }}
          </div>

          <!-- Form Actions -->
          <div class="flex space-x-3 pt-6">
            <button
              type="button"
              @click="closeModal"
              class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              <span v-if="!loading">Update User</span>
              <span v-else class="flex items-center space-x-2">
                <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Updating...</span>
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import userAPI, { type User } from '@/apis/admin/userAPI'

const props = defineProps<{
  isOpen: boolean
  user: User | null
}>()

const emit = defineEmits<{
  close: []
  userUpdated: []
}>()

const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const formData = reactive({
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  password: '',
})

// Watch for user changes and pre-fill form
watch(() => props.user, (newUser) => {
  if (newUser) {
    formData.email = newUser.email
    formData.first_name = newUser.full_name?.split(' ')[0] || ''
    formData.last_name = newUser.full_name?.split(' ').slice(1).join(' ') || ''
    formData.phone = ''
    formData.password = ''
    error.value = ''
  }
}, { deep: true })

const closeModal = () => {
  emit('close')
}

const handleSubmit = async () => {
  error.value = ''

  // Validation
  if (!formData.email) {
    error.value = 'Email is required'
    return
  }

  loading.value = true

  try {
    const updateData: any = {
      first_name: formData.first_name,
      last_name: formData.last_name,
    }

    // Only include password if provided
    if (formData.password) {
      updateData.password = formData.password
    }

    if (props.user) {
      await userAPI.updateUser(props.user.id, updateData)
      closeModal()
      emit('userUpdated')
    }
  } catch (err: any) {
    // Extract error message from API response
    const data = err.response?.data

    if (typeof data === 'string') {
      error.value = data
    } else if (data?.detail) {
      error.value = data.detail
    } else if (data?.non_field_errors && Array.isArray(data.non_field_errors)) {
      error.value = data.non_field_errors[0]
    } else if (typeof data === 'object') {
      const fieldErrors: string[] = []
      const errorFields = ['first_name', 'last_name', 'phone', 'password']
      for (const field of errorFields) {
        if (data[field] && Array.isArray(data[field])) {
          fieldErrors.push(`${field}: ${data[field][0]}`)
        }
      }
      if (fieldErrors.length > 0) {
        error.value = fieldErrors.join('\n')
      } else {
        error.value = 'Failed to update user. Please try again.'
      }
    } else {
      error.value = 'Failed to update user. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Smooth transitions */
</style>
