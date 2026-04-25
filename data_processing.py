import pandas as pd


# ===============================
# STEP 1: LOAD + CLEAN DATA
# ===============================
def load_data():

    try:
        df = pd.read_csv("Nassau.csv")
    except Exception as e:
        raise Exception(f"Error loading CSV file: {e}")

    # -------------------------------
    # STANDARDIZE COLUMN NAMES
    # -------------------------------
    df.columns = df.columns.str.strip()

    required_columns = ["Sales", "Cost", "Units", "Product Name", "Division"]

    for col in required_columns:
        if col not in df.columns:
            raise Exception(f"Missing required column: {col}")

    # -------------------------------
    # CLEANING
    # -------------------------------
    df = df.dropna(subset=["Sales", "Cost"])
    df = df[df["Sales"] > 0]
    df = df[df["Units"] > 0]

    df["Cost"] = df["Cost"].fillna(0)

    df["Product Name"] = df["Product Name"].astype(str).str.strip()
    df["Division"] = df["Division"].astype(str).str.strip()

    return df


# ===============================
# STEP 2: CALCULATE METRICS
# ===============================
def calculate_metrics(df):

    df["Profit"] = df["Sales"] - df["Cost"]

    df["Gross Margin %"] = (df["Profit"] / df["Sales"]).replace([float('inf'), -float('inf')], 0) * 100
    df["Gross Margin %"] = df["Gross Margin %"].fillna(0)

    df["Cost per Unit"] = (df["Cost"] / df["Units"]).replace([float('inf'), -float('inf')], 0)
    df["Profit per Unit"] = (df["Profit"] / df["Units"]).replace([float('inf'), -float('inf')], 0)

    df["Cost per Unit"] = df["Cost per Unit"].fillna(0)
    df["Profit per Unit"] = df["Profit per Unit"].fillna(0)

    total_profit = df["Profit"].sum()
    total_sales = df["Sales"].sum()

    df["Profit Contribution %"] = (df["Profit"] / total_profit * 100) if total_profit != 0 else 0
    df["Revenue Contribution %"] = (df["Sales"] / total_sales * 100) if total_sales != 0 else 0

    df["Profit Contribution %"] = df["Profit Contribution %"].fillna(0)
    df["Revenue Contribution %"] = df["Revenue Contribution %"].fillna(0)

    return df


# ===============================
# STEP 3: PRODUCT LEVEL ANALYSIS
# ===============================
def product_level_analysis(df):

    product_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum"
    }).reset_index()

    product_df["Gross Margin %"] = (product_df["Profit"] / product_df["Sales"]).replace([float('inf'), -float('inf')], 0) * 100
    product_df["Gross Margin %"] = product_df["Gross Margin %"].fillna(0)

    product_df = product_df.sort_values(by="Profit", ascending=False)

    profit_threshold = product_df["Profit"].quantile(0.7)
    margin_threshold = product_df["Gross Margin %"].quantile(0.7)
    low_sales_threshold = product_df["Sales"].quantile(0.3)

    def classify(row):
        if row["Profit"] >= profit_threshold and row["Gross Margin %"] >= margin_threshold:
            return "High Profit & High Margin"
        elif row["Sales"] >= product_df["Sales"].quantile(0.7) and row["Gross Margin %"] < margin_threshold:
            return "High Sales but Low Margin"
        elif row["Sales"] <= low_sales_threshold and row["Profit"] <= product_df["Profit"].quantile(0.3):
            return "Low Sales & Low Profit"
        else:
            return "Average"

    product_df["Category"] = product_df.apply(classify, axis=1)

    return product_df


# ==========================================
# STEP 4: DIVISION PERFORMANCE
# ==========================================
def division_performance(df):

    division_df = df.groupby("Division").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()

    division_df["Margin %"] = (division_df["Profit"] / division_df["Sales"]).replace([float('inf'), -float('inf')], 0) * 100
    division_df["Margin %"] = division_df["Margin %"].fillna(0)

    return division_df


# ==========================================
# STEP 5: PARETO ANALYSIS
# ==========================================
def pareto_analysis(df):

    pareto_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()

    pareto_df = pareto_df.sort_values(by="Profit", ascending=False)

    pareto_df["Cumulative Profit"] = pareto_df["Profit"].cumsum()
    total_profit = pareto_df["Profit"].sum()

    pareto_df["Cumulative Profit %"] = (pareto_df["Cumulative Profit"] / total_profit * 100) if total_profit != 0 else 0

    pareto_df["Cumulative Sales"] = pareto_df["Sales"].cumsum()
    total_sales = pareto_df["Sales"].sum()

    pareto_df["Cumulative Sales %"] = (pareto_df["Cumulative Sales"] / total_sales * 100) if total_sales != 0 else 0

    pareto_df["Top 80% Profit Contributor"] = pareto_df["Cumulative Profit %"] <= 80

    return pareto_df


# ==========================================
# STEP 6: COST STRUCTURE
# ==========================================
def cost_structure_analysis(df):

    cost_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum"
    }).reset_index()

    cost_df["Cost Ratio"] = (cost_df["Cost"] / cost_df["Sales"]).replace([float('inf'), -float('inf')], 0)

    cost_df["Cost Heavy"] = (cost_df["Cost Ratio"] > 0.7) & (cost_df["Profit"] < cost_df["Profit"].mean())
    cost_df["Low Margin"] = cost_df["Profit"] < cost_df["Profit"].mean()
    cost_df["Pricing Issue"] = (cost_df["Sales"] > cost_df["Sales"].mean()) & (cost_df["Profit"] < cost_df["Profit"].mean())

    cost_df["Needs Repricing"] = cost_df["Pricing Issue"]
    cost_df["Needs Cost Reduction"] = cost_df["Cost Heavy"]
    cost_df["Discontinue Review"] = (cost_df["Sales"] < cost_df["Sales"].mean()) & (cost_df["Profit"] < cost_df["Profit"].mean())

    return cost_df


# ==========================================
# STEP 7: KPI CALCULATIONS
# ==========================================
def calculate_kpis(df):

    kpi = {}

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_units = df["Units"].sum()

    kpi["Gross Margin (%)"] = (total_profit / total_sales * 100) if total_sales != 0 else 0
    kpi["Profit per Unit"] = (total_profit / total_units) if total_units != 0 else 0

    revenue_by_product = df.groupby("Product Name")["Sales"].sum()
    kpi["Top Product Revenue Contribution (%)"] = (revenue_by_product.max() / total_sales * 100) if total_sales != 0 else 0

    profit_by_product = df.groupby("Product Name")["Profit"].sum()
    kpi["Top Product Profit Contribution (%)"] = (profit_by_product.max() / total_profit * 100) if total_profit != 0 else 0

    margin = (df["Profit"] / df["Sales"]).replace([float('inf'), -float('inf')], 0).fillna(0)
    kpi["Margin Volatility"] = margin.std()

    return kpi


# ==========================================
# STEP 8: FILTERS
# ==========================================
def apply_filters(df, start_date=None, end_date=None, division=None, margin_threshold=None, product_search=None):

    filtered_df = df.copy()

    # DATE FILTER (SAFE)
    if start_date and end_date and "Order Date" in filtered_df.columns:
        filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"], errors='coerce')
        filtered_df = filtered_df[
            (filtered_df["Order Date"] >= start_date) &
            (filtered_df["Order Date"] <= end_date)
        ]

    # DIVISION
    if division:
        filtered_df = filtered_df[filtered_df["Division"] == division]

    # MARGIN FILTER
    if margin_threshold is not None:
        filtered_df["Margin"] = (filtered_df["Profit"] / filtered_df["Sales"]).replace([float('inf'), -float('inf')], 0)
        filtered_df = filtered_df[filtered_df["Margin"] >= margin_threshold]

    # PRODUCT SEARCH
    if product_search:
        filtered_df = filtered_df[
            filtered_df["Product Name"].str.contains(product_search, case=False, na=False)
        ]

    return filtered_df
