from fastapi import APIRouter, HTTPException

from app.schemas.transaction import (
    Transaction,
    TransactionSimulation,
)

from app.services.transaction_service import (
    update_transaction,
    simulate_transactions,
)

router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
)


@router.post("/")
def transaction(data: Transaction):

    customer = update_transaction(
        data.client_id,
        data.amount,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Client introuvable",
        )

    return customer


@router.post("/simulate")
def simulate(data: TransactionSimulation):

    result = simulate_transactions(
        data.client_id,
        data.number_of_transactions,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Client introuvable",
        )

    return result