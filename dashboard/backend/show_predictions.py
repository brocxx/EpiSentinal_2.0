#!/usr/bin/env python3
import requests, json
from pathlib import Path

r = requests.post(
    'http://127.0.0.1:8000/predict',
    files={'file': open(Path(__file__).parent.parent / 'frontend/synthetic_test_data.csv', 'rb')},
    timeout=30
)

data = r.json()
preds = data.get('predictions', {})
print(f'✅ Received {len(preds)} predictions\n')
for i, (district, pred) in enumerate(list(preds.items())[:4]):
    print(f"{i+1}. {district}")
    print(f"   Risk: {pred['risk_score']}%  Status: {pred['status']}")
    print(f"   Cases: {pred['predicted_cases']}  Driver: {pred.get('top_driver', 'N/A')}\n")
