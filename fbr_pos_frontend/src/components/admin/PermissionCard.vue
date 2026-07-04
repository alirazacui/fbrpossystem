<template>
  <div class="bg-white rounded-lg shadow overflow-hidden">
    <!-- Card Header -->
    <div class="bg-gradient-to-r from-teal-50 to-teal-100 border-b border-teal-200 px-6 py-4 flex items-center justify-between">
      <h3 class="text-lg font-bold text-teal-900">{{ group.module_display }}</h3>
      <div class="flex items-center space-x-3">
        <button
          @click="$emit('select-all')"
          class="text-sm px-3 py-1 bg-teal-600 text-white rounded hover:bg-teal-700 transition font-medium"
        >
          Select All
        </button>
        <button
          @click="$emit('select-none')"
          class="text-sm px-3 py-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition font-medium"
        >
          None
        </button>
      </div>
    </div>

    <!-- Card Body - Permissions Grid -->
    <div class="px-6 py-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <div 
          v-for="permission in group.permissions"
          :key="permission.id"
          class="flex items-center space-x-3"
        >
          <input
            type="checkbox"
            :id="`perm-${permission.id}`"
            :checked="isSelected(permission.id)"
            @change="$emit('toggle', permission.id)"
            class="w-5 h-5 text-teal-600 rounded cursor-pointer accent-teal-600"
          />
          <label
            :for="`perm-${permission.id}`"
            class="flex-1 text-sm text-gray-700 cursor-pointer hover:text-teal-600 transition"
            :title="permission.label"
          >
            {{ capitalize(permission.action) }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PermissionPanelGroup } from '@/apis/admin/permissionAPI'

defineProps<{
  group: PermissionPanelGroup
  isSelected: (permissionId: number) => boolean
}>()

defineEmits<{
  'select-all': []
  'select-none': []
  'toggle': [permissionId: number]
}>()

const capitalize = (str: string) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}
</script>

<style scoped>
/* Add a custom capitalize filter */
</style>
