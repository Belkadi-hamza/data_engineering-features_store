from pymongo import MongoClient

# ==========================================
# MongoDB Configuration
# ==========================================

MONGO_URI = "mongodb://localhost:27017"

DATABASE_NAME = "bank_feature_store"

COLLECTION_NAME = "customer_features"

# ==========================================
# Connection
# ==========================================

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]