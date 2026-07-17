from datetime import timedelta

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    Project,
)

from feast.types import Float32, Int64

# --------------------------------------------------
# Project
# --------------------------------------------------

project = Project(
    name="bank_feature_store",
    description="Bank Customer Churn Feature Store",
)

# --------------------------------------------------
# Entity
# --------------------------------------------------

customer = Entity(
    name="customer",
    join_keys=["CLIENTNUM"],
)

# --------------------------------------------------
# Offline Source
# --------------------------------------------------

customer_source = FileSource(
    name="customer_source",
    path="data/customers.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# --------------------------------------------------
# Feature View
# --------------------------------------------------

customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    ttl=timedelta(days=365),

    schema=[
        Field(name="Customer_Age", dtype=Int64),
        Field(name="Dependent_count", dtype=Int64),
        Field(name="Months_on_book", dtype=Int64),
        Field(name="Total_Relationship_Count", dtype=Int64),
        Field(name="Months_Inactive_12_mon", dtype=Int64),
        Field(name="Contacts_Count_12_mon", dtype=Int64),

        Field(name="Credit_Limit", dtype=Float32),
        Field(name="Avg_Open_To_Buy", dtype=Float32),

        Field(name="Total_Revolving_Bal", dtype=Int64),

        Field(name="Total_Amt_Chng_Q4_Q1", dtype=Float32),

        Field(name="Total_Trans_Amt", dtype=Int64),
        Field(name="Total_Trans_Ct", dtype=Int64),

        Field(name="Total_Ct_Chng_Q4_Q1", dtype=Float32),

        Field(name="Avg_Utilization_Ratio", dtype=Float32),
    ],

    source=customer_source,

    online=True,
)

# --------------------------------------------------
# Feature Service
# --------------------------------------------------

customer_service = FeatureService(
    name="customer_service",
    features=[customer_features],
)