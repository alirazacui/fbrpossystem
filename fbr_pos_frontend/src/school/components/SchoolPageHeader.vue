<!-- SchoolPageHeader.vue — Reusable premium page header for all school pages -->
<template>
  <div class="bg-white border-b border-gray-200 px-8 py-5 sticky top-0 z-20">
    <!-- Breadcrumb -->
    <div v-if="backTo" class="flex items-center gap-2 mb-3 text-sm text-gray-400">
      <router-link :to="backTo" class="w-7 h-7 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400 hover:text-gray-700 mr-1">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </router-link>
      <router-link :to="backTo" class="hover:text-gray-700 transition-colors">{{ backLabel || 'Back' }}</router-link>
      <svg class="w-3.5 h-3.5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      <span class="text-gray-600 font-medium">{{ title }}</span>
    </div>

    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900">{{ title }}</h1>
        <p v-if="subtitle" class="text-sm text-gray-500 mt-0.5">{{ subtitle }}</p>
      </div>
      <div class="flex items-center gap-3">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
  backTo?: string
  backLabel?: string
}>()
</script>
