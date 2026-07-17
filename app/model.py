from pathlib import Path

import joblib

# ==========================================
# Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.pkl"

# ==========================================
# Load model
# ==========================================

model = joblib.load(MODEL_PATH)