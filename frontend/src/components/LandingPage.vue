<template>
  <div class="pt-20">
    <!-- Hero Section Only -->
    <section class="relative overflow-hidden bg-gradient-to-br from-teal-50/30 via-blue-50/20 to-green-50/30 py-16">
      <!-- Medical Background Pattern -->
      <div class="absolute inset-0 opacity-20">
        <svg class="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="medical-pattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
              <!-- Medical Cross -->
              <path d="M40 30 h20 v10 h10 v20 h-10 v10 h-20 v-10 h-10 v-20 h10 z" fill="#5aaccf" opacity="0.3"/>
              <!-- Heartbeat -->
              <path d="M10 80 L20 80 L25 70 L30 90 L35 75 L40 80 L50 80" stroke="#34D399" fill="none" stroke-width="2" opacity="0.4"/>
              <!-- DNA Helix -->
              <ellipse cx="85" cy="15" rx="3" ry="8" fill="#0d9488" opacity="0.3"/>
              <ellipse cx="85" cy="35" rx="3" ry="8" fill="#0d9488" opacity="0.3"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#medical-pattern)" />
        </svg>
      </div>
      <!-- Floating Medical Icons -->
      <div class="absolute top-20 left-10 text-teal-500 opacity-20 animate-pulse">
        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
      </div>
      <div class="absolute bottom-20 right-20 text-blue-400 opacity-20 animate-pulse" style="animation-delay: 1s;">
        <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 6v6l4 2"/>
        </svg>
      </div>
      <div class="absolute top-40 right-32 text-green-500 opacity-20 animate-pulse" style="animation-delay: 2s;">
        <svg width="45" height="45" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </div>
      <div class="max-w-7xl mx-auto px-6 font-display relative z-10">
        <!-- CARD HERO -->
        <div
          class="rounded-[40px] bg-linear-to-br from-[#5aaccf] via-[#cededb] to-[#34D399]
                 p-10 md:p-14 lg:p-16 shadow-[0_20px_60px_rgba(0,0,0,0.08)]
                 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center
                 hover:shadow-[0_25px_70px_rgba(0,0,0,0.12)] hover:scale-[1.02]
                 transition-all duration-500 ease-out cursor-default"
        >
          <!-- Left - Text -->
          <div
            v-motion
            :initial="{ opacity: 0, x: -50 }"
            :enter="{ opacity: 1, x: 0, transition: { duration: 600 } }"
          >
            <div class="inline-block bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm mb-6 border border-white/30">
              AI-Powered Skin Health
            </div>
            <h1 class="text-5xl mb-6 font-semibold text-white hover:scale-105 hover:-translate-y-1 transition-all duration-300 ease-out cursor-default">
              AI-Skin Disease Detect
            </h1>
            <p class="text-lg text-white/95 mb-8 hover:opacity-90 hover:translate-y-0.5 transition-all duration-300 ease-out">
              Dengan teknologi AI yang dilatih dari ribuan data medis, SkinCheck AI mampu mendeteksi gejala awal berbagai kondisi kulit secara instan. Solusi modern untuk pengecekan kulit mandiri.
            </p>
            <div class="flex gap-4 mb-8">
              <router-link 
                to="/ai-check"
                class="bg-white text-teal-600 px-8 py-3 rounded-full hover:bg-teal-50 hover:scale-105 transition-all duration-300 font-semibold shadow-lg"
              >
                Mulai Deteksi Sekarang
              </router-link>
            </div>
            <div class="flex flex-col gap-3">
              <div class="flex items-center gap-2 text-sm text-white/90">
                <CheckCircle2 :size="20" class="text-white" />
                <span>Model AI dilatih dari dataset terkurasi</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-white/90">
                <Lock :size="20" class="text-white" />
                <span>Privasi terjaga — foto tidak disimpan permanen</span>
              </div>
            </div>
          </div>
          <!-- Right - Illustration (Doctor PNG) -->
          <div
            v-motion
            :initial="{ opacity: 0, x: 50 }"
            :enter="{ opacity: 10, x: 0, transition: { duration: 600, delay: 200 } }"
            class="relative"
          >
            <div class="relative max-w-md mx-auto">
              <div
                class="rounded-3xl bg-linear-to-br from-[#DCFCE7] via-[#D1FAE5] to-[#E0F2FE]
                      w-full aspect-4/3 flex items-center justify-center overflow-hidden"
              >
                <img
                  src="@/assets/doctor-hero.png"
                  alt="Dokter konsultasi online SkinGuard AI"
                  class="w-72 md:w-80 lg:w-96 object-contain drop-shadow-xl"
                />
              </div>
            </div>
            <!-- optional glow -->
            <div class="absolute -inset-4 -z-10 rounded-4xl bg-green-500/5 blur-2xl"></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Camera, Shield, Cpu, Upload, Scan, FileCheck, ChevronDown, Lock, CheckCircle2 } from 'lucide-vue-next'

const openFaq = ref(null)

const toggleFaq = (index) => {
  openFaq.value = openFaq.value === index ? null : index
}

const features = [
  {
    icon: Camera,
    title: 'Cek Cepat',
    description: 'Dapatkan hasil analisis dalam hitungan detik hanya dengan satu foto. Praktis dan efisien.'
  },
  {
    icon: Cpu,
    title: 'Berbasis AI',
    description: 'Menggunakan model kecerdasan buatan yang dilatih dengan dataset medis terkurasi.'
  },
  {
    icon: Shield,
    title: 'Privasi Terjaga',
    description: 'Foto Anda tidak disimpan permanen. Kami menjaga keamanan dan privasi data Anda.'
  }
]

const steps = [
  {
    number: '01',
    icon: Upload,
    title: 'Upload Foto Kulit',
    description: 'Ambil atau upload foto area kulit yang ingin Anda periksa dengan pencahayaan yang baik.'
  },
  {
    number: '02',
    icon: Scan,
    title: 'AI Menganalisis Gambar',
    description: 'Model AI kami akan memproses dan menganalisis gambar untuk mendeteksi kondisi kulit.'
  },
  {
    number: '03',
    icon: FileCheck,
    title: 'Lihat Hasil & Edukasi',
    description: 'Dapatkan hasil deteksi beserta informasi edukatif dan saran penanganan awal.'
  }
]

const faqs = [
  {
    question: 'Apakah ini menggantikan dokter?',
    answer: 'Tidak. SkinGuard AI adalah alat bantu deteksi dini yang memberikan informasi awal. Untuk diagnosis pasti dan pengobatan, Anda tetap harus berkonsultasi dengan dokter atau dermatolog profesional.'
  },
  {
    question: 'Apakah foto saya disimpan?',
    answer: 'Tidak permanen. Foto yang Anda upload hanya diproses untuk analisis dan tidak disimpan dalam database kami setelah sesi selesai. Privasi Anda adalah prioritas kami.'
  },
  {
    question: 'Berapa lama analisis?',
    answer: 'Proses analisis AI kami sangat cepat, biasanya hanya membutuhkan 2-5 detik setelah foto berhasil diupload untuk menghasilkan hasil deteksi.'
  },
  {
    question: 'Apakah aman digunakan anak-anak?',
    answer: 'Ya, aplikasi ini aman digunakan untuk semua usia termasuk anak-anak. Namun untuk hasil yang lebih akurat dan tindakan medis, selalu konsultasikan dengan dokter anak atau dermatolog.'
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
