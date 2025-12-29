<template>
  <div>
    <!-- Hero Section Only (plain white background) -->
    <section class="relative overflow-hidden bg-white py-16">

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
          <div>
            <div class="inline-block bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm mb-6 border border-white/30">
              AI-Powered Skin Health
            </div>
            <h1 class="text-5xl mb-6 font-semibold text-white">
              AI-Skin Disease Detect
            </h1>
            <p class="text-lg text-white/95 mb-8">
              Dengan teknologi AI yang dilatih dari ribuan data medis, SkinGuard AI mampu mendeteksi gejala awal berbagai kondisi kulit secara instan. Solusi modern untuk pengecekan kulit mandiri.
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

          <!-- Right - Illustration -->
          <div class="relative">
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
            <!-- decorative backdrop removed to keep page background plain white -->
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
