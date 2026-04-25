import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
    apply_filters
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

st.title("🏢 Division Performance Dashboard")

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

# Apply filters
filtered_df = apply_filters(
    df,
    division=division,
    margin_threshold=margin_threshold
)

# -----------------------------
# DIVISION AGGREGATION
# -----------------------------
division_df = filtered_df.groupby("Division").agg({
    "Sales": "sum",
    "Profit": "sum"
}).reset_index()

# Calculate margin
division_df["Margin %"] = (division_df["Profit"] / division_df["Sales"]) * 100
division_df["Margin %"] = division_df["Margin %"].fillna(0)

# -----------------------------
# KPI CARDS
# -----------------------------
st.subheader("📌 Division KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${division_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${division_df['Profit'].sum():,.0f}")
col3.metric("Avg Margin", f"{division_df['Margin %'].mean():.2f}%")

st.markdown("---")

# -----------------------------
# REVENUE vs PROFIT
# -----------------------------
st.subheader("📊 Revenue vs Profit by Division")

fig1 = px.bar(
    division_df,
    x="Division",
    y=["Sales", "Profit"],
    barmode="group",
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# MARGIN DISTRIBUTION
# -----------------------------
st.subheader("📈 Margin Comparison by Division")

fig2 = px.bar(
    division_df,
    x="Division",
    y="Margin %",
    color="Division",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# INSIGHT TABLE
# -----------------------------
st.subheader("📋 Division Summary Table")

if division_df.empty:
    st.info("No data available with current filters.")
else:
    st.dataframe(division_df.sort_values(by="Profit", ascending=False))
