"""
Script sederhana untuk test API Skin Disease Detection
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test endpoint health check"""
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_classes():
    """Test endpoint get classes"""
    print("\n" + "="*50)
    print("TEST 2: Get All Classes")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/classes")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Total Classes: {len(data['classes'])}")
    print("\nClasses:")
    for i, cls in enumerate(data['classes'][:5], 1):
        print(f"  {i}. {cls}")
    print(f"  ... dan {len(data['classes']) - 5} lainnya")
    return response.status_code == 200

def test_model_info():
    """Test endpoint model info"""
    print("\n" + "="*50)
    print("TEST 3: Get Model Info")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_predict(image_path):
    """Test endpoint predict dengan gambar"""
    print("\n" + "="*50)
    print("TEST 4: Predict Image")
    print("="*50)
    print(f"Image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/predict", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ HASIL PREDIKSI:")
            print(f"  Penyakit: {data['prediction']['class']}")
            print(f"  Confidence: {data['prediction']['confidence']:.2%}")
            print(f"  Severity: {data['disease_info']['severity']}")
            print(f"\n  Deskripsi: {data['disease_info']['description']}")
            print(f"\n  Rekomendasi: {data['disease_info']['recommendation']}")
            
            print("\n  Top 3 Predictions:")
            for i, pred in enumerate(data['all_predictions'][:3], 1):
                print(f"    {i}. {pred['class']}: {pred['confidence']:.2%}")
            
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except FileNotFoundError:
        print(f"❌ File tidak ditemukan: {image_path}")
        print("Silakan ganti path dengan gambar yang valid")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print(" 🧪 TESTING SKIN DISEASE DETECTION API")
    print("="*60)
    
    # Test semua endpoint
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("Get Classes", test_get_classes()))
    results.append(("Model Info", test_model_info()))
    
    # Test predict - GANTI PATH INI DENGAN GAMBAR ANDA
    image_path = "test_image.jpg"  # ⬅️ GANTI INI
    results.append(("Predict Image", test_predict(image_path)))
    
    # Summary
    print("\n" + "="*60)
    print(" 📊 TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {test_name}")
    
    total_pass = sum(1 for _, passed in results if passed)
    print(f"\n  Total: {total_pass}/{len(results)} tests passed")

if __name__ == "__main__":
    main()
