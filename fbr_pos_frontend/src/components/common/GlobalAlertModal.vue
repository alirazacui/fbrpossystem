<template>
  <ConfirmModal
    v-model="alertStore.isVisible"
    :title="alertStore.title"
    :message="alertStore.message"
    :type="alertStore.type"
    :confirm-label="alertStore.confirmLabel"
    :cancel-label="alertStore.isConfirm ? 'Cancel' : ''"
    @confirm="alertStore.handleClose(true)"
    @update:model-value="!$event && alertStore.handleClose(false)"
  />
</template>

<script setup lang="ts">
import ConfirmModal from '@/components/ConfirmModal.vue'
import { useAlertStore } from '@/stores/common/alertStore'

const alertStore = useAlertStore()
</script>
