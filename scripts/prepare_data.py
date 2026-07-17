from pathlib import Path
from datetime import datetime
import pandas as pd

# ==============================
# Paths
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
parquet_dir = PROJECT_ROOT / "feature_repo" / "feature_repo" / "data"

INPUT_FILE = DATA_DIR / "BankChurners.csv"
OUTPUT_FILE = parquet_dir / "customers.parquet"

# ==============================
# Load data
# ==============================

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Shape : {df.shape}")

# ==============================
# Remove duplicates
# ==============================

df = df.drop_duplicates(subset=["CLIENTNUM"])

# ==============================
# Missing values
# ==============================

print("\nMissing values")

print(df.isnull().sum())

# ==============================
# Target encoding
# ==============================

df["Attrition_Flag"] = (
    df["Attrition_Flag"]
    .map({
        "Existing Customer": 0,
        "Attrited Customer": 1
    })
    .astype("int8")
)

# ==============================
# Convert categorical columns
# ==============================

categorical_columns = [
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
]

for col in categorical_columns:
    df[col] = df[col].astype("category")

# ==============================
# Timestamp required by Feast
# ==============================

current_time = pd.Timestamp.utcnow().floor("s")

df["event_timestamp"] = current_time

df["created_timestamp"] = current_time

# ==============================
# Sort by entity id
# ==============================

df = df.sort_values("CLIENTNUM")

# ==============================
# Save parquet
# ==============================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_parquet(
    OUTPUT_FILE,
    index=False,
    engine="pyarrow"
)

# ==============================
# Summary
# ==============================

print("\nDataset prepared successfully")

print(f"Rows      : {len(df)}")
print(f"Columns   : {len(df.columns)}")
print(f"Saved to  : {OUTPUT_FILE}")

print("\nDtypes")

print(df.dtypes)