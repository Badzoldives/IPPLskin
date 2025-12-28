<template>
  <div class="pt-20 min-h-screen bg-gradient-to-br from-teal-50/30 via-blue-50/20 to-green-50/30">
    <div class="max-w-4xl mx-auto px-6 py-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-3">
          Konsultasi AI Kesehatan Kulit
        </h1>
        <p class="text-gray-600 text-lg">
          Tanyakan seputar penyakit kulit, gejala, dan perawatan kepada asisten AI kami
        </p>
      </div>

      <!-- Chat Container -->
      <div class="bg-white rounded-3xl shadow-xl overflow-hidden">
        <!-- Chat Messages -->
        <div 
          ref="chatContainer"
          class="h-[500px] overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-white to-gray-50"
        >
          <!-- Welcome Message -->
          <div v-if="messages.length === 0" class="text-center py-16">
            <div class="w-20 h-20 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-10 h-10 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Selamat datang!</h3>
            <p class="text-gray-600 max-w-md mx-auto">
              Saya siap membantu Anda dengan pertanyaan seputar kesehatan kulit, penyakit kulit, dan perawatan.
            </p>
            
            <!-- Quick Questions -->
            <div class="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-2xl mx-auto">
              <button
                v-for="question in quickQuestions"
                :key="question"
                @click="sendQuickQuestion(question)"
                class="p-4 bg-white border-2 border-teal-100 rounded-xl text-left hover:border-teal-300 hover:shadow-md transition-all duration-200"
              >
                <p class="text-sm text-gray-700">{{ question }}</p>
              </button>
            </div>
          </div>

          <!-- Chat Messages -->
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="flex"
            :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div
              class="max-w-[80%] rounded-2xl px-5 py-3 shadow-sm"
              :class="message.role === 'user' 
                ? 'bg-teal-600 text-white' 
                : 'bg-white border border-gray-200 text-gray-800'"
            >
              <p class="whitespace-pre-wrap leading-relaxed">{{ message.content }}</p>
              <span class="text-xs opacity-70 mt-2 block">
                {{ formatTime(message.timestamp) }}
              </span>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="flex justify-start">
            <div class="bg-white border border-gray-200 rounded-2xl px-5 py-3 shadow-sm">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="border-t border-gray-200 p-4 bg-white">
          <form @submit.prevent="sendMessage" class="flex gap-3">
            <input
              v-model="userInput"
              type="text"
              placeholder="Ketik pertanyaan Anda tentang kesehatan kulit..."
              class="flex-1 px-5 py-3 border-2 border-gray-200 rounded-full focus:border-teal-400 focus:outline-none transition-colors"
              :disabled="isTyping"
            />
            <button
              type="submit"
              :disabled="!userInput.trim() || isTyping"
              class="px-6 py-3 bg-teal-600 text-white rounded-full hover:bg-teal-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2 font-medium"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
              Kirim
            </button>
          </form>
          
          <!-- Disclaimer -->
          <p class="text-xs text-gray-500 mt-3 text-center">
            ⚠️ Informasi dari chatbot ini bersifat umum dan tidak menggantikan konsultasi dengan dokter profesional
          </p>
        </div>
      </div>

      <!-- Info Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900">Informasi Akurat</h3>
          </div>
          <p class="text-sm text-gray-600">Didukung oleh AI Gemini dengan pengetahuan medis terkini</p>
        </div>

        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900">Respon Cepat</h3>
          </div>
          <p class="text-sm text-gray-600">Dapatkan jawaban instan untuk pertanyaan Anda</p>
        </div>

        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900">Privasi Terjaga</h3>
          </div>
          <p class="text-sm text-gray-600">Percakapan Anda aman dan terlindungi</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { chatWithBot } from '../utils/api'

const messages = ref([])
const userInput = ref('')
const isTyping = ref(false)
const chatContainer = ref(null)

const quickQuestions = [
  'Apa saja gejala umum penyakit kulit?',
  'Bagaimana cara merawat kulit berjerawat?',
  'Apa perbedaan eksim dan psoriasis?',
  'Bagaimana mencegah infeksi kulit?'
]

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const sendQuickQuestion = (question) => {
  userInput.value = question
  sendMessage()
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
  
  isTyping.value = true

  try {
    const response = await chatWithBot(currentInput)
    
    const botMessage = {
      role: 'assistant',
      content: response.reply,
      timestamp: Date.now()
    }

    messages.value.push(botMessage)
  } catch (error) {
    console.error('Error:', error)
    
    const errorMessage = {
      role: 'assistant',
      content: 'Maaf, terjadi kesalahan saat memproses pertanyaan Anda. Silakan coba lagi.',
      timestamp: Date.now()
    }

    messages.value.push(errorMessage)
  } finally {
    isTyping.value = false
    await scrollToBottom()
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
