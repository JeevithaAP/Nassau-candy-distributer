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
# CUSTOM CSS
# =========================
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 0;
    }

    .sub-title {
        text-align: center;
        font-size: 1.2em;
        color: #cccccc;
        margin-bottom: 30px;
    }

    /* Feature cards */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(255, 210, 0, 0.2);
    }

    .card-icon {
        font-size: 2em;
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 1.1em;
        font-weight: 700;
        color: #ffd200;
        margin-bottom: 6px;
    }

    .card-desc {
        font-size: 0.9em;
        color: #aaaaaa;
    }

    /* Navigation cards */
    .nav-card {
        background: linear-gradient(135deg, rgba(247,151,30,0.15), rgba(255,210,0,0.05));
        border: 1px solid rgba(247,151,30,0.3);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 6px 0;
        color: #ffd200;
        font-weight: 600;
        font-size: 1em;
    }

    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #ffd200, transparent);
        margin: 30px 0;
        border: none;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.85em;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }

    /* Badge */
    .badge {
        display: inline-block;
        background: rgba(255, 210, 0, 0.15);
        border: 1px solid #ffd200;
        color: #ffd200;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.8em;
        margin: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown('<div class="main-title">🍬 Nassau Candy Distributor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Product Line Profitability & Margin Performance Dashboard</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# =========================
# FEATURE CARDS
# =========================
st.markdown("### 📊 What This Dashboard Provides")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🏆</div>
        <div class="card-title">Product Profitability</div>
        <div class="card-desc">Identify top and bottom performing products by profit and margin</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🏢</div>
        <div class="card-title">Division Performance</div>
        <div class="card-desc">Compare revenue vs profit across all product divisions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">💰</div>
        <div class="card-title">Cost Diagnostics</div>
        <div class="card-desc">Spot pricing inefficiencies and cost-heavy products</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📈</div>
        <div class="card-title">Pareto Analysis</div>
        <div class="card-desc">Discover which few products drive 80% of total profit</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# =========================
# NAVIGATION SECTION
# =========================
st.markdown("### 📂 Navigate Using the Sidebar")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="nav-card">📊 1 — Overview Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card">🏆 2 — Product Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card">🏢 3 — Division Performance</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="nav-card">💰 4 — Cost Diagnostics</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card">📈 5 — Profit Concentration</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# =========================
# BUILT WITH SECTION
# =========================
st.markdown("### 🚀 Built With")

st.markdown("""
<span class="badge">🐍 Python</span>
<span class="badge">📊 Streamlit</span>
<span class="badge">🐼 Pandas</span>
<span class="badge">📉 Plotly</span>
""", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    Developed for Data Analytics Project &nbsp;|&nbsp; Nassau Candy Distributor &nbsp;|&nbsp; 2025
</div>
""", unsafe_allow_html=True)
