"""
Script untuk test API backend-ml
"""
import requests
import sys

# Base URL
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_classes():
    """Test get classes endpoint"""
    print("🔍 Testing get classes...")
    response = requests.get(f"{BASE_URL}/classes")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total classes: {data['total']}")
    for i, cls in enumerate(data['classes'], 1):
        print(f"  {i}. {cls}")
    print()

def test_model_info():
    """Test model info endpoint"""
    print("🔍 Testing model info...")
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_predict(image_path):
    """Test predict endpoint"""
    print(f"🔍 Testing predict with image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/predict", files=files)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Prediction Result:")
            print(f"  Status: {data.get('status')}")
            
            prediction = data.get('prediction', {})
            print(f"\n  🔬 Diagnosis: {prediction.get('label')}")
            print(f"  📈 Confidence: {prediction.get('confidence'):.2%}")
            print(f"  📝 Description: {prediction.get('description')}")
            print(f"  ⚠️  Severity: {prediction.get('severity')}")
            print(f"  💡 Recommendation: {prediction.get('recommendation')}")
            
            print(f"\n  📊 Top 3 Predictions:")
            for i, pred in enumerate(data.get('top_3_predictions', []), 1):
                print(f"    {i}. {pred['class']}: {pred['confidence']:.2%}")
        else:
            print(f"❌ Error: {response.json()}")
    
    except FileNotFoundError:
        print(f"❌ Error: File not found - {image_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("  SKIN DISEASE DETECTION API - TEST SCRIPT")
    print("=" * 60)
    print()
    
    # Test endpoints
    test_health()
    test_get_classes()
    test_model_info()
    
    # Test predict if image path provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_predict(image_path)
    else:
        print("ℹ️  Untuk test predict, jalankan:")
        print("   python test_api.py path/to/image.jpg")
    
    print("=" * 60)
    print("✅ Test completed!")
    print("=" * 60)
