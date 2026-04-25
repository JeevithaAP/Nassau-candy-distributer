import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

st.title("📊 Nassau Candy - Overview Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Nassau.csv")
df.columns = df.columns.str.strip()

# =========================
# CLEANING
# =========================
df = df[df["Sales"] > 0]
df["Units"] = df["Units"].fillna(1)

# =========================
# CALCULATIONS
# =========================
df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"]) * 100

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin (%)"].mean()

# =========================
# KPI CARDS (IMPROVED UI)
# =========================
st.markdown("## 📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
### 💰 Total Sales  
### {total_sales:,.0f}
""")

col2.markdown(f"""
### 📈 Total Profit  
### {total_profit:,.0f}
""")

col3.markdown(f"""
### 📊 Avg Margin  
### {avg_margin:.2f}%
""")

st.markdown("---")

# =========================
# ROW 1: SALES + PROFIT
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Sales by Division")

    sales_data = df.groupby("Division")["Sales"].sum().reset_index()

    fig1 = px.bar(
        sales_data,
        x="Division",
        y="Sales",
        color="Division",
        template="plotly_dark"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("💰 Profit by Division")

    profit_data = df.groupby("Division")["Gross Profit"].sum().reset_index()

    fig2 = px.bar(
        profit_data,
        x="Division",
        y="Gross Profit",
        color="Division",
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =========================
# ROW 2: DISTRIBUTION + TOP PRODUCTS
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Profit Distribution")

    fig3 = px.histogram(
        df,
        x="Gross Profit",
        nbins=30,
        color_discrete_sequence=["#00C9A7"],
        template="plotly_dark"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🏆 Top 10 Products")

    top_products = df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False).head(10)
    top_products = top_products.reset_index()

    fig4 = px.bar(
        top_products,
        x="Gross Profit",
        y="Product Name",
        orientation="h",
        color="Gross Profit",
        template="plotly_dark"
    )

    fig4.update_yaxes(categoryorder="total ascending")

    st.plotly_chart(fig4, use_container_width=True)
