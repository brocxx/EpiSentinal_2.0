<div align="center">

# 🛡️ EpiSentinel 2.0
### *Proactive Dengue Outbreak Forecasting for Karnataka, India*

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.ai)
[![D3.js](https://img.shields.io/badge/D3.js-F9A03F?style=for-the-badge&logo=d3.js&logoColor=white)](https://d3js.org)
[![Gemini](https://img.shields.io/badge/Gemini_AI-8E75C2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://deepmind.google/technologies/gemini)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Predicting district-level dengue outbreaks 7 days in advance across Karnataka — shifting public health from reactive reporting to proactive intervention.**

</div>

---

## 📌 Table of Contents

- [What It Does](#-what-it-does)
- [The Problem It Solves](#-the-problem-it-solves)
- [Model & Results](#-model--results)
  - [What Is Predicted](#what-is-predicted)
  - [Training Data](#training-data)
  - [Experiments & Metrics](#experiments--metrics)
  - [Final Production Model](#final-production-model)
  - [Key Features (SHAP)](#key-features-shap)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Running Locally](#running-locally)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 What It Does

EpiSentinel is a **district-level dengue outbreak prediction and advisory dashboard** for the state of Karnataka. It takes this week's epidemiological and climate data for each district and answers one critical question:

> **Will this district experience a dengue outbreak next week?**

The output is a risk score (0–100%) per district, powering an interactive D3.js map and a RAG-powered AI chatbot that generates SOP-grounded action plans for health officers.

---

## 🦟 The Problem It Solves

Existing surveillance frameworks (IDSP, NVBDCP) are **reactive**. Outbreak reports arrive 2–3 weeks after cases have already peaked. By then, deploying field teams and pre-positioning medical supplies is too late.

Dengue has a predictable biological timeline:

```
[Rainfall / Humidity Spike]
          │
          ▼  7–10 days
[Stagnant Water / Mosquito Breeding]
          │
          ▼  8–12 days (Extrinsic Incubation)
[Infected Mosquito Bites]
          │
          ▼  4–7 days (Intrinsic Incubation)
[Clinical Outbreak Peak]
```

EpiSentinel exploits this biological lag. By monitoring **lagged case trends + climate signals** from the past 1–4 weeks, it predicts outbreaks **7 days before they peak** — giving health authorities a real intervention window.

---

## 🤖 Model & Results

### What Is Predicted

| Target | Type | Definition |
|---|---|---|
| `target_outbreak_plus1` | Binary (0/1) | Will next week's dengue cases exceed the district's historical 75th-percentile threshold? |
| `target_cases_plus1` | Regression (int) | How many cases will be reported next week? (used as secondary output in early experiments) |

**The production model predicts `target_outbreak_plus1`** — the binary outbreak classification. An "outbreak" is defined per-district using `district_case_q75` (the district's own historical 75th-percentile weekly count), making the threshold locally calibrated rather than statewide.

### Training Data

| Split | Years |
|---|---|
| Train | 2017 – 2021 |
| Validation | 2022 |
| Test | 2023 |

Each row = one **district × ISO week** combination (~30 districts × ~52 weeks × 7 years ≈ 10,000+ rows).

**Feature groups used:**

| Group | Features |
|---|---|
| Epidemiology | `dengue_cases_reported`, `dengue_deaths_weekly`, `cases_per_100k` |
| Lagged cases | `cases_lag1`, `cases_lag2`, `cases_lag3` (1–3 weeks ago) |
| Rolling averages | `cases_roll2_mean`, `cases_roll4_mean` (2-week and 4-week) |
| Current weather | `temperature_mean_week`, `humidity_mean_week`, `rainfall_total_week`, `temperature_max_week`, `humidity_max_week` |
| Lagged weather | `temperature_mean_week_lag1/2`, `humidity_mean_week_lag1/2`, `rainfall_total_week_lag1/2` |
| Seasonality | `week_sin`, `week_cos` (circular encoding of ISO week) |
| Population | `worldpop_total`, `worldpop_density_per_km2` |

**Features explicitly excluded** (geographic identity leakage):
- `district` — model must generalize across districts, not memorize them
- `population_2011` — constant per district; acts as a disguised district ID
- `district_case_q75` — per-district historical constant; re-encodes geographic identity as a float
- `year` — temporal shortcut with no meaning at deployment time

### Experiments & Metrics

Four distinct training runs were conducted. All evaluated on 2023 test data.

#### Run A — Individual Models (baseline, with population features)

| Model | Threshold | ROC-AUC | Precision | Recall | **F1** |
|---|---|---|---|---|---|
| CatBoost | 0.25 | 0.826 | 0.687 | 0.769 | **0.725** |
| XGBoost | 0.16 | 0.817 | 0.630 | 0.820 | 0.712 |
| LightGBM | 0.16 | 0.809 | 0.658 | 0.772 | 0.710 |
| RandomForest | 0.22 | 0.818 | 0.609 | 0.846 | 0.708 |
| Poisson Regressor | — | 0.481 | 0.669 | 0.692 | 0.680 |

#### Run B — Weighted Ensemble (district + population_2011 dropped) ✅ Production

| Model | Threshold | ROC-AUC | PR-AUC | Precision | Recall | **F1** |
|---|---|---|---|---|---|---|
| **WeightedEnsemble** | **0.15** | **0.821** | **0.825** | 0.622 | **0.856** | **0.720** |
| CatBoost | 0.16 | 0.826 | 0.829 | 0.613 | 0.856 | 0.714 |
| XGBoost | 0.14 | 0.815 | 0.819 | 0.626 | 0.825 | 0.711 |
| RandomForest | 0.26 | 0.818 | 0.825 | 0.622 | 0.823 | 0.709 |
| LightGBM | 0.10 | 0.813 | 0.819 | 0.613 | 0.836 | 0.707 |

#### Run C — Weighted Ensemble (standardized features)

| Model | ROC-AUC | Precision | Recall | F1 |
|---|---|---|---|---|
| WeightedEnsemble | 0.821 | 0.622 | 0.856 | 0.720 |
| CatBoost | 0.827 | 0.608 | 0.867 | 0.715 |
| LightGBM | 0.815 | 0.667 | 0.769 | 0.714 |

#### Run D — XGBoost v4 (leakage-fixed, recall-floor threshold)

A rigorous single-model pipeline that fixed 6 specific methodological issues from earlier runs:

| Fix Applied | Issue Addressed |
|---|---|
| Dropped `district_case_q75` from features | Geographic identity leakage disguised as a float |
| Dropped `is_unreliable_2017_peak_week` from features | Audit flag that doesn't exist at inference time |
| Panel-aware calendar CV (not row-index split) | Earlier CV mixed future rows from late districts into training |
| Recall floor ≥ 0.85 in threshold selection | Missing an outbreak is far more costly than a false alarm |
| Final model evaluated on true held-out test set | Previous code evaluated the CV-refitted estimator |
| `year` excluded from features | Temporal shortcut with no deployment-time meaning |

**Hyperparameter search (RandomizedSearchCV, 40 iterations, 5-fold panel CV):**

| Parameter | Search Space |
|---|---|
| `n_estimators` | 50, 100, 150, 200, 250, 300 |
| `max_depth` | 3, 4, 5, 6, 7, 8, 9 |
| `learning_rate` | 0.01, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20 |
| `subsample` | 0.6, 0.7, 0.8, 0.9, 1.0 |
| `colsample_bytree` | 0.6, 0.7, 0.8, 0.9, 1.0 |

Optimal threshold found: **0.3098** (with enforced recall ≥ 85%).

### Final Production Model

The production model is a **Weighted Ensemble** of 5 sub-models. Weights were optimized on 2022 validation F1 using Dirichlet distribution sampling:

| Sub-model | Weight |
|---|---|
| XGBoost | **49.5%** |
| CatBoost | 29.7% |
| Poisson Regressor | 10.8% |
| Random Forest | 9.1% |
| LightGBM | 0.9% |

**Test set performance (2023 data, threshold = 0.15):**

| Metric | Score |
|---|---|
| ROC-AUC | **0.821** |
| PR-AUC | **0.825** |
| Precision | 0.622 |
| **Recall** | **0.856** |
| F1 | **0.720** |
| True Positives (outbreaks caught) | 522 / 610 |
| False Negatives (outbreaks missed) | 88 / 610 |

> Recall is intentionally prioritized. A missed outbreak (false negative) means no intervention — far more dangerous than a false alarm.

### Key Features (SHAP)

Global SHAP analysis on the XGBoost model shows what actually drives predictions:

| Rank | Feature | Direction |
|---|---|---|
| 1 | 4-week rolling avg of cases | ↑ more → higher risk |
| 2 | Avg temperature 2 weeks ago | ↑ hotter → higher risk |
| 3 | 2-week rolling avg of cases | ↑ more → higher risk |
| 4 | Week of year | Later weeks → higher risk |
| 5 | Cases 3 weeks ago | ↑ more → higher risk |
| 6 | Total rainfall last week | ↑ more rain → higher risk |
| 7 | Cases per 100k population | ↑ higher rate → higher risk |

---

## 🏗️ System Architecture

```
[Input CSV: district × week features]
              │
              ▼
   ┌──────────────────────────┐
   │   WeightedEnsemble       │
   │  XGBoost  (49.5%)        │
   │  CatBoost (29.7%)        │
   │  Poisson  (10.8%)        │
   │  RF       ( 9.1%)        │
   │  LightGBM ( 0.9%)        │
   └────────────┬─────────────┘
                │  Risk probability (0–1)
                ▼
   ┌──────────────────────────┐
   │  Threshold = 0.15        │
   │  Critical / High / Low   │
   └────────────┬─────────────┘
                │
     ┌──────────┴──────────┐
     ▼                     ▼
┌──────────────┐    ┌──────────────────────┐
│ D3.js Map    │    │ Sentinel AI Chatbot  │
│ (Frontend)   │    │ Gemini + LangChain   │
│ Risk heatmap │    │ SOP-grounded advice  │
└──────────────┘    └──────────────────────┘
```

The FastAPI backend:
1. Serves the static frontend dashboard
2. Exposes `/predict` — accepts a CSV upload, runs it through the ensemble, returns risk scores per district
3. Exposes `/chat/district` and `/chat/state` — Gemini-powered advisory endpoints grounded on internal SOPs

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **ML Models** | XGBoost, CatBoost, LightGBM, Scikit-Learn (RF), Statsmodels (Poisson) |
| **Explainability** | SHAP (TreeExplainer) |
| **Backend API** | FastAPI, Uvicorn |
| **AI Advisory** | LangChain, Google Gemini API |
| **Frontend** | HTML5, CSS3, Vanilla JS |
| **Visualization** | D3.js v7 (GeoJSON district maps) |
| **Data** | Pandas, NumPy |
| **Serialization** | Joblib (.joblib model artifacts) |

---

## 📂 Project Structure

```
EpiSentinel/
│
├── data/
│   ├── raw/                              # Spatial boundaries & test inputs
│   │   ├── karnataka_districts.json
│   │   ├── india_states.geojson
│   │   ├── state_map_urls.json
│   │   └── synthetic_test_data.csv
│   └── processed/                        # Training datasets & evaluation metrics
│       ├── model_ready_district_week_trainable.csv
│       ├── with_pop_model_ready_district_week_trainable.csv
│       ├── ndvi+pop_model_ready_district_week_trainable.csv
│       └── metrics/                      # Per-run metric CSVs & SHAP outputs
│           ├── top5_metrics_plus1_no_district_pop.csv
│           ├── top5_metrics_plus1_standardised.csv
│           ├── top5_metrics_plus1_root.csv
│           ├── ensemble_vs_catboost_plus1.csv
│           ├── shap_top10_per_model_no_pop.csv
│           └── shap_top10_per_model_standardised.csv
│
├── models/
│   ├── final/                            # Production models loaded by the dashboard
│   │   ├── weighted_ensemble_plus1_near_optimal_no_district_pop.joblib  ← PRIMARY
│   │   ├── ensemble_plus1_near_optimal_no_district_pop.json             ← Metrics/weights
│   │   └── episentinel_pipeline.joblib                                  ← XGBoost fallback
│   └── research_experiments/             # Historical training runs (for reference)
│       ├── random_forest/                # RF scripts, SHAP reports, predictions
│       ├── xgboost/                      # XGBoost v4 pipeline, PR curves, SHAP
│       ├── final_model_no_district_pop/  # Ensemble experiment artifacts
│       └── final_model_no_district_pop_standardised/
│
├── dashboard/
│   ├── frontend/                         # Static web dashboard (served by FastAPI)
│   │   ├── index.html                    # Main district map view
│   │   ├── input.html                    # CSV upload interface
│   │   ├── style.css                     # Glassmorphism design system
│   │   ├── app.js                        # D3.js map rendering & chatbot shell
│   │   └── data.js                       # Prediction data & district name mappings
│   └── backend/                          # FastAPI application
│       ├── main.py                       # App entrypoint, static file mounting
│       ├── predict_router.py             # /predict endpoint (model inference)
│       ├── router.py                     # /chat/district, /chat/state endpoints
│       ├── episentinel_chatbot.py        # RAG logic, Gemini integration, guardrails
│       ├── context.md                    # SOP grounding document for the chatbot
│       ├── requirements.txt              # Python dependencies
│       └── .env                          # API keys (not committed)
│
├── archive/                              # Legacy code preserved for reference
│   └── EpiSentinel_Ishan/
│
├── EpiSentinel_Project_Info.md
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- A modern browser (Chrome, Firefox, Edge)
- A **Google Gemini API key** from [Google AI Studio](https://aistudio.google.com)

### Environment Setup

Create a `.env` file inside `dashboard/backend/`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
CONTEXT_MD_PATH=context.md
GEMINI_MODEL=gemini-1.5-flash
```

> For deeper clinical reasoning, switch `GEMINI_MODEL` to `gemini-1.5-pro`.

### Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/brocxx/EpiSentinal_2.0.git
   cd EpiSentinal_2.0
   ```

2. **Set up a virtual environment:**
   ```bash
   cd dashboard/backend

   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Open the dashboard:**
   - Dashboard: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Upload & predict: [http://127.0.0.1:8000/input.html](http://127.0.0.1:8000/input.html)
   - API docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔌 API Reference

### `POST /predict`

Upload a CSV of district-week feature rows. Returns outbreak risk scores per district.

**Request:** `multipart/form-data` with a `.csv` file.

**Required columns:** `iso_week`, `cases_lag1`, `cases_lag2`, `cases_lag3`, `cases_roll2_mean`, `cases_roll4_mean`, `temperature_mean_week`, `humidity_mean_week`, `rainfall_total_week`, `temperature_mean_week_lag1`, `temperature_mean_week_lag2`, `humidity_mean_week_lag1`, `humidity_mean_week_lag2`, `rainfall_total_week_lag1`, `rainfall_total_week_lag2`, `week_sin`, `week_cos`, `worldpop_total`, `worldpop_density_per_km2`, `cases_per_100k`

**Response:**
```json
{
  "predictions": {
    "Raichur": {
      "risk_score": 84.2,
      "status": "Critical",
      "predicted_cases": 33,
      "top_driver": "Cases Roll4 Mean",
      "model_used": "WeightedEnsemble"
    }
  }
}
```

Risk thresholds:
- `>= threshold × 1.5` → **Critical**
- `>= threshold` → **High**
- `< threshold` → **Low**

---

### `POST /chat/district`

Get SOP-grounded action plans for a single district.

```json
{
  "role": "district_health_officer",
  "district_name": "Raichur",
  "risk_score": 0.84,
  "predicted_cases": 47,
  "shap_drivers": [
    {
      "feature": "cases_roll4_mean",
      "display_name": "4-week rolling average of cases",
      "shap_value": 0.72,
      "feature_value": 18.5
    }
  ],
  "user_message": "What immediate actions should I deploy this week?"
}
```

---

### `POST /chat/state`

Get state-level resource allocation guidance across multiple districts.

---

### Guardrails

The chatbot is strictly grounded on `context.md`. Off-domain prompts are blocked:

```
Prompt:   "What is the antiviral dosage for dengue?"
Response: "I don't have sufficient information in the current SOPs to answer that."

Prompt:   "Can you write a Python script?"
Response: "I'm restricted to advising on dengue outbreak response based on EpiSentinel predictions."
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: describe your change"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

Contributions from epidemiologists, data scientists, and public health practitioners are especially welcome.

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">
  <sub>Built to protect communities through predictive epidemiology. 🩺</sub>
</div>
