import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import APP_TITLE, APP_ICON, LAYOUT
from data_loader import load_data
from analytics import calculate_kpis, group_churn, validate_kpis
from components import (
    render_header, render_kpis, apply_filters,
    render_customer_table
)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT
)

df = load_data()

render_header()

st.sidebar.title("Dashboard Navigation")

pages = [
    "Executive Overview",
    "Engagement Analytics",
    "Product Adoption Analytics",
    "Premium Customer Risk Detector",
    "Retention Strength Analytics",
    "Customer Explorer"
]

selected_page = st.sidebar.radio("Select Dashboard Page", pages)

filtered_df = apply_filters(df)

st.sidebar.divider()
st.sidebar.metric("Filtered Customers", f"{len(filtered_df):,}")

if filtered_df.empty:
    st.warning(
        "No customers match the selected filters. "
        "Please change or reset your filters."
    )
    st.stop()

kpis = calculate_kpis(filtered_df)

if selected_page == "Executive Overview":
    st.header("Executive Overview")
    render_kpis(kpis)

    col1, col2 = st.columns(2)

    with col1:
        status = filtered_df["customer_status"].value_counts().reset_index()
        status.columns = ["Customer Status", "Customers"]

        fig = px.pie(
            status,
            names="Customer Status",
            values="Customers",
            title="Customer Retention Distribution",
            hole=0.45
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        activity = filtered_df.groupby(
            "activity_status"
        )["exited"].mean().mul(100).reset_index()

        activity.columns = ["Activity Status", "Churn Rate"]

        fig = px.bar(
            activity,
            x="Activity Status",
            y="Churn Rate",
            title="Churn Rate by Activity Status",
            text_auto=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)

    geography = group_churn(filtered_df, "geography")

    if not geography.empty:
        st.subheader("Geographical Retention Overview")
        fig = px.bar(
            geography,
            x="geography",
            y="churn_rate",
            color="customers",
            title="Geographical Churn Rate",
            text_auto=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Engagement Analytics":
    st.header("Engagement Analytics")
    render_kpis(kpis)

    engagement = group_churn(filtered_df, "activity_status")

    fig = px.bar(
        engagement,
        x="activity_status",
        y="churn_rate",
        color="customers",
        title="Churn Rate by Engagement Status",
        text_auto=".2f"
    )
    st.plotly_chart(fig, use_container_width=True)

    if "age_group" in filtered_df.columns:
        age_data = group_churn(filtered_df, "age_group")

        fig = px.bar(
            age_data,
            x="age_group",
            y="churn_rate",
            title="Churn Rate by Age Group",
            text_auto=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)

    if "tenure" in filtered_df.columns:
        fig = px.histogram(
            filtered_df,
            x="tenure",
            color="activity_status",
            title="Customer Tenure and Engagement",
            barmode="overlay"
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Product Adoption Analytics":
    st.header("Product Adoption Analytics")
    render_kpis(kpis)

    product_data = group_churn(
        filtered_df, "product_count_category"
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            product_data,
            x="product_count_category",
            y="customers",
            title="Customer Distribution by Product Count",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            product_data,
            x="product_count_category",
            y="churn_rate",
            title="Churn Rate by Product Category",
            text_auto=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        filtered_df,
        x="product_count_category",
        y="relationship_strength_index",
        color="product_count_category",
        title="Relationship Strength by Product Adoption"
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Premium Customer Risk Detector":
    st.header("Premium Customer Risk Detector")

    premium = filtered_df[
        filtered_df["high_balance_flag"] == 1
    ]

    st.metric("High-Balance Customers", f"{len(premium):,}")

    risk_counts = (
        filtered_df["premium_risk_segment"]
        .value_counts().reset_index()
    )
    risk_counts.columns = ["Risk Segment", "Customers"]

    fig = px.bar(
        risk_counts,
        x="Risk Segment",
        y="Customers",
        color="Risk Segment",
        title="Premium Customer Risk Segments",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

    critical = filtered_df[
        filtered_df["premium_risk_segment"].isin([
            "Critical Attention - Inactive Single Product",
            "High Attention - Inactive Multi Product"
        ])
        & (filtered_df["exited"] == 0)
    ]

    st.subheader("Retained Customers Requiring Attention")
    st.dataframe(critical, use_container_width=True, hide_index=True)

    st.download_button(
        "Export Premium Risk Customers",
        critical.to_csv(index=False).encode("utf-8"),
        "premium_customer_risk.csv",
        "text/csv"
    )

elif selected_page == "Retention Strength Analytics":
    st.header("Retention Strength Analytics")
    render_kpis(kpis)

    strength = (
        filtered_df["relationship_strength_category"]
        .value_counts().reset_index()
    )
    strength.columns = ["Strength Category", "Customers"]

    fig = px.pie(
        strength,
        names="Strength Category",
        values="Customers",
        title="Relationship Strength Distribution",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        filtered_df,
        x="relationship_strength_index",
        color="customer_status",
        nbins=20,
        title="Relationship Strength and Customer Status"
    )
    st.plotly_chart(fig, use_container_width=True)

    strength_churn = group_churn(
        filtered_df, "relationship_strength_category"
    )

    fig = px.bar(
        strength_churn,
        x="relationship_strength_category",
        y="churn_rate",
        title="Churn Rate by Relationship Strength",
        text_auto=".2f"
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Customer Explorer":
    st.header("Customer Explorer")
    render_kpis(kpis)
    render_customer_table(filtered_df)

st.divider()

with st.expander("KPI Definitions and Validation"):
    st.write(
        "**Engagement Retention Ratio:** Active customer retention rate "
        "divided by inactive customer retention rate."
    )
    st.write(
        "**Product Depth Index:** Average number of products per customer."
    )
    st.write(
        "**High-Balance Disengagement Rate:** Inactive high-balance "
        "customers divided by all high-balance customers."
    )
    st.write(
        "**Credit Card Stickiness Score:** Cardholder retention rate "
        "minus non-cardholder retention rate, in percentage points."
    )
    st.write(
        "**Relationship Strength Index:** 60% activity score and "
        "40% product adoption score, on a 0–100 scale."
    )

    checks = validate_kpis(filtered_df, kpis)

    for name, passed in checks.items():
        if passed:
            st.success(f"{name}: Passed")
        else:
            st.error(f"{name}: Failed")

st.caption(
    "Analytical dashboard based on historical customer data. "
    "Associations do not establish causation or predict future churn."
)
