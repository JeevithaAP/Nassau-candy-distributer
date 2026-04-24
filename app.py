import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Dashboard", layout="wide")

st.title("🍬 Nassau Candy - Profitability Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Nassau.csv")

# =========================
# DATA CLEANING
# =========================

# Rename columns (remove spaces problem)
df.columns = df.columns.str.strip()

# Remove invalid rows
df = df[df["Sales"] > 0]

# Fill missing values
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

st.sidebar.header("Filters")

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

margin_filter = st.sidebar.slider(
    "Minimum Margin %",
    0, 100, 0
)

filtered_df = df[
    (df["Division"].isin(division)) &
    (df["Gross Margin (%)"] >= margin_filter)
]

# =========================
# KPI CARDS
# =========================

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.0f}")
col3.metric("Avg Margin", f"{df['Gross Margin (%)'].mean():.2f}%")

# =========================
# PRODUCT ANALYSIS
# =========================

st.subheader("📊 Top Products by Profit")

top_products = filtered_df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_products,
    x=top_products.values,
    y=top_products.index,
    orientation='h',
    title="Top 10 Products by Profit"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# DIVISION ANALYSIS
# =========================

st.subheader("🏢 Division Performance")

division_data = filtered_df.groupby("Division").agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

fig2 = px.bar(
    division_data,
    x="Division",
    y=["Sales", "Gross Profit"],
    barmode="group",
    title="Revenue vs Profit by Division"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# COST vs SALES (DIAGNOSTIC)
# =========================

st.subheader("💰 Cost vs Sales Analysis")

fig3 = px.scatter(
    filtered_df,
    x="Cost",
    y="Sales",
    color="Division",
    size="Gross Profit",
    hover_data=["Product Name"],
    title="Cost vs Sales"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# PARETO ANALYSIS
# =========================

st.subheader("📈 Profit Contribution (Pareto)")

pareto = filtered_df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False)
pareto_df = pareto.cumsum() / pareto.sum()

fig4 = px.line(
    pareto_df,
    title="Cumulative Profit Contribution"
)

st.plotly_chart(fig4, use_container_width=True)
