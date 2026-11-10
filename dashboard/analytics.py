import pandas as pd
import numpy as np

def safe_rate(numerator, denominator):
    return (
        float(numerator) / float(denominator) * 100
        if denominator else 0.0
    )

def calculate_kpis(df):
    total = len(df)

    retained = int((df["exited"] == 0).sum())
    exited = int((df["exited"] == 1).sum())

    active = df[df["active"] == 1]
    inactive = df[df["active"] == 0]

    active_retention = safe_rate(
        (active["exited"] == 0).sum(), len(active)
    )

    inactive_retention = safe_rate(
        (inactive["exited"] == 0).sum(), len(inactive)
    )

    engagement_ratio = (
        active_retention / inactive_retention
        if inactive_retention else 0
    )

    product_depth = (
        df["products"].sum() / total if total else 0
    )

    high_balance = df[df["high_balance_flag"] == 1]

    high_balance_disengagement = safe_rate(
        high_balance["inactive_high_balance_flag"].sum(),
        len(high_balance)
    )

    if "card" in df.columns:
        cardholders = df[df["card"] == 1]
        non_cardholders = df[df["card"] == 0]

        card_retention = safe_rate(
            (cardholders["exited"] == 0).sum(), len(cardholders)
        )

        non_card_retention = safe_rate(
            (non_cardholders["exited"] == 0).sum(),
            len(non_cardholders)
        )

        card_stickiness = card_retention - non_card_retention
    else:
        card_stickiness = 0

    return {
        "total_customers": total,
        "retained_customers": retained,
        "exited_customers": exited,
        "retention_rate": safe_rate(retained, total),
        "churn_rate": safe_rate(exited, total),
        "active_customers": len(active),
        "inactive_customers": len(inactive),
        "engagement_retention_ratio": engagement_ratio,
        "product_depth_index": product_depth,
        "high_balance_disengagement_rate": high_balance_disengagement,
        "credit_card_stickiness_score": card_stickiness,
        "average_relationship_strength": (
            df["relationship_strength_index"].mean()
            if total else 0
        )
    }

def group_churn(df, column):
    if column not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby(column, observed=False)
        .agg(
            customers=("exited", "size"),
            exited=("exited", "sum"),
            average_products=("products", "mean")
        )
        .reset_index()
    )

    result["churn_rate"] = (
        result["exited"] / result["customers"] * 100
    )

    return result

def validate_kpis(df, kpis):
    checks = {
        "Total customers": kpis["total_customers"] == len(df),
        "Retained + exited": (
            kpis["retained_customers"] + kpis["exited_customers"]
            == len(df)
        ),
        "Active + inactive": (
            kpis["active_customers"] + kpis["inactive_customers"]
            == len(df)
        ),
        "Product depth": np.isclose(
            kpis["product_depth_index"],
            df["products"].sum() / len(df) if len(df) else 0
        )
    }

    return checks
