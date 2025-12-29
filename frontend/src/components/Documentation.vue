<template>
  <div class="pt-28 pb-20 bg-bg-soft min-h-screen">
    <div class="max-w-5xl mx-auto px-6">
      
      <!-- Card 1 - Header -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0 }"
        class="glassmorphism rounded-4xl p-8 mb-6"
      >
        <div class="flex items-start gap-6">
          <div class="w-20 h-20 gradient-primary rounded-3xl flex items-center justify-center glow-icon shrink-0">
            <ClipboardCheck :size="40" class="text-white" />
          </div>
          <div>
            <h1 class="text-4xl mb-3">Tata Cara Penggunaan</h1>
            <p class="text-lg text-gray-600">
              Panduan lengkap menggunakan SkinCheck AI untuk deteksi kondisi kulit
            </p>
          </div>
        </div>
      </div>

      <!-- Card 2 - Step 1: Upload -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 100 } }"
        class="bg-white rounded-4xl p-8 card-shadow mb-6"
      >
        <div class="flex items-start gap-6">
          <div class="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center glow-icon shrink-0">
            <Upload :size="32" class="text-white" />
          </div>
          <div class="flex-1">
            <div class="text-3xl gradient-text mb-2">01</div>
            <h2 class="text-2xl mb-3">Upload Foto</h2>
            <p class="text-gray-600 mb-4">
              Langkah pertama adalah mengupload foto area kulit yang ingin Anda periksa. Anda dapat mengambil foto langsung menggunakan kamera atau memilih foto yang sudah ada di perangkat Anda.
            </p>
            <p class="text-gray-600">
              Pastikan foto yang diupload memiliki kualitas yang baik dengan pencahayaan yang cukup agar AI dapat menganalisis dengan lebih akurat.
            </p>
          </div>
        </div>
      </div>

      <!-- Card 3 - Step 2: AI Analysis -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 200 } }"
        class="bg-white rounded-4xl p-8 card-shadow mb-6"
      >
        <div class="flex items-start gap-6">
          <div class="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center glow-icon shrink-0">
            <Cpu :size="32" class="text-white" />
          </div>
          <div class="flex-1">
            <div class="text-3xl gradient-text mb-2">02</div>
            <h2 class="text-2xl mb-3">AI Analisis Gambar</h2>
            <p class="text-gray-600 mb-4">
              Setelah foto berhasil diupload, model kecerdasan buatan kami akan secara otomatis memproses dan menganalisis gambar. Proses ini biasanya hanya membutuhkan beberapa detik.
            </p>
            <p class="text-gray-600">
              AI kami telah dilatih menggunakan ribuan dataset gambar kondisi kulit yang dikurasi untuk memberikan prediksi yang akurat. Sistem akan mengidentifikasi pola, tekstur, dan karakteristik visual dari foto yang Anda upload.
            </p>
          </div>
        </div>
      </div>

      <!-- Card 4 - Step 3: View Results -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 300 } }"
        class="bg-white rounded-4xl p-8 card-shadow mb-6"
      >
        <div class="flex items-start gap-6">
          <div class="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center glow-icon shrink-0">
            <ClipboardCheck :size="32" class="text-white" />
          </div>
          <div class="flex-1">
            <div class="text-3xl gradient-text mb-2">03</div>
            <h2 class="text-2xl mb-3">Lihat Hasil</h2>
            <p class="text-gray-600 mb-4">
              Setelah analisis selesai, Anda akan melihat hasil deteksi lengkap yang mencakup nama kondisi kulit yang terdeteksi, tingkat kepercayaan AI, dan informasi edukatif detail.
            </p>
            <p class="text-gray-600">
              Hasil juga dilengkapi dengan ringkasan kondisi, cara penanganan awal, rekomendasi umum, dan informasi kapan Anda harus segera berkonsultasi dengan dokter. Ingat, ini bukan diagnosis medis pasti.
            </p>
          </div>
        </div>
      </div>

      <!-- Card 5 - Photo Tips -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 400 } }"
        class="bg-white rounded-4xl p-8 card-shadow mb-6"
      >
        <h2 class="text-2xl mb-6">Cara Mengambil Foto yang Baik</h2>
        
        <div class="space-y-4">
          <div
            v-for="(tip, index) in photoTips"
            :key="index"
            class="flex items-start gap-3 p-4 bg-green-50 rounded-xl"
          >
            <CheckCircle2 :size="24" class="text-primary-green shrink-0 mt-0.5" />
            <div>
              <h4 class="mb-1">{{ tip.title }}</h4>
              <p class="text-sm text-gray-600">
                {{ tip.description }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Card 6 - Good vs Bad Photos -->
      <div
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 500 } }"
        class="bg-white rounded-4xl p-8 card-shadow mb-6"
      >
        <h2 class="text-2xl mb-6">Foto Benar vs Foto Salah</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Good Photo -->
          <div class="p-6 bg-green-50 rounded-2xl border-2 border-primary-green">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-primary-green rounded-xl flex items-center justify-center glow-icon">
                <CheckCircle2 :size="24" class="text-white" />
              </div>
              <h3 class="text-xl text-navy-dark">Foto Benar ✔</h3>
            </div>
            
            <ul class="space-y-3">
              <li v-for="(item, index) in goodPhotoItems" :key="index" class="flex items-start gap-2">
                <span class="text-primary-green shrink-0">✓</span>
                <span class="text-sm text-gray-700">{{ item }}</span>
              </li>
            </ul>
          </div>

          <!-- Bad Photo -->
          <div class="p-6 bg-red-50 rounded-2xl border-2 border-red-400">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-red-500 rounded-xl flex items-center justify-center">
                <X :size="24" class="text-white" />
              </div>
              <h3 class="text-xl text-navy-dark">Foto Salah ✖</h3>
            </div>
            
            <ul class="space-y-3">
              <li v-for="(item, index) in badPhotoItems" :key="index" class="flex items-start gap-2">
                <span class="text-red-500 shrink-0">✗</span>
                <span class="text-sm text-gray-700">{{ item }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- FAQ and Supported Diseases sections removed to keep documentation concise. -->

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Upload, Cpu, ClipboardCheck, CheckCircle2, X, ChevronDown } from 'lucide-vue-next'

const openFaq = ref(null)

const toggleFaq = (index) => {
  openFaq.value = openFaq.value === index ? null : index
}

const photoTips = [
  {
    title: 'Gunakan Cahaya Terang Alami',
    description: 'Ambil foto di area dengan pencahayaan yang baik, sebaiknya menggunakan cahaya alami dari jendela. Hindari pencahayaan yang terlalu redup atau terlalu terang.'
  },
  {
    title: 'Hindari Bayangan Keras',
    description: 'Pastikan tidak ada bayangan yang jatuh pada area kulit yang difoto. Bayangan dapat mengganggu analisis AI dan mengurangi akurasi hasil.'
  },
  {
    title: 'Jarak Ideal 10-15 cm',
    description: 'Ambil foto dari jarak yang cukup dekat (sekitar 10-15 cm) agar detail kulit terlihat jelas, namun tidak terlalu dekat sehingga gambar menjadi buram.'
  },
  {
    title: 'Fokus Harus Jelas',
    description: 'Pastikan kamera dalam keadaan fokus dan gambar tidak blur. Ketuk layar pada area kulit yang ingin difoto untuk memastikan fokus yang tepat.'
  },
  {
    title: 'Tidak Blur atau Menggunakan Filter',
    description: 'Jangan gunakan filter kamera atau efek editing. Foto harus menampilkan kondisi kulit yang natural dan sebenarnya untuk hasil analisis yang akurat.'
  }
]

const goodPhotoItems = [
  'Pencahayaan terang dan merata',
  'Fokus tajam, tidak blur',
  'Warna natural, tanpa filter',
  'Jarak yang tepat (10-15 cm)',
  'Tidak ada bayangan menutupi area',
  'Detail kulit terlihat jelas'
]

const badPhotoItems = [
  'Terlalu gelap atau terlalu terang',
  'Blur atau tidak fokus',
  'Menggunakan filter kamera',
  'Terlalu dekat atau terlalu jauh',
  'Ada bayangan keras pada area kulit',
  'Detail tidak terlihat jelas'
]

const faqs = [
  {
    question: 'Apakah foto saya disimpan?',
    answer: 'Tidak. Foto yang Anda upload hanya diproses untuk analisis AI dan tidak disimpan permanen di server kami. Setelah analisis selesai, foto akan otomatis terhapus. Kami sangat menjaga privasi dan keamanan data pengguna.'
  },
  {
    question: 'Apakah ini pengganti dokter?',
    answer: 'Tidak sama sekali. SkinCheck AI adalah alat bantu deteksi dini yang memberikan informasi edukatif awal. Hasil analisis AI tidak dapat menggantikan diagnosis medis profesional. Anda tetap harus berkonsultasi dengan dokter atau dermatolog untuk diagnosis yang akurat dan pengobatan yang tepat.'
  },
  {
    question: 'Berapa lama analisis?',
    answer: 'Proses analisis AI sangat cepat. Setelah foto berhasil diupload, model AI kami biasanya membutuhkan waktu 2-5 detik untuk memproses dan menghasilkan hasil deteksi beserta informasi edukatif terkait.'
  },
  {
    question: 'Apakah aman untuk anak-anak?',
    answer: 'Ya, aplikasi ini aman digunakan untuk semua usia termasuk anak-anak. Namun, untuk hasil yang lebih akurat dan tindakan medis yang tepat, kami sangat menyarankan untuk selalu berkonsultasi dengan dokter anak atau dermatolog profesional, terutama jika kondisi kulit anak Anda memerlukan perhatian khusus.'
  }
]

const diseases = [
  {
    name: 'Dermatitis',
    description: 'Peradangan kulit yang menyebabkan kemerahan dan gatal',
    icon: '🔴'
  },
  {
    name: 'Jerawat',
    description: 'Kondisi kulit dengan komedo dan benjolan meradang',
    icon: '🔵'
  },
  {
    name: 'Psoriasis',
    description: 'Kondisi autoimun dengan bercak kulit bersisik',
    icon: '🟣'
  },
  {
    name: 'Infeksi Jamur',
    description: 'Infeksi kulit oleh jamur seperti ringworm',
    icon: '🟡'
  },
  {
    name: 'Eksim',
    description: 'Kulit kering, gatal, dan iritasi kronis',
    icon: '🟠'
  },
  {
    name: 'Hiperpigmentasi',
    description: 'Area kulit yang lebih gelap dari sekitarnya',
    icon: '🟤'
  }
]
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
