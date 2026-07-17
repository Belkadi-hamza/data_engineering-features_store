from pathlib import Path
import joblib
import pandas as pd

from config.features import MODEL_FEATURES
from feast import FeatureStore

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# ==========================================
# Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPO_PATH = PROJECT_ROOT / "feature_repo" / "feature_repo"

DATA_PATH = REPO_PATH / "data" / "customers.parquet"

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "churn_model.pkl"

# ==========================================
# Load Feast
# ==========================================

store = FeatureStore(repo_path=str(REPO_PATH))

# ==========================================
# Load original dataset
# ==========================================

df = pd.read_parquet(DATA_PATH)

# Entity dataframe required by Feast
entity_df = df[["CLIENTNUM", "event_timestamp"]]

# ==========================================
# Retrieve historical features from Feast
# ==========================================

training_df = (
    store.get_historical_features(
        entity_df=entity_df,
        features=[f"customer_features:{feature}" for feature in MODEL_FEATURES],
    )
    .to_df()
)

# ==========================================
# Add target
# ==========================================

training_df["Attrition_Flag"] = df["Attrition_Flag"].values

# ==========================================
# Features / Label
# ==========================================

X = training_df.drop(
    columns=[
        "CLIENTNUM",
        "event_timestamp",
        "Attrition_Flag",
    ]
)

y = training_df["Attrition_Flag"]

# ==========================================
# Train / Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# ==========================================
# Train model
# ==========================================

model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
)

model.fit(X_train, y_train)

# ==========================================
# Evaluation
# ==========================================

pred = model.predict(X_test)

print("=" * 50)
print("Accuracy :", accuracy_score(y_test, pred))
print("=" * 50)

print(classification_report(y_test, pred))

print(confusion_matrix(y_test, pred))

# ==========================================
# Save model
# ==========================================

joblib.dump(model, MODEL_PATH)

print("\nModel saved to")
print(MODEL_PATH)