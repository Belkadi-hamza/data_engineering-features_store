from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017")

db = client["bank_feature_store"]
collection = db["customer_features"]

CLIENT_ID = 768805383

customer = collection.find_one({"CLIENTNUM": CLIENT_ID})

if customer is None:
    print("Client introuvable.")
    exit()

print("=" * 60)
print("Avant mise à jour")
print(customer)

new_amount = random.randint(100, 1000)

collection.update_one(
    {"CLIENTNUM": CLIENT_ID},
    {
        "$inc": {
            "Total_Trans_Amt": new_amount,
            "Total_Trans_Ct": 1,
        },
        "$set": {
            "Avg_Utilization_Ratio": round(random.uniform(0.05, 0.95), 3)
        },
    },
)

print("\nNouvelle transaction :", new_amount)

updated = collection.find_one({"CLIENTNUM": CLIENT_ID})

print("\nAprès mise à jour")
print(updated)
print("=" * 60)