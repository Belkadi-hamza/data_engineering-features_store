from pathlib import Path
import joblib
import pandas as pd
from config.features import MODEL_FEATURES
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# -----------------------------
# Charger le modèle
# -----------------------------
model = joblib.load(
    PROJECT_ROOT / "models" / "churn_model.pkl"
)

# -----------------------------
# Connexion MongoDB
# -----------------------------
client = MongoClient("mongodb://localhost:27017")

db = client["bank_feature_store"]

collection = db["customer_features"]

CLIENT_ID = 768805383

customer = collection.find_one(
    {"CLIENTNUM": CLIENT_ID},
    {"_id": 0}
)

print("=" * 50)
print("Features utilisées :")
print(customer)

# -----------------------------
# Construire DataFrame
# -----------------------------
feature_columns = MODEL_FEATURES

X = pd.DataFrame([{col: customer[col] for col in feature_columns}])
# -----------------------------
# Prédiction
# -----------------------------
prediction = model.predict(X)[0]

probability = model.predict_proba(X)[0]

print("\n")

print("=" * 50)

print("Résultat")

print("=" * 50)

print(f"Classe prédite : {prediction}")

print(
    f"Probabilité churn : {probability[1]*100:.2f}%"
)

if prediction == 1:
    print("\n⚠️ Client à risque de départ")
else:
    print("\n✅ Client fidèle")