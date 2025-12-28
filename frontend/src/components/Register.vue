<template>
  <div class="min-h-screen bg-linear-to-br from-bg-soft to-white pt-28 pb-20">
    <div class="max-w-md mx-auto px-6">
      <!-- Header -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0 }"
        class="text-center mb-8"
      >
        <div class="w-20 h-20 gradient-primary rounded-3xl flex items-center justify-center mx-auto mb-6 glow-icon">
          <UserPlus :size="40" class="text-white" />
        </div>
        <h1 class="text-4xl mb-3">Buat Akun Baru</h1>
        <p class="text-gray-600">
          Sudah punya akun? 
          <router-link to="/login" class="text-primary-blue hover:underline">
            Masuk di sini
          </router-link>
        </p>
      </div>

      <!-- Register Form -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 100 } }"
        class="bg-white rounded-4xl p-8 card-shadow"
      >
        <form @submit.prevent="handleRegister">
          <!-- Full Name -->
          <div class="mb-6">
            <label class="block text-sm mb-2 text-gray-700">Nama Lengkap</label>
            <div class="relative">
              <User :size="20" class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                v-model="form.full_name"
                type="text"
                placeholder="Masukkan nama lengkap"
                class="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent"
              />
            </div>
          </div>

          <!-- Username -->
          <div class="mb-6">
            <label class="block text-sm mb-2 text-gray-700">Username</label>
            <div class="relative">
              <AtSign :size="20" class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                v-model="form.username"
                type="text"
                placeholder="pilih username"
                required
                class="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent"
              />
            </div>
          </div>

          <!-- Email -->
          <div class="mb-6">
            <label class="block text-sm mb-2 text-gray-700">Email</label>
            <div class="relative">
              <Mail :size="20" class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                v-model="form.email"
                type="email"
                placeholder="nama@email.com"
                required
                class="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent"
              />
            </div>
          </div>

          <!-- Password -->
          <div class="mb-6">
            <label class="block text-sm mb-2 text-gray-700">Password</label>
            <div class="relative">
              <Lock :size="20" class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Minimal 6 karakter"
                required
                minlength="6"
                class="w-full pl-12 pr-12 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <Eye v-if="showPassword" :size="20" />
                <EyeOff v-else :size="20" />
              </button>
            </div>
            <p class="text-xs text-gray-500 mt-2">Minimal 6 karakter</p>
          </div>

          <!-- Confirm Password -->
          <div class="mb-6">
            <label class="block text-sm mb-2 text-gray-700">Konfirmasi Password</label>
            <div class="relative">
              <Lock :size="20" class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                v-model="form.confirm_password"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Ulangi password"
                required
                class="w-full pl-12 pr-12 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <Eye v-if="showConfirmPassword" :size="20" />
                <EyeOff v-else :size="20" />
              </button>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
            <div class="flex items-start gap-2">
              <AlertCircle :size="20" class="text-red-500 shrink-0 mt-0.5" />
              <p class="text-sm text-red-700">{{ error }}</p>
            </div>
          </div>

          <!-- Terms -->
          <div class="mb-6">
            <label class="flex items-start gap-2 cursor-pointer">
              <input
                v-model="form.agree_terms"
                type="checkbox"
                required
                class="mt-1 w-4 h-4 text-primary-blue border-gray-300 rounded focus:ring-primary-blue"
              />
              <span class="text-sm text-gray-600">
                Saya setuju dengan <a href="#" class="text-primary-blue hover:underline">Syarat & Ketentuan</a> 
                dan <a href="#" class="text-primary-blue hover:underline">Kebijakan Privasi</a>
              </span>
            </label>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full gradient-primary text-white py-3 rounded-full hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <Loader2 v-if="isLoading" :size="20" class="animate-spin" />
            <span>{{ isLoading ? 'Memproses...' : 'Daftar Sekarang' }}</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-white text-gray-500">atau</span>
          </div>
        </div>

        <!-- Login Link -->
        <router-link
          to="/login"
          class="block w-full text-center border-2 border-primary-blue text-primary-blue py-3 rounded-full hover:bg-blue-50 transition-colors"
        >
          Masuk ke Akun Existing
        </router-link>
      </div>

      <!-- Info -->
      <div class="mt-6 text-center text-sm text-gray-500">
        <Lock :size="16" class="inline mr-1" />
        Data Anda aman dan terenkripsi
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlus, User, AtSign, Mail, Lock, Eye, EyeOff, AlertCircle, Loader2 } from 'lucide-vue-next'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { register } = useAuth()

const form = ref({
  full_name: '',
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  agree_terms: false
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const error = ref(null)

const handleRegister = async () => {
  error.value = null

  // Validation
  if (form.value.password !== form.value.confirm_password) {
    error.value = 'Password dan konfirmasi password tidak cocok'
    return
  }

  if (form.value.password.length < 6) {
    error.value = 'Password minimal 6 karakter'
    return
  }

  if (!form.value.agree_terms) {
    error.value = 'Anda harus menyetujui Syarat & Ketentuan'
    return
  }

  isLoading.value = true

  try {
    await register({
      full_name: form.value.full_name,
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    })
    router.push('/ai-check')
  } catch (err) {
    error.value = err.message || 'Registrasi gagal. Silakan coba lagi.'
  } finally {
    isLoading.value = false
  }
}
</script>
