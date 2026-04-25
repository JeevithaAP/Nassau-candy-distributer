import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data_processing import (
    load_data,
    calculate_metrics,
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

# Reduce clutter (top 20 products)
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
    name="Profit"
))

# Cumulative line
fig.add_trace(go.Scatter(
    x=pareto_df["Product Name"],
    y=pareto_df["Cumulative Profit %"],
    name="Cumulative %",
    yaxis="y2"
))

# Layout
fig.update_layout(
    template="plotly_dark",
    xaxis_title="Product",
    yaxis_title="Profit",
    yaxis2=dict(
        title="Cumulative %",
        overlaying='y',
        side='right'
    ),
    title="Pareto Analysis (Top Profit Contributors)",
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# DEPENDENCY INDICATOR
# -----------------------------
st.subheader("⚠️ Dependency Indicator")

# Find how many products contribute 80% profit
top_80 = pareto_df[pareto_df["Cumulative Profit %"] <= 80]

num_products = len(top_80)
total_products = len(pareto_df)

st.metric(
    "Products contributing 80% Profit",
    f"{num_products} out of {total_products}"
)

# Risk message
if num_products < (0.3 * total_products):
    st.error("⚠️ High Dependency Risk: Business relies on very few products")
else:
    st.success("✅ Balanced Profit Distribution")
