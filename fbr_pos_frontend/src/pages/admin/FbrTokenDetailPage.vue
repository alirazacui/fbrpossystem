<template>
  <div class="flex flex-col h-[calc(100vh-64px)] overflow-hidden bg-gray-50/50">
    <!-- Header -->
    <div class="px-8 py-6 bg-white border-b border-gray-200 flex items-center justify-between">
      <div class="flex items-center text-sm text-gray-500">
        <button @click="$router.push('/admin/fbr-tokens')" class="hover:text-gray-900 transition-colors mr-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <RouterLink to="/admin/fbr-tokens" class="hover:text-gray-900 transition-colors">Fbr</RouterLink>
        <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <RouterLink to="/admin/fbr-tokens" class="hover:text-gray-900 transition-colors">Fbr tokens</RouterLink>
        <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <span class="font-bold text-gray-900" v-if="token">{{ token.id }} {{ token.environment.toLowerCase() }}</span>
        <span class="font-bold text-gray-900" v-else>Loading...</span>
      </div>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 rounded shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none">
        <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        History
      </button>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto px-8 py-6 custom-scrollbar">
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
      </div>
      <div v-else-if="token" class="bg-white border border-gray-200 rounded-lg shadow-sm">
        <dl>
          <!-- Created at -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Created at</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ formatDate(token.created_at) }}</dd>
          </div>
          
          <!-- Updated at -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Updated at</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ formatDate(token.updated_at) }}</dd>
          </div>
          
          <!-- Tenant -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Tenant</dt>
            <dd class="text-sm text-teal-600 font-medium uppercase col-span-2">{{ token.tenant_name }}</dd>
          </div>
          
          <!-- Id -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Id</dt>
            <dd class="text-sm text-gray-700 col-span-2 font-mono">{{ token.id }}</dd>
          </div>
          
          <!-- Environment -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Environment</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ token.environment }}</dd>
          </div>
          
          <!-- Licensed integrator -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Licensed integrator</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ token.licensed_integrator }}</dd>
          </div>
          
          <!-- Token encrypted -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Token encrypted</dt>
            <dd class="text-sm text-gray-500 col-span-2 break-all">{{ token.token_encrypted || '-' }}</dd>
          </div>
          
          <!-- Api endpoint -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Api endpoint</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ token.api_endpoint }}</dd>
          </div>
          
          <!-- Is active -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200">
            <dt class="text-sm font-bold text-gray-900">Is active</dt>
            <dd class="text-sm col-span-2">
              <div v-if="token.is_active" class="flex items-center justify-center w-5 h-5 bg-green-100 text-green-600 rounded-full">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
              </div>
              <div v-else class="flex items-center justify-center w-5 h-5 bg-red-100 text-red-500 rounded-full">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
              </div>
            </dd>
          </div>
          
          <!-- Activated at -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4 border-b border-gray-200 bg-gray-50/50">
            <dt class="text-sm font-bold text-gray-900">Activated at</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ formatDate(token.activated_at) }}</dd>
          </div>
          
          <!-- Expires at -->
          <div class="px-6 py-4 grid grid-cols-3 gap-4">
            <dt class="text-sm font-bold text-gray-900">Expires at</dt>
            <dd class="text-sm text-gray-700 col-span-2">{{ formatDate(token.expires_at) }}</dd>
          </div>
        </dl>
      </div>
      <div v-else class="flex justify-center items-center py-20 text-red-500">
        Failed to load token details.
      </div>
    </div>

    <!-- Bottom Actions -->
    <div class="px-8 py-4 bg-white border-t border-gray-200 flex justify-end items-center space-x-3">
      <button class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded hover:bg-gray-50 transition">
        Save and continue editing
      </button>
      <button class="px-6 py-2 bg-green-600 text-white text-sm font-medium rounded hover:bg-green-700 transition">
        Save
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fbrTokensAPI } from '@/apis/admin/fbrTokensAPI'

const route = useRoute()
const token = ref<any>(null)
const loading = ref(true)

const fetchTokenDetail = async () => {
  loading.value = true
  try {
    const tokenId = route.params.id as string
    const res = await fbrTokensAPI.getById(tokenId)
    token.value = res.data
  } catch (error) {
    console.error('Failed to fetch token detail:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string | null) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(date)
}

onMounted(() => {
  fetchTokenDetail()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 20px;
}
</style>
