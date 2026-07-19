import streamlit as st
import pandas as pd
from utils import db

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("📈 Nifty100 Stock Screener")

# -------------------------------
# Load Data
# -------------------------------
years = db.get_available_years()

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

df = db.get_screener_data(selected_year)
# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

roe_min = st.sidebar.slider(
    "ROE Min",
    0.0,
    100.0,
    10.0
)

de_max = st.sidebar.slider(
    "Debt/Equity Max",
    0.0,
    5.0,
    2.0
)

pe_max = st.sidebar.slider(
    "PE Max",
    0.0,
    100.0,
    50.0
)

fcf_min = st.sidebar.slider(
    "FCF Min",
    float(df["free_cash_flow_cr"].fillna(0).min()),
    float(df["free_cash_flow_cr"].fillna(0).max()),
    0.0
)

# -------------------------------
# Apply Filters
# -------------------------------
filtered = df[
    (df["return_on_equity_pct"].fillna(0) >= roe_min)
    &
    (df["debt_to_equity"].fillna(0) <= de_max)
]

if "pe_ratio" in filtered.columns:
    filtered = filtered[
        filtered["pe_ratio"].fillna(0) <= pe_max
    ]

if "free_cash_flow_cr" in filtered.columns:
    filtered = filtered[
        filtered["free_cash_flow_cr"].fillna(0) >= fcf_min
    ]

# -------------------------------
# Result Count
# -------------------------------
st.subheader(
    f"Companies Found: {len(filtered)}"
)

# -------------------------------
# Display Table
# -------------------------------
st.dataframe(
    filtered,
    use_container_width=True
)

# -------------------------------
# CSV Download
# -------------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="screener_results.csv",
    mime="text/csv"
)