<template>
  <div class="space-y-6 pb-12">

    <!-- ── Header ─────────────────────────────────────────────── -->
    <div class="flex items-center justify-between">
      <div>
        <div class="flex items-center space-x-3 mb-1">
          <button @click="goBack" class="text-gray-500 hover:text-gray-800 transition">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <span class="text-sm text-gray-500">Back to Company</span>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">Company Permissions</h1>
        <p class="text-gray-500 mt-1 text-sm">
          These are the default permissions granted to every new Owner of
          <span class="font-semibold text-teal-700">{{ companyName }}</span>.
          Only modules enabled on this company are shown.
        </p>
      </div>

      <!-- Save button -->
      <button
        @click="savePermissions"
        :disabled="saving || loading"
        class="px-6 py-3 bg-teal-600 text-white rounded-xl font-semibold hover:bg-teal-700 transition shadow-sm disabled:opacity-50 flex items-center space-x-2 min-w-[140px] justify-center"
      >
        <div v-if="saving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        <span>{{ saving ? 'Saving...' : 'Save Changes' }}</span>
      </button>
    </div>

    <!-- ── Loading ─────────────────────────────────────────────── -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="bg-white rounded-2xl shadow-sm p-6 animate-pulse">
        <div class="h-4 bg-gray-200 rounded w-2/3 mb-4"></div>
        <div v-for="j in 4" :key="j" class="h-3 bg-gray-100 rounded mb-3"></div>
      </div>
    </div>

    <!-- ── Error ───────────────────────────────────────────────── -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center">
      <svg class="w-10 h-10 text-red-400 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M12 3a9 9 0 110 18A9 9 0 0112 3z"/>
      </svg>
      <p class="text-red-700 font-medium">{{ error }}</p>
      <button @click="fetchPermissions" class="mt-3 text-sm text-teal-600 hover:underline">Try again</button>
    </div>

    <!-- ── Empty ───────────────────────────────────────────────── -->
    <div v-else-if="modules.length === 0" class="bg-white rounded-2xl shadow-sm p-12 text-center">
      <svg class="w-14 h-14 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      <p class="text-gray-500 text-lg font-medium">No permissions available</p>
      <p class="text-gray-400 text-sm mt-1">Enable feature modules on the company first.</p>
    </div>

    <!-- ── Permission Modules Grid ─────────────────────────────── -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div
        v-for="mod in modules"
        :key="mod.module"
        class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
      >
        <!-- Card Header -->
        <div class="px-5 py-4 bg-gradient-to-r from-teal-50 to-white border-b border-gray-100 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-9 h-9 bg-teal-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h3 class="text-sm font-bold text-gray-900 leading-tight">{{ mod.module_display }}</h3>
          </div>

          <!-- All / None buttons -->
          <div class="flex items-center space-x-1">
            <button
              @click="selectAll(mod)"
              class="px-2.5 py-1 text-xs font-semibold bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition"
            >
              All
            </button>
            <button
              @click="selectNone(mod)"
              class="px-2.5 py-1 text-xs font-semibold bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition"
            >
              None
            </button>
          </div>
        </div>

        <!-- Permission Rows -->
        <div class="divide-y divide-gray-50">
          <label
            v-for="perm in mod.permissions"
            :key="perm.id"
            class="flex items-center justify-between px-5 py-3 hover:bg-gray-50 transition cursor-pointer group"
          >
            <div class="flex items-center space-x-3">
              <!-- Custom Checkbox -->
              <div
                :class="selected.has(perm.id)
                  ? 'bg-teal-600 border-teal-600'
                  : 'bg-white border-gray-300 group-hover:border-teal-400'"
                class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all flex-shrink-0"
                @click="togglePermission(perm.id)"
              >
                <svg v-if="selected.has(perm.id)" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-800">{{ perm.label }}</p>
                <p class="text-xs text-gray-400 font-mono">{{ perm.codename }}</p>
              </div>
            </div>

            <!-- Action badge -->
            <span :class="actionBadge(perm.action)" class="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0">
              {{ perm.action }}
            </span>
          </label>
        </div>

        <!-- Card Footer: count -->
        <div class="px-5 py-2.5 bg-gray-50 border-t border-gray-100 flex justify-between items-center">
          <span class="text-xs text-gray-400">
            {{ countGranted(mod) }} / {{ mod.permissions.length }} granted
          </span>
          <div class="flex space-x-1">
            <div
              v-for="perm in mod.permissions" :key="perm.id"
              :class="selected.has(perm.id) ? 'bg-teal-500' : 'bg-gray-200'"
              class="w-2 h-2 rounded-full transition-colors"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Save Success Toast ──────────────────────────────────── -->
    <Transition name="toast">
      <div
        v-if="showToast"
        class="fixed bottom-6 right-6 bg-gray-900 text-white px-5 py-3 rounded-xl shadow-2xl flex items-center space-x-3 z-50"
      >
        <svg class="w-5 h-5 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        <span class="text-sm font-medium">Permissions saved successfully!</span>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import permissionsAPI, { type PermissionModule } from '@/apis/permissions/permissionsAPI'
import companyAPI from '@/apis/admin/companyAPI'

const route  = useRoute()
const router = useRouter()

// This page is opened in context of a company — we need the company's Owner user_id
// The company owner is fetched from the company details
const companyId = Number(route.params.id)

const modules    = ref<PermissionModule[]>([])
const selected   = ref<Set<number>>(new Set())
const loading    = ref(true)
const saving     = ref(false)
const error      = ref('')
const showToast  = ref(false)
const companyName = ref('')
const ownerUserId = ref<number | null>(null)

const fetchPermissions = async () => {
  loading.value = true
  error.value = ''
  try {
    // 1. Get company detail — now includes owner_id from backend
    const company = await companyAPI.getCompanyDetail(companyId)
    companyName.value = company.business_name

    if (!company.owner_id) {
      error.value = 'No Owner user found for this company. Create an Owner first before managing permissions.'
      loading.value = false
      return
    }
    ownerUserId.value = company.owner_id

    // 2. Get permission panel for this owner (filtered to company modules)
    const panel = await permissionsAPI.getUserPermissionPanel(ownerUserId.value)
    modules.value = panel

    // 3. Pre-select all currently granted permissions
    const grantedIds = new Set<number>()
    panel.forEach(mod => {
      mod.permissions.forEach(perm => {
        if (perm.granted) grantedIds.add(perm.id)
      })
    })
    selected.value = grantedIds

  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load permissions. Ensure the backend is running.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchPermissions)

const togglePermission = (id: number) => {
  const updated = new Set(selected.value)
  if (updated.has(id)) {
    updated.delete(id)
  } else {
    updated.add(id)
  }
  selected.value = updated
}

const selectAll = (mod: PermissionModule) => {
  const updated = new Set(selected.value)
  mod.permissions.forEach(p => updated.add(p.id))
  selected.value = updated
}

const selectNone = (mod: PermissionModule) => {
  const updated = new Set(selected.value)
  mod.permissions.forEach(p => updated.delete(p.id))
  selected.value = updated
}

const countGranted = (mod: PermissionModule): number => {
  return mod.permissions.filter(p => selected.value.has(p.id)).length
}

const savePermissions = async () => {
  if (!ownerUserId.value) return
  saving.value = true
  try {
    await permissionsAPI.assignPermissions(ownerUserId.value, Array.from(selected.value))
    showToast.value = true
    setTimeout(() => { showToast.value = false }, 3000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.permission_ids || 'Failed to save permissions'
    console.error(err)
  } finally {
    saving.value = false
  }
}

const actionBadge = (action: string): string => {
  const map: Record<string, string> = {
    view:    'bg-blue-100 text-blue-700',
    create:  'bg-green-100 text-green-700',
    edit:    'bg-yellow-100 text-yellow-700',
    delete:  'bg-red-100 text-red-700',
    export:  'bg-purple-100 text-purple-700',
    approve: 'bg-teal-100 text-teal-700',
  }
  return map[action] || 'bg-gray-100 text-gray-600'
}

const goBack = () => router.push(`/admin/tenants/${companyId}`)
</script>

<style scoped>
.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>
