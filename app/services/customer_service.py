from app.database import collection


def get_customer(client_id: int):

    customer = collection.find_one(
        {"CLIENTNUM": client_id},
        {"_id": 0},
    )

    return customer