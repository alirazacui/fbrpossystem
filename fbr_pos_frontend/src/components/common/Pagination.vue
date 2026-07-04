<template>
  <div class="flex justify-center items-center gap-2 mt-6">
    <button
      @click="previousPage"
      :disabled="page === 1"
      class="px-3 py-2 bg-gray-200 text-gray-700 rounded-md disabled:opacity-50"
    >
      Previous
    </button>
    <span class="text-sm text-gray-600">Page {{ page }} of {{ totalPages }}</span>
    <button
      @click="nextPage"
      :disabled="page >= totalPages"
      class="px-3 py-2 bg-gray-200 text-gray-700 rounded-md disabled:opacity-50"
    >
      Next
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  total: number
  page: number
  pageSize: number
}>()

const emit = defineEmits<{
  changePage: [page: number]
}>()

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

const previousPage = () => {
  if (props.page > 1) {
    emit('changePage', props.page - 1)
  }
}

const nextPage = () => {
  if (props.page < totalPages.value) {
    emit('changePage', props.page + 1)
  }
}
</script>
