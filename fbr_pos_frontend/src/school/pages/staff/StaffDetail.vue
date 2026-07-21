<template>
  <div class="p-8 space-y-6 max-w-3xl">
    <div class="flex items-center gap-3">
      <router-link to="/school/staff" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <h1 class="text-2xl font-bold text-gray-900">Staff Detail</h1>
    </div>
    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    <template v-else-if="member">
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-6">
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-xl">{{ member.fullname.charAt(0).toUpperCase() }}</div>
            <div>
              <h2 class="text-xl font-bold text-gray-900">{{ member.fullname }}</h2>
              <p class="text-sm text-gray-500">{{ member.designation || 'Staff Member' }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <span :class="member.status === 'active' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-100 text-gray-500 border-gray-200'" class="px-3 py-1 rounded-full text-xs font-bold border">{{ member.status === 'active' ? 'Active' : 'Inactive' }}</span>
            <router-link :to="`/school/staff/${member.id}/edit`" class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-indigo-700 bg-indigo-50 rounded-lg hover:bg-indigo-100">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              Edit
            </router-link>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-6 border-t border-gray-100 pt-5">
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Email</p><p class="text-sm text-gray-800">{{ member.email || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Phone</p><p class="text-sm text-gray-800">{{ member.phone_number || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">CNIC</p><p class="text-sm text-gray-800">{{ member.cnic || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Date of Birth</p><p class="text-sm text-gray-800">{{ member.date_of_birth || '—' }}</p></div>
          <div><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Date of Joining</p><p class="text-sm text-gray-800">{{ member.date_of_joining || '—' }}</p></div>
          <div class="col-span-2"><p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Address</p><p class="text-sm text-gray-800">{{ member.address || '—' }}</p></div>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { staffAPI, type Staff } from '@/school/apis/staffAPI'
const route = useRoute(); const staffId = route.params.id as string
const member = ref<Staff | null>(null); const loading = ref(true); const error = ref('')
onMounted(async () => { try { const res = await staffAPI.retrieve(staffId); member.value = res.data } catch { error.value = 'Failed to load staff.' } finally { loading.value = false } })
</script>
