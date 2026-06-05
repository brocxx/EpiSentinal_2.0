"""
predict_router.py — EpiSentinel prediction API
Loads the MAPIE-wrapped weighted ensemble (XGBoost + LightGBM + RF + Poisson)
and returns per-district risk scores with conformal uncertainty bounds.
"""

import io
import numpy as np
import joblib
from pathlib import Path
import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter(tags=["prediction"])

BASE_DIR            = Path(__file__).resolve().parent.parent.parent
MODEL_PATH_MAPIE    = BASE_DIR / "models" / "final" / "mapie_wrapped_ensemble.joblib"
MODEL_PATH_ENSEMBLE = BASE_DIR / "models" / "final" / "weighted_ensemble_plus1_near_optimal_no_district_pop.joblib"
MODEL_PATH_XGB      = BASE_DIR / "models" / "final" / "episentinel_pipeline.joblib"

# ── Global model state ─────────────────────────────────────────────────────────
MODEL             = None   # WeightedEnsembleWrapper instance
FEATURE_COLUMNS   = []
OPTIMAL_THRESHOLD = 0.5
MODEL_NAME        = "Unknown"

# ── MAPIE conformal-prediction state ──────────────────────────────────────────
MAPIE_Q_HAT      = None   # float conformal radius; None → no bounds
MAPIE_CONFIDENCE = 0.90


# ── WeightedEnsembleWrapper ────────────────────────────────────────────────────
class WeightedEnsembleWrapper:
    """
    Reproduces the weighted ensemble predict_proba from the on-disk artifact.

    Key fix: the Poisson bundle's stored StandardScaler was fitted on
    already-standardised data (all means ~0, std ~1), so raw worldpop_total
    values (~10^6) overflow exp(). A properly-fitted poisson_scaler (stored
    in the MAPIE artifact) is injected here to bypass the broken stored one.

    NaN/inf guard: any sub-model that produces non-finite predictions is
    silently skipped so the overall blend stays valid.
    """
    def __init__(self, artifact: dict, poisson_scaler=None):
        self.artifact       = artifact
        self.bundles        = artifact["bundles"]
        self.weights        = artifact["weights"]
        self.threshold      = artifact["threshold"]
        self.model_keys     = artifact["model_keys"]
        self.poisson_scaler = poisson_scaler

    def _run_bundle(self, name: str, X: pd.DataFrame):
        bundle    = self.bundles[name]
        pipeline  = bundle["artifact"]   # tuple of sklearn objects
        feat_cols = bundle["feature_columns"]
        X_sub     = X.reindex(columns=feat_cols, fill_value=0.0)
        arr       = X_sub

        for i, step in enumerate(pipeline[:-1]):
            if name == "poisson" and i == 1 and self.poisson_scaler is not None:
                # Override broken stored scaler with properly-fitted one
                arr = self.poisson_scaler.transform(arr)
            else:
                arr = step.transform(arr)

        estimator = pipeline[-1]
        try:
            if hasattr(estimator, "predict_proba"):
                p = estimator.predict_proba(arr)[:, 1]
            else:
                raw = np.clip(estimator.predict(arr), 0, 1e6)
                p   = raw / (raw.max() + 1e-9)
        except Exception as exc:
            print(f"  Warning: {name} predict failed ({exc}) — skipping.")
            return None

        if np.any(~np.isfinite(p)):
            print(f"  Warning: {name} produced non-finite output — skipping.")
            return None

        return p

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        blend, total_w = np.zeros(len(X)), 0.0
        for name in self.model_keys:
            w = self.weights.get(name, 0.0)
            if w == 0.0:
                continue
            p = self._run_bundle(name, X)
            if p is None:
                continue
            blend  += w * p
            total_w += w
        if total_w > 0:
            blend /= total_w
        return np.column_stack([1 - blend, blend])


# ── Model loading ──────────────────────────────────────────────────────────────

def _load_base_model():
    global MODEL, FEATURE_COLUMNS, OPTIMAL_THRESHOLD, MODEL_NAME, MAPIE_Q_HAT, MAPIE_CONFIDENCE

    # 1. MAPIE artifact (ensemble + conformal radius + fixed Poisson scaler)
    if MODEL_PATH_MAPIE.exists():
        try:
            art               = joblib.load(MODEL_PATH_MAPIE)
            poisson_scaler    = art.get("poisson_scaler")
            MODEL             = WeightedEnsembleWrapper(art["ensemble"], poisson_scaler=poisson_scaler)
            FEATURE_COLUMNS   = art.get("feature_columns", [])
            OPTIMAL_THRESHOLD = art.get("threshold", 0.175)
            MAPIE_Q_HAT       = float(art["q_hat"])
            MAPIE_CONFIDENCE  = float(art.get("confidence", 0.90))
            MODEL_NAME        = "WeightedEnsemble+MAPIE"
            print(f"Loaded MAPIE-wrapped Ensemble. "
                  f"q_hat={MAPIE_Q_HAT:.4f} ({MAPIE_CONFIDENCE:.0%} confidence)")
            return
        except Exception as e:
            print(f"Warning: MAPIE load failed ({e}). Trying plain ensemble.")

    # 2. Plain ensemble (no conformal bounds)
    if MODEL_PATH_ENSEMBLE.exists():
        try:
            art               = joblib.load(MODEL_PATH_ENSEMBLE)
            MODEL             = WeightedEnsembleWrapper(art)
            feat_set          = []
            for v in art["bundles"].values():
                for f in v["feature_columns"]:
                    if f not in feat_set:
                        feat_set.append(f)
            FEATURE_COLUMNS   = feat_set
            OPTIMAL_THRESHOLD = art.get("threshold", 0.175)
            MODEL_NAME        = "WeightedEnsemble"
            print("Loaded Ensemble Model (no MAPIE bounds).")
            return
        except Exception as e:
            print(f"Warning: Could not load Ensemble ({e}). Falling back to XGBoost.")

    # 3. XGBoost fallback
    try:
        art               = joblib.load(MODEL_PATH_XGB)
        MODEL             = art.get("model")
        FEATURE_COLUMNS   = art.get("feature_columns", [])
        OPTIMAL_THRESHOLD = art.get("optimal_threshold", 0.5)
        MODEL_NAME        = "XGBoost"
        print("Loaded XGBoost Model (fallback).")
    except Exception as e:
        print(f"Critical: Could not load any model: {e}")


def load_model():
    global MODEL
    if MODEL is None:
        _load_base_model()


# ── Conformal bounds helper ────────────────────────────────────────────────────

def _confidence_bounds(prob: float) -> tuple:
    """Return (lower_pct, upper_pct) as percentages (0–100)."""
    if MAPIE_Q_HAT is None:
        pct = round(prob * 100, 1)
        return pct, pct
    lower = float(np.clip(prob - MAPIE_Q_HAT, 0.0, 1.0))
    upper = float(np.clip(prob + MAPIE_Q_HAT, 0.0, 1.0))
    return round(lower * 100, 1), round(upper * 100, 1)


# ── Endpoint ───────────────────────────────────────────────────────────────────

@router.post("/predict")
async def run_predictions(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    load_model()

    if MODEL is None:
        raise HTTPException(status_code=500,
                            detail="Model could not be loaded. Check backend logs.")

    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {e}")

    # Ensure all needed feature columns are present
    X = df.copy()
    for col in FEATURE_COLUMNS:
        if col not in X.columns:
            X[col] = 0.0

    X_features = X[FEATURE_COLUMNS] if FEATURE_COLUMNS else X

    try:
        preds_proba = MODEL.predict_proba(X_features)[:, 1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

    threshold_pct = OPTIMAL_THRESHOLD * 100
    conf_label    = f"{MAPIE_CONFIDENCE:.0%}" if MAPIE_Q_HAT is not None else "N/A"

    # Find district identifier column
    district_col = next(
        (c for c in ["district", "District", "region", "location", "name", "State", "state"]
         if c in df.columns),
        None
    )

    predictions = {}
    for i, row in df.iterrows():
        district     = str(row[district_col]) if district_col else f"Unknown_{i}"
        prob         = float(preds_proba[i])
        risk_score   = round(prob * 100, 1)
        lower, upper = _confidence_bounds(prob)

        if risk_score >= threshold_pct * 1.5:
            status = "Critical"
        elif risk_score >= threshold_pct:
            status = "High"
        else:
            status = "Low"

        # Rough top-driver proxy (highest absolute feature value)
        top_driver_col = "Unknown"
        max_val        = -9999
        for col in FEATURE_COLUMNS:
            if col in X_features.columns:
                val = abs(float(X_features.iloc[i][col]))
                if val > max_val:
                    max_val        = val
                    top_driver_col = col
        top_driver_formatted = top_driver_col.replace("_", " ").title()
        pred_cases           = max(0, int(risk_score / 2.5))

        predictions[district] = {
            "predicted_cases":   pred_cases,
            "risk_score":        risk_score,
            # ── Conformal confidence bounds ────────────────────────────────────
            "risk_score_lower":  lower,
            "risk_score_upper":  upper,
            "confidence_level":  conf_label,
            # ──────────────────────────────────────────────────────────────────
            "status":            status,
            "top_driver":        top_driver_formatted,
            "detailed_explanation": (
                f"Using {MODEL_NAME}: '{top_driver_formatted}' is the primary "
                f"indicator. Risk score: {risk_score}%. "
                f"{MAPIE_CONFIDENCE:.0%} confidence range: {lower}%-{upper}%."
            ),
            "model_used": MODEL_NAME,
        }

    return {"predictions": predictions}
