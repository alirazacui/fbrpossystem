<template>
  <div class="h-full flex flex-col bg-gray-50 overflow-y-auto">
    <!-- Header Area -->
    <div class="bg-white border-b border-gray-200 px-8 py-6 flex-shrink-0">
      <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4 cursor-pointer hover:text-teal-600 transition" @click="$router.push('/reports')">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Reports</span>
      </div>

      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 capitalize">{{ title }}</h1>
        </div>
        <div class="flex items-center space-x-3">
          <button @click="$emit('export', 'csv')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500">
            CSV
          </button>
          <button @click="$emit('export', 'excel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500">
            Excel
          </button>
          <button @click="$emit('export', 'pdf')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500">
            PDF
          </button>
        </div>
      </div>
    </div>

    <!-- Filters Area -->
    <div class="px-8 py-4 bg-white border-b border-gray-200 flex-shrink-0">
      <div class="flex flex-wrap items-end gap-4">
        <div>
          <label class="block text-xs font-medium text-gray-700 uppercase tracking-wider mb-1">From</label>
          <input type="date" v-model="filters.from" class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm px-3 py-2 border" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-700 uppercase tracking-wider mb-1">To</label>
          <input type="date" v-model="filters.to" class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm px-3 py-2 border" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-700 uppercase tracking-wider mb-1">Branch ID</label>
          <input type="text" v-model="filters.branch_id" placeholder="optional" class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm px-3 py-2 border" />
        </div>
        
        <!-- Slot for extra specific filters -->
        <slot name="extra-filters"></slot>

        <div class="flex items-center gap-2">
          <button @click="$emit('run', filters)" class="px-5 py-2 text-sm font-medium text-white bg-teal-600 border border-transparent rounded-md shadow-sm hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500">
            Run
          </button>
        </div>

        <!-- Favorite Actions -->
        <div class="flex items-center gap-2 ml-auto border-l border-gray-200 pl-4">
          <input type="text" v-model="favoriteName" placeholder="Favorite name" class="block w-40 border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500 sm:text-sm px-3 py-2 border" />
          <button class="px-4 py-2 text-sm font-medium text-teal-700 bg-teal-50 border border-teal-200 rounded-md hover:bg-teal-100 transition">
            Save
          </button>
        </div>
      </div>
      <p v-if="hint" class="mt-3 text-sm text-gray-500">This report supports additional filters: {{ hint }}.</p>
    </div>

    <!-- Results Area -->
    <div class="flex-1 p-8">
      <div class="mb-4">
        <h2 class="text-lg font-medium text-gray-900">Results <span class="text-gray-500 text-sm ml-2">{{ rowCount }} rows</span></h2>
      </div>
      
      <div class="bg-white shadow rounded-lg border border-gray-200 overflow-hidden">
        <div v-if="loading" class="p-12 flex justify-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
        </div>
        <div v-else-if="rowCount === 0" class="p-12 text-center text-gray-500">
          No rows for these filters.
        </div>
        <div v-else class="overflow-x-auto">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const props = defineProps<{
  title: string
  hint?: string
  rowCount: number
  loading?: boolean
}>()

const emit = defineEmits(['export', 'run'])

const filters = reactive({
  from: '',
  to: '',
  branch_id: ''
})

const favoriteName = ref('')
</script>
