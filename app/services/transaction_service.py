import random

from app.database import collection


def update_transaction(client_id: int, amount: float):

    customer = collection.find_one({"CLIENTNUM": client_id})

    if customer is None:
        return None

    customer["Total_Trans_Amt"] += amount
    customer["Total_Trans_Ct"] += 1

    customer["Avg_Utilization_Ratio"] = round(
        random.uniform(0.02, 0.99),
        3,
    )

    collection.update_one(
        {"CLIENTNUM": client_id},
        {
            "$set": {
                "Total_Trans_Amt": customer["Total_Trans_Amt"],
                "Total_Trans_Ct": customer["Total_Trans_Ct"],
                "Avg_Utilization_Ratio": customer["Avg_Utilization_Ratio"],
            }
        },
    )

    return collection.find_one(
        {"CLIENTNUM": client_id},
        {"_id": 0},
    )


def simulate_transactions(client_id: int, n: int):

    customer = collection.find_one({"CLIENTNUM": client_id})

    if customer is None:
        return None

    history = []

    for i in range(n):

        amount = random.randint(20, 800)

        customer["Total_Trans_Amt"] += amount
        customer["Total_Trans_Ct"] += 1

        utilization = round(
            random.uniform(0.02, 0.99),
            3,
        )

        customer["Avg_Utilization_Ratio"] = utilization

        history.append(
            {
                "transaction": i + 1,
                "amount": amount,
                "total_amount": customer["Total_Trans_Amt"],
                "total_transactions": customer["Total_Trans_Ct"],
                "utilization": utilization,
            }
        )

    collection.update_one(
        {"CLIENTNUM": client_id},
        {
            "$set": {
                "Total_Trans_Amt": customer["Total_Trans_Amt"],
                "Total_Trans_Ct": customer["Total_Trans_Ct"],
                "Avg_Utilization_Ratio": customer["Avg_Utilization_Ratio"],
            }
        },
    )

    return {
        "client_id": client_id,
        "transactions": history,
        "customer": collection.find_one(
            {"CLIENTNUM": client_id},
            {"_id": 0},
        ),
    }