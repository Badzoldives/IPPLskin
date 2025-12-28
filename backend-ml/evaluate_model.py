"""
Script untuk evaluasi akurasi model deteksi penyakit kulit

Cara pakai:
1. Siapkan dataset berlabel (folder dengan struktur: dataset/class_name/image.jpg)
   ATAU CSV dengan kolom: filename, label
2. Jalankan: python evaluate_model.py --dataset ./test_dataset
   ATAU: python evaluate_model.py --csv labels.csv --images ./images

Output:
- Confusion matrix
- Accuracy, Precision, Recall, F1-Score per class
- Report lengkap
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import json

# Import fungsi inference
from src.inference import predict_skin_disease
from src.config import CLASS_NAMES

def evaluate_from_folder(dataset_path):
    """
    Evaluasi dari folder dengan struktur: dataset/class_name/image.jpg
    """
    dataset_path = Path(dataset_path)
    results = []
    
    print(f"📂 Scanning dataset: {dataset_path}")
    
    # Cari semua gambar
    image_extensions = ['.jpg', '.jpeg', '.png']
    for class_folder in dataset_path.iterdir():
        if not class_folder.is_dir():
            continue
        
        true_label = class_folder.name
        if true_label not in CLASS_NAMES:
            print(f"⚠️  Warning: '{true_label}' tidak ada di CLASS_NAMES, skip folder")
            continue
        
        images = [f for f in class_folder.iterdir() 
                  if f.suffix.lower() in image_extensions]
        
        print(f"\n📊 Processing class: {true_label} ({len(images)} images)")
        
        for img_path in tqdm(images, desc=f"  {true_label}"):
            result = predict_skin_disease(str(img_path))
            
            results.append({
                'filename': img_path.name,
                'true_label': true_label,
                'predicted_label': result.get('prediction'),
                'confidence': result.get('confidence', 0),
                'error': result.get('error', None),
                'top_3': result.get('top_3', [])
            })
    
    return pd.DataFrame(results)


def evaluate_from_csv(csv_path, images_folder):
    """
    Evaluasi dari CSV dengan kolom: filename, label
    """
    df = pd.read_csv(csv_path)
    images_folder = Path(images_folder)
    results = []
    
    print(f"📂 Loading labels from: {csv_path}")
    print(f"📂 Images folder: {images_folder}")
    print(f"📊 Total samples: {len(df)}")
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
        img_path = images_folder / row['filename']
        
        if not img_path.exists():
            print(f"⚠️  File not found: {img_path}")
            continue
        
        result = predict_skin_disease(str(img_path))
        
        results.append({
            'filename': row['filename'],
            'true_label': row['label'],
            'predicted_label': result.get('prediction'),
            'confidence': result.get('confidence', 0),
            'error': result.get('error', None),
            'top_3': result.get('top_3', [])
        })
    
    return pd.DataFrame(results)


def calculate_metrics(df):
    """
    Hitung metrik evaluasi
    """
    try:
        from sklearn.metrics import (
            accuracy_score, precision_recall_fscore_support,
            confusion_matrix, classification_report
        )
    except ImportError:
        print("❌ scikit-learn tidak terinstall. Install dengan: pip install scikit-learn")
        return None
    
    # Filter hasil yang valid (tidak error)
    df_valid = df[df['predicted_label'].notna()].copy()
    
    print(f"\n📊 Statistik Dataset:")
    print(f"   Total samples: {len(df)}")
    print(f"   Valid predictions: {len(df_valid)}")
    print(f"   Errors (not_skin/low_confidence): {len(df) - len(df_valid)}")
    
    if len(df_valid) == 0:
        print("❌ Tidak ada prediksi valid!")
        return None
    
    # Errors breakdown
    errors = df[df['predicted_label'].isna()]
    if len(errors) > 0:
        print(f"\n⚠️  Error breakdown:")
        error_counts = errors['error'].value_counts()
        for error_type, count in error_counts.items():
            print(f"   - {error_type}: {count} samples ({count/len(df)*100:.1f}%)")
    
    y_true = df_valid['true_label']
    y_pred = df_valid['predicted_label']
    
    # Accuracy
    accuracy = accuracy_score(y_true, y_pred)
    
    # Per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, labels=CLASS_NAMES, zero_division=0
    )
    
    # Macro averages
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0
    )
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_NAMES)
    
    # Classification report
    report = classification_report(y_true, y_pred, zero_division=0)
    
    return {
        'accuracy': accuracy,
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'macro_f1': macro_f1,
        'per_class_precision': precision,
        'per_class_recall': recall,
        'per_class_f1': f1,
        'per_class_support': support,
        'confusion_matrix': cm,
        'classification_report': report,
        'df_valid': df_valid
    }


def print_report(metrics, output_file=None):
    """
    Print dan simpan laporan evaluasi
    """
    if metrics is None:
        return
    
    report = f"""
{'='*80}
                    LAPORAN EVALUASI MODEL
{'='*80}

📊 METRIK GLOBAL:
   - Accuracy (Overall):     {metrics['accuracy']*100:.2f}%
   - Precision (Macro avg):  {metrics['macro_precision']*100:.2f}%
   - Recall (Macro avg):     {metrics['macro_recall']*100:.2f}%
   - F1-Score (Macro avg):   {metrics['macro_f1']*100:.2f}%

📈 METRIK PER KELAS:
"""
    
    # Per-class table
    print(report)
    print(f"{'Class':<40} {'Precision':>10} {'Recall':>10} {'F1':>10} {'Support':>10}")
    print('-' * 80)
    
    for i, class_name in enumerate(CLASS_NAMES):
        if metrics['per_class_support'][i] > 0:
            print(f"{class_name:<40} {metrics['per_class_precision'][i]*100:>9.1f}% "
                  f"{metrics['per_class_recall'][i]*100:>9.1f}% "
                  f"{metrics['per_class_f1'][i]*100:>9.1f}% "
                  f"{int(metrics['per_class_support'][i]):>10}")
    
    print('\n' + '='*80)
    print("\n📋 CLASSIFICATION REPORT:")
    print(metrics['classification_report'])
    
    # Confidence statistics
    df_valid = metrics['df_valid']
    print(f"\n📊 STATISTIK CONFIDENCE:")
    print(f"   Mean confidence: {df_valid['confidence'].mean()*100:.2f}%")
    print(f"   Median confidence: {df_valid['confidence'].median()*100:.2f}%")
    print(f"   Min confidence: {df_valid['confidence'].min()*100:.2f}%")
    print(f"   Max confidence: {df_valid['confidence'].max()*100:.2f}%")
    
    # Confidence distribution
    print(f"\n📊 DISTRIBUSI CONFIDENCE:")
    print(f"   > 75% (Good):    {len(df_valid[df_valid['confidence'] > 0.75])} samples ({len(df_valid[df_valid['confidence'] > 0.75])/len(df_valid)*100:.1f}%)")
    print(f"   50-75% (Medium): {len(df_valid[(df_valid['confidence'] > 0.50) & (df_valid['confidence'] <= 0.75)])} samples ({len(df_valid[(df_valid['confidence'] > 0.50) & (df_valid['confidence'] <= 0.75)])/len(df_valid)*100:.1f}%)")
    print(f"   35-50% (Low):    {len(df_valid[(df_valid['confidence'] > 0.35) & (df_valid['confidence'] <= 0.50)])} samples ({len(df_valid[(df_valid['confidence'] > 0.35) & (df_valid['confidence'] <= 0.50)])/len(df_valid)*100:.1f}%)")
    
    # Save to file
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            f.write(f"\n\nClassification Report:\n{metrics['classification_report']}")
        print(f"\n💾 Report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Evaluasi akurasi model deteksi penyakit kulit')
    parser.add_argument('--dataset', type=str, help='Path ke folder dataset (struktur: dataset/class/image.jpg)')
    parser.add_argument('--csv', type=str, help='Path ke CSV file dengan kolom: filename,label')
    parser.add_argument('--images', type=str, help='Path ke folder images (jika pakai --csv)')
    parser.add_argument('--output', type=str, default='evaluation_report.txt', help='Output file untuk report')
    parser.add_argument('--save-results', type=str, help='Simpan hasil prediksi ke CSV')
    
    args = parser.parse_args()
    
    # Validasi input
    if not args.dataset and not (args.csv and args.images):
        print("❌ Error: Harus provide --dataset ATAU --csv + --images")
        parser.print_help()
        return
    
    print("\n🔬 EVALUASI MODEL DETEKSI PENYAKIT KULIT")
    print("="*80)
    
    # Load dan evaluasi
    if args.dataset:
        df_results = evaluate_from_folder(args.dataset)
    else:
        df_results = evaluate_from_csv(args.csv, args.images)
    
    # Save results
    if args.save_results:
        df_results.to_csv(args.save_results, index=False)
        print(f"\n💾 Results saved to: {args.save_results}")
    
    # Calculate metrics
    print("\n🔢 Menghitung metrik...")
    metrics = calculate_metrics(df_results)
    
    # Print report
    print_report(metrics, args.output)
    
    print("\n✅ Evaluasi selesai!")
    print("\n📌 REKOMENDASI:")
    if metrics and metrics['accuracy'] < 0.70:
        print("   ⚠️  Akurasi < 70% - Model TIDAK SIAP untuk produksi")
        print("   🔧 Saran: Kumpulkan lebih banyak data, lakukan augmentasi, atau fine-tune ulang")
    elif metrics and metrics['accuracy'] < 0.85:
        print("   ⚠️  Akurasi 70-85% - Model perlu improvement sebelum produksi")
        print("   🔧 Saran: Test lebih ekstensif, perbaiki class dengan F1 rendah")
    else:
        print("   ✅ Akurasi > 85% - Model cukup baik, tapi tetap perlu monitoring")
        print("   📝 Catatan: Untuk aplikasi medis, tetap perlu disclaimer dan validasi klinis")


if __name__ == "__main__":
    main()
