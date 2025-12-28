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
          <LogIn :size="40" class="text-white" />
        </div>
        <h1 class="text-4xl mb-3">Masuk ke Akun</h1>
        <p class="text-gray-600">
          Belum punya akun? 
          <router-link to="/register" class="text-primary-blue hover:underline">
            Daftar sekarang
          </router-link>
        </p>
      </div>

      <!-- Login Form -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 100 } }"
        class="bg-white rounded-4xl p-8 card-shadow"
      >
        <form @submit.prevent="handleLogin">
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
                placeholder="Masukkan password"
                required
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
          </div>

          <!-- Error Message -->
          <div v-if="error" class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
            <div class="flex items-start gap-2">
              <AlertCircle :size="20" class="text-red-500 shrink-0 mt-0.5" />
              <p class="text-sm text-red-700">{{ error }}</p>
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full gradient-primary text-white py-3 rounded-full hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <Loader2 v-if="isLoading" :size="20" class="animate-spin" />
            <span>{{ isLoading ? 'Memproses...' : 'Masuk' }}</span>
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

        <!-- Register Link -->
        <router-link
          to="/register"
          class="block w-full text-center border-2 border-primary-blue text-primary-blue py-3 rounded-full hover:bg-blue-50 transition-colors"
        >
          Buat Akun Baru
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
import { LogIn, Mail, Lock, Eye, EyeOff, AlertCircle, Loader2 } from 'lucide-vue-next'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { login } = useAuth()

const form = ref({
  email: '',
  password: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  error.value = null
  isLoading.value = true

  try {
    await login({
      email: form.value.email,
      password: form.value.password
    })
    router.push('/ai-check')
  } catch (err) {
    error.value = err.message || 'Login gagal. Periksa email dan password Anda.'
  } finally {
    isLoading.value = false
  }
}
</script>
