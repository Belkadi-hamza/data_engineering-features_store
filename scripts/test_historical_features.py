from pathlib import Path
import pandas as pd

from feast import FeatureStore

# ==========================================
# Load Feature Store
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPO_PATH = PROJECT_ROOT / "feature_repo" / "feature_repo"

store = FeatureStore(repo_path=str(REPO_PATH))

# ==========================================
# Entity DataFrame
# ==========================================

entity_df = pd.DataFrame(
    {
        "CLIENTNUM": [
            768805383,
            713982108,
            709106358,
            711156558,
            788134008,
        ],

        "event_timestamp": pd.Timestamp.utcnow(),
    }
)

# ==========================================
# Retrieve historical features
# ==========================================

training_df = (
    store
    .get_historical_features(
        entity_df=entity_df,

        features=[
            "customer_features:Customer_Age",
            "customer_features:Credit_Limit",
            "customer_features:Total_Trans_Amt",
            "customer_features:Total_Trans_Ct",
            "customer_features:Avg_Utilization_Ratio",
        ],
    )
    .to_df()
)

print(training_df)