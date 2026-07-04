<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-white flex items-center justify-center px-4">
    <!-- Main Container -->
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="inline-block bg-teal-600 rounded-full p-4 mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">FBR POS</h1>
        <p class="text-gray-600 mt-2">Company Portal</p>
        <p class="text-sm text-gray-500 mt-1">Business Operations</p>
      </div>

      <!-- Login Form Card -->
      <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Email Field -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
            <div class="relative">
              <input
                v-model="credentials.email"
                type="email"
                required
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-teal-600 transition-colors"
                placeholder="owner@company.com"
              />
              <svg
                class="absolute right-3 top-3 w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>

          <!-- Password Field -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
            <div class="relative">
              <input
                v-model="credentials.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-teal-600 transition-colors"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-3 text-gray-400 hover:text-teal-600"
              >
                <svg
                  v-if="!showPassword"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-4.803m5.596-3.856a3.375 3.375 0 11-4.753 4.753m4.753-4.753L3.596 3.039m10.318 10.318L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Remember Me -->
          <div class="flex items-center">
            <input
              v-model="rememberMe"
              type="checkbox"
              id="remember"
              class="w-4 h-4 rounded border-gray-300 text-teal-600 focus:ring-teal-600"
            />
            <label for="remember" class="ml-2 text-sm text-gray-600">
              Remember this device
            </label>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.loading"
            class="w-full bg-teal-600 hover:bg-teal-700 disabled:bg-gray-400 text-white font-semibold py-3 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
          >
            <svg
              v-if="!authStore.loading"
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
            <svg
              v-else
              class="animate-spin w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ authStore.loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
      </div>

      <!-- Back Link -->
      <div class="text-center">
        <RouterLink
          to="/login"
          class="text-teal-600 hover:text-teal-700 font-medium text-sm flex items-center justify-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back to Login Selection
        </RouterLink>
      </div>

      <!-- Info Box -->
      <div class="mt-8 bg-teal-50 border border-teal-200 rounded-lg p-4">
        <p class="text-xs text-teal-900">
          <span class="font-semibold">💡 Tip:</span> Use your company email and password to access your business dashboard.
        </p>
      </div>

      <div class="mt-4 text-center">
        <button type="button" class="text-sm font-semibold text-teal-700 hover:text-teal-800 underline underline-offset-4" @click="openForgotPassword = true">
          Forgot password?
        </button>
      </div>

      <!-- Footer -->
      <div class="mt-6 pt-6 border-t border-gray-200 text-center">
        <p class="text-sm text-gray-600">
          FBR POS Platform · Powered by Digital Invoicing
        </p>
      </div>
    </div>
  </div>

  <div v-if="openForgotPassword" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4">
    <div class="w-full max-w-lg rounded-3xl border border-white/10 bg-slate-900 p-6 text-white shadow-2xl">
      <div class="flex items-start justify-between gap-4">
        <div>
          <p class="text-xs uppercase tracking-[0.3em] text-teal-300">Reset access</p>
          <h3 class="mt-2 text-2xl font-bold">Forgot Password</h3>
        </div>
        <button class="rounded-full bg-white/10 px-3 py-1 text-sm text-white hover:bg-white/20" @click="closeForgotPassword">Close</button>
      </div>

      <div v-if="resetStep === 'request'" class="mt-6 space-y-4">
        <p class="text-sm text-white/70">Enter your company login email. An OTP will be sent there.</p>
        <input v-model="resetEmail" type="email" class="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-teal-400" placeholder="Email address" />
        <button class="w-full rounded-2xl bg-teal-500 px-4 py-3 font-semibold text-slate-950 hover:bg-teal-400" @click="requestResetOtp" :disabled="resetLoading">
          {{ resetLoading ? 'Sending...' : 'Send OTP' }}
        </button>
      </div>

      <div v-else-if="resetStep === 'verify'" class="mt-6 space-y-4">
        <p class="text-sm text-white/70">Enter the OTP sent to {{ resetEmail }}.</p>
        <input v-model="resetOtp" type="text" maxlength="6" class="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-teal-400" placeholder="Enter OTP" />
        <button class="w-full rounded-2xl bg-teal-500 px-4 py-3 font-semibold text-slate-950 hover:bg-teal-400" @click="verifyResetOtp" :disabled="resetLoading">
          {{ resetLoading ? 'Verifying...' : 'Verify OTP' }}
        </button>
      </div>

      <div v-else class="mt-6 space-y-4">
        <p class="text-sm text-white/70">Create a new password for your company account.</p>
        <input v-model="newPassword" type="password" class="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-teal-400" placeholder="New password" />
        <input v-model="confirmPassword" type="password" class="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-teal-400" placeholder="Confirm password" />
        <button class="w-full rounded-2xl bg-teal-500 px-4 py-3 font-semibold text-slate-950 hover:bg-teal-400" @click="confirmResetPassword" :disabled="resetLoading">
          {{ resetLoading ? 'Updating...' : 'Reset Password' }}
        </button>
      </div>

      <p v-if="resetError" class="mt-4 text-sm text-rose-300">{{ resetError }}</p>
      <p v-if="resetSuccess" class="mt-4 text-sm text-emerald-300">{{ resetSuccess }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/authStore'
import { authAPI } from '@/apis/auth/authAPI'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref({
  email: '',
  password: '',
})

const showPassword = ref(false)
const rememberMe = ref(false)
const error = ref('')
const openForgotPassword = ref(false)
const resetStep = ref<'request' | 'verify' | 'confirm'>('request')
const resetEmail = ref('')
const resetOtp = ref('')
const resetToken = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const resetLoading = ref(false)
const resetError = ref('')
const resetSuccess = ref('')

const closeForgotPassword = () => {
  openForgotPassword.value = false
  resetStep.value = 'request'
  resetEmail.value = ''
  resetOtp.value = ''
  resetToken.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  resetError.value = ''
  resetSuccess.value = ''
}

const requestResetOtp = async () => {
  resetError.value = ''
  resetSuccess.value = ''

  if (!resetEmail.value) {
    resetError.value = 'Email is required.'
    return
  }

  resetLoading.value = true
  try {
    await authAPI.requestPasswordReset(resetEmail.value)
    resetStep.value = 'verify'
    resetSuccess.value = 'OTP sent to your email.'
  } catch (err: any) {
    resetError.value = err.response?.data?.detail || 'Unable to send OTP.'
  } finally {
    resetLoading.value = false
  }
}

const verifyResetOtp = async () => {
  resetError.value = ''
  resetSuccess.value = ''
  resetLoading.value = true

  try {
    const response = await authAPI.verifyPasswordResetOtp(resetEmail.value, resetOtp.value)
    resetToken.value = response.data.reset_token
    resetStep.value = 'confirm'
    resetSuccess.value = 'OTP verified. Set your new password.'
  } catch (err: any) {
    resetError.value = err.response?.data?.detail || 'Invalid OTP.'
  } finally {
    resetLoading.value = false
  }
}

const confirmResetPassword = async () => {
  resetError.value = ''
  resetSuccess.value = ''

  if (!newPassword.value || !confirmPassword.value) {
    resetError.value = 'Both password fields are required.'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    resetError.value = 'Passwords do not match.'
    return
  }

  resetLoading.value = true
  try {
    await authAPI.confirmPasswordReset(resetToken.value, newPassword.value, confirmPassword.value)
    resetSuccess.value = 'Password reset successful. You can log in now.'
    setTimeout(() => closeForgotPassword(), 1500)
  } catch (err: any) {
    resetError.value = err.response?.data?.detail || 'Unable to reset password.'
  } finally {
    resetLoading.value = false
  }
}

const handleLogin = async () => {
  error.value = ''

  try {
    await authStore.login(credentials.value)
    
    // Check if user is company-related role
    const validRoles = ['owner', 'manager', 'cashier', 'salesperson']
    if (validRoles.includes(authStore.user?.role || '')) {
      router.push('/dashboard')
    } else {
      // Not a company user
      error.value = 'Unauthorized: Company access required'
      await authStore.logout()
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.'
  }
}
</script>
