<template>
  <div class="bg-white rounded-lg shadow p-4">
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      <p class="text-2xl font-bold text-gray-900">{{ value }}</p>
    </div>
    <p v-if="change" :class="['mt-2 text-sm', negative ? 'text-red-600' : 'text-green-600']">
      <span v-if="!negative" class="text-green-600">↑</span>
      <span v-else class="text-red-600">↓</span>
      {{ change }}
    </p>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    value: string
    change?: string
    negative?: boolean
  }>(),
  {
    negative: false,
  }
)
</script>
