from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import collection
from app.model import model

from app.routers.customer import router as customer_router
from app.routers.transaction import router as transaction_router
from app.routers.prediction import router as prediction_router
from app.routers.sync import router as sync_router

PROJECT_ROOT = Path(__file__).resolve().parent

app = FastAPI(
    title="Bank Feature Store API",
    version="1.0.0",
    description="Feature Store + MongoDB + Machine Learning API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(customer_router)
app.include_router(transaction_router)
app.include_router(prediction_router)
app.include_router(sync_router)


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "OK",
        "mongodb_documents": collection.count_documents({}),
        "model_loaded": model is not None,
    }

# uvicorn app.main:app --reload