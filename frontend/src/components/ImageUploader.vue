<template>
  <div class="image-uploader">
    <!-- Upload Area -->
    <div
      v-if="!previewUrl"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      class="border-2 border-dashed rounded-3xl p-12 text-center transition-colors cursor-pointer"
      :class="isDragging ? 'border-primary-blue bg-blue-50' : 'border-border-light hover:border-primary-blue'"
    >
      <div class="flex flex-col items-center">
        <div class="w-20 h-20 gradient-primary rounded-3xl flex items-center justify-center mb-6 glow-icon">
          <Upload :size="40" class="text-white" />
        </div>
        <h3 class="mb-2">Tarik & lepaskan atau klik untuk memilih file</h3>
        <p class="text-gray-500 mb-6">Format: JPG, PNG (Max {{ maxSizeMB }}MB)</p>
        
        <label class="gradient-primary text-white px-8 py-3 rounded-full hover:opacity-90 transition-opacity cursor-pointer">
          Pilih Foto
          <input
            ref="fileInput"
            type="file"
            accept="image/jpeg,image/png,image/jpg"
            @change="handleFileSelect"
            class="hidden"
          />
        </label>
        
        
      </div>
    </div>

    <!-- Preview & Actions -->
    <div v-else class="space-y-6">
      <!-- Image Preview -->
      <div class="relative rounded-3xl overflow-hidden">
        <img 
          :src="previewUrl" 
          alt="Preview" 
          class="w-full max-h-96 object-cover"
        />
        
        <!-- Upload Progress Overlay -->
        <div 
          v-if="isUploading" 
          class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center"
        >
          <div class="bg-white rounded-2xl p-6 max-w-xs w-full mx-4">
            <div class="flex items-center gap-3 mb-3">
              <Loader2 :size="24" class="text-primary-blue animate-spin" />
              <span class="text-navy-dark">Mengupload...</span>
            </div>
            <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                class="h-full gradient-primary transition-all duration-300"
                :style="{ width: uploadProgress + '%' }"
              ></div>
            </div>
            <p class="text-sm text-gray-600 mt-2">{{ uploadProgress }}%</p>
          </div>
        </div>
      </div>

      <!-- File Info -->
      <div class="bg-blue-50 rounded-2xl p-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <ImageIcon :size="20" class="text-primary-blue" />
          <div>
            <p class="text-sm text-navy-dark">{{ fileName }}</p>
            <p class="text-xs text-gray-600">{{ fileSizeFormatted }}</p>
          </div>
        </div>
        <CheckCircle2 :size="24" class="text-primary-green" />
      </div>
      
      <!-- Action Buttons -->
      <div class="flex gap-4">
        <button
          @click="analyzeImage"
          :disabled="isAnalyzing || isUploading"
          class="flex-1 bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium shadow-md"
        >
          <Loader2 v-if="isAnalyzing" :size="20" class="animate-spin" />
          <span>{{ isAnalyzing ? 'Menganalisis...' : 'Analisis Sekarang' }}</span>
        </button>
        
        <label class="flex-1 border-2 border-blue-600 text-blue-600 px-6 py-3 rounded-full hover:bg-blue-50 transition-colors cursor-pointer text-center font-medium shadow-sm">
          Ganti Foto
          <input
            type="file"
            accept="image/jpeg,image/png,image/jpg"
            @change="handleFileSelect"
            class="hidden"
          />
        </label>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-4 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
      <div class="flex items-start gap-2">
        <AlertCircle :size="20" class="text-red-500 shrink-0 mt-0.5" />
        <p class="text-sm text-red-700">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Upload, Loader2, ImageIcon, CheckCircle2, AlertCircle } from 'lucide-vue-next'
import Compressor from 'compressorjs'

const props = defineProps({
  maxSizeMB: {
    type: Number,
    default: 10
  },
  compressImage: {
    type: Boolean,
    default: true
  },
  compressionQuality: {
    type: Number,
    default: 0.8
  }
})

const emit = defineEmits(['upload-success', 'analyze-complete', 'error'])

const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)
const isDragging = ref(false)
const isUploading = ref(false)
const isAnalyzing = ref(false)
const hasAnalyzed = ref(false)
const uploadProgress = ref(0)
const error = ref(null)

const fileName = computed(() => selectedFile.value?.name || '')
const fileSize = computed(() => selectedFile.value?.size || 0)
const fileSizeFormatted = computed(() => {
  const size = fileSize.value
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(2) + ' KB'
  return (size / (1024 * 1024)).toFixed(2) + ' MB'
})

const validateFile = (file) => {
  error.value = null
  
  if (!file) {
    error.value = 'File tidak ditemukan'
    return false
  }

  if (!file.type.match(/image\/(jpeg|jpg|png)/)) {
    error.value = 'Format file harus JPG atau PNG'
    return false
  }

  const maxSize = props.maxSizeMB * 1024 * 1024
  if (file.size > maxSize) {
    error.value = `Ukuran file maksimal ${props.maxSizeMB}MB`
    return false
  }

  return true
}

const compressFile = (file) => {
  return new Promise((resolve, reject) => {
    if (!props.compressImage) {
      resolve(file)
      return
    }

    new Compressor(file, {
      quality: props.compressionQuality,
      maxWidth: 1920,
      maxHeight: 1920,
      mimeType: 'image/jpeg',
      success(result) {
        resolve(result)
      },
      error(err) {
        reject(err)
      }
    })
  })
}

const createPreview = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleFileSelect = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  if (!validateFile(file)) return

  try {
    const compressedFile = await compressFile(file)
    selectedFile.value = compressedFile
    createPreview(compressedFile)
    hasAnalyzed.value = false
    
    // Auto upload (optional)
    // await uploadToServer(compressedFile)
  } catch (err) {
    error.value = 'Gagal memproses gambar: ' + err.message
    emit('error', err)
  }
}

const handleDrop = async (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  
  if (!file) return
  if (!validateFile(file)) return

  try {
    const compressedFile = await compressFile(file)
    selectedFile.value = compressedFile
    createPreview(compressedFile)
    hasAnalyzed.value = false
  } catch (err) {
    error.value = 'Gagal memproses gambar: ' + err.message
    emit('error', err)
  }
}

// Example image feature removed

const uploadToServer = async (file) => {
  isUploading.value = true
  uploadProgress.value = 0
  error.value = null

  try {
    const { uploadImage } = await import('../utils/api')
    
    const data = await uploadImage(file, (progress) => {
      uploadProgress.value = progress
    })
    
    emit('upload-success', data)
    return data
  } catch (err) {
    error.value = 'Upload gagal: ' + err.message
    emit('error', err)
    throw err
  } finally {
    isUploading.value = false
  }
}

const analyzeImage = async () => {
  if (!selectedFile.value) return

  isAnalyzing.value = true
  error.value = null

  try {
    const { predictImage } = await import('../utils/api')
    
    // Directly predict using the image file
    const result = await predictImage(selectedFile.value)
    hasAnalyzed.value = true
    emit('analyze-complete', result)
  } catch (err) {
    console.error('Analysis error:', err)
    error.value = 'Analisis gagal: ' + (err.response?.data?.message || err.message || 'Silakan coba lagi')
    emit('error', err)
  } finally {
    isAnalyzing.value = false
  }
}

// Expose methods to parent
defineExpose({
  reset: () => {
    selectedFile.value = null
    previewUrl.value = null
    error.value = null
    hasAnalyzed.value = false
    uploadProgress.value = 0
  }
})
</script>

<style scoped>
/* Add any additional styles here */
</style>
