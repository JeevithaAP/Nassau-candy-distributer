import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Nassau Dashboard", layout="wide")

st.title("🍬 Nassau Candy - Profitability Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Nassau.csv")
df.columns = df.columns.str.strip()

# =========================
# DATA CLEANING
# =========================
df = df[df["Sales"] > 0]
df["Units"] = df["Units"].fillna(1)

# =========================
# KPI CALCULATIONS
# =========================
df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()

df["Revenue Contribution"] = df["Sales"] / total_sales
df["Profit Contribution"] = df["Gross Profit"] / total_profit

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

product_search = st.sidebar.text_input("Search Product")

margin_filter = st.sidebar.slider(
    "Minimum Margin %",
    0, 100, 0
)

filtered_df = df[
    (df["Division"].isin(division)) &
    (df["Gross Margin (%)"] >= margin_filter)
].copy()

if product_search:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(product_search, case=False)
    ]

# =========================
# KPI CARDS
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"{filtered_df['Gross Profit'].sum():,.0f}")
col3.metric("Avg Margin", f"{filtered_df['Gross Margin (%)'].mean():.2f}%")

# =========================
# PRODUCT CLASSIFICATION
# =========================
st.subheader("📊 Product Performance Classification")

filtered_df["Category"] = pd.cut(
    filtered_df["Gross Margin (%)"],
    bins=[-1, 15, 40, 100],
    labels=["Low Profit", "Medium", "High Profit"]
)

fig0 = px.histogram(
    filtered_df,
    x="Category",
    color="Category",
    title="Product Classification by Margin",
    template="plotly_dark"
)

st.plotly_chart(fig0, use_container_width=True)

# =========================
# TOP PRODUCTS
# =========================
st.markdown("### 📊 Top Performing Products")

top_products = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    top_products,
    x="Gross Profit",
    y="Product Name",
    color="Gross Profit",
    color_continuous_scale="greens",
    orientation="h",
    template="plotly_dark"
)

fig1.update_yaxes(categoryorder="total ascending")

fig1.update_layout(
    title="Top 10 Products by Profit",
    height=500,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# DIVISION ANALYSIS
# =========================
st.subheader("🏢 Division Performance")

division_data = filtered_df.groupby("Division").agg({
    "Sales": "sum",
    "Gross Profit": "sum",
    "Gross Margin (%)": "mean"
}).reset_index()

fig2 = px.bar(
    division_data,
    x="Division",
    y="Gross Margin (%)",
    color="Division",
    title="Average Margin by Division",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# COST vs SALES
# =========================
st.subheader("💰 Cost vs Sales Diagnostics")

fig3 = px.scatter(
    filtered_df,
    x="Cost",
    y="Sales",
    color="Division",
    size="Gross Profit",
    hover_data=["Product Name"],
    title="Cost vs Sales Analysis",
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# PARETO ANALYSIS
# =========================
st.subheader("📈 Profit Contribution (Pareto)")

pareto = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
)

pareto_df = (pareto.cumsum() / pareto.sum()).reset_index()
pareto_df.columns = ["Product Name", "Cumulative Profit"]

fig4 = px.line(
    pareto_df,
    x="Product Name",
    y="Cumulative Profit",
    markers=True,
    title="Cumulative Profit Contribution",
    template="plotly_dark"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# MARGIN RISK TABLE
# =========================
st.subheader("⚠️ Low Margin Risk Products")

risk_df = filtered_df[filtered_df["Gross Margin (%)"] < 15][
    ["Product Name", "Sales", "Cost", "Gross Profit", "Gross Margin (%)"]
]

st.dataframe(
    risk_df.sort_values(by="Gross Margin (%)"),
    use_container_width=True
)
