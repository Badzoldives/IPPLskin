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

      <!-- Results Section -->
      <transition name="fade">
        <div v-if="showResult && analysisResult" class="space-y-6">
          <!-- Card 1 - AI Analysis Result -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 30 }"
            :enter="{ opacity: 1, y: 0 }"
            class="bg-white rounded-4xl p-8 card-shadow"
          >
            <div class="flex items-start gap-4 mb-6">
              <div class="w-14 h-14 gradient-primary rounded-xl flex items-center justify-center glow-icon">
                <ImageIcon :size="28" class="text-white" />
              </div>
              <div class="flex-1">
                <h2 class="text-2xl mb-2">Hasil Analisis AI</h2>
                <p class="text-gray-600">Berdasarkan analisis gambar yang Anda upload</p>
              </div>
            </div>

            <div class="border-t border-gray-200 pt-6">
              <h3 class="text-xl mb-4">{{ analysisResult.condition }}</h3>
              
              <div class="mb-6">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm text-gray-600">Tingkat Kepercayaan AI</span>
                  <span class="text-sm">{{ analysisResult.confidence }}%</span>
                </div>
                <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    class="h-full gradient-primary transition-all duration-500"
                    :style="{ width: analysisResult.confidence + '%' }"
                  ></div>
                </div>
              </div>

              <!-- Warning jika confidence rendah -->
              <div v-if="analysisResult.warning" class="mb-4 bg-orange-50 border-l-4 border-orange-500 p-4 rounded-lg">
                <p class="text-sm text-orange-800">
                  <strong>⚠️ Perhatian:</strong> {{ analysisResult.warning }}
                </p>
              </div>

              <div class="bg-yellow-50 border-l-4 border-warning p-4 rounded-lg">
                <p class="text-sm text-gray-dark">
                  ⚠️ <strong>Penting:</strong> Ini bukan diagnosis pasti. Hasil ini adalah prediksi AI yang dapat membantu Anda mendapat gambaran awal.
                </p>
              </div>
            </div>
          </div>

          <!-- Card 2 - Condition Summary -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 30 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: 100 } }"
            class="bg-white rounded-4xl p-8 card-shadow"
          >
            <h2 class="text-2xl mb-6">Ringkasan Kondisi</h2>
            
            <div class="space-y-4 text-gray-600">
              <p>{{ analysisResult.description }}</p>
              <p>
                Dermatitis atopik sering kali dimulai pada masa kanak-kanak, namun dapat berlanjut atau bahkan baru muncul pada usia dewasa. Kondisi ini tidak menular dan bersifat kambuhan (dapat hilang dan muncul kembali).
              </p>
              <p>
                Penyebab pasti dermatitis atopik belum sepenuhnya dipahami, namun diduga terkait dengan kombinasi faktor genetik, disfungsi sistem kekebalan tubuh, dan gangguan pada penghalang pelindung kulit.
              </p>
              <p>
                Gejala utama meliputi kulit yang sangat kering, gatal (terutama malam hari), ruam merah atau kecoklatan, kulit menebal atau bersisik, dan kulit yang mudah teriritasi.
              </p>
            </div>
          </div>

          <!-- Card 3 - Initial Treatment -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 30 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: 200 } }"
            class="bg-white rounded-4xl p-8 card-shadow"
          >
            <h2 class="text-2xl mb-6">Cara Penanganan Awal</h2>
            
            <div class="space-y-4">
              <div 
                v-for="(recommendation, index) in analysisResult.recommendations"
                :key="index"
                class="flex items-start gap-3"
              >
                <CheckCircle2 :size="24" class="text-primary-green shrink-0 mt-1" />
                <div>
                  <p class="text-gray-dark">{{ recommendation }}</p>
                </div>
              </div>

              <div class="flex items-start gap-3">
                <CheckCircle2 :size="24" class="text-primary-green shrink-0 mt-1" />
                <div>
                  <h4 class="mb-1">Jaga Kebersihan Kulit</h4>
                  <p class="text-sm text-gray-600">
                    Mandi dengan air hangat (bukan panas) selama 5-10 menit. Hindari menggosok kulit terlalu keras.
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-3">
                <CheckCircle2 :size="24" class="text-primary-green shrink-0 mt-1" />
                <div>
                  <h4 class="mb-1">Gunakan Sabun Lembut</h4>
                  <p class="text-sm text-gray-600">
                    Pilih sabun atau pembersih yang lembut, bebas pewangi, dan pH seimbang yang dirancang khusus untuk kulit sensitif.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 4 - Medication Recommendations -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 30 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: 300 } }"
            class="bg-white rounded-4xl p-8 card-shadow"
          >
            <h2 class="text-2xl mb-6">Rekomendasi Obat & Tindakan</h2>
            
            <div class="space-y-4 text-gray-600 mb-6">
              <div>
                <h4 class="text-navy-dark mb-2">Kortikosteroid Topikal</h4>
                <p class="text-sm">
                  Krim atau salep kortikosteroid dapat membantu mengurangi peradangan dan gatal. Gunakan sesuai anjuran dokter.
                </p>
              </div>

              <div>
                <h4 class="text-navy-dark mb-2">Antihistamin</h4>
                <p class="text-sm">
                  Dapat membantu mengurangi rasa gatal, terutama yang mengganggu tidur di malam hari.
                </p>
              </div>

              <div>
                <h4 class="text-navy-dark mb-2">Pelembap Medis (Emolien)</h4>
                <p class="text-sm">
                  Produk berbasis ceramide atau asam hialuronat dapat membantu memperbaiki barrier kulit.
                </p>
              </div>

              <div>
                <h4 class="text-navy-dark mb-2">Imunomodulator Topikal</h4>
                <p class="text-sm">
                  Untuk kasus yang tidak merespons terhadap kortikosteroid, dokter mungkin meresepkan alternatif ini.
                </p>
              </div>
            </div>

            <div class="bg-orange-50 border-l-4 border-warning p-4 rounded-lg">
              <div class="flex items-start gap-2">
                <AlertTriangle :size="20" class="text-warning shrink-0 mt-0.5" />
                <p class="text-sm text-gray-dark">
                  <strong>Perhatian:</strong> Jangan menggunakan obat tanpa konsultasi dokter. Informasi di atas hanya bersifat edukatif. Dokter akan menentukan jenis dan dosis obat yang tepat untuk kondisi Anda.
                </p>
              </div>
            </div>
          </div>

          <!-- Card 5 - When to See Doctor -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 30 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: 400 } }"
            class="bg-white rounded-4xl p-8 card-shadow"
          >
            <h2 class="text-2xl mb-6">Kapan Harus ke Dokter?</h2>
            
            <p class="text-gray-600 mb-6">
              Segera konsultasikan dengan dokter atau dermatolog jika Anda mengalami:
            </p>

            <div class="space-y-3">
              <div class="flex items-start gap-3 p-4 bg-red-50 rounded-xl">
                <AlertCircle :size="20" class="text-red-500 shrink-0 mt-0.5" />
                <p class="text-sm text-gray-700">
                  Nyeri yang sangat mengganggu atau tidak tertahankan
                </p>
              </div>

              <div class="flex items-start gap-3 p-4 bg-red-50 rounded-xl">
                <AlertCircle :size="20" class="text-red-500 shrink-0 mt-0.5" />
                <p class="text-sm text-gray-700">
                  Ruam menyebar dengan cepat atau meluas ke area tubuh lain
                </p>
              </div>

              <div class="flex items-start gap-3 p-4 bg-red-50 rounded-xl">
                <AlertCircle :size="20" class="text-red-500 shrink-0 mt-0.5" />
                <p class="text-sm text-gray-700">
                  Tidak ada perbaikan setelah beberapa hari perawatan mandiri
                </p>
              </div>

              <div class="flex items-start gap-3 p-4 bg-red-50 rounded-xl">
                <AlertCircle :size="20" class="text-red-500 shrink-0 mt-0.5" />
                <p class="text-sm text-gray-700">
                  Timbul demam, nanah, atau tanda-tanda infeksi lainnya
                </p>
              </div>
            </div>

            <div class="mt-6 p-4 bg-blue-50 rounded-xl">
              <p class="text-sm text-primary-blue">
                💡 <strong>Ingat:</strong> Dermatolog adalah spesialis yang paling tepat untuk mendiagnosis dan merawat kondisi kulit Anda.
              </p>
            </div>
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
