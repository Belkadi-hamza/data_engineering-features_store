import pandas as pd

from app.model import model
from app.services.customer_service import get_customer

from config.features import MODEL_FEATURES


def predict_customer(client_id: int):

    customer = get_customer(client_id)

    if customer is None:
        return None

    X = pd.DataFrame(
        [[customer[col] for col in MODEL_FEATURES]],
        columns=MODEL_FEATURES,
    )

    prediction = int(
        model.predict(X)[0]
    )

    probability = float(
        model.predict_proba(X)[0][1]
    )

    return {
        "client_id": client_id,
        "prediction": prediction,
        "probability": round(probability * 100, 2),
        "label": (
            "Attrited Customer"
            if prediction == 1
            else "Existing Customer"
        ),
    }