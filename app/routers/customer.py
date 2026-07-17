from fastapi import APIRouter, HTTPException

from app.services.customer_service import get_customer

router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)


@router.get("/{client_id}")
def customer(client_id: int):

    customer = get_customer(client_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Client introuvable",
        )

    return customer