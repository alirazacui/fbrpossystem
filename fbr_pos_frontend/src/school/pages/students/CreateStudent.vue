<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200 px-8 py-6">
      <div class="flex items-center gap-3 mb-1">
        <router-link to="/school/students" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <span class="text-sm text-gray-400">Students</span>
        <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-sm font-medium text-gray-700">New Student</span>
      </div>
      <div class="flex items-center justify-between mt-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Register New Student</h1>
          <p class="text-sm text-gray-500 mt-0.5">Fill in all required fields to create a student profile.</p>
        </div>
        <div class="flex items-center gap-3">
          <router-link to="/school/students" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm">
            Cancel
          </router-link>
          <button @click="handleSubmit" :disabled="loading" class="px-6 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm disabled:opacity-50 flex items-center gap-2 transition-colors">
            <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            {{ loading ? 'Creating...' : 'Create Student' }}
          </button>
        </div>
      </div>
    </div>

    <div class="px-8 py-6 grid grid-cols-3 gap-6">
      <!-- Left Column: Main Form -->
      <div class="col-span-2 space-y-6">

        <!-- Section: Identity -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
            <h2 class="font-bold text-gray-900">Identity & Basic Info</h2>
            <p class="text-xs text-gray-500 mt-0.5">Core student identification details</p>
          </div>
          <div class="p-6 grid grid-cols-2 gap-5">
            <div class="col-span-2">
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Full Name <span class="text-red-500">*</span></label>
              <input v-model="form.fullname" type="text" placeholder="e.g. Ahmad Ali Khan" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow" />
              <p v-if="errors.fullname" class="text-red-500 text-xs mt-1.5 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                {{ errors.fullname }}
              </p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Registration Number</label>
              <input v-model="form.registration_number" type="text" placeholder="e.g. STU-2024-001" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Gender</label>
              <select v-model="form.gender" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white">
                <option value="">Select gender...</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Date of Birth</label>
              <input v-model="form.date_of_birth" type="date" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Admission Date</label>
              <input v-model="form.admission_date" type="date" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">CNIC / B-Form Number</label>
              <input v-model="form.cnic" type="text" placeholder="e.g. 35202-1234567-1" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
              <p class="text-xs text-gray-400 mt-1">Required for FBR invoices over Rs 20,000</p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Status</label>
              <div class="flex gap-3">
                <button @click="form.status = 'active'" :class="form.status === 'active' ? 'bg-green-600 text-white border-green-600' : 'bg-white text-gray-700 border-gray-300'" class="flex-1 py-3 text-sm font-semibold rounded-lg border transition-all">Active</button>
                <button @click="form.status = 'inactive'" :class="form.status === 'inactive' ? 'bg-gray-600 text-white border-gray-600' : 'bg-white text-gray-700 border-gray-300'" class="flex-1 py-3 text-sm font-semibold rounded-lg border transition-all">Inactive</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Section: Contact -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
            <h2 class="font-bold text-gray-900">Contact Information</h2>
            <p class="text-xs text-gray-500 mt-0.5">Phone, email and home address</p>
          </div>
          <div class="p-6 grid grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Phone Number</label>
              <input v-model="form.phone_number" type="tel" placeholder="03xx-xxxxxxx" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Email Address</label>
              <input v-model="form.email" type="email" placeholder="student@example.com" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
            </div>

            <div class="col-span-2">
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Home Address</label>
              <textarea v-model="form.address" rows="3" placeholder="Street, Area, City..." class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"></textarea>
            </div>
          </div>
        </div>

        <!-- Error display -->
        <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-5 py-4 flex items-start gap-3">
          <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          {{ serverError }}
        </div>
      </div>

      <!-- Right Column: Photo + Class Assignment -->
      <div class="space-y-6">

        <!-- Photo Upload -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
            <h2 class="font-bold text-gray-900">Profile Photo</h2>
          </div>
          <div class="p-6">
            <div class="flex flex-col items-center gap-4">
              <div class="w-28 h-28 rounded-2xl overflow-hidden bg-indigo-50 border-2 border-dashed border-indigo-200 flex items-center justify-center cursor-pointer hover:bg-indigo-100 transition-colors relative" @click="triggerPhotoUpload">
                <img v-if="photoPreview" :src="photoPreview" class="w-full h-full object-cover" />
                <div v-else class="text-center">
                  <svg class="w-8 h-8 text-indigo-400 mx-auto mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  <p class="text-xs text-indigo-400 font-medium">Upload Photo</p>
                </div>
              </div>
              <input ref="photoInput" type="file" accept="image/*" class="hidden" @change="handlePhotoChange" />
              <button v-if="photoPreview" @click="photoPreview = ''; form.photo = null" class="text-xs text-red-500 hover:text-red-700">Remove photo</button>
              <p class="text-xs text-gray-400 text-center">JPG, PNG up to 2MB<br>Passport size recommended</p>
            </div>
          </div>
        </div>

        <!-- Class / Section Assignment -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
            <h2 class="font-bold text-gray-900">Class Assignment</h2>
            <p class="text-xs text-gray-500 mt-0.5">Assign section and grade</p>
          </div>
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Section</label>
              <select v-model="form.current_section_id" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
                <option value="">Unassigned</option>
                <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.name }} {{ sec.grade_name ? `(${sec.grade_name})` : '' }}</option>
              </select>
            </div>
            <div v-if="sectionsLoading" class="text-xs text-gray-400 flex items-center gap-2">
              <div class="w-3 h-3 border-2 border-gray-200 border-t-gray-500 rounded-full animate-spin"></div>
              Loading sections...
            </div>
          </div>
        </div>

        <!-- Quick Tips -->
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="text-sm font-bold text-blue-900 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            After Creating
          </h3>
          <ul class="space-y-2 text-xs text-blue-700">
            <li class="flex items-start gap-2">
              <span class="w-4 h-4 bg-blue-200 rounded-full flex items-center justify-center text-blue-800 font-bold text-[10px] flex-shrink-0 mt-0.5">1</span>
              Link a guardian from the student's detail page
            </li>
            <li class="flex items-start gap-2">
              <span class="w-4 h-4 bg-blue-200 rounded-full flex items-center justify-center text-blue-800 font-bold text-[10px] flex-shrink-0 mt-0.5">2</span>
              Create an enrollment for the current session
            </li>
            <li class="flex items-start gap-2">
              <span class="w-4 h-4 bg-blue-200 rounded-full flex items-center justify-center text-blue-800 font-bold text-[10px] flex-shrink-0 mt-0.5">3</span>
              Generate a fee invoice for this student
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { studentAPI } from '@/school/apis/studentAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'

const router = useRouter()
const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})
const sectionsLoading = ref(false)
const photoInput = ref<HTMLInputElement | null>(null)
const photoPreview = ref('')

const form = ref({
  fullname: '',
  email: '',
  phone_number: '',
  cnic: '',
  date_of_birth: '',
  gender: '' as 'male' | 'female' | '',
  registration_number: '',
  admission_date: new Date().toISOString().split('T')[0],
  current_section_id: '',
  address: '',
  status: 'active' as 'active' | 'inactive',
  photo: null as File | null,
})

const sections = ref<Section[]>([])

onMounted(async () => {
  sectionsLoading.value = true
  try {
    const res = await sectionAPI.list({ page_size: 100 })
    sections.value = res.data.results || (res.data as any)
  } catch {
    // sections optional
  } finally {
    sectionsLoading.value = false
  }
})

const triggerPhotoUpload = () => photoInput.value?.click()

const handlePhotoChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  form.value.photo = file
  const reader = new FileReader()
  reader.onload = (ev) => { photoPreview.value = ev.target?.result as string }
  reader.readAsDataURL(file)
}

const handleSubmit = async () => {
  errors.value = {}
  serverError.value = ''
  if (!form.value.fullname.trim()) { errors.value.fullname = 'Full name is required.'; return }

  loading.value = true
  try {
    const payload = new FormData()
    Object.entries(form.value).forEach(([key, val]) => {
      if (val === null || val === '') return
      if (val instanceof File) { payload.append(key, val) }
      else { payload.append(key, String(val)) }
    })

    await studentAPI.create(payload as any)
    router.push('/school/students')
  } catch (err: any) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([k, v]: any) => {
        errors.value[k] = Array.isArray(v) ? v.join(', ') : String(v)
      })
    }
    serverError.value = data?.detail || 'Failed to create student. Please check the form.'
  } finally {
    loading.value = false
  }
}
</script>
