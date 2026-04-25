import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_and_clean_data,
    calculate_metrics,
    calculate_kpis,
    apply_filters
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 Overview Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_and_clean_data()
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
) / 100   # ✅ FIXED SCALE

product_search = st.sidebar.text_input("Search Product")

# Apply filters
filtered_df = apply_filters(
    df,
    division=division,
    margin_threshold=margin_threshold,
    product_search=product_search
)

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📌 Key Performance Indicators")

kpi = calculate_kpis(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"{filtered_df['Profit'].sum():,.0f}")
col3.metric("Avg Margin", f"{kpi['Gross Margin (%)']:.2f}%")

st.markdown("---")

# -----------------------------
# DIVISION PERFORMANCE
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Sales by Division")
    sales_div = filtered_df.groupby("Division")["Sales"].sum().reset_index()

    fig1 = px.bar(sales_div, x="Division", y="Sales", color="Division", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("💰 Profit by Division")
    profit_div = filtered_df.groupby("Division")["Profit"].sum().reset_index()

    fig2 = px.bar(profit_div, x="Division", y="Profit", color="Division", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# PROFIT DISTRIBUTION
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Profit Distribution")
    fig3 = px.histogram(filtered_df, x="Profit", nbins=30, template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(top_products, x="Profit", y="Product Name", orientation="h", template="plotly_dark")
    fig4.update_yaxes(categoryorder="total ascending")

    st.plotly_chart(fig4, use_container_width=True)
