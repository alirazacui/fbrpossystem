<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200 px-8 py-6 flex-shrink-0">
      <div class="flex items-center gap-3 mb-1">
        <router-link to="/school/students" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </router-link>
        <span class="text-sm text-gray-400">Students</span>
        <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-sm font-medium text-gray-700">Admit Student</span>
      </div>
      <div class="flex items-center justify-between mt-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Student Admission Wizard</h1>
          <p class="text-sm text-gray-500 mt-0.5">Complete all steps to admit a student and generate their enrollment.</p>
        </div>
        <div class="flex items-center gap-3">
          <router-link to="/school/students" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-colors">
            Cancel
          </router-link>
          <button v-if="currentStep < 3" @click="nextStep" class="px-6 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm flex items-center gap-2 transition-colors">
            Next Step
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
          <button v-if="currentStep === 3" @click="handleSubmit" :disabled="loading" class="px-6 py-2 text-sm font-semibold text-white bg-green-600 rounded-lg hover:bg-green-700 shadow-sm disabled:opacity-50 flex items-center gap-2 transition-colors">
            <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            {{ loading ? 'Admitting...' : 'Complete Admission' }}
          </button>
        </div>
      </div>
    </div>

    <div class="flex-1 overflow-auto p-8">
      <div class="max-w-4xl mx-auto">
        
        <!-- Progress Bar -->
        <div class="mb-10 relative">
          <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
            <div :style="`width: ${((currentStep) / 3) * 100}%`" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500 transition-all duration-500"></div>
          </div>
          <div class="flex justify-between text-xs font-bold text-gray-400 px-1">
            <span :class="{'text-indigo-600': currentStep >= 1}">1. Student Details</span>
            <span :class="{'text-indigo-600': currentStep >= 2}">2. Guardian Link</span>
            <span :class="{'text-indigo-600': currentStep >= 3}">3. Enrollment</span>
          </div>
        </div>

        <!-- Error Alert -->
        <div v-if="serverError" class="mb-6 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-5 py-4 flex items-start gap-3 shadow-sm">
          <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          {{ serverError }}
        </div>

        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden relative min-h-[400px]">
          
          <!-- Step 1: Student Details -->
          <div v-show="currentStep === 1" class="p-8 animate-fade-in">
            <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center">1</div>
              Student Information
            </h2>
            
            <div class="grid grid-cols-2 gap-6">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Full Name <span class="text-red-500">*</span></label>
                <input v-model="form.student.fullname" type="text" placeholder="e.g. Ahmad Ali" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
                <p v-if="errors.fullname" class="text-red-500 text-xs mt-1.5">{{ errors.fullname }}</p>
              </div>
              
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Registration Number</label>
                <input v-model="form.student.registration_number" type="text" placeholder="Auto-generated if empty" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Date of Birth</label>
                <input v-model="form.student.date_of_birth" type="date" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Gender</label>
                <select v-model="form.student.gender" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 bg-white">
                  <option value="">Select...</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">B-Form / CNIC</label>
                <input v-model="form.student.cnic" type="text" placeholder="Optional for minors" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Phone Number</label>
                <input v-model="form.student.phone_number" type="tel" placeholder="03xx-xxxxxxx" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>

              <div class="col-span-2">
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Home Address</label>
                <textarea v-model="form.student.address" rows="2" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
              </div>
            </div>
          </div>

          <!-- Step 2: Guardian Details -->
          <div v-show="currentStep === 2" class="p-8 animate-fade-in">
             <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center">2</div>
              Guardian Details
            </h2>

            <!-- Guardian mode toggle -->
            <div class="flex gap-4 mb-8">
              <label class="flex-1 flex items-center gap-3 p-4 border rounded-xl cursor-pointer transition-colors" :class="guardianMode === 'new' ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 hover:bg-gray-50'">
                <input type="radio" v-model="guardianMode" value="new" class="text-indigo-600 focus:ring-indigo-500 h-5 w-5" />
                <div>
                  <span class="block font-bold text-gray-900">Add New Guardian</span>
                  <span class="text-xs text-gray-500">Create a new guardian profile</span>
                </div>
              </label>
              
              <label class="flex-1 flex items-center gap-3 p-4 border rounded-xl cursor-pointer transition-colors" :class="guardianMode === 'existing' ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 hover:bg-gray-50'">
                <input type="radio" v-model="guardianMode" value="existing" class="text-indigo-600 focus:ring-indigo-500 h-5 w-5" />
                <div>
                  <span class="block font-bold text-gray-900">Link Existing</span>
                  <span class="text-xs text-gray-500">Search for a sibling's guardian</span>
                </div>
              </label>
            </div>

            <!-- Existing Guardian Search -->
            <div v-if="guardianMode === 'existing'" class="space-y-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Select Guardian <span class="text-red-500">*</span></label>
                <select v-model="form.guardian.id" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 bg-white">
                  <option value="">-- Choose Guardian --</option>
                  <option v-for="g in guardiansList" :key="g.id" :value="g.id">{{ g.first_name }} {{ g.last_name }} ({{ g.phone_number || g.cnic || 'No contact info' }})</option>
                </select>
                <div v-if="guardiansLoading" class="text-xs text-gray-400 mt-2">Loading guardians...</div>
              </div>
            </div>

            <!-- New Guardian Form -->
            <div v-if="guardianMode === 'new'" class="grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">First Name <span class="text-red-500">*</span></label>
                <input v-model="form.guardian.first_name" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Last Name <span class="text-red-500">*</span></label>
                <input v-model="form.guardian.last_name" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Phone Number <span class="text-red-500">*</span></label>
                <input v-model="form.guardian.phone_number" type="tel" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">CNIC</label>
                <input v-model="form.guardian.cnic" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
                <p class="text-xs text-gray-400 mt-1">Highly recommended for FBR billing.</p>
              </div>
            </div>

            <!-- Relation (Shared) -->
            <div class="mt-8 pt-6 border-t border-gray-100 grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Relationship to Student <span class="text-red-500">*</span></label>
                <select v-model="form.guardian.relation" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 bg-white">
                  <option value="Father">Father</option>
                  <option value="Mother">Mother</option>
                  <option value="Guardian">Guardian</option>
                  <option value="Uncle">Uncle</option>
                  <option value="Aunt">Aunt</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div class="flex items-center">
                <label class="flex items-center gap-3 mt-4 cursor-pointer">
                  <input v-model="form.guardian.is_primary_billing_contact" type="checkbox" class="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
                  <span class="text-sm font-semibold text-gray-900">Primary Billing Contact</span>
                </label>
              </div>
            </div>

          </div>

          <!-- Step 3: Enrollment -->
          <div v-show="currentStep === 3" class="p-8 animate-fade-in">
             <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center">3</div>
              Academic Enrollment
            </h2>

            <div class="grid grid-cols-2 gap-6">
              
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Academic Session <span class="text-red-500">*</span></label>
                <select v-model="form.enrollment.academic_session_id" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 bg-white">
                  <option value="">Select Session...</option>
                  <option v-for="s in sessionsList" :key="s.id" :value="s.id">{{ s.name }}</option>
                </select>
              </div>

              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Grade <span class="text-red-500">*</span></label>
                <select v-model="form.enrollment.grade_id" @change="handleGradeChange" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 bg-white">
                  <option value="">Select Grade...</option>
                  <option v-for="g in gradesList" :key="g.id" :value="g.id">{{ g.name }}</option>
                </select>
              </div>

              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Section <span class="text-red-500">*</span></label>
                <select v-model="form.enrollment.section_id" :disabled="!form.enrollment.grade_id" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 bg-white disabled:bg-gray-100">
                  <option value="">Select Section...</option>
                  <option v-for="sec in filteredSections" :key="sec.id" :value="sec.id">{{ sec.name }}</option>
                </select>
              </div>
              
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Enrollment Date</label>
                <input v-model="form.enrollment.enrollment_date" type="date" class="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>

            </div>

            <!-- Final Review Box -->
            <div class="mt-8 p-5 bg-green-50 border border-green-200 rounded-xl">
              <h3 class="text-sm font-bold text-green-900 mb-1">Ready to Admit</h3>
              <p class="text-xs text-green-700">Clicking Complete Admission will automatically register the student, link the guardian, and create the enrollment in one transaction.</p>
            </div>
          </div>

        </div>
        
        <!-- Bottom Nav Bar -->
        <div class="flex items-center justify-between mt-6">
          <button v-if="currentStep > 1" @click="currentStep--" class="px-6 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-colors">
            &larr; Back
          </button>
          <div v-else></div> <!-- Spacer -->
          
          <button v-if="currentStep < 3" @click="nextStep" class="px-6 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm transition-colors">
            Next Step &rarr;
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { studentAPI } from '@/school/apis/studentAPI'
import { sectionAPI, type Section } from '@/school/apis/sectionAPI'
import { academicSessionAPI, type AcademicSession } from '@/school/apis/academicSessionAPI'
import { gradeAPI, type Grade } from '@/school/apis/gradeAPI'
import { guardianAPI, type Guardian } from '@/school/apis/guardianAPI'

const router = useRouter()
const currentStep = ref(1)

const loading = ref(false)
const serverError = ref('')
const errors = ref<Record<string, string>>({})

const guardianMode = ref<'new' | 'existing'>('new')

const guardiansList = ref<Guardian[]>([])
const guardiansLoading = ref(false)

const sessionsList = ref<AcademicSession[]>([])
const gradesList = ref<Grade[]>([])
const sectionsList = ref<Section[]>([])

const form = ref({
  student: {
    fullname: '',
    registration_number: '',
    date_of_birth: '',
    gender: '',
    cnic: '',
    phone_number: '',
    address: '',
    admission_date: new Date().toISOString().split('T')[0],
  },
  guardian: {
    id: '', // for existing
    first_name: '',
    last_name: '',
    phone_number: '',
    cnic: '',
    relation: 'Father',
    is_primary_billing_contact: true
  },
  enrollment: {
    academic_session_id: '',
    grade_id: '',
    section_id: '',
    enrollment_date: new Date().toISOString().split('T')[0],
  }
})

// Auto filter sections when grade changes
const filteredSections = computed(() => {
  if (!form.value.enrollment.grade_id) return []
  return sectionsList.value.filter(s => s.grade_id === form.value.enrollment.grade_id)
})

const handleGradeChange = () => {
  form.value.enrollment.section_id = ''
}

onMounted(async () => {
  try {
    const [sessRes, gradeRes, secRes, guardRes] = await Promise.all([
      academicSessionAPI.list({ page_size: 100 }),
      gradeAPI.list({ page_size: 100 }),
      sectionAPI.list({ page_size: 100 }),
      guardianAPI.list({ page_size: 500 }) // In real app, might want searchable select
    ])
    
    sessionsList.value = sessRes.data.results || sessRes.data
    gradesList.value = gradeRes.data.results || gradeRes.data
    sectionsList.value = secRes.data.results || secRes.data
    guardiansList.value = guardRes.data.results || guardRes.data

    // Auto-select active session
    const activeSession = sessionsList.value.find(s => s.is_active)
    if (activeSession) {
      form.value.enrollment.academic_session_id = activeSession.id
    }
  } catch (err) {
    console.error("Failed to load reference data", err)
  }
})

const nextStep = () => {
  errors.value = {}
  
  if (currentStep.value === 1) {
    if (!form.value.student.fullname) {
      errors.value.fullname = 'Full Name is required'
      return
    }
  } else if (currentStep.value === 2) {
    if (guardianMode.value === 'new') {
      if (!form.value.guardian.first_name || !form.value.guardian.phone_number) {
        serverError.value = 'Guardian First Name and Phone are required'
        return
      }
      form.value.guardian.id = '' // Ensure blank
    } else {
      if (!form.value.guardian.id) {
        serverError.value = 'Please select a guardian'
        return
      }
    }
    serverError.value = ''
  }

  currentStep.value++
}

const handleSubmit = async () => {
  serverError.value = ''
  
  // Validate Step 3
  if (!form.value.enrollment.academic_session_id || !form.value.enrollment.grade_id || !form.value.enrollment.section_id) {
    serverError.value = 'Session, Grade, and Section are all required to enroll the student.'
    return
  }

  loading.value = true
  try {
    const payload = {
      student: form.value.student,
      guardian: guardianMode.value === 'new' ? form.value.guardian : { id: form.value.guardian.id, relation: form.value.guardian.relation, is_primary_billing_contact: form.value.guardian.is_primary_billing_contact },
      enrollment: form.value.enrollment
    }

    await studentAPI.admit(payload)
    router.push('/school/students')
  } catch (err: any) {
    const data = err.response?.data
    serverError.value = data?.error || data?.detail || 'Failed to complete admission process.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
