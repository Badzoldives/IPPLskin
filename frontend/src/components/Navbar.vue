<template>
  <nav class="sticky top-0 left-0 right-0 z-50 bg-white shadow-sm border-b border-slate-200" style="height:72px; backdrop-filter: none;">
    <div class="max-w-7xl mx-auto px-8 h-full">
      <div class="flex items-center justify-between h-full">
        <!-- Logo -->
        <router-link to="/" class="flex flex-col">
          <span class="text-2xl gradient-text">SkinGuard AI</span>
          <span class="text-xs text-gray-500">AI-Powered Skin Health</span>
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
            AI Skin Check
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
            
            <!-- Dropdown -->
            <transition name="dropdown">
              <div
                v-if="showUserMenu"
                @click.away="showUserMenu = false"
                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-sm py-2 z-50"
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

      <!-- Mobile Menu -->
      <transition name="slide">
        <div v-if="mobileMenuOpen" class="md:hidden mt-0 pb-4">
          <div class="flex flex-col gap-4">
            <router-link 
              to="/" 
              @click="closeMobileMenu"
              class="hover:text-primary-blue transition-colors"
              :class="isActive('/') ? 'text-primary-blue' : 'text-gray-700'"
            >
              Beranda
            </router-link>
            
            <router-link 
              to="/ai-check" 
              @click="closeMobileMenu"
              class="hover:text-primary-blue transition-colors"
              :class="isActive('/ai-check') ? 'text-primary-blue' : 'text-gray-700'"
            >
              AI Skin Check
            </router-link>
            <template v-if="isAuthenticated">
              <router-link 
                to="/history" 
                @click="closeMobileMenu"
                class="hover:text-primary-blue transition-colors"
                :class="isActive('/history') ? 'text-primary-blue' : 'text-gray-700'"
              >
                Riwayat
              </router-link>
            </template>
            
            <router-link 
              to="/dokumentasi" 
              @click="closeMobileMenu"
              class="hover:text-primary-blue transition-colors"
              :class="isActive('/dokumentasi') ? 'text-primary-blue' : 'text-gray-700'"
            >
              Dokumentasi
            </router-link>
            
            <!-- Chat AI Button Mobile -->
            <button
              @click="openChatbot(); closeMobileMenu()"
              class="flex items-center justify-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full hover:shadow-sm transition-all duration-200"
            >
              <span class="text-sm">Chat AI</span>
            </button>
            
            <template v-if="!isAuthenticated">
              <router-link 
                to="/login"
                @click="closeMobileMenu"
                class="border-2 border-primary-blue text-primary-blue px-6 py-2.5 rounded-full hover:bg-blue-50 transition-colors text-center"
              >
                Masuk
              </router-link>
              <router-link 
                to="/register"
                @click="closeMobileMenu"
                class="gradient-primary text-white px-6 py-2.5 rounded-full hover:opacity-90 transition-opacity text-center"
              >
                Daftar
              </router-link>
            </template>
            
            <template v-else>
              <div class="pt-4 border-t border-gray-200">
                <p class="text-sm text-navy-dark mb-1">{{ user?.full_name || user?.username }}</p>
                <p class="text-xs text-gray-500 mb-4">{{ user?.email }}</p>
                <button
                  @click="handleLogout"
                  class="w-full text-left text-red-600 flex items-center gap-2"
                >
                  <LogOut :size="16" />
                  <span>Keluar</span>
                </button>
              </div>
            </template>
          </div>
        </div>
      </transition>
    </div>
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
