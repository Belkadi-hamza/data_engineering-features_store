from fastapi import APIRouter

from app.services.sync_service import sync_mongodb

router = APIRouter(
    prefix="/sync",
    tags=["Synchronization"],
)


@router.post("/")
def sync():

    return sync_mongodb()