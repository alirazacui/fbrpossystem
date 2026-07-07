<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-2xl max-w-md w-full">
      <!-- Header -->
      <div class="bg-red-50 border-b border-red-200 px-6 py-4">
        <div class="flex items-center space-x-3">
          <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4v2m0 -8a9 9 0 110 18 9 9 0 010-18z" />
          </svg>
          <h2 class="text-xl font-bold text-red-900">Delete User</h2>
        </div>
      </div>

      <!-- Body -->
      <div class="px-6 py-6">
        <p class="text-gray-700 mb-2">
          Are you sure you want to delete <span class="font-semibold">{{ user?.email }}</span>?
        </p>
        <p class="text-red-600 text-sm font-medium mb-6">
          ⚠️ This action cannot be undone. The user will be permanently removed from the system.
        </p>

        <!-- Footer Actions -->
        <div class="flex space-x-3">
          <button
            @click="closeModal"
            :disabled="loading"
            class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-medium disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            @click="handleDelete"
            :disabled="loading"
            class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            <span v-if="!loading">Delete</span>
            <span v-else class="flex items-center space-x-2">
              <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Deleting...</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import userAPI, { type User } from '@/apis/admin/userAPI'

const props = defineProps<{
  isOpen: boolean
  user: User | null
}>()

const emit = defineEmits<{
  close: []
  userDeleted: []
}>()

const loading = ref(false)

const closeModal = () => {
  emit('close')
}

const handleDelete = async () => {
  if (!props.user) return

  loading.value = true
  try {
    // Assuming deleteUser method exists in userAPI
    await userAPI.deleteUser(props.user.id)
    emit('userDeleted')
    closeModal()
  } catch (err) {
    console.error('Failed to delete user:', err)
    alert('Failed to delete user. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Smooth transitions */
</style>
