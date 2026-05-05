🍬 Nassau Candy Distributor
Product Line Profitability & Margin Performance Analysis

📌 Project Overview
This project is a data analytics dashboard built for Nassau Candy Distributor to analyze their product line profitability and margin performance. The dashboard helps the company identify which products are truly generating profit, which divisions are underperforming, and where pricing or cost improvements are needed.

❓ Problem Statement
Nassau Candy Distributor lacked visibility into:
Which products deliver the highest gross margin
Whether high-sales products are actually profitable
How profitability varies across product divisions
Which products represent margin risk

📁 Dataset
File: Nassau.csv
Divisions: Chocolate, Sugar, Other
Products: 15 unique candy products
Factories: 5 manufacturing factories
Fields: Order ID, Product Name, Division, Sales, Cost, Units, Gross Profit

🚀 Technologies Used
Python — Programming language
Pandas — Data processing and analysis
Plotly — Interactive charts and visualizations
Streamlit — Web dashboard application

📊 Dashboard Pages
Page
Description
📊 Overview
Overall KPIs — Total Sales, Profit, Margin
🏆 Product Analysis
Product level profitability and classification
🏢 Division Performance
Revenue vs Profit by division
💰 Cost Diagnostics
Cost heavy and pricing inefficiency products
📈 Profit Concentration
Pareto 80/20 analysis
⚙️ Project Structure
Nassau-candy-distributer/
│
├── app.py                          # Landing page
├── data_processing.py              # Backend data processing
├── Nassau.csv                      # Dataset
├── requirements.txt                # Dependencies
│
└── pages/
    ├── 1_overview.py               # Overview Dashboard
    ├── 2_product_Analysis.py       # Product Analysis
    ├── 3_division_performance.py   # Division Performance
    ├── 4_Cost_Diagnostics.py       # Cost Diagnostics
    └── 5_Profit_Concentration.py   # Profit Concentration
📈 Key Findings
Chocolate division is the top profit driver
Only 4 out of 15 products contribute 80% of total profit
Wonka Bar products dominate top profit positions
Some products have high sales but low margin — need repricing
Few products flagged for discontinuation review
▶️ How to Run
Clone the repository
git clone https://github.com/JeevithaAP/Nassau-candy-distributer.git
Install dependencies
pip install -r requirements.txt
Run the app
streamlit run app.py
👩‍💻 Developed By
Jeevitha AP — Data Analytics Project 2025
