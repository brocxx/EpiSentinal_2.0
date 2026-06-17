import requests
import sys
from pathlib import Path

API = 'http://127.0.0.1:8000/predict'
CSV = Path(__file__).parent.parent / 'frontend' / 'synthetic_test_data.csv'

if not CSV.exists():
    print('Test CSV not found at', CSV)
    sys.exit(2)

print('Posting', CSV)
with open(CSV, 'rb') as f:
    files = {'file': ('data.csv', f, 'text/csv')}
    try:
        r = requests.post(API, files=files, timeout=30)
    except Exception as e:
        print('Request failed:', e)
        sys.exit(3)

print('Status:', r.status_code)
try:
    print(r.json())
except Exception:
    print(r.text)
