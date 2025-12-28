<template>
  <!-- Floating Chat Bubble -->
  <div class="fixed bottom-6 right-6 z-50">
    <!-- Chat Bubble Button -->
    <Transition name="bubble">
      <button
        v-if="!isOpen"
        @click="toggleChat"
        class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full shadow-2xl hover:shadow-blue-500/50 hover:scale-110 transition-all duration-300 flex items-center justify-center group relative"
        aria-label="Open Chat"
      >
        <span class="text-3xl">💬</span>
        
        <!-- Notification Badge (optional) -->
        <span class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center animate-pulse">
          !
        </span>
        
        <!-- Hover Tooltip -->
        <div class="absolute bottom-full right-0 mb-2 px-3 py-1 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
          Chat dengan AI
        </div>
      </button>
    </Transition>

    <!-- Chat Panel -->
    <Transition name="slide-up">
      <div
        v-if="isOpen"
        class="fixed bottom-0 right-0 w-full md:w-[400px] md:bottom-6 md:right-6 bg-white rounded-t-3xl md:rounded-3xl shadow-2xl overflow-hidden"
        style="height: 40vh; min-height: 400px; max-height: 600px;"
      >
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-500 to-blue-600 px-5 py-4 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <span class="text-2xl">🤖</span>
            </div>
            <div>
              <h3 class="text-white font-semibold">SkinGuard AI Assistant</h3>
              <p class="text-blue-100 text-xs">Selalu siap membantu</p>
            </div>
          </div>
          <button
            @click="toggleChat"
            class="w-8 h-8 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center transition-colors"
            aria-label="Close Chat"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Chat Messages Area -->
        <div
          ref="chatContainer"
          class="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50"
          style="height: calc(100% - 140px);"
        >
          <!-- Welcome Message -->
          <div v-if="messages.length === 0" class="text-center py-8">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-3xl">👋</span>
            </div>
            <p class="text-gray-600 text-sm">
              Halo! Ada yang bisa saya bantu tentang<br/>kesehatan kulit Anda?
            </p>
          </div>

          <!-- Messages -->
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="flex"
            :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div
              class="max-w-[75%] rounded-2xl px-4 py-2 shadow-sm"
              :class="message.role === 'user' 
                ? 'bg-blue-500 text-white rounded-br-sm' 
                : 'bg-white text-gray-800 rounded-bl-sm border border-gray-200'"
            >
              <p class="text-sm whitespace-pre-wrap">{{ message.content }}</p>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isLoading" class="flex justify-start">
            <div class="bg-white rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm border border-gray-200">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
                <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="border-t border-gray-200 p-3 bg-white">
          <form @submit.prevent="sendMessage" class="flex gap-2">
            <input
              v-model="userInput"
              type="text"
              placeholder="Ketik pesan..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100 text-sm"
              :disabled="isLoading"
            />
            <button
              type="submit"
              :disabled="!userInput.trim() || isLoading"
              class="w-10 h-10 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center flex-shrink-0"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
            </button>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { chatWithBot } from '../utils/api'

const props = defineProps({
  openFromNavbar: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:openFromNavbar'])

const isOpen = ref(false)
const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const chatContainer = ref(null)

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (!isOpen.value) {
    emit('update:openFromNavbar', false)
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const userMessage = {
    role: 'user',
    content: userInput.value,
    timestamp: Date.now()
  }

  messages.value.push(userMessage)
  const currentInput = userInput.value
  userInput.value = ''
  
  await scrollToBottom()
  
  isLoading.value = true

  try {
    const response = await chatWithBot(currentInput)
    
    const botMessage = {
      role: 'assistant',
      content: response.reply,
      timestamp: Date.now()
    }

    messages.value.push(botMessage)
  } catch (error) {
    console.error('❌ Chat Error:', error)
    
    const errorMessage = {
      role: 'assistant',
      content: 'Maaf, terjadi kesalahan. Silakan coba lagi.',
      timestamp: Date.now()
    }

    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

// Watch for navbar trigger
watch(() => props.openFromNavbar, (newVal) => {
  if (newVal) {
    isOpen.value = true
  }
})
</script>

<style scoped>
/* Bubble Animation */
.bubble-enter-active,
.bubble-leave-active {
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.bubble-enter-from,
.bubble-leave-to {
  transform: scale(0) rotate(45deg);
  opacity: 0;
}

/* Slide Up Animation */
.slide-up-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.slide-up-leave-active {
  transition: all 0.3s ease-in;
}

.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
