<template>
  <div class="p-8 space-y-6 max-w-3xl">
    <div class="flex items-center gap-3">
      <router-link to="/school/subjects" class="text-gray-400 hover:text-gray-700"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></router-link>
      <h1 class="text-2xl font-bold text-gray-900">Subject Detail</h1>
    </div>
    <div v-if="loading" class="flex items-center justify-center py-20"><div class="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div></div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">{{ error }}</div>
    <template v-else-if="subject">
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h2 class="text-xl font-bold text-gray-900">{{ subject.name }}</h2>
              <span v-if="subject.code" class="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded text-xs font-mono font-bold">{{ subject.code }}</span>
            </div>
            <p class="text-sm text-gray-500">{{ subject.description || 'No description' }}</p>
          </div>
          <router-link :to="`/school/subjects/${subject.id}/edit`" class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-indigo-700 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            Edit
          </router-link>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { subjectAPI, type Subject } from '@/school/apis/subjectAPI'
const route = useRoute(); const subjectId = route.params.id as string
const subject = ref<Subject | null>(null); const loading = ref(true); const error = ref('')
onMounted(async () => { try { const res = await subjectAPI.retrieve(subjectId); subject.value = res.data } catch { error.value = 'Failed to load subject.' } finally { loading.value = false } })
</script>
