import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
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
df = load_data("Nassau.csv")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=list(df["Division"].unique())
)

margin_threshold = st.sidebar.slider(
    "Minimum Margin (%)",
    0, 100, 0
) / 100

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
    size_max=40,
    color="Cost Heavy",
    color_discrete_map={True: "#ff4b4b", False: "#4b9eff"},
    hover_data=["Product Name", "Cost Ratio", "Profit"],
    template="plotly_dark",
    labels={
        "Cost": "Total Cost ($)",
        "Sales": "Total Sales ($)",
        "Cost Heavy": "Cost Heavy?"
    }
)

fig1.update_layout(
    xaxis_tickprefix="$",
    yaxis_tickprefix="$",
    legend_title_text="Cost Heavy"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# PRICING ISSUE PRODUCTS
# -----------------------------
st.subheader("⚠️ Pricing Inefficiency (High Sales but Low Profit)")

pricing_issue = cost_df[cost_df["Pricing Issue"] == True]

if pricing_issue.empty:
    st.info("No pricing inefficiency products found with current filters.")
else:
    st.dataframe(pricing_issue)

st.markdown("---")

# -----------------------------
# COST HEAVY PRODUCTS
# -----------------------------
st.subheader("🚨 Cost Heavy Products")

cost_heavy = cost_df[cost_df["Cost Heavy"] == True]

if cost_heavy.empty:
    st.info("No cost heavy products found with current filters.")
else:
    st.dataframe(cost_heavy)

st.markdown("---")

# -----------------------------
# DISCONTINUE SUGGESTION
# -----------------------------
st.subheader("❌ Products for Discontinuation Review")

discontinue = cost_df[cost_df["Discontinue Review"] == True]

if discontinue.empty:
    st.info("No products flagged for discontinuation with current filters.")
else:
    st.dataframe(discontinue)
