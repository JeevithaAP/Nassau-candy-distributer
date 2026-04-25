import streamlit as st
import pandas as pd
import plotly.express as px

from data_processing import (
    load_data,
    calculate_metrics,
    product_level_analysis,
    apply_filters
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

st.title("🏆 Product Analysis Dashboard")

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
# PRODUCT LEVEL ANALYSIS
# -----------------------------
product_df = product_level_analysis(filtered_df)

# -----------------------------
# TOP PRODUCTS BY PROFIT
# -----------------------------
st.subheader("🏆 Top 10 Products by Profit")

top_profit = product_df.head(10)

fig1 = px.bar(
    top_profit,
    x="Profit",
    y="Product Name",
    orientation="h",
    color="Profit",
    template="plotly_dark"
)

fig1.update_yaxes(categoryorder="total ascending")

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# TOP PRODUCTS BY MARGIN
# -----------------------------
st.subheader("📈 Top Products by Margin")

top_margin = product_df.sort_values(by="Gross Margin %", ascending=False).head(10)

fig2 = px.bar(
    top_margin,
    x="Gross Margin %",
    y="Product Name",
    orientation="h",
    color="Gross Margin %",
    template="plotly_dark"
)

fig2.update_yaxes(categoryorder="total ascending")

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# PRODUCT CLASSIFICATION
# -----------------------------
st.subheader("📊 Product Performance Classification")

fig3 = px.histogram(
    product_df,
    x="Category",
    color="Category",
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# -----------------------------
# HIGH SALES BUT LOW MARGIN
# -----------------------------
st.subheader("⚠️ High Sales but Low Margin Products")

problem_products = product_df[
    product_df["Category"] == "High Sales but Low Margin"
]

st.dataframe(problem_products)
