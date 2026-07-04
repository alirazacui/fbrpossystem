#!/bin/bash
# ============================================================
# Setup script: FBR POS Platform — Frontend
# Creates two Nuxt 3 apps:
#   admin-app  → Platform admin portal
#   pos-app    → POS terminal for client companies
#
# Run from: fbr_pos_project/ (same level as fbr_pos_platform/)
# ============================================================

set -e

echo "==> Creating Admin App"
npx nuxi@latest init admin-app --package-manager npm --no-install

echo "==> Creating POS App"
npx nuxi@latest init pos-app --package-manager npm --no-install

# ── Install dependencies for Admin App ──────────────────────
echo "==> Installing Admin App dependencies"
cd admin-app
npm install

# Core dependencies
npm install \
  @nuxtjs/tailwindcss \
  @pinia/nuxt \
  pinia \
  @vueuse/nuxt \
  @vueuse/core \
  axios \
  @tanstack/vue-query \
  vue-toastification \
  @headlessui/vue \
  @heroicons/vue \
  dayjs \
  numeral \
  chart.js \
  vue-chartjs \
  vue3-apexcharts \
  apexcharts \
  xlsx \
  file-saver

# Dev dependencies
npm install -D \
  @nuxtjs/color-mode \
  @iconify/vue \
  prettier \
  eslint \
  @nuxtjs/eslint-config-typescript \
  typescript \
  @types/numeral \
  @types/file-saver

cd ..

# ── Install dependencies for POS App ────────────────────────
echo "==> Installing POS App dependencies"
cd pos-app
npm install

npm install \
  @nuxtjs/tailwindcss \
  @pinia/nuxt \
  pinia \
  @vueuse/nuxt \
  @vueuse/core \
  axios \
  @tanstack/vue-query \
  vue-toastification \
  @headlessui/vue \
  @heroicons/vue \
  dayjs \
  numeral \
  vue-barcode-reader \
  qrcode.vue

npm install -D \
  @iconify/vue \
  prettier \
  eslint \
  typescript \
  @types/numeral

cd ..

echo ""
echo "============================================================"
echo " Done! Two Nuxt 3 apps created."
echo " admin-app/ → Platform admin portal"
echo " pos-app/   → POS terminal"
echo ""
echo " Next: cd admin-app && npm run dev"
echo "============================================================"
