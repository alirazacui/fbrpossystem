<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center"
        @click.self="$emit('update:modelValue', false)"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm"></div>

        <!-- Modal Card -->
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
          
          <!-- Top colored bar -->
          <div :class="barClass" class="h-1.5 w-full"></div>

          <!-- Content -->
          <div class="p-6">
            <!-- Icon + Title -->
            <div class="flex items-start space-x-4">
              <div :class="iconBgClass" class="flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center">
                <!-- Danger icon -->
                <svg v-if="type === 'danger'" class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <!-- Warning icon -->
                <svg v-else-if="type === 'warning'" class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <!-- Success icon -->
                <svg v-else class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>

              <div class="flex-1">
                <h3 class="text-lg font-bold text-gray-900 mb-1">{{ title }}</h3>
                <p class="text-sm text-gray-500 leading-relaxed">{{ message }}</p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 flex space-x-3 justify-end">
              <button
                @click="$emit('update:modelValue', false)"
                class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition"
              >
                {{ cancelLabel }}
              </button>
              <button
                @click="handleConfirm"
                :disabled="loading"
                :class="confirmBtnClass"
                class="px-5 py-2.5 text-sm font-medium text-white rounded-lg transition disabled:opacity-60 flex items-center space-x-2 min-w-[100px] justify-center"
              >
                <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>{{ loading ? 'Please wait...' : confirmLabel }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  modelValue: boolean
  title: string
  message: string
  type?: 'danger' | 'warning' | 'success'
  confirmLabel?: string
  cancelLabel?: string
  loading?: boolean
}>(), {
  type: 'danger',
  confirmLabel: 'Confirm',
  cancelLabel: 'Cancel',
  loading: false,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'confirm'): void
}>()

const handleConfirm = () => {
  emit('confirm')
}

const barClass = computed(() => ({
  'bg-red-500': props.type === 'danger',
  'bg-yellow-400': props.type === 'warning',
  'bg-teal-500': props.type === 'success',
}))

const iconBgClass = computed(() => ({
  'bg-red-50': props.type === 'danger',
  'bg-yellow-50': props.type === 'warning',
  'bg-teal-50': props.type === 'success',
}))

const confirmBtnClass = computed(() => ({
  'bg-red-600 hover:bg-red-700': props.type === 'danger',
  'bg-yellow-500 hover:bg-yellow-600': props.type === 'warning',
  'bg-teal-600 hover:bg-teal-700': props.type === 'success',
}))
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.2s ease;
}
.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95) translateY(-8px);
}
</style>
