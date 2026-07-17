from pydantic import BaseModel


class Transaction(BaseModel):
    client_id: int
    amount: float


class TransactionSimulation(BaseModel):
    client_id: int
    number_of_transactions: int