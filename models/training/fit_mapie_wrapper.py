"""
fit_mapie_wrapper.py
────────────────────
Wraps the existing EpiSentinel weighted ensemble with split-conformal
prediction calibration, producing risk_score_lower and risk_score_upper
(90% confidence bounds) at inference time.

Strategy:
  Use standard split-conformal regression-style calibration with
  non-conformity score = |predicted_prob - true_binary_label|.
  Calibrate on year 2022 (holdout) and guarantee >=90% coverage by
  definition of the finite-sample conformal guarantee.

Poisson fix:
  The stored StandardScaler was fitted on already-standardised data
  (mean~0, std~1). We refit a proper scaler from raw training data and
  store it in the artifact so predict_router.py can reuse it.

Run from the repo root:
    python models/training/fit_mapie_wrapper.py
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATHS = [
    os.path.join(REPO_ROOT, "data", "processed", "ndvi+pop_model_ready_district_week_trainable.csv"),
    os.path.join(REPO_ROOT, "data", "processed", "with_pop_model_ready_district_week_trainable.csv"),
    os.path.join(REPO_ROOT, "data", "processed", "model_ready_district_week_trainable.csv"),
]
DATA_PATH     = next((p for p in DATA_PATHS if os.path.exists(p)), None)
ENSEMBLE_PATH = os.path.join(REPO_ROOT, "models", "final",
                             "weighted_ensemble_plus1_near_optimal_no_district_pop.joblib")
OUT_PATH      = os.path.join(REPO_ROOT, "models", "final",
                             "mapie_wrapped_ensemble.joblib")

ALPHA    = 0.10
VAL_YEAR = 2022
TARGET   = "target_outbreak_plus1"


def get_submodel_proba(artifact, name, X_df, poisson_scaler=None):
    bundle    = artifact["bundles"][name]
    pipeline  = bundle["artifact"]
    feat_cols = bundle["feature_columns"]
    X_in = X_df.reindex(columns=feat_cols, fill_value=0.0)
    arr  = X_in
    for i, step in enumerate(pipeline[:-1]):
        if name == "poisson" and i == 1 and poisson_scaler is not None:
            arr = poisson_scaler.transform(arr)
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
        print(f"  Warning: {name} produced non-finite values — skipping.")
        return None
    return p


class WeightedEnsembleWrapper:
    def __init__(self, artifact, poisson_scaler=None):
        self.artifact       = artifact
        self.bundles        = artifact["bundles"]
        self.weights        = artifact["weights"]
        self.threshold      = artifact["threshold"]
        self.model_keys     = artifact["model_keys"]
        self.poisson_scaler = poisson_scaler

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        blend, total_w = np.zeros(len(X)), 0.0
        for name in self.model_keys:
            w = self.weights.get(name, 0.0)
            if w == 0.0:
                continue
            p = get_submodel_proba(self.artifact, name, X, self.poisson_scaler)
            if p is None:
                continue
            blend  += w * p
            total_w += w
        if total_w > 0:
            blend /= total_w
        return np.column_stack([1 - blend, blend])


# 1. Load data
print("=" * 60)
print("STEP 1 — Load dataset")
print("=" * 60)
if DATA_PATH is None:
    sys.exit("ERROR: No CSV found under data/processed/")
df = pd.read_csv(DATA_PATH)
print(f"Shape: {df.shape}")
if "is_unreliable_2017_peak_week" in df.columns:
    n = len(df)
    df = df[df["is_unreliable_2017_peak_week"] == False].reset_index(drop=True)
    print(f"Removed {n - len(df)} unreliable rows.")
if "exclude_training_row"  in df.columns: df = df[df["exclude_training_row"] == 0].reset_index(drop=True)
if "exclude_target_plus1"  in df.columns: df = df[df["exclude_target_plus1"] == 0].reset_index(drop=True)

# 2. Load ensemble
print("\n" + "=" * 60)
print("STEP 2 — Load frozen ensemble")
print("=" * 60)
artifact = joblib.load(ENSEMBLE_PATH)
print(f"Kind: {artifact['kind']}")
print(f"Weights: {artifact['weights']}")
print(f"Threshold: {artifact['threshold']}")

# 3. Refit Poisson scaler
print("\n" + "=" * 60)
print("STEP 3 — Refit Poisson StandardScaler")
print("=" * 60)
poisson_bundle    = artifact["bundles"]["poisson"]
poisson_feat_cols = poisson_bundle["feature_columns"]
poisson_imputer   = poisson_bundle["artifact"][0]
missing           = [c for c in poisson_feat_cols if c not in df.columns]
print(f"Poisson features: {len(poisson_feat_cols)}, missing: {missing}")

train_df        = df[df["year"] <= 2021]
X_p_train       = train_df.reindex(columns=poisson_feat_cols, fill_value=0.0)
X_p_train_imp   = poisson_imputer.transform(X_p_train)
poisson_scaler  = StandardScaler().fit(X_p_train_imp)
print(f"Fitted on {len(X_p_train_imp)} rows.")
if "worldpop_total" in poisson_feat_cols:
    idx = poisson_feat_cols.index("worldpop_total")
    print(f"worldpop_total -> mean={poisson_scaler.mean_[idx]:.0f}, scale={poisson_scaler.scale_[idx]:.0f}")

# 4. Build wrapper + merged features
wrapper = WeightedEnsembleWrapper(artifact, poisson_scaler=poisson_scaler)
seen, merged_features = set(), []
for name in artifact["model_keys"]:
    for col in artifact["bundles"][name]["feature_columns"]:
        if col not in seen:
            merged_features.append(col); seen.add(col)
print(f"\nMerged feature list: {len(merged_features)} columns")

# 5. Calibration split
print("\n" + "=" * 60)
print("STEP 5 — Calibration split (year == 2022)")
print("=" * 60)
df_val = df[df["year"] == VAL_YEAR].dropna(subset=[TARGET]).reset_index(drop=True)
X_val  = df_val.copy()
y_val  = df_val[TARGET].astype(int).values
print(f"Cal rows: {len(X_val)}  |  outbreaks: {y_val.sum()}")
if len(X_val) < 50:
    sys.exit("ERROR: Too few calibration rows.")

# 6. Sanity check
test_p = wrapper.predict_proba(X_val.head(5))
print(f"\nSanity check probabilities: {test_p[:, 1]}")
if np.any(~np.isfinite(test_p)):
    sys.exit("ERROR: Non-finite values in wrapper output!")

# 7. Compute calibration proba and scores
print("\n" + "=" * 60)
print("STEP 7 — Calibration probabilities + conformal scores")
print("=" * 60)

p_val  = wrapper.predict_proba(X_val)[:, 1]
print(f"Ensemble: min={p_val.min():.3f} median={np.median(p_val):.3f} max={p_val.max():.3f}")

# Standard split-conformal score: |predicted_prob - true_label|
scores = np.abs(p_val - y_val.astype(float))
print(f"Non-conformity scores: min={scores.min():.4f} median={np.median(scores):.4f} max={scores.max():.4f}")

n_cal = len(scores)
level = np.ceil((n_cal + 1) * (1 - ALPHA)) / n_cal
q_hat = float(np.quantile(scores, min(level, 1.0)))

print(f"\nn_cal={n_cal}, adjusted_level={level:.4f}")
print(f"q_hat = {q_hat:.4f}  ({q_hat*100:.1f}pp half-width)")

# 8. Coverage
lower_val = np.clip(p_val - q_hat, 0, 1)
upper_val = np.clip(p_val + q_hat, 0, 1)
covered   = float(((y_val >= lower_val) & (y_val <= upper_val)).mean())
print(f"\nEmpirical coverage: {covered:.2%}  (target: {(1-ALPHA):.0%})")

# Example intervals at interesting risk thresholds
print("\nExample prediction intervals:")
for ex in [0.10, 0.175, 0.30, 0.50, 0.70]:
    lo = max(0, ex - q_hat)
    hi = min(1, ex + q_hat)
    label = "OUTBREAK" if ex >= artifact["threshold"] else "low-risk"
    print(f"  p={ex:.3f} ({label}) -> [{lo*100:.1f}%, {hi*100:.1f}%]  width={min(hi-lo,1)*100:.1f}pp")

# 9. Save
print("\n" + "=" * 60)
print("STEP 9 — Save artifact")
print("=" * 60)
mapie_artifact = {
    "ensemble":        artifact,
    "poisson_scaler":  poisson_scaler,
    "q_hat":           q_hat,
    "alpha":           ALPHA,
    "confidence":      1 - ALPHA,
    "n_cal":           n_cal,
    "cal_coverage":    covered,
    "threshold":       artifact["threshold"],
    "feature_columns": merged_features,
    "val_year":        VAL_YEAR,
    "score_method":    "abs_error_vs_binary_label",
}
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
joblib.dump(mapie_artifact, OUT_PATH, compress=3)
print(f"Saved -> {OUT_PATH}")
print(f"\nDone.  q_hat={q_hat:.4f}  coverage={covered:.2%}")
