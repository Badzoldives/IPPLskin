<template>
	<div class="min-h-[calc(100vh-72px)] pb-12">
		<div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">

			<!-- Progress steps -->
			<div class="py-6">
				<div class="flex items-center gap-4 text-sm text-gray-600">
					<div class="flex items-center gap-3">
						<div :class="['w-8 h-8 rounded-full flex items-center justify-center text-white', step===1 ? 'bg-primary-blue' : 'bg-gray-200 text-gray-700']">1</div>
						<div class="hidden sm:block">Upload</div>
					</div>
					<div class="flex-1 h-px bg-gray-200"></div>
					<div class="flex items-center gap-3">
						<div :class="['w-8 h-8 rounded-full flex items-center justify-center text-white', step===2 ? 'bg-primary-blue' : 'bg-gray-200 text-gray-700']">2</div>
						<div class="hidden sm:block">Analisis</div>
					</div>
					<div class="flex-1 h-px bg-gray-200"></div>
					<div class="flex items-center gap-3">
						<div :class="['w-8 h-8 rounded-full flex items-center justify-center text-white', step===3 ? 'bg-primary-blue' : 'bg-gray-200 text-gray-700']">3</div>
						<div class="hidden sm:block">Hasil</div>
					</div>
				</div>
			</div>

			<!-- Title -->
			<div class="mb-6">
				<h1 class="text-2xl sm:text-3xl font-semibold">Cek Kondisi Kulit dengan Foto</h1>
				<p class="text-sm text-gray-600 mt-2">Ambil foto yang jelas, lalu klik Mulai Analisis.</p>
			</div>

			<!-- Main grid -->
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">

				<!-- Left: Upload & Preview -->
				<section class="bg-white rounded-2xl shadow-sm p-6 border border-gray-100">
					<div class="flex flex-col gap-4">
						<div
							class="w-full border-2 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-center text-gray-600 hover:border-primary-blue transition-colors"
							:class="previewUrl ? 'border-transparent p-0' : ''"
						>
							<input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
							<input ref="cameraInput" type="file" accept="image/*" capture="environment" class="hidden" @change="onFileChange" />

							<div v-if="!previewUrl" class="py-10 px-4 w-full">
								<div class="mx-auto w-24 h-24 rounded-full bg-blue-50 flex items-center justify-center text-3xl">📷</div>
								<h2 class="mt-4 font-semibold text-lg">Unggah atau ambil foto</h2>
								<p class="mt-2 text-sm text-gray-500">JPG/PNG • Maks 10MB</p>
								<div class="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
									<button @click="triggerCamera" class="h-12 px-5 rounded-lg border border-primary-blue text-primary-blue bg-white hover:bg-blue-50">Ambil Foto</button>
									<button @click="triggerFile" class="h-12 px-5 rounded-lg bg-primary-blue text-white">Upload Foto</button>
								</div>
								<p class="mt-3 text-xs text-gray-400">Foto tidak disimpan permanen</p>
							</div>

							<div v-else class="w-full">
								<div class="relative">
									<div class="aspect-[4/3] w-full overflow-hidden rounded-xl bg-gray-50">
										<img :src="previewUrl" alt="preview" class="w-full h-full object-cover" />
									</div>
									<div class="absolute top-4 left-4 bg-white/80 text-sm px-3 py-1 rounded-full border border-gray-100">Siap dianalisis</div>
								</div>

								<div class="mt-4 flex flex-wrap gap-3">
									<button @click="triggerFile" class="h-12 px-4 rounded-lg border border-gray-200 text-gray-700">Ganti Foto</button>
									<button @click="removeFile" class="h-12 px-4 rounded-lg bg-white text-red-600 border border-red-100">Hapus</button>
								</div>
							</div>
						</div>

						<!-- CTA area -->
						<div class="mt-3">
							<button :disabled="!file || loading" @click="analyzeImage" class="w-full h-14 rounded-xl text-white bg-primary-blue disabled:opacity-60 disabled:cursor-not-allowed"> 
								<span v-if="loading" class="inline-flex items-center gap-3">
									<span class="spinner w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
									Menganalisis...
								</span>
								<span v-else>Mulai Analisis</span>
							</button>
						</div>

						<p v-if="errorMsg" class="text-sm text-red-600 mt-2">{{ errorMsg }}</p>
					</div>
				</section>

				<!-- Right: Tips and Privacy -->
				<aside class="space-y-4">
					<div class="bg-white rounded-2xl shadow-sm p-5 border border-gray-100">
						<h3 class="font-semibold">Tips Foto yang Baik</h3>
						<ul class="mt-3 text-sm text-gray-600 space-y-2">
							<li>1. Pastikan area fokus terang dan jelas.</li>
							<li>2. Hindari bayangan dan blur.</li>
							<li>3. Ambil dari jarak 20-40 cm (atau gunakan zoom).</li>
						</ul>
					</div>

					<div class="bg-white rounded-2xl shadow-sm p-4 border border-gray-100 text-sm text-gray-600">
						<h4 class="font-medium">Privasi & Format</h4>
						<p class="mt-2">Foto tidak disimpan permanen. JPG/PNG • Maks 10MB</p>
					</div>

					<div class="bg-white rounded-2xl shadow-sm p-4 border border-gray-100 text-sm text-gray-600">
						<h4 class="font-medium">Kapan hasil tersedia?</h4>
						<p class="mt-2">Analisis biasanya selesai dalam beberapa detik — tergantung ukuran file dan koneksi.</p>
					</div>
				</aside>

			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const file = ref(null)
const previewUrl = ref('')
const loading = ref(false)
const errorMsg = ref('')
const step = ref(1)

const fileInput = ref(null)
const cameraInput = ref(null)

function triggerFile() {
	errorMsg.value = ''
	fileInput.value && fileInput.value.click()
}

function triggerCamera() {
	errorMsg.value = ''
	cameraInput.value && cameraInput.value.click()
}

function onFileChange(e) {
	const f = e.target.files && e.target.files[0]
	if (!f) return

	// validate
	const maxMB = 10
	if (f.size > maxMB * 1024 * 1024) {
		errorMsg.value = 'File terlalu besar (maks 10MB)'
		e.target.value = ''
		return
	}

	const allowed = ['image/jpeg', 'image/png', 'image/jpg']
	if (!allowed.includes(f.type)) {
		errorMsg.value = 'Format tidak didukung. Gunakan JPG atau PNG.'
		e.target.value = ''
		return
	}

	errorMsg.value = ''
	file.value = f
	if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
	previewUrl.value = URL.createObjectURL(f)
	step.value = 1
}

function removeFile() {
	if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
	previewUrl.value = ''
	file.value = null
	errorMsg.value = ''
}

async function analyzeImage() {
	if (!file.value) return
	loading.value = true
	step.value = 2
	errorMsg.value = ''

	try {
		const fd = new FormData()
		fd.append('file', file.value)

		const resp = await fetch('/predict', { method: 'POST', body: fd })
		if (!resp.ok) {
			const text = await resp.text()
			throw new Error(text || 'Gagal menghubungi server')
		}

		const data = await resp.json()
		// handle data as needed; for now advance to result state
		step.value = 3
		// TODO: navigate to result page or display result inline
	} catch (err) {
		errorMsg.value = err?.message || 'Terjadi kesalahan saat analisis.'
	} finally {
		loading.value = false
	}
}

onUnmounted(() => {
	if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
})
</script>

<style scoped>
.spinner { border-top-color: rgba(255,255,255,0.3); }

/* Ensure no accidental horizontal overflow */
:root { box-sizing: border-box; }
*, *::before, *::after { box-sizing: inherit; }

/* Mobile-friendly button sizing enforcement for the view */
button.h-12 { height: 48px; }
button.h-14 { height: 52px; }

</style>
