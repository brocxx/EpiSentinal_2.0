#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

import requests
import json
from pathlib import Path

CSV_FILE = Path(__file__).parent.parent / 'frontend' / 'synthetic_test_data.csv'
API_URL = 'http://127.0.0.1:8000/predict'

if not CSV_FILE.exists():
    print(f"❌ CSV not found: {CSV_FILE}")
    sys.exit(1)

print(f"📤 POSTing {CSV_FILE.name} to {API_URL}")

try:
    with open(CSV_FILE, 'rb') as f:
        response = requests.post(API_URL, files={'file': ('data.csv', f, 'text/csv')}, timeout=30)
    
    print(f"📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        predictions = data.get('predictions', {})
        print(f"✅ SUCCESS: Received {len(predictions)} district predictions")
        print("\nSample predictions:")
        for i, (district, pred) in enumerate(list(predictions.items())[:3]):
            print(f"  • {district}:")
            print(f"    Risk: {pred.get('risk_score', 'N/A')}%")
            print(f"    Status: {pred.get('status', 'N/A')}")
            print(f"    Cases: {pred.get('predicted_cases', 'N/A')}")
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.text[:500])
        sys.exit(1)

except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("Make sure backend is running: python -m uvicorn main:app --reload --port 8000")
    sys.exit(1)
