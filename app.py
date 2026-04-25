import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Nassau Dashboard",
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
- **Overview**
- **Product Analysis**
- **Division Performance**
- **Cost Diagnostics**
- **Profit Concentration**

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
st.markdown("Developed for Data Analytics Project")
