<template>
  <!-- Overlay (klik untuk tutup menu) -->
  <div
    v-if="mobileMenuOpen"
    class="fixed inset-0 bg-black/30 z-40 md:hidden"
    @click="closeMobileMenu"
    aria-hidden="true"
  />

  <nav class="site-navbar sticky top-0 left-0 right-0 z-50 bg-white border-b border-slate-200 shadow-sm relative">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- TOP BAR (tinggi fix 72px) -->
      <div class="h-[72px] flex items-center justify-between">
        <!-- Logo -->
          <router-link to="/" class="flex flex-col">
          <span class="text-2xl gradient-text">SkinGuard AI</span>
        </router-link>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center gap-8">
          <router-link
            to="/"
            class="hover:text-primary-blue transition-colors"
            :class="isActive('/') ? 'text-primary-blue' : 'text-gray-700'"
          >
            Beranda
          </router-link>

          <router-link
            to="/ai-check"
            class="hover:text-primary-blue transition-colors"
            :class="isActive('/ai-check') ? 'text-primary-blue' : 'text-gray-700'"
          >
            AI Skin Guard
          </router-link>

          <template v-if="isAuthenticated">
            <router-link
              to="/history"
              class="hover:text-primary-blue transition-colors"
              :class="isActive('/history') ? 'text-primary-blue' : 'text-gray-700'"
            >
              Riwayat
            </router-link>
          </template>

          <router-link
            to="/dokumentasi"
            class="hover:text-primary-blue transition-colors"
            :class="isActive('/dokumentasi') ? 'text-primary-blue' : 'text-gray-700'"
          >
            Dokumentasi
          </router-link>

          <!-- Chat AI Button -->
          <button
            @click="openChatbot"
            class="flex items-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full hover:shadow-sm transition-all duration-200"
            aria-label="Open chat"
          >
            <span class="text-base">💬</span>
            <span class="font-medium text-sm">Chat AI</span>
          </button>

          <!-- Auth Buttons -->
          <template v-if="!isAuthenticated">
            <router-link
              to="/login"
              class="px-4 py-2 rounded-md border border-gray-200 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Masuk
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 rounded-md bg-blue-600 text-white text-sm hover:bg-blue-700 transition-colors"
            >
              Daftar
            </router-link>
          </template>

          <!-- User Menu -->
          <div v-else class="relative">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center gap-2 hover:text-primary-blue transition-colors"
            >
              <div class="w-10 h-10 gradient-primary rounded-full flex items-center justify-center text-white">
                {{ user?.username?.charAt(0).toUpperCase() }}
              </div>
            </button>

            <transition name="dropdown">
              <div
                v-if="showUserMenu"
                @click.away="showUserMenu = false"
                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-sm py-2 z-50 border border-slate-100"
              >
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm text-navy-dark">{{ user?.full_name || user?.username }}</p>
                  <p class="text-xs text-gray-500">{{ user?.email }}</p>
                </div>

                <router-link
                  to="/history"
                  @click="showUserMenu = false"
                  class="flex items-center gap-2 px-4 py-2 hover:bg-gray-50 transition-colors"
                >
                  <HistoryIcon :size="16" />
                  <span class="text-sm">Riwayat Analisis</span>
                </router-link>

                <button
                  @click="handleLogout"
                  class="flex items-center gap-2 px-4 py-2 hover:bg-gray-50 transition-colors w-full text-left text-red-600"
                >
                  <LogOut :size="16" />
                  <span class="text-sm">Keluar</span>
                </button>
              </div>
            </transition>
          </div>
        </div>

        <!-- Mobile Menu Button -->
        <button
          @click="toggleMobileMenu"
          class="md:hidden text-gray-700 hover:text-blue-600 transition-colors"
          aria-label="Open menu"
        >
          <Menu v-if="!mobileMenuOpen" :size="22" />
          <X v-else :size="22" />
        </button>
      </div>
    </div>

    <!-- MOBILE MENU PANEL (solid putih & rapi) -->
    <transition name="slide">
      <div
        v-if="mobileMenuOpen"
        class="md:hidden absolute left-0 right-0 top-[72px] bg-white border-t border-slate-200 shadow-md z-50"
      >
        <div class="max-w-7xl mx-auto px-4 sm:px-6 py-4">
          <div class="flex flex-col gap-3">
            <router-link
              to="/"
              @click="closeMobileMenu"
              class="py-2 text-sm font-medium"
              :class="isActive('/') ? 'text-primary-blue' : 'text-gray-800'"
            >
              Beranda
            </router-link>

            <router-link
              to="/ai-check"
              @click="closeMobileMenu"
              class="py-2 text-sm font-medium"
              :class="isActive('/ai-check') ? 'text-primary-blue' : 'text-gray-800'"
            >
              AI Skin Guard
            </router-link>

            <template v-if="isAuthenticated">
              <router-link
                to="/history"
                @click="closeMobileMenu"
                class="py-2 text-sm font-medium"
                :class="isActive('/history') ? 'text-primary-blue' : 'text-gray-800'"
              >
                Riwayat
              </router-link>
            </template>

            <router-link
              to="/dokumentasi"
              @click="closeMobileMenu"
              class="py-2 text-sm font-medium"
              :class="isActive('/dokumentasi') ? 'text-primary-blue' : 'text-gray-800'"
            >
              Dokumentasi
            </router-link>

            <button
              @click="openChatbot(); closeMobileMenu()"
              class="mt-2 flex items-center justify-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full hover:shadow-sm transition-all duration-200"
            >
              <span class="text-sm font-medium">Chat AI</span>
            </button>

            <template v-if="!isAuthenticated">
              <div class="mt-2 grid grid-cols-2 gap-3">
                <router-link
                  to="/login"
                  @click="closeMobileMenu"
                  class="border border-blue-600 text-blue-700 px-4 py-2 rounded-full text-center text-sm font-medium hover:bg-blue-50"
                >
                  Masuk
                </router-link>

                <router-link
                  to="/register"
                  @click="closeMobileMenu"
                  class="bg-blue-600 text-white px-4 py-2 rounded-full text-center text-sm font-medium hover:bg-blue-700"
                >
                  Daftar
                </router-link>
              </div>
            </template>

            <template v-else>
              <div class="mt-4 pt-4 border-t border-slate-200">
                <p class="text-sm text-navy-dark mb-1">{{ user?.full_name || user?.username }}</p>
                <p class="text-xs text-gray-500 mb-3">{{ user?.email }}</p>
                <button
                  @click="handleLogout"
                  class="w-full text-left text-red-600 flex items-center gap-2 py-2"
                >
                  <LogOut :size="16" />
                  <span>Keluar</span>
                </button>
              </div>
            </template>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>


<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu, X, User, LogOut, History as HistoryIcon } from 'lucide-vue-next'
import { useAuth } from '../composables/useAuth'

const route = useRoute()
const router = useRouter()
const { isAuthenticated, user, logout } = useAuth()
const mobileMenuOpen = ref(false)
const showUserMenu = ref(false)

const emit = defineEmits(['open-chatbot'])

const isActive = (path) => {
  return route.path === path
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const openChatbot = () => {
  emit('open-chatbot')
}

const handleLogout = () => {
  logout()
  showUserMenu.value = false
  closeMobileMenu()
  router.push('/')
}
</script>

<style scoped>
/* Navbar local styles only - global page offset handled in global CSS */
:root {
  --navbar-height: 72px;
}

/* Mobile menu slide animation */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Dropdown animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}
</style>
