import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Nassau Candy Dashboard",
    page_icon="🍬",
    layout="wide"
)

# =========================
# MAIN TITLE
# =========================
st.title("🍬 Nassau Candy - Profitability Dashboard")

# =========================
# INTRO / LANDING PAGE
# =========================
st.markdown("""
Welcome to the **Product Line Profitability & Margin Performance Dashboard**.

### 📊 What this app provides:
- Product profitability insights
- Division-wise performance analysis
- Cost vs margin diagnostics
- Profit concentration (Pareto analysis)

---

### 📂 Navigate using the sidebar:
- **1 - Overview**
- **2 - Product Analysis**
- **3 - Division Performance**
- **4 - Cost Diagnostics**
- **5 - Profit Concentration**

---

### ⚙️ Backend Processing:
All data cleaning, KPI calculations, and analytics logic are handled in:
`data_processing.py`

---

### 🚀 Built Using:
- Streamlit
- Pandas
- Plotly
""")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("Developed for Data Analytics Project | Nassau Candy Distributor")
