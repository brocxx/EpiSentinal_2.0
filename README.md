<div align="center">
  <img src="https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=1200&q=80" alt="EpiSentinel Banner" width="100%" style="border-radius: 12px; margin-bottom: 20px;" />

  # 🛡️ EpiSentinel
  ### *AI-Powered Outbreak Prediction & Grounded Decision Advisory System*

  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
  [![D3.js](https://img.shields.io/badge/D3.js-F9A03F?style=for-the-badge&logo=d3.js&logoColor=white)](https://d3js.org)
  [![Gemini](https://img.shields.io/badge/Gemini_AI-8E75C2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://deepmind.google/technologies/gemini)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

  **Empowering public health leadership with proactive, block-level dengue risk forecasting and grounded action plans 14 days before clinical peaks.**
</div>

---

## 📌 Table of Contents
- [📖 Introduction \& The Biological Problem](#-introduction--the-biological-problem)
  - [The Core Challenge](#the-core-challenge)
  - [The Biological Clock: Why 14 Days Matters](#the-biological-clock-why-14-days-matters)
  - [EpiSentinel's Modern Paradigm Shift](#episentinels-modern-paradigm-shift)
- [⚡ Key Features by Persona](#-key-features-by-persona)
  - [🏥 Operational \& Strategic Personas](#-operational--strategic-personas)
  - [⚙️ Core Technical Capabilities](#️core-technical-capabilities)
- [🛠️ Tech Stack Breakdown](#️-tech-stack-breakdown)
- [🚀 Getting Started](#-getting-started)
  - [📋 Prerequisites](#-prerequisites)
  - [🔑 Environment Configuration](#-environment-configuration)
  - [📦 Installation Steps](#-installation-steps)
  - [💻 Running Locally](#-running-locally)
- [📂 Project Directory Structure](#-project-directory-structure)
- [🔌 API Endpoints \& Basic Usage](#-api-endpoints--basic-usage)
  - [1. District Advisory Chat (`/chat/district`)](#1-district-advisory-chat-chatdistrict)
  - [2. State-Level Aggregate Chat (`/chat/state`)](#2-state-level-aggregate-chat-chatstate)
  - [3. Guardrail and SOP Violations Handler](#3-guardrail-and-sop-violations-handler)
- [🏗️ System Architecture \& Data Pipeline](#️-system-architecture--data-pipeline)
- [🚢 Deployment \& CI/CD Pipeline](#-deployment--cicd-pipeline)
- [🤝 Contributing \& Code of Conduct](#-contributing--code-of-conduct)
- [📄 License](#-license)

---

## 📖 Introduction & The Biological Problem

### The Core Challenge
District Health Officers (DHOs) and block-level health workers in high-burden regions of India struggle to make proactive resource allocation decisions. Deploying field teams, initiating chemical vector control, and pre-positioning medical supplies at sub-district resolution are often delayed until an outbreak has already peaked. 

Existing public health surveillance frameworks, such as the Integrated Disease Surveillance Programme (IDSP) and the National Vector Borne Disease Control Programme (NVBDCP), operate with a passive, retrospective reporting workflow. Outbreak data is typically delayed by a **21-day administrative lag**, lacks sub-district granularity, and fails to integrate real-time environmental indicators. Responses are, by definition, reactive—missing the critical biological window of intervention.

### The Biological Clock: Why 14 Days Matters
Dengue transmission has a fixed, predictable environmental and biological timeline:

```
[Heavy Rainfall / Humidity Spike]
               │
               ▼
 [Stagnant Water Accumulation]   (7 - 10 Days)
               │
               ▼
  [Vector Breeding & Hatching]   (Extrinsic Incubation: 8 - 12 Days)
               │
               ▼
   [Infected Mosquito Bites]     (Intrinsic Incubation: 4 - 7 Days)
               │
               ▼
     [Clinical Outbreak Peak]    (Total Biological Lag: ~14 - 21 Days)
```

EpiSentinel leverages this biological lag. By monitoring daily climate anomalies and satellite data *before* cases begin to rise, it gives health administrators a **7-to-14-day early warning forecast**, buying the time needed to deploy preventative vector control measures.

### EpiSentinel's Modern Paradigm Shift
EpiSentinel is an advanced epidemic risk visualization, prediction, and advisory dashboard designed for the state of Karnataka. It shifts public health strategy from reactive firefighting to proactive, data-driven prevention:
1. **Dynamic Forecasting**: Blends time-series neural networks (LSTMs) and gradient boosting ensembles (XGBoost/Random Forest) to output district-specific outbreak probabilities.
2. **Explainable AI (XAI)**: Utilizes **SHAP (SHapley Additive exPlanations)** to dissect the machine learning decisions, converting complex mathematical features into clean, plain-language insights for clinicians.
3. **SOP-Grounded Advisory (RAG)**: Integrates a guardrailed Large Language Model chatbot powered by **Google Gemini** and **LangChain**, providing customized clinical and operational action plans strictly aligned with certified Standard Operating Procedures (SOPs).

---

## ⚡ Key Features by Persona

### 🏥 Operational & Strategic Personas

*   **District Health Officer (DHO) Portal**: 
    *   Interactive, localized D3.js district heatmap.
    *   Clear risk status tags (`LOW`, `MODERATE`, `HIGH`) and dynamic outbreak warnings.
    *   Tactical action items: specific SOP recommendations on fogging, larvicide application, and household surveys based on SHAP drivers.
*   **Hospital Operations & Clinical Managers**:
    *   Surge bed capacity planning guides.
    *   Clinical supply checklists (platelet reserves, IV fluids, NS1 rapid diagnostics) tailored to local risk metrics.
    *   Workforce rota planning advice based on predicted case trends.
*   **State Health Officials**:
    *   Statewide aggregate command map of Karnataka districts.
    *   Active Alert tracking (counting districts exceeding the $>50\%$ risk threshold).
    *   State-wide resource allocation, supply redirection guidance, and regional escalation alerts.

### ⚙️ Core Technical Capabilities

*   🔮 **Multi-Model ML Pipeline**: Ensemble of Long Short-Term Memory (LSTM) neural networks (analyzing temporal trends over a 30-day window) and XGBoost/Random Forest models (evaluating daily spatial feature snapshots).
*   🗺️ **Interactive D3.js Geospatial Layer**: Seamless SVG-rendered vector map of Karnataka with intuitive interactive zooms, custom path tooltips, and real-time risk-scaled color scales (Glassmorphism layout).
*   🛡️ **SOP-Grounded Advisory Chatbot (Sentinel AI)**: RAG chatbot strictly grounded on internal Standard Operating Procedures (`context.md`).
*   ⚖️ **Explainable AI (XAI)**: Built-in SHAP explanation breakdowns rendering mathematical feature importances into clear, plain-language statements (e.g., *"Risk is elevated due to a 30% surge in cumulative rainfall 14 days ago"*).
*   🔒 **Clinical & Domain Guardrails**: Hardcoded validation routines preventing hallucinated medical dosages, out-of-domain answers (e.g., general coding), or off-topic prompt injections.

---

## 🛠️ Tech Stack Breakdown

| Layer | Technology | Key Utility |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, CSS3, ES6+ Javascript | Modern glassmorphism system, responsive layout grids, sidebar transitions |
| **Visualization** | D3.js (v7), Lucide Icons | Responsive GeoJSON SVG rendering, dynamic geographic scaling, custom vector path overlays |
| **Backend API** | FastAPI, Uvicorn | High-performance async router, Pydantic data schemas, Static file mounting |
| **AI Advisory (RAG)** | LangChain, Google Gemini API | Grounded LLM advisory generation, Pydantic validation, structured prompt engineering |
| **Machine Learning** | XGBoost, Scikit-Learn, PyTorch | Ensemble predictions (Random Forest, XGBoost), LSTM temporal prediction models |
| **Explainability (XAI)**| SHAP | Extraction of shapley values mapped directly to API outputs for dashboard explainability |
| **Data Formats** | GeoJSON, JSON | Topographic boundary representation, prediction records schema |

---

## 🚀 Getting Started

### 📋 Prerequisites
Ensure you have the following installed on your machine:
*   **Python**: `3.10` or higher
*   **Modern Browser**: Chrome, Edge, Safari, or Firefox (supporting ES6 modules and D3.js v7)
*   **Google Gemini API Key**: Obtain a developer key from the [Google AI Studio](https://aistudio.google.com).

### 🔑 Environment Configuration
Create a `.env` file inside the `chatbot` subdirectory to authorize the Sentinel AI engine:

```env
# Path: chatbot/.env
GOOGLE_API_KEY=AIzaSy...your_gemini_api_key_here...
CONTEXT_MD_PATH=context.md
GEMINI_MODEL=gemini-1.5-flash
```

*Note: For deep clinical reasoning tasks, you can switch `GEMINI_MODEL` to `gemini-1.5-pro`.*

### 📦 Installation Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/BlackCatDisha/EpiSentinel.git
    cd EpiSentinel
    ```

2.  **Set Up the Python Backend Environment**:
    ```bash
    cd dashboard/backend
    python -m venv venv
    
    # On Windows (Command Prompt or PowerShell)
    .\venv\Scripts\activate
    
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 💻 Running Locally

EpiSentinel features an integrated architecture where the FastAPI backend hosts and serves the interactive frontend static dashboard. This avoids browser CORS errors when loading the local GeoJSON maps directly from the disk.

1.  **Launch the Unified Server**:
    Ensure your virtual environment is active in the `dashboard/backend/` folder, then run:
    ```bash
    uvicorn main:app --reload --port 8000
    ```

2.  **Verify the System Logs**:
    On startup, the system will verify and cache your Standard Operating Procedures file:
    ```text
    INFO:     context.md loaded from 'context.md' (3528 chars).
    INFO:     Gemini LLM initialised (model=gemini-1.5-flash).
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ```

3.  **Access the Dashboard**:
    Open your browser and navigate to:
    *   **Interactive Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (Automatically redirects to `/dashboard/`)
    *   **Swagger API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Interactive endpoints playground)

---

## 📂 Project Directory Structure

Below is the directory architecture of EpiSentinel, organizing its predictive, visual, and language-based components:

```directory
EpiSentinel/
│
├── data/                                # Unified Data Storage
│   ├── raw/                             # Spatial boundaries & synthetic test datasets
│   │   ├── india_states.geojson
│   │   ├── karnataka_districts.json
│   │   ├── state_map_urls.json
│   │   └── synthetic_test_data.csv
│   └── processed/                       # Trainable panel datasets & evaluation metrics
│       ├── model_ready_district_week_trainable.csv
│       ├── ndvi+pop_model_ready_district_week_trainable.csv
│       ├── with_pop_model_ready_district_week_trainable.csv
│       └── metrics/                     # Run metric summaries (combined, long, top10)
│
├── models/                              # Serialized ML Pipeline Artifacts
│   ├── final/                           # Production-ready models (Ensemble & XGBoost fallback)
│   │   ├── weighted_ensemble_plus1_near_optimal_no_district_pop.joblib
│   │   ├── ensemble_plus1_near_optimal_no_district_pop.json
│   │   └── episentinel_pipeline.joblib
│   └── research_experiments/             # Historical training runs & sub-models
│       ├── random_forest/               # RF scripts, prediction outputs, & feature logs
│       ├── xgboost/                     # XGBoost validation curves, SHAP explainers
│       ├── final_model_no_district_pop/ # Baseline ensemble metrics
│       └── final_model_no_district_pop_standardised/
│
├── dashboard/                           # Web Dashboard Components
│   ├── frontend/                        # Web dashboard client (D3.js maps, layouts, charts)
│   │   ├── index.html
│   │   ├── input.html
│   │   ├── style.css
│   │   ├── app.js
│   │   └── data.js
│   └── backend/                         # FastAPI predictive endpoints & RAG Chatbot
│       ├── .env                         # API configurations & credentials
│       ├── main.py                      # FastAPI entrypoint (serves static dashboard)
│       ├── router.py                    # Endpoint declarations (/chat/district, /chat/state)
│       ├── predict_router.py            # Prediction metadata routing
│       ├── episentinel_chatbot.py       # Core Pydantic validators, prompts & RAG logic
│       ├── context.md                   # SOP Grounding documents
│       └── requirements.txt             # Python backend dependencies
│
├── archive/                             # Safe keeping of legacy/duplicate folders
│   └── EpiSentinel_Ishan/               # Preserved user-specific historical workspace clone
│
├── EpiSentinel_Project_Info.md          # Internal system specifications markdown
├── .gitignore                           # Git ignore mappings
└── README.md                            # Comprehensive system documentation
```

---

## 🔌 API Endpoints & Basic Usage

FastAPI serves two core chatbot interfaces mapping to strategic and tactical use-cases.

### 1. District Advisory Chat (`/chat/district`)
For DHOs or Facility Managers seeking actions on a single district.
*   **Method**: `POST`
*   **URL**: `http://localhost:8000/chat/district`
*   **Sample Request Body**:
    ```json
    {
      "role": "district_health_officer",
      "district_name": "Raichur",
      "risk_score": 0.84,
      "predicted_cases": 47,
      "shap_drivers": [
        {
          "feature": "cases_roll4_mean",
          "display_name": "4-week rolling average of reported cases",
          "shap_value": 0.72,
          "feature_value": 18.5
        },
        {
          "feature": "rainfall_total_week_lag1",
          "display_name": "total rainfall last week",
          "shap_value": 0.41,
          "feature_value": 97.6
        }
      ],
      "user_message": "What immediate tactical actions should I deploy this week?"
    }
    ```
*   **Sample Response Output**:
    ```json
    {
      "response": "Based on Raichur's critical risk (84.0% Outbreak Probability, 47 predicted cases) driven by high rolling cases and heavy recent rainfall (97.6mm), execute standard Level 3 transmission protocols immediately:\n1. Deploy emergency vector control teams for targeted indoor residual spraying and larvicide application in the highest-burden wards.\n2. Initiate daily mosquito breeding checks in stagnant water locations.\n3. Mobilize auxiliary nursing midwives (ANMs) to carry out active household fever surveys. Refer to SOP Section 3.2 for field assignment guidelines."
    }
    ```

---

### 2. State-Level Aggregate Chat (`/chat/state`)
Used by state command centers to evaluate multi-district priority lists.
*   **Method**: `POST`
*   **URL**: `http://localhost:8000/chat/state`
*   **Sample Request Body**:
    ```json
    {
      "role": "state_official",
      "aggregates": {
        "total_predicted_cases": 312,
        "average_risk_score": 0.61,
        "active_alerts": 3
      },
      "districts": [
        {
          "district_name": "Raichur",
          "risk_score": 0.84,
          "predicted_cases": 47,
          "shap_drivers": [
            {
              "feature": "cases_roll4_mean",
              "display_name": "4-week rolling average of reported cases",
              "shap_value": 0.72,
              "feature_value": 18.5
            }
          ]
        },
        {
          "district_name": "Vijayapura",
          "risk_score": 0.21,
          "predicted_cases": 3,
          "shap_drivers": [
            {
              "feature": "iso_week",
              "display_name": "week of the year",
              "shap_value": -0.31,
              "feature_value": 12.0
            }
          ]
        }
      ],
      "user_message": "Which districts must receive resource priority from the state depot?"
    }
    ```

---

### 3. Guardrail and SOP Violations Handler
If a user submits an off-domain prompt or requests unverified treatments (e.g. antibiotic or specific antiviral dosages not covered in the local SOP), the API returns a protective validation block:

*   **Prompt**: *"What is the recommended antiviral dosage for dengue treatment?"*
*   **Response**:
    ```text
    "I don't have sufficient information in the current SOPs to answer that. Please consult your state health authority guidelines."
    ```
*   **Prompt**: *"Can you write me a python script to sort a list?"*
*   **Response**:
    ```text
    "I'm restricted to advising on dengue outbreak response based on EpiSentinel predictions and your organisation's SOPs. I can't help with that request."
    ```

---

## 🏗️ System Architecture & Data Pipeline

EpiSentinel runs an automated, cyclical pipeline to keep predictions fresh:

```
                  ┌───────────────────────────────┐
                  │   SCHEDULED MORNING SCHEMAS  │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   IMD & ERA5    │      │  IDSP Weekly    │      │ Google GEE Sat  │
│ Weather API     │      │  PDF Reports    │      │ (NDWI & NDVI)   │
└────────┬────────┘      └────────┬────────┘      └────────┬────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │ Feature Engineering Engine    │
                  │ (Lags, rolling avg, breeding  │
                  │ index: NDWI x Rain x Temp)    │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │      Parallel ML Pipeline     │
                  │   ┌───────────────────────┐   │
                  │   │ LSTM (Temporal trends)│   │
                  │   ├───────────────────────┤   │
                  │   │ XGBoost (Today's snap)│   │
                  │   └───────────┬───────────┘   │
                  └───────────────┼───────────────┘
                                  │ Blended Risk Scores + SHAP
                                  ▼
                  ┌───────────────────────────────┐
                  │       predictions.json        │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌────────────────────────────────┐       ┌────────────────────────────────┐
│   Interactive Geospatial map   │       │   Sentinel AI RAG Chatbot      │
│   D3.js (Front-end Dashboard)  │       │   (FastAPI Backend / Gemini)   │
└────────────────────────────────┘       └────────────────────────────────┘
```

---

## 🚢 Deployment & CI/CD Pipeline

To move EpiSentinel to a production cloud topology:

*   **Containerization**: Use the multi-stage `Dockerfile` to compile and package the FastAPI application.
*   **Serverless Pipeline**: Run the scheduled Data Ingestion Pipeline inside **AWS Lambda** (triggered weekly by Amazon EventBridge) to fetch IMD/ERA5 climate datasets, re-predict with the trained XGBoost/LSTM bins, and write the updated `predictions.json` into **AWS S3**.
*   **Static Hosting**: The client dashboard files can be packaged and delivered globally through **AWS CloudFront** / **Vercel** / **Netlify** or run natively out of the FastAPI Docker image.
*   **CI/CD Pipeline (GitHub Actions)**:
    *   Lints Python logic (`ruff` or `flake8`).
    *   Validates API router tests via `pytest`.
    *   Builds the Docker container and deploys it automatically to **AWS ECS / Fargate** or **Google Cloud Run** upon merges to the `main` branch.

---

## 🤝 Contributing & Code of Conduct

We welcome contributions from epidemiologists, data scientists, software engineers, and public health practitioners!

### How to Contribute
1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/your-awesome-feature`.
3. Commit your modifications: `git commit -m "feat: add detailed spatial correlation factors"`.
4. Push the branch: `git push origin feature/your-awesome-feature`.
5. Open a Pull Request detailing the changes, context, and verification steps.

### Code of Conduct
*   Maintain a respectful, professional, and inclusive space for all contributors.
*   Prioritize scientific accuracy and rigorous testing, especially concerning clinical safety limits and predictive model validation.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
<div align="center">
  <sub>Developed with 🩺 by the EpiSentinel Core Team. Protecting communities through predictive science.</sub>
</div>
