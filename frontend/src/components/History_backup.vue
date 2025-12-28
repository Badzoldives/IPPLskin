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

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center py-20">
        <Loader2 :size="48" class="text-primary-blue animate-spin" />
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
          class="bg-white rounded-4xl p-6 card-shadow"
        >
          <div class="flex flex-col md:flex-row gap-6">
            <!-- Image -->
            <div class="md:w-48 md:h-48 shrink-0">
              <img
                :src="`/api/uploads/${item.image_path}`"
                :alt="item.condition"
                class="w-full h-48 object-cover rounded-2xl"
              />
            </div>

            <!-- Content -->
            <div class="flex-1">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="text-2xl text-navy-dark mb-2">{{ item.condition }}</h3>
                  <p class="text-sm text-gray-500">
                    <Calendar :size="16" class="inline mr-1" />
                    {{ formatDate(item.created_at) }}
                  </p>
                </div>
                <button
                  @click="deleteAnalysis(item.id)"
                  class="text-red-500 hover:text-red-700 transition-colors"
                  title="Hapus"
                >
                  <Trash2 :size="20" />
                </button>
              </div>

              <!-- Confidence -->
              <div class="mb-4">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm text-gray-600">Tingkat Kepercayaan</span>
                  <span class="text-sm">{{ item.confidence }}%</span>
                </div>
                <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    class="h-full gradient-primary transition-all duration-500"
                    :style="{ width: item.confidence + '%' }"
                  ></div>
                </div>
              </div>

              <!-- Description -->
              <p class="text-gray-600 mb-4 line-clamp-2">
                {{ item.description }}
              </p>

              <!-- Recommendations -->
              <div class="mb-4">
                <h4 class="text-sm text-gray-700 mb-2">Rekomendasi:</h4>
                <ul class="space-y-1">
                  <li
                    v-for="(rec, idx) in item.recommendations.slice(0, 2)"
                    :key="idx"
                    class="flex items-start gap-2 text-sm text-gray-600"
                  >
                    <CheckCircle2 :size="16" class="text-primary-green shrink-0 mt-0.5" />
                    <span>{{ rec }}</span>
                  </li>
                </ul>
              </div>

              <!-- Actions -->
              <div class="flex gap-3">
                <button
                  @click="viewDetail(item)"
                  class="flex-1 md:flex-none border-2 border-primary-blue text-primary-blue px-6 py-2 rounded-full hover:bg-blue-50 transition-colors"
                >
                  Lihat Detail
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-8">
          <button
            v-for="page in totalPages"
            :key="page"
            @click="loadHistory(page)"
            :class="[
              'px-4 py-2 rounded-lg transition-colors',
              currentPage === page
                ? 'gradient-primary text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            ]"
          >
            {{ page }}
          </button>
        </div>
      </div>

      <!-- Detail Modal -->
      <transition name="modal">
        <div
          v-if="selectedItem"
          @click="selectedItem = null"
          class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-6"
        >
          <div
            @click.stop
            class="bg-white rounded-4xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          >
            <div class="flex items-start justify-between mb-6">
              <h2 class="text-2xl">Detail Analisis</h2>
              <button
                @click="selectedItem = null"
                class="text-gray-500 hover:text-gray-700"
              >
                <X :size="24" />
              </button>
            </div>

            <div class="space-y-6">
              <!-- Image -->
              <img
                :src="`/api/uploads/${selectedItem.image_path}`"
                :alt="selectedItem.condition"
                class="w-full rounded-2xl"
              />

              <!-- Condition -->
              <div>
                <h3 class="text-xl mb-2">{{ selectedItem.condition }}</h3>
                <p class="text-sm text-gray-500">{{ formatDate(selectedItem.created_at) }}</p>
              </div>

              <!-- Confidence -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm text-gray-600">Tingkat Kepercayaan</span>
                  <span class="text-sm">{{ selectedItem.confidence }}%</span>
                </div>
                <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    class="h-full gradient-primary"
                    :style="{ width: selectedItem.confidence + '%' }"
                  ></div>
                </div>
              </div>

              <!-- Description -->
              <div>
                <h4 class="mb-2">Deskripsi</h4>
                <p class="text-gray-600">{{ selectedItem.description }}</p>
              </div>

              <!-- Recommendations -->
              <div>
                <h4 class="mb-3">Rekomendasi Penanganan</h4>
                <ul class="space-y-2">
                  <li
                    v-for="(rec, idx) in selectedItem.recommendations"
                    :key="idx"
                    class="flex items-start gap-2"
                  >
                    <CheckCircle2 :size="20" class="text-primary-green shrink-0 mt-0.5" />
                    <span class="text-gray-600">{{ rec }}</span>
                  </li>
                </ul>
              </div>

              <!-- Warning -->
              <div class="bg-yellow-50 border-l-4 border-warning p-4 rounded-lg">
                <p class="text-sm text-gray-dark">
                  ⚠️ <strong>Disclaimer:</strong> Hasil ini bukan diagnosis medis pasti. Untuk diagnosis yang akurat dan pengobatan yang tepat, silakan konsultasi dengan dokter atau dermatolog profesional.
                </p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { History, Calendar, CheckCircle2, Trash2, Loader2, X } from 'lucide-vue-next'
import { getAnalysisHistory, deleteAnalysisById } from '../utils/api'

const histories = ref([])
const isLoading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const selectedItem = ref(null)

const loadHistory = async (page = 1) => {
  isLoading.value = true
  try {
    const response = await getAnalysisHistory(page, 10)
    histories.value = response.data
    currentPage.value = response.page
    totalPages.value = response.pages
  } catch (error) {
    console.error('Failed to load history:', error)
  } finally {
    isLoading.value = false
  }
}

const deleteAnalysis = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus analisis ini?')) return

  try {
    await deleteAnalysisById(id)
    histories.value = histories.value.filter(h => h.id !== id)
  } catch (error) {
    console.error('Failed to delete:', error)
    alert('Gagal menghapus analisis')
  }
}

const viewDetail = (item) => {
  selectedItem.value = item
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
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
</style>
