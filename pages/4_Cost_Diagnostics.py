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

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e2e8f0;
}

.page-header {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 30px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.kpi-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

.kpi-label {
    font-size: 0.75em;
    color: #94a3b8;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.kpi-value {
    font-size: 2em;
    font-weight: 800;
    color: #38bdf8;
}

.kpi-value-green {
    color: #22c55e;
}

.kpi-value-red {
    color: #ef4444;
}

.section-title {
    font-size: 1.2em;
    font-weight: 700;
    color: #38bdf8;
    margin: 25px 0 12px;
    border-left: 4px solid #38bdf8;
    padding-left: 10px;
}

.info-box {
    background: rgba(56,189,248,0.08);
    border-left: 4px solid #38bdf8;
    padding: 15px;
    border-radius: 10px;
    color: #cbd5f5;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="page-header">
    <h1>💰 Cost vs Margin Diagnostics</h1>
    <p>Identify inefficiencies, cost-heavy products, and pricing issues</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔧 Filters")

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
# KPI SUMMARY
# -----------------------------
st.markdown('<div class="section-title">📌 Cost Diagnostics Summary</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Pricing Issues</div>
        <div class="kpi-value-red">{len(cost_df[cost_df["Pricing Issue"] == True])}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Cost Heavy</div>
        <div class="kpi-value">{len(cost_df[cost_df["Cost Heavy"] == True])}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Discontinue Review</div>
        <div class="kpi-value-green">{len(cost_df[cost_df["Discontinue Review"] == True])}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# SCATTER PLOT
# -----------------------------
st.markdown('<div class="section-title">📊 Cost vs Sales Analysis</div>', unsafe_allow_html=True)

fig1 = px.scatter(
    filtered_df,
    x="Cost",
    y="Sales",
    color="Division",
    size="Profit",
    hover_data=["Product Name"],
    template="plotly_dark"
)

fig1.update_traces(marker=dict(opacity=0.7))
fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# INSIGHT
# -----------------------------
if not cost_df.empty:
    worst = cost_df.sort_values(by="Profit").iloc[0]

    st.markdown(f"""
    <div class="info-box">
    ⚠️ <b>Insight:</b> <b>{worst['Product Name']}</b> is generating low profit. 
    Consider reviewing pricing or reducing cost.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# PRICING ISSUES
# -----------------------------
st.markdown('<div class="section-title">⚠️ Pricing Inefficiency</div>', unsafe_allow_html=True)

pricing_issue = cost_df[cost_df["Pricing Issue"] == True]

if pricing_issue.empty:
    st.info("No pricing inefficiency found.")
else:
    st.dataframe(
        pricing_issue.sort_values(by="Sales", ascending=False),
        use_container_width=True,
        height=300
    )

st.markdown("---")

# -----------------------------
# COST HEAVY
# -----------------------------
st.markdown('<div class="section-title">🚨 Cost Heavy Products</div>', unsafe_allow_html=True)

cost_heavy = cost_df[cost_df["Cost Heavy"] == True]

if cost_heavy.empty:
    st.info("No cost heavy products.")
else:
    st.dataframe(
        cost_heavy.sort_values(by="Cost Ratio", ascending=False),
        use_container_width=True,
        height=300
    )

st.markdown("---")

# -----------------------------
# DISCONTINUE
# -----------------------------
st.markdown('<div class="section-title">❌ Discontinue Review</div>', unsafe_allow_html=True)

discontinue = cost_df[cost_df["Discontinue Review"] == True]

if discontinue.empty:
    st.info("No products flagged for discontinuation.")
else:
    st.dataframe(
        discontinue.sort_values(by="Profit"),
        use_container_width=True,
        height=300
    )
