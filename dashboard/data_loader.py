import pandas as pd
import numpy as np
import streamlit as st
from config import DATASET_PATH

ALIASES = {
    "customer_id": ["CustomerId", "CustomerID", "customer_id", "Customer Id"],
    "geography": ["Geography", "geography", "Country"],
    "gender": ["Gender", "gender"],
    "age": ["Age", "age"],
    "tenure": ["Tenure", "tenure"],
    "balance": ["Balance", "balance"],
    "products": ["NumOfProducts", "NumberOfProducts", "num_products"],
    "active": ["IsActiveMember", "ActiveMember", "is_active_member"],
    "card": ["HasCrCard", "HasCreditCard", "has_credit_card"],
    "exited": ["Exited", "Churn", "churn", "CustomerExited"],
    "credit_score": ["CreditScore", "credit_score"],
    "salary": ["EstimatedSalary", "Salary", "estimated_salary"],
    "surname": ["Surname", "surname"]
}

def find_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None

@st.cache_data
def load_data():
    df = pd.read_csv(DATASET_PATH)

    for standard, candidates in ALIASES.items():
        found = find_column(df, candidates)
        if found and found != standard:
            df[standard] = df[found]

    numeric_columns = [
        "age", "tenure", "balance", "products", "active",
        "card", "exited", "credit_score", "salary"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "customer_id" not in df.columns:
        df["customer_id"] = np.arange(1, len(df) + 1)

    if "active" not in df.columns and "activity_status" in df.columns:
        df["active"] = (
            df["activity_status"].astype(str).str.lower()
            .map({"active": 1, "inactive": 0})
        )

    if "products" not in df.columns:
        df["products"] = 0

    if "active" not in df.columns:
        df["active"] = 0

    if "exited" not in df.columns:
        df["exited"] = 0

    if "balance" not in df.columns:
        df["balance"] = 0

    df["products"] = df["products"].fillna(0)
    df["active"] = df["active"].fillna(0)
    df["exited"] = df["exited"].fillna(0)
    df["balance"] = df["balance"].fillna(0)

    df["active"] = df["active"].clip(0, 1)
    df["exited"] = df["exited"].clip(0, 1)

    df["activity_status"] = np.where(
        df["active"] == 1, "Active", "Inactive"
    )

    df["customer_status"] = np.where(
        df["exited"] == 1, "Exited", "Retained"
    )

    df["product_count_category"] = np.select(
        [
            df["products"] <= 1,
            df["products"] == 2,
            df["products"] >= 3
        ],
        ["Single Product", "Two Products", "Three or More Products"],
        default="Unknown"
    )

    if "age" in df.columns:
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 25, 35, 45, 55, 100],
            labels=["18-25", "26-35", "36-45", "46-55", "56+"]
        )

    if "geography" not in df.columns:
        df["geography"] = "Unknown"

    if "gender" not in df.columns:
        df["gender"] = "Unknown"

    positive_balances = df.loc[df["balance"] > 0, "balance"]

    if len(positive_balances):
        threshold = positive_balances.quantile(0.75)
    else:
        threshold = 0

    df["high_balance_flag"] = (
        (df["balance"] >= threshold) & (df["balance"] > 0)
    ).astype(int)

    df["inactive_high_balance_flag"] = (
        (df["active"] == 0) & (df["high_balance_flag"] == 1)
    ).astype(int)

    df["relationship_strength_index"] = (
        60 * df["active"]
        + 40 * np.minimum(df["products"], 2) / 2
    )

    df["relationship_strength_category"] = pd.cut(
        df["relationship_strength_index"],
        bins=[-1, 24, 49, 74, 89, 100],
        labels=[
            "Very Weak", "Weak", "Moderate",
            "Strong", "Very Strong"
        ]
    )

    df["premium_customer_candidate"] = (
        (df["high_balance_flag"] == 1)
        & (df["products"] >= 2)
    ).astype(int)

    df["premium_risk_segment"] = np.select(
        [
            (df["active"] == 0) & (df["products"] <= 1)
            & (df["exited"] == 0),

            (df["active"] == 0) & (df["products"] >= 2)
            & (df["exited"] == 0),

            (df["active"] == 1) & (df["high_balance_flag"] == 1),

            (df["exited"] == 1) & (df["high_balance_flag"] == 1)
        ],
        [
            "Critical Attention - Inactive Single Product",
            "High Attention - Inactive Multi Product",
            "Monitor - Active High Balance",
            "Historical Churn - Exited High Balance"
        ],
        default="Standard Segment"
    )

    return df
