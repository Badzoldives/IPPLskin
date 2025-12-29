<template>
  <footer class="bg-navy-dark text-white py-12 mt-20">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
        <!-- Brand -->
        <div>
          <div class="gradient-text text-2xl mb-2">SkinCheck AI</div>
          <p class="text-gray-400 text-sm">
            AI-Powered Skin Health Detection
          </p>
        </div>

        <!-- Links -->
        <div>
          <h4 class="mb-4 text-white">Menu</h4>
          <div class="flex flex-col gap-2 text-sm">
            <router-link to="/" class="text-gray-400 hover:text-white transition-colors">
              Beranda
            </router-link>
            <router-link to="/ai-check" class="text-gray-400 hover:text-white transition-colors">
              AI Skin Check
            </router-link>
            <router-link to="/dokumentasi" class="text-gray-400 hover:text-white transition-colors">
              Dokumentasi
            </router-link>
          </div>
        </div>

        <!-- Legal -->
        <div>
          <h4 class="mb-4 text-white">Legal</h4>
          <div class="flex flex-col gap-2 text-sm">
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              Kebijakan Privasi
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              Disclaimer Medis
            </a>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-700 pt-6 text-center text-sm text-gray-400">
        © {{ currentYear }} SkinCheck AI. All rights reserved.
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>
