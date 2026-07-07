import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAlertStore = defineStore('alert', () => {
  const isVisible = ref(false)
  const title = ref('')
  const message = ref('')
  const type = ref<'success' | 'warning' | 'danger'>('warning')
  const isConfirm = ref(false)
  const confirmLabel = ref('Confirm')
  
  // Resolve function for confirm dialogs
  let resolvePromise: ((value: boolean) => void) | null = null

  const showAlert = (msg: string, titleStr: string = 'Notice', alertType: 'success' | 'warning' | 'danger' = 'warning') => {
    title.value = titleStr
    message.value = msg
    type.value = alertType
    isConfirm.value = false
    confirmLabel.value = 'OK'
    isVisible.value = true
    return new Promise<boolean>((resolve) => {
      resolvePromise = resolve
    })
  }

  const showConfirm = (msg: string, titleStr: string = 'Please Confirm', alertType: 'warning' | 'danger' = 'warning', confirmBtn = 'Confirm') => {
    title.value = titleStr
    message.value = msg
    type.value = alertType
    isConfirm.value = true
    confirmLabel.value = confirmBtn
    isVisible.value = true
    return new Promise<boolean>((resolve) => {
      resolvePromise = resolve
    })
  }

  const handleClose = (result: boolean) => {
    isVisible.value = false
    if (resolvePromise) {
      resolvePromise(result)
      resolvePromise = null
    }
  }

  return {
    isVisible,
    title,
    message,
    type,
    isConfirm,
    confirmLabel,
    showAlert,
    showConfirm,
    handleClose
  }
})
