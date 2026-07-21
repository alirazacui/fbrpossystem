<template>
  <div class="p-8 space-y-6 max-w-3xl">
    <div class="flex items-center gap-3">
      <router-link to="/school/fee-heads" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <h1 class="text-2xl font-bold text-gray-900">Fee Head Detail</h1>
    </div>
    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    <template v-else-if="feeHead">
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ feeHead.name }}</h2>
            <p class="text-sm text-gray-500 mt-0.5">{{ feeHead.description || 'No description' }}</p>
          </div>
          <router-link :to="`/school/fee-heads/${feeHead.id}/edit`" class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-indigo-700 bg-indigo-50 rounded-lg hover:bg-indigo-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            Edit
          </router-link>
        </div>
        <div class="grid grid-cols-3 gap-6 border-t border-gray-100 pt-4">
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">PCT Code</p><p class="text-sm font-mono font-bold text-gray-800">{{ feeHead.default_pct_code || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Type</p><span :class="feeHead.is_recurring ? 'bg-blue-50 text-blue-700' : 'bg-gray-100 text-gray-600'" class="px-2 py-0.5 rounded-full text-xs font-semibold">{{ feeHead.is_recurring ? 'Recurring' : 'One-time' }}</span></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Status</p><span :class="feeHead.is_active ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-500'" class="px-2 py-0.5 rounded-full text-xs font-semibold">{{ feeHead.is_active ? 'Active' : 'Inactive' }}</span></div>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { feeHeadAPI, type FeeHead } from '@/school/apis/feeHeadAPI'
const route = useRoute(); const feeHeadId = route.params.id as string
const feeHead = ref<FeeHead | null>(null); const loading = ref(true); const error = ref('')
onMounted(async () => { try { const res = await feeHeadAPI.retrieve(feeHeadId); feeHead.value = res.data } catch { error.value = 'Failed to load fee head.' } finally { loading.value = false } })
</script>
