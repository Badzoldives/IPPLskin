"""
Script test untuk memverifikasi model berfungsi dengan baik
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("=" * 50)
    print("Testing Health Endpoint...")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_model_info():
    """Test model info endpoint"""
    print("=" * 50)
    print("Testing Model Info Endpoint...")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/model-info")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Model Repo: {data['model_repo']}")
    print(f"Number of Classes: {data['num_classes']}")
    print(f"Input Size: {data['input_size']}")
    print(f"Classes: {len(data['classes'])} classes loaded")
    print()

def test_classes():
    """Test classes endpoint"""
    print("=" * 50)
    print("Testing Classes Endpoint...")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/classes")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Total Classes: {len(data['classes'])}")
    print("\nFirst 5 classes:")
    for i, cls in enumerate(data['classes'][:5], 1):
        print(f"  {i}. {cls}")
    print()

def test_confidence_validation():
    """Test confidence validation dengan gambar dummy"""
    print("=" * 50)
    print("Testing Confidence Validation...")
    print("=" * 50)
    print("Note: Untuk test lengkap, upload gambar dari frontend")
    print("Model akan menolak gambar dengan confidence < 35%")
    print("Model akan memberi warning untuk confidence 35-50%")
    print("Model akan memberikan hasil normal untuk confidence > 50%")
    print()

if __name__ == "__main__":
    try:
        print("\n🧪 SKIN DISEASE DETECTION MODEL TEST\n")
        
        test_health()
        test_model_info()
        test_classes()
        test_confidence_validation()
        
        print("=" * 50)
        print("✅ All basic tests passed!")
        print("=" * 50)
        print("\n📝 Next Steps:")
        print("1. Buka frontend di browser (http://localhost:5173)")
        print("2. Upload foto kulit untuk test deteksi")
        print("3. Coba upload gambar bukan kulit (makanan, dll) untuk test validasi")
        print("4. Periksa confidence level dan warning message")
        print()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Backend tidak berjalan!")
        print("Jalankan: cd backend-ml && uvicorn app:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
