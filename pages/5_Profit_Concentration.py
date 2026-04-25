import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
    pareto_analysis,
    apply_filters
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

st.title("📈 Profit Concentration (Pareto Analysis)")

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
# PARETO ANALYSIS
# -----------------------------
pareto_df = pareto_analysis(filtered_df)

# Top 20 products
pareto_df = pareto_df.head(20)

# -----------------------------
# PARETO CHART
# -----------------------------
st.subheader("📊 Pareto Chart (80/20 Rule)")

fig = go.Figure()

# Profit bars
fig.add_trace(go.Bar(
    x=pareto_df["Product Name"],
    y=pareto_df["Profit"],
    name="Profit",
    marker_color="#4b9eff"
))

# Cumulative % line
fig.add_trace(go.Scatter(
    x=pareto_df["Product Name"],
    y=pareto_df["Cumulative Profit %"],
    name="Cumulative %",
    yaxis="y2",
    line=dict(color="#ff4b4b", width=2),
    mode="lines+markers"
))

# 80% reference line
fig.add_hline(
    y=80,
    line_dash="dash",
    line_color="yellow",
    annotation_text="80% Threshold",
    annotation_position="top left",
    yref="y2"
)

# Layout
fig.update_layout(
    template="plotly_dark",
    xaxis_title="Product",
    yaxis_title="Profit ($)",
    yaxis2=dict(
        title="Cumulative Profit %",
        overlaying="y",
        side="right",
        range=[0, 110]
    ),
    title="Pareto Analysis - Top Profit Contributors",
    showlegend=True,
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# DEPENDENCY INDICATOR
# -----------------------------
st.subheader("⚠️ Profit Dependency Indicator")

top_80 = pareto_df[pareto_df["Cumulative Profit %"] <= 80]
num_products = len(top_80)
total_products = len(pareto_df)

col1, col2 = st.columns(2)

col1.metric(
    "Products contributing 80% Profit",
    f"{num_products} out of {total_products}"
)

col2.metric(
    "Dependency Ratio",
    f"{(num_products / total_products * 100):.1f}%" if total_products > 0 else "N/A"
)

st.markdown("---")

# Risk message
if num_products < (0.3 * total_products):
    st.error("⚠️ High Dependency Risk: Business relies on very few products for most of its profit!")
else:
    st.success("✅ Balanced Profit Distribution across products.")

st.markdown("---")

# -----------------------------
# FULL PARETO TABLE
# -----------------------------
st.subheader("📋 Product Profit Contribution Table")

pareto_df_display = pareto_df[["Product Name", "Sales", "Profit", "Cumulative Profit %"]].copy()
pareto_df_display["Sales"] = pareto_df_display["Sales"].map("${:,.0f}".format)
pareto_df_display["Profit"] = pareto_df_display["Profit"].map("${:,.0f}".format)
pareto_df_display["Cumulative Profit %"] = pareto_df_display["Cumulative Profit %"].map("{:.1f}%".format)

st.dataframe(pareto_df_display, use_container_width=True)
