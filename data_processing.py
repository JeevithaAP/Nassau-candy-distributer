import pandas as pd


# ===============================
# STEP 1: LOAD + CLEAN DATA
# ===============================
def load_and_clean_data():

    # Load dataset
    df = pd.read_csv("Nassau.csv")

    # -------------------------------
    # CLEANING
    # -------------------------------

    # Remove rows where Sales or Cost is missing
    df = df.dropna(subset=["Sales", "Cost"])

    # Remove invalid rows (zero or negative values)
    df = df[df["Sales"] > 0]
    df = df[df["Units"] > 0]

    # Fill missing cost with 0 (safe fallback)
    df["Cost"] = df["Cost"].fillna(0)

    # Standardize text columns (important for grouping)
    df["Product Name"] = df["Product Name"].str.strip()
    df["Division"] = df["Division"].str.strip()

    return df


# ===============================
# STEP 2: CALCULATE METRICS
# ===============================
def calculate_metrics(df):

    # -------------------------------
    # BASIC PROFIT
    # -------------------------------
    df["Profit"] = df["Sales"] - df["Cost"]

    # -------------------------------
    # GROSS MARGIN %
    # -------------------------------
    df["Gross Margin %"] = (df["Profit"] / df["Sales"]) * 100
    df["Gross Margin %"] = df["Gross Margin %"].fillna(0)

    # -------------------------------
    # PER UNIT METRICS
    # -------------------------------
    df["Cost per Unit"] = df["Cost"] / df["Units"]
    df["Profit per Unit"] = df["Profit"] / df["Units"]

    df["Cost per Unit"] = df["Cost per Unit"].fillna(0)
    df["Profit per Unit"] = df["Profit per Unit"].fillna(0)

    # -------------------------------
    # CONTRIBUTION ANALYSIS
    # -------------------------------
    total_profit = df["Profit"].sum()
    total_sales = df["Sales"].sum()

    df["Profit Contribution %"] = (df["Profit"] / total_profit) * 100
    df["Revenue Contribution %"] = (df["Sales"] / total_sales) * 100

    df["Profit Contribution %"] = df["Profit Contribution %"].fillna(0)
    df["Revenue Contribution %"] = df["Revenue Contribution %"].fillna(0)

    return df

# ===============================
# STEP 3: PRODUCT LEVEL ANALYSIS
# ===============================
def product_level_analysis(df):

    # -------------------------------
    # GROUP BY PRODUCT
    # -------------------------------
    product_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum"
    }).reset_index()

    # -------------------------------
    # CALCULATE MARGIN %
    # -------------------------------
    product_df["Gross Margin %"] = (product_df["Profit"] / product_df["Sales"]) * 100
    product_df["Gross Margin %"] = product_df["Gross Margin %"].fillna(0)

    # -------------------------------
    # RANKING
    # -------------------------------
    product_df = product_df.sort_values(by="Profit", ascending=False)

    # -------------------------------
    # CLASSIFICATION LOGIC
    # -------------------------------
    # Define thresholds (simple and effective for viva)
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
# STEP 5: PROFIT CONCENTRATION (PARETO)
# ==========================================
def pareto_analysis(df):

    # Group data by product
    pareto_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()

    # Sort products by highest profit
    pareto_df = pareto_df.sort_values(by="Profit", ascending=False)

    # -------------------------------
    # CUMULATIVE PROFIT %
    # -------------------------------
    pareto_df["Cumulative Profit"] = pareto_df["Profit"].cumsum()
    total_profit = pareto_df["Profit"].sum()

    if total_profit != 0:
        pareto_df["Cumulative Profit %"] = (pareto_df["Cumulative Profit"] / total_profit) * 100
    else:
        pareto_df["Cumulative Profit %"] = 0

    # -------------------------------
    # CUMULATIVE SALES %
    # -------------------------------
    pareto_df["Cumulative Sales"] = pareto_df["Sales"].cumsum()
    total_sales = pareto_df["Sales"].sum()

    if total_sales != 0:
        pareto_df["Cumulative Sales %"] = (pareto_df["Cumulative Sales"] / total_sales) * 100
    else:
        pareto_df["Cumulative Sales %"] = 0

    # -------------------------------
    # IDENTIFY TOP 80% PRODUCTS
    # -------------------------------
    pareto_df["Top 80% Profit Contributor"] = pareto_df["Cumulative Profit %"] <= 80

    return pareto_df

# ==========================================
# STEP 6: COST STRUCTURE DIAGNOSTICS
# ==========================================
def cost_structure_analysis(df):

    # Group by product
    cost_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum"
    }).reset_index()

    # --------------------------------
    # CALCULATE COST RATIO
    # --------------------------------
    # Cost Ratio = Cost / Sales
    cost_df["Cost Ratio"] = cost_df["Cost"] / cost_df["Sales"]

    # --------------------------------
    # IDENTIFY COST-HEAVY PRODUCTS
    # --------------------------------
    # High cost but low profit
    cost_df["Cost Heavy"] = (cost_df["Cost Ratio"] > 0.7) & (cost_df["Profit"] < cost_df["Profit"].mean())

    # --------------------------------
    # IDENTIFY LOW MARGIN PRODUCTS
    # --------------------------------
    cost_df["Low Margin"] = cost_df["Profit"] < cost_df["Profit"].mean()

    # --------------------------------
    # PRICING INEFFICIENCY
    # --------------------------------
    # High sales but low profit → pricing issue
    cost_df["Pricing Issue"] = (cost_df["Sales"] > cost_df["Sales"].mean()) & (cost_df["Profit"] < cost_df["Profit"].mean())

    # --------------------------------
    # ACTION FLAGS
    # --------------------------------
    cost_df["Needs Repricing"] = cost_df["Pricing Issue"]

    cost_df["Needs Cost Reduction"] = cost_df["Cost Heavy"]

    cost_df["Discontinue Review"] = (cost_df["Sales"] < cost_df["Sales"].mean()) & (cost_df["Profit"] < cost_df["Profit"].mean())

    return cost_df

# ==========================================
# STEP 7: KPI CALCULATIONS
# ==========================================
def calculate_kpis(df):

    kpi = {}

    # --------------------------------
    # BASIC TOTALS
    # --------------------------------
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_units = df["Units"].sum()

    # --------------------------------
    # 1. GROSS MARGIN (%)
    # --------------------------------
    kpi["Gross Margin (%)"] = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # --------------------------------
    # 2. PROFIT PER UNIT
    # --------------------------------
    kpi["Profit per Unit"] = total_profit / total_units if total_units != 0 else 0

    # --------------------------------
    # 3. REVENUE CONTRIBUTION (TOP PRODUCT)
    # --------------------------------
    revenue_by_product = df.groupby("Product Name")["Sales"].sum()
    kpi["Top Product Revenue Contribution (%)"] = (revenue_by_product.max() / total_sales) * 100 if total_sales != 0 else 0

    # --------------------------------
    # 4. PROFIT CONTRIBUTION (TOP PRODUCT)
    # --------------------------------
    profit_by_product = df.groupby("Product Name")["Profit"].sum()
    kpi["Top Product Profit Contribution (%)"] = (profit_by_product.max() / total_profit) * 100 if total_profit != 0 else 0

    # --------------------------------
    # 5. MARGIN VOLATILITY
    # --------------------------------
    # Calculate margin per product
    margin = (df["Profit"] / df["Sales"]).replace([float('inf'), -float('inf')], 0).fillna(0)

    kpi["Margin Volatility"] = margin.std()

    return kpi

# ==========================================
# STEP 8: USER FILTERING FUNCTIONS
# ==========================================
def apply_filters(df, start_date=None, end_date=None, division=None, margin_threshold=None, product_search=None):

    filtered_df = df.copy()

    # --------------------------------
    # DATE RANGE FILTER
    # --------------------------------
    if start_date and end_date:
        filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])
        filtered_df = filtered_df[
            (filtered_df["Order Date"] >= start_date) &
            (filtered_df["Order Date"] <= end_date)
        ]

    # --------------------------------
    # DIVISION FILTER
    # --------------------------------
    if division:
        filtered_df = filtered_df[filtered_df["Division"] == division]

    # --------------------------------
    # MARGIN THRESHOLD FILTER
    # --------------------------------
    if margin_threshold is not None:
        filtered_df["Margin"] = filtered_df["Profit"] / filtered_df["Sales"]
        filtered_df = filtered_df[filtered_df["Margin"] >= margin_threshold]

    # --------------------------------
    # PRODUCT SEARCH
    # --------------------------------
    if product_search:
        filtered_df = filtered_df[
            filtered_df["Product Name"].str.contains(product_search, case=False, na=False)
        ]

    return filtered_df
