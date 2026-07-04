<template>
  <div id="app" class="min-h-screen">
    <!-- Login pages - no layout -->
    <template v-if="isLoginRoute">
      <RouterView />
    </template>
    <!-- Admin routes - use AdminLayout -->
    <template v-else-if="authStore.isAuthenticated && isAdminUser">
      <AdminLayout>
        <RouterView />
      </AdminLayout>
    </template>
    <!-- Other authenticated routes (use AppLayout) -->
    <template v-else-if="authStore.isAuthenticated">
      <AppLayout>
        <RouterView />
      </AppLayout>
    </template>
    <!-- Unauthenticated (no layout) -->
    <template v-else>
      <RouterView />
    </template>
    
    <GlobalAlertModal />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'
import AppLayout from '@/layouts/AppLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import GlobalAlertModal from '@/components/common/GlobalAlertModal.vue'
import { useAlertStore } from '@/stores/common/alertStore'

const alertStore = useAlertStore()

const authStore = useAuthStore()
const route = useRoute()

const isLoginRoute = computed(() => {
  return route.path === '/login' || route.path === '/login/admin' || route.path === '/login/company'
})

const isAdminUser = computed(() => {
  return authStore.user?.role === 'admin' || authStore.user?.role === 'admin_staff'
})

onMounted(async () => {
  // Override native alerts/confirms
  window.alert = (msg: string) => {
    alertStore.showAlert(msg)
  }
  
  // Note: Since our confirm modal is async but window.confirm is sync, 
  // replacing window.confirm globally with an async function breaks logic
  // unless we await window.confirm. We will just provide window.$confirm
  // and handle it locally in ProductDetail.vue
  ;(window as any).$confirm = (msg: string) => {
    return alertStore.showConfirm(msg)
  }
  
  await authStore.initialize()
})
</script>

<style scoped>
/* Global app styles */
</style>
