from pathlib import Path
from feast import FeatureStore

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_PATH = PROJECT_ROOT / "feature_repo" / "feature_repo"

store = FeatureStore(repo_path=str(REPO_PATH))

client_id = 768805383

result = store.get_online_features(
    features=[
        "customer_features:Customer_Age",
        "customer_features:Dependent_count",
        "customer_features:Credit_Limit",
        "customer_features:Total_Trans_Amt",
        "customer_features:Avg_Utilization_Ratio",
    ],
    entity_rows=[
        {
            "CLIENTNUM": client_id
        }
    ],
).to_dict()

print(result)