<template>
  <div class="space-y-6 pb-12">
    <div class="flex items-start justify-between gap-4">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-teal-600">Platform</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-900">Platform Settings</h1>
        <p class="mt-1 text-sm text-gray-500">Brand colors, SMTP email configuration, and admin password.</p>
      </div>
      <div v-if="settings" class="rounded-2xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-600 shadow-sm">
        Last saved: {{ settings.updated_at ? new Date(settings.updated_at).toLocaleString() : 'Never' }}
      </div>
    </div>

    <div v-if="loadError" class="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
      {{ loadError }}
    </div>
    <div v-if="saveMessage" class="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
      {{ saveMessage }}
    </div>

    <div class="grid gap-6 lg:grid-cols-3">
      <section class="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm lg:col-span-1">
        <h2 class="text-lg font-bold text-gray-900">Brand Colors</h2>
        <p class="mt-1 text-sm text-gray-500">These colors are stored for the admin interface.</p>
        <div class="mt-6 space-y-4">
          <label class="block space-y-2">
            <span class="text-sm font-medium text-gray-700">Primary color</span>
            <input v-model="form.primary_color" type="color" class="h-12 w-full rounded-xl border border-gray-200 bg-white p-1" />
          </label>
          <label class="block space-y-2">
            <span class="text-sm font-medium text-gray-700">Secondary color</span>
            <input v-model="form.secondary_color" type="color" class="h-12 w-full rounded-xl border border-gray-200 bg-white p-1" />
          </label>
          <label class="block space-y-2">
            <span class="text-sm font-medium text-gray-700">Accent color</span>
            <input v-model="form.accent_color" type="color" class="h-12 w-full rounded-xl border border-gray-200 bg-white p-1" />
          </label>
        </div>
      </section>

      <section class="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm lg:col-span-2">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="text-lg font-bold text-gray-900">SMTP Email Configuration</h2>
            <p class="mt-1 text-sm text-gray-500">Configure the mail account used for welcome emails and password reset OTPs.</p>
          </div>
          <button class="rounded-xl bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700" :disabled="savingSettings" @click="saveSettings">
            {{ savingSettings ? 'Saving...' : 'Save Settings' }}
          </button>
        </div>

        <div class="mt-6 grid gap-4 md:grid-cols-2">
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">SMTP host</span>
            <input v-model="form.smtp_host" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" placeholder="smtp.gmail.com" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">SMTP port</span>
            <input v-model.number="form.smtp_port" type="number" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" placeholder="587" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">SMTP username</span>
            <input v-model="form.smtp_username" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">SMTP password / app password</span>
            <input v-model="form.smtp_password" type="password" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Default from email</span>
            <input v-model="form.default_from_email" type="email" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="space-y-2">
            <span class="text-sm font-medium text-gray-700">Reply-to email</span>
            <input v-model="form.reply_to_email" type="email" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
          </label>
          <label class="flex items-center gap-3 md:col-span-2">
            <input v-model="form.smtp_use_tls" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-teal-600" />
            <span class="text-sm text-gray-700">Use TLS</span>
          </label>
        </div>

        <div class="mt-6 rounded-2xl bg-amber-50 p-4 text-sm text-amber-800">
          Gmail note: if you use Gmail, enable 2-step verification and create an app password. Use that app password in the SMTP password field, not your normal Gmail password.
        </div>
      </section>
    </div>

    <section class="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-gray-900">Admin Password</h2>
          <p class="mt-1 text-sm text-gray-500">Change your own admin password from here.</p>
        </div>
        <button class="rounded-xl bg-gray-900 px-4 py-2 text-sm font-semibold text-white hover:bg-gray-800" :disabled="savingPassword" @click="changePassword">
          {{ savingPassword ? 'Updating...' : 'Change Password' }}
        </button>
      </div>

      <div class="mt-6 grid gap-4 md:grid-cols-3">
        <label class="space-y-2">
          <span class="text-sm font-medium text-gray-700">Current password</span>
          <input v-model="passwordForm.current_password" type="password" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
        </label>
        <label class="space-y-2">
          <span class="text-sm font-medium text-gray-700">New password</span>
          <input v-model="passwordForm.new_password" type="password" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
        </label>
        <label class="space-y-2">
          <span class="text-sm font-medium text-gray-700">Confirm password</span>
          <input v-model="passwordForm.confirm_password" type="password" class="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-teal-500" />
        </label>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import platformSettingsAPI, { type PlatformSettings } from '@/apis/admin/platformSettingsAPI'

const settings = ref<PlatformSettings | null>(null)
const loadError = ref('')
const saveMessage = ref('')
const savingSettings = ref(false)
const savingPassword = ref(false)

const form = reactive<PlatformSettings>({
  primary_color: '#0f766e',
  secondary_color: '#f8fafc',
  accent_color: '#14b8a6',
  smtp_host: '',
  smtp_port: 587,
  smtp_use_tls: true,
  smtp_username: '',
  smtp_password: '',
  default_from_email: '',
  reply_to_email: '',
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const loadSettings = async () => {
  loadError.value = ''
  try {
    settings.value = await platformSettingsAPI.getSettings()
    Object.assign(form, settings.value)
  } catch (err: any) {
    loadError.value = err.response?.data?.detail || 'Failed to load platform settings.'
  }
}

const saveSettings = async () => {
  savingSettings.value = true
  saveMessage.value = ''
  try {
    const payload = {
      primary_color: form.primary_color,
      secondary_color: form.secondary_color,
      accent_color: form.accent_color,
      smtp_host: form.smtp_host,
      smtp_port: form.smtp_port,
      smtp_use_tls: form.smtp_use_tls,
      smtp_username: form.smtp_username,
      smtp_password: form.smtp_password,
      default_from_email: form.default_from_email,
      reply_to_email: form.reply_to_email,
    }
    settings.value = await platformSettingsAPI.updateSettings(payload)
    saveMessage.value = 'Platform settings saved successfully.'
  } catch (err: any) {
    loadError.value = err.response?.data?.detail || 'Failed to save settings.'
  } finally {
    savingSettings.value = false
  }
}

const changePassword = async () => {
  savingPassword.value = true
  saveMessage.value = ''
  try {
    await platformSettingsAPI.changeAdminPassword(passwordForm)
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    saveMessage.value = 'Admin password updated successfully.'
  } catch (err: any) {
    loadError.value = err.response?.data?.current_password || err.response?.data?.detail || 'Failed to update password.'
  } finally {
    savingPassword.value = false
  }
}

onMounted(loadSettings)
</script>