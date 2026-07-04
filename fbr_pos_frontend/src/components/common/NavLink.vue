<template>
  <RouterLink
    :to="to"
    class="flex items-center gap-3 px-6 py-2.5 text-sm font-medium transition-colors border-l-4"
    :class="[
      isActive 
        ? 'bg-teal-50 text-teal-700 border-teal-600' 
        : 'text-gray-600 border-transparent hover:bg-gray-50 hover:text-gray-900'
    ]"
  >
    <svg v-if="iconSvg" class="w-5 h-5 flex-shrink-0" :class="isActive ? 'text-teal-600' : 'text-gray-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor" v-html="iconSvg"></svg>
    <span v-else-if="icon" class="text-lg flex-shrink-0">{{ icon }}</span>
    <span>{{ label }}</span>
  </RouterLink>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps<{
  to: string
  icon?: string
  iconSvg?: string
  label: string
}>()

const route = useRoute()

const isActive = computed(() => route.path === props.to || (props.to !== '/dashboard' && route.path.startsWith(props.to)))
</script>
