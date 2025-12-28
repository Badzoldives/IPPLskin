<template>
  <div class="pt-28 pb-20 bg-bg-soft min-h-screen">
    <div class="max-w-6xl mx-auto px-6">
      <!-- Header -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0 }"
        class="text-center mb-12"
      >
        <h1 class="text-5xl mb-4">Riwayat Analisis</h1>
        <p class="text-lg text-gray-600">
          Semua hasil analisis kulit Anda tersimpan di sini
        </p>
      </div>

      <!-- Statistics Cards -->
      <div 
        v-if="stats && stats.total_diagnoses > 0"
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 50 } }"
        class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"
      >
        <div class="bg-white rounded-2xl p-6 card-shadow">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 gradient-primary rounded-xl flex items-center justify-center">
              <Activity :size="24" class="text-white" />
            </div>
            <div>
              <p class="text-2xl font-bold text-navy-dark">{{ stats.total_diagnoses }}</p>
              <p class="text-sm text-gray-500">Total Analisis</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-6 card-shadow">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
              <CheckCircle2 :size="24" class="text-white" />
            </div>
            <div>
              <p class="text-2xl font-bold text-navy-dark">{{ stats.severity_distribution?.low || 0 }}</p>
              <p class="text-sm text-gray-500">Severity Rendah</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-6 card-shadow">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-red-500 rounded-xl flex items-center justify-center">
              <AlertTriangle :size="24" class="text-white" />
            </div>
            <div>
              <p class="text-2xl font-bold text-navy-dark">{{ (stats.severity_distribution?.high || 0) + (stats.severity_distribution?.medium || 0) }}</p>
              <p class="text-sm text-gray-500">Perlu Perhatian</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div 
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 100 } }"
        class="flex flex-wrap gap-3 mb-8"
      >
        <button
          @click="loadHistory(1)"
          :disabled="isLoading"
          class="flex items-center gap-2 bg-white px-4 py-2 rounded-full card-shadow hover:bg-gray-50 transition-colors"
        >
          <RefreshCw :size="18" :class="{ 'animate-spin': isLoading }" />
          <span>Refresh</span>
        </button>

        <button
          v-if="histories.length > 0"
          @click="exportToCSV"
          class="flex items-center gap-2 bg-white px-4 py-2 rounded-full card-shadow hover:bg-gray-50 transition-colors"
        >
          <Download :size="18" />
          <span>Export CSV</span>
        </button>

        <button
          v-if="histories.length > 0"
          @click="confirmClearAll"
          class="flex items-center gap-2 bg-red-50 text-red-600 px-4 py-2 rounded-full hover:bg-red-100 transition-colors"
        >
          <Trash2 :size="18" />
          <span>Hapus Semua</span>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center py-20">
        <div class="text-center">
          <Loader2 :size="48" class="text-primary-blue animate-spin mx-auto mb-4" />
          <p class="text-gray-600">Memuat riwayat...</p>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="error"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0 }"
        class="text-center py-20"
      >
        <div class="w-32 h-32 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <AlertCircle :size="64" class="text-red-500" />
        </div>
        <h3 class="text-2xl text-gray-700 mb-3">Gagal Memuat Riwayat</h3>
        <p class="text-gray-600 mb-8">{{ error }}</p>
        <button
          @click="loadHistory(1)"
          class="inline-block gradient-primary text-white px-8 py-3 rounded-full hover:opacity-90 transition-opacity"
        >
          Coba Lagi
        </button>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="!histories.length"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0 }"
        class="text-center py-20"
      >
        <div class="w-32 h-32 bg-border-light rounded-full flex items-center justify-center mx-auto mb-6">
          <History :size="64" class="text-primary-blue" />
        </div>
        <h3 class="text-2xl text-gray-700 mb-3">Belum Ada Riwayat</h3>
        <p class="text-gray-600 mb-8">
          Anda belum melakukan analisis kulit. Mulai analisis pertama Anda sekarang!
        </p>
        <router-link
          to="/ai-check"
          class="inline-block gradient-primary text-white px-8 py-3 rounded-full hover:opacity-90 transition-opacity"
        >
          Mulai Analisis
        </router-link>
      </div>

      <!-- History List -->
      <div v-else class="space-y-6">
        <div
          v-for="(item, index) in histories"
          :key="item.id"
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: index * 50 } }"
          class="bg-white rounded-4xl p-6 card-shadow hover:shadow-lg transition-shadow"
        >
          <div class="flex flex-col md:flex-row gap-6">
            <!-- Image -->
            <div class="md:w-48 md:h-48 shrink-0">
              <img
                v-if="item.image_filename"
                :src="getImageUrl(item.image_filename)"
                :alt="item.condition"
                class="w-full h-48 object-cover rounded-2xl bg-gray-100"
                @error="handleImageError"
              />
              <div 
                v-else 
                class="w-full h-48 bg-gray-100 rounded-2xl flex items-center justify-center"
              >
                <ImageIcon :size="48" class="text-gray-400" />
              </div>
            </div>

            <!-- Content -->
            <div class="flex-1">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <h3 class="text-2xl text-navy-dark">{{ item.condition }}</h3>
                    <span 
                      :class="getSeverityClass(item.severity)"
                      class="px-2 py-1 rounded-full text-xs font-medium"
                    >
                      {{ getSeverityLabel(item.severity) }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-500 flex items-center gap-1">
                    <Calendar :size="16" />
                    {{ formatDate(item.created_at) }}
                  </p>
                </div>
                <button
                  @click="confirmDelete(item.id)"
                  class="text-red-400 hover:text-red-600 transition-colors p-2 rounded-full hover:bg-red-50"
                  title="Hapus"
                >
                  <Trash2 :size="20" />
                </button>
              </div>

              <!-- Confidence -->
              <div class="mb-4">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm text-gray-600">Tingkat Kepercayaan</span>
                  <span class="text-sm font-medium">{{ formatConfidence(item.confidence) }}%</span>
                </div>
                <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    class="h-full transition-all duration-500"
                    :class="getConfidenceBarClass(item.confidence)"
                    :style="{ width: formatConfidence(item.confidence) + '%' }"
                  ></div>
                </div>
              </div>

              <!-- Description -->
              <p class="text-gray-600 mb-4 line-clamp-2">
                {{ item.description || 'Tidak ada deskripsi tersedia.' }}
              </p>

              <!-- Recommendations Preview -->
              <div v-if="item.recommendations && item.recommendations.length > 0" class="mb-4">
                <h4 class="text-sm text-gray-700 mb-2 font-medium">Rekomendasi:</h4>
                <ul class="space-y-1">
                  <li
                    v-for="(rec, idx) in item.recommendations.slice(0, 2)"
                    :key="idx"
                    class="flex items-start gap-2 text-sm text-gray-600"
                  >
                    <CheckCircle2 :size="16" class="text-primary-green shrink-0 mt-0.5" />
                    <span class="line-clamp-1">{{ rec }}</span>
                  </li>
                </ul>
              </div>

              <!-- Actions -->
              <div class="flex gap-3">
                <button
                  @click="viewDetail(item)"
                  class="flex-1 md:flex-none border-2 border-primary-blue text-primary-blue px-6 py-2 rounded-full hover:bg-blue-50 transition-colors font-medium"
                >
                  Lihat Detail
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-8">
          <button
            @click="loadHistory(currentPage - 1)"
            :disabled="currentPage === 1"
            class="p-2 rounded-lg bg-white card-shadow disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
          >
            <ChevronLeft :size="20" />
          </button>

          <div class="flex gap-1">
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="loadHistory(page)"
              :class="[
                'px-4 py-2 rounded-lg transition-colors font-medium',
                currentPage === page
                  ? 'gradient-primary text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100 card-shadow'
              ]"
            >
              {{ page }}
            </button>
          </div>

          <button
            @click="loadHistory(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="p-2 rounded-lg bg-white card-shadow disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
          >
            <ChevronRight :size="20" />
          </button>
        </div>
      </div>

      <!-- Detail Modal -->
      <Teleport to="body">
        <transition name="modal">
          <div
            v-if="selectedItem"
            @click="selectedItem = null"
            class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 md:p-6"
          >
            <div
              @click.stop
              v-motion
              :initial="{ opacity: 0, scale: 0.95 }"
              :enter="{ opacity: 1, scale: 1 }"
              class="bg-white rounded-4xl p-6 md:p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            >
              <!-- Modal Header -->
              <div class="flex items-start justify-between mb-6">
                <div>
                  <h2 class="text-2xl font-bold text-navy-dark">Detail Analisis</h2>
                  <p class="text-sm text-gray-500 mt-1">{{ formatDate(selectedItem.created_at) }}</p>
                </div>
                <button
                  @click="selectedItem = null"
                  class="text-gray-400 hover:text-gray-600 p-2 rounded-full hover:bg-gray-100 transition-colors"
                >
                  <X :size="24" />
                </button>
              </div>

              <div class="space-y-6">
                <!-- Image -->
                <img
                  v-if="selectedItem.image_filename"
                  :src="getImageUrl(selectedItem.image_filename)"
                  :alt="selectedItem.condition"
                  class="w-full rounded-2xl max-h-64 object-cover"
                  @error="handleImageError"
                />

                <!-- Condition & Severity -->
                <div class="flex items-center gap-3 flex-wrap">
                  <h3 class="text-xl font-bold">{{ selectedItem.condition }}</h3>
                  <span 
                    :class="getSeverityClass(selectedItem.severity)"
                    class="px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {{ getSeverityLabel(selectedItem.severity) }}
                  </span>
                </div>

                <!-- Confidence -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm text-gray-600 font-medium">Tingkat Kepercayaan AI</span>
                    <span class="text-sm font-bold">{{ formatConfidence(selectedItem.confidence) }}%</span>
                  </div>
                  <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      class="h-full transition-all duration-500"
                      :class="getConfidenceBarClass(selectedItem.confidence)"
                      :style="{ width: formatConfidence(selectedItem.confidence) + '%' }"
                    ></div>
                  </div>
                </div>

                <!-- Description -->
                <div>
                  <h4 class="font-medium text-navy-dark mb-2">Deskripsi</h4>
                  <p class="text-gray-600 leading-relaxed">{{ selectedItem.description }}</p>
                </div>

                <!-- Recommendations -->
                <div v-if="selectedItem.recommendations && selectedItem.recommendations.length > 0">
                  <h4 class="font-medium text-navy-dark mb-3">Rekomendasi Penanganan</h4>
                  <ul class="space-y-2">
                    <li
                      v-for="(rec, idx) in selectedItem.recommendations"
                      :key="idx"
                      class="flex items-start gap-3 p-3 bg-green-50 rounded-xl"
                    >
                      <CheckCircle2 :size="20" class="text-primary-green shrink-0 mt-0.5" />
                      <span class="text-gray-700">{{ rec }}</span>
                    </li>
                  </ul>
                </div>

                <!-- Top 3 Predictions -->
                <div v-if="selectedItem.top_3_predictions && selectedItem.top_3_predictions.length > 1">
                  <h4 class="font-medium text-navy-dark mb-3">Prediksi Lainnya</h4>
                  <div class="space-y-2">
                    <div 
                      v-for="(pred, idx) in selectedItem.top_3_predictions.slice(1)"
                      :key="idx"
                      class="flex items-center justify-between p-3 bg-gray-50 rounded-xl"
                    >
                      <span class="text-gray-700">{{ pred.label }}</span>
                      <span class="text-sm text-gray-500">{{ pred.confidence }}%</span>
                    </div>
                  </div>
                </div>

                <!-- Warning -->
                <div class="bg-yellow-50 border-l-4 border-warning p-4 rounded-lg">
                  <div class="flex items-start gap-2">
                    <AlertTriangle :size="20" class="text-warning shrink-0 mt-0.5" />
                    <p class="text-sm text-gray-700">
                      <strong>Disclaimer:</strong> Hasil ini bukan diagnosis medis pasti. Untuk diagnosis yang akurat dan pengobatan yang tepat, silakan konsultasi dengan dokter atau dermatolog profesional.
                    </p>
                  </div>
                </div>

                <!-- Modal Actions -->
                <div class="flex gap-3 pt-4">
                  <button
                    @click="selectedItem = null"
                    class="flex-1 bg-gray-100 text-gray-700 px-6 py-3 rounded-full hover:bg-gray-200 transition-colors font-medium"
                  >
                    Tutup
                  </button>
                  <router-link
                    to="/ai-check"
                    class="flex-1 gradient-primary text-white px-6 py-3 rounded-full hover:opacity-90 transition-opacity text-center font-medium"
                  >
                    Analisis Baru
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </Teleport>

      <!-- Delete Confirmation Modal -->
      <Teleport to="body">
        <transition name="modal">
          <div
            v-if="showDeleteConfirm"
            @click="showDeleteConfirm = false"
            class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
          >
            <div
              @click.stop
              class="bg-white rounded-2xl p-6 max-w-sm w-full"
            >
              <div class="text-center mb-6">
                <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Trash2 :size="32" class="text-red-500" />
                </div>
                <h3 class="text-xl font-bold text-navy-dark mb-2">
                  {{ deleteAllMode ? 'Hapus Semua Riwayat?' : 'Hapus Riwayat?' }}
                </h3>
                <p class="text-gray-600">
                  {{ deleteAllMode 
                    ? 'Semua riwayat analisis akan dihapus permanen. Tindakan ini tidak dapat dibatalkan.'
                    : 'Riwayat analisis ini akan dihapus permanen. Tindakan ini tidak dapat dibatalkan.' 
                  }}
                </p>
              </div>
              <div class="flex gap-3">
                <button
                  @click="showDeleteConfirm = false"
                  class="flex-1 bg-gray-100 text-gray-700 px-4 py-3 rounded-full hover:bg-gray-200 transition-colors font-medium"
                >
                  Batal
                </button>
                <button
                  @click="executeDelete"
                  :disabled="isDeleting"
                  class="flex-1 bg-red-500 text-white px-4 py-3 rounded-full hover:bg-red-600 transition-colors font-medium disabled:opacity-50"
                >
                  <Loader2 v-if="isDeleting" :size="20" class="animate-spin mx-auto" />
                  <span v-else>Hapus</span>
                </button>
              </div>
            </div>
          </div>
        </transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  History, Calendar, CheckCircle2, Trash2, Loader2, X, 
  AlertCircle, AlertTriangle, ImageIcon, RefreshCw, Download,
  ChevronLeft, ChevronRight, Activity
} from 'lucide-vue-next'
import { 
  getAnalysisHistory, deleteAnalysisById, getHistoryStats, getImageUrl 
} from '../utils/api'

// =============================================================================
// STATE
// =============================================================================

const histories = ref([])
const stats = ref(null)
const isLoading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const perPage = ref(10)
const totalItems = ref(0)

const selectedItem = ref(null)
const showDeleteConfirm = ref(false)
const deleteTargetId = ref(null)
const deleteAllMode = ref(false)
const isDeleting = ref(false)

// =============================================================================
// COMPUTED
// =============================================================================

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// =============================================================================
// METHODS
// =============================================================================

const loadHistory = async (page = 1) => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await getAnalysisHistory(page, perPage.value)
    histories.value = response.data || []
    currentPage.value = response.page || 1
    totalPages.value = response.pages || 1
    totalItems.value = response.total || 0
    
    // Load stats if first page
    if (page === 1) {
      await loadStats()
    }
  } catch (err) {
    console.error('Failed to load history:', err)
    error.value = err.response?.data?.message || 'Gagal memuat riwayat. Pastikan server backend berjalan.'
  } finally {
    isLoading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await getHistoryStats()
    stats.value = response.data
  } catch (err) {
    console.error('Failed to load stats:', err)
  }
}

const confirmDelete = (id) => {
  deleteTargetId.value = id
  deleteAllMode.value = false
  showDeleteConfirm.value = true
}

const confirmClearAll = () => {
  deleteAllMode.value = true
  showDeleteConfirm.value = true
}

const executeDelete = async () => {
  isDeleting.value = true
  
  try {
    if (deleteAllMode.value) {
      // Delete all items one by one
      for (const item of histories.value) {
        await deleteAnalysisById(item.id)
      }
      histories.value = []
      stats.value = null
    } else {
      await deleteAnalysisById(deleteTargetId.value)
      histories.value = histories.value.filter(h => h.id !== deleteTargetId.value)
      
      // Reload if current page becomes empty
      if (histories.value.length === 0 && currentPage.value > 1) {
        await loadHistory(currentPage.value - 1)
      } else {
        await loadStats()
      }
    }
    
    showDeleteConfirm.value = false
    deleteTargetId.value = null
  } catch (err) {
    console.error('Failed to delete:', err)
    alert('Gagal menghapus riwayat: ' + (err.response?.data?.message || err.message))
  } finally {
    isDeleting.value = false
  }
}

const viewDetail = (item) => {
  selectedItem.value = item
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const formatConfidence = (confidence) => {
  if (confidence === null || confidence === undefined) return 0
  // Handle both 0-1 and 0-100 formats
  const value = confidence > 1 ? confidence : confidence * 100
  return Math.round(value * 10) / 10
}

const getSeverityClass = (severity) => {
  const classes = {
    'high': 'bg-red-100 text-red-700',
    'medium': 'bg-yellow-100 text-yellow-700',
    'low': 'bg-green-100 text-green-700',
    'unknown': 'bg-gray-100 text-gray-700'
  }
  return classes[severity] || classes['unknown']
}

const getSeverityLabel = (severity) => {
  const labels = {
    'high': 'Tinggi',
    'medium': 'Sedang',
    'low': 'Rendah',
    'unknown': 'Belum Diketahui'
  }
  return labels[severity] || labels['unknown']
}

const getConfidenceBarClass = (confidence) => {
  const value = formatConfidence(confidence)
  if (value >= 75) return 'bg-green-500'
  if (value >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

const handleImageError = (event) => {
  event.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect fill="%23f3f4f6" width="100" height="100"/><text fill="%239ca3af" font-size="12" x="50" y="50" text-anchor="middle" dy=".3em">No Image</text></svg>'
}

const exportToCSV = () => {
  if (histories.value.length === 0) return
  
  const headers = ['ID', 'Tanggal', 'Kondisi', 'Confidence (%)', 'Severity', 'Deskripsi', 'Rekomendasi']
  const rows = histories.value.map(item => [
    item.id,
    formatDate(item.created_at),
    item.condition,
    formatConfidence(item.confidence),
    getSeverityLabel(item.severity),
    `"${(item.description || '').replace(/"/g, '""')}"`,
    `"${(item.recommendation || '').replace(/"/g, '""')}"`
  ])
  
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `skincheck-history-${new Date().toISOString().split('T')[0]}.csv`
  link.click()
}

// =============================================================================
// LIFECYCLE
// =============================================================================

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.rounded-4xl {
  border-radius: 2rem;
}
</style>
