<template>
  <div>
    <div 
      class="grid grid-cols-12 gap-4 px-6 py-3 items-center group transition-colors duration-150 border-b border-gray-100 bg-white cursor-move hover:bg-gray-50"
      :class="{ 'bg-blue-50 ring-2 ring-inset ring-blue-400': dragOver }"
      draggable="true"
      @dragstart="onDragStart"
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop.prevent="onDrop"
    >
      <div class="col-span-8 flex items-center">
        <!-- Indentation spacer -->
        <div :style="{ width: `${level * 24}px` }" class="flex-shrink-0"></div>
        
        <!-- Drag Handle Icon -->
        <svg class="w-4 h-4 text-gray-300 mr-2 group-hover:text-gray-500 cursor-move flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>

        <!-- Folder/Node Icon -->
        <svg v-if="node.children.length > 0" class="w-5 h-5 text-gray-400 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        <svg v-else class="w-5 h-5 text-gray-300 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>

        <span class="text-sm font-medium text-gray-900 truncate">{{ node.name }}</span>
      </div>
      <div class="col-span-4 text-sm text-gray-500 flex items-center">
        <span v-if="node.parent_name" class="truncate bg-gray-100 px-2 py-1 rounded text-xs">{{ node.parent_name }}</span>
        <span v-else class="text-gray-400 italic text-xs">— Top level —</span>
      </div>
    </div>

    <!-- Recursive children -->
    <div v-if="node.children.length > 0">
      <CategoryRow
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :level="level + 1"
        @drag-start="$emit('drag-start', $event)"
        @drop-on="$emit('drop-on', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  node: any
  level: number
}>()

const emit = defineEmits(['drag-start', 'drop-on'])

const dragOver = ref(false)

const onDragStart = (e: DragEvent) => {
  // We don't really need to set data because we track dragged ID in parent, 
  // but it's good practice for Firefox compatibility.
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.setData('text/plain', props.node.id.toString())
  }
  emit('drag-start', props.node.id)
}

const onDrop = (e: DragEvent) => {
  dragOver.value = false
  emit('drop-on', props.node.id)
}
</script>
