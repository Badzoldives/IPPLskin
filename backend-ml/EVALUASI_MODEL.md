# Evaluasi Model & Kesiapan Produksi

## ⚠️ DISCLAIMER PENTING

**Model ini BELUM divalidasi secara klinis dan TIDAK BOLEH digunakan sebagai pengganti diagnosis medis profesional.**

## 🔍 Perbaikan yang Telah Dilakukan

### 1. **Skin Detection Preprocessing** ✅
- Tambah validasi warna HSV untuk deteksi kulit manusia
- Reject gambar bukan-kulit (makanan, objek, dll) dengan error message jelas
- Analisis persentase area kulit dalam gambar
- Threshold: minimal 15% pixel harus warna kulit

### 2. **Multi-Level Confidence Validation** ✅
- **< 35%**: REJECT - "Hasil tidak dapat dipercaya"
- **35-50%**: WARNING - "Tingkat kepercayaan rendah"
- **50-75%**: MEDIUM - "Hasil cukup baik"
- **> 75%**: GOOD - "Hasil baik"

### 3. **Error Handling** ✅
```json
{
  "status": "error",
  "message": "Gambar yang diupload bukan foto kulit",
  "reason": "Warna tidak konsisten dengan kulit",
  "suggestion": "Silakan upload foto kulit yang jelas..."
}
```

## 📊 Cara Evaluasi Akurasi Model

### Metode 1: Test Manual (Cepat)
1. Jalankan backend: `python app.py`
2. Buka frontend: `http://localhost:5173`
3. Upload berbagai gambar:
   - ✅ Foto penyakit kulit (sesuai 31 kelas)
   - ❌ Foto bukan kulit (makanan, landscape, dll)
   - ❌ Foto blur/gelap
4. Catat:
   - Berapa banyak yang benar?
   - Berapa yang salah?
   - Berapa yang di-reject?

### Metode 2: Evaluasi Dataset (Kuantitatif)
```bash
# Install dependencies
pip install scikit-learn pandas tqdm

# Struktur folder:
# test_dataset/
#   ├── Melanoma/
#   │   ├── img1.jpg
#   │   ├── img2.jpg
#   ├── Psoriasis/
#   │   ├── img1.jpg
#   └── ...

# Jalankan evaluasi
python evaluate_model.py --dataset ./test_dataset --output report.txt

# ATAU dari CSV
python evaluate_model.py --csv labels.csv --images ./images --output report.txt
```

**Output:**
- Accuracy global
- Precision, Recall, F1 per kelas
- Confusion matrix
- Distribusi confidence

## 🎯 Target Akurasi untuk Produksi

| Metrik | Minimum | Recommended | Ideal |
|--------|---------|-------------|-------|
| **Overall Accuracy** | 70% | 85% | 90%+ |
| **Per-Class F1** | 60% | 75% | 85%+ |
| **High Confidence (>75%)** | 50% | 70% | 80%+ |
| **Rejection Rate** | <30% | <20% | <10% |

## 🚨 Masalah & Keterbatasan Model Saat Ini

### 1. **Dataset Imbalance**
- Model `dinov2-base-finetuned-SkinDisease` dilatih pada dataset publik
- Beberapa kelas punya data lebih banyak (bias)
- Kelas langka: akurasi bisa sangat rendah

### 2. **Variasi Visual**
- Penyakit kulit bisa terlihat mirip secara visual
- Contoh: Eczema vs Dermatitis vs Psoriasis
- Model bisa keliru antara kelas mirip

### 3. **Konteks Klinis**
- Model hanya lihat gambar, tidak tahu:
  - Riwayat pasien
  - Gejala lain (gatal, nyeri, demam)
  - Durasi kondisi
  - Lokasi pada tubuh
- **Diagnosis medis BUTUH konteks lengkap**

### 4. **Kualitas Gambar**
- Pencahayaan buruk → confidence rendah
- Blur/tidak fokus → hasil tidak akurat
- Jarak terlalu jauh/dekat → deteksi gagal

## ✅ Rekomendasi untuk Produksi

### HARUS DILAKUKAN:
1. **Disclaimer Jelas** ✅ (Sudah ada di UI)
   - "Ini BUKAN diagnosis medis"
   - "Konsultasi dokter untuk diagnosis pasti"
   - Legal disclaimer di Terms of Service

2. **Evaluasi Dataset Nyata** ❗ BELUM
   - Kumpulkan min. 50-100 gambar per kelas
   - Label oleh dokter kulit (gold standard)
   - Test akurasi: target min. 85%

3. **Clinical Validation** ❗ BELUM
   - Validasi dengan dokter kulit
   - Inter-rater reliability
   - Sensitivity & Specificity untuk kondisi serius (Melanoma, Carcinoma)

4. **Monitoring & Logging** ⚠️ Partial
   - Track semua prediksi
   - User feedback: "Apakah hasil ini membantu?"
   - False positive/negative rate

5. **Batasan Penggunaan**
   ```
   ✅ Boleh: Skrining awal, edukasi
   ❌ Jangan: Diagnosis final, resep obat, pengganti dokter
   ```

### NICE TO HAVE:
- Ensemble multiple models
- Tambah model untuk skin vs non-skin (classifier terpisah)
- Active learning: user feedback → improve model
- Lokalisasi (GradCAM) untuk explain prediction

## 📋 Checklist Kesiapan Produksi

### Technical:
- [x] Model loaded & working
- [x] Skin detection preprocessing
- [x] Confidence thresholds
- [x] Error handling
- [x] API documentation
- [ ] Load testing (concurrent users)
- [ ] Model versioning
- [ ] Rollback mechanism

### Medical/Legal:
- [x] Disclaimer di UI
- [ ] Terms of Service
- [ ] Privacy Policy (GDPR/data handling)
- [ ] Clinical validation study
- [ ] Medical advisor review
- [ ] Liability insurance (jika komersial)

### Quality:
- [ ] Akurasi > 85% pada test set
- [ ] Per-class F1 > 75%
- [ ] False negative rate untuk kanker < 5%
- [ ] User acceptance testing
- [ ] Accessibility (WCAG)

## 💡 Kesimpulan & Saran

### Status Saat Ini: **⚠️ PROTOTYPE - NOT PRODUCTION READY**

**Alasan:**
1. ❌ Belum ada evaluasi kuantitatif dengan dataset berlabel
2. ❌ Belum validasi klinis dengan dokter
3. ❌ Tidak tahu akurasi sebenarnya (precision/recall per kelas)
4. ⚠️ Model publik (tidak di-train khusus untuk use case Anda)

**Langkah Selanjutnya:**
1. **Kumpulkan test dataset** (50-100 gambar per kelas, berlabel benar)
2. **Jalankan `evaluate_model.py`** untuk ukur akurasi
3. **Jika akurasi < 85%**:
   - Cari model lebih baik, ATAU
   - Fine-tune dengan data lokal, ATAU
   - Gunakan ensemble models
4. **Validasi dengan dokter kulit** (min. 2-3 orang)
5. **User testing** dengan target audience (pasien)
6. **Legal review** untuk disclaimer & T&C

**Untuk Publikasi Bertanggung Jawab:**
```
⚠️ APLIKASI INI HANYA UNTUK SKRINING AWAL
⚠️ BUKAN PENGGANTI KONSULTASI DOKTER
⚠️ JIKA RAGU, SEGERA KE DOKTER KULIT
```

**Timeline Estimasi:**
- Evaluasi kuantitatif: 1-2 minggu
- Clinical validation: 1-3 bulan
- Production-ready: 3-6 bulan

---

**Kontak untuk evaluasi klinis:**
- Cari dermatologist di universitas/rumah sakit
- Proposal: "Research collaboration untuk validasi AI tool"
- Offer: Co-authorship jika publish paper
