<template>
  <div class="space-y-4">
    <div class="flex gap-4 items-end">
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name, SKU, or barcode..."
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          @input="handleSearch"
        />
      </div>
      <button
        @click="handleClear"
        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
      >
        Clear
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  search: [query: string]
}>()

const searchQuery = ref('')

const handleSearch = () => {
  emit('search', searchQuery.value)
}

const handleClear = () => {
  searchQuery.value = ''
  emit('search', '')
}
</script>
