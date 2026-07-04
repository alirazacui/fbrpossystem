<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-white flex items-center justify-center px-4">
    <!-- Main Container -->
    <div class="w-full max-w-md">
      <!-- Logo Section -->
      <div class="text-center mb-12">
        <div class="inline-block bg-teal-600 rounded-full p-4 mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-gray-900">FBR POS</h1>
        <p class="text-gray-600 mt-2">Select Login Type</p>
      </div>

      <!-- Login Type Selection -->
      <div class="space-y-4">
        <!-- Admin Login Option -->
        <RouterLink
          to="/login/admin"
          class="block bg-white border-2 border-teal-200 rounded-lg p-6 hover:border-teal-600 hover:shadow-lg transition-all duration-300 group"
        >
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900 group-hover:text-teal-600">
                Admin Portal
              </h3>
              <p class="text-sm text-gray-600 mt-1">
                For administrators and platform staff
              </p>
            </div>
            <svg
              class="w-6 h-6 text-teal-600 group-hover:scale-110 transition-transform"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
        </RouterLink>

        <!-- Company Owner Login Option -->
        <RouterLink
          to="/login/company"
          class="block bg-white border-2 border-teal-200 rounded-lg p-6 hover:border-teal-600 hover:shadow-lg transition-all duration-300 group"
        >
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900 group-hover:text-teal-600">
                Company Login
              </h3>
              <p class="text-sm text-gray-600 mt-1">
                For business owners, managers & staff
              </p>
            </div>
            <svg
              class="w-6 h-6 text-teal-600 group-hover:scale-110 transition-transform"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
        </RouterLink>
      </div>

      <!-- Footer -->
      <div class="mt-12 pt-8 border-t border-gray-200 text-center">
        <p class="text-sm text-gray-600">
          Powered by FBR Digital Invoicing System
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Login choice page - no script logic needed
</script>
