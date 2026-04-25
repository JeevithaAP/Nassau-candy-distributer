import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Overview Dashboard")

# Load data
df = pd.read_csv("Nassau.csv")
df.columns = df.columns.str.strip()

# Basic cleaning
df = df[df["Sales"] > 0]

# KPIs
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = (df["Gross Profit"].sum() / df["Sales"].sum()) * 100

# KPI display
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.0f}")
col3.metric("Avg Margin %", f"{avg_margin:.2f}")

# =========================
# SALES BY DIVISION
# =========================
st.subheader("🏢 Sales by Division")

division_sales = df.groupby("Division")["Sales"].sum().reset_index()

fig1 = px.bar(
    division_sales,
    x="Division",
    y="Sales",
    color="Division"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# PROFIT DISTRIBUTION
# =========================
st.subheader("📈 Profit Distribution")

fig2 = px.histogram(
    df,
    x="Gross Profit",
    nbins=30
)

st.plotly_chart(fig2, use_container_width=True)
