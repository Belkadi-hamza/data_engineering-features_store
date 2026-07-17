from fastapi import APIRouter, HTTPException

from app.services.prediction_service import predict_customer

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)


@router.post("/{client_id}")
def predict(client_id: int):

    result = predict_customer(client_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Client introuvable",
        )

    return result