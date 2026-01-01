<template>
  <div class="image-uploader">
    <!-- Hidden file input always present to ensure trigger works -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      class="hidden"
      @change="onFileChange"
    />
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
        <p class="text-gray-500 mb-6">Format: JPG, JPEG, PNG, WEBP (Max {{ maxSizeMB }}MB). Format HEIC belum didukung.</p>

        <div class="flex gap-4">
          <label class="bg-white border border-gray-200 text-gray-800 px-6 py-3 rounded-full hover:bg-gray-50 transition-opacity cursor-pointer flex-1 text-center" @click.prevent="triggerFilePicker">
            Pilih Foto
          </label>
        </div>
        
        
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
      
      <!-- Action Buttons: Ganti Foto + Analisis Sekarang -->
      <div class="flex gap-4">
        <div class="flex-1 grid grid-cols-2 gap-2">
          <button
            @click="triggerFilePicker"
            class="border border-gray-300 text-gray-700 px-4 py-3 rounded-full hover:bg-gray-50 transition-colors cursor-pointer text-center font-medium shadow-sm"
          >
            Ganti Foto
          </button>
          <button
            @click="analyzeImage"
            :disabled="isAnalyzing || isUploading"
            class="border border-blue-600 text-blue-600 px-4 py-3 rounded-full hover:bg-blue-50 transition-colors cursor-pointer text-center font-medium shadow-sm"
          >
            {{ isAnalyzing ? 'Menganalisis...' : 'Analisis Sekarang' }}
          </button>
        </div>
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
const prevObjectUrl = ref(null)
const analysisResult = ref(null)
const isSkinValid = ref(null)
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

  const name = file.name || ''
  const ext = name.split('.').pop()?.toLowerCase() || ''

  // Reject HEIC/HEIF explicitly per user request
  if (ext === 'heic' || ext === 'heif' || (file.type && file.type.includes('heic'))) {
    error.value = 'Format HEIC belum didukung, silakan pilih JPG/PNG'
    return false
  }

  const allowedExt = ['jpg', 'jpeg', 'png', 'webp']
  if (file.type && file.type.startsWith('image/')) {
    // allow image MIME types; some browsers may report webp/png/jpeg
  } else if (!allowedExt.includes(ext)) {
    error.value = 'Format file harus JPG/JPEG/PNG/WEBP'
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
          // Jika kompresi gagal (mis. format HEIC/unsupported), fallback gunakan file asli
          resolve(file)
        }
    })
  })
}

// No client-side HEIC conversion: HEIC is rejected and user is asked to provide JPG/PNG.

const createPreview = (file) => {
  // Revoke previous object URL to prevent leaks
  try {
    if (prevObjectUrl.value) {
      URL.revokeObjectURL(prevObjectUrl.value)
      prevObjectUrl.value = null
    }
  } catch (e) {}

  const url = URL.createObjectURL(file)
  previewUrl.value = url
  prevObjectUrl.value = url
}

const handleSelectedFile = async (file) => {
  if (!file) return

  if (!validateFile(file)) return

  try {
    // Do not attempt to convert HEIC — validateFile already rejected HEIC.
    // Create preview immediately, then process/compress in background and replace selectedFile
    createPreview(file)
    selectedFile.value = file
    // reset analysis state
    analysisResult.value = null
    isSkinValid.value = null
    hasAnalyzed.value = false
    error.value = null

    const processed = await compressFile(file)
    selectedFile.value = processed
    // update preview to processed blob (revoke old URL)
    createPreview(processed)
  } catch (err) {
    error.value = 'Gagal memproses gambar: ' + (err?.message || err)
    emit('error', err)
  }
}

const onFileChange = (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  // Reset previous analysis state and errors
  analysisResult.value = null
  error.value = null
  isSkinValid.value = null
  hasAnalyzed.value = false
  isAnalyzing.value = false
  isUploading.value = false
  uploadProgress.value = 0

  // Revoke old preview if any
  try { if (prevObjectUrl.value) { URL.revokeObjectURL(prevObjectUrl.value); prevObjectUrl.value = null } } catch (e) {}

  // Immediately set preview using object URL
  const objUrl = URL.createObjectURL(file)
  previewUrl.value = objUrl
  prevObjectUrl.value = objUrl

  // Process file (compress and set selectedFile)
  handleSelectedFile(file)

  // Reset input value so same file can be selected again
  try { event.target.value = '' } catch (e) {}
}

const triggerFilePicker = () => {
  if (!fileInput.value) return
  try { fileInput.value.value = '' } catch (e) {}
  fileInput.value.click()
}

// Simple skin-detection heuristic using RGB thresholds on a downsized canvas.
// Returns true if a sufficient proportion of sampled pixels look like skin.
const isLikelySkinImage = (file) => {
  return new Promise((resolve) => {
    try {
      const img = new Image()
      img.onload = () => {
        // draw to small canvas
        const MAX = 200
        const w = img.width
        const h = img.height
        const scale = Math.min(1, Math.max(1, Math.min(MAX / w, MAX / h)))
        const cw = Math.max(50, Math.floor(w * scale))
        const ch = Math.max(50, Math.floor(h * scale))
        const canvas = document.createElement('canvas')
        canvas.width = cw
        canvas.height = ch
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, cw, ch)
        try {
          const data = ctx.getImageData(0, 0, cw, ch).data
          let skinCount = 0
          let total = 0
          // sample every 4th pixel to speed up
          for (let i = 0; i < data.length; i += 4 * 4) {
            const r = data[i]
            const g = data[i + 1]
            const b = data[i + 2]

            // basic RGB skin heuristic
            const max = Math.max(r, g, b)
            const min = Math.min(r, g, b)
            const rgDiff = Math.abs(r - g)
            if (
              r > 95 && g > 40 && b > 20 &&
              max - min > 15 && r > g && r > b && rgDiff > 15
            ) {
              skinCount++
            }
            total++
          }
          const ratio = total > 0 ? skinCount / total : 0
          // consider image skin if > 15% of sampled pixels match heuristic
          resolve(ratio >= 0.15)
        } catch (e) {
          // If cross-origin or other error, fallback to allowing analysis
          resolve(true)
        }
      }
      img.onerror = () => resolve(true)
      const reader = new FileReader()
      reader.onload = (ev) => {
        img.src = ev.target.result
      }
      reader.readAsDataURL(file)
    } catch (e) {
      resolve(true)
    }
  })
}

const handleDrop = async (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (!file) return
  await handleSelectedFile(file)
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
    // Run simple skin presence check first
    const isSkin = await isLikelySkinImage(selectedFile.value)
    if (!isSkin) {
      error.value = 'Foto tidak terdeteksi sebagai kulit. Silakan upload foto area kulit dengan pencahayaan baik.'
      isAnalyzing.value = false
      return
    }

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
    // revoke preview URL if any
    try { if (prevObjectUrl.value) { URL.revokeObjectURL(prevObjectUrl.value); prevObjectUrl.value = null } } catch (e) {}
    previewUrl.value = null
    error.value = null
    hasAnalyzed.value = false
    uploadProgress.value = 0
    analysisResult.value = null
    isSkinValid.value = null
    isAnalyzing.value = false
    isUploading.value = false
    if (fileInput.value) try { fileInput.value.value = '' } catch (e) {}
  }
})
</script>

<style scoped>
/* Add any additional styles here */
</style>
