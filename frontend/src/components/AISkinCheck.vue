<template>
  <div class="pt-28 pb-20 bg-bg-soft min-h-screen">
    <div class="max-w-5xl mx-auto px-6">
      <!-- Header -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0 }"
        class="text-center mb-12"
      >
        <h1 class="text-5xl mb-4">Deteksi Kondisi Kulit dengan Foto</h1>
        <p class="text-lg text-gray-600">
          Informasi ini bukan diagnosis medis. Konsultasikan dengan dokter untuk diagnosis pasti.
        </p>
      </div>

      <!-- Upload Card -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 100 } }"
        class="bg-white rounded-4xl p-8 card-shadow mb-6"
      >
        <h2 class="text-2xl mb-6">Upload Foto Kulit Anda</h2>
        
        <ImageUploader
          ref="uploaderRef"
          :max-size-m-b="10"
          :compress-image="true"
          :compression-quality="0.8"
          @upload-success="handleUploadSuccess"
          @analyze-complete="handleAnalyzeComplete"
          @error="handleError"
        />

        <!-- Tips -->
        <div class="mt-8 bg-blue-50 rounded-2xl p-6">
          <h4 class="mb-4 text-primary-blue">Tips Foto yang Baik:</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div class="flex items-start gap-2">
              <CheckCircle2 :size="20" class="text-primary-green shrink-0 mt-0.5" />
              <span class="text-sm text-gray-700">Gunakan cahaya terang alami</span>
            </div>
            <div class="flex items-start gap-2">
              <CheckCircle2 :size="20" class="text-primary-green shrink-0 mt-0.5" />
              <span class="text-sm text-gray-700">Hindari bayangan keras</span>
            </div>
            <div class="flex items-start gap-2">
              <CheckCircle2 :size="20" class="text-primary-green shrink-0 mt-0.5" />
              <span class="text-sm text-gray-700">Jarak ideal 10-15 cm</span>
            </div>
            <div class="flex items-start gap-2">
              <CheckCircle2 :size="20" class="text-primary-green shrink-0 mt-0.5" />
              <span class="text-sm text-gray-700">Pastikan fokus jelas</span>
            </div>
          </div>
        </div>

        <!-- Privacy Notice -->
        <div class="mt-6 flex items-center justify-center gap-2 text-sm text-gray-500">
          <Lock :size="16" />
          <span>Foto tidak disimpan permanen - privasi Anda terjaga</span>
        </div>
      </div>

      <!-- Results Section (minimal) -->
      <transition name="fade">
        <div v-if="showResult && analysisResult" class="flex justify-center">
          <div
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            class="bg-white rounded-2xl p-8 w-full max-w-xl card-shadow text-center"
            role="region"
            aria-labelledby="result-title"
          >
            <h2 id="result-title" class="text-2xl sm:text-3xl font-semibold mb-4">Hasil Analisis</h2>
            <p class="text-lg sm:text-xl text-gray-800 font-medium break-words">{{ analysisResult.condition }}</p>
          </div>
        </div>
      </transition>

      <!-- Empty State when no image -->
      <div
        v-if="!hasImage && !showResult"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 200 } }"
        class="text-center py-12"
      >
        <div class="w-32 h-32 bg-border-light rounded-full flex items-center justify-center mx-auto mb-6">
          <ImageIcon :size="64" class="text-primary-blue" />
        </div>
        <h3 class="text-xl text-gray-600 mb-2">Belum Ada Foto yang Diupload</h3>
        <p class="text-gray-500">
          Upload foto kulit Anda untuk memulai analisis AI
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { CheckCircle2, Lock, ImageIcon, AlertCircle, AlertTriangle } from 'lucide-vue-next'
import ImageUploader from './ImageUploader.vue'

const uploaderRef = ref(null)
const showResult = ref(false)
const analysisResult = ref(null)
const hasImage = computed(() => uploaderRef.value?.previewUrl != null)

const handleUploadSuccess = (data) => {
  console.log('Upload success:', data)
}

const handleAnalyzeComplete = (result) => {
  console.log('Analysis complete:', result)
  
  // Check jika ada error dari backend (gambar bukan kulit)
  if (result.status === 'error') {
    const errorMsg = result.message || 'Terjadi kesalahan pada analisis'
    const suggestion = result.suggestion ? `\n\n${result.suggestion}` : ''
    alert(errorMsg + suggestion)
    showResult.value = false
    return
  }
  
  // Map backend response to frontend format
  if (result.status === 'success' && result.prediction) {
    // Split recommendation into array if it's a string with bullet points or numbered list
    let recommendations = []
    if (result.prediction.recommendation) {
      recommendations = result.prediction.recommendation
        .split(/[•\-\d+\.\n]+/)
        .map(r => r.trim())
        .filter(r => r.length > 10) // Filter out empty or very short strings
    }
    
    analysisResult.value = {
      condition: result.prediction.label,
      confidence: Math.round(result.prediction.confidence * 100),
      description: result.prediction.description,
      severity: result.prediction.severity,
      recommendation: result.prediction.recommendation,
      recommendations: recommendations,
      top3: result.top_3_predictions || [],
      warning: result.warning || null // Tambah warning dari backend
    }
    showResult.value = true
    
    // Scroll to results
    setTimeout(() => {
      window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: 'smooth'
      })
    }, 300)
  } else {
    handleError(new Error('Format respons tidak valid'))
  }
}

const handleError = (error) => {
  console.error('Error:', error)
  // Jika error dari axios (response 400), tampilkan pesan backend
  if (error && error.response && error.response.data) {
    const data = error.response.data
    let msg = data.message || 'Terjadi kesalahan pada analisis.'
    if (data.reason) msg += '\n\nAlasan: ' + data.reason
    if (data.suggestion) msg += '\n\nSaran: ' + data.suggestion
    alert(msg)
  } else {
    alert('Terjadi kesalahan: ' + (error.message || 'Silakan coba lagi'))
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
