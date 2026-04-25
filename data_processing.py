import pandas as pd

def load_and_clean_data():

    # =========================
    # LOAD DATA
    # =========================
    df = pd.read_csv("Nassau.csv")

    # =========================
    # STANDARDIZE COLUMN NAMES
    # =========================
    df.columns = df.columns.str.strip()

    # =========================
    # VALIDATION CHECKS
    # =========================

    # Remove rows where Sales is zero or negative
    df = df[df["Sales"] > 0]

    # Remove rows where Cost is negative
    df = df[df["Cost"] >= 0]

    # Remove rows where Gross Profit is missing
    df = df.dropna(subset=["Gross Profit"])

    # =========================
    # HANDLE MISSING VALUES
    # =========================

    # If Units missing → assume 1
    df["Units"] = df["Units"].fillna(1)

    # =========================
    # STANDARDIZE TEXT DATA
    # =========================

    df["Product Name"] = df["Product Name"].str.strip()
    df["Division"] = df["Division"].str.strip()

    # =========================
    # REMOVE DUPLICATES
    # =========================
    df = df.drop_duplicates()

    return df
