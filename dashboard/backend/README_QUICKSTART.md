# EpiSentinel — Dashboard Running Guide

## ✅ Status
- **Backend**: Running on `http://127.0.0.1:8000` ✓
- **Model**: MAPIE-wrapped Ensemble loaded ✓
- **Predictions**: Working (30+ district predictions tested) ✓
- **Frontend**: Ready to use ✓

## 🚀 Quick Start

### Option 1: Start Everything (Recommended)

```powershell
cd dashboard/backend
python3 -m uvicorn main:app --reload --port 8000
```

In another terminal:
```powershell
# Navigate to the frontend folder and open in browser
Start-Process "http://localhost:8000/dashboard/input.html"
```

### Option 2: Manual Steps

1. **Terminal 1 — Start Backend**:
   ```powershell
   cd dashboard/backend
   python3 -m uvicorn main:app --reload --port 8000
   ```

2. **Terminal 2 — Test Predictions** (Optional):
   ```powershell
   cd dashboard/backend
   python3 show_predictions.py
   ```

3. **Browser** — Open Dashboard:
   ```
   http://localhost:8000/dashboard/input.html
   ```

## 📊 How to Use

1. **Upload CSV**: Click the upload zone and select `synthetic_test_data.csv` (or your own)
2. **Preview**: The data table shows the first 10 rows
3. **Run Predictions**: Click the red "Run Predictions" button
4. **View Results**:
   - **Heatmap**: Districts are color-coded:
     - 🟢 **Green** = Low Risk (≤50%)
     - 🟡 **Yellow** = High Risk (51-70%)
     - 🔴 **Red** = Critical Risk (>70%)
   - **Stats**: Total cases, average risk, high/low count
   - **Chatbot**: Ask about results and risk drivers
   - **Click Districts**: Modal with detailed predictions

## 🛠 Troubleshooting

**Backend won't start?**
- Ensure all dependencies are installed:
  ```powershell
  python3 -m pip install -r requirements.txt
  ```

**Model loading fails?**
- Check that model files exist in `models/final/`:
  - `mapie_wrapped_ensemble.joblib`
  - `weighted_ensemble_plus1_near_optimal_no_district_pop.joblib`
  - `episentinel_pipeline.joblib`

**CSV upload fails?**
- Ensure CSV has a `district`, `state`, or `region` column
- All other columns are treated as numeric features

**Port 8000 already in use?**
- Change port: `python3 -m uvicorn main:app --port 8001`
- Update frontend: Change `API_BASE_URL = 'http://localhost:8001'` in `input.html`

## 📁 Project Structure

```
dashboard/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── predict_router.py       # /predict endpoint
│   ├── requirements.txt        # Dependencies
│   └── [models loaded from ../../../models/final/]
├── frontend/
│   ├── input.html              # Data input & heatmap page (you are here!)
│   ├── index.html              # Dashboard
│   ├── synthetic_test_data.csv # Test data
│   └── style.css               # Styling
```

## 🔍 Backend API Reference

**POST `/predict`** — Run predictions

Request:
```
Content-Type: multipart/form-data
file: <CSV file with district/state column>
```

Response (200 OK):
```json
{
  "predictions": {
    "Karnataka": {
      "risk_score": 45.2,
      "predicted_cases": 18,
      "status": "High",
      "top_driver": "Rainfall_Total_Week_Lag1",
      "detailed_explanation": "..."
    },
    ...
  }
}
```

## 💾 Features

- ✅ Real ML ensemble predictions (MAPIE-wrapped with conformal bounds)
- ✅ Choropleth heatmap with color-coded risk levels
- ✅ Interactive tooltips on hover
- ✅ Detailed district reports in modal
- ✅ CSV preview and validation
- ✅ Result statistics
- ✅ Chatbot for interpretation

Enjoy! 🎉
