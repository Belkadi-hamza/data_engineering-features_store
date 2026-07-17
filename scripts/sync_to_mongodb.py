from pathlib import Path

import pandas as pd
from config.features import MODEL_FEATURES
from feast import FeatureStore
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_PATH = PROJECT_ROOT / "feature_repo" / "feature_repo"

store = FeatureStore(repo_path=str(REPO_PATH))

# Lire le fichier historique
df = pd.read_parquet(
    PROJECT_ROOT / "feature_repo" / "feature_repo" / "data" / "customers.parquet"
)

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017")

db = client["bank_feature_store"]

collection = db["customer_features"]

collection.delete_many({})

# Colonnes utilisées
features = ["CLIENTNUM"] + MODEL_FEATURES

documents = df[features].to_dict("records")

collection.insert_many(documents)

print("=" * 50)
print(f"{len(documents)} documents synchronisés.")
print("=" * 50)