import streamlit as st
import pandas as pd

def render_header():
    st.title("📊 Customer Engagement & Product Utilization Analytics")
    st.caption(
        "Customer retention, engagement, product adoption and premium risk analysis"
    )

def render_kpis(kpis):
    columns = st.columns(4)

    metrics = [
        ("Total Customers", f'{kpis["total_customers"]:,}'),
        ("Retention Rate", f'{kpis["retention_rate"]:.2f}%'),
        ("Churn Rate", f'{kpis["churn_rate"]:.2f}%'),
        ("Product Depth Index", f'{kpis["product_depth_index"]:.2f}')
    ]

    for col, (label, value) in zip(columns, metrics):
        col.metric(label, value)

    columns = st.columns(4)

    metrics = [
        ("Active Customers", f'{kpis["active_customers"]:,}'),
        ("Inactive Customers", f'{kpis["inactive_customers"]:,}'),
        ("High-Balance Disengagement", f'{kpis["high_balance_disengagement_rate"]:.2f}%'),
        ("Relationship Strength", f'{kpis["average_relationship_strength"]:.2f}')
    ]

    for col, (label, value) in zip(columns, metrics):
        col.metric(label, value)

def apply_filters(df):
    st.sidebar.header("Common Dashboard Filters")

    result = df.copy()

    if "geography" in result.columns:
        options = sorted(result["geography"].dropna().astype(str).unique())
        selected = st.sidebar.multiselect(
            "Geography", options, default=options
        )
        result = result[result["geography"].astype(str).isin(selected)]

    if "gender" in result.columns:
        options = sorted(result["gender"].dropna().astype(str).unique())
        selected = st.sidebar.multiselect(
            "Gender", options, default=options
        )
        result = result[result["gender"].astype(str).isin(selected)]

    activity_options = ["Active", "Inactive"]
    selected_activity = st.sidebar.multiselect(
        "Activity Status", activity_options, default=activity_options
    )
    result = result[
        result["activity_status"].isin(selected_activity)
    ]

    status_options = ["Retained", "Exited"]
    selected_status = st.sidebar.multiselect(
        "Customer Status", status_options, default=status_options
    )
    result = result[
        result["customer_status"].isin(selected_status)
    ]

    product_options = sorted(
        result["product_count_category"].dropna().unique().tolist()
    )
    selected_products = st.sidebar.multiselect(
        "Product Category", product_options, default=product_options
    )
    result = result[
        result["product_count_category"].isin(selected_products)
    ]

    if "age" in result.columns and result["age"].notna().any():
        minimum = int(result["age"].min())
        maximum = int(result["age"].max())

        if minimum < maximum:
            age_range = st.sidebar.slider(
                "Age Range",
                minimum,
                maximum,
                (minimum, maximum)
            )
            result = result[
                result["age"].between(age_range[0], age_range[1])
            ]

    return result

def render_customer_table(df):
    st.subheader("Customer Records")

    search = st.text_input(
        "Search customer by ID or surname",
        key="customer_search"
    )

    filtered = df.copy()

    if search.strip():
        mask = filtered["customer_id"].astype(str).str.contains(
            search, case=False, na=False
        )

        if "surname" in filtered.columns:
            mask |= filtered["surname"].astype(str).str.contains(
                search, case=False, na=False
            )

        filtered = filtered[mask]

    st.write(f"Matching customers: {len(filtered):,}")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download filtered customers as CSV",
        data=csv,
        file_name="filtered_customer_data.csv",
        mime="text/csv"
    )
