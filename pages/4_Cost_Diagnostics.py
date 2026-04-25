import streamlit as st
import pandas as pd
import plotly.express as px

from data_processing import (
    load_data,
    calculate_metrics,
    cost_structure_analysis,
    apply_filters
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

st.title("💰 Cost vs Margin Diagnostics Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data("master.csv")
df = calculate_metrics(df)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

margin_threshold = st.sidebar.slider(
    "Minimum Margin (%)",
    0, 100, 0
)

product_search = st.sidebar.text_input("Search Product")

# Apply filters
filtered_df = apply_filters(
    df,
    division=division,
    margin_threshold=margin_threshold,
    product_search=product_search
)

# -----------------------------
# COST ANALYSIS
# -----------------------------
cost_df = cost_structure_analysis(filtered_df)

# -----------------------------
# SCATTER: COST vs SALES
# -----------------------------
st.subheader("📊 Cost vs Sales Analysis")

fig1 = px.scatter(
    cost_df,
    x="Cost",
    y="Sales",
    size="Profit",
    color="Cost Heavy",
    hover_data=["Product Name"],
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# PRICING ISSUE PRODUCTS
# -----------------------------
st.subheader("⚠️ Pricing Inefficiency (High Sales but Low Profit)")

pricing_issue = cost_df[cost_df["Pricing Issue"] == True]

st.dataframe(pricing_issue)

st.markdown("---")

# -----------------------------
# COST HEAVY PRODUCTS
# -----------------------------
st.subheader("🚨 Cost Heavy Products")

cost_heavy = cost_df[cost_df["Cost Heavy"] == True]

st.dataframe(cost_heavy)

st.markdown("---")

# -----------------------------
# DISCONTINUE SUGGESTION
# -----------------------------
st.subheader("❌ Products for Discontinuation Review")

discontinue = cost_df[cost_df["Discontinue Review"] == True]

st.dataframe(discontinue)
